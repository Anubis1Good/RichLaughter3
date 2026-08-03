from strategies.BaseEG import BaseEG

class TestEG(BaseEG):
    def __init__(self, symbol='Test',price_step=None,mult_ps=1, stop=None, take=None):
        super().__init__(symbol, price_step, mult_ps, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.type_eg = 2
        # tdata - trading data
    def preprocessing(self,tdata):
        pdata = {}
        # print(self.symbol,tdata)
        return pdata
    
    # pdata - processed data
    def get_raw_action(self,pdata):
        return 'test'