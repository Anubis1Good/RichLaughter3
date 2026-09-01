import pandas as pd
import numpy as np
from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *
from utils.work_dfs.load_df import simple_load_df
from testing.test_constants import *

# ===== НАСТРОЙКИ =====
WINDOW = 80  # Размер окна
COLUMNS = ['supertrend']  # Колонки для сравнения
THRESHOLD = 0.05  # Порог разницы (абсолютное значение)
# =================================

# ===== ФУНКЦИЯ: Обработка датафрейма =====
def preprocessing(df):
    """Добавляем индикаторы в датафрейм"""
    df = df.copy()
    df = add_supertrend(df, 18, 3)
    # Если нужно добавить другие индикаторы - раскомментируй
    # df = add_percent_zz190826(df, percent_threshold=0.8)
    # df = add_plus_delta_fc2(df)
    return df

# ===== ОСНОВНОЙ КОД =====
def main():
    # Загружаем данные
    print("Загрузка данных...")
    df = simple_load_df(PATH_DF)
    print(f"Загружено {len(df)} строк")
    
    # Обрабатываем весь датафрейм (полный расчет)
    print("Обработка полного датафрейма...")
    df_full_processed = preprocessing(df)
    print("Готово")
    
    # Параметры для перебора
    window_size = WINDOW
    total_rows = len(df)
    all_differences = []
    
    # Перебираем все возможные окна
    print(f"Начинаем перебор окон размером {window_size}...")
    print(f"Всего окон: {total_rows - window_size + 1}")
    
    for start_idx in range(0, total_rows - window_size + 1):
        end_idx = start_idx + window_size
        last_bar_idx = end_idx - 1  # Индекс последнего бара в окне
        
        # Берем срез окна из полного датафрейма
        df_slice = df.iloc[start_idx:end_idx].copy()
        
        # Обрабатываем срез (пересчитываем индикатор на окне)
        df_slice_processed = preprocessing(df_slice)
        
        # Берем последний бар из обработанного среза
        last_bar_slice = df_slice_processed.iloc[-1]
        
        # Берем соответствующий бар из обработанного полного датафрейма
        last_bar_full = df_full_processed.iloc[last_bar_idx]
        
        # Сравниваем значения на последнем баре
        for col in COLUMNS:
            if col in last_bar_full and col in last_bar_slice:
                val_full = last_bar_full[col]
                val_slice = last_bar_slice[col]
                
                # Пропускаем NaN
                if pd.isna(val_full) or pd.isna(val_slice):
                    continue
                
                diff = abs(val_full - val_slice)
                
                # Если разница превышает порог - запоминаем
                if diff > THRESHOLD:
                    all_differences.append({
                        'index': last_bar_idx,
                        'window': f"{start_idx}:{end_idx}",
                        'column': col,
                        'value_full': val_full,
                        'value_slice': val_slice,
                        'difference': diff
                    })
                    
                    # Выводим сразу
                    print(f"Расхождение на индексе {last_bar_idx} "
                          f"(окно {start_idx}:{end_idx}): "
                          f"{col} = {val_full:.4f} (полный) vs "
                          f"{val_slice:.4f} (окно), разница = {diff:.4f}")
    
    # Итоговая статистика
    print("\n" + "="*60)
    print(f"ИТОГО НАЙДЕНО РАСХОЖДЕНИЙ: {len(all_differences)}")
    
    if all_differences:
        # Группируем по индексам, чтобы видеть, на каких барах были расхождения
        unique_indices = set(d['index'] for d in all_differences)
        print(f"Количество уникальных баров с расхождениями: {len(unique_indices)}")
        
        # Сортируем по величине разницы
        all_differences.sort(key=lambda x: x['difference'], reverse=True)
        
        print("\nТОП-10 НАИБОЛЬШИХ РАСХОЖДЕНИЙ:")
        print("-"*60)
        for i, diff in enumerate(all_differences[:10], 1):
            print(f"{i}. Индекс {diff['index']} (окно {diff['window']}): "
                  f"{diff['column']} - разница = {diff['difference']:.4f} "
                  f"({diff['value_full']:.4f} vs {diff['value_slice']:.4f})")
        
        # Собираем статистику по колонкам
        print("\nСТАТИСТИКА ПО КОЛОНКАМ:")
        for col in COLUMNS:
            col_diffs = [d for d in all_differences if d['column'] == col]
            if col_diffs:
                diffs_values = [d['difference'] for d in col_diffs]
                print(f"  {col}:")
                print(f"    Количество расхождений: {len(col_diffs)}")
                print(f"    Минимальная разница: {min(diffs_values):.4f}")
                print(f"    Максимальная разница: {max(diffs_values):.4f}")
                print(f"    Средняя разница: {np.mean(diffs_values):.4f}")
    else:
        print("Расхождений не найдено!")
    
    return all_differences

if __name__ == "__main__":
    differences = main()