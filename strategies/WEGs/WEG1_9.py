from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi
from for_strategies.vsa_indicators import add_CDV

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
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        if row['rsi'] < self.threshold:  
            return 'open_long'
        if row['rsi'] > 100 - self.threshold:  
            return 'open_short'