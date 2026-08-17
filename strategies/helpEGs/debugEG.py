import numpy as np
import pandas as pd
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_rsi_tw,add_williams_r,add_mfi,add_ultimate_oscillator,add_cmo,add_cci,add_stochastic,add_roc,add_fractals,add_bollinger,add_chop,add_supertrend,add_ema
from for_strategies.pva_indicators import add_integrity_index,add_mean_on_fractals,add_average_fractals,add_ext_on_fractals
from for_strategies.vsa_indicators import add_dvsai,add_cdvsai

class debugEG(BaseEG):
    """stop=None, take=None, period=15, period_fractal=10,period_winmean=55
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=15, period_fractal=10,period_winmean=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period_fractal = period_fractal
        self.period_winmean = period_winmean

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_fractals(df, self.period_fractal,self.period_winmean)
        df['new_up_fractal'] = (df['last_confirmed_up_x'] != df['last_confirmed_up_x'].shift(1)) & df['last_confirmed_up_x'].notna()
        df['new_down_fractal'] = (df['last_confirmed_down_x'] != df['last_confirmed_down_x'].shift(1)) & df['last_confirmed_down_x'].notna()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['new_up_fractal']:
                return 'open_short'
        if row['new_down_fractal']:
                return 'open_long'
        
class DebugMean(BaseEG):
    """Дебажная стратегия для проверки add_mean_on_fractals"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, 
                 period=15, period_fractal=10, period_mean=5, kind='rsi', max_period_for_mean=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.kind = kind
        self.period_fractal = period_fractal
        self.period_mean = period_mean
        self.max_period_for_mean = max_period_for_mean
        
        # Для сбора данных
        self.debug_data = []

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        
        # Добавляем индикатор (как в LEG1_BIBI)
        if self.kind == 'rsi':
            df = add_rsi(df, self.period)
        # ... добавь другие варианты если нужно (cmo, williams_r и т.д.)
        
        # Добавляем фракталы
        df = add_fractals(df, self.period_fractal, self.max_period_for_mean)
        
        # Добавляем средние по фракталам
        df = add_mean_on_fractals(df, self.period_mean, self.kind, self.max_period_for_mean)
        
        # Обрезаем
        df = self.add_slice_df(df)
        
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # Сохраняем значения для дебага
        self.debug_data.append({
            'x': row['x'],
            'kind': row[self.kind],
            'top_mean': row['top_mean'],
            'bottom_mean': row['bottom_mean'],
            'last_confirmed_up_x': row['last_confirmed_up_x'],
            'last_confirmed_down_x': row['last_confirmed_down_x']
        })
        
        # НЕ ТОРГУЕМ
        return None
    
    def print_debug(self):
        """Печатает последние 20 значений для сравнения"""
        print("\n=== ДЕБАГ: ПОСЛЕДНИЕ 20 ЗНАЧЕНИЙ ===")
        print(f"{'x':>6} | {'kind':>8} | {'top_mean':>10} | {'bottom_mean':>12} | {'last_up_x':>10} | {'last_down_x':>12}")
        print("-" * 75)
        for d in self.debug_data[-20:]:
            print(f"{d['x']:>6} | {d['kind']:>8.2f} | {d['top_mean']:>10.2f} | {d['bottom_mean']:>12.2f} | {d['last_confirmed_up_x']:>10} | {d['last_confirmed_down_x']:>12}")

    def save_to_csv(self, filename="debug_actions.csv"):
        """Сохраняет все данные в CSV файл"""
        df_log = pd.DataFrame(self.debug_data)
        df_log.to_csv(filename, index=False)
        print(f"Сохранено {len(df_log)} записей в {filename}")


import pandas as pd
import os

class DebugAction(BaseEG):
    """Дебажная стратегия для записи ВСЕХ действий в файл"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, 
                 period=15, period_fractal=10, period_mean=5, kind='rsi', max_period_for_mean=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.kind = kind
        self.period_fractal = period_fractal
        self.period_mean = period_mean
        self.max_period_for_mean = max_period_for_mean
        
        # Список для сбора данных (теперь с pos и delta)
        self.debug_data = []

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        
        # Добавляем индикатор
        if self.kind == 'rsi':
            df = add_rsi(df, self.period)
        
        # Добавляем фракталы
        df = add_fractals(df, self.period_fractal, self.max_period_for_mean)
        
        # Добавляем средние по фракталам
        df = add_mean_on_fractals(df, self.period_mean, self.kind, self.max_period_for_mean)
        
        # Создаём oversold/overbought
        df['oversold'] = df[self.kind] < df['bottom_mean']
        df['overbought'] = df[self.kind] > df['top_mean']
        
        # Обрезаем
        df = self.add_slice_df(df)
        
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # Логика как в LEG1_BIBI (без учета pos/delta, только сырой сигнал)
        action = None
        
        if pd.notna(row['top_mean']) and pd.notna(row['bottom_mean']):
            if row['top_mean'] > row['bottom_mean']:
                if row['oversold']:
                    action = 'open_long'
                elif row['overbought']:
                    action = 'open_short'
            else:
                if row['oversold']:
                    action = 'close_short'
                elif row['overbought']:
                    action = 'close_long'
        
        # Сохраняем данные (позже сюда добавим pos и delta из __call__)
        self.debug_data.append({
            'x': row['x'],
            'kind': row[self.kind],
            'top_mean': row['top_mean'],
            'bottom_mean': row['bottom_mean'],
            'oversold': row['oversold'],
            'overbought': row['overbought'],
            'raw_action': action,
            'pos': None,  # Заполним позже
            'delta': None # Заполним позже
        })
        
        return action

    def __call__(self, pdata, pos, delta, *args, **kwds):
        # Вызываем родительский __call__, чтобы получить финальное действие с учетом стопов
        final_action = super().__call__(pdata, pos, delta, *args, **kwds)
        
        # Теперь обновляем последнюю запись в логе, добавляя pos и delta
        if self.debug_data:
            self.debug_data[-1]['pos'] = pos
            self.debug_data[-1]['delta'] = delta
            self.debug_data[-1]['final_action'] = final_action
        
        return final_action

    def save_to_csv(self, filename="debug_actions.csv"):
        """Сохраняет все данные в CSV файл"""
        df_log = pd.DataFrame(self.debug_data)
        df_log.to_csv(filename, index=False)
        print(f"Сохранено {len(df_log)} записей в {filename}")

    def print_actions(self):
        """Печатает последние 30 действий для быстрой проверки"""
        print(f"\n=== ПОСЛЕДНИЕ 30 ДЕЙСТВИЙ (всего записей: {len(self.actions_log)}) ===")
        # ... (оставляем как было)
