from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_fractals,add_rsi,add_adx,add_bollinger
from for_strategies.pva_indicators import add_average_fractals,add_plus_delta_fc,add_exp_pdfc,add_ext_on_fractals,add_mean_on_fractals,add_average_fractals_window,add_exp_pdfc_window,add_plus_delta_fc_window,add_vodka_channel
from for_strategies.pva2_indicators import add_per_above_sma
from for_strategies.zigzag_indicators import add_percent_zz190826,add_dzz_peaks,add_analys_dzz,add_percent_zz_peaks,add_pattern18_dzz_czd,add_stop_loss_p18czd,add_exp_plusdelta_dzz_peaks,add_mean_dzz_peaks,add_plusdelta_dzz_peaks,add_zigzag180826,add_shift_zz_peaks,add_analys_dzz180826, add_zigzag_window_210926,add_pattern18_zzw_210926,add_zigzag_window_260926,add_mean_peaks_wzz260926, add_plusdelta_peaks_wzz260926,add_exp_plusdelta_peaks_wzz260926,add_mean_ind_wzz_peaks,add_extreme_ind_wzz_peaks,add_pattern18_zzw_260926,add_drop_last_wzp
from for_strategies.help_indicators import add_buffer_add
from for_strategies.fix_params import fix_supertrend_params,fix_two_periods_hm,fix_three_periods_hm

class UEG4_CANADIAN(BaseEG):
    """stop=None, take=None, period_window=55,period_fractal_free=5, n_fractals=3, allowance=0.1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_window=55,period_fractal_free=5, n_fractals=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df['ave_diff_percent'] = ((df['ave_up'] - df['ave_down']) / df['ave_down']) * 100
        df['allowance'] = df['ave_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['close'] >= row['ave_up']:
            return 'open_short'
        if row['close'] <= row['ave_down']:
            return 'open_long'
        
        return None
     
class UEG4_FALCON2(BaseEG):
    """stop=None, take=None, period_window=55,period_fractal_free=5, n_fractals=3, allowance=0.1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_window=55,period_fractal_free=5, n_fractals=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_plus_delta_fc_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['close'] >= row['pdf_up']:
                return 'open_short'
            if row['close'] <= row['pdf_down']:
                return 'open_long'
        
        return None

# Нужны версии с adx, есть ощущение, что хорошо работает на тренде и плохо на флете
# Честно очень плохие результаты. Как будто можно прощаться с этим роботом
class UEG4_PELICAN2(BaseEG):
    """stop=None, take=None, period_window=55,period_fractal_free=5, n_fractals=3, allowance=0.1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_window=55,period_fractal_free=5, n_fractals=3, allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_exp_pdfc_window(df, self.period_window,self.period_fractal_free,self.n_fractals)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period_zz=20, period_fractal=5, n_fractals=3, period_rsi=20, type_treshold=0, period_max=55, n_std=1.5, period_sma=3, threshold_trend=0.5, allowance=0.1, use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_zz=20, period_fractal=5, n_fractals=3, period_rsi=20, type_treshold=0, period_max=55, n_std=1.5, period_sma=3, threshold_trend=0.5, allowance=0.1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_zz = period_zz
        self.period_fractal = period_fractal
        self.n_fractals = n_fractals
        self.type_treshold = type_treshold
        self.period_max = period_max
        self.period_sma = period_sma
        self.n_std = n_std
        self.threshold_trend = threshold_trend
        self.period_rsi = period_rsi
        self.allowance = allowance
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def add_threshold(self, df):
        if self.type_treshold == 0:
            df = add_mean_on_fractals(df, self.period_max, 'rsi',self.period_fractal)
            df['oversold'] = df['rsi'] < df['bottom_mean']
            df['overbought'] = df['rsi'] > df['top_mean']
        else:
            df = add_ext_on_fractals(df, self.period_max, 'rsi',self.period_fractal)
            df['oversold'] = df['rsi'] < df['bottom_ext']
            df['overbought'] = df['rsi'] > df['top_ext']
        return df

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.period_fractal)
        df = add_exp_pdfc(df, self.n_fractals, self.period_fractal)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = add_rsi(df, self.period_rsi)
        df = self.add_threshold(df)
        df = add_zigzag180826(df, n_std=self.n_std,period=self.period_zz)
        df = add_shift_zz_peaks(df)
        df = add_analys_dzz180826(df, self.period_sma)
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period_adx=20, period_smas=2, adx_threshold=30, adx_stop=35
    \n
    фильтрованный по adx GGD быстрых параметров. RANGER + GGD
    ADX-фильтр + GGD (быстрые SMA). При сильном ADX → close_all
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=20, period_smas=2, adx_threshold=30, adx_stop=35):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.period_smas = period_smas
        self.adx_threshold = adx_threshold
        self.adx_stop = adx_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, use_stop=0,period_adx=27
    \n
    фильтрованный по adx, направленный по sma GGD быстрых параметров.
    ADX-фильтр + направление по SMA. В тренде — закрытие/открытие с учётом направления"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, use_stop=0,period_adx=27):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_adx = period_adx
        self.period_smas = period_smas
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma'] = df['close'].rolling(self.period).mean()
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, period_fractal=5, n_fractals=3, allowance=0.1, period_adx=27
    \n
    фильтрованный по adx, направленный по sma GGD(быстрых параметров) + PELICAN .
    ADX-фильтр + SMA + PELICAN (фрактальные каналы)"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, period_smas=2, adx_threshold=30, period_sma=20, period_fractal=5, n_fractals=3, allowance=0.1, period_adx=27):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_adx = period_adx
        self.period_smas = period_smas
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.period_fractal = period_fractal
        self.n_fractals = n_fractals
        self.allowance = allowance
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma'] = df['close'].rolling(self.period).mean()
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = add_fractals(df, self.period_fractal)
        df = add_exp_pdfc(df, self.n_fractals, self.period_fractal)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period=60, period_smas=2, period_sma=20, period_fractal=5, n_fractals=3, allowance=0.1, mult_bb=1, use_stop=0
    \n
    Что-то типо DRG+VULTURE
    Bollinger + фрактальные каналы. Комбинация DRG+VULTURE"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period_smas=2, period_sma=20, period_fractal=5, n_fractals=3, allowance=0.1, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_smas = period_smas
        self.period_sma = period_sma
        self.period_fractal = period_fractal
        self.n_fractals = n_fractals
        self.allowance = allowance
        self.mult_bb = mult_bb
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = add_fractals(df, self.period_fractal)
        df = add_exp_pdfc(df, self.n_fractals, self.period_fractal)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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

# Подумать над расширение области между скользящими средними
class UEG6_ADVENTURE(BaseEG):
    """stop=None, take=None, period=60, period_smas=2, period_sma=20, mult_bb=1, use_stop=0
    \n
    DRG+DUELDODO
    Bollinger + GGD. Комбинация DRG+DUELDODO"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period_smas=2, period_sma=20, mult_bb=1, use_stop=0):
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
        df = self.add_slice_df(df)
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

# 14.10.2026 может зайти на локальном лое в шорт в лонговом тренде
# 27.10.2026 нужна версия, с локальным подстраивание периода sma под волатильность
class UEG6_SURVIVALIST(BaseEG):
    """stop=None, take=None, period_bb=55, period_smas=2, mult_bb=1, use_stop=0,div_buff=2,period_rsi=30,thresh_rsi=30,use_rsi=0
    \n
    UEG6_ADVENTURE с буфером и rsi
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=55, period_smas=2, mult_bb=1, use_stop=0,div_buff=2,period_rsi=30,thresh_rsi=30,use_rsi=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bb = period_bb
        self.period_smas = period_smas
        self.mult_bb = mult_bb
        self.use_stop = use_stop
        self.div_buff = div_buff
        self.period_rsi = period_rsi
        self.thresh_rsi = thresh_rsi
        self.use_rsi = use_rsi

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period_bb, multiplier=self.mult_bb)
        df['high_sma'] = df['high'].rolling(self.period_smas).mean()
        df['low_sma'] = df['low'].rolling(self.period_smas).mean()
        df = add_buffer_add(df, 'high_sma', 'low_sma', self.div_buff)
        df = add_rsi(df,self.period_rsi)
        df['can_long'] = df['rsi'] < self.thresh_rsi if self.use_rsi else True        
        df['can_short'] = df['rsi'] > 100 - self.thresh_rsi if self.use_rsi else True        
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['high'] < row['bbu'] and row['low'] > row['bbd']:
            if row['close'] >= row['top_buff'] and row['can_short']:
                return 'open_short'
            if row['close'] <= row['bottom_buff'] and row['can_long']:
                return 'open_long'
        else:
            if row['low'] > row['bbu']:  # long
                if row['close'] <= row['bottom_buff'] and row['can_long']:
                    return 'open_long'
                if row['close'] >= row['top_buff']:
                    return 'close_long'
                if self.use_stop:
                    return 'close_short'
            if row['high'] < row['bbd']:  # short
                if row['close'] >= row['top_buff'] and row['can_short']:
                    return 'open_short'
                if row['close'] <= row['bottom_buff']:
                    return 'close_short'
                if self.use_stop:
                    return 'close_long'
        

# 02.10.2026 подумать над вариантом адаптивного периода. Что бы при низкой волатильности период уменьшался, при высокой увеличивался.
# 02.10.2026 при настройках на большое количество сделок, знатно пиздит.
class UEG6_SHERIFF(BaseEG):
    """stop=None, take=None, period=60, period_smas=2, mult_bb=2
    \n
    GGD+PUBG
    Bollinger + GGD (упрощённая версия). При выходе за BB — сигнал в сторону пробоя"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period_smas=2, mult_bb=2):
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
        df = self.add_slice_df(df)
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
    
# сделать 7 версии с оконными функциями внутри которых определяются фракталы
class UEG7_DODO(BaseEG):
    """stop=None, take=None, period_adx=20, period_fractal=5, max_period=55, adx_threshold=30, adx_stop=35, use_stop=0
    \n
    фильтрованный по adx GGD быстрых параметров. RANGER + GGD
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=20, period_fractal=5, max_period=55, adx_threshold=30, adx_stop=35, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.max_period = max_period
        self.period_fractal = period_fractal
        self.adx_threshold = adx_threshold
        self.adx_stop = adx_stop
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df = add_fractals(df, self.period_fractal)
        df = add_average_fractals(df, self.max_period, self.period_fractal)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if self.use_stop:
            if row['adx'] > self.adx_stop:
                return 'close_all'
        
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        
        return None
    
# Надо думать над фильтром тренда
# 05.10.2026 как будто тоже надо установить минимальный period_window выше
# 27.10.2026 ну как-то он прям перетягивает бывает. Весь день держал одну сделку. Мог кучу раз ее выгодно закрыть. В итоге закрыл по времени.
# 27.10.2026 слишком привязывает плотно. В итоге открывает на дне широкого боковика.
class UEG7_LOVERGOOSE(BaseEG):
    """stop=None, take=None, period_adx=20, period_window=55,period_fractal_free=5, n_fractals=3, adx_threshold=30, adx_stop=35, use_stop=0
    \n
    UEG7_DODO на add_average_fractals_window \n
    фильтрованный по adx GGD быстрых параметров. RANGER + GGD
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=20, period_window=55,period_fractal_free=5, n_fractals=3, adx_threshold=30, adx_stop=35, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.adx_threshold = adx_threshold
        self.adx_stop = adx_stop
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if self.use_stop:
            if row['adx'] > self.adx_stop:
                return 'close_all'
        
        if row['adx'] < self.adx_threshold:
            if row['close'] >= row['ave_up']:
                return 'open_short'
            if row['close'] <= row['ave_down']:
                return 'open_long'
        
        return None
            
class UEG7_DUELDODO(BaseEG):
    """stop=None, take=None, period_adx=20, period_fractal=5, max_period=55, adx_threshold=30, period_sma=20, use_stop=0
    \n
    фильтрованный по adx, направленный по sma GGD быстрых параметров."""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=20, period_fractal=5, max_period=55, adx_threshold=30, period_sma=20, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.max_period = max_period
        self.period_fractal = period_fractal
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma'] = df['close'].rolling(self.period_sma).mean()
        df = add_fractals(df, self.period_fractal)
        df = add_average_fractals(df, self.max_period, self.period_fractal)
        df = self.add_slice_df(df)
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
    
class UEG7_LOVERDUCK(BaseEG):
    """stop=None, take=None, period_adx=20, period_window=55, period_fractal_free=5, n_fractals=3, adx_threshold=30, period_sma=20, use_stop=0
    \n
    UEG7_DUELDODO на add_average_fractals_window \n
    фильтрованный по adx, направленный по sma GGD быстрых параметров."""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=20, period_window=55, period_fractal_free=5, n_fractals=3, adx_threshold=30, period_sma=20, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.use_stop = use_stop
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma'] = df['close'].rolling(self.period_sma).mean()
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period_sma=20, adx_threshold=30, period_fractal=7, n_fractals=5, period_fractal2=5, max_period=55, allowance=0.1, period_adx=27
    \n
    фильтрованный по adx, направленный по sma GGD(быстрых параметров) + PELICAN ."""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_sma=20, adx_threshold=30, period_fractal=7, n_fractals=5, period_fractal2=5, max_period=55, allowance=0.1, period_adx=27):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_sma = period_sma
        self.period_adx = period_adx
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.period_fractal = period_fractal
        self.n_fractals = n_fractals
        self.period_fractal2 = period_fractal2
        self.max_period = max_period
        self.allowance = allowance
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma'] = df['close'].rolling(self.period_sma).mean()
        df = add_fractals(df, self.period_fractal)
        df = add_average_fractals(df, self.max_period, self.period_fractal)
        df = df.drop(['fractal_up', 'fractal_down'], axis=1)
        df = add_fractals(df, self.period_fractal2)
        df = add_exp_pdfc(df, self.n_fractals, self.period_fractal2)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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

# 02.10.2026 при настройке на большое количество сделок может пиздеть
# 05.10.2026 сделать версию без закрытия в хаях
class UEG7_CANNIBAL(BaseEG):
    """stop=None, take=None, period_sma=20, adx_threshold=30, period_window=55,period_fractal_free=5, n_fractals=5, period_window2=55, period_fractal_free2=5,n_fractals2=3, allowance=0.1, period_adx=27
    \n
    UEG7_VULTURE на оконных функциях \n
    фильтрованный по adx, направленный по sma GGD(быстрых параметров) + PELICAN ."""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_sma=20, adx_threshold=30, period_window=55,period_fractal_free=5, n_fractals=5, period_window2=55, period_fractal_free2=5,n_fractals2=3, allowance=0.1, period_adx=27):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_sma = period_sma
        self.period_adx = period_adx
        self.adx_threshold = adx_threshold
        self.period_sma = period_sma
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.period_window2 = period_window2
        self.period_fractal_free2 = period_fractal_free2
        self.n_fractals2 = n_fractals2
        self.allowance = allowance


    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_adx(df, self.period_adx)
        df['sma'] = df['close'].rolling(self.period_sma).mean()
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df = add_exp_pdfc_window(df, self.period_window2,self.period_fractal_free2,self.n_fractals2)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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
                    if row['close'] >= row['pdf_up']: # из-за этого может зать в хаях
                        return 'close_all'
                    if row['close'] <= row['pdf_down']:
                        return 'open_long'
                else:
                    if row['close'] >= row['pdf_up']:
                        return 'open_short'
                    if row['close'] <= row['pdf_down']: # из-за этого может зать в хаях
                        return 'close_all'
        
        return None

class UEG7_PIGEON(BaseEG):
    """stop=None, take=None, period_bb=60, period_fractal=10, max_period=55, period_fractal2=5, n_fractals2=3, allowance=0.1, mult_bb=1, use_stop=0
    \n
    Что-то типо DRG+VULTURE"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=55, period_fractal=10, max_period=55, period_fractal2=5, n_fractals2=3, allowance=0.1, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bb = period_bb
        self.period_fractal = period_fractal
        self.max_period = max_period
        self.period_fractal2 = period_fractal2
        self.n_fractals2 = n_fractals2
        self.allowance = allowance
        self.mult_bb = mult_bb
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period_bb, multiplier=self.mult_bb)
        df = add_fractals(df, self.period_fractal)
        df = add_average_fractals(df, self.max_period, self.period_fractal)
        df = df.drop(['fractal_up', 'fractal_down'], axis=1)
        df = add_fractals(df, self.period_fractal2)
        df = add_exp_pdfc(df, self.n_fractals2, self.period_fractal2)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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
# слишком частит. В итоге в тренде закрывает убыток в лоях и переобувается. После чего получает люлей на откате.
#30.09.26 может весь день просидеть с убыточной сделкой, если рынок +- однонаправлен
# 2.10.26 откровенно вызывает вопросы. опять тупо весь день с убыточной сделкой.
class UEG7_CARRIER(BaseEG):
    """stop=None, take=None, period_bb=55, period_window=55,period_fractal_free=5, n_fractals=5, period_window2=55, period_fractal_free2=5,n_fractals2=3, allowance=0.1, mult_bb=1, use_stop=0
    \n
    UEG7_PIGEON на оконных функциях \n
    Что-то типо DRG+VULTURE"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=55, period_window=55,period_fractal_free=5, n_fractals=5, period_window2=55, period_fractal_free2=5,n_fractals2=3, allowance=0.1, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bb = period_bb
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.period_window2 = period_window2
        self.period_fractal_free2 = period_fractal_free2
        self.n_fractals2 = n_fractals2
        self.allowance = allowance
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period_bb, multiplier=self.mult_bb)
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df = add_exp_pdfc_window(df, self.period_window2,self.period_fractal_free2,self.n_fractals2)
        df['pdf_diff_percent'] = ((df['pdf_up'] - df['pdf_down']) / df['pdf_down']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period=60, period_fractal=5, max_period=55, mult_bb=1, use_stop=0
    \n
    DRG+DUELDODO"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period_fractal=5, max_period=55, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_fractal = period_fractal
        self.max_period = max_period
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_fractals(df, self.period_fractal)
        df = add_average_fractals(df, self.max_period, self.period_fractal)
        df = self.add_slice_df(df)
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
    
class UEG7_CELEBRITY(BaseEG):
    """stop=None, take=None, period_bb=55, period_window=55,period_fractal_free=5, n_fractals=5, mult_bb=1, use_stop=0
    \n
    UEG7_ADVENTURE на оконных функциях \n
    DRG+DUELDODO"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=55, period_window=55,period_fractal_free=5, n_fractals=5, mult_bb=1, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bb = period_bb
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.mult_bb = mult_bb
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period_bb, multiplier=self.mult_bb)
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df = self.add_slice_df(df)
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
    """stop=None, take=None, period=55, period_fractal=5, max_period=55, mult_bb=2
    \n
    GGD+PUBG"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period_fractal=5, max_period=55, mult_bb=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_fractal = period_fractal
        self.max_period = max_period
        self.mult_bb = mult_bb

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period, multiplier=self.mult_bb)
        df = add_fractals(df, self.period_fractal)
        df = add_average_fractals(df, self.max_period, self.period_fractal)
        df = self.add_slice_df(df)
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

# 13.10.2026 открывал и закрывал сделки жестко в хаях 'VTBR':(UEG7_DETECTIVE,(None,95,65,56,17,8,2.5),8,None),
# 19.10.2026 опять в лоях открывает сделки
class UEG7_DETECTIVE(BaseEG):
    """stop=None, take=None, period_bb=55, period_window=55,period_fractal_free=5, n_fractals=5, mult_bb=2
    \n
    UEG7_SHERIFF на оконными функциями
    GGD+PUBG"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bb=55, period_window=55,period_fractal_free=5, n_fractals=5, mult_bb=2):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bb = period_bb
        self.period_window = period_window
        self.period_fractal_free = period_fractal_free
        self.n_fractals = n_fractals
        self.mult_bb = mult_bb

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_bollinger(df, self.period_bb, multiplier=self.mult_bb)
        df = add_average_fractals_window(df,self.period_window,self.period_fractal_free,self.n_fractals)
        df = self.add_slice_df(df)
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
    stop=None, take=None, divider_buff=10, percent_threshold=0.2, threshold_dzz=0.2, buff=0.1, divider_stop=2, use_stop=1
    \n
    Сложная паттерн-стратегия на основе ZigZag и паттернов Volume Spread Analysis (VSA)
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, divider_buff=10, percent_threshold=0.2, threshold_dzz=0.2, buff=0.1, divider_stop=2, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.divider_buff = divider_buff
        self.percent_threshold = percent_threshold
        self.threshold_dzz = threshold_dzz
        self.buff = buff
        self.divider_stop = divider_stop
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_percent_zz190826(df, percent_threshold=self.percent_threshold)
        df['zigzag_peaks'] = df['zigzag_peaks'].shift(1)
        df = add_pattern18_dzz_czd(df, self.threshold_dzz, self.buff)
        df = add_stop_loss_p18czd(df, self.divider_stop)
        df['buffer'] = ((df['zp2'] - df['zp3']) / self.divider_buff).abs()
        df['pbzp2'] = df['zp2'] + df['buffer']
        df['mbzp2'] = df['zp2'] - df['buffer']
        df['pbzp3'] = df['zp3'] + df['buffer']
        df['mbzp3'] = df['zp3'] - df['buffer']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long, can_short = None, None
        
        if row['pattern18'] in ('bti', 'joc', 'top_range', 'double_top', 'weak_long', 'narrowing_down', 'spring', 'sos'):
            can_long = row['pbzp3'] >= row['close']
            can_short = row['mbzp2'] <= row['close']
        
        if row['pattern18'] in ('btc', 'bui', 'bottom_range', 'double_bottom', 'weak_short', 'narrowing_up', 'upthrust', 'sow'):
            can_short = row['close'] >= row['mbzp3']
            can_long = row['close'] <= row['pbzp2']
        
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

# Нужна версия вариантом с использования rsi на каждом паттерне
# 06.10.2026 ограничения оптимизации привели к тому, что сделок как-будто как-то очень мало
# 07.10.2026 открыл лонг в хаях     'SIBN':(UEG8_SOLDIER,(None,20,18,21,40,0.57,4,0.76,24,0,92,2,2,97,75,19,79,43),2,None),
# 07.10.2026 почему-то открывал вообще не правильные сделки. Все наоборот 'IRAO':(UEG8_SOLDIER,(None,30,18,57,48,0.95,10,0.72,30,0,73,21,69,0,90,82,73,95),3,None),
# 09.10.2026 надо сделать версию только для боковика
# 14.10.2026 целый день тянул контренд. В итоге закрыл -4.81%
# 20.10.2026 открыл хорошо, но почему-то не закрыл почти процент и в итоге закрыл минус
# 21.10.2026 возможно стоит попробовать объединить с дюной
# 21.10.2026 специально блокировать действия при joc. Успешный пример:     'ENPG':(UEG8_SOLDIER,(None,None,13,35,36,0.7,8,0.64,31,0,  26,51,87,75,94,73,55,90),1,None), получает он на joc только закрывал позицию, а на sos открывал только по тренду
# 21.10.2026 попробовать сделать на расширение. Помнять точки 'pbzp3' -> 'mbzp3'
class UEG8_SOLDIER(BaseEG):
    """stop=None, take=None, \n
    divider_buff=5, period_rsi=14, period_wzz=30, frac_wzz=0.1, n_wzp=6, threshold_p18=0.1, threshold_rsi=30, use_rsi=0, g_joc=99,g_tr=99,g_dt=99,g_wl=99,g_nd=99,g_s=99,g_sos=99,g_bti=99
    \n
    0-2 - ничего,
    3-6 - противоположную,
    7-9 - все"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, divider_buff=5, period_rsi=14, period_wzz=30, frac_wzz=0.1, n_wzp=6, threshold_p18=0.1, threshold_rsi=30, use_rsi=0, g_joc=99,g_tr=99,g_dt=99,g_wl=99,g_nd=99,g_s=99,g_sos=99,g_bti=99):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.divider_buff = divider_buff
        self.period_rsi = period_rsi
        self.period_wzz = period_wzz
        self.frac_wzz = frac_wzz
        self.n_wzp = n_wzp
        self.threshold_p18 = threshold_p18
        self.g_joc = g_joc
        self.g_tr = g_tr
        self.g_dt = g_dt
        self.g_wl = g_wl
        self.g_nd = g_nd
        self.g_s = g_s
        self.g_sos = g_sos
        self.g_bti = g_bti
        self.use_rsi=use_rsi
        self.threshold_rsi=threshold_rsi
        self.wzp2 = f'wzp{n_wzp - 2}'
        self.wzp3 = f'wzp{n_wzp - 1}'
        self.long_group = ('bti', 'joc', 'top_range', 'double_top', 'weak_long', 'narrowing_down', 'spring', 'sos')
        self.short_group = ('btc', 'bui', 'bottom_range', 'double_bottom', 'weak_short', 'narrowing_up', 'upthrust', 'sow')

    def get_group(self,pattern):
        if pattern == 'joc' or pattern == 'bui':
            return self.g_joc
        if pattern == 'top_range' or pattern == 'bottom_range':
            return self.g_tr
        if pattern == 'double_top' or pattern == 'double_bottom':
            return self.g_dt
        if pattern == 'weak_long' or pattern == 'weak_short':
            return self.g_wl
        if pattern == 'narrowing_down' or pattern == 'narrowing_up':
            return self.g_nd
        if pattern == 'spring' or pattern == 'upthrust':
            return self.g_s
        if pattern == 'sos' or pattern == 'sow':
            return self.g_sos
        if pattern == 'bti' or pattern == 'btc':
            return self.g_bti
        return 0

    def get_action_by_group(self,pattern,can):
        group = self.get_group(pattern)
        od = group // 10
        cd = group % 10
        if can == 'long':
            if od > 6:
                return 'open_long'
            if od > 2 and pattern in self.long_group:
                return 'open_long'
            if cd > 2:
                return 'close_short'  
        else:
            if od > 6:
                return 'open_short'
            if od > 2 and pattern in self.short_group:
                return 'open_short'
            if cd > 2:
                return 'close_long'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df,self.period_rsi)
        df = add_zigzag_window_260926(df,self.period_wzz,self.frac_wzz,self.n_wzp)
        df = add_pattern18_zzw_260926(df,self.threshold_p18)
        df['buffer'] = ((df[self.wzp2] - df[self.wzp3]) / self.divider_buff).abs()
        df['pbzp2'] = df[self.wzp2] + df['buffer']
        df['mbzp2'] = df[self.wzp2] - df['buffer']
        df['pbzp3'] = df[self.wzp3] + df['buffer']
        df['mbzp3'] = df[self.wzp3] - df['buffer']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long, can_short = None, None
        if row['pattern18'] in self.long_group:
            can_long = row['pbzp3'] >= row['close']
            can_short = row['mbzp2'] <= row['close']
        
        if row['pattern18'] in self.short_group:
            can_short = row['close'] >= row['mbzp3']
            can_long = row['close'] <= row['pbzp2']
        if self.use_rsi:
            rsi = row['rsi']
            oversold = rsi <= self.threshold_rsi
            overbought = rsi >= 100 - self.threshold_rsi
            can_short = can_short and overbought
            can_long = can_long and oversold
        if can_long:
            return self.get_action_by_group(row['pattern18'],'long')
        if can_short:
            return self.get_action_by_group(row['pattern18'],'short')
        

# Очень плохой результат, открывает сделки в лой.
class UEG9_BIRDWATCHER2(BaseEG):
    '''
    stop=None, take=None, period_wzz=55, frac_wzz=0.1, n_wzp=8, buffer_pd=0.1, mult_stop=0.5, allowance=0.1, use_exp=0, use_stop=0
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_wzz=55, frac_wzz=0.1, n_wzp=8, buffer_pd=0.1, mult_stop=0.5, allowance=0.1, use_exp=0, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_wzz = period_wzz
        self.frac_wzz = frac_wzz
        self.n_wzp = n_wzp
        self.buffer_pd = buffer_pd
        self.mult_stop = mult_stop
        self.plusdelta_func = add_exp_plusdelta_peaks_wzz260926 if use_exp else add_plusdelta_peaks_wzz260926
        self.use_stop = use_stop
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_zigzag_window_260926(df,self.period_wzz,self.frac_wzz,self.n_wzp)
        df = self.plusdelta_func(df, self.buffer_pd)
        df['top_stop'] = df['top_pd'] + df['delta_pd'] * self.mult_stop
        df['bottom_stop'] = df['bottom_pd'] - df['delta_pd'] * self.mult_stop
        df['pdf_diff_percent'] = ((df['top_pd'] - df['bottom_pd']) / df['bottom_pd']) * 100
        df['allowance'] = df['pdf_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['top_stop'] > row['close'] >= row['top_pd']:
                return 'open_short'
            if row['bottom_stop'] < row['close'] <= row['bottom_pd']:
                return 'open_long'
            if self.use_stop:
                if row['close'] > row['top_stop']:
                    return 'close_short'
                if row['close'] < row['bottom_stop']:
                    return 'close_long'

# В боковике ахуенно работает. Надо подумать над версией, которая включается, только в боковике
# 05.10.2026 нужна версия с отдельной работой для боковика и тренда
# 07.10.2026 нужна версия без входа в канале (без top_stop and bottom_stop)
# 14.10.2026 тоже бывает открывает прям в хае сделки
class UEG9_GRAVY2(BaseEG):
    '''
    stop=None, take=None, period_wzz=55, frac_wzz=0.1, n_wzp=8, buffer_mean=0.1, mult_stop=0.5, use_stop=1
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_wzz=55, frac_wzz=0.1, n_wzp=8, buffer_mean=0.1, mult_stop=0.5, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_wzz = period_wzz
        self.frac_wzz = frac_wzz
        self.n_wzp = n_wzp
        self.buffer_mean = buffer_mean
        self.mult_stop = mult_stop
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_zigzag_window_260926(df,self.period_wzz,self.frac_wzz,self.n_wzp)
        df = add_mean_peaks_wzz260926(df,self.buffer_mean)
        df['top_stop'] = df['top_mean'] + df['delta_mean'] * self.mult_stop
        df['bottom_stop'] = df['bottom_mean'] - df['delta_mean'] * self.mult_stop
        df = self.add_slice_df(df)
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

# 12.10.2026 Надо подумать над тем, что бы в тренде скользящие были ближе. Может два периода для тренда и боковика
# 21.10.2026 добавить версию, которая может закрывать сделки в случает запрета одной из сторон!
# 25.10.2026 возможно стоит классифицировать паттерны и отбирать те, на которых можно заходить и те, на которых нельзя
# 27.10.2026 какие-то частые входы прям в хаях. Надо это править!
class UEG9_POLITICIAN(BaseEG):
    '''
    stop=None, take=None, period_wzz=55, frac_wzz=0.1, n_wzp=8, buffer_mean=0.1,use_rsi=0,period_rsi=30,thresh_rsi=30
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_wzz=55, frac_wzz=0.1, n_wzp=8, buffer_mean=0.1,use_rsi=0,period_rsi=30,thresh_rsi=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_wzz = period_wzz
        self.frac_wzz = frac_wzz
        self.n_wzp = n_wzp
        self.buffer_mean = buffer_mean
        self.use_rsi = use_rsi
        self.period_rsi = period_rsi
        self.thresh_rsi = thresh_rsi

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_zigzag_window_260926(df,self.period_wzz,self.frac_wzz,self.n_wzp)
        df = add_mean_peaks_wzz260926(df,self.buffer_mean)
        if self.use_rsi:
            df = add_rsi(df,self.period_rsi)
            df['can_long'] = df['rsi'] <= self.thresh_rsi
            df['can_short'] = df['rsi'] >= 100 - self.thresh_rsi
        else:
            df['can_long'] = True
            df['can_short'] = True
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['close'] >= row['top_mean'] and row['can_short']:
            return 'open_short'
        if row['close'] <= row['bottom_mean'] and row['can_long']:
            return 'open_long'
        
class UEG9_ASTRAL(BaseEG):
    '''
    stop=None, take=None, period_vc=10, divider=1,allowance=0.1
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_vc=10, divider=1,allowance=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_vc = period_vc
        self.divider = divider
        self.allowance = allowance

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_vodka_channel(df,self.period_vc)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df['mean_diff_percent'] = ((df['top_mean'] - df['bottom_mean']) / df['bottom_mean']) * 100
        df['allowance'] = df['mean_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['close'] >= row['top_buff']:
                return 'open_short'
            if row['close'] <= row['bottom_buff']:
                return 'open_long'
            
class UEG9_MEDIUM(BaseEG):
    '''
    stop=None, take=None, period_vc=10, divider=1,allowance=0.1,period_pas1=10,period_pas2=60,max_period=70,pas_thresh=20
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_vc=10, divider=1,allowance=0.1,period_pas1=10,period_pas2=60,max_period=70,pas_thresh=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_vc = period_vc
        self.period_pas1, self.period_pas2 = fix_two_periods_hm(period_pas1,period_pas2,max_period)
        self.divider = divider
        self.allowance = allowance
        self.pas_thresh = pas_thresh

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_per_above_sma(df,self.period_pas1, self.period_pas2)
        df = add_vodka_channel(df,self.period_vc)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df['mean_diff_percent'] = ((df['top_mean'] - df['bottom_mean']) / df['bottom_mean']) * 100
        df['allowance'] = df['mean_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            if row['pas'] >= 100-self.pas_thresh or row['pas'] <= self.pas_thresh:
                top = 'top_buff' 
                bottom = 'bottom_buff' 
            else:
                top = 'top_mean' 
                bottom = 'bottom_mean' 
            if row['close'] >= row[top]:
                return 'open_short'
            if row['close'] <= row[bottom]:
                return 'open_long'
    
class UEG9_TRACKER(BaseEG):
    '''
    stop=None, take=None, period_vc=10, divider=1,allowance=0.1,period_pas1=10,period_pas2=60,max_period=70,pas_thresh=20
    '''
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_vc=10, divider=1,allowance=0.1,period_pas1=10,period_pas2=60,max_period=70,pas_thresh=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_vc = period_vc
        self.period_pas1, self.period_pas2 = fix_two_periods_hm(period_pas1,period_pas2,max_period)
        self.divider = divider
        self.allowance = allowance
        self.pas_thresh = pas_thresh

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_per_above_sma(df,self.period_pas1, self.period_pas2)
        df = add_vodka_channel(df,self.period_vc)
        df = add_buffer_add(df, 'top_mean', 'bottom_mean', self.divider)
        df['mean_diff_percent'] = ((df['top_mean'] - df['bottom_mean']) / df['bottom_mean']) * 100
        df['allowance'] = df['mean_diff_percent'] > self.allowance
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['allowance']:
            can_long = True
            can_short = True
            if row['pas'] >= 100-self.pas_thresh:
                can_short = False
            if row['pas'] <= self.pas_thresh:
                can_long = False

            if row['close'] >= row['top_buff']:
                if can_short:
                    return 'open_short'
                else:
                    return 'close_long'
            if row['close'] <= row['bottom_buff']:
                if can_long:
                    return 'open_long'
                else:
                    return 'close_short'
    

        
