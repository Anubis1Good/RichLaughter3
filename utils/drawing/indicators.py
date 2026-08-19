import matplotlib.pyplot as plt
import pandas as pd

def draw_wzp(df:pd.DataFrame,wzp=5,color='black',ax=None):
    if ax is not None:
        _plt = ax
    else:
        _plt = plt
    last_row = df.iloc[-1]
    
# Собираем точки
    points = []
    for i in range(1, wzp+1):
        idx_col = f'idx_wzp{i}'
        val_col = f'wzp{i}'
        if not pd.isna(last_row[idx_col]):
            points.append((int(last_row[idx_col]), last_row[val_col]))

    # Добавляем текущую цену
    # points.append((df.index.values[-1], last_row['close']))
    # print(points)
    # Сортируем по позиции
    points = sorted(points, key=lambda x: x[0])
    if len(points) > 1:
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        _plt.plot(x, y, 'r-o', linewidth=2.5, markersize=8, label='Zigzag',color=color)
        
        # Подписи
        for i, (x_val, y_val) in enumerate(zip(x, y)):
            _plt.annotate(f'{i+1}', (x_val, y_val), xytext=(5, 5), 
                        textcoords='offset points', fontsize=10, fontweight='bold',color=color)