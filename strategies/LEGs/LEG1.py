import numpy as np
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_rsi_tw,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_cci,add_stochastic,add_roc,add_fractals,add_bollinger,add_chop,add_supertrend,add_ema
from for_strategies.pva_indicators import add_integrity_index,add_mean_on_fractals,add_average_fractals,add_ext_on_fractals
from for_strategies.vsa_indicators import add_dvsai,add_cdvsai

class LEG1_CC(BaseEG):
    """stop=None, take=None, period=15, period_fractal=10, period_max=55, solution=8,period_avfr=30,mult=2,use_stop=1,use_ps=1 \n
    Crisis Counter 15 features"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_fractal=10, period_max=55, solution=8,period_avfr=30,mult=2,use_stop=1,use_ps=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.period = period
        self.solution = solution
        self.period_fractal = period_fractal
        self.period_max = period_max
        self.mult = mult
        self.use_stop = use_stop
        self.use_ps = use_ps
        self.period_avfr = period_avfr
        self.problems = 'Mcfly'

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
        df = add_stochastic(df,self.period,self.period//2)
        df = add_roc(df,self.period)
        df = add_integrity_index(df,self.period)
        df = add_fractals(df,self.period_fractal)
        inds = ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d','roc','ii')
        df['oversold'] = 0
        df['overbought'] = 0
        for i, ind in enumerate(inds):
            df = add_mean_on_fractals(df,self.period_max,ind,self.period_fractal)
            df['oversold'] += df[ind] < df['bottom_mean']
            df['overbought'] += df[ind] > df['top_mean']
        df = add_bollinger(df,self.period)
        df['oversold'] += df['close'] < df['bbd']
        df['overbought'] += df['close'] > df['bbu']
        df = add_average_fractals(df,self.period_avfr,self.period_fractal)
        df['oversold'] += df['close'] <= df['ave_down']
        df['overbought'] += df['close'] >= df['ave_up']
        df = add_dvsai(df,self.period,self.mult)
        df['oversold'] += df['dvsai'] < df['dvsaid']
        df['overbought'] += df['dvsai'] > df['dvsaiu']
        df = add_cdvsai(df,self.period)
        df = add_rsi(df,self.period,'cum_dvsai')
        df = add_mean_on_fractals(df,self.period_max,'rsi',self.period_fractal)
        df['oversold'] += df['rsi'] < df['bottom_mean']
        df['overbought'] += df['rsi'] > df['top_mean']
        
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
    """stop=None, take=None, period=15, period2=3, threshold=30, solution=5"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period2=3, threshold=30, solution=5):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
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
        df = add_stochastic(df, self.period, self.period2)
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

# Mcfly problem
class LEG1_BIBI(BaseEG):
    """stop=None, take=None, period=15, period_fractal=10, kind='rsi',period_winmean=55 \n
    'cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_fractal=10, kind='rsi',period_winmean=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.kind = kind
        self.period_fractal = period_fractal
        self.period_winmean = period_winmean
        self.problems = 'Mcfly'

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
            df = add_stochastic(df, self.period, self.period // 2)
        df = add_fractals(df, self.period_fractal,self.period_winmean)
        df = add_mean_on_fractals(df, self.period_winmean, self.kind,self.period_fractal)
        df['oversold'] = df[self.kind] < df['bottom_mean']
        df['overbought'] = df[self.kind] > df['top_mean']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['top_mean'] > row['bottom_mean']:
            if row['oversold']:
                return 'open_long'
            if row['overbought']:
                return 'open_short'
        else:
            if row['oversold']:
                return 'close_short'
            if row['overbought']:
                return 'close_long'
        
        return None

# Mcfly problem
class LEG1_IGOGOSHA(BaseEG):
    """stop=None, take=None, period=15, period_fractal=10, period_max=55, kind='rsi' \n
    'cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_fractal=10, period_max=55, kind='rsi'):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.kind = kind
        self.period_fractal = period_fractal
        self.period_max = period_max
        self.problems = 'Mcfly'

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
            df = add_stochastic(df, self.period, self.period // 2)
        df = add_fractals(df, self.period_fractal)
        df = add_ext_on_fractals(df, self.period_max, self.kind, self.period_fractal)
        df = add_mean_on_fractals(df, self.period_max,self.kind,self.period_fractal)
        df['oversold1'] = df[self.kind] < df['bottom_mean']
        df['overbought1'] = df[self.kind] > df['top_mean']
        df['oversold2'] = df[self.kind] < df['bottom_ext']
        df['overbought2'] = df[self.kind] > df['top_ext']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['top_ext'] > row['bottom_ext']:
            if row['oversold2']:
                return 'open_long'
            if row['overbought2']:
                return 'open_short'
        
        if row['oversold1']:
            return 'close_short'
        if row['overbought1']:
            return 'close_long'
        
        return None
        
class LEG1_IRONANNY(BaseEG):
    """stop=None, take=None, period=15, period_fractal=10, period_max=5, solution=5"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_fractal=10, period_max=55, solution=5):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.solution = solution
        self.period_fractal = period_fractal
        self.period_max = period_max
        self.problems = 'Mcfly'

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
        df = add_stochastic(df, self.period, self.period // 2)
        df = add_fractals(df, self.period_fractal)
        inds = ('cmo', 'rsi', 'rsi_tw', 'williams_r', 'mfi', 'ultimate_oscillator', 'cci', '%d')
        df['oversold'] = 0
        df['overbought'] = 0
        for i, ind in enumerate(inds):
            df = add_mean_on_fractals(df, self.period_max, ind,self.period_fractal)
            df['oversold'] += df[ind] < df['bottom_mean']
            df['overbought'] += df[ind] > df['top_mean']
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
    """stop=None, take=None, period=10, multiplier=3, period_mvol=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, multiplier=3, period_mvol=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
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
    """stop=None, take=None, period=10, multiplier=3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, multiplier=3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
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
        df = add_ema(df, self.period)
        df['local_max'] = df['close'].rolling(window=self.period2).max()
        df['local_min'] = df['close'].rolling(window=self.period2).min()
        df['nearest_long'] = df['high'] - df['close'] > df['close'] - df['low']
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['low'] <= df['local_min']) & (df['close'] > df['ema']) & (df['nearest_long'] == True), 'signal'] = 1  # Покупка
        df.loc[(df['high'] >= df['local_max']) & (df['close'] < df['ema']) & (df['nearest_long'] == False), 'signal'] = -1  # Продажа

        df = self.add_slice_df(df)
        # df[df['signal'] != 0].info()
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'
        
        return None