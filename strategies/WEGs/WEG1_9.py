from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_donchan_channel,add_adx,add_bollinger
from for_strategies.pva_indicators import add_quantile_params,add_velcro_indicator
from for_strategies.vsa_indicators import add_CDV,add_cdvsai,add_dvsai
from for_strategies.fix_params import fix_three_periods_hm,fix_two_periods_hm

class WEG3_BATYA(BaseEG):
    """stop=None, take=None, period=20, mult_spred = 2, sign_vol=0, sign_spred=0,sign_dir=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, mult_spred = 2, sign_vol=0, sign_spred=0,sign_dir=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.mult_spred = mult_spred
        self.sign_vol = sign_vol
        self.sign_spred = sign_spred
        self.sign_dir = sign_dir
        
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['spread'] = df['high'] - df['low']
        # Вычисление среднего объема и спреда
        df['avg_volume'] = df['volume'].rolling(window=self.period).mean()
        df['avg_spread'] = df['spread'].rolling(window=self.period).mean()
        condition = (df['volume'] < df['avg_volume']) if self.sign_vol == 0 else (df['volume'] > df['avg_volume'])
        condition &= (df['spread'] > self.mult_spred * df['avg_spread']) if self.sign_spred else (df['spread'] < self.mult_spred * df['avg_spread'])
        # Генерация сигналов
        df['signal'] = 0  # 0 = нет сигнала, 1 = покупка, -1 = продажа
        df.loc[condition & (df['close'] > df['open']), 'signal'] = 1 if self.sign_dir == 0 else -1 # Покупка
        df.loc[condition & (df['close'] < df['open']), 'signal'] = -1 if self.sign_dir == 0 else 1 # Продажа
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['signal'] == 1:
            return 'open_long'
        if row['signal'] == -1:
            return 'open_short'
        

# Нужна смесь WEG3/4 c PEG18 на st

class WEG4_DOG(BaseEG):
    """stop=None, take=None, period=14, threshold=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=14, threshold=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_CDV(df)
        df = add_rsi(df, self.period, 'cdv')
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['rsi'] < self.threshold:  
            return 'open_long'
        if row['rsi'] > 100 - self.threshold:  
            return 'open_short'

class WEG4_PUPPY(BaseEG):
    """stop=None, take=None, period=14, threshold_enter=30, threshold_exit=40"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=14, threshold_enter=30, threshold_exit=40):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_CDV(df)
        df = add_rsi(df, self.period, 'cdv')
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['rsi'] < self.threshold_enter:  
            return 'open_long'
        if row['rsi'] > 100 - self.threshold_enter:  
            return 'open_short'
        if row['rsi'] < self.threshold_exit:  
            return 'close_short'
        if row['rsi'] > 100 - self.threshold_exit:  
            return 'close_long'


        
class WEG7_PARADOX2(BaseEG):
    """stop=None, take=None, period_dvsai=14, mult_dvsai=1.8 ,period_bb=14, mult_bb=2"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_dvsai=14, mult_dvsai=1.8 ,period_bb=14, mult_bb=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_dvsai = period_dvsai
        self.mult_dvsai = mult_dvsai
        self.period_bb = period_bb
        self.mult_bb = mult_bb


    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df,self.period_bb,'close',self.mult_bb)
        df = add_dvsai(df, self.period_dvsai, self.mult_dvsai)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['dvsai'] <= row['dvsaid']:
            if row['close'] <= row['bbd']:
                return 'open_long'
        if row['dvsai'] >= row['dvsaiu']:  
            if row['close'] >= row['bbu']:
                return 'open_short'

# 07.10.2026 пока сыроват. Может открыть сделки в хаях, но и держать по тренду
class WEG8_MOUSE(BaseEG):
    """stop=None, take=None, period_dc=20, period_velcro=50, threshold_velcro=30, period_cdvsai=30, period_rsi=30, period_q=30, period_adx=40, threshold_adx=30, max_period=55, quantile=0.3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_dc=20, period_velcro=50, threshold_velcro=30, period_cdvsai=30, period_rsi=30, period_q=30, period_adx=40, threshold_adx=30, max_period=55, quantile=0.3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)
        self.period_cdvsai,self.period_rsi,self.period_q = fix_three_periods_hm(period_cdvsai,period_rsi,period_q,max_period)
        self.quantile = quantile
        self.threshold_velcro = threshold_velcro
        self.threshold_adx = threshold_adx
        self.period_adx = period_adx
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_adx(df,self.period_adx)
        df = add_cdvsai(df, period=self.period_cdvsai)
        df = add_rsi(df, self.period_rsi, 'cum_dvsai')
        df = add_quantile_params(df,self.period_q,'rsi',self.quantile)
        df['oversold'] = df['rsi'] < df['bottom_q']
        df['overbought'] = df['rsi'] > df['top_q']
        df = self.add_slice_df(df)
        # df['signal'] = add_signal(df) # поиск какого-то сигнала
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] < self.threshold_adx:
            if row['oversold'] and row['velcro'] < self.threshold_velcro:  
                return 'open_long'
            if row['overbought'] and row['velcro'] > 100 - self.threshold_velcro :  
                return 'open_short'
        else:
            if row['oversold'] and row['velcro'] > 100 - self.threshold_velcro:  
                return 'open_long'
            if row['overbought'] and row['velcro'] < self.threshold_velcro:  
                return 'open_short'
            
      
