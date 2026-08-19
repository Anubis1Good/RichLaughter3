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
from utils.drawing.indicators import draw_wzp
# Начальные параметры окна
window = 60
START = 60
END = START + window
WINDOW_SIZE = END - START
# COLUMNS = ['zigzag']  # <--- СПИСОК КОЛОНОК
COLUMNS = []  # <--- СПИСОК КОЛОНОК
draw_chart = True
# draw_chart = False

# ===== НАСТРОЙКА ЦВЕТОВ =====
# Для DF1 (полный расчет) - пунктирные линии
COLORS_DF1 = ['blue', 'green']  # для zigzag и zigzag_peaks соответственно

# Для DF2 (расчет на окне) - сплошные линии
COLORS_DF2 = ['red', 'orange']  # для zigzag и zigzag_peaks соответственно
# =================================

# ===== ФУНКЦИЯ 1: Обработка датафрейма =====
def preprocessing(df):
    """Добавляем индикаторы в датафрейм"""
    df = df.copy()
    # df = add_zigzag180826(df, 1.5)
    df = add_wzz5p(df)
    # df = add_percent_zz190826(df,percent_threshold=0.5,drop_last=False)
    # df['zigzag_peaks'] = df['zigzag_peaks'].shift(1)
    # df = add_pattern18_dzz_czd(df)
    return df
# ===== ФУНКЦИЯ ДЛЯ РИСОВАНИЯ ГРАФИКА =====
def draw_hb_chart_fast_on_ax(ax, df):
    """
    Рисует график на переданной оси
    """
    # Проверяем наличие необходимых колонок
    if not all(col in df.columns for col in ['direction', 'low', 'high']):
        print("Предупреждение: В датафрейме нет колонок direction, low, high")
        return
    
    # Разделяем данные по направлениям
    longs = df[df['direction'] == 1]
    shorts = df[df['direction'] != 1]
    
    # Рисуем все линии за один вызов для каждого направления
    ax.vlines(longs.index, longs['low'], longs['high'], colors='#b7ea00', linewidth=2, label='Long')
    ax.vlines(shorts.index, shorts['low'], shorts['high'], colors='#ff0013', linewidth=2, label='Short')


# ===== ФУНКЦИЯ 2: Отрисовка =====
def create_figure(df1, df2, start_idx, end_idx, columns=['rsi'], 
                  colors_df1=None, colors_df2=None, show_chart=True):
    """
    Создает фигуру с одним графиком, где наложены: график и индикаторы
    """
    # Проверка цветов
    if colors_df1 is None:
        colors_df1 = ['blue'] * len(columns)
    if colors_df2 is None:
        colors_df2 = ['red'] * len(columns)
    
    if isinstance(colors_df1, str):
        colors_df1 = [colors_df1] * len(columns)
    if isinstance(colors_df2, str):
        colors_df2 = [colors_df2] * len(columns)
    
    # Получаем срезы данных
    slice1 = df1.iloc[start_idx:end_idx]
    slice2 = df2
    
    # Выводим информацию о срезах
    print("="*50)
    print(f"СОЗДАНИЕ ГРАФИКА: {start_idx}-{end_idx}")
    print("-"*50)
    print("DF1 (полный расчет) - последние 5 строк:")
    print(slice1.tail())
    print("-"*50)
    print("DF2 (расчет на окне) - последние 5 строк:")
    print(slice2.tail())
    print("="*50)
    
    # Создаем фигуру с одним графиком
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # === Рисуем график ===
    if show_chart:
        draw_hb_chart_fast_on_ax(ax, slice1)
    # draw_wzp(slice1,color='blue',ax=ax)
    # draw_wzp(slice2,ax=ax)
    # === Рисуем индикаторы поверх графика ===
    # График DF1 (пунктирные линии)
    for i, col in enumerate(columns):
        if i < len(colors_df1):
            color = colors_df1[i]
        else:
            color = colors_df1[-1]
        ax.plot(slice1.index, slice1[col], linewidth=2, 
                label=f'DF1 (полный) - {col}', 
                color=color, alpha=0.7, linestyle='--')
    
    # График DF2 (сплошные линии)
    for i, col in enumerate(columns):
        if i < len(colors_df2):
            color = colors_df2[i]
        else:
            color = colors_df2[-1]
        ax.plot(slice2.index, slice2[col], linewidth=2, 
                label=f'DF2 (окно) - {col}', 
                color=color, alpha=0.7, linestyle='-')
    
    # Настройка графика
    ax.set_title(f'График и индикаторы: {start_idx}-{end_idx}')
    ax.set_ylabel('Значение')
    ax.set_xlabel('Индекс')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    # Выравниваем Y для всего графика
    all_values = []
    for col in columns:
        all_values.extend(slice1[col].values)
        all_values.extend(slice2[col].values)
    
    # Добавляем значения high/low для масштабирования
    if 'high' in slice1.columns and 'low' in slice1.columns:
        all_values.extend(slice1['high'].values)
        all_values.extend(slice1['low'].values)
    
    # Убираем NaN значения
    all_values = [v for v in all_values if not np.isnan(v)]
    
    if all_values:
        y_min = min(all_values)
        y_max = max(all_values)
        y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
        ax.set_ylim(y_min - y_padding, y_max + y_padding)
    
    plt.tight_layout()
    return fig, ax

# ===== ОСНОВНОЙ КОД С КНОПКАМИ =====

# Загружаем данные
filepath = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'
df = simple_load_df(filepath)

# 1. Обрабатываем ВЕСЬ датафрейм
df_full = preprocessing(df)

# Берем срез
df_slice = df.iloc[START:END].copy()
df_slice_processed = preprocessing(df_slice)

# Создаем фигуру с графиками
fig, ax = create_figure(
    df1=df_full,
    df2=df_slice_processed,
    start_idx=START,
    end_idx=END,
    columns=COLUMNS,
    colors_df1=COLORS_DF1,
    colors_df2=COLORS_DF2,
    show_chart=draw_chart
)

# Добавляем кнопки
ax_left = plt.axes([0.3, 0.02, 0.1, 0.04])
ax_right = plt.axes([0.6, 0.02, 0.1, 0.04])

btn_left = Button(ax_left, '<< Назад')
btn_right = Button(ax_right, 'Вперед >>')

# Функция обновления
def update_plot(new_start):
    global START, df_slice_processed, fig, ax
    
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
    
    # Получаем срезы данных
    slice1 = df_full.iloc[START:END]
    slice2 = df_slice_processed
    
    # Выводим информацию о срезах
    print("="*50)
    print(f"ОБНОВЛЕНИЕ ГРАФИКА: {START}-{END}")
    print("-"*50)
    print("DF1 (полный расчет) - последние 5 строк:")
    print(slice1.tail())
    print("-"*50)
    print("DF2 (расчет на окне) - последние 5 строк:")
    print(slice2.tail())
    print("="*50)
    
    # Очищаем график
    ax.clear()
    
    # === Рисуем график ===
    if draw_chart:
        draw_hb_chart_fast_on_ax(ax, slice1)
    # draw_wzp(slice1,color='blue',ax=ax)
    # draw_wzp(slice2,ax=ax)
    # === Рисуем индикаторы поверх графика ===
    # График DF1 (пунктирные линии)
    for i, col in enumerate(COLUMNS):
        if i < len(COLORS_DF1):
            color = COLORS_DF1[i]
        else:
            color = COLORS_DF1[-1]
        ax.plot(slice1.index, slice1[col], linewidth=2, 
                label=f'DF1 (полный) - {col}', 
                color=color, alpha=0.7, linestyle='--')
    
    # График DF2 (сплошные линии)
    for i, col in enumerate(COLUMNS):
        if i < len(COLORS_DF2):
            color = COLORS_DF2[i]
        else:
            color = COLORS_DF2[-1]
        ax.plot(slice2.index, slice2[col], linewidth=2, 
                label=f'DF2 (окно) - {col}', 
                color=color, alpha=0.7, linestyle='-')
    
    # Настройка графика
    ax.set_title(f'График и индикаторы: {START}-{END}')
    ax.set_ylabel('Значение')
    ax.set_xlabel('Индекс')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    # Выравниваем Y для всего графика
    all_values = []
    for col in COLUMNS:
        all_values.extend(slice1[col].values)
        all_values.extend(slice2[col].values)
    
    # Добавляем значения high/low для масштабирования
    if 'high' in slice1.columns and 'low' in slice1.columns:
        all_values.extend(slice1['high'].values)
        all_values.extend(slice1['low'].values)
    
    # Убираем NaN значения
    all_values = [v for v in all_values if not np.isnan(v)]
    
    if all_values:
        y_min = min(all_values)
        y_max = max(all_values)
        y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1.0
        ax.set_ylim(y_min - y_padding, y_max + y_padding)
    
    # Обновляем фигуру
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