from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_fractals
from for_strategies.pva_indicators import add_average_fractals

class UEG2_GGD(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        if row['close'] >= row['ave_up']:
            return 'open_short'
        if row['close'] <= row['ave_down']:
            return 'open_long'