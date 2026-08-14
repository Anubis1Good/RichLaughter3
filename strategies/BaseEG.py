import pandas as pd
from for_strategies.help_dtypes.actions_cls import OrderManager

# EG - Execution Governor — Управляющий исполнением
class BaseEG:
    def __init__(self,symbol='Test',price_step=None,mult_ps=1,mode=None,stop=None,take=None):
        self.symbol = symbol
        self.price_step = price_step
        self.mult_ps = mult_ps
        self.mode = mode
        self.stop = stop
        self.take = take
        self.needs_info = None 
        """self.needs_info = {
        'chart':True,
        'charts':(self.symbol,),
        'tapes':(self.symbol,),
        'poss':(self.symbol,),}
        """
        self.can_long = True
        self.can_short = True
        self.type_eg = 0 # 0 - D-ws, 1 - BD-ws, 2 - spred_glass
        self.block_type_egs = (0,)
        self.order_manager = OrderManager()
        self.amount_sl = 0
        self.amount_tp = 0
        self.last_action = None


    def add_slice_df(self, df:pd.DataFrame, period=20):
        df_slice = df.iloc[period+1:]
        df_slice = df_slice.reset_index(drop=True)
        return df_slice
    
    def get_test_df(self,df):
        df = self.preprocessing(df)
        return df
    
    def get_test_row(self,df):
        try:
            return df.iloc[-1]
        except Exception:
            # traceback.print_exc()
            pass

    def check_stop(self,pos,delta,action):
        # delta положительная, если мы в плюсе и отрицательная, если в минусе.
        if self.stop is not None and delta is not None:
            if delta*self.mult_ps <= -self.stop:
                if pos > 0:
                    if self.type_eg in self.block_type_egs:
                        self.can_long = False
                    if self.last_action != 'close_long':
                        self.amount_sl += 1
                    return 'close_long'
                elif pos < 0:
                    if self.type_eg in self.block_type_egs:
                        self.can_short = False
                    if self.last_action != 'close_short':
                        self.amount_sl += 1
                    return 'close_short'
        return action

    def check_take(self,delta,action):
        if self.take is not None and delta is not None:
            if delta >= self.take:
                if self.last_action != 'close_all':
                    self.amount_tp += 1
                return 'close_all'
        return action

    def check_valid_action(self,action:str,pos:int):
        if pos < 0:
            self.can_long = True
        elif pos > 0:
            self.can_short = True
        if action is not None:
            if not self.can_long:
                if 'open' in action:
                    if 'long' in action:
                        return None
                    if 'all' in action:
                        return action.replace('all','short')
            if not self.can_short:
                if 'open' in action:
                    if 'short' in action:
                        return None
                    if 'all' in action:
                        return action.replace('all','long')
        return action

    # tdata - trading data
    def preprocessing(self,tdata):
        '''Передаем все данные, что нужны датафреймы, списки уровней и т.д.'''
        pdata = {}
        return pdata
    
    # pdata - processed data
    def get_raw_action(self,pdata):
        return None
    
    # pdata - processed data
    def __call__(self, pdata,pos,delta, *args, **kwds):
        action = self.get_raw_action(pdata)

        if self.type_eg in self.block_type_egs:
            action = self.check_valid_action(action,pos)
        action = self.check_stop(pos,delta,action)
        action = self.check_take(delta,action)
        self.last_action = action
        return action # {self.symbol: 'close_all'}
    
        # Вариант 1: Для одного инструмента (основной, 99% случаев)
        # return 'open_long'  # строка
        
        # # Вариант 2: Для нескольких инструментов (арбитраж, хедж)
        # return {self.symbol: 'open_long', self.symbol2: 'close_short'}
        
        # # Вариант 3: Сложные действия для одного инструмента
        # return {self.symbol: ['open_long', 'set_stop_loss']}
        # _____________________[ стакан 1 ⬆ ,  стакан 2  ⬆  ]