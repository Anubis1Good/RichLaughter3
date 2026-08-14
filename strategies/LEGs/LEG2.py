from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_donchan_channel,add_bollinger,add_rsi,add_chop,add_adx
from for_strategies.pva_indicators import add_static_channel,add_vodka_channel
from for_strategies.help_indicators import add_buffer_add

class LEG2_HOTS(BaseEG):
    """stop=None, take=None,period=100,multiplier=2,period2=10,threshold_enter=40,threshold_exit=20,shift=10,use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,period=100,multiplier=2,period2=10,threshold_enter=40,threshold_exit=20,shift=10,use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df,self.period,multiplier=self.multiplier)
        df['bbu'] = df['bbu'].shift(self.shift)
        df['bbd'] = df['bbd'].shift(self.shift)
        df['sma'] = df['sma'].shift(self.shift)
        df = add_donchan_channel(df,self.period2)
        df = add_rsi(df,self.period2)
        df = self.add_slice_df(df,self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self,pdata):
        row = self.get_test_row(pdata['chart'])
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        if row['high'] >= row['max_hb']:
            if not nearest_long :
                if can_short and row['rsi'] > 100-self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100-self.threshold_exit:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
            
class LEG2_LOGAN(BaseEG):
    """stop=None, take=None, period=100, period2=50, threshold=50"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, period2=50, threshold=50):
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
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
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
        
class LEG2_DRINKER(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df['bbu'] = df['bbu'].shift(self.shift)
        df['bbd'] = df['bbd'].shift(self.shift)
        df['sma'] = df['sma'].shift(self.shift)
        df = add_vodka_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['bottom_mean']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        if row['high'] >= row['top_mean']:
            if not nearest_long:
                if can_short and row['rsi'] > 100 - self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'

class LEG2_ALKASH(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, multiplier=2, period2=10, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.shift = shift
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df['bbu'] = df['bbu'].shift(self.shift)
        df['bbd'] = df['bbd'].shift(self.shift)
        df['sma'] = df['sma'].shift(self.shift)
        df = add_vodka_channel(df, self.period2)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['bottom_mean']:
            if nearest_long:
                if can_long:
                    return 'open_long'
                else:
                    return 'close_short'
        if row['high'] >= row['top_mean']:
            if not nearest_long:
                if can_short:
                    return 'open_short'
                else:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'

class LEG2_FENNEC(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, shift=10, divider=1, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, shift=10, divider=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop
        self.divider = divider

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df['bbu'] = df['bbu'].shift(self.shift)
        df['bbd'] = df['bbd'].shift(self.shift)
        df['sma'] = df['sma'].shift(self.shift)
        df = add_vodka_channel(df, self.period2)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['bottom_buff']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        if row['high'] >= row['top_buff']:
            if not nearest_long:
                if can_short and row['rsi'] > 100 - self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'

class LEG2_LYNX(BaseEG):
    """stop=None, take=None, period=100, multiplier=2, period2=10, shift=10, divider=1, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, multiplier=2, period2=10, shift=10, divider=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.shift = shift
        self.use_stop = use_stop
        self.divider = divider

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df['bbu'] = df['bbu'].shift(self.shift)
        df['bbd'] = df['bbd'].shift(self.shift)
        df['sma'] = df['sma'].shift(self.shift)
        df = add_vodka_channel(df, self.period2)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['bottom_buff']:
            if nearest_long:
                if can_long:
                    return 'open_long'
                else:
                    return 'close_short'
        if row['high'] >= row['top_buff']:
            if not nearest_long:
                if can_short:
                    return 'open_short'
                else:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'

class LEG2_MONSTER(BaseEG):
    """stop=None, take=None, period=20, threshold=30, period2=10, shift=2, period_adx=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30, period2=10, shift=2, period_adx=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        self.period2 = period2
        self.shift = shift
        self.period_adx = period_adx

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma_adx'] = df['adx'].rolling(self.period).mean()
        df = add_donchan_channel(df, self.period2)
        df['stop_long'] = df['low'].shift(self.shift)
        df['stop_short'] = df['high'].shift(self.shift)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
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
    """stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, multiplier=2, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.multiplier)
        df['bbu'] = df['bbu'].shift(self.shift)
        df['bbd'] = df['bbd'].shift(self.shift)
        df['sma'] = df['sma'].shift(self.shift)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        can_long = row['close'] > row['bbd']
        can_short = row['close'] < row['bbu']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if can_long:
            if can_short:
                if row['low'] <= row['min_hb']:
                    if nearest_long:
                        if can_long and row['rsi'] < self.threshold_enter:
                            return 'open_long'
                    if row['rsi'] < self.threshold_exit:
                        return 'close_short'
            else:
                if row['close'] <= row['avarege']:
                    return 'open_long'
        if can_short:
            if can_long:
                if row['high'] >= row['max_hb']:
                    if not nearest_long:
                        if can_short and row['rsi'] > 100 - self.threshold_enter:
                            return 'open_short'
                        if row['rsi'] > 100 - self.threshold_exit:
                            return 'close_long'
            else:
                if row['close'] >= row['avarege']:
                    return 'open_short'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'