from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *

from utils.work_dfs.load_df import simple_load_df

filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'

df = simple_load_df(filepath)
df = df.iloc[-60:]
df = add_fractals(df)
# df = add_rsi(df)
max_period = 55
can_period = max_period // 3
# 58.056667    55.53666
df = add_donchan_channel(df, 10)
all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'min_hb')
df = add_benefit(df, all_starts, all_ends, 'DCr',50)


print(df.tail(60))