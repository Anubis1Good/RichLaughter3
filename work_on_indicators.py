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
df = df.iloc[-120:]
df = add_fractals(df)
df = add_rsi(df)

# 58.056667    55.53666

df = add_mean_on_fractals(df)
# print(df[['x', 'top_mean_list']].head(20))
# print(df[['x', 'bottom_mean_list']].head(20))

print(df.tail(60))