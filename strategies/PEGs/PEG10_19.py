from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_chop
from for_strategies.pva_indicators import add_kusuruken_channel

class PEG11_KUSURUKEN(BaseEG):
    """stop=None, take=None, period=60, period2=10, period3=20, threshold=20, kind_enter='hl'
    kind_enter -> hl | c
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, period2=10, period3=20, threshold=20, kind_enter='hl'):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.period3 = period3
        self.threshold = threshold
        self.kind_enter_l = 'low' if kind_enter == 'hl' else 'close'
        self.kind_enter_s = 'high' if kind_enter == 'hl' else 'close'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_channel(df, self.period2, self.period)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        # trend_context
        if row['sma'] > row['sma2']: 
            # long_context
            if row["avarege"] > row['avarege2']:
                if row['rsi'] > 100 - self.threshold + 10:
                    return 'close_long'
                if row[self.kind_enter_l] <= row['avarege2']:
                    return 'open_long'
            # short_context
            else:
                if row['rsi'] < self.threshold - 10:
                    return 'close_short'
                if row[self.kind_enter_s] >= row['avarege2']:
                    return 'open_short'
        # range_context
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
            if row['low'] <= row['min_hb']:
                if nearest_long:
                    if row['rsi'] < self.threshold:
                        return 'open_long'
            if row['high'] >= row['max_hb']:
                if row['rsi'] > 100 - self.threshold:
                    return 'open_short'