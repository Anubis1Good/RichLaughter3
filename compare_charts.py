import matplotlib.pyplot as plt
from matplotlib.widgets import Button
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

# ===== ФУНКЦИЯ 1: Обработка датафрейма =====
def preprocessing(df):
    """Добавляем индикаторы в датафрейм"""
    df = df.copy()
    df = add_supertrend(df)
    
    # Работаем с numpy массивами для максимальной скорости
    in_uptrend = df['in_uptrend'].fillna(False).values
    
    # Создаем массив сигналов
    signals = np.zeros(len(df), dtype=np.int8)
    
    # Векторизованная логика
    # Сигнал покупки: текущий True, предыдущий False
    buy_mask = (in_uptrend[1:] == True) & (in_uptrend[:-1] == False)
    signals[1:][buy_mask] = 1
    
    # Сигнал продажи: текущий False, предыдущий True
    sell_mask = (in_uptrend[1:] == False) & (in_uptrend[:-1] == True)
    signals[1:][sell_mask] = -1
    
    df['signal'] = signals
    
    return df

# ===== ФУНКЦИЯ 2: Отрисовка =====
def plot_comparison(df1, df2, start_idx, end_idx, columns=['rsi']):
    """
    Отрисовывает сравнение двух датафреймов на одном срезе
    Верхний график - из первого датафрейма
    Нижний график - из второго датафрейма
    columns - список колонок для отображения
    """
    slice1 = df1.iloc[start_idx:end_idx]
    slice2 = df2
    print(slice1.tail())
    print(slice2.tail())
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    
    # Верхний график - все колонки из первого датафрейма
    for col in columns:
        ax1.plot(range(len(slice1)), slice1[col], linewidth=2, label=col)
    ax1.set_title(f'DF1 - полный расчет')
    ax1.set_ylabel('Значение')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Нижний график - все колонки из второго датафрейма
    for col in columns:
        ax2.plot(range(len(slice2)), slice2[col], linewidth=2, label=col)
    ax2.set_title(f'DF2 - расчет на окне')
    ax2.set_ylabel('Значение')
    ax2.set_xlabel('Индекс')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Выравниваем Y для каждого графика отдельно
    y_min1 = min([slice1[col].min() for col in columns])
    y_max1 = max([slice1[col].max() for col in columns])
    y_padding1 = (y_max1 - y_min1) * 0.1
    ax1.set_ylim(y_min1 - y_padding1, y_max1 + y_padding1)
    
    y_min2 = min([slice2[col].min() for col in columns])
    y_max2 = max([slice2[col].max() for col in columns])
    y_padding2 = (y_max2 - y_min2) * 0.1
    ax2.set_ylim(y_min2 - y_padding2, y_max2 + y_padding2)
    
    plt.tight_layout()
    return fig, ax1, ax2

# ===== ОСНОВНОЙ КОД С КНОПКАМИ =====

# Загружаем данные
filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'
df = simple_load_df(filepath)

# 1. Обрабатываем ВЕСЬ датафрейм
df_full = preprocessing(df)

# Начальные параметры окна
window = 60
# window = 120
START = 60
START = 5031
END = START + window
WINDOW_SIZE = END - START
# COLUMNS = ['top_mean', 'bottom_mean']  # <--- СПИСОК КОЛОНОК
COLUMNS = ['signal']  # <--- СПИСОК КОЛОНОК

# Берем срез
df_slice = df.iloc[START:END].copy()
df_slice_processed = preprocessing(df_slice)

# Создаем фигуру с графиками
fig, ax1, ax2 = plot_comparison(
    df1=df_full,
    df2=df_slice_processed,
    start_idx=START,
    end_idx=END,
    columns=COLUMNS
)

# Добавляем кнопки
ax_left = plt.axes([0.3, 0.02, 0.1, 0.04])
ax_right = plt.axes([0.6, 0.02, 0.1, 0.04])

btn_left = Button(ax_left, '<< Назад')
btn_right = Button(ax_right, 'Вперед >>')

# Функция обновления
def update_plot(new_start):
    global START, df_slice_processed
    
    # Проверяем границы
    if new_start < 0:
        new_start = 0
    if new_start + WINDOW_SIZE > len(df):
        new_start = len(df) - WINDOW_SIZE
    
    START = new_start
    END = START + WINDOW_SIZE
    
    # Берем новый срез и обрабатываем
    df_slice = df.iloc[START:END].copy()
    df_slice_processed = preprocessing(df_slice)
    
    # Обновляем данные на графиках
    slice1 = df_full.iloc[START:END]
    slice2 = df_slice_processed
    
    # Очищаем и перерисовываем
    ax1.clear()
    ax2.clear()
    
    # Верхний график
    for col in COLUMNS:
        ax1.plot(range(len(slice1)), slice1[col], linewidth=2, label=col)
    ax1.set_title(f'DF1 - полный расчет  Окно: {START}-{END}')
    ax1.set_ylabel('Значение')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Нижний график
    for col in COLUMNS:
        ax2.plot(range(len(slice2)), slice2[col], linewidth=2, label=col)
    ax2.set_title(f'DF2 - расчет на окне  Окно: {START}-{END}')
    ax2.set_ylabel('Значение')
    ax2.set_xlabel('Индекс')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Выравниваем Y для каждого графика отдельно
    y_min1 = min([slice1[col].min() for col in COLUMNS])
    y_max1 = max([slice1[col].max() for col in COLUMNS])
    y_padding1 = (y_max1 - y_min1) * 0.1
    ax1.set_ylim(y_min1 - y_padding1, y_max1 + y_padding1)
    
    y_min2 = min([slice2[col].min() for col in COLUMNS])
    y_max2 = max([slice2[col].max() for col in COLUMNS])
    y_padding2 = (y_max2 - y_min2) * 0.1
    ax2.set_ylim(y_min2 - y_padding2, y_max2 + y_padding2)
    
    fig.canvas.draw_idle()

# Обработчики кнопок
def on_left_click(event):
    update_plot(START - 1)

def on_right_click(event):
    update_plot(START + 1)

btn_left.on_clicked(on_left_click)
btn_right.on_clicked(on_right_click)

# Навигация с клавиатуры
def on_key(event):
    if event.key == 'left':
        update_plot(START - 1)
    elif event.key == 'right':
        update_plot(START + 1)

fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()