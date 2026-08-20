import pandas as pd
import numpy as np

def add_vodka_channel(df:pd.DataFrame,period=20):
    '''add top_mean, bottom_mean, avarege_mean'''
    df['top_mean'] = df['high'].rolling(window=period).median()
    df['bottom_mean'] = df['low'].rolling(window=period).median()
    df['avarege_mean'] = (df['top_mean'] + df['bottom_mean']) / 2
    return df

def add_kusuruken_channel(df:pd.DataFrame, period=20,period2=40):
    """
    '''add "max_hb", "min_hb", "avarege","max_hb2", "min_hb2", "avarege2"'''
    
    :param df: DataFrame с колонками 'high', 'low'
    :param period: Период для расчета канала Дончиана (по умолчанию 20)
    :return: DataFrame с добавленными колонками
    """
    # Верхняя полоса (максимум за последние N периодов)
    df['max_hb'] = df['high'].rolling(window=period).max()
    df['max_hb2'] = df['high'].rolling(window=period2).max()
    
    # Нижняя полоса (минимум за последние N периодов)
    df['min_hb'] = df['low'].rolling(window=period).min()
    df['min_hb2'] = df['low'].rolling(window=period2).min()
    
    # Средняя линия
    df['avarege'] = (df['max_hb'] + df['min_hb']) / 2
    df['avarege2'] = (df['max_hb2'] + df['min_hb2']) / 2
    
    return df

# def add_average_fractals(df:pd.DataFrame, period=5):
#     """add 'ave_up', 'ave_down'"""
#     up_points = df[df['fractal_up']]
#     df['ave_up'] = up_points['high'].rolling(window=period).mean()
#     df['ave_up'] = df['ave_up'].ffill()
#     down_points = df[df['fractal_down']]
#     df['ave_down'] = down_points['low'].rolling(window=period).mean()
#     df['ave_down'] = df['ave_down'].ffill()
#     return df
def add_average_fractals(df: pd.DataFrame, period=30, period_fractal=5):
    """add 'ave_up', 'ave_down'"""
    df = df.copy()
    
    shift = (period_fractal - 1) // 2
    window = period - shift
    if window < 1:
        df['ave_up'] = np.nan
        df['ave_down'] = np.nan
        return df

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

def add_extremes_fractals(df:pd.DataFrame, period=5):
    """add 'ext_up', 'ext_down'"""
    up_points = df[df['fractal_up']]
    df['ext_up'] = up_points['high'].rolling(window=period).max()
    df['ext_up'] = df['ext_up'].ffill()
    down_points = df[df['fractal_down']]
    df['ext_down'] = down_points['low'].rolling(window=period).min()
    df['ext_down'] = df['ext_down'].ffill()
    return df

def add_velcro_indicator(df,period_check=10):
    '''add velcro'''
    df['delta_h'] = df['max_hb'] - df['high']
    df['delta_l'] = df['low'] - df['min_hb']
    df['lis'] = df['delta_l'].rolling(period_check).mean()
    df['his'] = df['delta_h'].rolling(period_check).mean()

    df['sis'] = df['lis'] + df['his']

    df['velcro'] = (df['lis'] / df['sis'])*100
    return df

def add_kvas_channel(df:pd.DataFrame,period=20):
    """add 'top_kvas','low_kvas'"""
    df['delta_p'] = (df['close'] - df['close'].shift(period))
    df['top_kvas'] = df['high'].rolling(period).max() + df['delta_p']
    df['low_kvas'] = df['low'].rolling(period).min() + df['delta_p']
    return df

#NEED EXPERIMENT
def add_kefir_channel(df:pd.DataFrame,period=20):
    """add 'top_kefir','low_kefir'"""
    df['delta_p'] = df['close'] - df['close'].shift(period)
    df['delta_t'] = df['delta_p'].shift(period).rolling(period).max()
    df['delta_l'] = df['delta_p'].shift(period).rolling(period).min()
    df['top_kefir'] = df['high'].rolling(period).max() + df['delta_t']
    df['low_kefir'] = df['low'].rolling(period).min() + df['delta_l']
    return df

def add_hl_stair_fast(df: pd.DataFrame, n=3, period=20):
    """ add 'stair'
    """
    high = df['high'].values
    low = df['low'].values

    # Предварительные расчеты
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n

    # Инициализация массивов
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.zeros(size)
    last_low = np.zeros(size)

    # Начальные значения
    last_high[0] = high[0]
    last_low[0] = low[0]

    # Основной цикл
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        h = high[i]
        l = low[i]

        if current_dir == 1:
            new_high = max(h, current_high)
            if l <= (new_high - th):
                current_dir = -1
                new_low = l
            else:
                new_low = current_low
        else:
            new_low = min(l, current_low)
            if h >= (new_low + th):
                current_dir = 1
                new_high = h
            else:
                new_high = current_high

        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low

    # Отмечаем точки разворота
    dir_changes = np.diff(last_dir, prepend=0) != 0
    df['stair'] = np.where(dir_changes, np.where(last_dir == -1, high, low), np.nan)
    
    # Заполняем значения вперед
    df['stair'] = df['stair'].ffill()
    return df

def add_pc_stair_fast(df: pd.DataFrame, n=3, period=20):
    """ add 'stair'
    'Mcfly'
    """
    # df = df.copy()
    # df = df.reset_index(drop=True)
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    
    # Предварительные расчеты
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n
    
    # Инициализация массивов состояний
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.empty(size)
    last_low = np.empty(size)
    
    # Начальные значения
    last_high[0] = prev_close[0]
    last_low[0] = prev_close[0]
    
    # Основной цикл (оптимизированный)
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        pc = prev_close[i]
        
        if current_dir == 1:
            new_high = max(pc, current_high)
            if pc <= (new_high - th):
                current_dir = -1
                new_low = pc
            else:
                new_low = current_low
        else:
            new_low = min(pc, current_low)
            if pc >= (new_low + th):
                current_dir = 1
                new_high = pc
            else:
                new_high = current_high
        
        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low
    
    # Построение финального индикатора
    dir_changes = np.where(np.diff(last_dir, prepend=last_dir[0]) != 0)[0]
    stair = np.full(size, np.nan)
    stair[dir_changes] = prev_close[dir_changes]
    
    df['stair'] = pd.Series(stair,df.index).ffill()
    return df

def add_integrity_index(df:pd.DataFrame,period:int=14):
    """add 'ii'"""
    df['spred'] = df['high'] - df['low']
    df['integrity'] = np.where(df['direction'] == 1, df['spred'],-df['spred'])
    df['ii'] = (df['integrity'].rolling(period).sum() / np.abs(df['integrity']).rolling(period).sum()) * 100
    df['ii'] = df['ii'].round(2)
    df = df.drop(['spred','integrity'],axis=1)
    return df

def add_cascade_channel(df: pd.DataFrame, n=3, period=20,period_smooth=100):
    """ add 'stair','top_line','bottom_line'
    Mcfly
    """
    df = df.copy()
    df = df.reset_index(drop=True)
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    
    # Предварительные расчеты
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n
    
    # Инициализация массивов состояний
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.empty(size)
    last_low = np.empty(size)
    
    # Начальные значения
    last_high[0] = prev_close[0]
    last_low[0] = prev_close[0]
    
    # Основной цикл (оптимизированный)
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        pc = prev_close[i]
        
        if current_dir == 1:
            new_high = max(pc, current_high)
            if pc <= (new_high - th):
                current_dir = -1
                new_low = pc
            else:
                new_low = current_low
        else:
            new_low = min(pc, current_low)
            if pc >= (new_low + th):
                current_dir = 1
                new_high = pc
            else:
                new_high = current_high
        
        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low
    
    # Построение финального индикатора
    dir_changes = np.where(np.diff(last_dir, prepend=last_dir[0]) != 0)[0]
    stair = np.full(size, np.nan)
    stair[dir_changes] = prev_close[dir_changes]
    
    df['stair'] = pd.Series(stair).ffill()
    df['top_line'] = (df['stair'] + threshold_break).rolling(period_smooth,1).median()
    df['bottom_line'] = (df['stair'] - threshold_break).rolling(period_smooth,1).median()
    
    return df

def add_static_channel(df:pd.DataFrame,period=60):
    """add 'center_line', 'top_line', 'bottom_line'"""
    df['center_line'] = df['close'].rolling(period,1).quantile(0.5)
    df['top_line'] = df['close'].rolling(period,1).quantile(0.9)
    df['bottom_line'] = df['close'].rolling(period,1).quantile(0.1)
    return df

#check thos
def add_assessment_motion_index(df:pd.DataFrame,period=100,period_filter=50):
    """add 'ami', 'ami_filter'"""
    df['ami'] = (((df['avarege'].diff().rolling(period,1).sum())/ np.abs(df['avarege'].diff()).rolling(period).sum())*100).round(2)
    df['ami_filter'] = df['ami'].rolling(period_filter).mean()
    return df

def add_hope_channel(df: pd.DataFrame, n=3, period=100,shift=10):
    """ add 'stair','top_line','bottom_line'
    Mcfly
    """
    df = df.copy()
    df = df.reset_index(drop=True)
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    
    # Предварительные расчеты
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    
    spread = high - low
    threshold_break = pd.Series(spread).rolling(period).mean().fillna(0).values * n
    
    # Инициализация массивов состояний
    size = len(df)
    last_dir = np.ones(size, dtype=np.int8)
    last_high = np.empty(size)
    last_low = np.empty(size)
    
    # Начальные значения
    last_high[0] = prev_close[0]
    last_low[0] = prev_close[0]
    
    # Основной цикл (оптимизированный)
    for i in range(1, size):
        current_dir = last_dir[i-1]
        current_high = last_high[i-1]
        current_low = last_low[i-1]
        th = threshold_break[i]
        pc = prev_close[i]
        
        if current_dir == 1:
            new_high = max(pc, current_high)
            if pc <= (new_high - th):
                current_dir = -1
                new_low = pc
            else:
                new_low = current_low
        else:
            new_low = min(pc, current_low)
            if pc >= (new_low + th):
                current_dir = 1
                new_high = pc
            else:
                new_high = current_high
        
        last_dir[i] = current_dir
        last_high[i] = new_high
        last_low[i] = new_low
    
    # Построение финального индикатора
    dir_changes = np.where(np.diff(last_dir, prepend=last_dir[0]) != 0)[0]
    stair = np.full(size, np.nan)
    stair[dir_changes] = prev_close[dir_changes]
    df['stair'] = pd.Series(stair).shift(shift)
    df['top_line'] = df['stair'] + threshold_break
    df['bottom_line'] = df['stair'] - threshold_break
    df['stair'] = df['stair'].ffill()
    df['top_line'] = df['top_line'].ffill()
    df['bottom_line'] = df['bottom_line'].ffill()
    return df

def add_delta_fractals(df: pd.DataFrame, period=1, period_fractals=5):
    """Оптимизированная версия с расчетом верхних и нижних фракталов"""
    
    # Создаем копии для безопасного изменения
    df = df.copy()
    
    # Обработка верхних фракталов
    up_mask = df['fractal_up']
    df['h_up'] = df.loc[up_mask, 'high'].reindex(df.index).ffill()
    
    up_points = df[up_mask].copy()
    up_deltas = (up_points['high'].diff() / up_points.index.to_series().diff()).rolling(period).mean()
    df['delta_up'] = up_deltas.reindex(df.index)
    
    # Кумулятивная сумма с reset по новым delta_up
    df['cum_temp_up'] = df['delta_up'].ffill()
    df['cum_temp_up'] = df.groupby(df['delta_up'].notna().cumsum())['cum_temp_up'].cumsum()
    df['fd_up'] = (df['h_up'] + df['cum_temp_up']).shift(period_fractals)
    
    # Обработка нижних фракталов
    down_mask = df['fractal_down']
    df['l_down'] = df.loc[down_mask, 'low'].reindex(df.index).ffill()
    
    down_points = df[down_mask].copy()
    down_deltas = (down_points['low'].diff() / down_points.index.to_series().diff()).rolling(period).mean()
    df['delta_down'] = down_deltas.reindex(df.index)
    
    # Кумулятивная сумма с reset по новым delta_down
    df['cum_temp_down'] = df['delta_down'].ffill()
    df['cum_temp_down'] = df.groupby(df['delta_down'].notna().cumsum())['cum_temp_down'].cumsum()
    df['fd_down'] = (df['l_down'] + df['cum_temp_down']).shift(period_fractals)
    
    # Удаляем промежуточные колонки
    cols_to_drop = ['h_up', 'l_down', 'delta_up', 'delta_down', 'cum_temp_up', 'cum_temp_down']
    return df.drop(columns=cols_to_drop)

# good indicator
def add_std_fractals_channel(df:pd.DataFrame, period=5,period_sma=10):
    """add 'std_up', 'std_down', 'sma'"""
    df['sma'] = df['middle'].rolling(period_sma).mean()
    up_points = df[df['fractal_up']]
    df['std_up'] = up_points['high'].rolling(window=period).std()
    df['std_up'] = df['std_up'].ffill() + df['sma']
    down_points = df[df['fractal_down']]
    df['std_down'] = down_points['low'].rolling(window=period).std()
    df['std_down'] = df['sma'] - df['std_down'].ffill() 
    return df

#good indicator
# def add_mean_on_fractals(df,period=5,kind='rsi'):
#     """add 'top_mean', bottom_mean'"""
#     ups = df[df['fractal_up']]
#     df['top_mean'] = ups[kind].rolling(period).mean()
#     df['top_mean'] = df['top_mean'].ffill()
#     downs = df[df['fractal_down']]
#     df['bottom_mean'] = downs[kind].rolling(period).mean()
#     df['bottom_mean'] = df['bottom_mean'].ffill()
#     return df

# def add_mean_on_fractals_(df, period=5, kind='rsi', max_period=55):
#     """
#     Использует last_confirmed_up_x/down_x для расчёта средних.
#     """
#     df = df.copy()
    
#     # Создаём словарь для быстрого доступа к значениям kind по x
#     x_to_kind = dict(zip(df['x'], df[kind]))
    
#     # Берём значения kind на моменте фрактала
#     df['top_val_at_fractal'] = df['last_confirmed_up_x'].map(x_to_kind)
#     df['bottom_val_at_fractal'] = df['last_confirmed_down_x'].map(x_to_kind)
    
#     # Rolling mean по последним period фракталам
#     df['top_mean'] = df['top_val_at_fractal'].rolling(window=period, min_periods=1).mean()
#     df['bottom_mean'] = df['bottom_val_at_fractal'].rolling(window=period, min_periods=1).mean()
    
#     # Убираем ffill, потому что он уже сделан в add_fractals с ограничением!
#     # (Или оставляем, но с лимитом)
#     df['top_mean'] = df['top_mean'].ffill(limit=max_period).round(2)
#     df['bottom_mean'] = df['bottom_mean'].ffill(limit=max_period).round(2)
    
#     df.drop(['top_val_at_fractal', 'bottom_val_at_fractal'], axis=1, inplace=True)
    
#     return df

def add_mean_on_fractals(df:pd.DataFrame, max_period=55, kind='rsi', period_fractal=5):
    """add 'top_mean', 'bottom_mean' \n
    Mcfly
    """
    shift = (period_fractal - 1) // 2
    window = max_period - shift
    
    # Если window < 1, создаём пустые колонки
    if window < 1:
        df['top_mean'] = np.nan
        df['bottom_mean'] = np.nan
        return df
    
    # Верхние фракталы
    ups = df[df['fractal_up']]
    df['top_mean'] = ups[kind]
    df['top_mean'] = df['top_mean'].shift(shift)
    df['top_mean'] = df['top_mean'].rolling(window=window, min_periods=1).mean().round(2)
    
    # Нижние фракталы
    downs = df[df['fractal_down']]
    df['bottom_mean'] = downs[kind]
    df['bottom_mean'] = df['bottom_mean'].shift(shift)
    df['bottom_mean'] = df['bottom_mean'].rolling(window=window, min_periods=1).mean().round(2)
    
    return df

# def add_mean_on_fractals(df, period=5, kind='rsi', max_window=55, shift=2):
#     """add 'top_mean', bottom_mean'"""
#     df['top_mean'] = np.nan
#     df['bottom_mean'] = np.nan
    
#     # start = df.index.values[0] + max_window
#     # end = df.index.values[-1]
#     start = df['x'].values[0] + max_window
#     end = df['x'].values[-1]
    
#     for i in range(start, end + 1):
#         # Верхние фракталы
#         df_slice = df.loc[i - max_window+shift+1:i - shift -1]
#         ups = df_slice[df_slice['fractal_up']]
#         values = ups[kind].values
        
#         if len(values) > 0:
#             if len(values) >= period:
#                 df.loc[i, 'top_mean'] = np.mean(values[-period:])
#             else:
#                 df.loc[i, 'top_mean'] = np.mean(values)
        
#         # Нижние фракталы
#         downs = df_slice[df_slice['fractal_down']]
#         values_down = downs[kind].values
        
#         if len(values_down) > 0:
#             if len(values_down) >= period:
#                 df.loc[i, 'bottom_mean'] = np.mean(values_down[-period:])
#             else:
#                 df.loc[i, 'bottom_mean'] = np.mean(values_down)
    
#     return df
#?good indicator
def add_diffmean_fractals_channel(df,period=2,kind='sma'):
    """add 'dmu', 'dmd'"""
    ups = df[df['fractal_up']]
    top_mean = ups[kind].rolling(period).mean()
    df['dmu'] = top_mean - ups['high']
    df['dmu'] = df['dmu'].ffill()
    df['dmu'] = df[kind] - df['dmu'] 
    downs = df[df['fractal_down']]
    bottom_mean = downs[kind].rolling(period).mean()
    df['dmd'] = bottom_mean - downs['low']
    df['dmd'] = df['dmd'].ffill()
    df['dmd'] = df[kind] - df['dmd'] 
    return df
#?good indicator
def add_sdiffmean_fractals_channel(df,period=2,kind='sma',period_smooth=20):
    """add 'sdmu', 'sdmd'"""
    df = add_diffmean_fractals_channel(df,period,kind)
    df['sdmu'] = df['dmu'].rolling(period_smooth).mean()
    df['sdmd'] = df['dmd'].rolling(period_smooth).mean()
    return df

#good indicator
# def add_ext_on_fractals(df,period=5,kind='rsi'):
#     """add 'top_ext', bottom_ext'"""
#     ups = df[df['fractal_up']]
#     df['top_ext'] = ups[kind].rolling(period).max()
#     df['top_ext'] = df['top_ext'].ffill()
#     downs = df[df['fractal_down']]
#     df['bottom_ext'] = downs[kind].rolling(period).min()
#     df['bottom_ext'] = df['bottom_ext'].ffill()
#     return df

def add_ext_on_fractals(df:pd.DataFrame, max_period=55, kind='rsi', period_fractal=5):
    """add 'top_ext', 'bottom_ext' \n
    Mcfly"""
    shift = (period_fractal - 1) // 2
    window = max_period - shift
    
    # Если window < 1, создаём пустые колонки
    if window < 1:
        df['top_ext'] = np.nan
        df['bottom_ext'] = np.nan
        return df
    
    # Верхние фракталы - максимум
    ups = df[df['fractal_up']]
    df['top_ext'] = ups[kind]
    df['top_ext'] = df['top_ext'].shift(shift)
    df['top_ext'] = df['top_ext'].rolling(window=window, min_periods=1).max()
    
    # Нижние фракталы - минимум
    downs = df[df['fractal_down']]
    df['bottom_ext'] = downs[kind]
    df['bottom_ext'] = df['bottom_ext'].shift(shift)
    df['bottom_ext'] = df['bottom_ext'].rolling(window=window, min_periods=1).min()
    
    return df

def add_smooth_channel(df:pd.DataFrame,period=20,smooth_features=('max_hb', 'min_hb', 'avarege'),variant_smooth='mean'):
    for sf in smooth_features:
        df[sf] = df[sf].rolling(period).agg([variant_smooth])
    return df

def add_plus_delta_fc(df:pd.DataFrame, period=1,period_fractal=5):
    """add 'pdf_up', 'pdf_down'
    \n plus delta fractal channel
    Mcfly
    """
    shift = (period_fractal - 1) // 2
    up_points = df[df['fractal_up']].copy()
    up_points['delta_high'] = up_points['high'].diff()
    up_points['dhm'] = up_points['delta_high'].rolling(period).mean()
    df['pdf_up'] = up_points['high'] + up_points['dhm']
    df['pdf_up'] = df['pdf_up'].ffill()
    df['pdf_up'] = df['pdf_up'].shift(shift)
    down_points = df[df['fractal_down']].copy()
    down_points['delta_low'] = down_points['low'].diff()
    down_points['dlm'] = down_points['delta_low'].rolling(period).mean()
    df['pdf_down'] = down_points['low'] + down_points['dlm']
    df['pdf_down'] = df['pdf_down'].ffill()
    df['pdf_down'] = df['pdf_down'].shift(shift)
    return df

def add_exp_pdfc(df:pd.DataFrame, period=1,period_fractal=5):
    """add 'pdf_up', 'pdf_down'
    \n exponential plus delta fractal channel
    Mcfly
    """
    shift = (period_fractal - 1) // 2
    up_points = df[df['fractal_up']].copy()
    up_points['delta_high'] = up_points['high'].diff()
    up_points['dhm'] = up_points['delta_high'].ewm(period).mean()
    df['pdf_up'] = up_points['high'] + up_points['dhm']
    df['pdf_up'] = df['pdf_up'].ffill()
    df['pdf_up'] = df['pdf_up'].shift(shift)
    down_points = df[df['fractal_down']].copy()
    down_points['delta_low'] = down_points['low'].diff()
    down_points['dlm'] = down_points['delta_low'].ewm(period).mean()
    df['pdf_down'] = down_points['low'] + down_points['dlm']
    df['pdf_down'] = df['pdf_down'].ffill()
    df['pdf_down'] = df['pdf_down'].shift(shift)
    return df

def add_stable_ma_direction(df:pd.DataFrame,period=10,kind:str='sma'):
    """add 'dir_ma'"""
    df['diff_ma'] = np.sign(df[kind].diff())
    df['dir_ma'] = df['diff_ma'].rolling(period).mean()
    return df

def add_quantile_params(df:pd.DataFrame,period:int=10,kind:str='rsi',quantile:float=0.1):
    """add 'top_q','bottom_q'"""
    roll = df[kind].rolling(period)
    df['top_q'] = roll.quantile(1-quantile)
    df['bottom_q'] = roll.quantile(quantile)
    return df

def add_bbi(df:pd.DataFrame,period=20,kind='close',multiplier=2):
    "add 'bbi' индекс перепроданности по типу RSI"
    df = df.copy()
    price = df[kind]
    df['sma'] = price.rolling(window=period).mean()
    
    # Вычисляем стандартное отклонение
    std_dev = price.rolling(window=period).std()
    
    # Вычисляем верхнюю и нижнюю полосы Боллинджера
    df['bbu'] = df['sma'] + (multiplier * std_dev)
    df['bbd'] = df['sma'] - (multiplier * std_dev)

    df['buff_bb'] = df['bbu'] - df['bbd']
    df['top_bb'] = df['bbu'] + df['buff_bb']
    df['bottom_bb'] = df['bbd'] - df['buff_bb']
    df['mult_bb'] = (df['top_bb']-df['bottom_bb']) / 100
    df['bbi'] = (df['close']-df['bottom_bb']) / df['mult_bb']
    return df

def add_benefit(df, all_starts, all_ends, id, period=60):
    """
    Максимально быстрая версия без создания промежуточных колонок.
    """
    # Конвертируем в numpy
    if not isinstance(all_starts, np.ndarray):
        all_starts = np.array(all_starts)
    if not isinstance(all_ends, np.ndarray):
        all_ends = np.array(all_ends)
    
    prices = df['close'].values
    n = len(df)
    
    # Создаем сигналы
    signals = np.full(n, np.nan)
    signals[~np.isnan(all_starts)] = 1
    signals[~np.isnan(all_ends)] = -1
    
    # Фильтруем чередование
    signal_idx = np.where(~np.isnan(signals))[0]
    
    if len(signal_idx) < 2:
        df[f'bl_{id}'] = 0
        df[f'bs_{id}'] = 0
        return df
    
    sig_values = signals[signal_idx]
    mask = np.concatenate([[True], sig_values[1:] != sig_values[:-1]])
    signal_idx = signal_idx[mask]
    sig_values = sig_values[mask]
    
    # Расчет изменений
    long_changes = np.zeros(n)
    short_changes = np.zeros(n)
    
    entries = signal_idx[::2]
    exits = signal_idx[1::2]
    min_len = min(len(entries), len(exits))
    
    if min_len > 0:
        entries = entries[:min_len]
        exits = exits[:min_len]
        entry_signals = sig_values[::2][:min_len]
        
        # LONG
        long_mask = entry_signals == 1
        if np.any(long_mask):
            le = entries[long_mask]
            lx = exits[long_mask]
            long_changes[lx] = prices[lx] - prices[le]
        
        # SHORT
        short_mask = entry_signals == -1
        if np.any(short_mask):
            se = entries[short_mask]
            sx = exits[short_mask]
            short_changes[sx] = prices[se] - prices[sx]
        
        # Незакрытые позиции
        if len(signal_idx) % 2 == 1:
            last_idx = signal_idx[-1]
            last_signal = sig_values[-1]
            if last_signal == 1:
                long_changes[-1] = prices[-1] - prices[last_idx]
            elif last_signal == -1:
                short_changes[-1] = prices[last_idx] - prices[-1]
    
    # Рассчитываем скользящее среднее
    df[f'bl_{id}'] = pd.Series(long_changes).rolling(period, min_periods=1).mean().fillna(0).values
    df[f'bs_{id}'] = pd.Series(short_changes).rolling(period, min_periods=1).mean().fillna(0).values
    
    return df

def get_all_enter_exit_DC(df, kind_top, kind_bottom, window=100):
    """
    Векторизованная версия с ограничением по окну.
    Использует расширяющееся окно (expanding) с ограничением.
    """
    n = len(df)
    all_starts = np.full(n, np.nan)
    all_ends = np.full(n, np.nan)
    
    # Предварительные вычисления для всего датафрейма
    high = df['high'].values
    low = df['low'].values
    top = df[kind_top].values
    bottom = df[kind_bottom].values
    
    # Маски для всех возможных точек
    start_mask = (high >= np.roll(top, 1)) & (np.roll(high, 1) < np.roll(top, 2))
    end_mask = (low <= np.roll(bottom, 1)) & (np.roll(low, 1) > np.roll(bottom, 2))
    
    # Сдвигаем маски, чтобы они соответствовали индексам
    start_mask = np.roll(start_mask, -1)
    end_mask = np.roll(end_mask, -1)
    start_mask[:2] = False
    end_mask[:2] = False
    
    # Для каждой точки проверяем, есть ли сигнал в окне
    for i in range(n):
        start_idx = max(0, i - window)
        
        # Проверяем, есть ли точка входа в окне
        if np.any(start_mask[start_idx:i+1]):
            # Берем последний сигнал в окне
            last_start_idx = np.where(start_mask[start_idx:i+1])[0][-1] + start_idx
            all_starts[i] = top[last_start_idx]
        
        if np.any(end_mask[start_idx:i+1]):
            last_end_idx = np.where(end_mask[start_idx:i+1])[0][-1] + start_idx
            all_ends[i] = bottom[last_end_idx]
    
    return all_starts, all_ends

def get_all_enter_exit_DC_(df, kind_top, kind_bottom):
    """all_starts,all_ends"""
    # 1. Находим ВСЕ возможные точки входа и выхода (как в оригинале)
    all_starts = np.where(
        (df['high'] >= df[kind_top].shift(1)) & 
        (df['high'].shift(1) < df[kind_top].shift(2)),
        df[kind_top].shift(1), 
        np.nan
    )
    
    all_ends = np.where(
        (df['low'] <= df[kind_bottom].shift(1)) & 
        (df['low'].shift(1) > df[kind_bottom].shift(2)),
        df[kind_bottom].shift(1), 
        np.nan
    )
    return all_starts,all_ends

def get_all_lup(df,kind_top,kind_bottom):
    all_starts = np.where((df['high'].shift(1) >= df[kind_top].shift(1))&(df['high'] < df[kind_top]), df['high'], np.nan)
    all_ends = np.where((df['low'].shift(1) <= df[kind_bottom].shift(1))&(df['low'] > df[kind_bottom]), df['low'], np.nan)
    return all_starts,all_ends

def add_simple_dynamics_ma(df: pd.DataFrame, period: int = 20, 
                           kind: str = 'sma', divider_period: int = 1,
                           epsilon: float = 1e-10) -> pd.DataFrame:
    values = df[kind].values
    n = len(values)
    
    sdiff = np.zeros(n)
    if n > 1:
        diff = values[1:] - values[:-1]
        sdiff[1:] = np.where(diff > epsilon, 1, 
                            np.where(diff < -epsilon, -1, 0))
    
    window = period // divider_period
    cumsum = np.concatenate([[0], np.cumsum(sdiff)])
    sdm = np.full(n, -1.0)
    if n >= window:
        sdm[window-1:] = (cumsum[window:] - cumsum[:-window]) / window
    
    df['sdm'] = sdm
    return df