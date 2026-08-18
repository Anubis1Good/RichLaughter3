import numpy as np
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_chop,add_awesome_oscillator,add_donchan_channel,add_adx
from for_strategies.pva_indicators import add_kusuruken_channel,add_velcro_indicator,add_quantile_params,add_benefit,get_all_enter_exit_DC,get_all_lup,add_pc_stair_fast,add_integrity_index,add_assessment_motion_index,add_hope_channel,add_cascade_channel
from for_strategies.other_indicators import add_vangerchik

class PEG11_KUSURUKEN(BaseEG):
    """stop=None, take=None, period=55, period2=10, period3=20, threshold=20, kind_enter='hl',max_period=55 \n
    kind_enter -> hl | c
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period2=10, period3=20, threshold=20, kind_enter='hl',max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        can_period = max_period // 3
        self.period3 = min(can_period,period3)
        max_total = can_period * 2
        total = self.period3 + period2

        if total > max_total:
            ratio = max_total / total
            self.period3 = int(self.period3 * ratio)
            self.period2 = int(period2 * ratio)
        else:
            self.period2 = period2

        self.threshold = threshold
        self.kind_enter_l = 'low' if kind_enter == 'hl' else 'close'
        self.kind_enter_s = 'high' if kind_enter == 'hl' else 'close'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_channel(df, self.period2, self.period)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # trend_context
        if row['sma'] > row['sma2']:
            # long_context
            if row["avarege"] > row['avarege2']:
                if row['rsi'] > 100 - self.threshold + 10:
                    return 'close_long'
                if row[self.kind_enter_l] <= row['avarege2']:
                    return 'open_long'
            # short_context
            else:
                if row['rsi'] < self.threshold - 10:
                    return 'close_short'
                if row[self.kind_enter_s] >= row['avarege2']:
                    return 'open_short'
        # range_context
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold:
                return 'open_short'
        
        return None

class PEG13_DWDDCr(BaseEG):
    """stop=None, take=None, period=60, threshold=30, period2=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, threshold=30, period2=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        df = add_awesome_oscillator(df, long_period=self.period)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold:
            if row['ao'] > 0:
                return 'open_long'
            else:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold:
            if row['ao'] < 0:
                return 'open_short'
            else:
                return 'close_long'
        
        return None

class PEG14_RWDDCr(BaseEG):
    """stop=None, take=None, period=20, threshold=30, period2=10, period3=20,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30, period2=10, period3=20,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        can_period = max_period // 3
        self.period3 = min(can_period,period3)
        max_total = can_period * 2
        total = self.period3 + period2

        if total > max_total:
            ratio = max_total / total
            self.period3 = int(self.period3 * ratio)
            self.period2 = int(period2 * ratio)
        else:
            self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = add_chop(df, self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['sma'] > row['sma2']:
            return 'close_all'
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold:
                return 'open_short'
        
        return None

class PEG14_RANGER(BaseEG):
    """stop=None, take=None, period=55, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        can_period = max_period // 2
        self.period = min(period,can_period)
        self.threshold_rsi = threshold_rsi
        self.threshold_chop = threshold_chop
        self.threshold_adx = threshold_adx
        self.period2 = period2
        self.period3 = period3

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period3)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period2)
        df = add_adx(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        ranger = row['chop'] > self.threshold_chop and row['adx'] < self.threshold_adx
        if not ranger:
            return 'close_all'
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold_rsi:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold_rsi:
                return 'open_short'
        
        return None

class PEG14_RENEGADE(BaseEG):
    """stop=None, take=None, period=55, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        can_period = max_period // 2
        self.period = min(period,can_period)
        self.threshold_rsi = threshold_rsi
        self.threshold_chop = threshold_chop
        self.threshold_adx = threshold_adx
        self.period2 = period2
        self.period3 = period3

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period3)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period2)
        df = add_adx(df, self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        ranger = row['chop'] > self.threshold_chop and row['adx'] < self.threshold_adx
        if ranger:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold_rsi:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold_rsi:
                return 'open_short'
        
        return None

class PEG15_ANNA(BaseEG):
    """stop=None, take=None, period=20, threshold=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df, self.period)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if not np.isnan(row['end_down']):
            if nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            else:
                return 'close_short'
        
        if not np.isnan(row['end_up']):
            if row['rsi'] > 100 - self.threshold:
                return 'open_short'
            else:
                return 'close_long'
        
        return None

class PEG15_SILVANA(BaseEG):
    """stop=None, take=None, period=20, threshold=30, period2=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30, period2=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df, self.period2)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['low'] < row['min_hb']:
            return 'close_long'
        if row['high'] > row['max_hb']:
            return 'close_short'
        
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if not np.isnan(row['end_down']):
            if nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            else:
                return 'close_short'
        
        if not np.isnan(row['end_up']):
            if row['rsi'] > 100 - self.threshold:
                return 'open_short'
            else:
                return 'close_long'
        
        return None

#Долгий, но использовать можно
# TODO решить проблему с индикаторами. Заглядывают слишком сильнов историю
class PEG16_LEORIC(BaseEG):
    """stop=None, take=None, period=30, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=50, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'DCr', self.period)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'avarege')
        df = add_benefit(df, all_starts, all_ends, 'DCmaxa', self.period)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'avarege', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'DCmina', self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata

    def get_bests(self, row):
        target_indices_long = ['bl_DCr', 'bl_DCmaxa', 'bl_DCmina']
        target_indices_short = ['bs_DCr', 'bs_DCmaxa', 'bs_DCmina']
        filtered_l = row[target_indices_long]
        filtered_s = row[target_indices_short]
        best_l = filtered_l.idxmax()
        best_s = filtered_s.idxmax()
        if best_l == 'bl_DCr':
            kind_l = 'min_hb'
            kind_cl = 'max_hb'
        if best_l == 'bl_DCmaxa':
            kind_l = 'avarege'
            kind_cl = 'max_hb'
        if best_l == 'bl_DCmina':
            kind_l = 'min_hb'
            kind_cl = 'avarege'
        if best_s == 'bs_DCr':
            kind_s = 'max_hb'
            kind_cs = 'min_hb'
        if best_s == 'bs_DCmaxa':
            kind_s = 'max_hb'
            kind_cs = 'avarege'
        if best_s == 'bs_DCmina':
            kind_s = 'avarege'
            kind_cs = 'min_hb'
        return best_l, best_s, kind_l, kind_s, kind_cl, kind_cs

    def _get_action_from_row(self, row):
        best_l, best_s, kind_l, kind_s, kind_cl, kind_cs = self.get_bests(row)
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row[best_l] > 0 and row['low'] <= row[kind_l] and nearest_long:
            return 'open_long'
        
        if row[best_s] > 0 and not nearest_long and row['high'] >= row[kind_s]:
            return 'open_short'
        
        if row['low'] <= row[kind_cs] and not nearest_long:
            return 'close_short'
        
        if row['high'] >= row[kind_cl] and nearest_long:
            return 'close_long'
        
        return None

#Быстрый товарищ
# TODO решить проблему с индикаторами. Заглядывают слишком сильнов историю
class PEG16_CHEN(BaseEG):
    """stop=None, take=None, period=30, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=30, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'DCr', self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        best_l = 'bl_DCr'
        best_s = 'bs_DCr'
        kind_l = 'min_hb'
        kind_s = 'max_hb'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row[best_l] > 0 and row['low'] <= row[kind_l] and nearest_long:
            return 'open_long'
        
        if row[best_s] > 0 and not nearest_long and row['high'] >= row[kind_s]:
            return 'open_short'
        
        if row['low'] <= row[kind_l] and nearest_long:
            return 'close_short'
        
        if row['high'] >= row[kind_s] and not nearest_long:
            return 'close_long'
        
        if row[best_l] < 0:
            return 'close_long'
        
        if row[best_s] < 0:
            return 'close_short'
        
        return None
        
#Быстрый товарищ     
# TODO решить проблему с индикаторами. Заглядывают слишком сильнов историю
class PEG16_ARTANIS(BaseEG):
    """stop=None, take=None, period=30, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=30, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        all_starts, all_ends = get_all_lup(df, 'max_hb', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'EDCr', self.period)
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        best_l = 'bl_EDCr'
        best_s = 'bs_EDCr'
        
        if not np.isnan(row['end_up']):
            if row[best_s] > 0:
                return 'open_short'
            else:
                return 'close_long'
        
        if not np.isnan(row['end_down']):
            if row[best_l] > 0:
                return 'open_long'
            else:
                return 'close_short'
        
        if row[best_l] < 0:
            return 'close_long'
        
        if row[best_s] < 0:
            return 'close_short'
        
        return None

class PEG17_PHOENIX(BaseEG):
    """stop=None, take=None, period=100, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, use_stop=0, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, use_stop=0, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.use_stop = use_stop

        max_total = (max_period // 3) * 2
        total = period_dc + period_velcro

        if total > max_total:
            ratio = max_total / total
            self.period_dc = int(period_dc * ratio)
            self.period_velcro = int(period_velcro * ratio)
        else:
            self.period_dc = period_dc
            self.period_velcro = period_velcro

        total = period + period_rsi

        if total > max_total:
            ratio = max_total / total
            self.period = int(period * ratio)
            self.period_rsi = int(period_rsi * ratio)
        else:
            self.period = period
            self.period_rsi = period_rsi

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['velcro'] > 100 - self.threshold_velcro:  # long
            if row['low'] <= row["avarege"]:
                return 'open_long'
            else:
                if self.use_stop:
                    return 'close_short'

        elif row['velcro'] < self.threshold_velcro:  # short
            if row['high'] >= row["avarege"]:
                return 'open_short'
            else:
                if self.use_stop:
                    return 'close_long'
        else:  # range
            if row['low'] <= row['min_hb'] and row['rsi'] <= row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] >= row['top_q']:
                return 'open_short'
        
        return None

class PEG18_REXXAR(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period2)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['stair']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        
        if row['high'] >= row['max_hb']:
            if not nearest_long:
                if not can_long and row['rsi'] > 100 - self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
        
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'

class PEG18_UTER(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, threshold=30, threshold_adx=40, period3=30, use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold=30, threshold_adx=40, period3=30, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.period3 = period3
        self.threshold_adx = threshold_adx
        self.threshold = threshold
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_adx(df, self.period3)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['adx'] > self.threshold_adx:
            can_long = row['close'] > row['stair']
            
            if row['low'] <= row['min_hb'] and nearest_long:
                if can_long:
                    return 'open_long'
                if row['rsi'] < self.threshold:
                    return 'close_short'
            
            if row['high'] >= row['max_hb'] and not nearest_long:
                if not can_long:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold:
                    return 'close_long'
            
            if self.use_stop:
                if can_long:
                    return 'close_short'
                else:
                    return 'close_long'
        else:
            if row['low'] <= row['min_hb'] and nearest_long:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not nearest_long:
                return 'open_short'
        
        return None

class PEG18_DIABLO(BaseEG):
    """stop=None, take=None, period=55, n_stairs=3, period2=10, threshold=30,use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold=30,use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold = threshold
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['stair']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['close'] <= row['avarege'] and nearest_long and can_long:
            return 'open_long'
        
        if row['close'] >= row['avarege'] and not nearest_long and not can_long:
            return 'open_short'
        
        if row['rsi'] < self.threshold and row['low'] <= row['min_hb']:
            return 'close_short'
        
        if row['rsi'] > 100 - self.threshold and row['high'] >= row['max_hb']:
            return 'close_long'
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'
        
class PEG18_VARIAN(BaseEG):
    """stop=None, take=None, period=55, n_stairs=3, period2=10, threshold=30, threshold_ii=25, period_ii=10, use_stop=0)"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, n_stairs=3, period2=10, threshold=30, threshold_ii=25, period_ii=10, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold = threshold
        self.threshold_ii = threshold_ii
        self.use_stop = use_stop
        self.period_ii = period_ii
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_integrity_index(df, self.period_ii)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['stair']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if nearest_long and can_long:
            if row['close'] <= row['avarege'] and row['ii'] > self.threshold_ii:
                return 'open_long'
            if row['low'] <= row['min_hb']:
                return 'open_long'
        
        if not nearest_long and not can_long:
            if row['close'] >= row['avarege'] and row['ii'] < -self.threshold_ii:
                return 'open_short'
            if row['high'] >= row['max_hb']:
                return 'open_short'
        
        if row['rsi'] < self.threshold and row['low'] <= row['min_hb']:
            return 'close_short'
        
        if row['rsi'] > 100 - self.threshold and row['high'] >= row['max_hb']:
            return 'close_long'
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'

class PEG18_BLAZE(BaseEG):
    """period=55, period2=10, period3=55, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period2=10, period3=55, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period2 = period2
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period + period3

        if total > max_total:
            ratio = max_total / total
            self.period = int(period * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period = period
            self.period3 = period3

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        df = add_assessment_motion_index(df, self.period, self.period3)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['ami'] > row['ami_filter']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if not can_long and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'
        
        return None

class PEG19_YREL(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_hope_channel(df, self.n_stairs, self.period2, self.shift)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_VALEERA(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_hope_channel(df, self.n_stairs, self.period, self.shift)
        df = add_donchan_channel(df, self.period2)
        df = add_vangerchik(df)
        df = add_rsi(df, self.period2)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['close'] < df['max_vg']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['close'] > df['min_vg']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        
        if not np.isnan(row['end_up']):
            if not can_long:
                return 'open_short'
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if not np.isnan(row['end_down']):
            if not can_short:
                return 'open_long'
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_ZERATUL(BaseEG):
    """stop=None, take=None, period=55, n_stairs=3, period2=55, period3=55, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=55, period3=55, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_vangerchik(df)
        df = add_rsi(df, self.period)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['close'] < df['max_vg']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['close'] > df['min_vg']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        
        if not np.isnan(row['end_up']):
            if not can_long:
                return 'open_short'
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if not np.isnan(row['end_down']):
            if not can_short:
                return 'open_long'
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_JOHANNA(BaseEG):
    """stop=None, take=None, period=10,n_stairs=3,period2=10,period3=20,threshold_enter=40,threshold_exit=20,use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10,n_stairs=3,period2=10,period3=20,threshold_enter=40,threshold_exit=20,use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        if row['high'] >= row['max_hb']:
            if not nearest_long :
                if can_short and row['rsi'] > 100-self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100-self.threshold_exit:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'

class PEG19_CASSIA(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.threshold_middle = (threshold_enter + threshold_exit) // 2
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        threshold_enter = self.threshold_middle if can_long and can_short else self.threshold_enter
        threshold_exit = self.threshold_middle if can_long and can_short else self.threshold_exit
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < threshold_enter:
                return 'open_long'
            if row['rsi'] < threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if can_short and row['rsi'] > 100 - threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_IMPERIUS(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.threshold_middle = (threshold_enter + threshold_exit) // 2
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        threshold_enter = self.threshold_middle if can_long and can_short else self.threshold_enter
        threshold_exit = self.threshold_middle if can_long and can_short else self.threshold_exit
        
        if nearest_long:
            if can_long and not can_short and row['close'] <= row['avarege']:
                return 'open_long'
            if row['low'] <= row['min_hb']:
                if can_long and row['rsi'] < threshold_enter:
                    return 'open_long'
                if row['rsi'] < threshold_exit:
                    return 'close_short'
        
        if not nearest_long:
            if can_short and not can_long and row['close'] >= row['avarege']:
                return 'open_short'
            if row['high'] >= row['max_hb']:
                if can_short and row['rsi'] > 100 - threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - threshold_exit:
                    return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None