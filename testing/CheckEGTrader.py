import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import time
from strategies.BaseEG import BaseEG
from utils.work_dfs.load_df import simple_load_df
from utils.work_dfs.convert_tf import convert_timeframe
from utils.work_dfs.other import get_price_step
from utils.drawing.chart import draw_hb_chart_fast

def duration_time(func):
    def wrapper(self, *args, **kwargs):
        if self.measure_time:
            start = time()
            print('start', func.__name__)
            result = func(self, *args, **kwargs)
            print('Time:', time() - start)
        else:
            result = func(self, *args, **kwargs)
        return result
    return wrapper

#добавить учет риск-менеджмента
class CheckWSTrader:
    def __init__(self,
                 df:pd.DataFrame | str, 
                 ws:list|tuple|BaseEG,
                 fee:float = 0.001,
                 symbol:str = 'Test',
                 tf:str = '5m',
                 close_on_time:bool=True,
                 close_map:tuple|list=(
                     (22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30),),
                 measure_time:bool=False,
                 use_tqdm:bool=False
                 ):
        self.symbol = symbol
        self.tf = tf
        self.reload_data()
        if isinstance(df,str):
            path_df = df
            self.df = simple_load_df(path_df)
        else:
            self.df = df.copy()
        self.price_step = get_price_step(self.df)
        if isinstance(ws,tuple) or isinstance(ws,list):
            # self.ws = ws[0](self.symbol,self.tf,'e',1,*ws[1])
            self.ws = ws[0](self.symbol,self.price_step,1,*ws[1])
        else:
            self.ws = ws
        self.fee = fee
        self.fee_one_p = fee  * 100
        self.close_on_time = close_on_time
        self.close_map = close_map
        self.actions = (None,'open_long','open_short','close_long','close_short','close_all')
        self.actions_dict = {action: idx for idx, action in enumerate(self.actions)}
        self.measure_time = measure_time
        self.use_tqdm = use_tqdm
        self.df = self.add_time_features(self.df)
        self.days = 0

    def reload_data(self):
        self.trade_data = {
            'total':0,
            'count':0, #количество разворотов
            'fees': 0, #комиссия в абсолютных
            'total_wfees_per':0, #прибыль в процентах с учетом комиссии TODO проверить правильность рассчетов
            'equity':[0], #динамика дохода
            'equity_fee':[0], #динамика дохода с комиссией
            'step_eq_fee':[0], #equity каждый шаг
            'unclosed_fee':[0], #equity незакрытый каждый шаг
            'step_eq_vtb':[0], #equity каждый шаг
            'unclosed_vtb':[0], #equity незакрытый каждый шаг
            'pos':0, #текущая позиция
            'hist_pos':[0],
            'open_price':0, #текущая цена
            'o_longs':[], #входы в лонг
            'o_shorts':[], #входы в шорт
            'c_longs':[], #закрытие лонгов
            'c_shorts':[], #закрытие шортов 
            'c_risks':[], #закрытие по риск менеджменту
        }
        self.open_fee = 0
        self.cur_wday = None
        self.cur_eq = None
        self.first_risk = True
        self.last_c_risk = None
        self.days = 0

    def get_iterator(self,data):
        if self.use_tqdm:
            return tqdm(data)
        return data
    
    def open_pos(self,price,feei):
        self.trade_data['open_price']= price
        self.trade_data['fees'] += feei
        self.open_fee = feei
        self.trade_data['total_wfees_per'] -= self.fee_one_p # комиссия за открытие
        self.trade_data['count'] += 1
    
    def open_long(self,price,feei,row_name):
        self.open_pos(price,feei)
        self.trade_data['o_longs'].append((row_name,price))
        self.trade_data['pos'] = 1

    def open_short(self,price,feei,row_name):
        self.open_pos(price,feei)
        self.trade_data['o_shorts'].append((row_name,price))
        self.trade_data['pos'] = -1

    def close_pos(self,price,feei,delta):
        self.trade_data['total'] += delta
        self.trade_data['total_wfees_per'] += ((delta  / price) * 100) - self.fee_one_p  # комиссия за закрытие
        self.trade_data['fees'] += feei
        self.trade_data['equity'].append(self.trade_data['equity'][-1] + delta)
        self.trade_data['equity_fee'].append(self.trade_data['equity_fee'][-1] + delta - feei - self.open_fee)
        self.open_fee = 0

    def close_long(self,price,feei,row_name):
        delta = price - self.trade_data['open_price']  # прибыль по лонгу (как при action=3)
        self.close_pos(price,feei,delta)
        self.trade_data['c_longs'].append((row_name,price))
        self.trade_data['pos'] = 0
    
    def close_short(self,price,feei,row_name):
        delta = self.trade_data['open_price'] - price  # прибыль по шорту (как при action=4)
        self.close_pos(price,feei,delta)
        self.trade_data['c_shorts'].append((row_name,price))
        self.trade_data['pos'] = 0

    def work_action(self,signal, price, row_name):
        """return pos,open_price,fees,open_fee"""
        # actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
        feei = self.fee * price  # fee абсолютное значение
        # print(feei)
        if signal == 1:  # long
            if self.trade_data['pos'] != 1:
                if self.trade_data['pos'] < 0: # был шорт, закрываем его и открываем лонг
                    self.close_short(price,feei,row_name)
                self.open_long(price,feei,row_name)
        elif signal == 2:  # short
            if self.trade_data['pos'] != -1:
                if self.trade_data['pos'] > 0:
                    self.close_long(price,feei,row_name)
                self.open_short(price,feei,row_name)  
        elif signal == 3:  # close long
            if self.trade_data['pos'] == 1:
                self.close_long(price,feei,row_name)
        elif signal == 4:  # close short
            if self.trade_data['pos'] == -1:
                self.close_short(price,feei,row_name)
        elif signal == 5:
            if self.trade_data['pos'] == 1:
                self.close_long(price,feei,row_name)
            elif self.trade_data['pos'] == -1:
                self.close_short(price,feei,row_name)

    def add_time_features(self,df):
        df = df.copy()
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['hour'] = df['ms'].dt.hour
        df['minute'] = df['ms'].dt.minute
        df['weekday'] = df['ms'].dt.weekday
        return df

    def update_step_data(self,price):
        self.trade_data['step_eq_fee'].append(self.trade_data['equity_fee'][-1])
        # self.trade_data['step_eq_vtb'].append(self.vtb_fee_func(self.trade_data['equity'][-1],0)-self.trade_data['count']*2)
        self.trade_data['step_eq_vtb'].append(self.vtb_fee_func(self.trade_data['equity'][-1],self.trade_data['count']))
        self.trade_data['hist_pos'].append(self.trade_data['pos'])
        if self.trade_data['pos'] > 0:
            unclosed_profit = price - self.trade_data['open_price']
        elif self.trade_data['pos'] < 0:
            unclosed_profit = self.trade_data['open_price'] - price
        else:
            unclosed_profit = 0
        self.trade_data['unclosed_fee'].append(self.trade_data['step_eq_fee'][-1] + unclosed_profit)
        self.trade_data['unclosed_vtb'].append(self.trade_data['step_eq_vtb'][-1] + self.vtb_fee_func(unclosed_profit,0))

    def check_risk(self,weekday,row_name,price,vtb=True):
        if self.cur_wday != weekday:
            self.days += 1
            self.cur_wday = weekday
        if self.stop_risk:
            eq = self.trade_data['unclosed_vtb'][-1] if vtb else self.trade_data['unclosed_fee'][-1]
            if self.cur_wday != weekday:
                self.cur_wday = weekday
                self.cur_eq = eq
                if not self.first_risk:
                    self.trade_data['c_risks'][-1] += self.last_c_risk
                    self.last_c_risk = None
                    self.first_risk = True
            else:
                if self.first_risk:
                    delta = eq - self.cur_eq
                    if delta < self.stop_risk:
                        self.first_risk = False
                        self.trade_data['c_risks'].append([row_name,price])
                        self.last_c_risk = [row_name,price]
                        return False
                else:
                    self.last_c_risk = [row_name,price]
                    return False
        return True
    
    # CHECKS_FUNCS
    @duration_time
    def check_strategy_fast(self, vtb=True):
        self.reload_data()
        df = self.ws.preprocessing(self.df.copy())
        
        # ПРЕДВЫЧИСЛИТЬ все сигналы разом
        df['action'] = df.apply(lambda row: self.ws(row), axis=1)
        
        if self.close_on_time:
            # Оптимизированная проверка времени
            mask = (df['hour'] >= df['weekday'].map(lambda wd: self.close_map[wd][0])) & \
                (df['minute'] >= df['weekday'].map(lambda wd: self.close_map[wd][1]))
            df.loc[mask, 'action'] = 'close_all_pw'
        
        # Преобразуем в массив индексов
        signals = df['action'].map(self.actions_dict).values
        prices = df['close'].values
        row_names = df['x'].values
        weekdays = df['weekday'].values if 'weekday' in df.columns else None
        
        # Основной цикл - теперь быстрый
        for i in self.get_iterator(range(len(df))):
            signal = signals[i]
            price = prices[i]
            row_name = row_names[i]
            
            # check_risk тоже нужно предвычислить или оптимизировать
            if not self.check_risk(weekdays[i] if weekdays is not None else 0, 
                                row_name, price, vtb):
                signal = self.actions_dict['close_all_pw']
            
            self.work_action(signal, price, row_name)
            self.update_step_data(price)

    @duration_time
    def check_strategy_window(self,window=150, normalization=False,vtb=True):
        """
        оконная версия
        """
        self.reload_data()
        price = None
        for i in self.get_iterator(range(len(self.df))):
            if i > window:
                df_slice = self.df.iloc[i-window:i].copy()
                row = df_slice.iloc[-1]
                price = row['close']
                row_name = row['x']
                
                if normalization:
                    candel_max = df_slice['high'].max()
                    df_norm = df_slice.copy()
                    df_norm['volume'] = df_norm['volume'] / df_norm['volume'].max()
                    df_norm['close'] = df_norm['close'] / candel_max
                    df_norm['open'] = df_norm['open'] / candel_max
                    df_norm['low'] = df_norm['low'] / candel_max
                    df_norm['high'] = df_norm['high'] / candel_max
                    row = self.ws.get_test_row(df_norm)
                else:
                    row = self.ws.get_test_row(df_slice)
                action = self.ws(row)
                if self.close_on_time:
                    time_close = self.close_map[row['weekday']]
                    if row['hour'] >= time_close[0] and row['minute'] >= time_close[1]:
                        action = 'close_all_pw'
                action = action if self.check_risk(row['weekday'],row_name,price,vtb) else 'close_all_pw'
                signal = self.actions_dict.get(action, None)
                self.work_action(signal, price, row_name)
            self.update_step_data(price)

    # POST_PROCESS_RESULT_FUNCS
    def process_old_type_result(self):
        df_eq = pd.DataFrame({'eq':self.trade_data['equity'],'eq_fee':self.trade_data['equity_fee']})
        trades = {'total': self.trade_data['total'], 'count': self.trade_data['count'], 'total_fee_per': self.trade_data['total_wfees_per']}
        if df_eq.empty:
            trades.update({
            'total_abs_fee': 0,
            'win_rate_wf': 0,
            'total_fee': self.trade_data['fees'],
            'mean_eq':0,
            'median_eq':0,
            'max_eq':0,
            'min_eq':0,
            'balance_eq':0,
            'mean_eqf':0,
            'median_eqf':0,
            'max_eqf':0,
            'min_eqf':0,
            'balance_eqf':0
            })
        else:
            df_eq['diff_eq'] = df_eq['eq'].diff()
            df_eq['diff_eq_fee'] = df_eq['eq_fee'].diff()
            mean_eq = df_eq['diff_eq'].mean()
            median_eq = df_eq['diff_eq'].median()
            min_eq = df_eq['diff_eq'].min()
            max_eq = df_eq['diff_eq'].max()
            mean_eqf = df_eq['diff_eq_fee'].mean()
            median_eqf = df_eq['diff_eq_fee'].median()
            min_eqf = df_eq['diff_eq_fee'].min()
            max_eqf = df_eq['diff_eq_fee'].max()
            wins = len(df_eq[df_eq['diff_eq'] > 0].index)
            loss = len(df_eq[df_eq['diff_eq'] < 0].index)
            if loss > 0:
                win_rate = round((wins / (wins + loss)) * 100,2)
            else:
                win_rate = 0

            trades['total_fee_per'] = round(self.trade_data['total_wfees_per'],2)
            trades.update({
                'total_abs_fee': self.trade_data['equity_fee'][-1],
                'win_rate_wf': win_rate,
                'total_fee': self.trade_data['fees'],
                'mean_eq':mean_eq,
                'median_eq':median_eq,
                'max_eq':max_eq,
                'min_eq':min_eq,
                'balance_eq':max_eq+min_eq,
                'mean_eqf':mean_eqf,
                'median_eqf':median_eqf,
                'max_eqf':max_eqf,
                'min_eqf':min_eqf,
                'balance_eqf':max_eqf+min_eqf
            })
        longs = np.array(self.trade_data['o_longs'])
        shorts = np.array(self.trade_data['o_shorts'])
        closes = np.array(self.trade_data['c_longs'] + self.trade_data['c_shorts'])
        equity = np.array(self.trade_data['equity'])
        equity_fee = np.array(self.trade_data['equity_fee'])
        return trades,equity,equity_fee,longs,shorts,closes

    def print_statistics(self,vtb=True):
        """Печать статистики по торгам"""
        td = self.trade_data
        print(f"\n=== СТАТИСТИКА ДЛЯ {self.symbol} ===")
        print(f"Прибыль ABC без комисии: {td['equity'][-1]:.2f}")
        if vtb:
            print(f"Прибыль ВТБ: {td['step_eq_vtb'][-1]}")
            print(f"Комиссия ВТБ: {td['count']*2}")
            type_unclosed = 'unclosed_vtb'
        else:
            type_unclosed = 'unclosed_fee'
            print(f"Прибыль ABC c комиссией: {td['equity_fee'][-1]:.2f}")
            print(f"Комисии: {td['fees']:.2f}")
            print(f"Прибыль PER c комиссией: {td['total_wfees_per']:.2f}")
        print(f"Всего сделок: {td['count']}")
        print(f"Максимальная прибыль: {max(td[type_unclosed]):.2f}")
        print(f"Максимальная просадка: {min(td[type_unclosed]):.2f}")
        print(f"Открыто лонгов: {len(td['o_longs'])}")
        print(f"Открыто шортов: {len(td['o_shorts'])}")
        print(f"Превышений просадок: {len(td['c_risks'])}")

    def get_statistics(self,vtb=True):
        td = self.trade_data
        type_unclosed = 'unclosed_vtb' if vtb else 'unclosed_fee'
        pick_profit = 0
        dropdown = 0
        pick_loss = 0
        dropup = 0
        for p in td[type_unclosed]:
            if p > pick_profit:
                pick_profit = p
            elif p < pick_profit:
                delta = pick_profit - p
                if delta > dropdown:
                    dropdown = delta
            if p < pick_loss:
                pick_loss = p
            elif p > pick_loss:
                delta = p - pick_loss
                if delta > dropup:
                    dropup = delta
        statistics = {
            'total':td['total'],
            'total_wfee': self.trade_data['equity_fee'][-1],
            'twf_per': round(self.trade_data['total_wfees_per'],2),
            'total_vtb': td['step_eq_vtb'][-1],
            'count':td['count'],
            'fees': td['fees'],
            'count_risk': len(td['c_risks']),
            'max_profit': max(td[type_unclosed]),
            'min_profit': min(td[type_unclosed]),
            'max_dropdown':dropdown,
            'max_dropup':dropup,
            'days':self.days,
            'eq_day':td['total'] / self.days,
            'vtb_day':td['step_eq_vtb'][-1] / self.days
        }
        df_eq = pd.DataFrame({'eq':self.trade_data['equity']})
        mean_eq = 0
        median_eq = 0
        min_eq = 0
        max_eq = 0
        win_rate = 0
        if not df_eq.empty:
            df_eq['diff_eq'] = df_eq['eq'].diff()
            mean_eq = df_eq['diff_eq'].mean()
            median_eq = df_eq['diff_eq'].median()
            min_eq = df_eq['diff_eq'].min()
            max_eq = df_eq['diff_eq'].max()
            wins = len(df_eq[df_eq['diff_eq'] > 0].index)
            loss = len(df_eq[df_eq['diff_eq'] < 0].index)
            if loss > 0:
                win_rate = round((wins / (wins + loss)) * 100,2)
        statistics.update({
            'win_rate':win_rate,
            'mean_eq':mean_eq,
            'median_eq':median_eq,
            'min_eq':min_eq,
            'max_eq':max_eq
        })
        return statistics

    def plot_transaction(self):
        td = self.trade_data
        td['o_longs'] = np.array(td['o_longs'])
        td['o_shorts'] = np.array(td['o_shorts'])
        td['c_longs'] = np.array(td['c_longs'])
        td['c_shorts'] = np.array(td['c_shorts'])
        td['c_risks'] = np.array(td['c_risks'])
        if len(td['o_longs'].shape) > 1:
            plt.scatter(td['o_longs'][:,0],td['o_longs'][:,1],marker='^',color='blue')
        if len(td['o_shorts'].shape) > 1:
            plt.scatter(td['o_shorts'][:,0],td['o_shorts'][:,1],marker='v',color='black')
        if len(td['c_longs'].shape) > 1:
            plt.scatter(td['c_longs'][:,0],td['c_longs'][:,1],marker='x',color='blue')
        if len(td['c_shorts'].shape) > 1:
            plt.scatter(td['c_shorts'][:,0],td['c_shorts'][:,1],marker='x',color='black')
        if len(td['c_risks'].shape) > 1:
            x_starts = td['c_risks'][:,0]
            y_starts = td['c_risks'][:,1]
            x_ends = td['c_risks'][:,2]
            y_ends = td['c_risks'][:,3]

            # Создаём массивы для plot (чередуем start-end)
            x_lines = np.empty((len(td['c_risks']) * 3,))
            y_lines = np.empty((len(td['c_risks']) * 3,))
            x_lines[0::3] = x_starts
            x_lines[1::3] = x_ends
            x_lines[2::3] = np.nan
            y_lines[0::3] = y_starts
            y_lines[1::3] = y_ends
            y_lines[2::3] = np.nan

            plt.plot(x_lines, y_lines, color='black')
    
    def plot_equity(self,show=True):
        plt.plot(self.trade_data['equity'],color='r')
        plt.plot(self.trade_data['equity_fee'],color='b')
        if show:
            plt.show()
    
    def plot_chart(self,convert_tf=None,show=True):
        chart = self.df.copy()
        if convert_tf:
            chart = convert_timeframe(chart,convert_tf)
        # td = self.trade_data
        draw_hb_chart_fast(chart)
        self.plot_transaction()
        if show:
            plt.show()
    
    def plot_chart_and_sequtity(self,convert_tf=None,vtb=True,help_info='complex',show=True):
        """Создаем фигуру с двумя subplot'ами
            Варианты:
            'step_equity'
            'pos'
            'complex'
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)  # sharex=True для синхронизации по оси X
        
        # Первый график
        plt.sca(ax1)
        self.plot_chart(convert_tf, show=False)
        
        # Второй график
        plt.sca(ax2)
        if help_info == 'step_equity':
            sequity = self.trade_data['step_eq_vtb'] if vtb else self.trade_data['step_eq_fee']
        elif help_info == 'pos':
            sequity = self.trade_data['hist_pos']
        elif help_info == 'unclosed':
            sequity = self.trade_data['unclosed_vtb'] if vtb else self.trade_data['unclosed_fee']
        elif help_info == 'complex':
            sequity = self.trade_data['unclosed_vtb'] if vtb else self.trade_data['unclosed_fee']
            ax2.plot(sequity)
            sequity = self.trade_data['step_eq_vtb'] if vtb else self.trade_data['step_eq_fee']
        else:
            sequity = np.array([0])
        ax2.plot(sequity)
        total_wfee = sequity[-1]
        
        # Добавляем подписи для удобства
        ax1.set_title(f'Chart for {self.symbol} days {self.days}')
        ax2.set_title('Sequity: ' + str(total_wfee) + ' MDS: ' + str(total_wfee/self.days))
        risk_lbl = 'Count_risk ' + str(self.stop_risk) + ": " + str(len(self.trade_data['c_risks'])) + '| Count_trades: ' + str(self.trade_data['count']) + '| Mean_profit: ' + str(total_wfee/self.trade_data['count'])
        ax2.set_xlabel(risk_lbl)
        
        # Автоматическая регулировка layout'а
        plt.tight_layout()
        if show:
            plt.show()   