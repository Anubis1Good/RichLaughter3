
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_adx,add_chop
from for_strategies.help_dtypes.actions_cls import OrderCords

#action large больше не поддерживается VT7
# class PEG30_RAYNOR(BaseEG):
#     """stop=None,take=None,period_adx=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40,work_trend=True,large_open='2',large_close='12',n_large='2'"""
#     def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=0, stop=None, take=None,period_adx=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40,work_trend=True,large_open='2',large_close='12',n_large='2'):
#         super().__init__(symbol, price_step, mult_ps, mode, stop, take)
#         self.needs_info = {'chart':self.symbol}
#         self.period_adx = period_adx
#         self.period_chop = period_chop
#         self.period_sma_l = period_sma_l
#         self.period_sma_s = period_sma_s
#         self.thr_adx = thr_adx
#         self.thr_chop = thr_chop
#         self.work_trend = work_trend
#         self.large_open = large_open
#         self.large_close = large_close
#         self.n_large = n_large
#         self.large_config = 'large_o'+large_open+'_c'+large_close+'_'+n_large
#         self.type_eg = 2
    
#     def preprocessing(self, tdata):
#         pdata = {}
#         df = tdata['chart']
#         df = add_adx(df,self.period_adx)
#         df = add_chop(df,self.period_chop)
#         df['sma_s'] = df['close'].rolling(self.period_sma_s).mean()
#         df['sma_l'] = df['close'].rolling(self.period_sma_l).mean()
#         df = self.add_slice_df(df,self.period_adx)
#         pdata['chart'] = df
#         return pdata
    
#     def get_raw_action(self,pdata):
#         row = self.get_test_row(pdata['chart'])
#         if row['adx'] < self.thr_adx and row['chop'] > self.thr_chop:
#             # print('range')
#             return 'all_'+self.large_config
#         # trend
#         else:
#             if self.work_trend:
#                 # long
#                 if row['sma_s'] > row['sma_l']:
#                     # print('long')
#                     return 'spred_long_'+self.large_config
#                 # short
#                 else:
#                     # print('short')
#                     return 'spred_short_'+self.large_config
#             else:
#                 return 'close_all'
            
class PEG30_MURKY(BaseEG):
    """stop=None, take=None, work_trend=True,min_spred=3,use_long=True,use_short=True,period_adx=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, work_trend=True,min_spred=3,use_long=True,use_short=True,period_adx=14,period_chop=14,period_sma_l=30,period_sma_s=15,thr_adx=25,thr_chop=40):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol,'spred':self.symbol}
        self.period_adx = period_adx
        self.period_chop = period_chop
        self.period_sma_l = period_sma_l
        self.period_sma_s = period_sma_s
        self.thr_adx = thr_adx
        self.thr_chop = thr_chop
        self.work_trend = work_trend
        self.min_spred = min_spred
        self.use_long = use_long
        self.use_short = use_short
        self.type_eg = 2
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df,self.period_adx)
        df = add_chop(df,self.period_chop)
        df['sma_s'] = df['close'].rolling(self.period_sma_s).mean()
        df['sma_l'] = df['close'].rolling(self.period_sma_l).mean()
        df = self.add_slice_df(df,self.period_adx)
        pdata['chart'] = df
        pdata['can_spred'] = tdata['spred'] > self.min_spred
        return pdata
    
    def get_raw_action(self,pdata):
        row = self.get_test_row(pdata['chart'])
        # print(self.symbol,pdata['can_spred'])
        if pdata['can_spred']:
            if row['adx'] < self.thr_adx and row['chop'] > self.thr_chop:
                # print('range')
                if not self.use_long:
                    return 'open_short'
                if not self.use_short:
                    return 'open_long'
                return 'open_all'
            # trend
            else:
                if self.work_trend:
                    # long
                    if row['sma_s'] > row['sma_l'] and self.use_long:
                        # print('long')
                        return 'open_long'
                    # short
                    else:
                        # print('short')
                        if self.use_short:
                            return 'open_short'
                else:
                    return 'close_all'

class PEG31_HYPERION(BaseEG):
    """stop=None, take=None, min_spred=3, work_direction = 0, work_trend=True, large_open=100,large_close=50, n_order=1, min_step=3, period_adx=14, period_chop=14, period_sma_l=30, period_sma_s=15, thr_adx=25, thr_chop=40"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, min_spred=3, work_direction = 0, work_trend=True, large_open=100,large_close=50, n_order=1, min_step=3, period_adx=14, period_chop=14, period_sma_l=30, period_sma_s=15, thr_adx=25, thr_chop=40):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':True,'full_glass':True}
        self.period_adx = period_adx
        self.period_chop = period_chop
        self.period_sma_l = period_sma_l
        self.period_sma_s = period_sma_s
        self.thr_adx = thr_adx
        self.thr_chop = thr_chop
        self.work_trend = work_trend
        self.large_open = large_open
        self.large_close = large_close
        self.n_order = n_order
        self.min_spred = min_spred
        self.min_step = min_step
        self.type_eg = 2
        self.work_direction = work_direction
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df,self.period_adx)
        df = add_chop(df,self.period_chop)
        df['sma_s'] = df['close'].rolling(self.period_sma_s).mean()
        df['sma_l'] = df['close'].rolling(self.period_sma_l).mean()
        df = self.add_slice_df(df,self.period_adx)
        pdata['chart'] = df
        pdata['fg'] = tdata['fg']
        return pdata
    
    def get_raw_action(self,pdata):
        row = self.get_test_row(pdata['chart'])
        fg = pdata['fg']
        # print(self.symbol,fg)
        actions = []
        direction = None
        # range
        if row['adx'] < self.thr_adx and row['chop'] > self.thr_chop:
            print('range')
            direction = 0
        # trend
        else:
            if self.work_trend:
                # long
                if row['sma_s'] > row['sma_l']:
                    print('long')
                    direction = 1
                # short
                else:
                    print('short')
                    direction = -1
        if self.work_direction != 0:
            if direction != self.work_direction:
                if direction == 0:
                    direction = self.work_direction
                else:
                    direction = None
        
        print(self.symbol,direction)
        if direction is not None:
            actions = self.order_manager.get_spred_orders(fg,direction,self.min_spred,self.large_open,self.large_close,self.n_order,self.min_step)
        else:
            actions = [OrderCords(type_order='close_all_smart', is_open=False,smart_per=self.large_close)]
        return actions

