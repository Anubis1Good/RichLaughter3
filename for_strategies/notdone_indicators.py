import pandas as pd
import numpy as np

def find_point_by_price(df, start_pos, end_pos, base_price, threshold, direction):
    """
    Ищет точку, где цена отклонилась от base_price на threshold процентов
    direction: 'up' - ищем high, 'down' - ищем low
    Возвращает позицию, цену, индекс и направление
    """
    for pos in range(end_pos - 1, start_pos - 1, -1):
        if direction == 'up':
            # Ищем high, который превысил base_price на threshold%
            high_price = df.iloc[pos, df.columns.get_loc('high')]
            if (high_price - base_price) / base_price * 100 > threshold:
                return pos, high_price, df.index[pos], direction
        else:  # direction == 'down'
            # Ищем low, который упал ниже base_price на threshold%
            low_price = df.iloc[pos, df.columns.get_loc('low')]
            if (base_price - low_price) / base_price * 100 > threshold:
                return pos, low_price, df.index[pos], direction
    
    return None, None, None, None

def add_some(df: pd.DataFrame, percent_threshold=0.3, period=55):
    cols = ['wzp1', 'wzp2', 'wzp3', 'wzp4', 
            'idx_wzp1', 'idx_wzp2', 'idx_wzp3', 'idx_wzp4',
            'dir_wzp1', 'dir_wzp2', 'dir_wzp3']
    df[cols] = np.nan
    df['diff_pct'] = df['close'].pct_change() * 100
    
    for i in range(period, len(df)):
        # wzp4 - текущая цена (close)
        current_close = df.iloc[i, df.columns.get_loc('close')]
        df.iloc[i, df.columns.get_loc('wzp4')] = current_close
        df.iloc[i, df.columns.get_loc('idx_wzp4')] = df.index[i]
        
        # 1. Находим wzp3 - первую точку, где накопление diff_pct превысило порог
        total = 0
        found_wzp3 = False
        pos3 = None
        price3 = None
        idx3 = None
        direction3 = None
        
        for pos in range(i - 1, i - period - 1, -1):
            total += df.iloc[pos, df.columns.get_loc('diff_pct')]
            
            if total > percent_threshold:
                # Точка вверх - берем high
                pos3 = pos
                price3 = df.iloc[pos, df.columns.get_loc('high')]
                idx3 = df.index[pos]
                direction3 = 'up'
                found_wzp3 = True
                break
            elif total < -percent_threshold:
                # Точка вниз - берем low
                pos3 = pos
                price3 = df.iloc[pos, df.columns.get_loc('low')]
                idx3 = df.index[pos]
                direction3 = 'down'
                found_wzp3 = True
                break
        
        if not found_wzp3:
            continue
        
        df.iloc[i, df.columns.get_loc('wzp3')] = price3
        df.iloc[i, df.columns.get_loc('idx_wzp3')] = idx3
        df.iloc[i, df.columns.get_loc('dir_wzp3')] = direction3
        
        # 2. Ищем wzp2 - от цены wzp3 до high/low (противоположное направление)
        # Если wzp3 была вверх (high), то ищем вниз (low) и наоборот
        opposite_direction = 'down' if direction3 == 'up' else 'up'
        
        pos2, price2, idx2, direction2 = find_point_by_price(df,
            i - period, pos3, price3, percent_threshold, opposite_direction
        )
        
        if pos2 is None:
            continue
        
        df.iloc[i, df.columns.get_loc('wzp2')] = price2
        df.iloc[i, df.columns.get_loc('idx_wzp2')] = idx2
        df.iloc[i, df.columns.get_loc('dir_wzp2')] = direction2
        
        # 3. Ищем wzp1 - от цены wzp2 до high/low (снова противоположное направление)
        opposite_direction2 = 'down' if direction2 == 'up' else 'up'
        
        pos1, price1, idx1, direction1 = find_point_by_price(df,
            i - period, pos2, price2, percent_threshold, opposite_direction2
        )
        
        if pos1 is None:
            continue
        
        df.iloc[i, df.columns.get_loc('wzp1')] = price1
        df.iloc[i, df.columns.get_loc('idx_wzp1')] = idx1
        df.iloc[i, df.columns.get_loc('dir_wzp1')] = direction1
    
    return df