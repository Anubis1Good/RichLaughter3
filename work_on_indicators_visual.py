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

filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'

df = simple_load_df(filepath)
df = df.iloc[-300:]


df = add_window_zigzag190826(df)
print(df.tail(20))
fig = draw_bars_chart_wo_vol(df)

# plt.plot(df['wzp1'])
# plt.plot(df['wzp2'])
# plt.plot(df['wzp3'])
# plt.plot(df['wzp4'])
draw_wzp(df)
plt.show()