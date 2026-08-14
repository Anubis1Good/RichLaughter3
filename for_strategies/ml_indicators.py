import numpy as np
import pandas as pd
from math import atan, degrees
from scipy.spatial.distance import cdist

def add_segmented_regression_from_end(df: pd.DataFrame, divider=60, std_dev=1.0, min_points=5):
    """
    'regression_line','upper_channel','lower_channel','regression_slope'
    Строит независимые линейные регрессии на каждом участке длиной divider баров,
    начиная с конца датафрейма, с каналами стандартного отклонения
    
    Параметры:
        df - DataFrame с ценами
        divider - длина участка для каждой регрессии (в барах)
        std_dev - количество стандартных отклонений для каналов
        min_points - минимальное количество точек для построения регрессии
    """
    result_df = df.copy()
    
    # Создаем колонки для результатов
    result_df['regression_line'] = np.nan
    result_df['upper_channel'] = np.nan
    result_df['lower_channel'] = np.nan
    result_df['regression_slope'] = np.nan
    
    # Идем с конца датафрейма к началу
    for i in range(len(result_df), 0, -divider):
        segment_end = i
        segment_start = max(0, i - divider)
        segment = result_df.iloc[segment_start:segment_end]
        
        # Проверяем, что в сегменте достаточно точек
        if len(segment) < min_points:
            continue
            
        x = np.arange(len(segment))
        close_prices = segment['close'].values
        
        try:
            # Строим линейную регрессию для сегмента
            coeffs = np.polyfit(x, close_prices, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            
            # Вычисляем предсказанные значения и стандартное отклонение
            y_pred = np.polyval(coeffs, x)
            residuals = close_prices - y_pred
            current_std = np.std(residuals)
            
            # Заполняем значения для всего сегмента
            result_df.loc[result_df.index[segment_start:segment_end], 'regression_line'] = y_pred
            result_df.loc[result_df.index[segment_start:segment_end], 'upper_channel'] = y_pred + std_dev * current_std
            result_df.loc[result_df.index[segment_start:segment_end], 'lower_channel'] = y_pred - std_dev * current_std
            result_df.loc[result_df.index[segment_start:segment_end], 'regression_slope'] = slope
            
        except (TypeError, np.linalg.LinAlgError) as e:
            continue
    
    # Рассчитываем нормализованный наклон
    result_df['norm_slope'] = np.tanh(result_df['regression_slope'])
    
    return result_df

def add_find_similar_pattern_lite(
    df, 
    window=20, 
    lookback=1000, 
    metric='correlation',
    forecast_length=30
):
    """
    add 'forecast_high'  'forecast_low'  'per_fs'
    Находит похожий паттерн и добавляет к последнему бару:
    - forecast_high: максимум прогноза.
    - forecast_low: минимум прогноза.
    "Метрика должна быть 'correlation', 'mse' или 'cosine'"
    """
    close_prices = df['close'].values
    
    # Проверка данных
    if len(df) < window + forecast_length:
        df['forecast_high'] = np.nan
        df['forecast_low'] = np.nan
        df['per_fs'] = np.nan
        return df
    
    # Корректировка lookback
    lookback = min(lookback, len(close_prices) - (window + forecast_length))
    history = close_prices[-lookback - window - forecast_length : - (window + forecast_length)]
    
    # Текущий паттерн (нормализованный)
    current_pattern = close_prices[-window:]
    current_mean = np.mean(current_pattern)
    current_std = np.std(current_pattern)
    current_norm = (current_pattern - current_mean) / current_std if current_std != 0 else current_pattern * 0
    
    # Поиск похожего паттерна
    best_distance = float('inf')
    best_future = None
    
    for i in range(len(history) - window - forecast_length):
        past_pattern = history[i:i + window]
        future_prices = history[i + window:i + window + forecast_length]
        
        past_mean = np.mean(past_pattern)
        past_std = np.std(past_pattern)
        past_norm = (past_pattern - past_mean) / past_std if past_std != 0 else past_pattern * 0
        
        if metric == 'correlation':
            corr = np.corrcoef(current_norm, past_norm)[0, 1]
            distance = 1 - corr
        elif metric == 'mse':
            distance = np.mean((current_norm - past_norm) ** 2)
        elif metric == 'cosine':
            distance = cdist([current_norm], [past_norm], 'cosine')[0][0]
        else:
            raise ValueError("Метрика должна быть 'correlation', 'mse' или 'cosine'")
        
        if distance < best_distance:
            best_distance = distance
            best_future = future_prices
            best_past_mean = past_mean
            best_past_std = past_std
    
    if best_future is None:
        df['forecast_high'] = np.nan
        df['forecast_low'] = np.nan
        df['per_fs'] = np.nan
        return df
    
    # Масштабируем прогноз
    scale = current_std / best_past_std if best_past_std > 1e-8 else 1.0
    forecast = (best_future - best_past_mean) * scale + current_mean
    
    # Записываем только highs/lows в последний бар
    df.loc[df.index[-1], 'forecast_high'] = np.max(forecast)
    df.loc[df.index[-1], 'forecast_low'] = np.min(forecast)
    epsilon = 1e-8  # Маленькое значение для стабильности
    df['per_fs'] = (((df['forecast_high'] - df['forecast_low']) / (df['forecast_high'] + epsilon)) * 100).round(2)
    return df
