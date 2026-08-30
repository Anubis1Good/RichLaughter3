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

# fee = 0.0001   # 0.01% — realistic для лимиток с учётом минимума
# fee = 0.0005   # 0.05% — realistic для рынка
# fee = 0.00005  # 0.005% — минимальная лимитная комиссия (для акций больше 500 р)


#добавить тесты с заявками
# возможно стоит добавить две комиссии
# подумать над видом стопа, можно сделать рыночный стоп, который может достигать 1%,5%,10%. Но он должен просто выставляться автоматически в приводе
class CheckEGTrader:
    def __init__(self,
                 df:pd.DataFrame | str, 
                 ws:list|tuple|BaseEG,
                 fee:float = 0.001, #в долях (абсолютное значение)
                 symbol:str = 'Test',
                 close_on_time:bool=True,
                 close_map:tuple|list=(
                     (22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30),),
                 measure_time:bool=False,
                 use_tqdm:bool=False,
                 window:int=60,
                 days_mode=None,
                 slip_stop_delta=1,
                 auto_take = 1
                 ):
        self.window = window
        self.symbol = symbol
        self.slip_stop_delta = slip_stop_delta
        if isinstance(df,str):
            path_df = df
            self.df = simple_load_df(path_df)
        else:
            self.df = df.copy()
        self.price_step = get_price_step(self.df)
        self.mean_price = self.df['close'].mean()
        self.price_step_per = (self.price_step / self.mean_price)*100
        # print(self.price_step)
        # print(self.price_step_per)
        # print(self.df.tail())
        if isinstance(ws,tuple) or isinstance(ws,list):
            self.ws = ws[0](self.symbol,self.price_step,1,None,*ws[1])
        else:
            self.ws = ws
        self.fee = fee
        self.fee_one_p = fee  * 100
        self.close_on_time = close_on_time
        self.close_map = close_map
        self.check_days_mode(days_mode)
        self.actions = (None,'open_long','open_short','close_long','close_short','close_all','stop_close_long','stop_close_short')
        self.actions_dict = {action: idx for idx, action in enumerate(self.actions)}
        self.measure_time = measure_time
        self.use_tqdm = use_tqdm
        self.df = self.add_time_features(self.df)
        self.days = self.df['ms'].dt.date.nunique()
        self.auto_take = auto_take
        self.reload_data()

    def check_days_mode(self,days_mode):
        if days_mode is not None:
            if days_mode == 5:
                # Меняем close_map для выходных на (0, 1)
                # Индексы 5 и 6 - это суббота и воскресенье
                close_map_list = list(self.close_map)
                close_map_list[5] = (0, 0)  # Суббота
                close_map_list[6] = (0, 0)  # Воскресенье
                self.close_map = tuple(close_map_list)
            elif days_mode == 2:
                # Оставляем только выходные, все будние дни -> (0, 0)
                close_map_list = list(self.close_map)
                # Индексы 0-4 - будние дни (пн-пт)
                for i in range(5):  # 0, 1, 2, 3, 4
                    close_map_list[i] = (0, 0)
                # Индексы 5-6 (сб, вс) оставляем как есть
                self.close_map = tuple(close_map_list)

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
            'pos':0, #текущая позиция
            'hist_pos':[0],
            'open_price':0, #текущая цена
            'o_longs':[], #входы в лонг
            'o_shorts':[], #входы в шорт
            'c_longs':[], #закрытие лонгов
            'c_shorts':[], #закрытие шортов 
            'takes':[0], #тейков
            'stops':[0], #стопов

        }
        self.open_fee = 0
        self.cur_eq = None
        self.tdata = {}
        self.tdata['chart'] = self.df.copy()
        if self.ws is not None:
            self.ws.amount_sl = 0
            self.ws.amount_tp = 0
            self.ws.can_long = True
            self.ws.can_short = True

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

    def close_pos(self,price,feei,delta,is_stop=False):
        if is_stop:
            delta = delta * self.slip_stop_delta
        self.trade_data['total'] += delta
        self.trade_data['total_wfees_per'] += ((delta  / price) * 100) - self.fee_one_p  # комиссия за закрытие
        self.trade_data['fees'] += feei
        self.trade_data['equity'].append(self.trade_data['equity'][-1] + delta)
        self.trade_data['equity_fee'].append(self.trade_data['equity_fee'][-1] + delta - feei - self.open_fee)
        self.open_fee = 0

    def close_long(self,price,feei,row_name,is_stop=False):
        delta = price - self.trade_data['open_price']  # прибыль по лонгу (как при action=3)
        self.close_pos(price,feei,delta,is_stop)
        self.trade_data['c_longs'].append((row_name,price))
        self.trade_data['pos'] = 0
    
    def close_short(self,price,feei,row_name,is_stop=False):
        delta = self.trade_data['open_price'] - price  # прибыль по шорту (как при action=4)
        self.close_pos(price,feei,delta,is_stop)
        self.trade_data['c_shorts'].append((row_name,price))
        self.trade_data['pos'] = 0

    def work_action(self,signal, price, row_name):
        """return pos,open_price,fees,open_fee"""
        # self.actions = (None,'open_long','open_short','close_long','close_short','close_all','stop_close_long','stop_close_short')
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
        elif signal == 5: # 'close_all'
            if self.trade_data['pos'] == 1:
                self.close_long(price,feei,row_name)
            elif self.trade_data['pos'] == -1:
                self.close_short(price,feei,row_name)
        elif signal == 6: #'stop_close_long'
            if self.trade_data['pos'] == 1:
                self.close_long(price,feei,row_name,True)
        elif signal == 7: #'stop_close_short'
            if self.trade_data['pos'] == -1:
                self.close_short(price,feei,row_name,True)

    def add_time_features(self,df:pd.DataFrame):
        df = df.copy()
        df['ms'] = pd.to_datetime(df['ms'], format='%Y-%m-%d %H:%M:%S')
        df['hour'] = df['ms'].dt.hour
        df['minute'] = df['ms'].dt.minute
        df['weekday'] = df['ms'].dt.weekday
        return df

    def update_step_data(self,price):
        self.trade_data['step_eq_fee'].append(self.trade_data['equity_fee'][-1])
        self.trade_data['hist_pos'].append(self.trade_data['pos'])
        if self.trade_data['pos'] > 0:
            unclosed_profit = price - self.trade_data['open_price']
        elif self.trade_data['pos'] < 0:
            unclosed_profit = self.trade_data['open_price'] - price
        else:
            unclosed_profit = 0
        self.trade_data['unclosed_fee'].append(self.trade_data['step_eq_fee'][-1] + unclosed_profit)
        self.trade_data['stops'].append(self.ws.amount_sl)
        self.trade_data['takes'].append(self.ws.amount_tp)
    
    def sync_step_data(self,df_processed):
        price = 0
        empty_test = len(self.df) - len(df_processed)
        if empty_test > 0:
            for i in range(empty_test - 1):
                self.update_step_data(price)

    # CHECKS_FUNCS
    # @duration_time
    # def check_strategy_fast(self, history_bars=60):
    #     """
    #     Быстрый тест для оптимизации.
    #     Индикаторы рассчитываются один раз на всех данных.
    #     Подходит для быстрой проверки множества параметров.
    #     """
    #     self.reload_data()
        
    #     # Подготавливаем данные через preprocessing
    #     pdata = self.ws.preprocessing(self.tdata)
    #     df = pdata['chart']
    #     window = self.window - (len(self.df) - len(df))
    #     self.sync_step_data(df)
        
    #     if self.close_on_time:
    #         mask = (df['hour'] >= df['weekday'].map(lambda wd: self.close_map[wd][0])) & \
    #             (df['minute'] >= df['weekday'].map(lambda wd: self.close_map[wd][1]))
    #         mask_values = mask.values
    #     else:
    #         mask_values = None
        
    #     prices = df['close'].values
    #     row_names = df['x'].values
        

    #     for i in self.get_iterator(range(len(df))):
    #         price = prices[i]
    #         if i < window:
    #             self.update_step_data(price)
    #             continue
    #         row_name = row_names[i]
            
    #         # Проверка времени закрытия
    #         if self.close_on_time and mask_values is not None and mask_values[i]:
    #             signal = self.actions_dict['close_all']
    #         else:
    #             # Берем срез до текущего индекса (не более history_bars)
    #             start_idx = max(0, i - history_bars + 1)
    #             current_df = df.iloc[start_idx:i+1]  # без .copy()!
                
    #             current_pdata = {'chart': current_df}
                
    #             # Вычисляем delta только если есть позиция
    #             pos = self.trade_data['pos']
    #             open_price = self.trade_data['open_price']
                
    #             delta = None
    #             if pos != 0 and open_price != 0:
    #                 if pos > 0:
    #                     delta = (price - open_price) // self.price_step
    #                 else:
    #                     delta = (open_price - price) // self.price_step
                
    #             action = self.ws(current_pdata, pos, delta)
    #             signal = self.actions_dict.get(action, 0)
            
    #         # Выполняем действие
    #         self.work_action(signal, price, row_name)
    #         self.update_step_data(price)

    @duration_time
    def check_strategy_faster(self, history_bars=None):
        """
        Быстрый тест для оптимизации.
        """
        self.reload_data()
        
        # Подготавливаем данные через preprocessing
        pdata = self.ws.preprocessing(self.tdata)
        df = pdata['chart']
        # print(df)
        window = self.window - (len(self.df) - len(df))
        self.sync_step_data(df)
        
        if self.close_on_time:
            mask = (df['hour'] >= df['weekday'].map(lambda wd: self.close_map[wd][0])) & \
                (df['minute'] >= df['weekday'].map(lambda wd: self.close_map[wd][1]))
            mask_values = mask.values
        else:
            mask_values = None
        highs = df['high'].values
        lows = df['low'].values
        prices = df['close'].values
        row_names = df['x'].values
        
        for i in self.get_iterator(range(len(df))):
            price = prices[i]
            if i < window:
                self.update_step_data(price)
                continue
            row_name = row_names[i]
            
            if self.close_on_time and mask_values[i]:
                signal = self.actions_dict['close_all']
            else:
                
                pos = self.trade_data['pos']
                open_price = self.trade_data['open_price']
                
                delta = None
                if pos != 0 and open_price != 0:
                    if pos > 0:
                        delta_nega = (lows[i] - open_price) // self.price_step
                        if self.ws.stop is not None and delta_nega <= -self.ws.stop:
                            delta = delta_nega
                        elif self.auto_take is not None and self.ws.take is not None:
                            delta_posi = (highs[i] - open_price) // self.price_step
                            auto_take = self.ws.take * self.auto_take
                            if delta_posi >= auto_take:
                                delta = auto_take
                            else:
                                delta = (price - open_price) // self.price_step
                        else:
                            delta = (price - open_price) // self.price_step
                    else:
                        delta_nega = (open_price - highs[i]) // self.price_step
                        if self.ws.stop is not None and delta_nega <= -self.ws.stop:
                            delta = delta_nega
                        elif self.auto_take is not None and self.ws.take is not None:
                            delta_posi = (open_price - lows[i]) // self.price_step
                            auto_take = self.ws.take * self.auto_take
                            if delta_posi >= auto_take:
                                delta = auto_take
                            else:
                                delta = (open_price - price) // self.price_step
                        else:
                            delta = (open_price - price) // self.price_step
                
                # БЫСТРЫЙ РЕЖИМ: передаем индексы, а не копию
                fast_pdata = {
                    'chart': df,
                    'idx': i,  # текущий индекс
                    'fast_mode': True
                }
                
                action = self.ws(fast_pdata, pos, delta)
                signal = self.actions_dict.get(action, 0)
            
            self.work_action(signal, price, row_name)
            self.update_step_data(price)
    @duration_time
    def check_strategy_window(self, normalization=True):
        """
        Честный оконный тест для проверки стратегии.
        Индикаторы пересчитываются на каждом окне независимо.
        Исключает возможность заглядывания в будущее.
        """
        self.reload_data()
        
        for i in self.get_iterator(range(len(self.df))):
            # Пропускаем первые window баров (нужно для расчета индикаторов)
            if i < self.window:
                self.update_step_data(self.df.iloc[i]['close'])
                continue
            
            # Берем срез окна
            df_slice = self.df.iloc[i-self.window:i+1].copy()
            price = df_slice.iloc[-1]['close']
            row_name = df_slice.iloc[-1]['x']
            low = df_slice.iloc[-1]['low']
            high = df_slice.iloc[-1]['high']
            
            # Проверка времени закрытия
            if self.close_on_time:
                last_row = df_slice.iloc[-1]
                time_close = self.close_map[last_row['weekday']]
                if last_row['hour'] >= time_close[0] and last_row['minute'] >= time_close[1]:
                    signal = self.actions_dict['close_all']
                    self.work_action(signal, price, row_name)
                    self.update_step_data(price)
                    continue

            # Нормализация если нужно
            if normalization:
                candle_max = df_slice['high'].max()
                if candle_max > 0:
                    df_slice['volume'] = df_slice['volume'] / df_slice['volume'].max() if df_slice['volume'].max() > 0 else 0
                    df_slice['close'] = df_slice['close'] / candle_max
                    df_slice['open'] = df_slice['open'] / candle_max
                    df_slice['low'] = df_slice['low'] / candle_max
                    df_slice['high'] = df_slice['high'] / candle_max
                    df_slice['middle'] = df_slice['middle'] / candle_max
            
            # Подготавливаем данные через preprocessing стратегии
            tdata = {'chart': df_slice}
            pdata = self.ws.preprocessing(tdata)
            
            
            # Вычисляем delta
            pos = self.trade_data['pos']
            open_price = self.trade_data['open_price']
            
            delta = None
            if pos != 0 and open_price != 0:
                if pos > 0:
                    delta_nega = (low - open_price) // self.price_step
                    if self.ws.stop is not None and delta_nega <= -self.ws.stop:
                        delta = delta_nega
                    elif self.auto_take is not None and self.ws.take is not None:
                        delta_posi = (high - open_price) // self.price_step
                        auto_take = self.ws.take * self.auto_take
                        if delta_posi >= auto_take:
                            delta = auto_take
                        else:
                            delta = (price - open_price) // self.price_step
                    else:
                        delta = (price - open_price) // self.price_step
                else:
                    delta_nega = (open_price - high) // self.price_step
                    if self.ws.stop is not None and  delta_nega <= -self.ws.stop:
                        delta = delta_nega
                    elif self.auto_take is not None and self.ws.take is not None:
                        delta_posi = (open_price - low) // self.price_step
                        auto_take = self.ws.take * self.auto_take
                        if delta_posi >= auto_take:
                            delta = auto_take
                        else:
                            delta = (open_price - price) // self.price_step
                    else:
                        delta = (open_price - price) // self.price_step
            
            # Получаем action от стратегии
            action = self.ws(pdata, pos, delta)
            signal = self.actions_dict.get(action, 0)
            
            # Выполняем действие
            self.work_action(signal, price, row_name)
            self.update_step_data(price)

    # POST_PROCESS_RESULT_FUNCS
    def process_old_type_result(self):
        df_eq = pd.DataFrame({'eq':self.trade_data['equity'],'eq_fee':self.trade_data['equity_fee']})
        trades = {'total': self.trade_data['total'], 'count': self.trade_data['count'], 'total_fee_per': self.trade_data['total_wfees_per']}
        if df_eq.empty or len(df_eq) < 2:
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
            
            # ==========================================
            # УБИРАЕМ NaN ИЗ diff (первая строка всегда NaN)
            # ==========================================
            diff_eq = df_eq['diff_eq'].dropna()
            diff_eq_fee = df_eq['diff_eq_fee'].dropna()
            
            # ==========================================
            # ПРОВЕРЯЕМ, ЧТО ЕСТЬ ДАННЫЕ ДЛЯ СТАТИСТИКИ
            # ==========================================
            if len(diff_eq) == 0:
                mean_eq = median_eq = min_eq = max_eq = 0
                mean_eqf = median_eqf = min_eqf = max_eqf = 0
                win_rate = 0
            else:
                mean_eq = diff_eq.mean()
                median_eq = diff_eq.median()
                min_eq = diff_eq.min()
                max_eq = diff_eq.max()
                
                mean_eqf = diff_eq_fee.mean()
                median_eqf = diff_eq_fee.median()
                min_eqf = diff_eq_fee.min()
                max_eqf = diff_eq_fee.max()
                
                wins = len(diff_eq[diff_eq > 0])
                loss = len(diff_eq[diff_eq < 0])
                win_rate = round((wins / (wins + loss)) * 100, 2) if loss > 0 else 0

            trades['total_fee_per'] = round(self.trade_data['total_wfees_per'],2)
            trades.update({
                'total_abs_fee': self.trade_data['equity_fee'][-1] if self.trade_data['equity_fee'] else 0,
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
        longs = np.array(self.trade_data['o_longs']) if self.trade_data['o_longs'] else np.array([])
        shorts = np.array(self.trade_data['o_shorts']) if self.trade_data['o_shorts'] else np.array([])
        closes = np.array(self.trade_data['c_longs'] + self.trade_data['c_shorts']) if (self.trade_data['c_longs'] or self.trade_data['c_shorts']) else np.array([])
        equity = np.array(self.trade_data['equity'])
        equity_fee = np.array(self.trade_data['equity_fee'])
        return trades,equity,equity_fee,longs,shorts,closes

    def print_statistics(self):
        """Печать статистики по торгам"""
        td = self.trade_data
        print(f"\n=== СТАТИСТИКА ДЛЯ {self.symbol} ===")
        print(f"Прибыль ABC без комисии: {td['equity'][-1]:.2f}")
        print(f"Прибыль ABC c комиссией: {td['equity_fee'][-1]:.2f}")
        print(f"Комисии: {td['fees']:.2f}")
        print(f"Прибыль PER c комиссией: {td['total_wfees_per']:.2f}")
        print(f"Всего сделок: {td['count']}")
        print(f"Максимальная прибыль: {max(td['unclosed_fee']):.2f}")
        print(f"Максимальная просадка: {min(td['unclosed_fee']):.2f}")
        print(f"Открыто лонгов: {len(td['o_longs'])}")
        print(f"Открыто шортов: {len(td['o_shorts'])}")
        print(f"Тейков: {td['takes'][-1]}")
        print(f"Стопов: {td['stops'][-1]}")

    def get_statistics(self):
        td = self.trade_data
        # Расчет максимальной просадки и подъема
        pick_profit = 0
        dropdown = 0
        pick_loss = 0
        dropup = 0
        for p in td['unclosed_fee']:
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
        
        # Базовая статистика
        statistics = {
            'total': td['total'],
            'total_wfee': td['equity_fee'][-1],
            'twf_per': round(td['total_wfees_per'], 2),
            'count': td['count'],
            'fees': td['fees'],
            'max_profit': max(td['unclosed_fee']),
            'min_profit': min(td['unclosed_fee']),
            'max_dropdown': dropdown,
            'max_dropup': dropup,
            'days': self.days,
            'eq_day': td['total'] / self.days if self.days > 0 else 0
        }
        
        # Расчет win_rate и статистики по сделкам
        df_eq = pd.DataFrame({'eq': td['equity']})
        mean_eq = 0
        median_eq = 0
        min_eq = 0
        max_eq = 0
        win_rate = 0
        
        if not df_eq.empty and len(df_eq) > 1:
            df_eq['diff_eq'] = df_eq['eq'].diff()
            diff_eq = df_eq['diff_eq'].dropna()
            
            if not diff_eq.empty:
                mean_eq = diff_eq.mean()
                median_eq = diff_eq.median()
                min_eq = diff_eq.min()
                max_eq = diff_eq.max()
                
                wins = len(diff_eq[diff_eq > 0])
                loss = len(diff_eq[diff_eq < 0])
                total = wins + loss
                if total > 0:
                    win_rate = round((wins / total) * 100, 2)
        
        statistics.update({
            'win_rate': win_rate,
            'mean_eq': mean_eq,
            'median_eq': median_eq,
            'min_eq': min_eq,
            'max_eq': max_eq
        })
        
        return statistics
    
    def plot_transaction(self):
        td = self.trade_data
        td['o_longs'] = np.array(td['o_longs'])
        td['o_shorts'] = np.array(td['o_shorts'])
        td['c_longs'] = np.array(td['c_longs'])
        td['c_shorts'] = np.array(td['c_shorts'])
        if len(td['o_longs'].shape) > 1:
            plt.scatter(td['o_longs'][:,0],td['o_longs'][:,1],marker='^',color='blue')
        if len(td['o_shorts'].shape) > 1:
            plt.scatter(td['o_shorts'][:,0],td['o_shorts'][:,1],marker='v',color='black')
        if len(td['c_longs'].shape) > 1:
            plt.scatter(td['c_longs'][:,0],td['c_longs'][:,1],marker='x',color='blue')
        if len(td['c_shorts'].shape) > 1:
            plt.scatter(td['c_shorts'][:,0],td['c_shorts'][:,1],marker='x',color='black')

    
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
    
    def plot_chart_and_sequtity(self,convert_tf=None,help_info='complex',show=True):
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
            sequity = self.trade_data['step_eq_fee']
        elif help_info == 'pos':
            sequity = self.trade_data['hist_pos']
        elif help_info == 'unclosed':
            sequity = self.trade_data['unclosed_fee']
        elif help_info == 'complex':
            sequity = self.trade_data['unclosed_fee']
            ax2.plot(sequity)
            sequity = self.trade_data['step_eq_fee']
        elif help_info == 'sltp':
            sequity = self.trade_data['stops']
            ax2.plot(sequity,color='red')
            sequity = self.trade_data['takes']
        else:
            sequity = np.array([0])
        ax2.plot(sequity)
        total_wfee = sequity[-1]
        
        # Добавляем подписи для удобства
        ax1.set_title(f'Chart for {self.symbol} days {self.days}')
        ax2.set_title('Sequity: ' + str(total_wfee) + ' MDS: ' + str(total_wfee/self.days if self.days > 0 else 0))
        risk_lbl = 'Count_trades: ' + str(self.trade_data['count']) + '| Mean_profit: ' + str(total_wfee/self.trade_data['count'])
        ax2.set_xlabel(risk_lbl)
        
        # Автоматическая регулировка layout'а
        plt.tight_layout()
        if show:
            plt.show()   