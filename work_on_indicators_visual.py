from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *

from utils.work_dfs.load_df import simple_load_df
from utils.drawing.chart import draw_bars_chart,draw_bars_chart_wo_vol
from utils.drawing.indicators import draw_wzp
import matplotlib.pyplot as plt
from testing.test_constants import *
# PATH_DF = '_data_for_tests\_before_opt\ALRS_5_1787155697.parquet'

df = simple_load_df(PATH_DF)
# df = df.iloc[-300:]
period=10
multiplier=3


df = add_supertrend(df)


# df['stair_pc'] = df['stair']
# df = add_hl_stair_fast(df)

print(df.tail(20))
fig = draw_bars_chart_wo_vol(df)

# plt.plot(df['stairl'])
# plt.plot(df['stairh'])
# plt.plot(df['stair_pc_windowed'],color='blue')
# plt.plot(df['stair'],color='green')
plt.plot(df['supertrend'],color='black')
# draw_wzp(df)
plt.show()