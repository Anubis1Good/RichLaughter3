from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_bollinger,add_adx,add_sma,add_rsi,add_ema
from for_strategies.zigzag_indicators import add_percent_zz190826
from for_strategies.help_indicators import add_big_volume,add_over_bb
from for_strategies.pva_indicators import add_simple_dynamics_ma,add_pc_stair_fast

class SEG1_LITE(BaseEG):
    """stop=None, take=None, period=20, multiplier=2, slope=0.5, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, multiplier=2, slope=0.5, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.multiplier = multiplier
        self.slope = slope
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_sma(df, self.period2)
        df = df.rename(columns={'sma': 'sma2'})
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_big_volume(df, self.period)
        df = add_over_bb(df)
        sdm_period = max(3, self.period2 // 3)
        df = add_simple_dynamics_ma(df, sdm_period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['sdm'] >= self.slope:
            if row['high'] > row['bbu'] and row['is_big']:
                return 'close_long'
            if row['over_bbu']:
                return 'close_long'
            if row['low'] < row['sma'] and row['sma2'] > row['sma']:
                return 'open_long'
        elif row['sdm'] <= -self.slope:
            if row['over_bbd']:
                return 'close_short'
            if row['low'] < row['bbd'] and row['is_big']:
                return 'close_short'
            if row['high'] > row['sma'] and row['sma2'] < row['sma']:
                return 'open_short'
        
        return None

class SEG2(BaseEG):
    """stop=None, take=None, period=55, n_stairs=3, period2=55,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=55,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        max_total = (max_period // 3) * 2
        total = period + period2

        if total > max_total:
            ratio = max_total / total
            self.period = int(period * ratio)
            self.period2 = int(period2 * ratio)
        else:
            self.period = period
            self.period2 = period2
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period2)
        df = add_bollinger(df, self.period2)
        df = add_big_volume(df, self.period2, 3)
        df = add_over_bb(df)
        df = add_rsi(df, self.period2)
        df['sma_delta'] = df['sma'].pct_change()
        df['dynamic_sma'] = df['sma_delta'].rolling(self.period).mean()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        go_long = row['close'] > row['stair']
        
        if go_long and row['dynamic_sma'] < -0.00001:
            return 'close_long'
        if not go_long and row['dynamic_sma'] > 0.00001:
            return 'close_short'
        
        if row['high'] > row['bbu'] and (row['is_big'] or row['over_bbu'] or row['rsi'] > 85):
            return 'close_long'
        
        if row['low'] < row['bbd'] and (row['is_big'] or row['over_bbd'] or row['rsi'] < 15):
            return 'close_short'
        
        if row['low'] < row['sma'] and go_long and row['dynamic_sma'] > 0:
            return 'open_long'
        
        if row['high'] > row['sma'] and not go_long and row['dynamic_sma'] < 0:
            return 'open_short'
        
        return None
        
class SEG2_FAST(BaseEG):
    """stop=None, take=None, period_adx=27, n_stairs=3, trend_period=55, adx_threshold=25"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=27, n_stairs=3, trend_period=55, adx_threshold=25):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.trend_period = trend_period
        self.n_stairs = n_stairs
        self.adx_threshold = adx_threshold
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, period=self.trend_period)
        df = add_ema(df, period=self.trend_period // 2)
        df = add_pc_stair_fast(df, self.n_stairs, self.trend_period)
        df = add_adx(df, self.period_adx)
        df['bbu_detach'] = (df['high'] < df['bbu']) & (df['high'].shift(1) < df['bbu'].shift(1)) & (df['high'].shift(2) > df['bbu'].shift(2))
        df['bbd_detach'] = (df['low'] > df['bbd']) & (df['low'].shift(1) > df['bbd'].shift(1)) & (df['low'].shift(2) < df['bbd'].shift(2))
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        go_long = row['close'] > row['stair']
        
        if row['adx'] > self.adx_threshold:
            if row['low'] < row['ema'] and go_long:
                return 'open_long'
            if row['high'] > row['ema'] and not go_long:
                return 'open_short'
        
        if go_long:
            if row['bbu_detach']:
                return 'close_long'
        else:
            if row['bbd_detach']:
                return 'close_short'
        
        return None

class SEG2_ULTRA(BaseEG):
    """stop=None, take=None, period_adx=27, n_stairs=3, period2=55, adx_threshold=25,period_dsma=25,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=27, n_stairs=3, period2=55, adx_threshold=25,period_dsma=25,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.n_stairs = n_stairs
        self.adx_threshold = adx_threshold
        max_total = (max_period // 3) * 2
        total = period2 + period_dsma

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period_dsma = int(period_dsma * ratio)
        else:
            self.period2 = period2
            self.period_dsma = period_dsma
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period2)
        df = add_bollinger(df, self.period2)
        df = add_big_volume(df, self.period2, 3)
        df = add_over_bb(df)
        df = add_adx(df, self.period_adx)
        df = add_rsi(df, self.period2)
        df['sma_delta'] = df['sma'].pct_change()
        df['dynamic_sma'] = df['sma_delta'].rolling(self.period2).mean()
        df['bbu_detach'] = (df['high'] < df['bbu']) & (df['high'].shift(1) < df['bbu'].shift(1)) & (df['high'].shift(2) > df['bbu'].shift(2))
        df['bbd_detach'] = (df['low'] > df['bbd']) & (df['low'].shift(1) > df['bbd'].shift(1)) & (df['low'].shift(2) < df['bbd'].shift(2))
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        go_long = row['close'] > row['stair']
        
        if go_long and row['dynamic_sma'] < -0.00001:
            return 'close_long'
        if not go_long and row['dynamic_sma'] > 0.00001:
            return 'close_short'
        
        if row['high'] > row['bbu'] and (row['is_big'] or row['over_bbu'] or row['rsi'] > 90):
            return 'close_long'
        
        if row['low'] < row['bbd'] and (row['is_big'] or row['over_bbd'] or row['rsi'] < 10):
            return 'close_short'
        
        if go_long and row['bbu_detach']:
            return 'close_long'
        if not go_long and row['bbd_detach']:
            return 'close_short'
        
        if row['adx'] > self.adx_threshold:
            if row['low'] < row['sma'] and go_long and row['dynamic_sma'] > 0:
                return 'open_long'
            if row['high'] > row['sma'] and not go_long and row['dynamic_sma'] < 0:
                return 'open_short'
        
        return None

class SEG3_FORCE(BaseEG):
    """stop=None, take=None, period=55, mult_bb=2, mult_bv=3, period_adx=30, threshold_adx=30, period_sma=55,percent_threshold=0.3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, mult_bb=2, mult_bv=3, period_adx=30, threshold_adx=30, period_sma=55,percent_threshold=0.3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.mult_bb = mult_bb
        self.mult_bv = mult_bv
        self.period_adx = period_adx
        self.threshold_adx = threshold_adx
        self.period_sma = period_sma
        self.percent_threshold = percent_threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_percent_zz190826(df, percent_threshold=self.percent_threshold,drop_last=False)
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_big_volume(df, self.period, self.mult_bv)
        df = add_over_bb(df)
        df = add_adx(df, self.period_adx)
        df['ma'] = df['close'].rolling(self.period_sma).mean()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        go_long = row['zigzag_direction'] == 1
        
        if row['high'] > row['bbu'] and (row['is_big'] or row['over_bbu']):
            return 'close_long'
        
        if row['low'] < row['bbd'] and (row['is_big'] or row['over_bbd']):
            return 'close_short'
        
        if row['adx'] > self.threshold_adx:
            if row['low'] < row['ma'] and go_long:
                return 'open_long'
            if row['high'] > row['ma'] and not go_long:
                return 'open_short'
        
        return None