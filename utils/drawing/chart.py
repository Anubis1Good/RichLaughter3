import matplotlib.pyplot as plt
import pandas as pd

def draw_hb_chart_fast(df):
    # Разделяем данные по направлениям
    longs = df[df['direction'] == 1]
    shorts = df[df['direction'] != 1]
    
    # Рисуем все линии за один вызов для каждого направления
    plt.vlines(longs.index, longs['low'], longs['high'], colors='#b7ea00')
    plt.vlines(shorts.index, shorts['low'], shorts['high'], colors='#ff0013')

def draw_bars_chart(df):
    fig, (ax_price, ax_volume) = plt.subplots(2, 1, figsize=(12, 8))
    longs = df[df['direction'] == 1]
    shorts = df[df['direction'] != 1]
    
    tick_width = 1.5
    longs_index = longs['x']
    short_index = shorts['x']

    # tick_width = 0.3
    # longs_index = longs.index
    # short_index = shorts.index
        # Рисуем вертикальные линии (high-low)
    ax_price.vlines(longs_index, longs['low'], longs['high'], 
                    colors='#b7ea00', linewidth=1.5)
    ax_price.vlines(short_index, shorts['low'], shorts['high'], 
                    colors='#ff0013', linewidth=1.5)
    ax_price.hlines(longs['open'], 
                    longs_index - tick_width,
                    longs_index, 
                    colors='#b7ea00', linewidth=2)
    ax_price.hlines(shorts['open'], 
                    short_index - tick_width,
                    short_index, 
                    colors='#ff0013', linewidth=2)
    ax_price.hlines(longs['close'], 
                    longs_index, 
                    longs_index + tick_width,
                    colors='#b7ea00', linewidth=2)
    ax_price.hlines(shorts['close'], 
                    short_index, 
                    short_index + tick_width,
                    colors='#ff0013', linewidth=2)
    ax_price.grid(True, alpha=0.3)
    ax_volume.vlines(longs_index, 0, longs['volume'], 
                    colors='#b7ea00', linewidth=1.5)
    ax_volume.vlines(short_index, 0, shorts['volume'], 
                    colors='#ff0013', linewidth=1.5)
    ax_volume.grid(True, alpha=0.3)
    ax_price.autoscale_view()
    ax_volume.autoscale_view()
    plt.subplots_adjust(hspace=0)
    plt.tight_layout()
    fig.canvas.draw()
    return fig