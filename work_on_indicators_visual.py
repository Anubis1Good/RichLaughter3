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
max_period = 55

p1=10
p2=10
p3=25
p1,p2=fix_two_periods_hm(p1,p2,max_period)
print(p1,p2,p3)
p1,p2,p3=fix_three_periods_hm(p1,p2,p3,max_period)
if p2 < p3:
    p3 = p2
print(p1,p2,p3)
df = add_donchan_channel(df, p1)
df = add_assessment_motion_index(df, p2, p3)
# df = add_quantile_params(df, p2)
# df = add_ext_params(df, p2)



# df['stair_pc'] = df['stair']
# df = add_hl_stair_fast(df)

print(df.tail(20))
# fig = draw_bars_chart_wo_vol(df)

plt.plot(df['ami'])
plt.plot(df['ami_filter'])
# plt.plot(df['stair_pc_windowed'],color='blue')
# plt.plot(df['top_ext'],color='green')
# plt.plot(df['bottom_ext'],color='black')
# draw_wzp(df)
plt.show()