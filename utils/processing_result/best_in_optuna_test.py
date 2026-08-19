import os
import pandas as pd
from tqdm import tqdm

main_folder = '_test_results\optuna'
ignore_folders = ('archive',)
amount_var = 1
inner_folders = os.listdir(main_folder)
df_total = pd.DataFrame()
for inner_folder in tqdm(inner_folders):
    inner_folder_path = os.path.join(main_folder,inner_folder)
    if inner_folder in ignore_folders or not os.path.isdir(inner_folder_path):
        continue
    variant_folders = os.listdir(inner_folder_path)
    for variant_folder in variant_folders:
        variant_folder_path = os.path.join(inner_folder_path,variant_folder)
        if not os.path.isdir(variant_folder_path):
            continue
        files = os.listdir(variant_folder_path)
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(variant_folder_path,file)
                df_file = pd.read_excel(file_path,'total')
                if not df_file.empty:
                    if df_total.empty:
                        df_total = df_file.head(amount_var)
                    else:
                        df_total = pd.concat([df_total,df_file.head(amount_var)])
# Переставляем 'origin' в начало
cols = df_total.columns.tolist()
cols.remove('origin')
cols = ['origin'] + cols
df_total = df_total[cols]
df_total = df_total.sort_values(['origin', 'total_abs_fee'], ascending=[True, False])
df_total = df_total.reset_index(drop=True)
df_total['ws_name'] = df_total['ws'].str.extract(r'^\(?([^,(]+)')
df_total['ws_type'] = df_total['ws_name'].str[:3]
if 'Unnamed: 0' in df_total.columns:
    df_total = df_total.drop('Unnamed: 0',axis=1)

# === НОВЫЙ КОД ДЛЯ РАНЖИРОВАНИЯ И АГРЕГАЦИИ ===

# 1. Создаем датафрейм с рангами внутри каждой группы origin
df_ranked = df_total.copy()
df_ranked['rank'] = df_ranked.groupby('origin')['total_abs_fee'].rank(method='min', ascending=False)
df_ranked = df_ranked.sort_values(['origin', 'rank'])

# 2. Агрегация по ws_name
df_ws_name_agg = df_ranked.groupby('ws_name').agg({
    'rank': 'mean',
    'count': 'mean',
    'total_fee_per': 'mean',
    'win_rate_wf': 'mean'
}).reset_index()
df_ws_name_agg.columns = ['ws_name', 'avg_rank', 'avg_count', 'avg_total_fee_per', 'avg_win_rate_wf']
df_ws_name_agg = df_ws_name_agg.sort_values('avg_rank')

# 3. Агрегация по ws_type
df_ws_type_agg = df_ranked.groupby('ws_type').agg({
    'rank': 'mean',
    'count': 'mean',
    'total_fee_per': 'mean',
    'win_rate_wf': 'mean'
}).reset_index()
df_ws_type_agg.columns = ['ws_type', 'avg_rank', 'avg_count', 'avg_total_fee_per', 'avg_win_rate_wf']
df_ws_type_agg = df_ws_type_agg.sort_values('avg_rank')

# === КОНЕЦ НОВОГО КОДА ===

full_name_doc = os.path.join(main_folder, 'total_optuna' + '.xlsx')
with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:  
    # Основной лист
    df_total.to_excel(writer, sheet_name='total', index=False)
    worksheet = writer.sheets['total']
    workbook = writer.book
    for i, col in enumerate(df_total.columns,start=1):
        width = max(df_total[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet.set_column(i, i, width)
        worksheet.conditional_format(1, i, len(df_total), i, {
            'type': 'cell',
            'criteria': 'less than',
            'value': 0,
            'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        })
        worksheet.conditional_format(1, i, len(df_total), i, {
            'type': '3_color_scale',
            'min_color': '#DA9694',
            'mid_color': '#FFFFFF',
            'max_color': '#00B0F0'
        })
    
    # Лист с рангами
    df_ranked.to_excel(writer, sheet_name='ranked', index=False)
    worksheet_ranked = writer.sheets['ranked']
    for i, col in enumerate(df_ranked.columns, start=1):
        width = max(df_ranked[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_ranked.set_column(i, i, width)
    
    # Лист с агрегацией по ws_name
    df_ws_name_agg.to_excel(writer, sheet_name='ws_name_agg', index=False)
    worksheet_name = writer.sheets['ws_name_agg']
    for i, col in enumerate(df_ws_name_agg.columns, start=1):
        width = max(df_ws_name_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_name.set_column(i, i, width)
    
    # Лист с агрегацией по ws_type
    df_ws_type_agg.to_excel(writer, sheet_name='ws_type_agg', index=False)
    worksheet_type = writer.sheets['ws_type_agg']
    for i, col in enumerate(df_ws_type_agg.columns, start=1):
        width = max(df_ws_type_agg[col].apply(lambda x: len(str(x))).max(), len(col))
        worksheet_type.set_column(i, i, width)