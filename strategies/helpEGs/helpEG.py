from strategies.BaseEG import BaseEG

class SampleEG(BaseEG):
    def __init__(self, symbol='Test',price_step=None,mult_ps=1, stop=None, take=None):
        super().__init__(symbol, price_step, mult_ps, stop, take)
        self.needs_info = {
            'chart':(self.symbol,),
            'pos':(self.symbol,)
            }
        self.levels = None # {self.symbol:(390,455)}
        # tdata - trading data
    def preprocessing(self,tdata):
        pdata = {}
        
        return pdata
    
    # pdata - processed data
    def __call__(self, pdata, *args, **kwds):
        return None # {self.symbol: 'close_all'}