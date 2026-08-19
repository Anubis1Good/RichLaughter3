from for_strategies.classic_indicators import *
from for_strategies.help_indicators import *
from for_strategies.ml_indicators import *
from for_strategies.other_indicators import *
from for_strategies.pva_indicators import *
from for_strategies.vsa_indicators import *
from for_strategies.zigzag_indicators import *

from utils.work_dfs.load_df import simple_load_df
from utils.drawing.chart import draw_bars_chart,draw_bars_chart_wo_vol
import matplotlib.pyplot as plt

filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'

df = simple_load_df(filepath)
df = df.iloc[-300:]

def add_wzz5p(df: pd.DataFrame, period=55):
    """ add 'wzp1''wzp2''wzp3''wzp4''wzp5' и их индексы \n
    создает 5 точек зигзага в окне
    Точки: 1 -> 2 -> 3 -> 4 -> 5
    где 3 и 4 - промежуточные экстремумы между 2 и 5
    """
    # Инициализация колонок
    cols = ['wzp1', 'wzp2', 'wzp3', 'wzp4', 'wzp5',
            'idx_wzp1', 'idx_wzp2', 'idx_wzp3', 'idx_wzp4', 'idx_wzp5']
    df[cols] = np.nan
    
    for i in range(period, len(df)):
        start_pos = i - period
        slice1 = df.iloc[start_pos:i]
        
        # Находим экстремумы в первом окне
        idx_h1 = slice1['high'].idxmax()
        idx_l1 = slice1['low'].idxmin()
        
        pos_h1 = df.index.get_loc(idx_h1)
        pos_l1 = df.index.get_loc(idx_l1)
        
        # Определяем паттерн для первых двух точек
        if pos_h1 > pos_l1 or (pos_h1 == pos_l1 and slice1.loc[idx_h1, 'direction'] == 1):
            # Паттерн "рост": l1 -> h1 -> ... -> l2
            first_idx, first_val = idx_l1, slice1.loc[idx_l1, 'low']
            second_idx, second_val = idx_h1, slice1.loc[idx_h1, 'high']
            pos_second = pos_h1
            is_up = True
        else:
            # Паттерн "падение": h1 -> l1 -> ... -> h2
            first_idx, first_val = idx_h1, slice1.loc[idx_h1, 'high']
            second_idx, second_val = idx_l1, slice1.loc[idx_l1, 'low']
            pos_second = pos_l1
            is_up = False
        
        # Сохраняем первые две точки
        df.loc[df.index[i], ['idx_wzp1', 'wzp1']] = first_idx, first_val
        df.loc[df.index[i], ['idx_wzp2', 'wzp2']] = second_idx, second_val
        
        # Ищем пятую точку (последний экстремум)
        if pos_second + 1 < len(df):
            slice_last = df.iloc[pos_second + 1:i + 1]
            if len(slice_last) > 0:
                if is_up:
                    # Для роста ищем минимум после максимума (точка 5)
                    fifth_idx = slice_last['low'].idxmin()
                    fifth_val = slice_last.loc[fifth_idx, 'low']
                else:
                    # Для падения ищем максимум после минимума (точка 5)
                    fifth_idx = slice_last['high'].idxmax()
                    fifth_val = slice_last.loc[fifth_idx, 'high']
                
                pos_fifth = df.index.get_loc(fifth_idx)
                
                # Сохраняем пятую точку
                df.loc[df.index[i], ['idx_wzp5', 'wzp5']] = fifth_idx, fifth_val
                
                # Теперь ищем точки 3 и 4 между точкой 2 и точкой 5
                if pos_second + 1 < pos_fifth:
                    # Разделяем промежуток между точкой 2 и точкой 5 пополам
                    mid_pos = (pos_second + pos_fifth) // 2
                    
                    # Первая половина: от точки 2 до середины
                    slice3 = df.iloc[pos_second + 1:mid_pos + 1]
                    if len(slice3) > 0:
                        if is_up:
                            # После максимума ищем минимум (точка 3)
                            third_idx = slice3['low'].idxmin()
                            third_val = slice3.loc[third_idx, 'low']
                        else:
                            # После минимума ищем максимум (точка 3)
                            third_idx = slice3['high'].idxmax()
                            third_val = slice3.loc[third_idx, 'high']
                        
                        df.loc[df.index[i], ['idx_wzp3', 'wzp3']] = third_idx, third_val
                    
                    # Вторая половина: от середины до точки 5
                    slice4 = df.iloc[mid_pos + 1:pos_fifth + 1]
                    if len(slice4) > 0:
                        if is_up:
                            # Ищем максимум перед минимумом (точка 4)
                            fourth_idx = slice4['high'].idxmax()
                            fourth_val = slice4.loc[fourth_idx, 'high']
                        else:
                            # Ищем минимум перед максимумом (точка 4)
                            fourth_idx = slice4['low'].idxmin()
                            fourth_val = slice4.loc[fourth_idx, 'low']
                        
                        df.loc[df.index[i], ['idx_wzp4', 'wzp4']] = fourth_idx, fourth_val
    
    # Приводим индексы к Int64
    idx_cols = ['idx_wzp1', 'idx_wzp2', 'idx_wzp3', 'idx_wzp4', 'idx_wzp5']
    df[idx_cols] = df[idx_cols].astype('Int64')
    
    return df
        
df = add_wzz5p(df)
print(df.tail(20))
fig = draw_bars_chart_wo_vol(df)

# plt.plot(df['wzp1'])
# plt.plot(df['wzp2'])
# plt.plot(df['wzp3'])
# plt.plot(df['wzp4'])
# draw_wzp(df)
plt.show()