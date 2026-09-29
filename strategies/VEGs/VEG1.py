from strategies.BaseEG import BaseEG
from for_strategies.zigzag_indicators import add_dzz_peaks,add_pattern18_dzz_czd,add_stop_loss_p18czd,add_percent_zz_peaks,add_percent_zz190826, add_zigzag_window_260926, add_pattern18_zzw_260926,add_stop_loss_p18zzw_260926, add_drop_last_wzp,add_zzw_levels_260926

# Надо разбираться или не надо, есть Venus, который работает норм
class VEG1_MERCURY(BaseEG):
    """stop=None, take=None, period=20, n_std=5, threshold_dzz=0.2, buff=0.1, divider=2, use_target=0, hard_stop=1, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, n_std=5, threshold_dzz=0.2, buff=0.1, divider=2, use_target=0, hard_stop=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_std = n_std
        self.threshold_dzz = threshold_dzz
        self.buff = buff
        self.divider = divider
        self.use_stop = use_stop
        self.use_target = use_target
        self.hard_stop = hard_stop
        self.problems = 'Vanga'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_dzz_peaks(df, period=self.period, n_std=self.n_std, drop_last=False)
        # df['zigzag_peaks'] = df['zigzag_peaks'].shift(1)
        df = add_pattern18_dzz_czd(df, self.threshold_dzz, self.buff)
        df = add_stop_loss_p18czd(df, self.divider)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata

    def stop_loss_action(self, row):
        if self.use_stop:
            if row['close'] > row['ssl']:
                return 'close_short'
            if row['close'] < row['lsl']:
                return 'close_long'
        return None

    def _get_action_from_row(self, row):
        # long
        if row['pattern18'] == 'joc':
            if row['bzp3'] < row['close'] <= row['bzp2']:
                return 'open_long'
        
        if row['pattern18'] == 'btc':
            if self.use_target:
                if row['target'] >= row['close'] >= row['btarget']:
                    return 'close_long'
            if row['zp4'] <= row['close'] <= row['bzp4']:
                return 'open_long'
            if self.hard_stop:
                return 'close_short'
        
        # short
        if row['pattern18'] == 'bui':
            if row['bzp3'] > row['close'] >= row['bzp2']:
                return 'open_short'
        
        if row['pattern18'] == 'bti':
            if self.use_target:
                if row['target'] <= row['close'] <= row['btarget']:
                    return 'close_short'
            if row['zp4'] >= row['close'] >= row['bzp4']:
                return 'open_short'
            if self.hard_stop:
                return 'close_long'
        
        # range
        if row['pattern18'] in ('top_range', 'double_top', 'weak_long'):
            if row['bzp1'] <= row['close'] <= row['bzp3']:
                return 'open_long'
            if row['bzp2'] >= row['close'] >= row['bzp4']:
                return 'open_short'
        
        if row['pattern18'] in ('bottom_range', 'double_bottom', 'weak_short'):
            if row['bzp1'] >= row['close'] >= row['bzp3']:
                return 'open_short'
            if row['bzp2'] <= row['close'] <= row['bzp4']:
                return 'open_long'
        
        if row['pattern18'] == 'narrowing_up':
            if row['bzp1'] >= row['close'] >= row['bzp3']:
                return 'close_long'
            if row['bzp2'] <= row['close'] <= row['zp2']:
                return 'close_short'
        
        if row['pattern18'] == 'narrowing_down':
            if row['bzp1'] <= row['close'] <= row['bzp3']:
                return 'close_short'
            if row['bzp2'] >= row['close'] >= row['zp2']:
                return 'close_long'
        
        if row['pattern18'] == 'upthrust':
            if row['zp3'] >= row['close'] >= row['bzp3']:
                return 'open_short'
            if row['bzp2'] <= row['close'] <= row['bzp4']:
                return 'open_long'
            if row['bzp3'] > row['close'] >= row['mzp']:
                return 'close_long'
        
        if row['pattern18'] == 'spring':
            if row['zp3'] <= row['close'] <= row['bzp3']:
                return 'open_long'
            if row['bzp2'] >= row['close'] >= row['bzp4']:
                return 'open_short'
            if row['bzp3'] < row['close'] <= row['mzp']:
                return 'close_short'
        
        if row['pattern18'] == 'sow':
            if row['bzp3'] > row['close'] >= row['bzp2']:
                return 'open_short'
        
        if row['pattern18'] == 'sos':
            if row['bzp3'] < row['close'] <= row['bzp2']:
                return 'open_long'
        
        return self.stop_loss_action(row)

# Кажется он очень плохо работает в тренде
# Сделать вариант VENUS, который работает только в боковике
# При прорыве структуры может закрывать сделки в хаях с выключенным стопом
# Пересмотреть работу в тренде!
class VEG1_VENUS(BaseEG):
    """stop=None, take=None,  percent_threshold=0.2, threshold_dzz=0.2, buff=0.1, divider=2, use_target=0, hard_stop=1, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,  percent_threshold=0.2, threshold_dzz=0.2, buff=0.1, divider=2, use_target=0, hard_stop=1, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.percent_threshold = percent_threshold
        self.threshold_dzz = threshold_dzz
        self.buff = buff
        self.divider = divider
        self.use_stop = use_stop
        self.use_target = use_target
        self.hard_stop = hard_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_percent_zz190826(df, percent_threshold=self.percent_threshold)
        df['zigzag_peaks'] = df['zigzag_peaks'].shift(1)
        df = add_pattern18_dzz_czd(df, self.threshold_dzz, self.buff)
        df = add_stop_loss_p18czd(df, self.divider)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata

    def stop_loss_action(self, row):
        if self.use_stop:
            if row['close'] > row['ssl']:
                return 'close_short'
            if row['close'] < row['lsl']:
                return 'close_long'
        return None

    def _get_action_from_row(self, row):
        # long
        if row['pattern18'] == 'joc':
            if row['bzp3'] < row['close'] <= row['bzp2']:
                return 'open_long'
        
        if row['pattern18'] == 'btc':
            if self.use_target:
                if row['target'] >= row['close'] >= row['btarget']:
                    return 'close_long'
            if row['zp4'] <= row['close'] <= row['bzp4']:
                return 'open_long'
            if self.hard_stop:
                return 'close_short'
        
        # short
        if row['pattern18'] == 'bui':
            if row['bzp3'] > row['close'] >= row['bzp2']:
                return 'open_short'
        
        if row['pattern18'] == 'bti':
            if self.use_target:
                if row['target'] <= row['close'] <= row['btarget']:
                    return 'close_short'
            if row['zp4'] >= row['close'] >= row['bzp4']:
                return 'open_short'
            if self.hard_stop:
                return 'close_long'
        
        # range
        if row['pattern18'] in ('top_range', 'double_top', 'weak_long'):
            if row['bzp1'] <= row['close'] <= row['bzp3']:
                return 'open_long'
            if row['bzp2'] >= row['close'] >= row['bzp4']:
                return 'open_short'
        
        if row['pattern18'] in ('bottom_range', 'double_bottom', 'weak_short'):
            if row['bzp1'] >= row['close'] >= row['bzp3']:
                return 'open_short'
            if row['bzp2'] <= row['close'] <= row['bzp4']:
                return 'open_long'
        
        if row['pattern18'] == 'narrowing_up':
            if row['bzp1'] >= row['close'] >= row['bzp3']:
                return 'close_long'
            if row['bzp2'] <= row['close'] <= row['zp2']:
                return 'close_short'
        
        if row['pattern18'] == 'narrowing_down':
            if row['bzp1'] <= row['close'] <= row['bzp3']:
                return 'close_short'
            if row['bzp2'] >= row['close'] >= row['zp2']:
                return 'close_long'
        
        if row['pattern18'] == 'upthrust':
            if row['zp3'] >= row['close'] >= row['bzp3']:
                return 'open_short'
            if row['bzp2'] <= row['close'] <= row['bzp4']:
                return 'open_long'
            if row['bzp3'] > row['close'] >= row['mzp']:
                return 'close_long'
        
        if row['pattern18'] == 'spring':
            if row['zp3'] <= row['close'] <= row['bzp3']:
                return 'open_long'
            if row['bzp2'] >= row['close'] >= row['bzp4']:
                return 'open_short'
            if row['bzp3'] < row['close'] <= row['mzp']:
                return 'close_short'
        
        if row['pattern18'] == 'sow':
            if row['bzp3'] > row['close'] >= row['bzp2']:
                return 'open_short'
        
        if row['pattern18'] == 'sos':
            if row['bzp3'] < row['close'] <= row['bzp2']:
                return 'open_long'
        
        return self.stop_loss_action(row)

# TODO надо лучше поработать над паттернами. Может стоит учитывать предыдущий паттерн. Пока странно выглядит.
class VEG1_EARTH(BaseEG):
    """stop=None, take=None, \n
        period_wzz=55, frac_wzz=0.1, n_wzp=8, threshold_p18=0.1, drop_last=1, buff=0.1, divider=2, use_target=0, hard_stop=0, use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,  period_wzz=55, frac_wzz=0.1, n_wzp=8, threshold_p18=0.1, drop_last=1, buff=0.1, divider=2, use_target=0, hard_stop=0, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_wzz = period_wzz
        self.frac_wzz = frac_wzz
        self.n_wzp = n_wzp
        self.threshold_p18 = threshold_p18
        self.drop_last = drop_last
        self.buff = buff
        self.divider = divider
        self.use_stop = use_stop
        self.use_target = use_target
        self.hard_stop = hard_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_zigzag_window_260926(df,self.period_wzz,self.frac_wzz,self.n_wzp)
        if self.drop_last:
            df = add_drop_last_wzp(df)
        df = add_pattern18_zzw_260926(df,self.threshold_p18)
        df = add_zzw_levels_260926(df,self.buff)
        df = add_stop_loss_p18zzw_260926(df, self.divider)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata

    def stop_loss_action(self, row):
        if self.use_stop:
            if row['close'] > row['ssl']:
                return 'close_short'
            if row['close'] < row['lsl']:
                return 'close_long'
        return None

    def _get_action_from_row(self, row):
        # long
        if row['pattern18'] == 'joc':
            if row['bzp3'] < row['close'] <= row['bzp2']:
                return 'open_long'
        
        if row['pattern18'] == 'btc':
            if self.use_target:
                if row['target'] >= row['close'] >= row['btarget']:
                    return 'close_long'
            if row['zp4'] <= row['close'] <= row['bzp4']:
                return 'open_long'
            if self.hard_stop:
                return 'close_short'
        
        # short
        if row['pattern18'] == 'bui':
            if row['bzp3'] > row['close'] >= row['bzp2']:
                return 'open_short'
        
        if row['pattern18'] == 'bti':
            if self.use_target:
                if row['target'] <= row['close'] <= row['btarget']:
                    return 'close_short'
            if row['zp4'] >= row['close'] >= row['bzp4']:
                return 'open_short'
            if self.hard_stop:
                return 'close_long'
        
        # range
        if row['pattern18'] in ('top_range', 'double_top', 'weak_long'):
            if row['bzp1'] <= row['close'] <= row['bzp3']:
                return 'open_long'
            if row['bzp2'] >= row['close'] >= row['bzp4']:
                return 'open_short'
        
        if row['pattern18'] in ('bottom_range', 'double_bottom', 'weak_short'):
            if row['bzp1'] >= row['close'] >= row['bzp3']:
                return 'open_short'
            if row['bzp2'] <= row['close'] <= row['bzp4']:
                return 'open_long'
        
        if row['pattern18'] == 'narrowing_up':
            if row['bzp1'] >= row['close'] >= row['bzp3']:
                return 'close_long'
            if row['bzp2'] <= row['close'] <= row['zp2']:
                return 'close_short'
        
        if row['pattern18'] == 'narrowing_down':
            if row['bzp1'] <= row['close'] <= row['bzp3']:
                return 'close_short'
            if row['bzp2'] >= row['close'] >= row['zp2']:
                return 'close_long'
        
        if row['pattern18'] == 'upthrust':
            if row['zp3'] >= row['close'] >= row['bzp3']:
                return 'open_short'
            if row['bzp2'] <= row['close'] <= row['bzp4']:
                return 'open_long'
            if row['bzp3'] > row['close'] >= row['mzp']:
                return 'close_long'
        
        if row['pattern18'] == 'spring':
            if row['zp3'] <= row['close'] <= row['bzp3']:
                return 'open_long'
            if row['bzp2'] >= row['close'] >= row['bzp4']:
                return 'open_short'
            if row['bzp3'] < row['close'] <= row['mzp']:
                return 'close_short'
        
        if row['pattern18'] == 'sow':
            if row['bzp3'] > row['close'] >= row['bzp2']:
                return 'open_short'
        
        if row['pattern18'] == 'sos':
            if row['bzp3'] < row['close'] <= row['bzp2']:
                return 'open_long'
        
        return self.stop_loss_action(row)
    

class VEG1_MOON(BaseEG):
    """stop=None, take=None, \n
    divider_buff=5, period_wzz=30, frac_wzz=0.1, n_wzp=6, threshold_p18=0.1, close_ext_trend=1,close_mid_range=1,close_mid_weak=1,open_reverse_weak=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, divider_buff=5, period_wzz=30, frac_wzz=0.1, n_wzp=6, threshold_p18=0.1, close_ext_trend=1,close_mid_range=1,close_mid_weak=1,open_reverse_weak=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.divider_buff = divider_buff
        self.period_wzz = period_wzz
        self.frac_wzz = frac_wzz
        self.n_wzp = n_wzp
        self.threshold_p18 = threshold_p18
        self.close_ext_trend = close_ext_trend
        self.close_mid_range = close_mid_range
        self.close_mid_weak = close_mid_weak
        self.open_reverse_weak = open_reverse_weak
        self.wzp2 = f'wzp{n_wzp - 2}'
        self.wzp3 = f'wzp{n_wzp - 1}'
        self.wzp4 = f'wzp{n_wzp}'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_zigzag_window_260926(df,self.period_wzz,self.frac_wzz,self.n_wzp)
        df = add_pattern18_zzw_260926(df,self.threshold_p18)
        df['buffer'] = ((df[self.wzp2] - df[self.wzp3]) / self.divider_buff).abs()
        df['pbzp2'] = df[self.wzp2] + df['buffer']
        df['mbzp2'] = df[self.wzp2] - df['buffer']
        df['pbzp3'] = df[self.wzp3] + df['buffer']
        df['mbzp3'] = df[self.wzp3] - df['buffer']
        df['pbzp4'] = df[self.wzp4] + df['buffer']
        df['mbzp4'] = df[self.wzp4] - df['buffer']
        df['mid_wzp23'] = (df[self.wzp2]+df[self.wzp3]) / 2
        df['mid_wzp34'] = (df[self.wzp3]+df[self.wzp4]) / 2
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        pattern = row['pattern18']
        close = row['close']
        if pattern == 'bui':
            if close >= row['mbzp2']:
                return 'open_short'
            if self.close_ext_trend and close <= row['pbzp4']:
                return 'close_short'
        if pattern == 'joc':
            if close <= row['pbzp2']:
                return 'open_long'
            if self.close_ext_trend and close >= row['mbzp4']:
                return 'close_long'
        if pattern == 'weak_short':
            if close >= row['mbzp3']:
                return 'open_short'
            if self.close_mid_weak and close <= row['mid_wzp23']:
                return 'close_short'
            if self.open_reverse_weak:
                if close > row['mid_wzp23']:
                    return 'close_long'
                if close <= row['pbzp2']:
                    return 'open_long'
        if pattern == 'weak_long':
            if close <= row['pbzp3']:
                return 'open_long'
            if self.close_mid_weak and close >= row['mid_wzp23']:
                return 'close_long'
            if self.open_reverse_weak:
                if close < row['mid_wzp23']:
                    return 'close_short'
                if close >= row['mbzp2']:
                    return 'open_short'
        if pattern == 'narrowing_up':
            if close >= row['mbzp3']:
                return 'open_short'
            if close <= row['mid_wzp23']:
                return 'open_long'
        if pattern == 'narrowing_down':
            if close <= row['pbzp3']:
                return 'open_long'
            if close >= row['mid_wzp23']:
                return 'open_short'
        if pattern == 'bottom_range' or pattern == 'double_top' or pattern == 'upthrust':
            if close >= row['mbzp3']:
                return 'open_short'
            if close <= row['pbzp2']:
                return 'open_long'
            if self.close_mid_range:
                if close > row['mid_wzp23']:
                    return 'close_long'
                else:
                    return 'close_short'
        if pattern == 'top_range' or pattern == 'double_bottom' or pattern == 'spring':
            if close <= row['pbzp3']:
                return 'open_long'
            if close >= row['mbzp2']:
                return 'open_short'
            if self.close_mid_range:
                if close < row['mid_wzp23']:
                    return 'close_short'
                else:
                    return 'close_long'
        if pattern == 'sow':
            if close >= row['mid_wzp34']:
                return 'open_short'
            if self.close_ext_trend and close <= row['pbzp4']:
                return 'close_short'
        if pattern == 'sos':
            if close <= row['mid_wzp34']:
                return 'open_long'
            if self.close_ext_trend and close >= row['mbzp4']:
                return 'close_long'
        if pattern == 'bti':
            if close >= row['mid_wzp23']:
                return 'open_short'
        if pattern == 'btc':
            if close <= row['mid_wzp23']:
                return 'open_long'
            