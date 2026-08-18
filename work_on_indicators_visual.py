from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *

from utils.work_dfs.load_df import simple_load_df
from utils.drawing.chart import draw_bars_chart,draw_bars_chart_wo_vol
import matplotlib.pyplot as plt

filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'

df = simple_load_df(filepath)
df = df.iloc[-300:]

df = add_zigzag180826(df,period=30)
df = add_shift_zz_peaks(df)
df['zp_s'] = df['zp_s'].ffill()
print(df.tail(20))
fig = draw_bars_chart_wo_vol(df)
plt.plot(df['zigzag'])
plt.plot(df['zp_s'])
plt.show()