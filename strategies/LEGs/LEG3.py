from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_donchan_channel,add_bollinger,add_rsi,add_stochastic
from for_strategies.classic_indicators2 import add_composite_blender_score,add_fractal_dimension_index,add_hurst_exponent,add_vhf,add_variance_ratio,add_range_compression_zscore,add_percentile_rank
from for_strategies.fix_params import fix_supertrend_params,fix_two_periods_hm,fix_three_periods_hm
from for_strategies.pva_indicators import add_static_channel,add_vodka_channel
from for_strategies.help_indicators import add_buffer_add

"""Надо протестить:
add_velcro_bb
add_zechan
add_zebra
add_two_perchan
add_perchan_mid
add_perchan_sma
add_real_perdirlong
add_perdirlong
add_fractal_dimension_index
add_hurst_exponent
add_vhf
add_variance_ratio
add_range_compression_zscore
add_percentile_rank
add_kvas_channel
add_kefir_channel
add_static_channel
add_stable_ma_direction
add_bbi
"""

class LEG3a_LOTR(BaseEG):
    """stop=None, take=None, period_pr=55, period_pctdc=20, min_width_pctdc=10,max_period=70"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_pr=55, period_pctdc=20, min_width_pctdc=10,max_period=70):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.min_width_pctdc = min_width_pctdc
        self.period_pr,self.period_pctdc = fix_two_periods_hm(period_pr,period_pctdc,max_period)


    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_percentile_rank(df,self.period_pr)
        roll = df['pct_rank'].rolling(self.period_pctdc)
        df['top_pr'] = roll.max()
        df['bot_pr'] = roll.min()
        df['width_pr'] = df['top_pr'] - df['bot_pr']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
       if row['width_pr'] > self.min_width_pctdc:
           if row['pct_rank'] == row['top_pr']:
               return 'open_short'
           if row['pct_rank'] == row['bot_pr']:
               return 'open_long'