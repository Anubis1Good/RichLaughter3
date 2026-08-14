from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_bollinger,add_rsi

class PEG20_HOGGER(BaseEG):
    """stop=None, take=None, period=100, period2=5, mult_big=2, mult_small=0.5, threshold_enter=40, threshold_exit=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, period2=5, mult_big=2, mult_small=0.5, threshold_enter=40, threshold_exit=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2
        self.mult_big = mult_big
        self.mult_small = mult_small
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['smab'] = df['middle'].rolling(window=self.period).mean()
        std_dev = df['middle'].rolling(window=self.period).std()
        # Вычисляем верхнюю и нижнюю полосы Боллинджера
        df['bbub'] = df['smab'] + (self.mult_big * std_dev)
        df['bbdb'] = df['smab'] - (self.mult_big * std_dev)
        df['mub'] = (df['bbub'] + df['smab']) / 2
        df['mdb'] = (df['bbdb'] + df['smab']) / 2
        df = add_bollinger(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        # nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        # long
        if row['low'] > row['smab']:
            if row['close'] >= row['mub']:
                if row['high'] >= row['bbu'] and row['close'] < row['bbub'] and row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
            else:
                if row['low'] <= row['bbd'] and row['rsi'] < self.threshold_enter:
                    return 'open_long'
            if row['sma'] > row['smab']:
                return 'close_short'
        # short
        if row['high'] < row['smab']:
            if row['close'] <= row['mdb']:
                if row['low'] <= row['bbd'] and row['close'] > row['bbdb'] and row['rsi'] < self.threshold_exit:
                    return 'close_short'
                if row['high'] >= row['bbu'] and row['rsi'] > 100 - self.threshold_enter:
                    return 'open_short'
            if row['sma'] < row['smab']:
                return 'close_long'