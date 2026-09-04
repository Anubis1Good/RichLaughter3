from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *
from for_strategies.fix_params import *
from testing.test_constants import *
from utils.work_dfs.load_df import simple_load_df

# PATH_DF = '_data_for_tests\_before_opt\ALRS_5_1787155697.parquet'

df = simple_load_df(PATH_DF)
# df = df.iloc[-WINDOW:]
df = df.iloc[-60:]
# df = add_fractals(df)
# df = add_rsi(df)
max_period = 55
can_period = max_period // 3
# 58.056667    55.53666
p1=55
p2=55
p3=25
p1,p2=fix_two_periods_hm(p1,p2,max_period)
print(p1,p2,p3)
# p1,p2,p3=fix_three_periods_hm(p1,p2,p3,max_period)
# if p2 < p3:
#     p3 = p2
print(p1,p2,p3)
df = add_donchan_channel(df, p1)
df = add_assessment_motion_index(df, p2, p3)


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
print(df.tail(20))