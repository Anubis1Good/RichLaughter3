from math import gcd
from functools import reduce
import pandas as pd
import numpy as np

def get_price_step(df, price_cols=['open', 'close', 'high', 'low']):
    """
    Вычисляет шаг цены через НОД всех разниц.
    Автоматически определяет масштаб по данным.
    """
    # Собираем все цены
    all_prices = pd.concat([df[col] for col in price_cols if col in df.columns])
    all_prices = all_prices.dropna()
    
    if len(all_prices) < 2:
        return None
    
    # Получаем уникальные значения
    unique = np.sort(all_prices.unique())
    
    # Вычисляем разницы между соседними значениями
    diffs = np.diff(unique)
    
    # Убираем слишком маленькие разницы
    diffs = diffs[diffs > 1e-9]
    
    if len(diffs) == 0:
        return None
    
    # Определяем масштаб по данным
    # Берем максимальное количество знаков после запятой
    max_decimals = 0
    for price in all_prices[:100]:  # Проверяем первые 100 значений
        price_str = f"{price:.12f}".rstrip('0')
        if '.' in price_str:
            decimals = len(price_str.split('.')[1])
            max_decimals = max(max_decimals, decimals)
    
    # Если все цены целые, шаг = 1 (или проверяем разницы)
    if max_decimals == 0:
        # Проверяем, есть ли разницы меньше 1
        if np.any(diffs < 1):
            max_decimals = 6  # Если есть дробные, увеличиваем точность
        else:
            # Вычисляем НОД целых разниц
            diffs_int = diffs.round().astype(int)
            diffs_int = diffs_int[diffs_int > 0]
            if len(diffs_int) > 0:
                gcd_val = reduce(gcd, diffs_int)
                return float(gcd_val)
            return 1.0
    
    scale = 10 ** max_decimals
    
    # Переводим разницы в целые числа
    diffs_int = (diffs * scale).round().astype(int)
    diffs_int = diffs_int[diffs_int > 0]
    
    if len(diffs_int) == 0:
        return None
    
    # Находим НОД всех разниц
    gcd_val = reduce(gcd, diffs_int)
    
    # Возвращаем шаг в исходном масштабе
    return gcd_val / scale