import pandas as pd
import numpy as np
def add_vangerchik(df: pd.DataFrame):
    """
    Добавляет колонки 'max_vg' и 'min_vg' в DataFrame.
    Оптимизированная версия с использованием векторизованных операций.
    
    :param df: DataFrame с колонками 'max_hb', 'min_hb'
    :return: DataFrame с добавленными колонками 'max_vg', 'min_vg'
    """
    # Вычисляем разницу между 'max_hb' и 'min_hb'
    diff = df['max_hb'] - df['min_hb']
    
    # Вычисляем 'max_vg' и 'min_vg' с использованием векторизованных операций
    df['max_vg'] = df['max_hb'] - diff / 10
    df['min_vg'] = df['min_hb'] + diff / 10
    
    return df

# Нейронка написала, можно докрутить как-то

def add_zigzag_stair(df, period=20, deviation=0.05):
    """Настоящий ZigZag как замена stair"""
    df = df.copy()
    df['stair'] = np.nan
    
    # Ищем локальные экстремумы
    highs = df['high'].values
    lows = df['low'].values
    size = len(df)
    
    # Первая точка
    last_extreme = df['close'].iloc[0]
    last_is_high = True
    
    for i in range(period, size - period):
        # Локальный максимум
        if highs[i] == highs[i-period:i+period+1].max():
            if last_is_high:
                # Проверяем отклонение
                if abs(highs[i] - last_extreme) / last_extreme > deviation:
                    df.loc[i, 'stair'] = highs[i]
                    last_extreme = highs[i]
                    last_is_high = True
            else:
                if abs(highs[i] - last_extreme) / last_extreme > deviation:
                    df.loc[i, 'stair'] = highs[i]
                    last_extreme = highs[i]
                    last_is_high = True
        
        # Локальный минимум
        elif lows[i] == lows[i-period:i+period+1].min():
            if not last_is_high:
                if abs(lows[i] - last_extreme) / last_extreme > deviation:
                    df.loc[i, 'stair'] = lows[i]
                    last_extreme = lows[i]
                    last_is_high = False
            else:
                if abs(lows[i] - last_extreme) / last_extreme > deviation:
                    df.loc[i, 'stair'] = lows[i]
                    last_extreme = lows[i]
                    last_is_high = False
    
    df['stair'] = df['stair'].ffill()
    return df