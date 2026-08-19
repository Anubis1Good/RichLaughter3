import pandas as pd
import numpy as np
from scipy.stats import linregress

def add_donchan_channel(df:pd.DataFrame, period=20):
    """
    '''add "max_hb", "min_hb", "avarege"'''
    
    :param df: DataFrame с колонками 'high', 'low'
    :param period: Период для расчета канала Дончиана (по умолчанию 20)
    :return: DataFrame с добавленными колонками
    """
    # Верхняя полоса (максимум за последние N периодов)
    df['max_hb'] = df['high'].rolling(window=period).max()
    
    # Нижняя полоса (минимум за последние N периодов)
    df['min_hb'] = df['low'].rolling(window=period).min()
    
    # Средняя линия
    df['avarege'] = (df['max_hb'] + df['min_hb']) / 2
    
    return df

def add_sma(df: pd.DataFrame, period=20, kind='close'):
    """
    Добавляет колонку 'sma' в DataFrame.
    Оптимизированная версия с использованием встроенных функций Pandas.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для SMA (по умолчанию 20)
    :param kind: Тип цены для расчета SMA ('middle', 'high', 'low', 'close')
    :return: DataFrame с добавленной колонкой 'sma'
    """
    # Выбираем колонку для расчета SMA
    if kind == 'middle':
        price = (df['high'] + df['low']) / 2
    elif kind == 'high':
        price = df['high']
    elif kind == 'low':
        price = df['low']
    elif kind == 'close':
        price = df['close']
    else:
        raise ValueError("Неподдерживаемый тип цены. Используйте 'middle', 'high', 'low' или 'close'.")
    
    # Вычисляем SMA с использованием встроенной функции rolling
    df['sma'] = price.rolling(window=period).mean()
    
    return df

def add_bollinger(df: pd.DataFrame, period=20, kind='close', multiplier=2):
    """
    Добавляет колонки 'bbu', 'bbd', 'sma' в DataFrame.
    Оптимизированная версия с использованием встроенных функций Pandas.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для расчета полос Боллинджера (по умолчанию 20)
    :param kind: Тип цены для расчета ('middle', 'high', 'low', 'close')
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками 'bbu', 'bbd', 'sma'
    """
    # Выбираем колонку для расчета
    if kind == 'middle':
        price = (df['high'] + df['low']) / 2
    elif kind == 'high':
        price = df['high']
    elif kind == 'low':
        price = df['low']
    elif kind == 'close':
        price = df['close']
    else:
        raise ValueError("Неподдерживаемый тип цены. Используйте 'middle', 'high', 'low' или 'close'.")
    
    # Вычисляем SMA
    df['sma'] = price.rolling(window=period).mean().round(2)
    
    # Вычисляем стандартное отклонение
    std_dev = price.rolling(window=period).std()
    
    # Вычисляем верхнюю и нижнюю полосы Боллинджера
    df['bbu'] = (df['sma'] + (multiplier * std_dev)).round(2)
    df['bbd'] = (df['sma'] - (multiplier * std_dev)).round(2)
    
    return df

def add_fractals(df: pd.DataFrame, period=5, max_period=55):
    """
    Добавляет фракталы Билла Вильямса.
    """
    shift = (period - 1) // 2
    
    # Расчёт фракталов
    fractal_up_condition = True
    for i in range(1, shift + 1):
        fractal_up_condition &= (df['high'] > df['high'].shift(i))
        fractal_up_condition &= (df['high'] > df['high'].shift(-i))
    
    fractal_down_condition = True
    for i in range(1, shift + 1):
        fractal_down_condition &= (df['low'] < df['low'].shift(i))
        fractal_down_condition &= (df['low'] < df['low'].shift(-i))
    
    df['fractal_up'] = fractal_up_condition
    df['fractal_down'] = fractal_down_condition
    
    return df

def add_rsi(df:pd.DataFrame, period=14,kind='close'):
    """
    add 'rsi'\n
    Вычисляет RSI для DataFrame с данными о ценах.
    
    :param data: DataFrame с колонкой 'Close' (цены закрытия)
    :param period: Период RSI (по умолчанию 14)
    :return: DataFrame с добавленной колонкой 'RSI'
    """
    # Вычисляем изменение цены
    delta = df[kind].diff()
    
    # Разделяем на рост и падение
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Вычисляем относительную силу (RS)
    rs = gain / loss
    
    # Вычисляем RSI
    df['rsi'] = (100 - (100 / (1 + rs))).round(2)
    
    return df

def add_rsi_tw(df:pd.DataFrame, period=14, kind='close'):
    """
    Добавляет колонку 'rsi_tw' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период RSI (по умолчанию 14)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'RSI'
    """
    # Вычисляем изменение цены
    delta = df[kind].diff()
    
    # Разделяем на рост и падение
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Вычисляем экспоненциальное скользящее среднее (EMA) для роста и падения
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    # Вычисляем относительную силу (RS)
    rs = avg_gain / avg_loss
    
    # Вычисляем RSI
    df['rsi_tw'] = (100 - (100 / (1 + rs))).round(2)
    
    return df


def add_ema(df:pd.DataFrame, period=20, kind='close'):
    """
    Вычисляет EMA для DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой цен (по умолчанию 'close')
    :param period: Период EMA (по умолчанию 20)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'ema'
    """
    alpha = 2 / (period + 1)
    
    # Используем expanding() и apply() для векторизованного расчета EMA
    sma = df[kind].rolling(window=period, min_periods=period).mean()
    ema = df[kind].ewm(alpha=alpha, adjust=False).mean()
    
    # Комбинируем SMA (первые period-1 значений) и EMA (остальные значения)
    df['ema'] = sma.where(sma.notna(), ema).round(2)
    
    return df


def add_stochastic(df:pd.DataFrame, k_period=14, d_period=3,kind='close'):
    """add 'lowest_so','highest_so','%k','%d' """
    df['lowest_so'] = df[kind].rolling(window=k_period).min()
    df['highest_so'] = df[kind].rolling(window=k_period).max()
    df['%k'] = (100 * ((df[kind] - df['lowest_so']) / (df['highest_so'] - df['lowest_so']))).round(2)
    df['%d'] = df['%k'].rolling(window=d_period).mean().round(2)
    return df

def add_atr(df:pd.DataFrame, period=5,kind='close'):
    '''"atr"'''
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = np.abs(df['high'] - df[kind].shift(1))
    df['low_close'] = np.abs(df['low'] - df[kind].shift(1))
    df['tr'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=period).mean()
    return df

def add_macd(data:pd.DataFrame, short_window=12, long_window=26, signal_window=9):
    """add 'ema_1','ema_2','macd','signal_line'"""
    data['ema_1'] = data['close'].ewm(span=short_window, adjust=False).mean()
    data['ema_2'] = data['close'].ewm(span=long_window, adjust=False).mean()
    data['macd'] = data['ema_1'] - data['ema_2']
    data['signal_line'] = data['macd'].ewm(span=signal_window, adjust=False).mean()
    return data

def add_adx(df:pd.DataFrame,adx_period=14):
    """
    'adx'
    Расчет индикатора ADX (Average Directional Index).
    :param df: DataFrame с данными
    :return: DataFrame с добавленным столбцом ADX
    """
    # Расчет True Range (TR)
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )

    # Расчет Positive Directional Movement (+DM) и Negative Directional Movement (-DM)
    df['plus_dm'] = np.where(
        (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
        np.maximum(df['high'] - df['high'].shift(1), 0),
        0
    )
    df['minus_dm'] = np.where(
        (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
        np.maximum(df['low'].shift(1) - df['low'], 0),
        0
    )

    # Сглаживание TR, +DM, -DM
    df['tr_smooth'] = df['tr'].rolling(window=adx_period, min_periods=adx_period).sum()
    df['plus_dm_smooth'] = df['plus_dm'].rolling(window=adx_period, min_periods=adx_period).sum()
    df['minus_dm_smooth'] = df['minus_dm'].rolling(window=adx_period, min_periods=adx_period).sum()

    # Расчет +DI и -DI
    df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
    df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100

    # Расчет ADX
    df['dx'] = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
    df['adx'] = df['dx'].rolling(window=adx_period, min_periods=adx_period).mean().round(2)
    cols_to_drop = ['tr', 'plus_dm', 'minus_dm', 'tr_smooth', 
                    'plus_dm_smooth', 'minus_dm_smooth', 
                    'plus_di', 'minus_di', 'dx']
    df.drop(columns=cols_to_drop, inplace=True)
    return df

def add_kama(df:pd.DataFrame, period=30,fast_ema=2,slow_ema=30):
    """
    Расчет индикатора KAMA (Kaufman Adaptive Moving Average).
    :param df: DataFrame с данными
    :param period: Период для расчета KAMA
    :return: DataFrame с добавленным столбцом KAMA
    """
    change = abs(df['close'] - df['close'].shift(period))
    volatility = df['close'].diff().abs().rolling(window=period).sum()
    efficiency_ratio = change / volatility

    fast_sc = 2 / (fast_ema + 1)
    slow_sc = 2 / (slow_ema + 1)
    smooth_constant = (efficiency_ratio * (fast_sc - slow_sc) + slow_sc) ** 2

    df[f'kama_{period}'] = 0.0
    for i in range(period, len(df)):
        df.loc[df.index[i], f'kama_{period}'] = (
            df.loc[df.index[i - 1], f'kama_{period}'] +
            smooth_constant[i] * (df.loc[df.index[i], 'close'] - df.loc[df.index[i - 1], f'kama_{period}'])
        )
    return df

def add_chop(df:pd.DataFrame,chop_period=14):
    """
    'chop'
    Расчет индикатора CHOP (Choppiness Index).
    :param df: DataFrame с данными
    :return: DataFrame с добавленным столбцом CHOP
    """
    # Расчет True Range (TR)
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )

    # Сумма TR за период
    df['tr_sum'] = df['tr'].rolling(window=chop_period).sum()

    # Максимальная и минимальная цена за период
    df['high_max'] = df['high'].rolling(window=chop_period).max()
    df['low_min'] = df['low'].rolling(window=chop_period).min()

    # Расчет CHOP
    df['chop'] = 100 * np.log10(df['tr_sum'] / (df['high_max'] - df['low_min'])) / np.log10(chop_period)
    return df

def add_cci(df:pd.DataFrame, period=20, kind='close'):
    """
    Добавляет колонку 'cci' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период CCI (по умолчанию 20)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'CCI'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low'] + df[kind]) / 3
    
    # Вычисляем скользящее среднее типичной цены (SMA)
    sma = typical_price.rolling(window=period).mean()
    
    # Вычисляем среднее отклонение (Mean Deviation)
    mean_deviation = typical_price.rolling(window=period).apply(
        lambda x: np.abs(x - x.mean()).mean(), raw=True
    )
    
    # Вычисляем CCI
    df['cci'] = (typical_price - sma) / (0.015 * mean_deviation)
    df['cci'] = df['cci'].round(2)

    return df

def add_williams_r(df:pd.DataFrame, period=14, kind='close'):
    """
    Добавляет колонку 'williams_r' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонками 'high', 'low' и 'close'
    :param period: Период Williams %R (по умолчанию 14)
    :param kind: Название колонки с ценами закрытия (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'williams_r'
    """
    # Вычисляем максимум и минимум за период
    highest_high = df['high'].rolling(window=period).max()
    lowest_low = df['low'].rolling(window=period).min()
    
    # Вычисляем Williams %R
    df['williams_r'] = -100 * (highest_high - df[kind]) / (highest_high - lowest_low)
    df['williams_r'] = df['williams_r'].round(2)
    
    return df

def add_mfi(df:pd.DataFrame, period=14):
    """
    Добавляет колонку 'mfi' в DataFrame с данными о ценах и объемах.
    
    :param df: DataFrame с колонками 'high', 'low', 'close' и 'volume'
    :param period: Период MFI (по умолчанию 14)
    :return: DataFrame с добавленной колонкой 'MFI'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Вычисляем денежный поток (Money Flow)
    money_flow = typical_price * df['volume']
    
    # Определяем положительный и отрицательный денежный поток
    positive_flow = (typical_price > typical_price.shift(1)) * money_flow
    negative_flow = (typical_price < typical_price.shift(1)) * money_flow
    
    # Вычисляем сумму положительного и отрицательного денежного потока за период
    positive_flow_sum = positive_flow.rolling(window=period).sum()
    negative_flow_sum = negative_flow.rolling(window=period).sum()
    
    # Вычисляем Money Flow Ratio (MFR)
    money_flow_ratio = positive_flow_sum / negative_flow_sum
    
    # Вычисляем MFI
    df['mfi'] = 100 - (100 / (1 + money_flow_ratio))
    df['mfi'] = df['mfi'].round(2)
    return df

def add_awesome_oscillator(df:pd.DataFrame, short_period=5, long_period=34):
    """
    Добавляет колонку 'ao' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param short_period: Период короткой скользящей средней (по умолчанию 5)
    :param long_period: Период длинной скользящей средней (по умолчанию 34)
    :return: DataFrame с добавленной колонкой 'ao'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low']) / 2
    
    # Вычисляем короткую и длинную скользящие средние (SMA)
    sma_short = typical_price.rolling(window=short_period).mean()
    sma_long = typical_price.rolling(window=long_period).mean()
    
    # Вычисляем Awesome Oscillator (AO)
    df['ao'] = sma_short - sma_long
        # Вычисляем Awesome Oscillator (AO)
    # ao = sma_short - sma_long
    
    # # Делим AO на цену закрытия
    # ao_relative_to_close = ao / df['close']
    
    # df['ao'] = ao_relative_to_close
    
    return df

def add_roc(df:pd.DataFrame, period=12, kind='close'):
    """
    Добавляет колонку 'roc' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период ROC (по умолчанию 12)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'ROC'
    """
    # Вычисляем ROC
    df['roc'] = ((df[kind] - df[kind].shift(period)) / df[kind].shift(period)) * 100
    
    return df

def add_ultimate_oscillator(df:pd.DataFrame, short_period=7, medium_period=14, long_period=28):
    """
    Добавляет колонку 'ultimate_oscillator' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param short_period: Короткий период (по умолчанию 7)
    :param medium_period: Средний период (по умолчанию 14)
    :param long_period: Длинный период (по умолчанию 28)
    :return: DataFrame с добавленной колонкой 'ultimate_oscillator'
    """
    # Вычисляем типичную цену (Typical Price)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Определяем давление покупок и продаж
    buying_pressure = typical_price - df[['low', 'close']].min(axis=1)
    true_range = df[['high', 'close']].max(axis=1) - df[['low', 'close']].min(axis=1)
    
    # Вычисляем средние значения для каждого периода
    avg_buying_pressure_short = buying_pressure.rolling(window=short_period).sum()
    avg_true_range_short = true_range.rolling(window=short_period).sum()
    
    avg_buying_pressure_medium = buying_pressure.rolling(window=medium_period).sum()
    avg_true_range_medium = true_range.rolling(window=medium_period).sum()
    
    avg_buying_pressure_long = buying_pressure.rolling(window=long_period).sum()
    avg_true_range_long = true_range.rolling(window=long_period).sum()
    
    # Вычисляем компоненты осциллятора
    short_component = avg_buying_pressure_short / avg_true_range_short
    medium_component = avg_buying_pressure_medium / avg_true_range_medium
    long_component = avg_buying_pressure_long / avg_true_range_long
    
    # Вычисляем Ultimate Oscillator
    df['ultimate_oscillator'] = (4 * short_component + 2 * medium_component + long_component) / 7 * 100
    df['ultimate_oscillator'] = df['ultimate_oscillator'].round(2)

    return df

def add_cmo(df:pd.DataFrame, period=14, kind='close'):
    """
    Добавляет колонку 'cmo' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close' (цены закрытия)
    :param period: Период CMO (по умолчанию 14)
    :param kind: Название колонки с ценами (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой 'CMO'
    """
    # Вычисляем изменение цены
    delta = df[kind].diff()
    
    # Разделяем на рост и падение
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Вычисляем сумму роста и падения за период
    sum_gain = gain.rolling(window=period).sum()
    sum_loss = loss.rolling(window=period).sum()
    
    # Вычисляем CMO
    df['cmo'] = ((sum_gain - sum_loss) / (sum_gain + sum_loss)) * 100
    df['cmo'] = df['cmo'].round(2)
    return df


def add_keltner_channel(df:pd.DataFrame, period=20, multiplier=2):
    """
    Добавляет колонки 'keltner_upper', 'keltner_middle', 'keltner_lower' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для EMA и ATR (по умолчанию 20)
    :param multiplier: Множитель для ATR (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    # Вычисляем EMA (центральная линия)
    df['keltner_middle'] = df['close'].ewm(span=period, adjust=False).mean()
    
    # Вычисляем ATR (средний истинный диапазон)
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    # Вычисляем верхнюю и нижнюю полосы
    df['keltner_upper'] = df['keltner_middle'] + (multiplier * atr)
    df['keltner_lower'] = df['keltner_middle'] - (multiplier * atr)
    
    return df
# Слишком большой канал
def add_ma_envelope(df:pd.DataFrame, period=20, deviation=0.05):
    """
    Добавляет колонки 'envelope_upper', 'envelope_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для SMA (по умолчанию 20)
    :param deviation: Процент отклонения (по умолчанию 0.05)
    :return: DataFrame с добавленными колонками
    """
    df['sma'] = df['close'].rolling(window=period).mean()
    df['envelope_upper'] = df['sma'] * (1 + deviation)
    df['envelope_lower'] = df['sma'] * (1 - deviation)
    return df

def add_std_dev_channel(df:pd.DataFrame, period=20, multiplier=2):
    """
    Добавляет колонки 'std_upper', 'std_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для SMA и стандартного отклонения (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    df['sma'] = df['close'].rolling(window=period).mean()
    std_dev = df['close'].rolling(window=period).std()
    df['std_upper'] = df['sma'] + (multiplier * std_dev)
    df['std_lower'] = df['sma'] - (multiplier * std_dev)
    return df




def add_linear_regression_channel(df:pd.DataFrame, period=20, multiplier=2):
    """
    Добавляет колонки 'regression_upper', 'regression_lower','regression_middle' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для линейной регрессии (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    def calculate_regression(values):
        x = range(len(values))  # Создаем массив индексов
        slope, intercept, _, _, _ = linregress(x, values)
        return slope * x[-1] + intercept  # Возвращаем значение на последней точке
    
    # Применяем линейную регрессию к скользящему окну
    df['regression_middle'] = df['close'].rolling(window=period).apply(calculate_regression, raw=True)
    
    # Вычисляем стандартное отклонение
    std_dev = df['close'].rolling(window=period).std()
    
    # Вычисляем верхнюю и нижнюю полосы
    df['regression_upper'] = df['regression_middle'] + (multiplier * std_dev)
    df['regression_lower'] = df['regression_middle'] - (multiplier * std_dev)
    
    return df

def add_lrchl(df:pd.DataFrame, period=20):
    """
    Добавляет колонки 'regression_upper', 'regression_lower' в DataFrame.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для линейной регрессии (по умолчанию 20)
    :param multiplier: Множитель для стандартного отклонения (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    def calculate_regression(values):
        x = range(len(values))  # Создаем массив индексов
        slope, intercept, _, _, _ = linregress(x, values)
        return slope * x[-1] + intercept  # Возвращаем значение на последней точке
    
    # Применяем линейную регрессию к скользящему окну
    df['regression_upper'] = df['high'].rolling(window=period).apply(calculate_regression, raw=True)
    df['regression_lower'] = df['low'].rolling(window=period).apply(calculate_regression, raw=True)

    
    return df

def add_atr_channel(df:pd.DataFrame, period=20, multiplier=2):
    """
    Добавляет колонки 'atr_upper', 'atr_lower' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param period: Период для ATR (по умолчанию 20)
    :param multiplier: Множитель для ATR (по умолчанию 2)
    :return: DataFrame с добавленными колонками
    """
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=period).mean()
    
    df['atr_upper'] = df['close'] + (multiplier * atr)
    df['atr_lower'] = df['close'] - (multiplier * atr)
    return df

def add_parabolic_sar(df:pd.DataFrame, acceleration=0.02, maximum=0.2):
    """
    Добавляет колонку 'parabolic_sar' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low'
    :param acceleration: Начальное ускорение (по умолчанию 0.02)
    :param maximum: Максимальное ускорение (по умолчанию 0.2)
    :return: DataFrame с добавленной колонкой
    """
    sar = []
    trend = 1  # 1 для восходящего тренда, -1 для нисходящего
    ep = df['high'].iloc[0]  # Экстремальная точка
    af = acceleration  # Фактор ускорения
    
    for i in range(len(df)):
        if i == 0:
            sar.append(df['low'].iloc[0])
            continue
        
        if trend == 1:
            sar.append(sar[-1] + af * (ep - sar[-1]))
        else:
            sar.append(sar[-1] + af * (ep - sar[-1]))
        
        if trend == 1:
            if df['high'].iloc[i] > ep:
                ep = df['high'].iloc[i]
                af = min(af + acceleration, maximum)
            if df['low'].iloc[i] < sar[-1]:
                trend = -1
                sar[-1] = ep
                ep = df['low'].iloc[i]
                af = acceleration
        else:
            if df['low'].iloc[i] < ep:
                ep = df['low'].iloc[i]
                af = min(af + acceleration, maximum)
            if df['high'].iloc[i] > sar[-1]:
                trend = 1
                sar[-1] = ep
                ep = df['high'].iloc[i]
                af = acceleration
    
    df['parabolic_sar'] = sar
    return df

def add_volume_profile(df:pd.DataFrame, period=14):
    """
    Добавляет Volume Profile в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low', 'close', 'volume'
    :param period: Период для расчета Volume Profile (по умолчанию 14)
    :return: DataFrame с добавленными колонками 'poc', 'value_area_high', 'value_area_low'
    """
    # Создаем пустые колонки для результатов
    df['poc'] = np.nan
    df['value_area_high'] = np.nan
    df['value_area_low'] = np.nan
    
    for i in range(period, len(df)):
        # Выбираем данные за последние `period` дней
        window = df.iloc[i-period:i]
        
        # Создаем гистограмму объема по ценам
        price_bins = np.linspace(window['low'].min(), window['high'].max(), num=100)
        volume_profile = np.zeros_like(price_bins)
        
        for j in range(len(window)):
            low = window.iloc[j]['low']
            high = window.iloc[j]['high']
            close = window.iloc[j]['close']
            volume = window.iloc[j]['volume']
            
            # Распределяем объем по ценам
            mask = (price_bins >= low) & (price_bins <= high)
            volume_profile[mask] += volume
        
        # Находим POC (цена с максимальным объемом)
        poc_index = np.argmax(volume_profile)
        poc = price_bins[poc_index]
        
        # Находим Value Area (70% объема)
        total_volume = np.sum(volume_profile)
        sorted_volume_indices = np.argsort(volume_profile)[::-1]
        cumulative_volume = 0
        value_area_indices = []
        
        for idx in sorted_volume_indices:
            cumulative_volume += volume_profile[idx]
            value_area_indices.append(idx)
            if cumulative_volume >= 0.7 * total_volume:
                break
        
        value_area_prices = price_bins[value_area_indices]
        value_area_high = np.max(value_area_prices)
        value_area_low = np.min(value_area_prices)
        
        # Записываем результаты
        df.at[df.index[i], 'poc'] = poc
        df.at[df.index[i], 'value_area_high'] = value_area_high
        df.at[df.index[i], 'value_area_low'] = value_area_low
    
    return df

def add_rvi(df:pd.DataFrame, period=14):
    """
    Добавляет колонку 'rvi' в DataFrame с данными о ценах.
    
    :param df: DataFrame с колонкой 'close'
    :param period: Период для RVI (по умолчанию 14)
    :return: DataFrame с добавленной колонкой 'RVI'
    """
    # Вычисляем стандартное отклонение цен закрытия
    std_dev = df['close'].rolling(window=period).std()
    
    # Сглаживаем стандартное отклонение с помощью EMA
    smoothed_std_dev = std_dev.ewm(span=period, adjust=False).mean()
    
    # Вычисляем среднее значение сглаженного стандартного отклонения
    mean_smoothed_std_dev = smoothed_std_dev.rolling(window=period).mean()
    
    # Вычисляем RVI
    df['rvi'] = (smoothed_std_dev / mean_smoothed_std_dev) * 100
    
    return df

def add_pivot_points_by_bars(df:pd.DataFrame, bars=5):
    """
    Добавляет Pivot Points, которые визуально растягиваются на весь период действия.
    Уровни выглядят как плоские линии, а не "сдвигаются" к началу группы.
    
    :param df: DataFrame с колонками 'high', 'low', 'close'
    :param bars: Количество свечей в группе (5, 60 и т.д.)
    :return: DataFrame с добавленными PP, R1, R2, S1, S2
    """
    # Сбрасываем индекс, чтобы был 0, 1, 2, ...
    df = df.reset_index(drop=True)
    
    # Создаем группы: 0,0,0,1,1,1,2,2,2...
    group_ids = np.arange(len(df)) // bars
    
    # Находим границы каждой группы (начальный и конечный индекс)
    group_ranges = df.groupby(group_ids).apply(lambda x: (x.index[0], x.index[-1]))
    
    # Рассчитываем Pivot Points для каждой группы
    grouped = df.groupby(group_ids).agg({
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })
    grouped['PP'] = (grouped['high'] + grouped['low'] + grouped['close']) / 3
    grouped['R1'] = 2 * grouped['PP'] - grouped['low']
    grouped['S1'] = 2 * grouped['PP'] - grouped['high']
    grouped['R2'] = grouped['PP'] + (grouped['high'] - grouped['low'])
    grouped['S2'] = grouped['PP'] - (grouped['high'] - grouped['low'])
    
    # Инициализируем колонки для уровней
    for col in ['PP', 'R1', 'R2', 'S1', 'S2']:
        df[col] = np.nan
    
    # Заполняем уровни для каждой группы (горизонтальные линии)
    for group_id, (start_idx, end_idx) in group_ranges.items():
        df.loc[start_idx:end_idx, 'PP'] = grouped.loc[group_id, 'PP']
        df.loc[start_idx:end_idx, 'R1'] = grouped.loc[group_id, 'R1']
        df.loc[start_idx:end_idx, 'S1'] = grouped.loc[group_id, 'S1']
        df.loc[start_idx:end_idx, 'R2'] = grouped.loc[group_id, 'R2']
        df.loc[start_idx:end_idx, 'S2'] = grouped.loc[group_id, 'S2']
    
    return df

#USE THIS
def add_chaikin_volatility(df: pd.DataFrame, ema_period=10, change_period=10):
    """
    Добавляет колонку 'chaikin_volatility' в DataFrame.
    
    :param df: DataFrame с колонками 'high', 'low'
    :param ema_period: Период для EMA (по умолчанию 10)
    :param change_period: Период для расчета изменения (по умолчанию 10)
    :return: DataFrame с добавленной колонкой 'chaikin_volatility'
    """
    # Вычисляем разницу между максимумом и минимумом
    df['range'] = df['high'] - df['low']
    
    # Вычисляем EMA разницы
    df['ema_range'] = df['range'].ewm(span=ema_period, adjust=False).mean()
    
    # Вычисляем изменение волатильности
    df['chaikin_volatility'] = (df['ema_range'] - df['ema_range'].shift(change_period)) / df['ema_range'].shift(change_period) * 100
    
    return df

def add_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    """ 
    Mcfly \n
    Оптимизированный расчет индикатора SuperTrend.
    Использует списки вместо .iloc для максимальной скорости.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame с колонками 'high', 'low', 'close'
    period : int
        Период для расчета ATR (по умолчанию 10)
    multiplier : float
        Множитель для ATR (по умолчанию 3.0)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame с добавленными колонками:
        - 'atr': Average True Range
        - 'supertrend': значения индикатора
        - 'in_uptrend': булевый флаг (True - восходящий тренд)
        - 'upper_band': верхняя полоса
        - 'lower_band': нижняя полоса
    """
    # 1. Рассчитываем ATR
    df = add_atr(df, period)
    
    # 2. Конвертируем в списки для быстрого доступа
    high = df['high'].tolist()
    low = df['low'].tolist()
    close = df['close'].tolist()
    atr = df['atr'].tolist()
    n = len(df)
    
    # 3. Инициализируем списки для результатов
    upper_band = [0.0] * n
    lower_band = [0.0] * n
    supertrend = [0.0] * n
    in_uptrend = [True] * n
    
    # 4. Первая итерация (базовые значения)
    upper_band[0] = (high[0] + low[0]) / 2 + multiplier * atr[0]
    lower_band[0] = (high[0] + low[0]) / 2 - multiplier * atr[0]
    supertrend[0] = lower_band[0]  # Начинаем с бычьего тренда
    
    # 5. Основной цикл
    for i in range(1, n):
        # Текущие значения
        high_i = high[i]
        low_i = low[i]
        close_i = close[i]
        atr_i = atr[i]
        
        # Средняя точка (HL2)
        hl2 = (high_i + low_i) / 2
        basic_upper = hl2 + multiplier * atr_i
        basic_lower = hl2 - multiplier * atr_i
        
        # Пересчет полос в зависимости от предыдущего тренда
        if in_uptrend[i-1]:
            # Восходящий тренд
            upper_band[i] = basic_upper
            lower_band[i] = max(basic_lower, lower_band[i-1])
        else:
            # Нисходящий тренд
            lower_band[i] = basic_lower
            upper_band[i] = min(basic_upper, upper_band[i-1])
        
        # Определение тренда
        if close_i > upper_band[i-1]:
            in_uptrend[i] = True
        elif close_i < lower_band[i-1]:
            in_uptrend[i] = False
        else:
            in_uptrend[i] = in_uptrend[i-1]
        
        # Значение SuperTrend
        supertrend[i] = lower_band[i] if in_uptrend[i] else upper_band[i]
    
    # 6. Записываем результаты в DataFrame (быстрое присвоение)
    df['upper_band'] = upper_band
    df['lower_band'] = lower_band
    df['supertrend'] = supertrend
    df['in_uptrend'] = in_uptrend
    
    return df