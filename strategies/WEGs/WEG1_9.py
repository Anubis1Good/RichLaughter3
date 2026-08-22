from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_fractals
from for_strategies.pva_indicators import add_mean_on_fractals
from for_strategies.vsa_indicators import add_CDV,add_cdvsai,add_dvsai

class WEG4_DOG(BaseEG):
    """stop=None, take=None, period=14, threshold=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=14, threshold=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_CDV(df)
        df = add_rsi(df, self.period, 'cdv')
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['rsi'] < self.threshold:  
            return 'open_long'
        if row['rsi'] > 100 - self.threshold:  
            return 'open_short'

class WEG4_PUPPY(BaseEG):
    """stop=None, take=None, period=14, threshold_enter=30, threshold_exit=40"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=14, threshold_enter=30, threshold_exit=40):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_CDV(df)
        df = add_rsi(df, self.period, 'cdv')
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['rsi'] < self.threshold_enter:  
            return 'open_long'
        if row['rsi'] > 100 - self.threshold_enter:  
            return 'open_short'
        if row['rsi'] < self.threshold_exit:  
            return 'close_short'
        if row['rsi'] > 100 - self.threshold_exit:  
            return 'close_long'
        
class WEG4_RAT(BaseEG):
    """stop=None, take=None, period=14, period_fractal=5, period_max=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=14, period_fractal=5, period_max=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_fractal = period_fractal
        self.period_max = period_max
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cdvsai(df, period=self.period)
        df = add_rsi(df, self.period, 'cum_dvsai')
        df = add_fractals(df, self.period_fractal)
        df = add_mean_on_fractals(df, self.period_max, 'rsi',self.period_fractal)
        df['oversold'] = df['rsi'] < df['bottom_mean']
        df['overbought'] = df['rsi'] > df['top_mean']
        df = self.add_slice_df(df)
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['oversold']:  
            return 'open_long'
        if row['overbought']:  
            return 'open_short'

class WEG7_PARADOX(BaseEG):
    """stop=None, take=None, period=14, mult=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=14, mult=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.mult = mult

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dvsai(df, self.period, self.mult)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['dvsai'] < row['dvsaid']:  
            return 'open_long'
        if row['dvsai'] > row['dvsaiu']:  
            return 'open_short'
        
class WEG3_DS(BaseEG):
    """stop=None, take=None, period=20, mult_spred = 1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, mult_spred = 1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.mult_spred = mult_spred

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['spread'] = df['high'] - df['low']

        # Вычисление среднего объема и спреда
        df['avg_volume'] = df['volume'].rolling(window=self.period).mean()
        df['avg_spread'] = df['spread'].rolling(window=self.period).mean()

        # Генерация сигналов
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[(df['volume'] > df['avg_volume']) & (df['spread'] < self.mult_spred * df['avg_spread']) & (df['close'] > df['open']), 'signal'] = 1  # Покупка
        df.loc[(df['volume'] > df['avg_volume']) & (df['spread'] < self.mult_spred * df['avg_spread']) & (df['close'] < df['open']), 'signal'] = -1  # Продажа
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
      
class WEG3_BATYA(BaseEG):
    """stop=None, take=None, period=20, mult_spred = 2, sign_vol=0, sign_spred=0,sign_dir=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, mult_spred = 2, sign_vol=0, sign_spred=0,sign_dir=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.mult_spred = mult_spred
        self.sign_vol = sign_vol
        self.sign_spred = sign_spred
        self.sign_dir = sign_dir
        
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['spread'] = df['high'] - df['low']
        # Вычисление среднего объема и спреда
        df['avg_volume'] = df['volume'].rolling(window=self.period).mean()
        df['avg_spread'] = df['spread'].rolling(window=self.period).mean()
        condition = (df['volume'] < df['avg_volume']) if self.sign_vol == 0 else (df['volume'] > df['avg_volume'])
        condition &= (df['spread'] > self.mult_spred * df['avg_spread']) if self.sign_spred else (df['spread'] < self.mult_spred * df['avg_spread'])
        # Генерация сигналов
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[condition & (df['close'] > df['open']), 'signal'] = 1 if self.sign_dir == 0 else -1 # Покупка
        df.loc[condition & (df['close'] < df['open']), 'signal'] = -1 if self.sign_dir == 0 else 1 # Продажа
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'