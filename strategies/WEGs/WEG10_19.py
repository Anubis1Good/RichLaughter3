import numpy as np
import pandas as pd
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_donchan_channel,add_adx,add_bollinger
from for_strategies.vsa_indicators import add_reversal_patterns
from for_strategies.fix_params import fix_three_periods_hm,fix_two_periods_hm

class WEG10_sleep(BaseEG):
    """stop=None, take=None, period_bb=20, mult_bb = 2,period_big_bar=20,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=20, mult_bb = 2,period_big_bar=20,max_period=55,close_sma=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.mult_bb = mult_bb
        self.period_bb,self.period_big_bar = fix_two_periods_hm(period_bb,period_big_bar,max_period)
        self.close_long = 'sma' if close_sma else 'bbu'
        self.close_short = 'sma' if close_sma else 'bbd'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df,self.period_bb,multiplier=self.mult_bb)
        df['spred'] = df['high'] - df['low']
        df['big_spred'] = df['spred'].rolling(self.period_big_bar).max()
        df['big_volume'] = df['volume'].rolling(self.period_big_bar).max()
        df['is_big_bar'] = (df['big_spred'] == df['spred']) | (df['big_volume'] == df['volume'])
        df['signal'] = np.where(
            (df['low'].shift(1) < df['low']) &
            (df['is_big_bar'].shift(1)),
            1,0
        )
        df['signal'] = np.where(
            (df['high'].shift(1) > df['high']) &
            (df['is_big_bar'].shift(1)),
            -1,0
        )
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            if row['close'] <= row['bbd']:
                return 'open_long'
            if row['close'] >= row['sma']:
                return 'close_long'
        if row['signal'] == -1:
            if row['close'] >= row['bbu']:
                return 'open_short'
            if row['close'] <= row['sma']:
                return 'close_short'
        if row['close'] >= row[self.close_long]:
            return 'close_long'
        if row['close'] <= row[self.close_short]:
            return 'close_short'
        
class WEG10_(BaseEG):
    """stop=None, take=None, period_bb=20, mult_bb = 2,period_big_bar=20,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=20, mult_bb = 2,period_big_bar=20,max_period=55,close_sma=1, quantile=0.7):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.mult_bb = mult_bb
        self.quantile = quantile
        self.period_bb,self.period_big_bar = fix_two_periods_hm(period_bb,period_big_bar,max_period)
        self.close_long = 'sma' if close_sma else 'bbu'
        self.close_short = 'sma' if close_sma else 'bbd'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df,self.period_bb,multiplier=self.mult_bb)
        df['spred'] = df['high'] - df['low']
        df['big_spred'] = df['spred'].rolling(self.period_big_bar).quantile(self.quantile)
        df['big_volume'] = df['volume'].rolling(self.period_big_bar).quantile(self.quantile)
        df['is_big_bar'] = (df['big_spred'] == df['spred']) | (df['big_volume'] == df['volume'])
        df = add_reversal_patterns(df)
        df['signal'] = np.where(
            (df['direction'] == -1) &
            (df['is_big_bar'].shift(1)),
            1,0
        )
        df['signal'] = np.where(
            (df['direction'] == 1) &
            (df['is_big_bar'].shift(1)),
            -1,0
        )
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1 and row['bbd'] >= row['low']:
            return 'open_long'
        if row['signal'] == -1 and row['bbu'] <= row['high']:
            return 'open_short'
        if row['close'] >= row[self.close_long]:
            return 'close_long'
        if row['close'] <= row[self.close_short]:
            return 'close_short'
