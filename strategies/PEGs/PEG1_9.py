from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_donchan_channel,add_bollinger,add_rsi_tw,add_mfi,add_stochastic,add_ultimate_oscillator,add_rsi,add_fractals
from for_strategies.pva_indicators import add_smooth_channel,add_vodka_channel,add_mean_on_fractals
from for_strategies.other_indicators import add_vangerchik
from for_strategies.help_indicators import add_buffer_add,add_over_bb,add_big_volume
        
class PEG2_DDCrWork(BaseEG):
    "stop=None, take=None,period=20"
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,period=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.period = period

    def preprocessing(self,tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df,self.period)
        df = self.add_slice_df(df,self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        """Только логика!"""
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            return 'open_long'
        if row['high'] >= row['max_hb'] and not nearest_long:
            return 'open_short'
        return None
    
class PEG2_SDDCr(BaseEG):
    """stop=None, take=None, period=20, period2=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period2=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period)
        df = add_smooth_channel(df, self.period2)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            return 'open_long'
        if row['high'] >= row['max_hb']:
            return 'open_short'
        return None
    
class PEG4_UNIVERSAL(BaseEG):
    '''
    stop=None, take=None, period=20, period_rsi=20, threshold_long=30, threshold_short=30
    kind_channel in ["DC","VG","BB","VC","WC"]
    kind_rsi in ["rsi","rsi_tw","mfi","s","uo"]
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_rsi=20, threshold_long=30, threshold_short=30, kind_channel='DC', kind_rsi='rsi'):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold_long = threshold_long
        self.threshold_short = threshold_short
        self.period_rsi = period_rsi
        self.kind_channel = kind_channel
        self.kind_rsi = kind_rsi
        self.rsi = 'rsi'
        self.up = 'up'
        self.down = 'down'

    def add_channel(self, df):
        if self.kind_channel == 'VG':
            df = add_donchan_channel(df, self.period)
            df = add_vangerchik(df)
            df = df.rename({'max_vg': self.up, 'min_vg': self.down}, axis=1)
        elif self.kind_channel == 'BB':
            df = add_bollinger(df, self.period)
            df = df.rename({'bbu': self.up, 'bbd': self.down}, axis=1)
        elif self.kind_channel == 'VC':
            df = add_vodka_channel(df, self.period)
            df = df.rename({'top_mean': self.up, 'bottom_mean': self.down}, axis=1)
        elif self.kind_channel == 'WC':
            df = add_vodka_channel(df, self.period)
            df = add_buffer_add(df, 'top_mean', 'bottom_mean', 2)
            df = df.rename({'top_buff': self.up, 'bottom_buff': self.down}, axis=1)
        else:
            df = add_donchan_channel(df, self.period)
            df = df.rename({'max_hb': self.up, 'min_hb': self.down}, axis=1)
        return df
    
    def add_rsi(self, df):
        if self.kind_rsi == 'rsi_tw':
            df = add_rsi_tw(df, self.period_rsi)
            df = df.rename({'rsi_tw': 'rsi'}, axis=1)
        elif self.kind_rsi == 'mfi':
            df = add_mfi(df, self.period_rsi)
            df = df.rename({'mfi': 'rsi'}, axis=1)
        elif self.kind_rsi == 's':
            df = add_stochastic(df, self.period_rsi, self.period_rsi // 3)
            df = df.rename({'%d': 'rsi'}, axis=1)
        elif self.kind_rsi == 'uo':
            df = add_ultimate_oscillator(df, self.period_rsi // 3, self.period_rsi // 2, self.period_rsi)
            df = df.rename({'ultimate_oscillator': 'rsi'}, axis=1)
        else:
            df = add_rsi(df, self.period_rsi)
        return df
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = self.add_channel(df)
        df = self.add_rsi(df)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row[self.down]:
            if nearest_long:
                if row['rsi'] < self.threshold_long:
                    if self.can_long:
                        return 'open_long'
                    else:
                        return 'close_short'
        
        if row['high'] >= row[self.up]:
            if row['rsi'] > 100 - self.threshold_short:
                if self.can_short:
                    return 'open_short'
                else:
                    return 'close_long'
        
        return None
                
class PEG4_U3(BaseEG):
    '''
    stop=None, take=None, period=20, period_rsi=20, period_fractal=10, period_mean=5
    kind_channel in ["DC","VG","BB","VC","WC"]
    kind_rsi in ["rsi","rsi_tw","mfi","s","uo"]
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_rsi=20, period_fractal=10, period_mean=5, kind_channel='DC', kind_rsi='rsi'):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_fractal = period_fractal
        self.period_mean = period_mean
        self.period_rsi = period_rsi
        self.kind_channel = kind_channel
        self.kind_rsi = kind_rsi
        self.rsi = 'rsi'
        self.up = 'up'
        self.down = 'down'

    def add_channel(self, df):
        if self.kind_channel == 'VG':
            df = add_donchan_channel(df, self.period)
            df = add_vangerchik(df)
            df = df.rename({'max_vg': self.up, 'min_vg': self.down}, axis=1)
        elif self.kind_channel == 'BB':
            df = add_bollinger(df, self.period)
            df = df.rename({'bbu': self.up, 'bbd': self.down}, axis=1)
        elif self.kind_channel == 'VC':
            df = add_vodka_channel(df, self.period)
            df = df.rename({'top_mean': self.up, 'bottom_mean': self.down}, axis=1)
        elif self.kind_channel == 'WC':
            df = add_vodka_channel(df, self.period)
            df = add_buffer_add(df, 'top_mean', 'bottom_mean', 2)
            df = df.rename({'top_buff': self.up, 'bottom_buff': self.down}, axis=1)
        else:
            df = add_donchan_channel(df, self.period)
            df = df.rename({'max_hb': self.up, 'min_hb': self.down}, axis=1)
        return df
    
    def add_rsi(self, df):
        if self.kind_rsi == 'rsi_tw':
            df = add_rsi_tw(df, self.period_rsi)
            df = df.rename({'rsi_tw': 'rsi'}, axis=1)
        elif self.kind_rsi == 'mfi':
            df = add_mfi(df, self.period_rsi)
            df = df.rename({'mfi': 'rsi'}, axis=1)
        elif self.kind_rsi == 's':
            df = add_stochastic(df, self.period_rsi, self.period_rsi // 3)
            df = df.rename({'%d': 'rsi'}, axis=1)
        elif self.kind_rsi == 'uo':
            df = add_ultimate_oscillator(df, self.period_rsi // 3, self.period_rsi // 2, self.period_rsi)
            df = df.rename({'ultimate_oscillator': 'rsi'}, axis=1)
        else:
            df = add_rsi(df, self.period_rsi)
        return df
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = self.add_channel(df)
        df = self.add_rsi(df)
        df = add_fractals(df, self.period_fractal)
        df = add_mean_on_fractals(df, self.period_mean, 'rsi')
        df['oversold'] = df['rsi'] < df['bottom_mean']
        df['overbought'] = df['rsi'] > df['top_mean']
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['low'] <= row[self.down] and row['oversold']:
            return 'open_long'
        if row['high'] >= row[self.up] and row['overbought']:
            return 'open_short'
        return None

class PEG8_DOBBY(BaseEG):
    """stop=None, take=None, period=20, multiplier=2"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, multiplier=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.multiplier = multiplier

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df, self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] > row['bbu'] and (row['is_big'] or row['over_bbu']):
            return 'open_short'
        
        if row['low'] < row['bbd'] and (row['is_big'] or row['over_bbd']):
            return 'open_long'
        
        if row['low'] < row['sma'] and row['is_big']:
            return 'close_short'
        
        if row['high'] > row['sma'] and row['is_big']:
            return 'close_long'
        
        return None

class PEG8_LOBSTER(BaseEG):
    """stop=None, take=None, period=20, multiplier=2"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, multiplier=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.multiplier = multiplier
        self.type_eg = 1

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_over_bb(df)
        df = add_big_volume(df, self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # Приоритет: закрытие по экстремальным условиям
        if row['over_bbu']:
            return 'close_long'
        if row['over_bbd']:
            return 'close_short'
        
        # Основные сигналы (когда цена внутри канала)
        if row['high'] > row['bbu'] and row['is_big']:
            return 'open_long'
        if row['low'] < row['bbd'] and row['is_big']:
            return 'open_short'
        
        # Закрытие по SMA
        if row['low'] < row['sma'] and row['is_big']:
            return 'close_long'
        if row['high'] > row['sma'] and row['is_big']:
            return 'close_short'
        
        return None
            
