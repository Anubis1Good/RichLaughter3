from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_donchan_channel
        
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
    
    def get_raw_action(self,pdata):
        row = self.get_test_row(pdata['chart'])
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        if row['low'] <= row['min_hb'] and nearest_long:
            return 'open_long'
        if row['high'] >= row['max_hb'] and not nearest_long:
            return 'open_short'
    
