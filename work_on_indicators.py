from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *
from testing.test_constants import *
from utils.work_dfs.load_df import simple_load_df

# PATH_DF = '_data_for_tests\_before_opt\ALRS_5_1787155697.parquet'

df = simple_load_df(PATH_DF)
df = df.iloc[-WINDOW:]
# df = add_fractals(df)
# df = add_rsi(df)
max_period = 55
can_period = max_period // 3
# 58.056667    55.53666
period=55
period2=55
df = add_velcro_indicator(df)


# candle_max = df['high'].max()
# if candle_max > 0:
#     df['volume'] = df['volume'] / df['volume'].max() if df['volume'].max() > 0 else 0
#     df['close'] = df['close'] / candle_max
#     df['open'] = df['open'] / candle_max
#     df['low'] = df['low'] / candle_max
#     df['high'] = df['high'] / candle_max
#     df['middle'] = df['middle'] / candle_max
# # df = add_percent_zz190826(df)
# df = add_ultimate_oscillator(df, period // 3, period // 2, period)
# print(55 // 8)
print(df.tail(60))