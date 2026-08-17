from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *

from utils.work_dfs.load_df import simple_load_df

filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'

df = simple_load_df(filepath)
df = df.iloc[-300:]
df = add_fractals(df)
df = add_rsi(df)
# def get_fractals_in_window(df, window=55):
#     """
#     Для каждой строки находит все верхние фракталы в окне [i-window, i]
#     Возвращает список значений 'x' фракталов, где x <= last_confirmed_up_x
#     """
#     df = df.copy()
    
#     # Получаем все подтвержденные фракталы
#     # Фрактал считается подтвержденным, если его x <= last_confirmed_up_x
#     # Но last_confirmed_up_x это значение x последнего подтвержденного фрактала
#     # Нам нужны все фракталы, у которых x <= last_confirmed_up_x
    
#     # Создаем список для хранения результатов
#     fractals_by_row = []
    
#     # Получаем все индексы где fractal_up == True и их значения x
#     up_fractals = df[df['fractal_up'] == True][['x']].copy()
#     up_indices = up_fractals.index.tolist()
#     up_x_values = up_fractals['x'].tolist()
    
#     # Для каждой строки
#     for i, idx in enumerate(df.index):
#         start_idx = max(df.index[0], idx - window)
#         last_confirmed = df.loc[idx, 'last_confirmed_up_x']
        
#         # Собираем значения x фракталов
#         fractals_x = []
#         for j, f_idx in enumerate(up_indices):
#             if start_idx <= f_idx <= idx:
#                 f_x = up_x_values[j]
#                 # Проверяем, что фрактал подтвержден (x <= last_confirmed)
#                 if not pd.isna(last_confirmed) and f_x <= last_confirmed:
#                     fractals_x.append(f_x)
#                 elif pd.isna(last_confirmed):
#                     # Если last_confirmed нет (начало данных), берем только если f_x <= idx
#                     fractals_x.append(f_x)
        
#         fractals_by_row.append(fractals_x)
    
#     # Присваиваем все сразу
#     df['up_fractals_x_in_window'] = fractals_by_row
    
#     return df
# df = get_fractals_in_window(df, 55)

df = add_mean_on_fractals(df,max_period=10)

print(df.tail(30))