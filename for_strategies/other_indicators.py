import pandas as pd

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