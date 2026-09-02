import numpy as np
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_rsi_tw,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_cci,add_stochastic,add_roc,add_fractals,add_bollinger,add_chop,add_supertrend,add_sma
from for_strategies.pva_indicators import add_integrity_index,add_mean_on_fractals,add_average_fractals,add_ext_on_fractals,add_quantile_params,add_ext_params
from for_strategies.vsa_indicators import add_dvsai,add_cdvsai
from for_strategies.fix_params import fix_supertrend_params,fix_two_periods_hm

class LEG1_CC2(BaseEG):
    """stop=None, take=None, period=15, period_q=10, max_period=55, solution=8,mult=2,use_stop=1,use_ps=1,period2s = 3, quantile=0.3 \n
    Crisis Counter 13 features"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_q=10, max_period=55, solution=8,mult=2,use_stop=1,use_ps=1,period2s = 3, quantile=0.3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.solution = solution
        self.period,self.period_q = fix_two_periods_hm(period,period_q,max_period)
        self.quantile = quantile
        self.period2s = period2s
        self.mult = mult
        self.use_stop = use_stop
        self.use_ps = use_ps
        self.inds = ('cmo', 'rsi', 'rsi_tw', 'williams_r', 'mfi', 'ultimate_oscillator', 'cci', '%d')

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_williams_r(df,self.period)
        df = add_mfi(df,self.period)
        df = add_ultimate_oscillator(df,self.period//3,self.period//2,self.period)
        df = add_cmo(df,self.period)
        df = add_cci(df,self.period)
        df = add_stochastic(df,self.period,self.period2s)
        df = add_roc(df,self.period)
        df = add_integrity_index(df,self.period)
        df['oversold'] = 0
        df['overbought'] = 0
        for i, ind in enumerate(self.inds):
            df = add_quantile_params(df,self.period_q,ind,self.quantile)
            df['oversold'] += df[ind] < df['bottom_q']
            df['overbought'] += df[ind] > df['top_q']
        df = add_bollinger(df,self.period)
        df['oversold'] += df['close'] < df['bbd']
        df['overbought'] += df['close'] > df['bbu']
        df = add_dvsai(df,self.period,self.mult)
        df['oversold'] += df['dvsai'] < df['dvsaid']
        df['overbought'] += df['dvsai'] > df['dvsaiu']
        df = add_cdvsai(df,self.period)
        df = add_rsi(df,self.period,'cum_dvsai')
        df = add_quantile_params(df,self.period_q,'rsi',self.quantile)
        df['oversold'] += df['rsi'] < df['bottom_q']
        df['overbought'] += df['rsi'] > df['top_q']
        
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata

    def _get_action_from_row(self, row):
        if row['oversold'] > self.solution:
            return 'open_long'
        
        if row['overbought'] > self.solution:
            return 'open_short'
        
        if self.use_ps:
            sol = self.solution // 2
            if row['oversold'] > sol or row['overbought'] > sol:
                return None
        
        if self.use_stop:
            return 'close_all'
        
        return None

# Healthy
class LEG1_OKROSHKA(BaseEG):
    """stop=None, take=None, period=15, period_chop=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_chop=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_chop = period_chop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df, self.period)
        df = add_chop(df, self.period_chop)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        threshold = 30
        if 60 > row['chop'] > 45:
            threshold = 30
        elif row['chop'] > 60:
            threshold = 25
        elif 45 > row['chop'] > 30:
            threshold = 20
        else:
            threshold = 10
        
        if row['rsi'] < threshold:
            return 'open_long'
        if row['rsi'] > 100 - threshold:
            return 'open_short'
        
        return None
    
# Healthy   
class LEG1_PIN(BaseEG):
    """stop=None, take=None, period=15, period2s=3, threshold=30, solution=5"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period2s=3, threshold=30, solution=5):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2s = period2s
        self.threshold = threshold
        self.solution = solution

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df, self.period)
        df = add_rsi_tw(df, self.period)
        df = add_williams_r(df, self.period)
        df = add_mfi(df, self.period)
        df = add_ultimate_oscillator(df, self.period // 3, self.period // 2, self.period)
        df = add_cmo(df, self.period)
        df = add_cci(df, self.period)
        df = add_stochastic(df, self.period, self.period2s)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        pins_solution = 0
        
        if row['rsi'] < self.threshold:
            pins_solution += 1
        if row['rsi_tw'] < self.threshold:
            pins_solution += 1
        if row['williams_r'] < -100 + self.threshold:
            pins_solution += 1
        if row['mfi'] < self.threshold:
            pins_solution += 1
        if row['ultimate_oscillator'] < self.threshold + 10:
            pins_solution += 1
        if row['cmo'] < -100 + self.threshold + 10:
            pins_solution += 1
        if row['cci'] < -200 + self.threshold:
            pins_solution += 1
        if row['%k'] > row['%d'] < self.threshold:
            pins_solution += 1
        
        if row['rsi'] > 100 - self.threshold:
            pins_solution -= 1
        if row['rsi_tw'] > 100 - self.threshold:
            pins_solution -= 1
        if row['williams_r'] > 0 - self.threshold:
            pins_solution -= 1
        if row['mfi'] > 100 - self.threshold:
            pins_solution -= 1
        if row['ultimate_oscillator'] > 100 - self.threshold - 10:
            pins_solution -= 1
        if row['cmo'] > 100 - self.threshold - 10:
            pins_solution -= 1
        if row['cci'] > 200 - self.threshold:
            pins_solution -= 1
        if row['%k'] < row['%d'] > 100 - self.threshold:
            pins_solution -= 1
        
        if pins_solution > self.solution:
            return 'open_long'
        if pins_solution < -self.solution:
            return 'open_short'
        
        return None

class LEG1_BIBI2(BaseEG):
    """stop=None, take=None, period=15, period_q=10, kind='rsi',max_period=55,period2s = 3, quantile=0.3 \n
    'cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_q=10, kind='rsi',max_period=55,period2s = 3, quantile=0.3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.kind = kind
        self.period2s = period2s
        self.period,self.period_q = fix_two_periods_hm(period,period_q,max_period)
        self.quantile = quantile

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        if self.kind == 'rsi':
            df = add_rsi(df, self.period)
        if self.kind == 'rsi_tw':
            df = add_rsi_tw(df, self.period)
        if self.kind == 'williams_r':
            df = add_williams_r(df, self.period)
        if self.kind == 'mfi':
            df = add_mfi(df, self.period)
        if self.kind == 'ultimate_oscillator':
            df = add_ultimate_oscillator(df, self.period // 3, self.period // 2, self.period)
        if self.kind == 'cmo':
            df = add_cmo(df, self.period)
        if self.kind == 'cci':
            df = add_cci(df, self.period)
        if self.kind == '%d':
            df = add_stochastic(df, self.period, self.period2s)
        df = add_quantile_params(df,self.period_q,self.kind,self.quantile)
        df['oversold'] = df[self.kind] < df['bottom_q']
        df['overbought'] = df[self.kind] > df['top_q']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['top_q'] > row['bottom_q']:
            if row['oversold']:
                return 'open_long'
            if row['overbought']:
                return 'open_short'
        else:
            if row['oversold'] and row['overbought']:
                return 'close_all'
            if row['oversold']:
                return 'close_short'
            if row['overbought']:
                return 'close_long'      
        return None

class LEG1_IGOGOSHA2(BaseEG):
    """stop=None, take=None, period=15, period_q=10, kind='rsi',period2s=3, quantile=0.3,period_ext=10,max_period=55 \n
    'cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_q=10, kind='rsi',period2s=3, quantile=0.3,period_ext=10,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.kind = kind
        self.period, self.period_q = fix_two_periods_hm(period,period_q,max_period)
        if period_ext + self.period > max_period:
            self.period_ext = max_period - self.period
        else:
            self.period_ext = period_ext
        self.quantile = quantile
        self.period2s = period2s

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        if self.kind == 'rsi':
            df = add_rsi(df, self.period)
        if self.kind == 'rsi_tw':
            df = add_rsi_tw(df, self.period)
        if self.kind == 'williams_r':
            df = add_williams_r(df, self.period)
        if self.kind == 'mfi':
            df = add_mfi(df, self.period)
        if self.kind == 'ultimate_oscillator':
            df = add_ultimate_oscillator(df, self.period // 3, self.period // 2, self.period)
        if self.kind == 'cmo':
            df = add_cmo(df, self.period)
        if self.kind == 'cci':
            df = add_cci(df, self.period)
        if self.kind == '%d':
            df = add_stochastic(df, self.period, self.period2s)
        df = add_quantile_params(df,self.period_q,self.kind,self.quantile)
        df = add_ext_params(df,self.period_ext)
        df['oversold1'] = df[self.kind] < df['bottom_q']
        df['overbought1'] = df[self.kind] > df['top_q']
        df['oversold2'] = df[self.kind] < df['bottom_ext'].shift(1)
        df['overbought2'] = df[self.kind] > df['top_ext'].shift(1)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['top_ext'] > row['bottom_ext']:
            if row['oversold2']:
                return 'open_long'
            if row['overbought2']:
                return 'open_short'
                    
        if row['oversold1'] and row['overbought1']:
            return 'close_all'
        if row['oversold1']:
            return 'close_short'
        if row['overbought1']:
            return 'close_long'
        
        return None
        
class LEG1_IRONANNY2(BaseEG):
    """stop=None, take=None, period=15, period_q=10, max_period=55, solution=5,period2s=3, quantile=0.3 \n
    8 макс solution"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_q=10, max_period=55, solution=5,period2s=3, quantile=0.3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.solution = solution
        self.period,self.period_q = fix_two_periods_hm(period,period_q,max_period)
        self.quantile = quantile
        self.period2s = period2s
        self.inds = ('cmo', 'rsi', 'rsi_tw', 'williams_r', 'mfi', 'ultimate_oscillator', 'cci', '%d')

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df, self.period)
        df = add_rsi_tw(df, self.period)
        df = add_williams_r(df, self.period)
        df = add_mfi(df, self.period)
        df = add_ultimate_oscillator(df, self.period // 3, self.period // 2, self.period)
        df = add_cmo(df, self.period)
        df = add_cci(df, self.period)
        df = add_stochastic(df, self.period, self.period2s)
        df['oversold'] = 0
        df['overbought'] = 0
        for i, ind in enumerate(self.inds):
            df = add_quantile_params(df,self.period_q,ind,self.quantile)
            df['oversold'] += df[ind] < df['bottom_q']
            df['overbought'] += df[ind] > df['top_q']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['oversold'] > self.solution:
            return 'open_long'
        if row['overbought'] > self.solution:
            return 'open_short'
        
        return None
        
#хз что за супертренд, надо проверять, но нейронка высоко оценила стратегию 
class LEG1_PHOGA(BaseEG):
    """stop=None, take=None, period=10, multiplier=3, period_mvol=10, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, multiplier=3, period_mvol=10, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period= fix_supertrend_params(period,multiplier,max_period)
        self.multiplier = multiplier
        self.period_mvol = period_mvol
        self.type_eg = 1
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart'].copy()
        
        df = add_supertrend(df, self.period, self.multiplier)
        df['mean_volume'] = df['volume'].rolling(self.period_mvol).mean()
        
        # Работаем с numpy массивами
        in_uptrend = df['in_uptrend'].fillna(False).astype(bool).values
        volume = df['volume'].values
        mean_volume = df['mean_volume'].values
        
        # Создаем массив сигналов
        signals = np.zeros(len(df), dtype=np.int8)
        
        # Условия для покупки и продажи
        buy_condition = (in_uptrend[1:]) & (~in_uptrend[:-1]) & (volume[1:] > mean_volume[1:])
        sell_condition = (~in_uptrend[1:]) & (in_uptrend[:-1]) & (volume[1:] > mean_volume[1:])
        
        signals[1:][buy_condition] = 1
        signals[1:][sell_condition] = -1
        
        df['signal'] = signals
        
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'
        
        return None
        
class LEG1_BORSCH(BaseEG):
    """stop=None, take=None, period=20, period_mvol=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_mvol=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.type_eg = 1
        self.period_mvol = period_mvol

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart'].copy()
        
        # Расчёт моментума (если нужен - добавьте)
        
        # Добавление уровней недавних максимумов и минимумов
        df['recent_max'] = df['high'].rolling(window=self.period).max()
        df['recent_min'] = df['low'].rolling(window=self.period).min()
        
        # Фильтр по объёму
        df['mean_volume'] = df['volume'].rolling(self.period_mvol).mean()
        df['above_avg_volume'] = df['volume'] > df['mean_volume']
        
        # Векторизованная генерация сигналов (без цикла!)
        # Сдвигаем уровни для сравнения с предыдущим баром
        recent_max_shifted = df['recent_max'].shift(1)
        recent_min_shifted = df['recent_min'].shift(1)
        
        # Сигналы
        df['signal'] = 0
        df.loc[(df['close'] > recent_max_shifted) & df['above_avg_volume'], 'signal'] = 1
        df.loc[(df['close'] < recent_min_shifted) & df['above_avg_volume'], 'signal'] = -1
        
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'
        
        return None
    
class LEG1_PHOBO(BaseEG):
    """stop=None, take=None, period=10, multiplier=3, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, multiplier=3, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period= fix_supertrend_params(period,multiplier,max_period)
        self.multiplier = multiplier
        self.type_eg = 1
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart'].copy()
        
        df = add_supertrend(df, self.period, self.multiplier)
        
        # Работаем с numpy массивами
        in_uptrend = df['in_uptrend'].fillna(False).values
        n = len(in_uptrend)
        
        # Создаем массив сигналов
        signals = np.zeros(n, dtype=np.int8)
        
        # Покупка: текущий True, предыдущий False
        buy_mask = (in_uptrend[1:] == True) & (in_uptrend[:-1] == False)
        signals[1:][buy_mask] = 1
        
        # Продажа: текущий False, предыдущий True
        sell_mask = (in_uptrend[1:] == False) & (in_uptrend[:-1] == True)
        signals[1:][sell_mask] = -1
        
        df['signal'] = signals
        
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'
        
        return None
        
class LEG1_LAKSAe(BaseEG):
    """stop=None, take=None, period=20, period2=5"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period2=5):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_sma(df, self.period)
        df['local_max'] = df['close'].rolling(window=self.period2).max()
        df['local_min'] = df['close'].rolling(window=self.period2).min()
        df['nearest_long'] = df['high'] - df['close'] > df['close'] - df['low']
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['low'] <= df['local_min']) & (df['close'] > df['sma']) & (df['nearest_long'] == True), 'signal'] = 1  # Покупка
        df.loc[(df['high'] >= df['local_max']) & (df['close'] < df['sma']) & (df['nearest_long'] == False), 'signal'] = -1  # Продажа

        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'
        
        return None