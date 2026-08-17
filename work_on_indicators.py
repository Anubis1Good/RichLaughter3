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
# df = add_rsi(df)

# 58.056667    55.53666
def add_average_fractals(df: pd.DataFrame, period=30, period_fractal=5):
    """add 'ave_up', 'ave_down'"""
    df = df.copy()
    
    shift = (period_fractal - 1) // 2
    window = period - shift

    # Верхние фракталы
    up_points = df[df['fractal_up']]
    df['ave_up'] = up_points['high']
    df['ave_up'] = df['ave_up'].shift(shift)
    df['ave_up'] = df['ave_up'].rolling(window, min_periods=1).mean().round(2)

    # Нижние фракталы
    down_points = df[df['fractal_down']]
    df['ave_down'] = down_points['low']
    df['ave_down'] = df['ave_down'].shift(shift)
    df['ave_down'] = df['ave_down'].rolling(window, min_periods=1).mean().round(2)
    
    return df

df = add_average_fractals(df)
# print(df[['x', 'top_mean_list']].head(20))
# print(df[['x', 'bottom_mean_list']].head(20))

print(df.tail(60))