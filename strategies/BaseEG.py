import pandas as pd

# EG - Execution Governor — Управляющий исполнением
class BaseEG:
    def __init__(self,symbol='Test',price_step=None,mult_ps=1,stop=None,take=None):
        self.symbol = symbol
        self.price_step = price_step
        self.mult_ps = mult_ps
        self.stop = stop
        self.take = take
        self.needs_info = None # {'chart':(self.symbol,),'tape':(self.symbol,),'pos':(self.symbol,),}
        self.levels = None # {self.symbol:(390,455)}
        self.can_long = True
        self.can_short = True

    def add_slice_df(self, df:pd.DataFrame, period=20):
        df_slice = df.iloc[period+1:]
        df_slice = df_slice.reset_index(drop=True)
        return df_slice
    
    def check_stop(self,pos,delta):
        if self.stop is not None:
            if delta*self.mult_ps < -self.stop:
                if pos > 0:
                    self.can_long = False
                    return 'stop_long'
                elif pos < 0:
                    self.can_short = False
                    return 'stop_short'

    def check_take(self,delta):
        if self.take is not None:
            if delta > self.take:
                return 'close_all'

    def check_valid_action(self,action:str,pos:int):
        if action is not None:
            if not self.can_long:
                if pos < 0:
                    self.can_long = True
                elif 'open' in action:
                    if 'long' in action:
                        return None
                    if 'all' in action:
                        return action.replace('all','short')
            if not self.can_short:
                if pos > 0:
                    self.can_short = True
                if 'open' in action:
                    if 'short' in action:
                        return None
                    if 'all' in action:
                        return action.replace('all','long')
        return action

    # tdata - trading data
    def preprocessing(self,tdata):
        pdata = {}
        return pdata
    
    def get_raw_action(self,pdata):
        return None
    
    # pdata - processed data
    def __call__(self, pdata, *args, **kwds):
        return None # {self.symbol: 'close_all'}