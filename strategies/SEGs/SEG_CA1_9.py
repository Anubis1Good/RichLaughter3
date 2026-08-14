from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_bollinger,add_adx
from for_strategies.zigzag_indicators import add_precent_zigzag
from for_strategies.help_indicators import add_big_volume,add_over_bb

class SEG3_FORCE(BaseEG):
    """stop=None, take=None, period=60, divider_percent=5, mult_bb=2, mult_bv=3, period_adx=30, threshold=30, period_sma=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, divider_percent=5, mult_bb=2, mult_bv=3, period_adx=30, threshold=30, period_sma=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.divider_percent = divider_percent
        self.mult_bb = mult_bb
        self.mult_bv = mult_bv
        self.period_adx = period_adx
        self.threshold = threshold
        self.period_sma = period_sma

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df_slice = df.copy().iloc[-200:] if len(df.index) > 200 else df.copy()
        cur_percent = ((df_slice['high'].max() - df_slice['low'].min()) / df_slice['low'].min() * 100) / self.divider_percent
        df = add_precent_zigzag(df, reversal=cur_percent)
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_big_volume(df, self.period, self.mult_bv)
        df = add_over_bb(df)
        df = add_adx(df, self.period_adx)
        df['ma'] = df['close'].rolling(self.period_sma).mean()
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        go_long = row['zigzag_direction'] == 1
        if row['high'] > row['bbu']:
            if row['is_big'] or row['over_bbu']:
                return 'close_long'
        if row['low'] < row['bbd']:
            if row['is_big'] or row['over_bbd']:
                return 'close_short'
        if row['adx'] > self.threshold:
            if row['low'] < row['ma'] and go_long:
                return 'open_long'
            if row['high'] > row['ma'] and not go_long:
                return 'open_short'