from strategies.BaseEG import BaseEG


class PEG2_BDDC_FIX(BaseEG):
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, stop=None, take=None):
        super().__init__(symbol, price_step, mult_ps, stop, take)
        
# class PTA2_BDDC_FIX(BaseTABitget):
#     """period=20,can_long=True,can_short=True"""
#     def __init__(self, symbol="BTCUSDT", granularity="1m", productType="usdt-futures", n_parts=1, period=20,can_long=True,can_short=True):
#         super().__init__(symbol, granularity, productType, n_parts, period)
#         self.can_long = can_long
#         self.can_short = can_short
#     def preprocessing(self,df):
#         df = add_donchan_channel(df,self.period)
#         df = add_enter_price2close(df)
#         df = add_slice_df(df,period=self.period)
#         return df
    
#     def __call__(self,row, *args, **kwds):
#         if row['high'] >= row['max_hb']:
#             if self.can_long:
#                 return 'long_pw'
#         if row['low'] <= row['min_hb']:
#             if self.can_short:
#                 return 'short_pw'
#         if row['low'] < row['avarege']:
#             return "close_long_pw"
#         if row['high'] > row['avarege']:
#             return "close_short_pw"

