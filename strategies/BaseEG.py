

# EG - Execution Governor — Управляющий исполнением
class BaseEG:
    def __init__(self,symbol='Test'):
        self.symbol = symbol
        self.needs_info = None #('chart','tape','pos')
    
    # tdata - trading data
    def preprocessing(self,tdata):
        pdata = {}
        return pdata
    
    # pdata - processed data
    def __call__(self, pdata, *args, **kwds):
        return None