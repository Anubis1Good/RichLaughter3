import pandas as pd
import numpy as np

# GOOD INDICATOR
def add_precent_zigzag(df:pd.DataFrame, source='high_low', reversal=0.1, use_pct=True):
    """
    Рабочий индикатор ZigZag с правильным отображением линий
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    reversal - величина разворота (в % если use_pct=True, в пунктах если False)
    use_pct - использовать проценты или абсолютные значения для разворота
    """
    df = df.copy()
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Инициализация массивов
    zz = np.full(size, np.nan)
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    
    # Начальные условия
    direction[0] = 1
    last_pivot = highs[0]
    last_pivot_idx = 0
    zz[0] = last_pivot
    
    for i in range(1, size):
        high = highs[i]
        low = lows[i]
        
        if direction[i-1] == 1:  # Предыдущее направление - вверх
            # Обновляем максимум
            if high > last_pivot:
                zz[last_pivot_idx] = np.nan  # Удаляем старый максимум
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            
            # Проверяем разворот
            threshold = last_pivot * (1 - reversal/100) if use_pct else last_pivot - reversal
            if low <= threshold:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            # Обновляем минимум
            if low < last_pivot:
                zz[last_pivot_idx] = np.nan  # Удаляем старый минимум
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            
            # Проверяем разворот
            threshold = last_pivot * (1 + reversal/100) if use_pct else last_pivot + reversal
            if high >= threshold:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    
    # Соединяем точки линиями
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                # Линейная интерполяция между точками
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    return df

def add_dynamic_zigzag(df:pd.DataFrame, source='high_low', n_std=1.5, method='std', period=20):
    """
    ZigZag с динамическим reversal на основе волатильности
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    n_std - множитель для std или среднего (1.5 по умолчанию)
    method - 'std' (стандартное отклонение) или 'mean' (средний диапазон)
    period - период для расчета волатильности
    """
    df = df.copy()
    
    # Проверка на достаточное количество данных
    if len(df) < period:
        raise ValueError(f"Недостаточно данных. Требуется минимум {period} баров")
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Расчет динамического порога разворота
    if method == 'std':
        rolling_std = df['close'].rolling(period).std().bfill()
        reversal_values = rolling_std * n_std
    elif method == 'mean':
        ranges = df['high'] - df['low']
        reversal_values = ranges.rolling(period).mean().bfill() * n_std
    else:
        raise ValueError("method должен быть 'std' или 'mean'")
    
    # Инициализация массивов
    zz = np.full(size, np.nan)
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    
    # Начальные условия (используем первые доступные значения)
    first_valid = max(1, period-1)  # Первый валидный индекс после заполнения rolling
    direction[:first_valid] = 1
    last_pivot = highs[first_valid]
    last_pivot_idx = first_valid
    zz[first_valid] = last_pivot
    
    for i in range(first_valid+1, size):
        high = highs[i]
        low = lows[i]
        reversal = reversal_values.iloc[i]  # Используем iloc для безопасного доступа
        
        if direction[i-1] == 1:  # Предыдущее направление - вверх
            # Обновляем максимум
            if high > last_pivot:
                zz[last_pivot_idx] = np.nan  # Удаляем старый максимум
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            
            # Проверяем разворот
            threshold = last_pivot - reversal
            if low <= threshold:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            # Обновляем минимум
            if low < last_pivot:
                zz[last_pivot_idx] = np.nan  # Удаляем старый минимум
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            
            # Проверяем разворот
            threshold = last_pivot + reversal
            if high >= threshold:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    
    # Соединяем точки линиями
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                # Линейная интерполяция между точками
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    return df

# Good variant
def add_dzz_peaks(df: pd.DataFrame, source='high_low', n_std=1.5, method='std', period=20,drop_last=True):
    """
    add 'zigzag','zigzag_peaks'
    ZigZag с динамическим reversal на основе волатильности
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    n_std - множитель для std или среднего (1.5 по умолчанию)
    method - 'std' (стандартное отклонение) или 'mean' (средний диапазон)
    period - период для расчета волатильности
    
    Возвращает:
    df с колонками:
        zigzag - линейно интерполированные значения зигзага
        zigzag_peaks - точки перелома (пики/впадины)
        zigzag_direction - направление (1=up, -1=down)
        reversal_threshold - порог разворота
    """
    df = df.copy()
    
    # Проверка на достаточное количество данных
    if len(df) < period:
        raise ValueError(f"Недостаточно данных. Требуется минимум {period} баров")
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Расчет динамического порога разворота
    if method == 'std':
        rolling_std = df['close'].rolling(period).std().bfill()
        reversal_values = rolling_std * n_std
    elif method == 'mean':
        ranges = df['high'] - df['low']
        reversal_values = ranges.rolling(period).mean().bfill() * n_std
    else:
        raise ValueError("method должен быть 'std' или 'mean'")
    
    # Инициализация массивов
    zz = np.full(size, np.nan)  # Точки разворота
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    
    # Начальные условия
    first_valid = max(1, period-1)  # Первый валидный индекс после заполнения rolling
    direction[:first_valid] = 1
    last_pivot = highs[first_valid]
    last_pivot_idx = first_valid
    zz[first_valid] = last_pivot  # Первая точка
    
    for i in range(first_valid+1, size):
        high = highs[i]
        low = lows[i]
        reversal = reversal_values.iloc[i]
        prev_dir = direction[i-1]
        
        if prev_dir == 1:  # Предыдущее направление - вверх
            # Сначала проверяем обновление максимума
            if high > last_pivot:
                # Удаляем старый максимум
                zz[last_pivot_idx] = np.nan
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
                direction[i] = 1  # Подтверждаем текущее направление
            # Затем проверяем разворот (только если не обновили максимум)
            elif low <= last_pivot - reversal:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            # Сначала проверяем обновление минимума
            if low < last_pivot:
                # Удаляем старый минимум
                zz[last_pivot_idx] = np.nan
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
                direction[i] = -1  # Подтверждаем текущее направление
            # Затем проверяем разворот (только если не обновили минимум)
            elif high >= last_pivot + reversal:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    
    # Сохраняем точки перелома до интерполяции
    if drop_last:
        zz[-1] = np.nan
    df['zigzag_peaks'] = zz.copy()
    
    # Линейная интерполяция между точками для непрерывного зигзага
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    
    return df


def add_zigzag180826(df: pd.DataFrame, n_std: float = 1.5, period: int = 20):
    """
    ZigZag индикатор.
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    n_std - множитель для std
    period - период для расчета волатильности
    
    Возвращает:
    df с колонками:
        zigzag - линейно интерполированные значения зигзага
        zigzag_peaks - точки перелома
        zigzag_direction - направление (1=up, -1=down)
        reversal_threshold - порог разворота
    """
    df = df.copy()
    
    rolling_std = df['close'].rolling(period).std().bfill()
    reversal_values = rolling_std * n_std
    
    size = len(df)
    zz = np.full(size, np.nan)
    direction = np.zeros(size, dtype=np.int8)
    
    # Первая точка - пик
    first_idx = 0
    first_high = df['high'].iloc[first_idx]
    first_low = df['low'].iloc[first_idx]
    
    # Вторая точка
    second_idx = 1
    second_high = df['high'].iloc[second_idx]
    second_low = df['low'].iloc[second_idx]
    
    if second_high > first_high:
        # Направление 1: точка 1 - локальный минимум, точка 2 - локальный максимум
        direction[first_idx] = 1
        zz[first_idx] = first_low
        local_min = first_low
        local_min_idx = first_idx
        local_max = second_high
        local_max_idx = second_idx
        zz[second_idx] = second_high
        direction[second_idx] = 1
        current_dir = 1
    else:
        # Направление -1: точка 1 - локальный максимум, точка 2 - локальный минимум
        direction[first_idx] = -1
        zz[first_idx] = first_high
        local_max = first_high
        local_max_idx = first_idx
        local_min = second_low
        local_min_idx = second_idx
        zz[second_idx] = second_low
        direction[second_idx] = -1
        current_dir = -1
    
    for i in range(second_idx + 1, size):
        high = df['high'].iloc[i]
        low = df['low'].iloc[i]
        reversal = reversal_values.iloc[i]
        
        if current_dir == 1:
            if high > local_max:
                # Обновляем максимум
                zz[local_max_idx] = np.nan
                local_max = high
                local_max_idx = i
                zz[i] = local_max
                direction[i] = 1
            elif local_max - low > reversal:
                # Разворот вниз
                zz[local_max_idx] = local_max
                current_dir = -1
                local_min = low
                local_min_idx = i
                zz[i] = local_min
                direction[i] = -1
            else:
                direction[i] = 1
        else:  # current_dir == -1
            if low < local_min:
                # Обновляем минимум
                zz[local_min_idx] = np.nan
                local_min = low
                local_min_idx = i
                zz[i] = local_min
                direction[i] = -1
            elif high - local_min > reversal:
                # Разворот вверх
                zz[local_min_idx] = local_min
                current_dir = 1
                local_max = high
                local_max_idx = i
                zz[i] = local_max
                direction[i] = 1
            else:
                direction[i] = -1
    
    # Линейная интерполяция
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    
    df['zigzag_peaks'] = np.where(
        ((df['zigzag'].shift(1) < df['zigzag']) & (df['zigzag'] > df['zigzag'].shift(-1))) |
        ((df['zigzag'].shift(1) > df['zigzag']) & (df['zigzag'] < df['zigzag'].shift(-1))),
        df['zigzag'],
        np.nan
    )
    
    df['reversal_threshold'] = reversal_values


    return df



def add_percent_zz190826(df: pd.DataFrame, source='high_low', percent_threshold=0.1, drop_last=False):
    """
    add 'zigzag','zigzag_peaks'
    ZigZag с динамическим reversal на основе процентного отклонения
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    percent_threshold - процент отклонения для разворота (0.1 = 0.1%)
    drop_last - исключать последний бар (еще не сформировавшийся)
    
    Возвращает:
    df с колонками:
        zigzag - линейно интерполированные значения зигзага
        zigzag_peaks - точки перелома (пики/впадины)
        zigzag_direction - направление (1=up, -1=down)
        reversal_threshold - порог разворота (в абсолютных значениях)
    """
    df = df.copy()
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Инициализация массивов
    zz = np.full(size, np.nan)  # Точки разворота
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    reversal_values = np.full(size, np.nan)  # Пороги разворота
    
    # Начальные условия
    direction[0] = 1  # Начинаем с восходящего тренда
    last_pivot = highs[0]
    last_pivot_idx = 0
    zz[0] = last_pivot  # Первая точка
    
    for i in range(1, size):
        high = highs[i]
        low = lows[i]
        reversal = last_pivot * (percent_threshold / 100)  # Вычисляем процентный порог
        reversal_values[i] = reversal  # Сохраняем порог
        prev_dir = direction[i-1]
        
        if prev_dir == 1:  # Предыдущее направление - вверх
            # Сначала проверяем обновление максимума
            if high > last_pivot:
                # Удаляем старый максимум
                zz[last_pivot_idx] = np.nan
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
                direction[i] = 1  # Подтверждаем текущее направление
            # Затем проверяем разворот (только если не обновили максимум)
            elif low <= last_pivot - reversal:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            # Сначала проверяем обновление минимума
            if low < last_pivot:
                # Удаляем старый минимум
                zz[last_pivot_idx] = np.nan
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
                direction[i] = -1  # Подтверждаем текущее направление
            # Затем проверяем разворот (только если не обновили минимум)
            elif high >= last_pivot + reversal:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    
    # Сохраняем точки перелома до интерполяции
    if drop_last:
        zz[-1] = np.nan

    
    # Линейная интерполяция между точками для непрерывного зигзага
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]

    df['zigzag'] = zz_final
    df['zigzag_peaks'] = np.where(
        ((df['zigzag'].shift(1) < df['zigzag']) & (df['zigzag'] > df['zigzag'].shift(-1))) |
        ((df['zigzag'].shift(1) > df['zigzag']) & (df['zigzag'] < df['zigzag'].shift(-1))),
        df['zigzag'],
        np.nan
    )
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    
    return df

def add_percent_zz_peaks(df: pd.DataFrame, source='high_low', percent_threshold=0.1, drop_last=True):
    """
    add 'zigzag','zigzag_peaks'
    ZigZag с динамическим reversal на основе процентного отклонения
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    percent_threshold - процент отклонения для разворота (0.1 = 0.1%)
    drop_last - исключать последний бар (еще не сформировавшийся)
    
    Возвращает:
    df с колонками:
        zigzag - линейно интерполированные значения зигзага
        zigzag_peaks - точки перелома (пики/впадины)
        zigzag_direction - направление (1=up, -1=down)
        reversal_threshold - порог разворота (в абсолютных значениях)
    """
    df = df.copy()
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Инициализация массивов
    zz = np.full(size, np.nan)  # Точки разворота
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    reversal_values = np.full(size, np.nan)  # Пороги разворота
    
    # Начальные условия
    direction[0] = 1  # Начинаем с восходящего тренда
    last_pivot = highs[0]
    last_pivot_idx = 0
    zz[0] = last_pivot  # Первая точка
    
    for i in range(1, size):
        high = highs[i]
        low = lows[i]
        reversal = last_pivot * (percent_threshold / 100)  # Вычисляем процентный порог
        reversal_values[i] = reversal  # Сохраняем порог
        prev_dir = direction[i-1]
        
        if prev_dir == 1:  # Предыдущее направление - вверх
            # Сначала проверяем обновление максимума
            if high > last_pivot:
                # Удаляем старый максимум
                zz[last_pivot_idx] = np.nan
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
                direction[i] = 1  # Подтверждаем текущее направление
            # Затем проверяем разворот (только если не обновили максимум)
            elif low <= last_pivot - reversal:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            # Сначала проверяем обновление минимума
            if low < last_pivot:
                # Удаляем старый минимум
                zz[last_pivot_idx] = np.nan
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
                direction[i] = -1  # Подтверждаем текущее направление
            # Затем проверяем разворот (только если не обновили минимум)
            elif high >= last_pivot + reversal:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    
    # Сохраняем точки перелома до интерполяции
    if drop_last:
        zz[-1] = np.nan
    df['zigzag_peaks'] = zz.copy()
    
    # Линейная интерполяция между точками для непрерывного зигзага
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    
    return df

def add_dzz_level_channel(df:pd.DataFrame):
    """add 'upper_channel','lower_channel'"""
    points = df[~pd.isna(df['zigzag_peaks'])].iloc[:-1]
    df['upper_channel'] = points[points['zigzag_direction'] == 1]['zigzag_peaks']
    df['lower_channel'] = points[points['zigzag_direction'] == -1]['zigzag_peaks']

    df['upper_channel'] = df['upper_channel'].ffill()
    df['lower_channel'] = df['lower_channel'].ffill()
    return df

def add_dzz_line_channel(df:pd.DataFrame, source='high_low', n_std=1.5, method='std', period=20):
    """
    ZigZag с динамическим reversal и линиями канала
    
    Параметры:
    df - DataFrame с колонками: high, low, close
    source - 'high_low' (по экстремумам) или 'close' (по ценам закрытия)
    n_std - множитель для std или среднего (1.5 по умолчанию)
    method - 'std' (стандартное отклонение) или 'mean' (средний диапазон)
    period - период для расчета волатильности
    
    Возвращает:
    df с колонками:
        zigzag - линейно интерполированные значения зигзага
        zigzag_peaks - точки перелома
        upper_channel - верхняя линия канала
        lower_channel - нижняя линия канала
        reversal_threshold - порог разворота
    """
    df = df.copy()
    
    # Проверка на достаточное количество данных
    if len(df) < period:
        raise ValueError(f"Недостаточно данных. Требуется минимум {period} баров")
    
    # Выбор источника данных
    if source == 'high_low':
        prices = df[['high', 'low']].values
    elif source == 'close':
        prices = df[['close', 'close']].values
    else:
        raise ValueError("source должен быть 'high_low' или 'close'")
    
    highs = prices[:, 0]
    lows = prices[:, 1]
    size = len(df)
    
    # Расчет динамического порога разворота
    if method == 'std':
        rolling_std = df['close'].rolling(period).std().bfill()
        reversal_values = rolling_std * n_std
    elif method == 'mean':
        ranges = df['high'] - df['low']
        reversal_values = ranges.rolling(period).mean().bfill() * n_std
    else:
        raise ValueError("method должен быть 'std' или 'mean'")
    
    # Инициализация массивов
    zz = np.full(size, np.nan)  # Точки разворота
    direction = np.zeros(size, dtype=np.int8)  # 1=up, -1=down
    
    # Начальные условия
    first_valid = max(1, period-1)
    direction[:first_valid] = 1
    last_pivot = highs[first_valid]
    last_pivot_idx = first_valid
    zz[first_valid] = last_pivot
    
    for i in range(first_valid+1, size):
        high = highs[i]
        low = lows[i]
        reversal = reversal_values.iloc[i]
        
        if direction[i-1] == 1:  # Предыдущее направление - вверх
            if high > last_pivot:
                zz[last_pivot_idx] = np.nan
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            
            threshold = last_pivot - reversal
            if low <= threshold:
                direction[i] = -1
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = 1
                
        else:  # Предыдущее направление - вниз
            if low < last_pivot:
                zz[last_pivot_idx] = np.nan
                last_pivot = low
                last_pivot_idx = i
                zz[i] = last_pivot
            
            threshold = last_pivot + reversal
            if high >= threshold:
                direction[i] = 1
                last_pivot = high
                last_pivot_idx = i
                zz[i] = last_pivot
            else:
                direction[i] = -1
    zz[-1] = np.nan
    # Сохраняем точки перелома
    df['zigzag_peaks'] = zz.copy()
    
    # Линейная интерполяция для зигзага
    zz_final = np.full(size, np.nan)
    start_idx = None
    start_val = np.nan
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if start_idx is not None:
                zz_final[start_idx:i+1] = np.linspace(start_val, zz[i], i - start_idx + 1)
            start_idx = i
            start_val = zz[i]
    
    df['zigzag'] = zz_final
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    
    # Собираем верхние и нижние точки
    upper_points = []
    lower_points = []
    
    for i in range(size):
        if not np.isnan(zz[i]):
            if direction[i] == -1:
                upper_points.append((i, zz[i]))
            else:
                lower_points.append((i, zz[i]))
    
    # Инициализация каналов
    upper_channel = np.full(size, np.nan)
    lower_channel = np.full(size, np.nan)
    
    # Функция для построения канала
    def build_channel(points, channel_array):
        if len(points) < 2:
            return
        
        # Для всех точек, начиная со второй
        for i in range(1, len(points)):
            prev_idx, prev_val = points[i-1]
            curr_idx, curr_val = points[i]
            
            # Рассчитываем наклон между предыдущими точками
            slope = (curr_val - prev_val) / (curr_idx - prev_idx)
            
            # Определяем конечный индекс сегмента
            if i < len(points) - 1:
                end_idx = points[i+1][0]
            else:
                end_idx = size - 1  # До конца графика
            
            # Строим линию от текущей точки до конца сегмента
            for k in range(curr_idx, min(end_idx + 1, size)):
                channel_array[k] = curr_val + slope * (k - curr_idx)
    
    # Строим каналы
    build_channel(upper_points, upper_channel)
    build_channel(lower_points, lower_channel)
    
    # Добавляем каналы в датафрейм
    df['upper_channel'] = upper_channel
    df['lower_channel'] = lower_channel
    
    return df

#good indicator
def add_analys_dzz(df, period_sma=3):
    """add 'trend','trend_sma'"""
    # Создаем явную копию DataFrame
    df = df.copy()
    df['trend'] = np.nan
    
    # Создаем копию для работы с пиками
    peacks = df[~df['zigzag_peaks'].isna()].copy()  # Явное копирование
    
    if len(peacks) < 4:
        df['trend'] = 0
        df['trend_sma'] = 0
        return df
    
    # Условия для тренда
    up_condition = (peacks['zigzag_peaks'] > peacks['zigzag_peaks'].shift(2)) & \
                  (peacks['zigzag_peaks'].shift(1) > peacks['zigzag_peaks'].shift(3))
    down_condition = (peacks['zigzag_peaks'] < peacks['zigzag_peaks'].shift(2)) & \
                    (peacks['zigzag_peaks'].shift(1) < peacks['zigzag_peaks'].shift(3))
    
    # Используем .loc для безопасного присвоения
    peacks.loc[:, 'trend'] = 0  # Инициализация через .loc
    peacks.loc[up_condition, 'trend'] = 1
    peacks.loc[down_condition, 'trend'] = -1
    
    # Считаем SMA
    peacks.loc[:, 'trend_sma'] = peacks['trend'].rolling(period_sma).mean()
    
    # Заполняем основной DataFrame
    df['trend'] = peacks['trend'].reindex(df.index).ffill().fillna(0)
    df['trend_sma'] = peacks['trend_sma'].reindex(df.index).ffill().fillna(0)
    
    return df

def add_analys_dzz180826(df, period_sma=3):
    """add 'trend','trend_sma' \n
    180826"""
    # Создаем явную копию DataFrame
    df = df.copy()
    df['trend'] = np.nan
    
    # Создаем копию для работы с пиками
    peacks = df[~df['zp_s'].isna()].copy()  # Явное копирование
    
    if len(peacks) < 4:
        df['trend'] = 0
        df['trend_sma'] = 0
        return df
    
    # Условия для тренда
    up_condition = (peacks['zp_s'] > peacks['zp_s'].shift(2)) & \
                  (peacks['zp_s'].shift(1) > peacks['zp_s'].shift(3))
    down_condition = (peacks['zp_s'] < peacks['zp_s'].shift(2)) & \
                    (peacks['zp_s'].shift(1) < peacks['zp_s'].shift(3))
    
    # Используем .loc для безопасного присвоения
    peacks.loc[:, 'trend'] = 0  # Инициализация через .loc
    peacks.loc[up_condition, 'trend'] = 1
    peacks.loc[down_condition, 'trend'] = -1
    
    # Считаем SMA
    peacks.loc[:, 'trend_sma'] = peacks['trend'].rolling(period_sma).mean()
    
    # Заполняем основной DataFrame
    df['trend'] = peacks['trend'].reindex(df.index).ffill().fillna(0)
    df['trend_sma'] = peacks['trend_sma'].reindex(df.index).ffill().fillna(0)
    
    return df

def help_analiz_pattern18(row,threshold=0.2):
    if pd.isna(row['zp1']):
        return 'none_pattern'
    big = 1 + threshold
    small = 1 - threshold
    if row['r12_23'] > big:
        if row['r23_34'] > big:
            if row['p1_2'] > 0:
                return 'weak_short'
            else:
                return 'weak_long'
        elif row['r23_34'] < small:
            if row['p1_2'] > 0:
                return 'strong_short'
            else:
                return 'strong_long'
        else:
            if row['p1_2'] > 0:
                return 'enter_short_range'
            else:
                return 'enter_long_range'
    elif row['r12_23'] < small:
        if row['r23_34'] > big:
            if row['p1_2'] > 0:
                return 'btc'
            else:
                return 'bti'
        elif row['r23_34'] < small:
            if row['p1_2'] > 0:
                return 'sow'
            else:
                return 'sos'
        else:
            if row['p1_2'] > 0:
                return 'upthrust'
            else:
                return 'spring'
    else:
        if row['r23_34'] > big:
            if row['p1_2'] > 0:
                return 'narrowing_up'
            else:
                return 'narrowing_down'
        elif row['r23_34'] < small:
            if row['p1_2'] > 0:
                return 'bui'
            else:
                return 'joc'
        else:
            if row['p1_2'] > 0:
                return 'bottom_range'
            else:
                return 'top_range'
def add_my_pattern_dzz(df:pd.DataFrame, threshold=0.2):
    """add 'pattern18'"""
    # Создаем явную копию DataFrame
    df = df.copy()
    # Создаем копию для работы с пиками
    peacks = df[~df['zigzag_peaks'].isna()].copy()  # Явное копирование
    if len(peacks) < 4:
        df['pattern18'] = 'none_pattern'
        return df
    peacks['zp1'] = peacks['zigzag_peaks'].shift(3)
    peacks['zp2'] = peacks['zigzag_peaks'].shift(2)
    peacks['zp3'] = peacks['zigzag_peaks'].shift(1)
    peacks['zp4'] = peacks['zigzag_peaks']
    peacks['p1_2'] = peacks['zp1'] - peacks['zp2']
    peacks['p2_3'] = peacks['zp2'] - peacks['zp3']
    peacks['p3_4'] = peacks['zp3'] - peacks['zp4']
    peacks['r12_23'] = abs(peacks['p1_2'] / peacks['p2_3'])
    peacks['r23_34'] = abs(peacks['p2_3'] / peacks['p3_4'])
    peacks['pattern'] = peacks.apply(lambda row: help_analiz_pattern18(row,threshold),axis=1)
    df['pattern18'] = peacks['pattern']
    df['pattern18'] = df['pattern18'].ffill()
    
    return df

def add_pattern18_dzz(df: pd.DataFrame, threshold: float = 0.2, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    add 'pattern18', 'prev_pattern18', 
                'zp1', 'zp2', 'zp3', 'zp4',
                'bzp1', 'bzp2', 'bzp3', 'bzp4',
                'target', 'btarget', 'mzp' \n
    с классификацией паттернов зигзага и буферизованными точками
    patterns:
        'weak_short', 'weak_long',
        'bui', 'joc',
        'double_bottom', 'double_top',
        'btc', 'bti',
        'sow', 'sos',
        'upthrust', 'spring',
        'narrowing_up', 'narrowing_down',
        'bui', 'joc',
        'bottom_range', 'top_range'
    Параметры:
        df - DataFrame с колонкой 'zigzag_peaks'
        threshold - порог для определения соотношения сегментов
        buffer_percent - процент буфера (0.1 = 10%)
    
    Возвращает:
        DataFrame с добавленными колонками
    """
    # Создаем копию DataFrame
    result_df = df.copy()
    
    # Инициализируем колонки
    result_df = result_df.assign(
        pattern18=pd.NA, 
        prev_pattern18=pd.NA,
        bzp1=pd.NA, bzp2=pd.NA, bzp3=pd.NA, bzp4=pd.NA
    )
    
    # Выбираем только точки пиков зигзага
    peaks_mask = ~result_df['zigzag_peaks'].isna()
    peaks = result_df.loc[peaks_mask].copy()
    
    # Недостаточно точек для анализа паттерна
    if len(peaks) < 4:
        return result_df.assign(
            pattern18='none_pattern', 
            prev_pattern18='none_pattern',
            bzp1=pd.NA, bzp2=pd.NA, bzp3=pd.NA, bzp4=pd.NA
        )
    
    # Вычисляем 4 последовательные точки
    peaks = peaks.assign(
        zp1=peaks['zigzag_peaks'].shift(3),
        zp2=peaks['zigzag_peaks'].shift(2),
        zp3=peaks['zigzag_peaks'].shift(1),
        zp4=peaks['zigzag_peaks']
    )
    
    # Удаляем строки с недостаточными данными
    peaks = peaks.loc[~peaks['zp1'].isna()].copy()
    
    # Вычисляем разницы между точками
    peaks = peaks.assign(
        p1_2=peaks['zp1'] - peaks['zp2'],
        p2_3=peaks['zp2'] - peaks['zp3'],
        p3_4=peaks['zp3'] - peaks['zp4']
    )
    
    # Вычисляем буферизованные точки
    peaks = peaks.assign(
        # Внешний буфер для bzp1 (направление зависит от p2_3)
        bzp1=peaks['zp1'] - np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        
        # Внешний буфер для bzp2 (направление зависит от p2_3)
        bzp2=peaks['zp2'] + np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        
        # Внутренний буфер для bzp3 (направление зависит от p3_4)
        bzp3=peaks['zp3'] - np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent,
        
        # Внутренний буфер для bzp4 (направление зависит от p3_4)
        bzp4=peaks['zp4'] + np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent
    )
        # Добавляем целевые точки
    peaks = peaks.assign(
        target=peaks['zp4'] - peaks['p2_3'],  # zp4 + (zp3 - zp4) = zp3
        btarget=peaks['zp4'] - peaks['p2_3'] * (1 - buffer_percent/2),
        mzp = (peaks['zp3'] + peaks['zp4']) / 2
    )
    # Остальной код без изменений
    with np.errstate(divide='ignore', invalid='ignore'):
        r12_23 = np.abs(peaks['p1_2'] / peaks['p2_3'])
        r23_34 = np.abs(peaks['p2_3'] / peaks['p3_4'])
    
    big = 1 + threshold
    small = 1 - threshold
    p1_2_pos = peaks['p1_2'] > 0
    
    conditions = [
        (r12_23 > big) & (r23_34 > big) & p1_2_pos,
        (r12_23 > big) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & ~p1_2_pos
    ]
    
    choices = [
        'weak_short', 'weak_long',
        'bui', 'joc',
        'double_bottom', 'double_top',
        'btc', 'bti',
        'sow', 'sos',
        'upthrust', 'spring',
        'narrowing_up', 'narrowing_down',
        'bui', 'joc',
        'bottom_range', 'top_range'
    ]
    
    peaks_pattern = pd.Series(
        data=np.select(conditions, choices, default='none_pattern'),
        index=peaks.index,
        dtype='object'
    )
    
    prev_peaks_pattern = peaks_pattern.shift(1)
    prev_peaks_pattern.fillna('none_pattern', inplace=True)
    
    result_df['pattern18'] = peaks_pattern.reindex(result_df.index).ffill()
    result_df['prev_pattern18'] = prev_peaks_pattern.reindex(result_df.index).ffill()
    
    result_df['pattern18'] = result_df['pattern18'].replace(pd.NA, 'none_pattern')
    result_df['prev_pattern18'] = result_df['prev_pattern18'].replace(pd.NA, 'none_pattern')
    
    # Обновляем основной DataFrame всеми колонками
    # Разделяем колонки по типам
    num_cols = ['zp1', 'zp2', 'zp3', 'zp4', 
               'bzp1', 'bzp2', 'bzp3', 'bzp4',
               'target', 'btarget', 'mzp']
    
    # Создаем временный DataFrame с числовыми данными
    num_data = peaks[num_cols].reindex(result_df.index).ffill()
    for col in num_cols:
        # Явное преобразование к float64 через numpy
        result_df[col] = num_data[col].values.astype('float64')
       
    return result_df

def add_pattern18_dzz_shifted(df: pd.DataFrame, threshold: float = 0.2, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    Версия индикатора, где все значения смещены на 1 пик назад
    """
    # Создаем копию DataFrame
    result_df = df.copy()
    
    # Инициализируем колонки
    result_df = result_df.assign(
        pattern18='none_pattern', 
        prev_pattern18='none_pattern',
        zp1=pd.NA, zp2=pd.NA, zp3=pd.NA, zp4=pd.NA,
        bzp1=pd.NA, bzp2=pd.NA, bzp3=pd.NA, bzp4=pd.NA,
        target=pd.NA, btarget=pd.NA, mzp=pd.NA
    )
    
    # Выбираем только точки пиков зигзага
    peaks_mask = ~result_df['zigzag_peaks'].isna()
    peaks = result_df.loc[peaks_mask].copy()
    
    # Недостаточно точек для анализа паттерна
    if len(peaks) < 4:
        return result_df
    
    # Вычисляем 4 последовательные точки (оригинальный расчет)
    peaks = peaks.assign(
        zp1=peaks['zigzag_peaks'].shift(3),
        zp2=peaks['zigzag_peaks'].shift(2),
        zp3=peaks['zigzag_peaks'].shift(1),
        zp4=peaks['zigzag_peaks']
    )
    
    # Удаляем строки с недостаточными данными
    peaks = peaks.loc[~peaks['zp1'].isna()].copy()
    
    # Вычисляем разницы между точками
    peaks = peaks.assign(
        p1_2=peaks['zp1'] - peaks['zp2'],
        p2_3=peaks['zp2'] - peaks['zp3'],
        p3_4=peaks['zp3'] - peaks['zp4']
    )
    
    # Вычисляем буферизованные точки
    peaks = peaks.assign(
        bzp1=peaks['zp1'] - np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        bzp2=peaks['zp2'] + np.sign(peaks['p2_3']) * np.abs(peaks['p2_3']) * buffer_percent,
        bzp3=peaks['zp3'] - np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent,
        bzp4=peaks['zp4'] + np.sign(peaks['p3_4']) * np.abs(peaks['p3_4']) * buffer_percent,
        target=peaks['zp4'] - peaks['p2_3'],
        btarget=peaks['zp4'] - peaks['p2_3'] * (1 - buffer_percent/2),
        mzp=(peaks['zp3'] + peaks['zp4']) / 2
    )
    
    # Определяем паттерны
    with np.errstate(divide='ignore', invalid='ignore'):
        r12_23 = np.abs(peaks['p1_2'] / peaks['p2_3'])
        r23_34 = np.abs(peaks['p2_3'] / peaks['p3_4'])
    
    big = 1 + threshold
    small = 1 - threshold
    p1_2_pos = peaks['p1_2'] > 0
    
    conditions = [
        (r12_23 > big) & (r23_34 > big) & p1_2_pos,
        (r12_23 > big) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & p1_2_pos,
        (r12_23 > big) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 > big) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & p1_2_pos,
        (r12_23 < small) & (r23_34 > big) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & p1_2_pos,
        (r12_23 < small) & (r23_34 < small) & ~p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & p1_2_pos,
        (r12_23 < small) & (r23_34 >= small) & (r23_34 <= big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 > big) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & (r23_34 < small) & ~p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & p1_2_pos,
        (~(r12_23 < small) & ~(r12_23 > big)) & ~(r23_34 < small) & ~(r23_34 > big) & ~p1_2_pos
    ]
    
    choices = [
        'weak_short', 'weak_long',
        'bui', 'joc',
        'double_bottom', 'double_top',
        'btc', 'bti',
        'sow', 'sos',
        'upthrust', 'spring',
        'narrowing_up', 'narrowing_down',
        'bui', 'joc',
        'bottom_range', 'top_range'
    ]
    
    peaks['pattern18'] = np.select(conditions, choices, default='none_pattern')
    peaks['prev_pattern18'] = peaks['pattern18'].shift(1).fillna('none_pattern')
    
    # Ключевое изменение: смещаем все вычисленные значения на 1 пик назад
    shifted_peaks = peaks.copy()
    shifted_cols = ['pattern18', 'prev_pattern18',
                   'zp1', 'zp2', 'zp3', 'zp4',
                   'bzp1', 'bzp2', 'bzp3', 'bzp4',
                   'target', 'btarget', 'mzp']
    
    for col in shifted_cols:
        shifted_peaks[col] = shifted_peaks[col].shift(1)
    
    # Переносим смещенные значения в основной DataFrame
    for col in shifted_cols:
        # Для числовых колонок используем прямое присвоение
        if col in ['zp1', 'zp2', 'zp3', 'zp4', 'bzp1', 'bzp2', 'bzp3', 'bzp4', 'target', 'btarget', 'mzp']:
            result_df[col] = shifted_peaks[col].reindex(result_df.index).ffill()
        # Для паттернов делаем ffill и заполнение
        else:
            result_df[col] = shifted_peaks[col].reindex(result_df.index).ffill().fillna('none_pattern')
    
    return result_df

def add_pattern18_dzz_czd(df: pd.DataFrame, threshold: float = 0.2, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    Модифицированная версия индикатора паттернов зигзага.
    Паттерны фиксируются только в момент смены направления зигзага.
    """
    result_df = df.copy()
    
    # Инициализация колонок с правильными типами данных
    # Строковые колонки инициализируем строкой, числовые - np.nan
    result_df = result_df.assign(
        pattern18=pd.NA,  # строка
        prev_pattern18=pd.NA,  # строка
        bzp1=np.nan, bzp2=np.nan, bzp3=np.nan, bzp4=np.nan,
        zp1=np.nan, zp2=np.nan, zp3=np.nan, zp4=np.nan,
        target=np.nan, btarget=np.nan, mzp=np.nan
    )
    
    # Проверка наличия необходимых колонок
    if 'zigzag_direction' not in df.columns:
        raise ValueError("DataFrame must contain 'zigzag_direction' column")
    
    # Находим моменты смены направления зигзага
    direction_changes = result_df['zigzag_direction'].diff().ne(0)
    change_indices = direction_changes[direction_changes].index.tolist()
    
    # Если нет смен направления, возвращаем исходный df
    if len(change_indices) == 0:
        result_df['pattern18'] = result_df['pattern18'].fillna('none_pattern')
        result_df['prev_pattern18'] = result_df['prev_pattern18'].fillna('none_pattern')
        return result_df
    
    # Собираем все пики зигзага
    peaks_mask = ~result_df['zigzag_peaks'].isna()
    peaks = result_df.loc[peaks_mask, 'zigzag_peaks']
    
    # Создаем список для хранения результатов
    results = []
    big = 1 + threshold
    small = 1 - threshold
    # Обрабатываем каждую смену направления
    for i, change_idx in enumerate(change_indices):
        # Получаем последние 4 пика до текущей смены направления
        prev_peaks = peaks[peaks.index <= change_idx].tail(4)
        
        # Если не набралось 4 пика, пропускаем
        if len(prev_peaks) < 4:
            continue
        
        # Извлекаем 4 последних пика
        zp1, zp2, zp3, zp4 = prev_peaks[-4:].values
        
        # Вычисляем разницы между точками
        p1_2 = zp1 - zp2
        p2_3 = zp2 - zp3
        p3_4 = zp3 - zp4
        
        # Вычисляем буферизованные точки
        bzp1 = zp1 - np.sign(p2_3) * abs(p2_3) * buffer_percent
        bzp2 = zp2 + np.sign(p2_3) * abs(p2_3) * buffer_percent
        bzp3 = zp3 - np.sign(p3_4) * abs(p3_4) * buffer_percent
        bzp4 = zp4 + np.sign(p3_4) * abs(p3_4) * buffer_percent
        
        # Вычисляем целевые точки
        target = zp4 - p2_3
        btarget = zp4 - p2_3 * (1 - buffer_percent/2)
        mzp = (zp3 + zp4) / 2
        
        # Вычисляем соотношения сегментов
        with np.errstate(divide='ignore', invalid='ignore'):
            r12_23 = abs(p1_2 / p2_3) if p2_3 != 0 else float('inf')
            r23_34 = abs(p2_3 / p3_4) if p3_4 != 0 else float('inf')
        
        # Условия для классификации паттернов

        p1_2_pos = p1_2 > 0
        
        # Определяем паттерн через последовательную проверку условий
        pattern = 'none_pattern'
        
        if r12_23 > big and r23_34 > big:
            pattern = 'weak_short' if p1_2_pos else 'weak_long'
        elif r12_23 > big and r23_34 < small:
            pattern = 'bui' if p1_2_pos else 'joc'
        elif r12_23 > big and small <= r23_34 <= big:
            pattern = 'double_bottom' if p1_2_pos else 'double_top'
        elif r12_23 < small and r23_34 > big:
            pattern = 'btc' if p1_2_pos else 'bti'
        elif r12_23 < small and r23_34 < small:
            pattern = 'sow' if p1_2_pos else 'sos'
        elif r12_23 < small and small <= r23_34 <= big:
            pattern = 'upthrust' if p1_2_pos else 'spring'
        elif (small <= r12_23 <= big) and r23_34 > big:
            pattern = 'narrowing_up' if p1_2_pos else 'narrowing_down'
        elif (small <= r12_23 <= big) and r23_34 < small:
            pattern = 'bui' if p1_2_pos else 'joc'
        elif (small <= r12_23 <= big) and (small <= r23_34 <= big):
            pattern = 'bottom_range' if p1_2_pos else 'top_range'
        # Предыдущий паттерн
        prev_pattern = 'none_pattern'
        if results:
            prev_pattern = results[-1]['pattern18']
        
        # Сохраняем результаты
        results.append({
            'index': change_idx,
            'pattern18': pattern,
            'prev_pattern18': prev_pattern,
            'zp1': zp1, 'zp2': zp2, 'zp3': zp3, 'zp4': zp4,
            'bzp1': bzp1, 'bzp2': bzp2, 'bzp3': bzp3, 'bzp4': bzp4,
            'target': target, 'btarget': btarget, 'mzp': mzp
        })
    
    # Если нет результатов, возвращаем исходный df
    if not results:
        result_df['pattern18'] = result_df['pattern18'].fillna('none_pattern')
        result_df['prev_pattern18'] = result_df['prev_pattern18'].fillna('none_pattern')
        return result_df
    
    # Создаем DataFrame из результатов
    confirmed_data = pd.DataFrame(results).set_index('index')
    
    # Заполняем результаты в основной DataFrame
    # Для каждой колонки из confirmed_data
    for col in confirmed_data.columns:
        # Обновляем значения только в точках смены направления
        result_df.loc[confirmed_data.index, col] = confirmed_data[col]
    
    # Форвардное заполнение для всех колонок
    # Числовые колонки
    num_cols = ['zp1', 'zp2', 'zp3', 'zp4', 'bzp1', 'bzp2', 'bzp3', 'bzp4', 'target', 'btarget', 'mzp']
    for col in num_cols:
        result_df[col] = result_df[col].ffill().astype(float)
    
    # Строковые колонки
    str_cols = ['pattern18', 'prev_pattern18']
    for col in str_cols:
        result_df[col] = result_df[col].ffill().fillna('none_pattern')
    
    return result_df

def add_stop_loss_p18czd(df,divider=2):
    """add 'lsl','ssl'"""
    df = df.copy()
    df['cur_range'] = (df['zp3'] - df['zp4']).abs()

    # Вычисляем min и max между zp3 и zp4 для каждой строки
    df['min_zp'] = df[['zp3', 'zp4']].min(axis=1)
    df['max_zp'] = df[['zp3', 'zp4']].max(axis=1)

    # Вычисляем lsl и ssl
    df['lsl'] = df['min_zp'] - df['cur_range'] / divider
    df['ssl'] = df['max_zp'] + df['cur_range'] / divider

    # Удаляем временные колонки (опционально)
    df = df.drop(columns=['min_zp', 'max_zp'])
    return df

def add_buffer_dzz(df:pd.DataFrame,period=20):
    """add 'hbzz','lbzz'"""
    df['hdz'] = (df['high'] - df['zigzag']).rolling(period).std()
    df['ldz'] = (df['zigzag'] - df['low']).rolling(period).std()
    df['hbzz'] =  df['zigzag'] + df['hdz']
    df['lbzz'] =  df['zigzag'] - df['ldz']
    return df

def add_mean_dzz_peaks(df: pd.DataFrame, period=2, buffer=0.1):
    """add 'top_mean','bottom_mean','delta_mean'"""
    df = df.copy()
    peaks = df[~pd.isna(df['zigzag_peaks'])].copy()  # Добавляем .copy() здесь
    
    # Создаем копии для top и bottom peaks
    top_peaks = peaks[peaks['zigzag_direction'] == 1].copy()
    bottom_peaks = peaks[peaks['zigzag_direction'] == -1].copy()
    
    # Используем .loc для присвоения значений
    top_peaks.loc[:, 'top_mean'] = top_peaks['high'].rolling(period).mean()
    bottom_peaks.loc[:, 'bottom_mean'] = bottom_peaks['low'].rolling(period).mean()
    
    # Объединяем результаты обратно
    df = df.join(top_peaks[['top_mean']], how='left')
    df = df.join(bottom_peaks[['bottom_mean']], how='left')
    
    df['top_mean'] = df['top_mean'].ffill()
    df['bottom_mean'] = df['bottom_mean'].ffill()
    df['delta_mean'] = df['top_mean'] - df['bottom_mean']
    df['buffer_mean'] = df['delta_mean']  * buffer
    df['top_mean'] = df['top_mean'] - df['buffer_mean']
    df['bottom_mean'] = df['bottom_mean'] + df['buffer_mean']
    
    return df

def add_plusdelta_dzz_peaks(df: pd.DataFrame, period=2, buffer=0.1):
    """add 'top_pd','bottom_pd','delta_pd'"""
    df = df.copy()
    peaks = df[~pd.isna(df['zigzag_peaks'])].copy()  # Добавляем .copy() здесь
    
    # Создаем копии для top и bottom peaks
    top_peaks = peaks[peaks['zigzag_direction'] == 1].copy()
    bottom_peaks = peaks[peaks['zigzag_direction'] == -1].copy()
    
    # Используем .loc для присвоения значений
    top_peaks.loc[:, 'delta'] = top_peaks['high'].diff()
    bottom_peaks.loc[:, 'delta'] = bottom_peaks['low'].diff()
    top_peaks.loc[:, 'delta_mean'] = top_peaks['delta'].rolling(period).mean()
    bottom_peaks.loc[:, 'delta_mean'] = bottom_peaks['delta'].rolling(period).mean()
    top_peaks.loc[:, 'top_pd'] = top_peaks['high'] + top_peaks['delta_mean']
    bottom_peaks.loc[:, 'bottom_pd'] = bottom_peaks['low'] + bottom_peaks['delta_mean']
    # Объединяем результаты обратно
    df = df.join(top_peaks[['top_pd']], how='left')
    df = df.join(bottom_peaks[['bottom_pd']], how='left')
    
    df['top_pd'] = df['top_pd'].ffill()
    df['bottom_pd'] = df['bottom_pd'].ffill()
    df['delta_pd'] = df['top_pd'] - df['bottom_pd']
    df['buffer_mean'] = df['delta_pd']  * buffer
    df['top_pd'] = df['top_pd'] - df['buffer_mean']
    df['bottom_pd'] = df['bottom_pd'] + df['buffer_mean']
    return df

def add_exp_plusdelta_dzz_peaks(df: pd.DataFrame, period=2, buffer=0.1):
    """add 'top_pd','bottom_pd','delta_pd'"""
    df = df.copy()
    peaks = df[~pd.isna(df['zigzag_peaks'])].copy()  # Добавляем .copy() здесь
    
    # Создаем копии для top и bottom peaks
    top_peaks = peaks[peaks['zigzag_direction'] == 1].copy()
    bottom_peaks = peaks[peaks['zigzag_direction'] == -1].copy()
    
    # Используем .loc для присвоения значений
    top_peaks.loc[:, 'delta'] = top_peaks['high'].diff()
    bottom_peaks.loc[:, 'delta'] = bottom_peaks['low'].diff()
    top_peaks.loc[:, 'delta_mean'] = top_peaks['delta'].ewm(period).mean()
    bottom_peaks.loc[:, 'delta_mean'] = bottom_peaks['delta'].ewm(period).mean()
    top_peaks.loc[:, 'top_pd'] = top_peaks['high'] + top_peaks['delta_mean']
    bottom_peaks.loc[:, 'bottom_pd'] = bottom_peaks['low'] + bottom_peaks['delta_mean']
    # Объединяем результаты обратно
    df = df.join(top_peaks[['top_pd']], how='left')
    df = df.join(bottom_peaks[['bottom_pd']], how='left')
    
    df['top_pd'] = df['top_pd'].ffill()
    df['bottom_pd'] = df['bottom_pd'].ffill()
    df['delta_pd'] = df['top_pd'] - df['bottom_pd']
    df['buffer_mean'] = df['delta_pd']  * buffer
    df['top_pd'] = df['top_pd'] - df['buffer_mean']
    df['bottom_pd'] = df['bottom_pd'] + df['buffer_mean']
    return df


def add_van_zigzag(df, period=7):
    """add swing_high  swing_low  zigzag  zigzag_high  zigzag_low  zigzag_line"""
    # Создаем копию DataFrame и сбрасываем индекс
    df = df.copy(deep=True).reset_index(drop=True)
    n = len(df)
    
    # Предварительный расчет экстремумов
    df['swing_high'] = df['high'].rolling(window=period+1, min_periods=1).max()
    df['swing_low'] = df['low'].rolling(window=period+1, min_periods=1).min()
    
    # Инициализация массивов
    zigzag = np.full(n, np.nan)
    zigzag_high = np.full(n, np.nan)
    zigzag_low = np.full(n, np.nan)
    
    # Получаем сырые массивы значений
    high_values = df['high'].values
    low_values = df['low'].values
    swing_high_values = df['swing_high'].values
    swing_low_values = df['swing_low'].values
    
    # Основные переменные состояния
    trend_dir = 0
    last_swing_index = -1
    last_swing_price = np.nan
    
    for idx in range(2*period, n):
        high = high_values[idx]
        low = low_values[idx]
        
        # Проверка экстремумов с учетом погрешности
        is_swing_high = np.isclose(high, swing_high_values[idx], atol=1e-5)
        is_swing_low = np.isclose(low, swing_low_values[idx], atol=1e-5)

        if not is_swing_high and not is_swing_low:
            continue

        # Логика обновления зигзага
        if trend_dir == 1 and is_swing_high and high >= last_swing_price:
            _update_zigzag(zigzag, zigzag_high, idx, high, last_swing_index)
            last_swing_index, last_swing_price = idx, high
            
        elif trend_dir == -1 and is_swing_low and low <= last_swing_price:
            _update_zigzag(zigzag, zigzag_low, idx, low, last_swing_index)
            last_swing_index, last_swing_price = idx, low
            
        elif trend_dir <= 0 and is_swing_high:
            trend_dir = 1
            zigzag[idx] = zigzag_high[idx] = high
            last_swing_index, last_swing_price = idx, high
            
        elif trend_dir >= 0 and is_swing_low:
            trend_dir = -1
            zigzag[idx] = zigzag_low[idx] = low
            last_swing_index, last_swing_price = idx, low

    # Добавляем результаты в DataFrame
    df['zigzag'] = zigzag
    df['zigzag_high'] = zigzag_high
    df['zigzag_low'] = zigzag_low
    df['zigzag_line'] = _interpolate_zigzag(zigzag)
    
    # Удаление начальных/конечных NaN
    return _trim_nan(df)

# Вспомогательные функции
def _update_zigzag(zigzag, target_arr, idx, value, last_idx):
    if last_idx != -1:
        zigzag[last_idx] = np.nan
        target_arr[last_idx] = np.nan
    zigzag[idx] = target_arr[idx] = value

def _interpolate_zigzag(zigzag):
    line = np.full_like(zigzag, np.nan)
    points = np.where(~np.isnan(zigzag))[0]
    
    for i in range(len(points)-1):
        start, end = points[i], points[i+1]
        line[start:end+1] = np.linspace(zigzag[start], zigzag[end], end-start+1)
    
    return line

def _trim_nan(df):
    first_valid = df['zigzag'].first_valid_index()
    last_valid = df['zigzag'].last_valid_index()
    
    if first_valid is not None and last_valid is not None:
        cols = ['zigzag', 'zigzag_line', 'zigzag_high', 'zigzag_low']
        df.loc[:first_valid, cols] = np.nan
        df.loc[last_valid+1:, cols] = np.nan
    
    return df

def add_shift_zz_peaks(df, shift=1, add_lust_fake_peak=True):
    """
    add 'zp_s' , 'zp_istop'
    'zp_s' - сдвинутая точка зигзага на shift
    'zp_istop' - точка вверху? (True/False)
    """
    if add_lust_fake_peak:
        last_idx = df.index[-1]

        # Проверяем направление и присваиваем соответствующее значение
        if df.loc[last_idx, 'zigzag_direction'] == 1:
            df.at[last_idx, 'zigzag_peaks'] = df.loc[last_idx, 'high']
        else:
            df.at[last_idx, 'zigzag_peaks'] = df.loc[last_idx, 'low']
    # Создаем маску для строк, где zigzag_peaks не NaN
    mask = ~pd.isna(df['zigzag_peaks'])
    
    # Создаем новый DataFrame только с нужными строками (явная копия)
    zz = df.loc[mask].copy()
    
    # Добавляем колонки в копию
    zz['zp_s'] = zz['zigzag_peaks'].shift(shift)
    zz['zp_istop'] = zz['zigzag_direction'] < 0
    
    # Инициализируем колонки в исходном df с правильными типами
    df['zp_s'] = np.nan  # float64
    df['zp_istop'] = pd.NA  # или False, или pd.Series(dtype='boolean')
    
    # Записываем значения из zz обратно в df с явным приведением типа
    df.loc[zz.index, 'zp_s'] = zz['zp_s'].astype(float)
    df.loc[zz.index, 'zp_istop'] = zz['zp_istop'].astype('boolean')
    
    return df

# Долгий, не всегда правильные точки выбирает
def add_wzz3p(df: pd.DataFrame, period=55):
    """ add 'wzp1''wzp2''wzp3''idx_wzp1''idx_wzp2''idx_wzp3' \n
    создает 3 точки зигзага в окне
    19.08.2026
    """
    # Инициализация колонок одной строкой
    df[['wzp1', 'wzp2', 'wzp3', 'idx_wzp1', 'idx_wzp2', 'idx_wzp3']] = np.nan
    
    for i in range(period, len(df)):
        start_pos = i - period
        slice1 = df.iloc[start_pos:i]
        
        # Находим экстремумы
        idx_h1 = slice1['high'].idxmax()
        idx_l1 = slice1['low'].idxmin()
        
        pos_h1 = df.index.get_loc(idx_h1)
        pos_l1 = df.index.get_loc(idx_l1)
        
        # Определяем паттерн
        if pos_h1 > pos_l1 or (pos_h1 == pos_l1 and slice1.loc[idx_h1, 'direction'] == 1):
            # Паттерн "рост": l1 -> h1 -> l2
            first_idx, first_val = idx_l1, slice1.loc[idx_l1, 'low']
            second_idx, second_val = idx_h1, slice1.loc[idx_h1, 'high']
            pos_second = pos_h1
            search_min = True
        else:
            # Паттерн "падение": h1 -> l1 -> h2
            first_idx, first_val = idx_h1, slice1.loc[idx_h1, 'high']
            second_idx, second_val = idx_l1, slice1.loc[idx_l1, 'low']
            pos_second = pos_l1
            search_min = False
        
        # Сохраняем первые две точки
        df.loc[df.index[i], ['idx_wzp1', 'wzp1']] = first_idx, first_val
        df.loc[df.index[i], ['idx_wzp2', 'wzp2']] = second_idx, second_val
        
        # Ищем третью точку
        if pos_second + 1 < len(df):
            slice2 = df.iloc[pos_second + 1:i + 1]
            if len(slice2) > 0:
                col = 'low' if search_min else 'high'
                third_idx = slice2[col].idxmin() if search_min else slice2[col].idxmax()
                third_val = slice2.loc[third_idx, col]
                
                df.loc[df.index[i], ['idx_wzp3', 'wzp3']] = third_idx, third_val
    
    # Приводим к Int64
    df[['idx_wzp1', 'idx_wzp2', 'idx_wzp3']] = df[['idx_wzp1', 'idx_wzp2', 'idx_wzp3']].astype('Int64')
    
    return df

# Долгий, не всегда правильные точки выбирает
def add_wzz5p(df: pd.DataFrame, period=55):
    """ add 'wzp1''wzp2''wzp3''wzp4''wzp5' и их индексы \n
    создает 5 точек зигзага в окне
    Точки: 1 -> 2 -> 3 -> 4 -> 5
    где 3 и 4 - промежуточные экстремумы между 2 и 5
    """
    # Инициализация колонок
    cols = ['wzp1', 'wzp2', 'wzp3', 'wzp4', 'wzp5',
            'idx_wzp1', 'idx_wzp2', 'idx_wzp3', 'idx_wzp4', 'idx_wzp5']
    df[cols] = np.nan
    
    for i in range(period, len(df)):
        start_pos = i - period
        slice1 = df.iloc[start_pos:i]
        
        # Находим экстремумы в первом окне
        idx_h1 = slice1['high'].idxmax()
        idx_l1 = slice1['low'].idxmin()
        
        pos_h1 = df.index.get_loc(idx_h1)
        pos_l1 = df.index.get_loc(idx_l1)
        
        # Определяем паттерн для первых двух точек
        if pos_h1 > pos_l1 or (pos_h1 == pos_l1 and slice1.loc[idx_h1, 'direction'] == 1):
            # Паттерн "рост": l1 -> h1 -> ... -> l2
            first_idx, first_val = idx_l1, slice1.loc[idx_l1, 'low']
            second_idx, second_val = idx_h1, slice1.loc[idx_h1, 'high']
            pos_second = pos_h1
            is_up = True
        else:
            # Паттерн "падение": h1 -> l1 -> ... -> h2
            first_idx, first_val = idx_h1, slice1.loc[idx_h1, 'high']
            second_idx, second_val = idx_l1, slice1.loc[idx_l1, 'low']
            pos_second = pos_l1
            is_up = False
        
        # Сохраняем первые две точки
        df.loc[df.index[i], ['idx_wzp1', 'wzp1']] = first_idx, first_val
        df.loc[df.index[i], ['idx_wzp2', 'wzp2']] = second_idx, second_val
        
        # Ищем пятую точку (последний экстремум)
        if pos_second + 1 < len(df):
            slice_last = df.iloc[pos_second + 1:i + 1]
            if len(slice_last) > 0:
                if is_up:
                    # Для роста ищем минимум после максимума (точка 5)
                    fifth_idx = slice_last['low'].idxmin()
                    fifth_val = slice_last.loc[fifth_idx, 'low']
                else:
                    # Для падения ищем максимум после минимума (точка 5)
                    fifth_idx = slice_last['high'].idxmax()
                    fifth_val = slice_last.loc[fifth_idx, 'high']
                
                pos_fifth = df.index.get_loc(fifth_idx)
                
                # Сохраняем пятую точку
                df.loc[df.index[i], ['idx_wzp5', 'wzp5']] = fifth_idx, fifth_val
                
                # Теперь ищем точки 3 и 4 между точкой 2 и точкой 5
                if pos_second + 1 < pos_fifth:
                    # Разделяем промежуток между точкой 2 и точкой 5 пополам
                    mid_pos = (pos_second + pos_fifth) // 2
                    
                    # Первая половина: от точки 2 до середины
                    slice3 = df.iloc[pos_second + 1:mid_pos + 1]
                    if len(slice3) > 0:
                        if is_up:
                            # После максимума ищем минимум (точка 3)
                            third_idx = slice3['low'].idxmin()
                            third_val = slice3.loc[third_idx, 'low']
                        else:
                            # После минимума ищем максимум (точка 3)
                            third_idx = slice3['high'].idxmax()
                            third_val = slice3.loc[third_idx, 'high']
                        
                        df.loc[df.index[i], ['idx_wzp3', 'wzp3']] = third_idx, third_val
                    
                    # Вторая половина: от середины до точки 5
                    slice4 = df.iloc[mid_pos + 1:pos_fifth + 1]
                    if len(slice4) > 0:
                        if is_up:
                            # Ищем максимум перед минимумом (точка 4)
                            fourth_idx = slice4['high'].idxmax()
                            fourth_val = slice4.loc[fourth_idx, 'high']
                        else:
                            # Ищем минимум перед максимумом (точка 4)
                            fourth_idx = slice4['low'].idxmin()
                            fourth_val = slice4.loc[fourth_idx, 'low']
                        
                        df.loc[df.index[i], ['idx_wzp4', 'wzp4']] = fourth_idx, fourth_val
    
    # Приводим индексы к Int64
    idx_cols = ['idx_wzp1', 'idx_wzp2', 'idx_wzp3', 'idx_wzp4', 'idx_wzp5']
    df[idx_cols] = df[idx_cols].astype('Int64')
    
    return df


def get_rolling_extremes_indices(series: pd.Series, period: int, extremum: str):
    """Получает индексы экстремумов для скользящего окна"""
    indices = []
    for i in range(len(series)):
        start = max(0, i - period + 1)
        window = series.iloc[start:i+1]
        if len(window) == period:
            if extremum == 'max':
                indices.append(window.idxmax())
            else:  # 'min'
                indices.append(window.idxmin())
        else:
            indices.append(pd.NaT)
    return indices


# Прикольно, но как будто, можно лучше сделать. В любом случае с этим нужно будет что-то сделать
def add_window_zigzag190826(df: pd.DataFrame, period=55):
    cols = ['wzp1', 'wzp2', 'wzp3', 'wzp4', 
            'idx_wzp1', 'idx_wzp2', 'idx_wzp3', 'idx_wzp4',
            'dir_wzp1', 'dir_wzp2', 'dir_wzp3']
    df[cols] = np.nan
    
    # Получаем rolling экстремумы
    df['max_value'] = df['high'].rolling(period).max()
    df['min_value'] = df['low'].rolling(period).min()
    df['max_idx'] = get_rolling_extremes_indices(df['high'], period, 'max')
    df['min_idx'] = get_rolling_extremes_indices(df['low'], period, 'min')
    
    # Основные случаи - векторизация
    mask_max_after_min = df['max_idx'] > df['min_idx']
    mask_min_after_max = df['max_idx'] < df['min_idx']
    
    # Заполняем основные случаи одной операцией
    df.loc[mask_max_after_min, ['wzp4', 'wzp3', 'wzp2']] = df.loc[mask_max_after_min, ['low', 'max_value', 'min_value']].values
    df.loc[mask_max_after_min, ['idx_wzp4', 'idx_wzp3', 'idx_wzp2']] = np.column_stack([
        df.index[mask_max_after_min],
        df.loc[mask_max_after_min, 'max_idx'],
        df.loc[mask_max_after_min, 'min_idx']
    ])
    
    df.loc[mask_min_after_max, ['wzp4', 'wzp3', 'wzp2']] = df.loc[mask_min_after_max, ['high', 'min_value', 'max_value']].values
    df.loc[mask_min_after_max, ['idx_wzp4', 'idx_wzp3', 'idx_wzp2']] = np.column_stack([
        df.index[mask_min_after_max],
        df.loc[mask_min_after_max, 'min_idx'],
        df.loc[mask_min_after_max, 'max_idx']
    ])
    
    # Equal cases - минимизируем обращения к df
    mask_equal = df['max_idx'] == df['min_idx']
    equal_indices = df.index[mask_equal]
    
    # Подготовка данных для equal cases
    for idx in equal_indices:
        pos = df.index.get_loc(idx)
        if pos < period:
            continue
            
        max_idx_val = df.loc[idx, 'max_idx']
        close_ext = df.loc[max_idx_val, 'close']
        nearest_long = df.loc[idx, 'max_value'] - close_ext > close_ext - df.loc[idx, 'min_value']
        
        if nearest_long:
            df.loc[idx, ['wzp4', 'wzp3', 'wzp2']] = [df.loc[idx, 'low'], df.loc[idx, 'max_value'], df.loc[idx, 'min_value']]
            df.loc[idx, ['idx_wzp4', 'idx_wzp3', 'idx_wzp2']] = [idx, max_idx_val, df.loc[idx, 'min_idx']]
        else:
            df.loc[idx, ['wzp4', 'wzp3', 'wzp2']] = [df.loc[idx, 'high'], df.loc[idx, 'min_value'], df.loc[idx, 'max_value']]
            df.loc[idx, ['idx_wzp4', 'idx_wzp3', 'idx_wzp2']] = [idx, df.loc[idx, 'min_idx'], max_idx_val]
    
    # wzp1 - используем предварительно созданные массивы для скорости
    wzp1_values = np.full(len(df), np.nan)
    idx_wzp1_values = np.full(len(df), pd.NaT, dtype='object')
    
    for i in range(period, len(df)):
        if pd.isna(df.iloc[i]['wzp2']):
            continue
            
        wzp2_is_low = df.iloc[i]['wzp2'] == df.iloc[i]['min_value']
        end_idx = df.iloc[i]['idx_wzp2']
        start_idx = df.index[i - period]
        
        if wzp2_is_low:
            mask = (df.index >= start_idx) & (df.index <= end_idx)
            if mask.any():
                wzp1_values[i] = df.loc[mask, 'high'].max()
                idx_wzp1_values[i] = df.loc[mask, 'high'].idxmax()
        else:
            mask = (df.index >= start_idx) & (df.index <= end_idx)
            if mask.any():
                wzp1_values[i] = df.loc[mask, 'low'].min()
                idx_wzp1_values[i] = df.loc[mask, 'low'].idxmin()
    
    df['wzp1'] = wzp1_values
    df['idx_wzp1'] = idx_wzp1_values
    
    return df


"""
    Идеи для зигзагов:
    1. Какая-нибудь функция синусоиды и по ней строить зигзаг
    2. Попытаться строить по скользящей стредней
    3. Диагонали в канеле дончана
"""
# 21092026
# 21 оптимизированная

# ---------- базовые экстремумы ----------

def find_extremum_zzw210926(h, l, from_pos, to_pos, kind):
    """Первый экстремум в [from_pos, to_pos). kind: 'H' или 'L'."""
    if to_pos - from_pos < 1:
        return None
    if kind == 'H':
        sub = h[from_pos:to_pos]
        k = int(np.argmax(sub))
        return (from_pos + k, sub[k], 'H')
    else:
        sub = l[from_pos:to_pos]
        k = int(np.argmin(sub))
        return (from_pos + k, sub[k], 'L')


def find_extremum_last_zzw210926(h, l, from_pos, to_pos, kind):
    """Последний экстремум в [from_pos, to_pos). kind: 'H' или 'L'."""
    if to_pos - from_pos < 1:
        return None
    if kind == 'H':
        sub = h[from_pos:to_pos]
        m = sub.max()
        k = int(np.flatnonzero(sub == m)[-1])
        return (from_pos + k, sub[k], 'H')
    else:
        sub = l[from_pos:to_pos]
        m = sub.min()
        k = int(np.flatnonzero(sub == m)[-1])
        return (from_pos + k, sub[k], 'L')


# ---------- зоны ----------

def pick_zone_zzw210926(S_left, S_mid, S_right, tol_frac):
    max_size = max(S_left, S_mid, S_right)
    if max_size <= 0:
        return 'mid'
    threshold = max_size - tol_frac * max_size
    # порядок важен: right -> mid -> left
    if S_right >= threshold:
        return 'right'
    if S_mid >= threshold:
        return 'mid'
    return 'left'


# ---------- mid-логика: черновые + уточнение ----------

def mid_extras_zzw210926(h, l, L_pos, L_type, R_pos, R_type):
    """
    Логика mid с двумя проходами:
      1. th2_temp — экстремум в левой половине [L, mid(L,R)]
      2. tl3_temp — экстремум в правой половине [th2_temp, R]
      3. h2_real  — последний экстремум в [L+1, tl3_temp)
      4. l3_real  — последний экстремум в [h2_real+1, R)

    Возвращает 2 уточнённые точки (h2_real, l3_real).
    Чередование типов нерушимо: L → p1(opp L) → p2(как L) → R.
    Конвенция границ: левая включается, правая — нет.
    """
    p1_type = 'L' if L_type == 'H' else 'H'
    p2_type = L_type

    # --- черновая th2 ---
    mid1 = (L_pos + R_pos) // 2
    th2 = find_extremum_zzw210926(h, l, L_pos + 1, mid1 + 1, p1_type)
    if th2 is None:
        th2 = find_extremum_zzw210926(h, l, L_pos + 1, R_pos, p1_type)
    if th2 is None:
        return []

    # --- черновая tl3 ---
    mid2 = (th2[0] + R_pos) // 2
    tl3 = find_extremum_zzw210926(h, l, th2[0] + 1, mid2 + 1, p2_type)
    if tl3 is None:
        tl3 = find_extremum_zzw210926(h, l, th2[0] + 1, R_pos, p2_type)
    if tl3 is None:
        return [th2]

    # --- уточнение h2_real: последний экстремум в [L+1, tl3) ---
    h2_real = find_extremum_last_zzw210926(h, l, L_pos + 1, tl3[0], p1_type)
    if h2_real is None:
        h2_real = th2

    # --- уточнение l3_real: последний экстремум в [h2_real+1, R) ---
    l3_real = find_extremum_last_zzw210926(h, l, h2_real[0] + 1, R_pos, p2_type)
    if l3_real is None:
        l3_real = tl3

    return [h2_real, l3_real]


# ---------- helpers для Шагов 5/5.5/6 ----------

def _build_alternating_sequence(all_points, h, l):
    """Чередование с дозаполнением между соседями одного типа."""
    validated = [all_points[0]]
    for p in all_points[1:]:
        prev = validated[-1]
        if p[2] == prev[2]:
            opposite = 'L' if p[2] == 'H' else 'H'
            extra = find_extremum_zzw210926(h, l, prev[0] + 1, p[0], opposite)
            if extra is not None:
                validated.append(extra)
            validated.append(p)
        else:
            validated.append(p)
    return validated


def _dedupe_points(pts):
    seen = set()
    unique = []
    for p in pts:
        key = (p[0], p[2])
        if key not in seen:
            unique.append(p)
            seen.add(key)
    return unique


def _trim_to_four(validated, L_pos, R_pos, op_positions):
    """Обрезка до 4 точек с приоритетом опорных L_pos/R_pos."""
    if len(validated) > 4:
        validated = _dedupe_points(validated)

    if len(validated) > 4:
        final = validated[:4]
        positions_in_final = {p[0] for p in final}
        for op_pos in (L_pos, R_pos):
            if op_pos not in positions_in_final:
                op_point = next(p for p in validated if p[0] == op_pos)
                non_op_indices = [idx for idx, p in enumerate(final)
                                  if p[0] != L_pos and p[0] != R_pos]
                if non_op_indices:
                    final[non_op_indices[-1]] = op_point
        final.sort(key=lambda p: (p[0], p[0] not in op_positions))
        validated = final

    return validated


def _has_strict_alternation(pts):
    for k in range(len(pts) - 1):
        if pts[k][2] == pts[k + 1][2]:
            return False
    return True


# ---------- основной пайплайн ----------
# Слишком сильный прыгает туда-сюда, надо менять по хорошему. Скорее всего проблема, в том, что мы ищем точки то в одном месте, то в другом. Но принцип определения экстремумом в середине, можно перенести на более глубокие версии
def add_zigzag_window_210926(df, period=55, tol_frac=0.10):
    
    n = len(df)
    high = df['high'].to_numpy(dtype=float)
    low = df['low'].to_numpy(dtype=float)
    df_index = df.index.to_numpy()

    # 2D-массивы: 4 точки × n баров
    wzp_prices = np.full((4, n), np.nan)
    wzp_idx = np.full((4, n), np.nan)

    for i in range(period - 1, n):
        start = i - period + 1

        h = high[start:start + period]
        l = low[start:start + period]

        # --- Шаг 1: опорные точки ---
        pos_max = int(np.argmax(h))
        pos_min = int(np.argmin(l))

        if pos_max == pos_min:
            h_masked = h.copy()
            l_masked = l.copy()
            h_masked[pos_max] = -np.inf
            l_masked[pos_min] = np.inf
            alt_max = int(np.argmax(h_masked))
            alt_min = int(np.argmin(l_masked))
            if h[pos_max] - h[alt_max] <= l[alt_min] - l[pos_min]:
                pos_max = alt_max
            else:
                pos_min = alt_min

        if pos_max < pos_min:
            L_pos, L_type = pos_max, 'H'
            R_pos, R_type = pos_min, 'L'
        else:
            L_pos, L_type = pos_min, 'L'
            R_pos, R_type = pos_max, 'H'

        L_price = h[L_pos] if L_type == 'H' else l[L_pos]
        R_price = h[R_pos] if R_type == 'H' else l[R_pos]

        # --- Шаг 2: зоны ---
        S_left = L_pos
        S_mid = R_pos - L_pos - 1
        S_right = period - 1 - R_pos

        chosen = pick_zone_zzw210926(S_left, S_mid, S_right, tol_frac)

        # --- Шаг 3: 2 дополнительные точки ---
        extras = []

        if chosen == 'left':
            t1 = 'L' if L_type == 'H' else 'H'
            t2 = L_type
            p1 = find_extremum_last_zzw210926(h, l, 0, L_pos, t1)
            if p1 is not None:
                extras.append(p1)
                p2 = find_extremum_last_zzw210926(h, l, 0, p1[0], t2)
                if p2 is not None:
                    extras.append(p2)

        elif chosen == 'right':
            t1 = 'L' if R_type == 'H' else 'H'
            t2 = R_type
            p1 = find_extremum_zzw210926(h, l, R_pos + 1, period, t1)
            if p1 is not None:
                extras.append(p1)
                p2 = find_extremum_zzw210926(h, l, p1[0], period, t2)
                if p2 is not None:
                    extras.append(p2)

        else:  # mid
            extras = mid_extras_zzw210926(h, l, L_pos, L_type, R_pos, R_type)

        # --- Шаг 4: сборка и сортировка ---
        op_positions = (L_pos, R_pos)
        all_points = [(L_pos, L_price, L_type), (R_pos, R_price, R_type)] + extras
        all_points.sort(key=lambda p: (p[0], 0 if p[0] in op_positions else 1))

        # --- Шаг 5 + 5.5 ---
        validated = _build_alternating_sequence(all_points, h, l)
        validated = _trim_to_four(validated, L_pos, R_pos, op_positions)

        # --- Шаг 6: fallback на mid-логику ---
        if len(validated) < 4 or not _has_strict_alternation(validated):
            extras_mid = mid_extras_zzw210926(h, l, L_pos, L_type, R_pos, R_type)
            all_points_mid = [(L_pos, L_price, L_type),
                              (R_pos, R_price, R_type)] + extras_mid
            all_points_mid.sort(key=lambda p: (p[0], 0 if p[0] in op_positions else 1))

            validated = _build_alternating_sequence(all_points_mid, h, l)
            validated = _trim_to_four(validated, L_pos, R_pos, op_positions)

        # --- Шаг 6.5: крайний fallback ---
        while len(validated) < 4:
            last = validated[-1]
            if last[2] == 'H':
                validated.append((last[0], l[last[0]], 'L'))
            else:
                validated.append((last[0], h[last[0]], 'H'))

        points = validated[:4]

        # --- Шаг 7: индексы с разрешением коллизий ---
        raw_idx = [p[0] for p in points]
        final_idx = raw_idx[:]
        changed = True
        it = 0
        while changed and it < 100:
            changed = False
            it += 1
            for k in range(len(final_idx) - 1):
                if final_idx[k] >= final_idx[k + 1]:
                    if final_idx[k] - 1 >= 0:
                        final_idx[k] -= 1
                        changed = True
                    elif final_idx[k + 1] + 1 < period:
                        final_idx[k + 1] += 1
                        changed = True

        for k in range(4):
            wzp_prices[k, i] = points[k][1]
            wzp_idx[k, i] = df_index[start + final_idx[k]]

    for k in range(4):
        df[f'wzp{k+1}'] = wzp_prices[k]
        df[f'idx_wzp{k+1}'] = wzp_idx[k]

    return df


def add_pattern18_zzw_210926(
    df: pd.DataFrame,
    threshold: float = 0.2,
    add_codes: bool = False,
) -> pd.DataFrame:
    """
    Добавляет pattern18 на основе уже посчитанных wzp1..wzp4.
    Паттерн определяется на каждом баре (по своему окну).

    Параметры:
        threshold  — граница big/small (1 ± threshold).
        add_codes  — если True, добавит pattern18_code (int) для ML/скорости.
    """
    df = df.copy()

    zp1 = df['wzp1'].to_numpy(dtype=float)
    zp2 = df['wzp2'].to_numpy(dtype=float)
    zp3 = df['wzp3'].to_numpy(dtype=float)
    zp4 = df['wzp4'].to_numpy(dtype=float)

    n = len(df)
    patterns = np.full(n, 'none_pattern', dtype=object)

    p1_2 = zp1 - zp2
    p2_3 = zp2 - zp3
    p3_4 = zp3 - zp4

    valid = (
        ~np.isnan(zp1) & ~np.isnan(zp2) & ~np.isnan(zp3) & ~np.isnan(zp4)
        & (p2_3 != 0) & (p3_4 != 0)
    )

    with np.errstate(divide='ignore', invalid='ignore'):
        r12_23 = np.abs(p1_2 / p2_3)
        r23_34 = np.abs(p2_3 / p3_4)

    big = 1 + threshold
    small = 1 - threshold
    p1_2_pos = p1_2 > 0

    # (имя_условия, маска)
    conds = [
        ((r12_23 > big) & (r23_34 > big),                          'weak'),
        ((r12_23 > big) & (r23_34 < small),                        'r12big_r23small'),
        ((r12_23 > big) & (r23_34 >= small) & (r23_34 <= big),     'r12big_r23mid'),
        ((r12_23 < small) & (r23_34 > big),                        'r12small_r23big'),
        ((r12_23 < small) & (r23_34 < small),                      'r12small_r23small'),
        ((r12_23 < small) & (r23_34 >= small) & (r23_34 <= big),   'r12small_r23mid'),
        ((r12_23 >= small) & (r12_23 <= big) & (r23_34 > big),     'r12mid_r23big'),
        ((r12_23 >= small) & (r12_23 <= big) & (r23_34 < small),   'r12mid_r23small'),
        ((r12_23 >= small) & (r12_23 <= big) & (r23_34 >= small) & (r23_34 <= big), 'both_mid'),
    ]

    # Таблица соответствия: (условие, p1_2_pos) -> паттерн
    table = {
        ('weak',                True):  'weak_short',
        ('weak',                False): 'weak_long',
        ('r12big_r23small',     True):  'bui',
        ('r12big_r23small',     False): 'joc',
        ('r12big_r23mid',       True):  'double_bottom',
        ('r12big_r23mid',       False): 'double_top',
        ('r12small_r23big',     True):  'btc',
        ('r12small_r23big',     False): 'bti',
        ('r12small_r23small',   True):  'sow',
        ('r12small_r23small',   False): 'sos',
        ('r12small_r23mid',     True):  'upthrust',
        ('r12small_r23mid',     False): 'spring',
        ('r12mid_r23big',       True):  'narrowing_up',
        ('r12mid_r23big',       False): 'narrowing_down',
        ('r12mid_r23small',     True):  'bui',
        ('r12mid_r23small',     False): 'joc',
        ('both_mid',            True):  'bottom_range',
        ('both_mid',            False): 'top_range',
    }

    assigned = np.zeros(n, dtype=bool)
    for mask, name in conds:
        m = mask & valid & ~assigned
        if not m.any():
            continue
        idx = np.flatnonzero(m)
        pos_sel = p1_2_pos[idx]
        vals = np.array(
            [table[(name, bool(p))] for p in pos_sel],
            dtype=object,
        )
        patterns[idx] = vals
        assigned |= m

    df['pattern18'] = patterns

    if add_codes:
        # детерминированный код для ML: алфавитный порядок имён
        codes = sorted(set(patterns.tolist()))
        mapping = {name: i for i, name in enumerate(codes)}
        df['pattern18_code'] = np.array(
            [mapping[p] for p in patterns], dtype=np.int16
        )

    return df

def add_zzw_levels(df: pd.DataFrame, buffer_percent: float = 0.1) -> pd.DataFrame:
    """
    Добавляет bzp1..bzp4, target, btarget, mzp на основе wzp1..wzp4.
    Вызывать отдельно — только если нужны уровни.
    """
    df = df.copy()

    zp1 = df['wzp1'].to_numpy(dtype=float)
    zp2 = df['wzp2'].to_numpy(dtype=float)
    zp3 = df['wzp3'].to_numpy(dtype=float)
    zp4 = df['wzp4'].to_numpy(dtype=float)

    p1_2 = zp1 - zp2
    p2_3 = zp2 - zp3
    p3_4 = zp3 - zp4

    df['bzp1'] = zp1 - np.sign(p2_3) * np.abs(p2_3) * buffer_percent
    df['bzp2'] = zp2 + np.sign(p2_3) * np.abs(p2_3) * buffer_percent
    df['bzp3'] = zp3 - np.sign(p3_4) * np.abs(p3_4) * buffer_percent
    df['bzp4'] = zp4 + np.sign(p3_4) * np.abs(p3_4) * buffer_percent

    df['target']  = zp4 - p2_3
    df['btarget'] = zp4 - p2_3 * (1 - buffer_percent / 2)
    df['mzp']     = (zp3 + zp4) / 2

    return df

def add_stop_loss_p18zzw(df, divider=2):
    """
    Добавляет 'lsl' и 'ssl' на основе последних двух точек зигзага (wzp3, wzp4).

    cur_range = |wzp3 - wzp4|
    lsl       = min(wzp3, wzp4) - cur_range / divider
    ssl       = max(wzp3, wzp4) + cur_range / divider

    Параметры:
        df      — DataFrame с колонками wzp3, wzp4
        divider — делитель диапазона (по умолчанию 2)
    """
    df = df.copy()

    zp3 = df['wzp3']
    zp4 = df['wzp4']

    cur_range = (zp3 - zp4).abs()

    min_zp = pd.concat([zp3, zp4], axis=1).min(axis=1)
    max_zp = pd.concat([zp3, zp4], axis=1).max(axis=1)

    df['cur_range'] = cur_range
    df['lsl'] = min_zp + cur_range / divider
    df['ssl'] = max_zp - cur_range / divider

    return df
"""
Название главной функции add_zigzag_window_220926, суффикс для доп функций _zzw220926
Параметры главной функиции df, n_points=8, period=55
1. Надой пройтись окном [i-period:i] по датафрейму (i включаем в окно)
2. Ищем в каждом окне максимум и минимум (это две опорные точки ОТ1 и ОТ2)
3. Далее берем расстояние в барах между ЛКО (левый край окна) и ОТ1, ОТ1 и ОТ2, ОТ2 и ПКО
4. Выбираем большее из них и находим там 2 точки. Тут есть два варианта:
 а) диапазон между двумя точками. Стороим линию т1 и т2. Вычисляем разницу между dhl = high-line и dll = line-low. Берем бар с максимальным dhl или dll. Здесь важно учесть порядок типов, если у нас новая точка А одинакого типа с т1, то искать точку Б, будем между ними, инача, между А:т2. Точка Б можно найти, как локальный экстремум. После чего надо будет убедиться, что точка А - это тоже локальный экстремум в окне между Т1 и Б или Б и т2 в зависимости от того, где мы искали. Если нет переместить точку туда.
 б) диапазон между краем и точкой. Здесь берем сначала экстремум противоположный точке на открезке край:точка или точка:край. А затем экстремум противоположный новой точке на отрезке край:новая точка или новая точка:край
5. точки могут быть на одном баре, если это происходит, то значение сохраняем, а индекс левой точки смещаем на 1 назад.
6. Железобетонное правило нужно соблюдать строгий порядок чередования L-H-L-H или H-L-H-L.
7. все точки должны быть определенны всегда, кроме случая, когда period < n_points
8. Все это выполняется в цикле, пока точек меньше, чем n_points. При этом расстояние мы проверяемся между всеми уже добавленными точками и ищем самом большое
"""

# 22092026
# def add_zigzag_window_220926(df:pd.DataFrame, n_points=4, period=55):
    
#     for k in range(1,n_points+1):
#         df[f'wzp{k}'] = np.nan
#         df[f'idx_wzp{k}'] = np.nan

#     for i in range(period, len(df)):
#         points = []
#         start = i-period
#         end = i+1
#         window = df.iloc[start:end]
#         max_h = window['high'].max()
#         min_l = window['low'].min()
#         idx_max = window['high'].idxmax()
#         idx_min = window['low'].idxmin()
#         points.append([idx_max,max_h,True])
#         points.append([idx_min,min_l,False])
#         points.sort(key=lambda x: x[0])

#         while len(points) < n_points:
#             zones = [start]
#             for p in points:
#                 zones.append(p[0])
#             zones.append(end)
#             # разницы между соседними точками
#             diffs = [zones[i+1] - zones[i] for i in range(len(zones) - 1)]

#             # максимальный диапазон
#             max_diff = max(diffs)
#             max_idx = diffs.index(max_diff)

#             # границы самого большого диапазона
#             zone_start = zones[max_idx]
#             zone_end = zones[max_idx + 1]

#             small_window = window.iloc[zone_start:zone_end+1]
#             if zone_start == start:
#                 right_point = next(p for p in points if p[0] == zone_end)
#                 if right_point[2]:
#                     local_min_l = small_window['low'].min()
#                     local_idx_min = small_window['low'].idxmin()
#                     micro_window = small_window.iloc[zone_start:local_idx_min+1]
#                     local_max_h = micro_window['high'].max()
#                     local_idx_max = micro_window['high'].idxmax()
#                 else:
#                     local_max_h = small_window['high'].max()
#                     local_idx_max = small_window['high'].idxmax()
#                     micro_window = small_window.iloc[zone_start:local_idx_max+1]
#                     local_min_l = micro_window['low'].min()
#                     local_idx_min = micro_window['low'].idxmin()
#             elif zone_end == end:
#                 left_point = next(p for p in points if p[0] == zone_start)
#                 if left_point[2]:
#                     local_min_l = small_window['low'].min()
#                     local_idx_min = small_window['low'].idxmin()
#                     micro_window = small_window.iloc[local_idx_min:zone_end+1]
#                     local_max_h = micro_window['high'].max()
#                     local_idx_max = micro_window['high'].idxmax()
#                 else:
#                     local_max_h = small_window['high'].max()
#                     local_idx_max = small_window['high'].idxmax()
#                     micro_window = small_window.iloc[local_idx_min:zone_end+1]
#                     local_min_l = micro_window['low'].min()
#                     local_idx_min = micro_window['low'].idxmin()
#             else:
#                 left_point = next(p for p in points if p[0] == zone_start)
#                 right_point = next(p for p in points if p[0] == zone_end)
#                 x0, y0, lpT = left_point    # p[0] = индекс, p[1] = цена
#                 x1, y1, rpT = right_point

#                 # приращение на один шаг по индексу
#                 slope = (y1 - y0) / (x1 - x0)
#                 x = np.arange(zone_start, zone_end + 1)
#                 yh = window.iloc[zone_start:zone_end+1]['high'].to_numpy()
#                 y_line = y0 + slope * (x - x0)
#                 diffs_h = yh - y_line
#                 local_pos_h = np.argmax(diffs_h)
#                 max_diff_h = diffs_h[local_pos_h]
#                 global_pos_in_df_h = start + zone_start + local_pos_h   # <-- аккуратно с offset
#                 yl = window.iloc[zone_start:zone_end+1]['low'].to_numpy()
#                 y_line = y0 + slope * (x - x0)
#                 diffs_l = y_line - yl 
#                 local_pos_l = np.argmax(diffs_l)
#                 max_diff_l = diffs_l[local_pos_l]
#                 global_pos_in_df_l = start + zone_start + local_pos_l   # <-- аккуратно с offset
#                 if max_diff_h > max_diff_l:
#                     a_point = [global_pos_in_df_h, small_window.iloc[global_pos_in_df_h]['high'], True]
#                 else:
#                     a_point = [global_pos_in_df_l, small_window.iloc[global_pos_in_df_l]['low'], False]
                
#                 if lpT == a_point[2]:
#                     micro_window = small_window.iloc[x0:a_point[0]+1] 
#                     x1, y1, rpT = a_point
#                     # приращение на один шаг по индексу
#                     slope = (y1 - y0) / (x1 - x0)
#                     x = np.arange(zone_start, zone_end + 1)
#                     yh = window.iloc[zone_start:zone_end+1]['high'].to_numpy()
#                     y_line = y0 + slope * (x - x0)
#                     diffs_h = yh - y_line
#                     local_pos_h = np.argmax(diffs_h)
#                     max_diff_h = diffs_h[local_pos_h]
#                     global_pos_in_df_h = start + zone_start + local_pos_h   # <-- аккуратно с offset
#                     yl = window.iloc[zone_start:zone_end+1]['low'].to_numpy()
#                     y_line = y0 + slope * (x - x0)
#                     diffs_l = y_line - yl 
#                     local_pos_l = np.argmax(diffs_l)
#                     max_diff_l = diffs_l[local_pos_l]
#                     global_pos_in_df_l = start + zone_start + local_pos_l   # <-- аккуратно с offset
#                     if max_diff_h > max_diff_l:
#                         b_point = [global_pos_in_df_h, small_window.iloc[global_pos_in_df_h]['high'], True]
#                     else:
#                         b_point = [global_pos_in_df_l, small_window.iloc[global_pos_in_df_l]['low'], False]
#                 else:
#                     micro_window = small_window.iloc[a_point[0]:x1+1]
#                     x0, y0, lpT = a_point
#                     # приращение на один шаг по индексу
#                     slope = (y1 - y0) / (x1 - x0)
#                     x = np.arange(zone_start, zone_end + 1)
#                     yh = window.iloc[zone_start:zone_end+1]['high'].to_numpy()
#                     y_line = y0 + slope * (x - x0)
#                     diffs_h = yh - y_line
#                     local_pos_h = np.argmax(diffs_h)
#                     max_diff_h = diffs_h[local_pos_h]
#                     global_pos_in_df_h = start + zone_start + local_pos_h   # <-- аккуратно с offset
#                     yl = window.iloc[zone_start:zone_end+1]['low'].to_numpy()
#                     y_line = y0 + slope * (x - x0)
#                     diffs_l = y_line - yl 
#                     local_pos_l = np.argmax(diffs_l)
#                     max_diff_l = diffs_l[local_pos_l]
#                     global_pos_in_df_l = start + zone_start + local_pos_l   # <-- аккуратно с offset
#                     if max_diff_h > max_diff_l:
#                         b_point = [global_pos_in_df_h, small_window.iloc[global_pos_in_df_h]['high'], True]
#                     else:
#                         b_point = [global_pos_in_df_l, small_window.iloc[global_pos_in_df_l]['low'], False]
#                 average_idx = (a_point[0] + b_point[0]) // 2
#                 if a_point[0] < b_point[0]:
#                     micro_window1 = small_window.iloc[a_point[0]:average_idx+1]
#                     micro_window2 = small_window.iloc[average_idx:b_point[0]+1]
#                     if a_point[2]:
#                         local_max_h = micro_window1['high'].max()
#                         local_idx_max = micro_window1['high'].idxmax() 
#                         local_min_l = micro_window2['low'].min()
#                         local_idx_min = micro_window2['low'].idxmin()
#                     else:
#                         local_min_l = micro_window1['low'].min()
#                         local_idx_min = micro_window1['low'].idxmin()
#                         local_max_h = micro_window2['high'].max()
#                         local_idx_max = micro_window2['high'].idxmax() 

#                 else:
#                     micro_window1 = small_window.iloc[b_point[0]:average_idx+1]
#                     micro_window2 = small_window.iloc[average_idx:a_point[0]+1]
#                     if a_point[2]:
#                         local_min_l = micro_window1['low'].min()
#                         local_idx_min = micro_window1['low'].idxmin()
#                         local_max_h = micro_window2['high'].max()
#                         local_idx_max = micro_window2['high'].idxmax() 
#                     else:
#                         local_max_h = micro_window1['high'].max()
#                         local_idx_max = micro_window1['high'].idxmax() 
#                         local_min_l = micro_window2['low'].min()
#                         local_idx_min = micro_window2['low'].idxmin()

#             points.append([local_idx_max,local_max_h,True])
#             points.append([local_idx_min,local_min_l,False])

#         for k, (idx, val, _) in enumerate(points, start=1):
#             df.loc[df.index[i], f'wzp{k}'] = val
#             df.loc[df.index[i], f'idx_wzp{k}'] = idx
    
#     return df



# 23092026

# def add_zigzag_window_230926(df:pd.DataFrame, n_points=8, period=55):
#     for k in range(1,n_points+1):
#         df[f'wzp{k}'] = np.nan
#         df[f'idx_wzp{k}'] = np.nan

#     for i in range(period, len(df)):
#         points = []
#         start = i-period
#         end = i
#         window = df.iloc[start+1:end]
#         max_h = window['high'].max()
#         min_l = window['low'].min()
#         idx_max = window['high'].idxmax()
#         idx_min = window['low'].idxmin()
#         points.append([idx_max,max_h,True])
#         points.append([idx_min,min_l,False])

#         if idx_max < idx_min:
#             p_row = df.iloc[start] 
#             points.append([p_row['x'],p_row['low'],False])
#             p_row = df.iloc[end] 
#             points.append([p_row['x'],p_row['high'],True])
#         else:
#             p_row = df.iloc[start]
#             points.append([p_row['x'],p_row['high'],True])
#             p_row = df.iloc[end] 
#             points.append([p_row['x'],p_row['low'],False])

#         while len(points) < n_points+2:
#             points.sort(key=lambda x: x[0])
#             idxs = [p[0] for p in points]
#             arr = np.asarray(idxs)
#             gaps = np.diff(arr)
#             j = int(np.argmax(gaps))
#             left_point  = points[j]
#             right_point = points[j + 1]
#             # print(max_gap,left_point,right_point)
#             x0, y0, lpT = left_point    # p[0] = индекс, p[1] = цена
#             x1, y1, rpT = right_point

#             slope = (y1 - y0) / (x1 - x0)
#             x = np.arange(x0, x1 + 1)                    # метки, шаг 1 — ок
#             y_line = y0 + slope * (x - x0)

#             yh = df.loc[x0:x1, 'high'].to_numpy()        # 27 значений — ок
#             diffs_h = yh - y_line
#             diffs_h =diffs_h[1:-1]
#             local_pos_h = int(np.argmax(diffs_h))          # 0..26
#             # print(diffs_h,local_pos_h)                       # 27 vs 27 — ок
#             max_diff_h  = diffs_h[local_pos_h]

#             yl = df.loc[x0:x1, 'low'].to_numpy()        # 27 значений — ок
#             diffs_l = y_line - yl
#             diffs_l = diffs_l[1:-1]                        # 27 vs 27 — ок
#             local_pos_l = int(np.argmax(diffs_l))          # 0..26
#             # print(diffs_l,local_pos_l)                       # 27 vs 27 — ок
#             max_diff_l  = diffs_l[local_pos_l]

#             if max_diff_h > max_diff_l:
#                 point_pos = x0+1 + local_pos_h
#                 # print('h')
#                 if lpT:
#                     mw = df.loc[x0:point_pos]
#                     min_l = mw['low'].min()
#                     idx_min = mw['low'].idxmin()
#                     a_point = [idx_min,min_l,False]
#                     mw = df.loc[idx_min:x1]
#                     max_h = mw['high'].max()
#                     idx_max = mw['high'].idxmax()
#                     b_point = [idx_max,max_h,True]
#                 else:
#                     mw = df.loc[point_pos:x1]
#                     min_l = mw['low'].min()
#                     idx_min = mw['low'].idxmin()
#                     a_point = [idx_min,min_l,False]
#                     mw = df.loc[x0:idx_min]
#                     max_h = mw['high'].max()
#                     idx_max = mw['high'].idxmax()
#                     b_point = [idx_max,max_h,True]

#             else:
#                 point_pos = x0+1 + local_pos_l
#                 # print('l',point_pos)
#                 if rpT:
#                     mw = df.loc[x0:point_pos]
#                     max_h = mw['high'].max()
#                     idx_max = mw['high'].idxmax()
#                     b_point = [idx_max,max_h,True]
#                     mw = df.loc[idx_max:x1]
#                     min_l = mw['low'].min()
#                     idx_min = mw['low'].idxmin()
#                     a_point = [idx_min,min_l,False]
#                 else:
#                     mw = df.loc[point_pos:x1]
#                     max_h = mw['high'].max()
#                     idx_max = mw['high'].idxmax()
#                     b_point = [idx_max,max_h,True]
#                     mw = df.loc[x0:idx_max]
#                     min_l = mw['low'].min()
#                     idx_min = mw['low'].idxmin()
#                     a_point = [idx_min,min_l,False]

#             points.append(a_point)
#             points.append(b_point)

#         # print(points)
#         points.sort(key=lambda x: x[0])
#         new_points = []
#         for index,p in enumerate(points):
#             if index == 0 or index == len(points)-1:
#                 last_dir = p[2]
#                 continue
#             if p[0] == points[index+1][0]:
#                 if last_dir != p[2]:
#                     p[0] -= 1
#                 else:
#                     p[0] += 1
#             new_points.append(p)
#             last_dir = p[2]
#         new_points.sort(key=lambda x: x[0])
#         points = new_points
#         # points = points[1:-1]
#         for k, (idx, val, _) in enumerate(points, start=1):
#             df.loc[df.index[i], f'wzp{k}'] = val
#             df.loc[df.index[i], f'idx_wzp{k}'] = idx
    
#     return df

# def add_zigzag_window_230926(df: pd.DataFrame, n_points=8, period=55):
#     n = len(df)
#     high = df['high'].to_numpy(dtype=np.float64)
#     low  = df['low'].to_numpy(dtype=np.float64)
#     x_labels = df['x'].to_numpy() if 'x' in df.columns else df.index.to_numpy()

#     out_wzp    = np.full((n, n_points), np.nan)
#     out_idxwzp = np.full((n, n_points), np.nan)

#     NEG_INF = -np.inf
#     POS_INF =  np.inf

#     for i in range(period, n):
#         start = i - period
#         end   = i

#         # окно start+1 : end (не включая end) — как у вас
#         w_high = high[start + 1:end]
#         w_low  = low[start + 1:end]
#         if w_high.size == 0:
#             continue

#         pos_max = start + 1 + int(np.argmax(w_high))
#         pos_min = start + 1 + int(np.argmin(w_low))

#         p_pos  = [pos_max, pos_min]
#         p_val  = [high[pos_max], low[pos_min]]
#         p_high = [True, False]

#         if pos_max < pos_min:
#             p_pos  += [start, end]
#             p_val  += [low[start], high[end]]
#             p_high += [False, True]
#         else:
#             p_pos  += [start, end]
#             p_val  += [high[start], low[end]]
#             p_high += [True, False]

#         while len(p_pos) < n_points + 2:
#             order = np.argsort(p_pos)
#             p_pos  = [p_pos[k]  for k in order]
#             p_val  = [p_val[k]  for k in order]
#             p_high = [p_high[k] for k in order]

#             gaps = np.diff(p_pos)
#             j = int(np.argmax(gaps))
#             x0, x1 = p_pos[j], p_pos[j + 1]
#             y0, y1 = p_val[j], p_val[j + 1]
#             lpT, rpT = p_high[j], p_high[j + 1]

#             if x1 - x0 <= 2:
#                 break

#             xs = np.arange(x0, x1 + 1, dtype=np.float64)
#             y_line = y0 + (y1 - y0) * (xs - x0) / (x1 - x0)

#             seg_high = high[x0:x1 + 1]
#             seg_low  = low[x0:x1 + 1]

#             diffs_h = seg_high - y_line
#             diffs_l = y_line - seg_low
#             # обрезка краёв — как у вас
#             diffs_h = diffs_h[1:-1]
#             diffs_l = diffs_l[1:-1]
#             if diffs_h.size == 0:
#                 break

#             local_pos_h = int(np.argmax(diffs_h))
#             local_pos_l = int(np.argmax(diffs_l))
#             max_diff_h  = diffs_h[local_pos_h]
#             max_diff_l  = diffs_l[local_pos_l]

#             if max_diff_h > max_diff_l:
#                 point_pos = x0 + 1 + local_pos_h
#                 if lpT:
#                     # min на [x0, point_pos]
#                     seg = low[x0:point_pos + 1]
#                     k = int(np.argmin(seg))
#                     idx_min = x0 + k; min_l = seg[k]
#                     a_point = [idx_min, min_l, False]
#                     # max на [idx_min, x1]
#                     seg = high[idx_min:x1 + 1]
#                     k = int(np.argmax(seg))
#                     idx_max = idx_min + k; max_h = seg[k]
#                     b_point = [idx_max, max_h, True]
#                 else:
#                     # min на [point_pos, x1]
#                     seg = low[point_pos:x1 + 1]
#                     k = int(np.argmin(seg))
#                     idx_min = point_pos + k; min_l = seg[k]
#                     a_point = [idx_min, min_l, False]
#                     # max на [x0, idx_min]
#                     seg = high[x0:idx_min + 1]
#                     k = int(np.argmax(seg))
#                     idx_max = x0 + k; max_h = seg[k]
#                     b_point = [idx_max, max_h, True]
#             else:
#                 point_pos = x0 + 1 + local_pos_l
#                 if rpT:
#                     # max на [x0, point_pos]
#                     seg = high[x0:point_pos + 1]
#                     k = int(np.argmax(seg))
#                     idx_max = x0 + k; max_h = seg[k]
#                     b_point = [idx_max, max_h, True]
#                     # min на [idx_max, x1]
#                     seg = low[idx_max:x1 + 1]
#                     k = int(np.argmin(seg))
#                     idx_min = idx_max + k; min_l = seg[k]
#                     a_point = [idx_min, min_l, False]
#                 else:
#                     # max на [point_pos, x1]
#                     seg = high[point_pos:x1 + 1]
#                     k = int(np.argmax(seg))
#                     idx_max = point_pos + k; max_h = seg[k]
#                     b_point = [idx_max, max_h, True]
#                     # min на [x0, idx_max]
#                     seg = low[x0:idx_max + 1]
#                     k = int(np.argmin(seg))
#                     idx_min = x0 + k; min_l = seg[k]
#                     a_point = [idx_min, min_l, False]

#             p_pos.append(a_point[0]);  p_val.append(a_point[1]);  p_high.append(a_point[2])
#             p_pos.append(b_point[0]);  p_val.append(b_point[1]);  p_high.append(b_point[2])

#         # финальная сортировка
#         order = np.argsort(p_pos)
#         p_pos  = [p_pos[k]  for k in order]
#         p_val  = [p_val[k]  for k in order]
#         p_high = [p_high[k] for k in order]

#         # ваша логика обрезки + чистки дублей со сдвигом
#         new_pos, new_val, new_high = [], [], []
#         last_dir = None
#         L = len(p_pos)
#         for idx in range(L):
#             if idx == 0 or idx == L - 1:
#                 last_dir = p_high[idx]
#                 continue
#             pos = p_pos[idx]
#             # если следующая точка совпадает по x — сдвигаем
#             if idx + 1 < L and pos == p_pos[idx + 1]:
#                 if last_dir != p_high[idx]:
#                     pos -= 1
#                 else:
#                     pos += 1
#             new_pos.append(pos)
#             new_val.append(p_val[idx])
#             new_high.append(p_high[idx])
#             last_dir = p_high[idx]

#         # ещё раз отсортировать (сдвиг мог поменять порядок)
#         order = np.argsort(new_pos)
#         new_pos  = [new_pos[k]  for k in order]
#         new_val  = [new_val[k]  for k in order]

#         m = min(len(new_pos), n_points)
#         for k in range(m):
#             out_wzp[i, k]    = new_val[k]
#             out_idxwzp[i, k] = x_labels[new_pos[k]]

#     for k in range(n_points):
#         df[f'wzp{k+1}']     = out_wzp[:, k]
#         df[f'idx_wzp{k+1}'] = out_idxwzp[:, k]

#     return df
