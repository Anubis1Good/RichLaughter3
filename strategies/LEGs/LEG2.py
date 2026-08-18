from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_donchan_channel,add_bollinger,add_rsi,add_chop,add_adx
from for_strategies.pva_indicators import add_static_channel,add_vodka_channel
from for_strategies.help_indicators import add_buffer_add

class LEG2_HOTS(BaseEG):
    """stop=None, take=None,period=100,multiplier=2,period2=10,threshold_enter=40,threshold_exit=20,use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,period=55,multiplier=2,period2=10,threshold_enter=40,threshold_exit=20,use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df = add_donchan_channel(df,self.period2)
        df = add_rsi(df,self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None
            
class LEG2_LOGAN(BaseEG):
    """stop=None, take=None, period=100, period2=50, threshold=50"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period2=50, threshold=50):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.threshold = threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_static_channel(df, self.period)
        df = add_chop(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['chop'] > self.threshold:
            if row['top_line'] < row['close']:
                return 'open_short'
            if row['bottom_line'] > row['close']:
                return 'open_long'
            if row['center_line'] > row['close']:
                return 'close_short'
            if row['center_line'] < row['close']:
                return 'close_long'
        else:
            return 'close_all'
        
        return None
        
class LEG2_DRINKER(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_vodka_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['bottom_mean'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['top_mean'] and not nearest_long:
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class LEG2_ALKASH(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, multiplier=2, period2=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_vodka_channel(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['bottom_mean'] and nearest_long:
            if can_long:
                return 'open_long'
            else:
                return 'close_short'
        
        if row['high'] >= row['top_mean'] and not nearest_long:
            if can_short:
                return 'open_short'
            else:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class LEG2_FENNEC(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, divider=1, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, divider=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        self.divider = divider

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_vodka_channel(df, self.period2)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['bottom_buff'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['top_buff'] and not nearest_long:
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class LEG2_LYNX(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, divider=1, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, multiplier=2, period2=10, divider=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.use_stop = use_stop
        self.divider = divider

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_vodka_channel(df, self.period2)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['bottom_buff'] and nearest_long:
            if can_long:
                return 'open_long'
            else:
                return 'close_short'
        
        if row['high'] >= row['top_buff'] and not nearest_long:
            if can_short:
                return 'open_short'
            else:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class LEG2_MONSTER(BaseEG):
    """stop=None, take=None, period=20, threshold=30, period2=10, shift=2, period_adx=30,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30, period2=10, shift=2, period_adx=30,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        max_total = (max_period // 3) * 2
        total = period + period_adx

        if total > max_total:
            ratio = max_total / total
            self.period = int(period * ratio)
            self.period_adx = int(period_adx * ratio)
        else:
            self.period = period
            self.period_adx = period_adx
        self.threshold = threshold
        self.period2 = period2
        self.shift = shift
        self.type_eg = 1

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma_adx'] = df['adx'].rolling(self.period).mean()
        df = add_donchan_channel(df, self.period2)
        df['stop_long'] = df['low'].shift(self.shift)
        df['stop_short'] = df['high'].shift(self.shift)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if self.threshold < row['adx'] > row['sma_adx']:
            if row['high'] == row['max_hb']:
                return 'open_long'
            if row['low'] == row['min_hb']:
                return 'open_short'
            if row['close'] < row['stop_long']:
                return 'close_long'
            if row['close'] > row['stop_short']:
                return 'close_short'
        
        return 'close_all'

class LEG2_DRG(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20,  use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20,  use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if can_long and can_short:
            if row['low'] <= row['min_hb'] and nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        elif can_long and not can_short:
            if row['close'] <= row['avarege']:
                return 'open_long'
        
        if can_short and can_long:
            if row['high'] >= row['max_hb'] and not nearest_long:
                if can_short and row['rsi'] > 100 - self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
        elif can_short and not can_long:
            if row['close'] >= row['avarege']:
                return 'open_short'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None