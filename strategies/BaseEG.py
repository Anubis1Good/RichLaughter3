

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
    
    # tdata - trading data
    def preprocessing(self,tdata):
        pdata = {}
        return pdata
    
    # pdata - processed data
    def __call__(self, pdata, *args, **kwds):
        return None # {self.symbol: 'close_all'}