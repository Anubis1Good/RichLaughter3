import pandas as pd
import numpy as np

def compare_files_verbose(file1_path, file2_path, round_decimals=3):
    """Сравнение с детальной статистикой"""
    
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # Округляем числа
    for col in df1.select_dtypes(include=[np.number]).columns:
        df1[col] = df1[col].round(round_decimals)
    for col in df2.select_dtypes(include=[np.number]).columns:
        df2[col] = df2[col].round(round_decimals)
    
    print("=" * 80)
    print("🔍 СРАВНЕНИЕ ФАЙЛОВ")
    print("=" * 80)
    print(f"Файл 1: {file1_path} → {df1.shape[0]} строк, {df1.shape[1]} колонок")
    print(f"Файл 2: {file2_path} → {df2.shape[0]} строк, {df2.shape[1]} колонок")
    print("=" * 80)
    
    # Общее количество ячеек
    total_cells = len(df1) * len(df1.columns)
    print(f"📊 Всего ячеек для сравнения: {total_cells}")
    
    # Проверяем количество строк
    if len(df1) != len(df2):
        print(f"\n❌ РАЗНОЕ КОЛИЧЕСТВО СТРОК!")
        print(f"   Файл 1: {len(df1)} строк")
        print(f"   Файл 2: {len(df2)} строк")
        return
    
    # Проверяем колонки
    if not df1.columns.equals(df2.columns):
        print(f"\n❌ РАЗНЫЕ КОЛОНКИ!")
        print(f"   Только в файле 1: {set(df1.columns) - set(df2.columns)}")
        print(f"   Только в файле 2: {set(df2.columns) - set(df1.columns)}")
        return
    
    # Сравниваем построчно и поколоночно
    differences = []
    total_diffs = 0
    
    for i in range(len(df1)):
        row_diffs = []
        for col in df1.columns:
            val1 = df1.iloc[i][col]
            val2 = df2.iloc[i][col]
            
            # Проверяем на равенство с учетом NaN
            if pd.isna(val1) and pd.isna(val2):
                continue
            elif pd.isna(val1) or pd.isna(val2):
                row_diffs.append((col, val1, val2))
                total_diffs += 1
            elif val1 != val2:
                row_diffs.append((col, val1, val2))
                total_diffs += 1
        
        if row_diffs:
            differences.append((i, row_diffs))
    
    # Выводим результаты
    if not differences:
        print("\n✅ ФАЙЛЫ ПОЛНОСТЬЮ ИДЕНТИЧНЫ!")
        print(f"   Совпадает {total_cells} из {total_cells} ячеек (100%)")
        return
    
    matching_cells = total_cells - total_diffs
    match_percent = (matching_cells / total_cells) * 100
    
    print(f"\n❌ НАЙДЕНО {len(differences)} СТРОК С НЕСОВПАДЕНИЯМИ")
    print(f"   ВСЕГО НЕСОВПАДЕНИЙ: {total_diffs} из {total_cells} ячеек")
    print(f"   СОВПАДАЕТ: {matching_cells} ячеек ({match_percent:.3f}%)")
    print("=" * 80)
    
    # Выводим все несовпадения
    for i, row_diffs in differences:
        print(f"\n📌 СТРОКА {i} (позиция в датафрейме):")
        
        # Выводим last_confirmed_up
        if 'last_confirmed_up' in df1.columns and 'last_confirmed_up' in df2.columns:
            val1 = df1.iloc[i]['last_confirmed_up']
            val2 = df2.iloc[i]['last_confirmed_up']
            print(f"\n   last_confirmed_up:")
            print(f"      Файл 1: {val1}")
            print(f"      Файл 2: {val2}")
            if val1 == val2:
                print(f"      ✅ СОВПАДАЕТ")
            else:
                print(f"      ❌ НЕ СОВПАДАЕТ")
        
        # Выводим last_confirmed_down
        if 'last_confirmed_down' in df1.columns and 'last_confirmed_down' in df2.columns:
            val1 = df1.iloc[i]['last_confirmed_down']
            val2 = df2.iloc[i]['last_confirmed_down']
            print(f"\n   last_confirmed_down:")
            print(f"      Файл 1: {val1}")
            print(f"      Файл 2: {val2}")
            if val1 == val2:
                print(f"      ✅ СОВПАДАЕТ")
            else:
                print(f"      ❌ НЕ СОВПАДАЕТ")
        
        # Выводим все несовпадения
        print(f"\n   📋 НЕСОВПАДЕНИЯ В ЯЧЕЙКАХ:")
        for col, val1, val2 in row_diffs:
            # Определяем тип различия
            if pd.isna(val1):
                diff_type = "NaN vs значение"
            elif pd.isna(val2):
                diff_type = "значение vs NaN"
            else:
                diff_type = f"разница = {abs(val1 - val2):.3f}" if isinstance(val1, (int, float)) else "разные значения"
            
            print(f"      {col}: '{val1}' != '{val2}'  [{diff_type}]")
    
    print("\n" + "=" * 80)
    print(f"📊 ИТОГО: {len(differences)} строк с ошибками, {total_diffs} несовпадений")
    print(f"   Совпадение на {match_percent:.3f}%")

# Использование
if __name__ == "__main__":
    # compare_files_verbose("faster_actions.csv", "window_actions.csv", round_decimals=3)
    compare_files_verbose("faster_means.csv", "window_means.csv", round_decimals=3)