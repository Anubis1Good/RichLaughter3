from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *
from for_strategies.fix_params import *
from utils.work_dfs.load_df import simple_load_df
from utils.drawing.chart import draw_bars_chart,draw_bars_chart_wo_vol
from utils.drawing.indicators import draw_wzp
import matplotlib.pyplot as plt
from testing.test_constants import *
# PATH_DF = '_data_for_tests\_before_opt\ALRS_5_1787155697.parquet'

df = simple_load_df(PATH_DF)
# df = df.iloc[-60:]
period=10
multiplier=3

# p1,p2 = fix_two_periods_hm(55,55,55)
# p1,p2 = 31,31
# print(p1,p2)
df = add_donchan_channel(df)
df = add_velcro_indicator(df)
# df = add_quantile_params(df, p2)
# df = add_ext_params(df, p2)



# df['stair_pc'] = df['stair']
# df = add_hl_stair_fast(df)

print(df.tail(20))
# fig = draw_bars_chart_wo_vol(df)

plt.plot(df['velcro'])
# plt.plot(df['stairh'])
# plt.plot(df['stair_pc_windowed'],color='blue')
# plt.plot(df['top_ext'],color='green')
# plt.plot(df['bottom_ext'],color='black')
# draw_wzp(df)
plt.show()