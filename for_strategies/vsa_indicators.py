import pandas as pd
import numpy as np

def get_rails(row,df:pd.DataFrame):
    if row.name < 1:
        return 0
    prev = df.loc[row.name-1]
    if prev['is_big'] or row['is_big']:
        if prev['direction'] == 1:
            if row['low'] <= prev['low']:
                return -1
        if prev['direction'] == -1:
            if row['high'] >= prev['high']:
                return 1
    return 0

def get_cancel_rails(row,df:pd.DataFrame):
    if row.name < 1:
        return 0
    prev = df.loc[row.name-1]
    if row['rails'] == 1:
        return 
    
stop_long,stop_short = -1,-1
def get_stop_price(row):
    global stop_long,stop_short
    if row.name > 1:
        if row['rails'] == 1:
            stop_long = row['low']
        if row['rails'] == -1:
            stop_short = row['high']
    return np.array([stop_long,stop_short])

def add_stop_price(df:pd.DataFrame):
    """add stop_long,stop_short"""
    points = df.apply(get_stop_price,axis=1)
    points = np.stack(points.values)
    df['stop_long'] = pd.Series(points[:,0])
    df['stop_short'] = pd.Series(points[:,1])
    return df

def add_rails(df:pd.DataFrame):
    """add 'rails', 'stop_long', 'stop_short'"""
    df['rails'] = df.apply(lambda row: get_rails(row,df),axis=1)
    df = add_stop_price(df)
    return df

fl,fs,ps = 0,0,0
def get_period_slice(row):
    global fl,fs, ps
    if not fl:
        if row['rails'] == 1:
            fl = row.name
    if not fs:
        if row['rails'] == -1:
            fs = row.name
    ps = max(fl,fs)

def add_rails_slice(df:pd.DataFrame):
    df.apply(get_period_slice,axis=1)
    df_slice  = df.iloc[ps:]
    df_slice = df_slice.reset_index(drop=True)
    return df_slice

def add_allowance_rails(df:pd.DataFrame):
    """add 'allowance', 'sc'"""
    df['sc'] = df.apply(lambda row: max(row['spred_channel_long'],row['spred_channel_short']),axis=1)
    df['allowance'] = df['sc'] < df['delta_2v']
    return df

def add_spred(df:pd.DataFrame):
    'add "spred"'
    df['spred'] = df['high'] - df['low']
    return df

def get_ogta2_info(row,df:pd.DataFrame):
    info = 0
    if row.name > 1:
        prev = df.loc[row.name-1]
        if prev['spred'] > prev['mean_spred']:
            if prev['low'] > row['low']:
                info -= 1
            if prev['high'] < row['high']:
                info += 1
    return info
    
def add_OGTA2_rails_info(df:pd.DataFrame):
    'add "info"'
    df['info'] = df.apply(lambda row: get_ogta2_info(row,df),axis=1)
    return df

def help_delta(row):
    if row['close'] > row['open']:  # Бычья свеча
        return row['volume']
    elif row['close'] < row['open']:  # Медвежья свеча
        return -row['volume']
    return 0

def add_CDV(df:pd.DataFrame):
    'add "cdv"'
    df['delta'] = df.apply(help_delta,axis=1)
    df['cdv'] = df['delta'].cumsum()  # Кумулятивная сумма
    return df

def add_real_vsa_stop_action(df, volume_threshold=1.2, trend_lookback=3):
    """
    Добавляет колонку 'real_stop_action' с точными сигналами VSA Stop-Action.
    
    Сигналы:
      1  = Buy Stop-Action (остановка падения, разворот вверх)
     -1  = Sell Stop-Action (остановка роста, разворот вниз)
      0  = Нет сигнала
    
    :param df: DataFrame с колонками ['open', 'high', 'low', 'close', 'volume']
    :param volume_threshold: Порог аномального объема (1.2 = на 20% выше среднего)
    :param trend_lookback: Глубина анализа тренда (по умолчанию 3 свечи)
    :return: DataFrame с колонкой 'real_stop_action'
    """
    df = df.copy()
    
    # Средний объем
    df['avg_volume'] = df['volume'].rolling(trend_lookback).mean()
    
    # Аномальный объем
    df['volume_spike'] = (df['volume'] > (volume_threshold * df['avg_volume'])).astype(bool)
    
    # Функции для определения тренда
    def check_downtrend(window):
        return all(window[i] < window[i-1] for i in range(1, len(window)))
    
    def check_uptrend(window):
        return all(window[i] > window[i-1] for i in range(1, len(window)))
    
    # Определяем тренды
    df['downtrend'] = df['low'].rolling(trend_lookback).apply(check_downtrend, raw=True)
    df['uptrend'] = df['high'].rolling(trend_lookback).apply(check_uptrend, raw=True)
    
    # Преобразуем в bool
    df['downtrend'] = df['downtrend'].astype(bool)
    df['uptrend'] = df['uptrend'].astype(bool)
    
    # Условия для сигналов
    mid_price = (df['high'] + df['low']) / 2
    bullish_cond = (df['downtrend'].shift(1)) & (df['close'] > mid_price) & (~df['volume_spike'])
    bearish_cond = (df['uptrend'].shift(1)) & (df['close'] < mid_price) & (~df['volume_spike'])
    
    # Создаем колонку с сигналами
    df['real_stop_action'] = 0
    df.loc[bullish_cond, 'real_stop_action'] = 1
    df.loc[bearish_cond, 'real_stop_action'] = -1
    
    # Удаляем временные колонки
    df.drop(['avg_volume', 'volume_spike', 'downtrend', 'uptrend'], 
            axis=1, 
            inplace=True, 
            errors='ignore')
    
    return df

def add_vsa_stop_action(df, volume_multiplier=2.0, min_spread_ratio=0.7):
    """
    Реализация Stop-Action по VSA:
    - Ищет бар с аномально большими объемом и спредом (финальный импульс)
    - Следующий бар должен показать резкое замедление (спад объема и спреда)

    Параметры:
    :volume_multiplier: Во сколько раз объем должен превышать средний (по умолч. 2x)
    :min_spread_ratio: Минимальный спред (High-Low) относительно среднего (по умолч. 70%)

    Возвращает:
    - Колонку 'vsa_sa' с сигналами: 1 (бычий SA), -1 (медвежий SA), 0 (нет сигнала)
    """
    df = df.copy()
    
    # Средние значения за 5 баров
    df['avg_volume'] = df['volume'].rolling(5).mean()
    df['avg_spread'] = (df['high'] - df['low']).rolling(5).mean()
    
    # Критерии для "стоп-бара" (финальный импульс)
    is_wide_spread = (df['high'] - df['low']) > (min_spread_ratio * df['avg_spread'])
    is_high_volume = df['volume'] > (volume_multiplier * df['avg_volume'])
    
    # Бычий SA: 
    # - Стоп-бар вниз (закрытие в нижней части + большой объем/спред)
    # - Следующий бар - маленький спред/объем и закрытие в верхней половине
    bullish_sa = (
        is_wide_spread & 
        is_high_volume & 
        (df['close'] < (df['high'] + df['low']) * 0.4)  # Закрытие в нижних 40%
    ).shift(1)  # Сигнал на СЛЕДУЮЩЕМ баре
    
    # Медвежий SA:
    # - Стоп-бар вверх (закрытие в верхней части + большой объем/спред)
    # - Следующий бар - маленький спред/объем и закрытие в нижней половине
    bearish_sa = (
        is_wide_spread & 
        is_high_volume & 
        (df['close'] > (df['high'] + df['low']) * 0.6)  # Закрытие в верхних 60%
    ).shift(1)
    
    # Проверка замедления на следующем баре
    next_bar_small = (
        (df['volume'] < df['avg_volume']) & 
        ((df['high'] - df['low']) < df['avg_spread'])
    )
    
    # Итоговые сигналы
    df['vsa_sa'] = 0
    df.loc[bullish_sa & next_bar_small & (df['close'] > (df['high'] + df['low']) / 2), 'vsa_sa'] = 1
    df.loc[bearish_sa & next_bar_small & (df['close'] < (df['high'] + df['low']) / 2), 'vsa_sa'] = -1
    
    # Очистка временных колонок
    df.drop(['avg_volume', 'avg_spread'], axis=1, inplace=True)
    
    return df

def add_simple_stop_action(df, volume_multiplier=2.0, spread_multiplier=1.5, trend_lookback=3):
    """
    'sa_signal'
    Простой Stop-Action индикатор:
    - Ищет бары с аномально большими объемом и спредом
    - Определяет тренд по последним N барам
    - Генерирует сигналы: 1 (покупка), -1 (продажа), 0 (нет сигнала)
    
    Параметры:
    :volume_multiplier: во сколько раз объем должен превышать средний
    :spread_multiplier: во сколько раз спред должен превышать средний
    :trend_lookback: количество баров для определения тренда
    """
    df = df.copy()
    
    # Рассчитываем средние значения
    df['avg_volume'] = df['volume'].rolling(trend_lookback).mean()
    df['avg_spread'] = (df['high'] - df['low']).rolling(trend_lookback).mean()
    
    # Критерии аномального бара
    high_volume = df['volume'] > (volume_multiplier * df['avg_volume'])
    wide_spread = (df['high'] - df['low']) > (spread_multiplier * df['avg_spread'])
    
    # Определяем тренд
    df['trend'] = 0  # 1 = восходящий, -1 = нисходящий
    
    # Восходящий тренд - последние N баров с ростом
    up_trend = df['close'].rolling(trend_lookback).apply(
        lambda x: 1 if all(x[i] > x[i-1] for i in range(1, len(x))) else 0,
        raw=True
    )
    
    # Нисходящий тренд - последние N баров с падением
    down_trend = df['close'].rolling(trend_lookback).apply(
        lambda x: 1 if all(x[i] < x[i-1] for i in range(1, len(x))) else 0,
        raw=True
    )
    
    df.loc[up_trend == 1, 'trend'] = 1
    df.loc[down_trend == 1, 'trend'] = -1
    
    # Генерируем сигналы
    df['sa_signal'] = 0
    df.loc[high_volume & wide_spread & (df['trend'] == 1), 'sa_signal'] = -1  # Продажа
    df.loc[high_volume & wide_spread & (df['trend'] == -1), 'sa_signal'] = 1   # Покупка
    
    # Удаляем временные колонки
    df.drop(['avg_volume', 'avg_spread', 'trend'], axis=1, inplace=True)
    
    return df

def add_aggressive_stop_action(df, volume_multiplier=2.0, spread_multiplier=2.0, trend_lookback=2, min_volume=1000):
    """
    'sa_signal'
    Более агрессивный Stop-Action индикатор с увеличенным количеством сигналов
    
    Параметры:
    :volume_multiplier: менее строгий критерий объема (по умолчанию 1.5x)
    :spread_multiplier: менее строгий критерий спреда (по умолчанию 1.2x)
    :trend_lookback: меньше баров для определения тренда (по умолчанию 2)
    :min_volume: минимальный абсолютный объем для учета
    """
    df = df.copy()
    
    # Рассчитываем средние значения за меньший период
    df['avg_volume'] = df['volume'].rolling(3).mean()
    df['avg_spread'] = (df['high'] - df['low']).rolling(3).mean()
    
    # Более мягкие критерии аномального бара
    high_volume = (df['volume'] > (volume_multiplier * df['avg_volume'])) & (df['volume'] > min_volume)
    wide_spread = (df['high'] - df['low']) > (spread_multiplier * df['avg_spread'])
    
    # Упрощенное определение тренда
    df['trend'] = 0
    df.loc[df['close'] > df['close'].shift(trend_lookback), 'trend'] = 1    # Восходящий
    df.loc[df['close'] < df['close'].shift(trend_lookback), 'trend'] = -1   # Нисходящий
    
    # Дополнительные условия для увеличения сигналов:
    # 1. Учитываем бары с закрытием в экстремуме
    # 2. Добавляем "почти" аномальные бары
    
    # Сигналы на покупку (нисходящий тренд + аномальный бар)
    buy_cond = (df['trend'] == -1) & (high_volume | wide_spread)
    
    # Сигналы на продажу (восходящий тренд + аномальный бар)
    sell_cond = (df['trend'] == 1) & (high_volume | wide_spread)
    
    # Расширенные сигналы (бары с закрытием в экстремуме)
    extended_buy = (df['trend'] == -1) & (df['close'] == df['low']) & (df['volume'] > df['avg_volume'])
    extended_sell = (df['trend'] == 1) & (df['close'] == df['high']) & (df['volume'] > df['avg_volume'])
    
    # Комбинируем все условия
    df['sa_signal'] = 0
    df.loc[buy_cond | extended_buy, 'sa_signal'] = 1
    df.loc[sell_cond | extended_sell, 'sa_signal'] = -1
    
    # Удаляем временные колонки
    df.drop(['avg_volume', 'avg_spread', 'trend'], axis=1, inplace=True, errors='ignore')
    
    return df

def add_balanced_stop_action(df, volume_multiplier=1.5, spread_multiplier=1.2, trend_lookback=2, min_volume=1000):
    """
    'sa_signal'
    Сбалансированная версия индикатора Stop-Action
    
    Параметры для умеренной агрессивности:
    :volume_multiplier: 1.7x среднего объема
    :spread_multiplier: 1.3x среднего спреда
    :trend_lookback: 2 бара для определения тренда
    :min_volume: минимальный объем 1500
    """
    df = df.copy()
    
    # Усреднение за 5 баров для более плавных значений
    df['avg_volume'] = df['volume'].rolling(5).mean()
    df['avg_spread'] = (df['high'] - df['low']).rolling(5).mean()
    
    # Условия для аномальных баров (оба условия должны выполняться)
    anomaly_bar = (
        (df['volume'] > (volume_multiplier * df['avg_volume'])) & 
        (df['volume'] > min_volume) &
        ((df['high'] - df['low']) > (spread_multiplier * df['avg_spread']))
    )
    
    # Определение тренда (более надежное)
    df['trend'] = 0
    df.loc[df['close'] > df['close'].rolling(trend_lookback).mean(), 'trend'] = 1    # Восходящий
    df.loc[df['close'] < df['close'].rolling(trend_lookback).mean(), 'trend'] = -1   # Нисходящий
    
    # Дополнительные фильтры качества:
    # 1. Закрытие в верхней/нижней трети диапазона
    # 2. Объем должен быть выше предыдущего
    price_range = df['high'] - df['low']
    strong_close_bearish = df['close'] > (df['low'] + price_range * 0.66)  # Верхняя треть
    strong_close_bullish = df['close'] < (df['low'] + price_range * 0.33)  # Нижняя треть
    
    # Генерация сигналов
    df['sa_signal'] = 0
    df.loc[
        anomaly_bar & 
        (df['trend'] == 1) & 
        strong_close_bearish &
        (df['volume'] > df['volume'].shift(1)),
        'sa_signal'
    ] = -1  # Сигнал на продажу
    
    df.loc[
        anomaly_bar & 
        (df['trend'] == -1) & 
        strong_close_bullish &
        (df['volume'] > df['volume'].shift(1)),
        'sa_signal'
    ] = 1   # Сигнал на покупку
    
    # Удаление временных колонок
    df.drop(['avg_volume', 'avg_spread', 'trend'], axis=1, inplace=True, errors='ignore')
    
    return df

def add_detect_volume_zones(df, window=10, volume_multiplier=1.5, spread_threshold=1.2):
    """
    Определяет зоны больших баров по объему и спреду
    :param df: DataFrame с колонками ['high', 'low', 'close', 'volume']
    :param window: окно для скользящего среднего
    :param volume_multiplier: во сколько раз объем должен превышать средний
    :param spread_threshold: порог для спреда (в стандартных отклонениях)
    :return: DataFrame с добавленными колонками зон
    """
    # Рассчет базовых показателей
    df['mean_volume'] = df['volume'].rolling(window).mean()
    df['volume_std'] = df['volume'].rolling(window).std()
    df['spread'] = df['high'] - df['low']
    df['mean_spread'] = df['spread'].rolling(window).mean()
    df['spread_std'] = df['spread'].rolling(window).std()
    
    # Комбинированные условия для значимых баров
    volume_condition = df['volume'] > (df['mean_volume'] + volume_multiplier * df['volume_std'])
    spread_condition = df['spread'] > (df['mean_spread'] + spread_threshold * df['spread_std'])
    df['big_spred'] = np.where(spread_condition,True,False)
    # Определение зон
    df['big_bar'] = volume_condition & spread_condition
    df['top_zone'] = np.where(df['big_bar'], df['high'], np.nan)
    df['bottom_zone'] = np.where(df['big_bar'], df['low'], np.nan)
    
    # Заполнение зон вперед с "затуханием"
    df['top_zone'] = df['top_zone'].ffill()
    df['bottom_zone'] = df['bottom_zone'].ffill()
    
    # Дополнительные метрики
    df['zone_width'] = df['top_zone'] - df['bottom_zone']
    df['mid_zone'] = (df['top_zone'] + df['bottom_zone']) / 2
    
    return df

def add_vsai(df,period=20):
    """add 'vsai','vsaima'"""
    df['hl'] = df['high'] - df['low']
    df['vsai'] = df['volume'] / df['hl']
    vsai_roll = df['vsai'].rolling(period, min_periods=1)
    df['vsaima'] = vsai_roll.mean()+vsai_roll.std()
    return df

def add_dvsai(df,period=20,mult=2):
    """add 'dvsai','dvsaima','dvsaiu','dvsaid'"""
    df['hl'] = df['high'] - df['low']
    df['dvsai'] = (df['volume'] / df['hl']) * df['direction']
    vsai_roll = df['dvsai'].rolling(period, min_periods=1)
    df['dvsaima'] = vsai_roll.mean()
    std_roll = vsai_roll.std() * mult
    df['dvsaiu'] = df['dvsaima'] + std_roll
    df['dvsaid'] = df['dvsaima'] - std_roll
    return df

def add_cdvsai(df:pd.DataFrame,period=20,period_ma1=10,period_ma2=5):
    """add 'dvsai','cum_dvsai','ma_cdv1','ma_cdv2'"""
    df['hl'] = df['high'] - df['low']
    df['dvsai'] = (df['volume'] / df['hl']) * df['direction']
    vsai_roll = df['dvsai'].rolling(period, min_periods=1)
    df['cum_dvsai'] = vsai_roll.sum()
    df['ma_cdv1'] = df['cum_dvsai'].rolling(period_ma1).mean()
    df['ma_cdv2'] = df['cum_dvsai'].rolling(period_ma2).mean()
    return df