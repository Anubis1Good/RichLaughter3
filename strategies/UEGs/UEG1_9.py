from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_fractals,add_rsi,add_adx,add_bollinger
from for_strategies.pva_indicators import add_average_fractals,add_plus_delta_fc,add_exp_pdfc,add_ext_on_fractals,add_mean_on_fractals
from for_strategies.zigzag_indicators import add_dynamic_zigzag,add_dzz_peaks,add_analys_dzz,add_percent_zz_peaks,add_pattern18_dzz_czd,add_stop_loss_p18czd,add_exp_plusdelta_dzz_peaks,add_mean_dzz_peaks,add_plusdelta_dzz_peaks

class UEG2_GGD(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['close'] >= row['ave_up']:
            return 'open_short'
        if row['close'] <= row['ave_down']:
            return 'open_long'
        
        return None

class UEG2_GOOSE(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_exp_pdfc(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['close'] >= row['pdf_up']:
            return 'open_short'
        if row['close'] <= row['pdf_down']:
            return 'open_long'
        
        return None
        
class UEG2_DUCK(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_plus_delta_fc(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['close'] >= row['pdf_up']:
            return 'open_short'
        if row['close'] <= row['pdf_down']:
            return 'open_long'
        
        return None
        
class UEG3_ZEUS(BaseEG):
    """stop=None, take=None, period=20, n_std=5, method='std'|'mean'"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_std=5, method='std'):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_std = n_std
        self.method = method

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dynamic_zigzag(df, n_std=self.n_std, method=self.method, period=self.period)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['zigzag_direction'] == -1:
            return 'open_short'
        if row['zigzag_direction'] == 1:
            return 'open_long'
        
        return None
            
class UEG3_REVAN(BaseEG):
    """stop=None, take=None, period=60, n_std=5"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, n_std=5):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_std = n_std

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['zigzag_direction'] == -1:
            return 'open_long'
        if row['zigzag_direction'] == 1:
            return 'open_short'
        
        return None
    
class UEG4_FALCON(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3, allowance=0.1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_plus_delta_fc(df, self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['close'] >= row['pdf_up']:
                return 'open_short'
            if row['close'] <= row['pdf_down']:
                return 'open_long'
        
        return None

class UEG4_PELICAN(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3, allowance=0.1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_exp_pdfc(df, self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['close'] >= row['pdf_up']:
                return 'open_short'
            if row['close'] <= row['pdf_down']:
                return 'open_long'
        
        return None
            
class UEG5_HAWK(BaseEG):
    """stop=None, take=None, period=100, n_candles=5, n_fractals=3, period_rsi=20, type_treshold=0, period_mean=5, n_std=1.5, period_sma=3, threshold_trend=0.5, allowance=0.1, use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=100, n_candles=5, n_fractals=3, period_rsi=20, type_treshold=0, period_mean=5, n_std=1.5, period_sma=3, threshold_trend=0.5, allowance=0.1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.type_treshold = type_treshold
        self.period_mean = period_mean
        self.period_sma = period_sma
        self.n_std = n_std
        self.threshold_trend = threshold_trend
        self.period_rsi = period_rsi
        self.allowance = allowance
        self.use_stop = use_stop

    def add_threshold(self, df):
        if self.type_treshold == 0:
            df = add_mean_on_fractals(df, self.period_mean, 'rsi')
            df['oversold'] = df['rsi'] < df['bottom_mean']
            df['overbought'] = df['rsi'] > df['top_mean']
        else:
            df = add_ext_on_fractals(df, self.period_mean, 'rsi')
            df['oversold'] = df['rsi'] < df['bottom_ext']
            df['overbought'] = df['rsi'] > df['top_ext']
        return df

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.n_candles)
        df = add_exp_pdfc(df, self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = add_rsi(df, self.period_rsi)
        df = self.add_threshold(df)
        df = add_dzz_peaks(df, n_std=self.n_std)
        df = add_analys_dzz(df, self.period_sma)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['low'] <= row['pdf_down'] and row['oversold']:
                if row['trend_sma'] >= -self.threshold_trend:
                    return 'open_long'
                else:
                    return 'close_short'
            if row['high'] >= row['pdf_up'] and row['overbought']:
                if row['trend_sma'] <= self.threshold_trend:
                    return 'open_short'
                else:
                    return 'close_long'
        
        if self.use_stop:
            if row['trend_sma'] < -0.8:
                return 'close_long'
            if row['trend_sma'] > 0.8:
                return 'close_short'
        
        return None
            
class UEG6_DODO(BaseEG):
    """stop=None, take=None, period=20, period_smas=2, adx_threshold=30, adx_stop=35
    \n
    фильтрованный по adx GGD быстрых параметров. RANGER + GGD
    ADX-фильтр + GGD (быстрые SMA). При сильном ADX → close_all
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_smas=2, adx_threshold=30, adx_stop=35):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.adx_threshold = adx_threshold
        self.adx_stop = adx_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] > self.adx_stop:
            return 'close_all'
        
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['high_sma']:
                return 'open_short'
            if row['close'] <= row['low_sma']:
                return 'open_long'
        
        return None

class UEG6_DUELDODO(BaseEG):
    """stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, use_stop=0
    \n
    фильтрованный по adx, направленный по sma GGD быстрых параметров.
    ADX-фильтр + направление по SMA. В тренде — закрытие/открытие с учётом направления"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period)
        df['sma'] = df['close'].rolling(self.period).mean()
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['high_sma']:
                return 'open_short'
            if row['close'] <= row['low_sma']:
                return 'open_long'
        else:
            if row['close'] > row['sma']:  # long
                if row['close'] >= row['high_sma']:
                    if self.use_stop:
                        return 'close_all'
                    return 'close_long'
                if row['close'] <= row['low_sma']:
                    return 'open_long'
            else:
                if row['close'] >= row['high_sma']:
                    return 'open_short'
                if row['close'] <= row['low_sma']:
                    if self.use_stop:
                        return 'close_all'
                    return 'close_short'
        
        return None

class UEG6_VULTURE(BaseEG):
    """stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, n_candles=5, n_fractals=3, allowance=0.1
    \n
    фильтрованный по adx, направленный по sma GGD(быстрых параметров) + PELICAN .
    ADX-фильтр + SMA + PELICAN (фрактальные каналы)"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, n_candles=5, n_fractals=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period)
        df['sma'] = df['close'].rolling(self.period).mean()
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = add_fractals(df, self.n_candles)
        df = add_exp_pdfc(df, self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['high_sma']:
                return 'open_short'
            if row['close'] <= row['low_sma']:
                return 'open_long'
        else:
            if row['allowance']:
                if row['close'] > row['sma']:  # long
                    if row['close'] >= row['pdf_up']:
                        return 'close_all'
                    if row['close'] <= row['pdf_down']:
                        return 'open_long'
                else:
                    if row['close'] >= row['pdf_up']:
                        return 'open_short'
                    if row['close'] <= row['pdf_down']:
                        return 'close_all'
        
        return None

class UEG6_PIGEON(BaseEG):
    """stop=None, take=None, period=60, period_smas=2, period_sma=20, n_candles=5, n_fractals=3, allowance=0.1, mult_bb=1, use_stop=0
    \n
    Что-то типо DRG+VULTURE
    Bollinger + фрактальные каналы. Комбинация DRG+VULTURE"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, period_smas=2, period_sma=20, n_candles=5, n_fractals=3, allowance=0.1, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.period_sma = period_sma
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.allowance = allowance
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = add_fractals(df, self.n_candles)
        df = add_exp_pdfc(df, self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['high_sma']:
                return 'open_short'
            if row['close'] <= row['low_sma']:
                return 'open_long'
        else:
            if row['allowance']:
                if row['low'] > row['bbu']:  # long
                    if row['close'] >= row['pdf_up']:
                        return 'close_long'
                    if row['close'] <= row['pdf_down']:
                        return 'open_long'
                    if self.use_stop:
                        return 'close_short'
                if row['high'] < row['bbd']:  # short
                    if row['close'] >= row['pdf_up']:
                        return 'open_short'
                    if row['close'] <= row['pdf_down']:
                        return 'close_short'
                    if self.use_stop:
                        return 'close_long'
        
        return None

class UEG6_ADVENTURE(BaseEG):
    """stop=None, take=None, period=60, period_smas=2, period_sma=20, mult_bb=1, use_stop=0
    \n
    DRG+DUELDODO
    Bollinger + GGD. Комбинация DRG+DUELDODO"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, period_smas=2, period_sma=20, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.period_sma = period_sma
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['high_sma']:
                return 'open_short'
            if row['close'] <= row['low_sma']:
                return 'open_long'
        else:
            if row['low'] > row['bbu']:  # long
                if row['close'] >= row['high_sma']:
                    return 'close_long'
                if row['close'] <= row['low_sma']:
                    return 'open_long'
                if self.use_stop:
                    return 'close_short'
            if row['high'] < row['bbd']:  # short
                if row['close'] >= row['high_sma']:
                    return 'open_short'
                if row['close'] <= row['low_sma']:
                    return 'close_short'
                if self.use_stop:
                    return 'close_long'
        
        return None
                
class UEG6_SHERIFF(BaseEG):
    """stop=None, take=None, period=60, period_smas=2, mult_bb=2
    \n
    GGD+PUBG
    Bollinger + GGD (упрощённая версия). При выходе за BB — сигнал в сторону пробоя"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, period_smas=2, mult_bb=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.mult_bb = mult_bb

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['high_sma']:
                return 'open_short'
            if row['close'] <= row['low_sma']:
                return 'open_long'
        else:
            if row['low'] > row['bbu']:  # long
                return 'open_long'
            if row['high'] < row['bbd']:  # short
                return 'open_short'
        
        return None
            
class UEG7_DODO(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3, adx_threshold=30, adx_stop=35
    \n
    фильтрованный по adx GGD быстрых параметров. RANGER + GGD
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3, adx_threshold=30, adx_stop=35):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.adx_threshold = adx_threshold
        self.adx_stop = adx_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period)
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] > self.adx_stop:
            return 'close_all'
        
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        
        return None
            
class UEG7_DUELDODO(BaseEG):
    """stop=None, take=None, period=20, n_candles=5, n_fractals=3, adx_threshold=30, period_sma=20, use_stop=0
    \n
    фильтрованный по adx, направленный по sma GGD быстрых параметров."""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_candles=5, n_fractals=3, adx_threshold=30, period_sma=20, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period)
        df['sma'] = df['close'].rolling(self.period).mean()
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        else:
            if row['close'] > row['sma']:  # long
                if row['close'] >= row['ave_up']:
                    if self.use_stop:
                        return 'close_all'
                    return 'close_long'
                if row['close'] <= row['ave_down']:
                    return 'open_long'
            else:
                if row['close'] >= row['ave_up']:
                    return 'open_short'
                if row['close'] <= row['ave_down']:
                    if self.use_stop:
                        return 'close_all'
                    return 'close_short'
        
        return None

class UEG7_VULTURE(BaseEG):
    """stop=None, take=None, period=20, adx_threshold=30, period_sma=20, n_candles=7, n_fractals=5, n_candles2=5, n_fractals2=3, allowance=0.1
    \n
    фильтрованный по adx, направленный по sma GGD(быстрых параметров) + PELICAN ."""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, adx_threshold=30, period_sma=20, n_candles=7, n_fractals=5, n_candles2=5, n_fractals2=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.n_candles2 = n_candles2
        self.n_fractals2 = n_fractals2
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period)
        df['sma'] = df['close'].rolling(self.period).mean()
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = df.drop(['fractal_up', 'fractal_down'], axis=1)
        df = add_fractals(df, self.n_candles2)
        df = add_exp_pdfc(df, self.n_fractals2)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        else:
            if row['allowance']:
                if row['close'] > row['sma']:  # long
                    if row['close'] >= row['pdf_up']:
                        return 'close_all'
                    if row['close'] <= row['pdf_down']:
                        return 'open_long'
                else:
                    if row['close'] >= row['pdf_up']:
                        return 'open_short'
                    if row['close'] <= row['pdf_down']:
                        return 'close_all'
        
        return None

class UEG7_PIGEON(BaseEG):
    """stop=None, take=None, period=60, n_candles=10, n_fractals=6, n_candles2=5, n_fractals2=3, allowance=0.1, mult_bb=1, use_stop=0
    \n
    Что-то типо DRG+VULTURE"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, n_candles=10, n_fractals=6, n_candles2=5, n_fractals2=3, allowance=0.1, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.n_candles2 = n_candles2
        self.n_fractals2 = n_fractals2
        self.allowance = allowance
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = df.drop(['fractal_up', 'fractal_down'], axis=1)
        df = add_fractals(df, self.n_candles2)
        df = add_exp_pdfc(df, self.n_fractals2)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        else:
            if row['allowance']:
                if row['low'] > row['bbu']:  # long
                    if row['close'] >= row['pdf_up']:
                        return 'close_long'
                    if row['close'] <= row['pdf_down']:
                        return 'open_long'
                    if self.use_stop:
                        return 'close_short'
                if row['high'] < row['bbd']:  # short
                    if row['close'] >= row['pdf_up']:
                        return 'open_short'
                    if row['close'] <= row['pdf_down']:
                        return 'close_short'
                    if self.use_stop:
                        return 'close_long'
        
        return None
                    
class UEG7_ADVENTURE(BaseEG):
    """stop=None, take=None, period=60, n_candles=5, n_fractals=3, mult_bb=1, use_stop=0
    \n
    DRG+DUELDODO"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, n_candles=5, n_fractals=3, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        else:
            if row['low'] > row['bbu']:  # long
                if row['close'] >= row['ave_up']:
                    return 'close_long'
                if row['close'] <= row['ave_down']:
                    return 'open_long'
                if self.use_stop:
                    return 'close_short'
            if row['high'] < row['bbd']:  # short
                if row['close'] >= row['ave_up']:
                    return 'open_short'
                if row['close'] <= row['ave_down']:
                    return 'close_short'
                if self.use_stop:
                    return 'close_long'
        
        return None

class UEG7_SHERIFF(BaseEG):
    """stop=None, take=None, period=60, n_candles=5, n_fractals=3, mult_bb=2
    \n
    GGD+PUBG"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, n_candles=5, n_fractals=3, mult_bb=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_candles = n_candles
        self.n_fractals = n_fractals
        self.mult_bb = mult_bb

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_fractals(df, self.n_candles)
        df = add_average_fractals(df, self.n_fractals)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        else:
            if row['low'] > row['bbu']:  # long
                return 'open_long'
            if row['high'] < row['bbd']:  # short
                return 'open_short'
        
        return None
            
class UEG8_AVENGER(BaseEG):
    '''
    stop=None, take=None, period=20, divider_buff=10, percent_threshold=0.2, threshold_dzz=0.2, buff=0.1, divider_stop=2, use_stop=1
    \n
    Сложная паттерн-стратегия на основе ZigZag и паттернов Volume Spread Analysis (VSA)
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, divider_buff=10, percent_threshold=0.2, threshold_dzz=0.2, buff=0.1, divider_stop=2, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.divider_buff = divider_buff
        self.percent_threshold = percent_threshold
        self.threshold_dzz = threshold_dzz
        self.buff = buff
        self.divider_stop = divider_stop
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_percent_zz_peaks(df, percent_threshold=self.percent_threshold)
        df = add_pattern18_dzz_czd(df, self.threshold_dzz, self.buff)
        df = add_stop_loss_p18czd(df, self.divider_stop)
        df['buffer'] = ((df['zp2'] - df['zp3']) / self.divider_buff).abs()
        df['pbzp2'] = df['zp2'] + df['buffer']
        df['mbzp2'] = df['zp2'] - df['buffer']
        df['pbzp3'] = df['zp3'] + df['buffer']
        df['mbzp3'] = df['zp3'] - df['buffer']
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long, can_short = None, None
        
        if row['pattern18'] in ('bti', 'joc', 'top_range', 'double_top', 'weak_long', 'narrowing_down', 'spring', 'sos'):
            can_long = row['pbzp3'] >= row['close'] >= row['mbzp3']
            can_short = row['mbzp2'] <= row['close'] <= row['pbzp2']
        
        if row['pattern18'] in ('btc', 'bui', 'bottom_range', 'double_bottom', 'weak_short', 'narrowing_up', 'upthrust', 'sow'):
            can_short = row['pbzp3'] >= row['close'] >= row['mbzp3']
            can_long = row['mbzp2'] <= row['close'] <= row['pbzp2']
        
        if can_long:
            return 'open_long'
        if can_short:
            return 'open_short'
        
        if self.use_stop:
            if row['close'] > row['ssl']:
                return 'close_short'
            if row['close'] < row['lsl']:
                return 'close_long'
        
        return None

class UEG9_BIRDWATCHER(BaseEG):
    '''
    stop=None, take=None, period=20, n_std=3, period_pd=2, buffer_pd=0.1, mult_stop=0.5, use_exp=1, use_stop=1
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_std=3, period_pd=2, buffer_pd=0.1, mult_stop=0.5, use_exp=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_std = n_std
        self.period_pd = period_pd
        self.buffer_pd = buffer_pd
        self.mult_stop = mult_stop
        self.plusdelta_func = add_exp_plusdelta_dzz_peaks if use_exp else add_plusdelta_dzz_peaks
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = self.plusdelta_func(df, self.period_pd, self.buffer_pd)
        df['top_stop'] = df['top_pd'] + df['delta_pd'] * self.mult_stop
        df['bottom_stop'] = df['bottom_pd'] - df['delta_pd'] * self.mult_stop
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        try:
            if row['top_stop'] > row['close'] >= row['top_pd']:
                return 'open_short'
            if row['bottom_stop'] < row['close'] <= row['bottom_pd']:
                return 'open_long'
            if self.use_stop:
                if row['close'] > row['top_stop']:
                    return 'close_short'
                if row['close'] < row['bottom_stop']:
                    return 'close_long'
        except:
            return None
        
        return None

class UEG9_GRAVY(BaseEG):
    '''
    stop=None, take=None, period=20, n_std=3, period_mean=2, buffer_mean=0.1, mult_stop=0.5, use_stop=1
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_std=3, period_mean=2, buffer_mean=0.1, mult_stop=0.5, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_std = n_std
        self.period_mean = period_mean
        self.buffer_mean = buffer_mean
        self.mult_stop = mult_stop
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = add_mean_dzz_peaks(df, self.period_mean, self.buffer_mean)
        df['top_stop'] = df['top_mean'] + df['delta_mean'] * self.mult_stop
        df['bottom_stop'] = df['bottom_mean'] - df['delta_mean'] * self.mult_stop
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['top_stop'] > row['close'] >= row['top_mean']:
            return 'open_short'
        if row['bottom_stop'] < row['close'] <= row['bottom_mean']:
            return 'open_long'
        if self.use_stop:
            if row['close'] > row['top_stop']:
                return 'close_short'
            if row['close'] < row['bottom_stop']:
                return 'close_long'
        
        return None