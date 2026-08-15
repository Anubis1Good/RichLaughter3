from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_chop,add_adx,add_donchan_channel
from for_strategies.zigzag_indicators import add_dzz_peaks,add_analys_dzz
from for_strategies.help_indicators import add_ideal_pos
from for_strategies.ml_indicators import add_segmented_regression_from_end,add_find_similar_pattern_lite
from sklearn.tree import DecisionTreeClassifier

class SEGML2_NEWAVE(BaseEG):
    """stop=None, take=None, period=60, min_points=5, multiplier=1, threshold=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, min_points=5, multiplier=1, threshold=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.min_points = min_points
        self.multiplier = multiplier
        self.threshold = threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_segmented_regression_from_end(df, self.period, self.multiplier, self.min_points)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['upper_channel'] < row['close'] and row['rsi'] > 100 - self.threshold:
            return 'open_short'
        if row['lower_channel'] > row['close'] and row['rsi'] < self.threshold:
            return 'open_long'
        
        return None

#TODO Переделать
class SEGML2_SID(BaseEG):
    """stop=None, take=None, period=200, window=10, forecast_length=5, threshold=30, percent_threshold=0.1
    \n
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=200, window=10, forecast_length=5, threshold=30, percent_threshold=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.window = window
        self.forecast_length = forecast_length
        self.threshold = threshold
        self.percent_threshold = percent_threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_rsi(df, self.window)
        df = add_find_similar_pattern_lite(df, self.window, self.period, forecast_length=self.forecast_length)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata

    def _get_action_from_row(self, row):
        if row is None:
            return None
        
        delta_fc = (row['forecast_high'] - row['forecast_low']) / 10
        
        if row['close'] > row['forecast_high'] - delta_fc:
            if row['per_fs'] > self.percent_threshold and row['rsi'] > 100 - self.threshold:
                return 'open_short'
            else:
                return 'close_long'
        
        if row['close'] < row['forecast_low'] + delta_fc:
            if row['per_fs'] > self.percent_threshold and row['rsi'] < self.threshold:
                return 'open_long'
            else:
                return 'close_short'
        
        return None
            
#что-то интересное         
class SEGML2_TRENDWAVE(BaseEG):
    """stop=None, take=None, period=60, min_points=5, multiplier=1, threshold_enter=40, threshold_exit=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=60, min_points=5, multiplier=1, threshold_enter=40, threshold_exit=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.min_points = min_points
        self.multiplier = multiplier
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_segmented_regression_from_end(df, self.period, self.multiplier, self.min_points)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df, self.period)
        pdata['chart'] = df
        return pdata

    def _get_action_from_row(self, row):
        if row['upper_channel'] < row['close']:
            if row['rsi'] > 100 - self.threshold_enter and row['regression_slope'] < 0:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if row['lower_channel'] > row['close']:
            if row['rsi'] < self.threshold_enter and row['regression_slope'] > 0:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        return None
            
#хз хз тут даже не очень понятно, на какой сигнал открыть что
class SEGML2b_RAPTOR(BaseEG):
    """stop=None, take=None, period=60, n_std=3, period_dc=30, period_rsi=30, period_adx=30, mode_ideal=0, mode_enter=0, max_depth=None"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_std=3, period_dc=30, period_rsi=30, period_adx=30, mode_ideal=0, mode_enter=0, max_depth=None):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_std = n_std
        self.model = None
        self.period_dc = period_dc
        self.period_rsi = period_rsi
        self.period_adx = period_adx
        self.max_depth = max_depth
        if mode_ideal == 0:
            self.mode_ideal = 'ideal_pos'
        else:
            self.mode_ideal = 'ideal_enter'
        if mode_enter == 0:
            self.enters = (2, 1)
        else:
            self.enters = (1, 2)

    def get_model(self, X_train, y_train):
        if self.max_depth:
            self.model = DecisionTreeClassifier(max_depth=self.max_depth)
        else:
            self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dzz_peaks(df, n_std=self.n_std, period=self.period)
        df = add_ideal_pos(df)
        df = add_donchan_channel(df, self.period_dc)
        df = add_adx(df, self.period_adx)
        df['adx'] = df['adx'] / 100
        df = add_chop(df, self.period_adx)
        df['chop'] = df['chop'] / 100
        df = add_rsi(df, period=self.period_rsi)
        df['rsi'] = df['rsi'] / 100
        df = add_analys_dzz(df, self.period_dc)
        df['trend'] = (df['trend'] + 1) / 2
        df['trend_sma'] = (df['trend_sma'] + 1) / 2
        df['c_max_hb'] = df['close'] >= df['max_hb']
        df['c_min_hb'] = df['close'] <= df['min_hb']
        df['c_avarege'] = df['close'] >= df['min_hb']
        # Инициализируем сигнал нулями
        df['signal'] = 0
        train_set = ['trend', 'trend_sma', 'c_max_hb', 'c_min_hb', 'c_avarege', 'rsi', 'chop', 'adx']

        # Убедимся, что нет пропущенных значений
        df_train = df.copy()
        df_train = df_train.dropna(subset=train_set + [self.mode_ideal]).copy()
        if not df_train.empty:
            y_train = df_train[self.mode_ideal]
            X_train = df_train[train_set]

            # Обучаем модель
            self.get_model(X_train, y_train)
            # Получаем предсказания и присваиваем их обратно в исходный DataFrame
            df.loc[X_train.index, 'signal'] = self.model.predict(X_train)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata

    def _get_action_from_row(self, row):
        if row['signal'] == self.enters[0]:
            return 'open_long'
        if row['signal'] == self.enters[1]:
            return 'open_short'
        
        return None