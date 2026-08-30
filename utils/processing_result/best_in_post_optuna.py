import os
import pandas as pd
from tqdm import tqdm
import math
import re

MAX_LENGTH_GLASS_POINT = 12

main_folder = '_test_results\post_optuna_results'
output_filename = 'total_post_optuna_aggregated.xlsx'
df_total = pd.DataFrame()

# Собираем все данные из всех файлов в папке, исключая выходной файл
files = os.listdir(main_folder)
for file in tqdm(files):
    if file.endswith('.xlsx') and file != output_filename:
        file_path = os.path.join(main_folder, file)
        df_file = pd.read_excel(file_path, 'results')
        if not df_file.empty:
            if df_total.empty:
                df_total = df_file
            else:
                df_total = pd.concat([df_total, df_file])

# Дропаем ненужные столбцы
columns_to_drop = ['amount_sl', 'amount_tp', 'sl/tp', 'sl_pct', 'tp_pct']
df_total = df_total.drop(columns=[col for col in columns_to_drop if col in df_total.columns])

# Сортируем по total_fee_per_window
df_total = df_total.sort_values(['origin', 'total_fee_per_window'], ascending=[True, False])
df_total = df_total.reset_index(drop=True)

MAX_LENGTH_GLASS_POINT = 12

def fix_ws_string(s):
    # Ищем имя и значения
    match = re.match(r'\(([^,]+),\((.+)\)\)', s)
    if not match:
        return s
    
    name = match.group(1)
    values_str = match.group(2)
    
    # Разбиваем значения, учитывая что в кавычках может быть запятая
    values = []
    current = ""
    in_quotes = False
    
    for char in values_str:
        if char in ['"', "'"]:
            in_quotes = not in_quotes
            current += char
        elif char == ',' and not in_quotes:
            if current.strip():
                # Пробуем преобразовать
                val = current.strip()
                if val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                elif val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                
                # Обработка 'None' как строки
                if val == 'None':
                    values.append(None)
                else:
                    try:
                        # Пробуем как int, если не получается - как float
                        if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                            values.append(int(val))
                        else:
                            values.append(float(val))
                    except ValueError:
                        # Если не число - сохраняем как строку (без кавычек, добавим позже)
                        values.append(val)
                current = ""
        else:
            current += char
    
    # Последнее значение
    if current.strip():
        val = current.strip()
        if val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        elif val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        
        # Обработка 'None' как строки
        if val == 'None':
            values.append(None)
        else:
            try:
                if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
                    values.append(int(val))
                else:
                    values.append(float(val))
            except ValueError:
                # Если не число - сохраняем как строку (без кавычек, добавим позже)
                values.append(val)
    
    # ==========================================
    # ВЫЧИСЛЕНИЕ new_val ПО НОВОЙ ЛОГИКЕ
    # ==========================================
    if len(values) >= 2:
        first = values[0]
        second = values[1]
        
        is_first_none = first is None
        is_second_none = second is None
        
        try:
            if is_first_none and is_second_none:
                # Оба None -> 1
                new_val = 1
            elif is_first_none:
                # Только первый None -> берем второе число
                new_val = math.ceil(second / MAX_LENGTH_GLASS_POINT)
            elif is_second_none:
                # Только второй None -> берем первое число
                new_val = math.ceil(first / MAX_LENGTH_GLASS_POINT)
            else:
                # Оба числа -> берем максимальное
                max_val = max(first, second)
                new_val = math.ceil(max_val / MAX_LENGTH_GLASS_POINT)
        except (TypeError, ValueError, ZeroDivisionError):
            new_val = 1
    else:
        new_val = 1
    
    # ==========================================
    # ФОРМИРУЕМ НОВУЮ СТРОКУ С КАВЫЧКАМИ
    # ==========================================
    values_str_new = []
    for v in values:
        if v is None:
            values_str_new.append('None')
        elif isinstance(v, str):
            # Строки оборачиваем в кавычки
            values_str_new.append(f"'{v}'")
        else:
            # Числа без кавычек
            values_str_new.append(str(v))
    
    return f"({name},({','.join(values_str_new)}),{new_val},None),"

# Применяем к колонке
df_total['ws'] = df_total['ws'].apply(fix_ws_string)
# Добавляем новые столбцы
df_total['ws_name'] = df_total['ws'].str.extract(r'^\(?([^,(]+)')
df_total['ws_type'] = df_total['ws_name'].str[:3]

if 'Unnamed: 0' in df_total.columns:
    df_total = df_total.drop('Unnamed: 0', axis=1)

# === РАНЖИРОВАНИЕ И АГРЕГАЦИЯ ===

# 1. Создаем датафрейм с рангами внутри каждой группы origin по total_fee_per_window
df_ranked = df_total.copy()
df_ranked['rank'] = df_ranked.groupby('origin')['total_fee_per_window'].rank(method='min', ascending=False)
df_ranked = df_ranked.sort_values(['origin', 'rank'])

# 2. Агрегация по ws_name для разных показателей
df_ws_name_agg = df_ranked.groupby('ws_name').agg({
    'rank': 'mean',
    'count_window': 'mean',
    'total_fee_per_window': 'mean',
    'win_rate_window': 'mean'
}).reset_index()
df_ws_name_agg.columns = ['ws_name', 'avg_rank', 'avg_count_window', 'avg_total_fee_per_window', 'avg_win_rate_window']
df_ws_name_agg = df_ws_name_agg.sort_values('avg_rank')
df_ws_name_agg.reset_index(drop=True,inplace=True)

# 3. Агрегация по ws_type
df_ws_type_agg = df_ranked.groupby('ws_type').agg({
    'rank': 'mean',
    'count_window': 'mean',
    'total_fee_per_window': 'mean',
    'win_rate_window': 'mean'
}).reset_index()
df_ws_type_agg.columns = ['ws_type', 'avg_rank', 'avg_count_window', 'avg_total_fee_per_window', 'avg_win_rate_window']
df_ws_type_agg = df_ws_type_agg.sort_values('avg_rank')

# === НОВЫЕ АГРЕГАЦИИ ===

# 4. Агрегация по total_fee_per_window (сортировка по убыванию - чем выше, тем лучше)
df_total_fee_window_agg = df_ranked.groupby('ws_name').agg({
    'total_fee_per_window': 'mean',
    'count_window': 'mean',
    'win_rate_window': 'mean'
}).reset_index()
df_total_fee_window_agg.columns = ['ws_name', 'avg_total_fee_per_window', 'avg_count_window', 'avg_win_rate_window']
df_total_fee_window_agg = df_total_fee_window_agg.sort_values('avg_total_fee_per_window', ascending=False)
df_total_fee_window_agg.reset_index(drop=True,inplace=True)
# 5. Агрегация по diff_total_fee_per (минимальное отклонение - чем ближе к 0, тем лучше)
df_diff_fee_agg = df_ranked.groupby('ws_name').agg({
    'diff_total_fee_per': 'mean',
    'diff_count': 'mean',
    'diff_total': 'mean'
}).reset_index()

# Добавляем столбец с абсолютным значением для сортировки
df_diff_fee_agg['abs_diff_total_fee_per'] = df_diff_fee_agg['diff_total_fee_per'].abs()
df_diff_fee_agg = df_diff_fee_agg.sort_values('abs_diff_total_fee_per', ascending=True)
df_diff_fee_agg = df_diff_fee_agg.drop('abs_diff_total_fee_per', axis=1)
df_diff_fee_agg.columns = ['ws_name', 'avg_diff_total_fee_per', 'avg_diff_count', 'avg_diff_total']
df_diff_fee_agg.reset_index(drop=True,inplace=True)
# 6. То же самое, но по ws_type
df_total_fee_window_type_agg = df_ranked.groupby('ws_type').agg({
    'total_fee_per_window': 'mean',
    'count_window': 'mean',
    'win_rate_window': 'mean'
}).reset_index()
df_total_fee_window_type_agg.columns = ['ws_type', 'avg_total_fee_per_window', 'avg_count_window', 'avg_win_rate_window']
df_total_fee_window_type_agg = df_total_fee_window_type_agg.sort_values('avg_total_fee_per_window', ascending=False)

df_diff_fee_type_agg = df_ranked.groupby('ws_type').agg({
    'diff_total_fee_per': 'mean',
    'diff_count': 'mean',
    'diff_total': 'mean'
}).reset_index()
df_diff_fee_type_agg['abs_diff_total_fee_per'] = df_diff_fee_type_agg['diff_total_fee_per'].abs()
df_diff_fee_type_agg = df_diff_fee_type_agg.sort_values('abs_diff_total_fee_per', ascending=True)
df_diff_fee_type_agg = df_diff_fee_type_agg.drop('abs_diff_total_fee_per', axis=1)
df_diff_fee_type_agg.columns = ['ws_type', 'avg_diff_total_fee_per', 'avg_diff_count', 'avg_diff_total']

# === СОХРАНЕНИЕ В EXCEL ===

full_name_doc = os.path.join(main_folder, output_filename)
with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:
    
    # Основной лист
    df_total.to_excel(writer, sheet_name='total', index=True)
    worksheet = writer.sheets['total']
    workbook = writer.book
    
    # Настройка ширины для колонки индекса
    worksheet.set_column(0, 0, 10)
    
    # Настройка ширины для остальных колонок
    for i, col in enumerate(df_total.columns):
        col_idx = i + 1  # Исправлено: i + 1, так как колонка индекса - это 0
        width = max(df_total[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(col_idx, col_idx, width)
        worksheet.conditional_format(1, col_idx, len(df_total), col_idx, {
            'type': 'cell',
            'criteria': 'less than',
            'value': 0,
            'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        })
        worksheet.conditional_format(1, col_idx, len(df_total), col_idx, {
            'type': '3_color_scale',
            'min_color': '#DA9694',
            'mid_color': '#FFFFFF',
            'max_color': '#00B0F0'
        })
    
    # Лист с рангами
    df_ranked.to_excel(writer, sheet_name='ranked', index=True)
    worksheet_ranked = writer.sheets['ranked']
    worksheet_ranked.set_column(0, 0, 10)
    for i, col in enumerate(df_ranked.columns):
        col_idx = i + 1
        width = max(df_ranked[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_ranked.set_column(col_idx, col_idx, width)
    
    # Лист с агрегацией по ws_name (ранг)
    df_ws_name_agg.to_excel(writer, sheet_name='ws_name_agg', index=True)
    worksheet_name = writer.sheets['ws_name_agg']
    worksheet_name.set_column(0, 0, 10)
    for i, col in enumerate(df_ws_name_agg.columns):
        col_idx = i + 1
        width = max(df_ws_name_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_name.set_column(col_idx, col_idx, width)
    
    # Лист с агрегацией по ws_type (ранг)
    df_ws_type_agg.to_excel(writer, sheet_name='ws_type_agg', index=True)
    worksheet_type = writer.sheets['ws_type_agg']
    worksheet_type.set_column(0, 0, 10)
    for i, col in enumerate(df_ws_type_agg.columns):
        col_idx = i + 1
        width = max(df_ws_type_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_type.set_column(col_idx, col_idx, width)
    
    # НОВЫЙ ЛИСТ: Агрегация по total_fee_per_window (ws_name)
    df_total_fee_window_agg.to_excel(writer, sheet_name='fee_window_agg', index=True)
    worksheet_fee_window = writer.sheets['fee_window_agg']
    worksheet_fee_window.set_column(0, 0, 10)
    for i, col in enumerate(df_total_fee_window_agg.columns):
        col_idx = i + 1
        width = max(df_total_fee_window_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_fee_window.set_column(col_idx, col_idx, width)
    
    # НОВЫЙ ЛИСТ: Агрегация по total_fee_per_window (ws_type)
    df_total_fee_window_type_agg.to_excel(writer, sheet_name='fee_window_type_agg', index=True)
    worksheet_fee_window_type = writer.sheets['fee_window_type_agg']
    worksheet_fee_window_type.set_column(0, 0, 10)
    for i, col in enumerate(df_total_fee_window_type_agg.columns):
        col_idx = i + 1
        width = max(df_total_fee_window_type_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_fee_window_type.set_column(col_idx, col_idx, width)
    
    # НОВЫЙ ЛИСТ: Агрегация по diff_total_fee_per (ws_name) - минимальное отклонение
    df_diff_fee_agg.to_excel(writer, sheet_name='diff_fee_agg', index=True)
    worksheet_diff_fee = writer.sheets['diff_fee_agg']
    worksheet_diff_fee.set_column(0, 0, 10)
    for i, col in enumerate(df_diff_fee_agg.columns):
        col_idx = i + 1
        width = max(df_diff_fee_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_diff_fee.set_column(col_idx, col_idx, width)
    
    # НОВЫЙ ЛИСТ: Агрегация по diff_total_fee_per (ws_type) - минимальное отклонение
    df_diff_fee_type_agg.to_excel(writer, sheet_name='diff_fee_type_agg', index=True)
    worksheet_diff_fee_type = writer.sheets['diff_fee_type_agg']
    worksheet_diff_fee_type.set_column(0, 0, 10)
    for i, col in enumerate(df_diff_fee_type_agg.columns):
        col_idx = i + 1
        width = max(df_diff_fee_type_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_diff_fee_type.set_column(col_idx, col_idx, width)