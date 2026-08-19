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
# df = df.iloc[-60:]
# df = add_fractals(df)
# df = add_rsi(df)
max_period = 55
can_period = max_period // 3
# 58.056667    55.53666
period=55
period2=55
df = add_bollinger(df, period=period)
df = add_ema(df, period=period // 2)
df = add_pc_stair_fast(df, 3, period)
df = add_adx(df,27)
df['bbu_detach'] = (df['high'] < df['bbu']) & (df['high'].shift(1) < df['bbu'].shift(1)) & (df['high'].shift(2) > df['bbu'].shift(2))
df['bbd_detach'] = (df['low'] > df['bbd']) & (df['low'].shift(1) > df['bbd'].shift(1)) & (df['low'].shift(2) < df['bbd'].shift(2))


print(df.tail(60))