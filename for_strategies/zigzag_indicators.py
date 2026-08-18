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


def add_zigzag180826(df: pd.DataFrame, n_std: float = 1.5, period: int = 20, add_lust_fake_peak=True):
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
    
    df['zigzag_peaks'] = np.where(
        ((df['zigzag'].shift(1) < df['zigzag']) & (df['zigzag'] > df['zigzag'].shift(-1))) |
        ((df['zigzag'].shift(1) > df['zigzag']) & (df['zigzag'] < df['zigzag'].shift(-1))),
        df['zigzag'],
        np.nan
    )
    
    df['zigzag_direction'] = direction
    df['reversal_threshold'] = reversal_values
    if add_lust_fake_peak:
        last_idx = df.index[-1]

        # Проверяем направление и присваиваем соответствующее значение
        if df.loc[last_idx, 'zigzag_direction'] == 1:
            df.at[last_idx, 'zigzag_peaks'] = df.loc[last_idx, 'high']
        else:
            df.at[last_idx, 'zigzag_peaks'] = df.loc[last_idx, 'low']

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

def add_shift_zz_peaks(df, shift=1):
    """
    add 'zp_s' , 'zp_istop'
    'zp_s' - сдвинутая точка зигзага на shift
    'zp_istop' - точка вверху? (True/False)
    """
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