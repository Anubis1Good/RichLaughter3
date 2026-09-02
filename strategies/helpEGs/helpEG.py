from strategies.BaseEG import BaseEG


class TestEG(BaseEG):
    def __init__(self, symbol='Test',price_step=None,mult_ps=1, mode=None, stop=None, take=None):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':True,'full_glass':True}
        self.type_eg = 2
        # tdata - trading data
    def preprocessing(self,tdata):
        pdata = {}
        df = tdata['chart']
        top_level = df['high'].rolling(20).max().iat[-1]
        bottom_level = df['low'].rolling(20).min().iat[-1]
        # print(self.symbol,tdata)
        # pdata['levels'] = [top_level,bottom_level]
        return pdata
    
    # pdata - processed data
    def get_raw_action(self,pdata):
        # return 'level_all_2'
        return 'test'
    
class CloseAllEG(BaseEG):
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
    
    def get_raw_action(self, pdata):
        return 'close_all'
