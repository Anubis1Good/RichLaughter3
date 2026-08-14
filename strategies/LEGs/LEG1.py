from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_rsi_tw,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_cci,add_stochastic,add_roc,add_fractals,add_bollinger
from for_strategies.pva_indicators import add_integrity_index,add_mean_on_fractals,add_average_fractals
from for_strategies.vsa_indicators import add_dvsai,add_cdvsai

class LEG1_CC(BaseEG):
    """stop=None, take=None, period=15, period_fractal=10, period_mean=5, solution=8,n_fractals=3,mult=2,use_stop=1,use_ps=1 \n
    Crisis Counter 15 features"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_fractal=10, period_mean=5, solution=8,n_fractals=3,mult=2,use_stop=1,use_ps=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart':self.symbol}
        self.period = period
        self.solution = solution
        self.period_fractal = period_fractal
        self.period_mean = period_mean
        self.n_fractals = n_fractals
        self.mult = mult
        self.use_stop = use_stop
        self.use_ps = use_ps
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df,self.period)
        df = add_rsi_tw(df,self.period)
        df = add_williams_r(df,self.period)
        df = add_mfi(df,self.period)
        df = add_ultimate_oscillator(df,self.period//3,self.period//2,self.period)
        df = add_cmo(df,self.period)
        df = add_cci(df,self.period)
        df = add_stochastic(df,self.period,self.period//2)
        df = add_roc(df,self.period)
        df = add_integrity_index(df,self.period)
        df = add_fractals(df,self.period_fractal)
        inds = ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d','roc','ii')
        df['oversold'] = 0
        df['overbought'] = 0
        for i, ind in enumerate(inds):
            df = add_mean_on_fractals(df,self.period_mean,ind)
            df['oversold'] += df[ind] < df['bottom_mean']
            df['overbought'] += df[ind] > df['top_mean']
        df = add_bollinger(df,self.period)
        df['oversold'] += df['close'] < df['bbd']
        df['overbought'] += df['close'] > df['bbu']
        df = add_average_fractals(df,self.n_fractals)
        df['oversold'] += df['close'] <= df['ave_down']
        df['overbought'] += df['close'] >= df['ave_up']
        df = add_dvsai(df,self.period,self.mult)
        df['oversold'] += df['dvsai'] < df['dvsaid']
        df['overbought'] += df['dvsai'] > df['dvsaiu']
        df = add_cdvsai(df,self.period)
        df = add_rsi(df,self.period,'cum_dvsai')
        df = add_mean_on_fractals(df,self.period_mean,'rsi')
        df['oversold'] += df['rsi'] < df['bottom_mean']
        df['overbought'] += df['rsi'] > df['top_mean']
        
        df = self.add_slice_df(df,self.period)
        pdata['chart'] = df
        return pdata

    def get_raw_action(self, pdata):
        row = self.get_test_row(pdata['chart'])
        if row['oversold'] > self.solution:  
            return 'open_long'
        if row['overbought'] > self.solution:  
            return 'open_short'
        if self.use_ps:
            sol = self.solution // 2
            if row['oversold'] > sol or row['overbought'] > sol:  
                return None 
        if self.use_stop:
            return 'close_all'