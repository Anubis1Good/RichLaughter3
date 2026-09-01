from strategies.BaseEG import BaseEG
from for_strategies.zigzag_indicators import add_dzz_peaks,add_pattern18_dzz_czd,add_stop_loss_p18czd,add_percent_zz_peaks,add_percent_zz190826

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