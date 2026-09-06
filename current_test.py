import os
import pandas as pd
import psutil
from time import time
from multiprocessing import Pool
from testing.CheckEGTrader import CheckEGTrader
import traceback
import re
import matplotlib.pyplot as plt
from time import time
from testing.test_constants import *
# Импортируем все стратегии
from strategies.all_egs import *

class CurrentTester:
    def __init__(self,
                 data_folder: str,
                 output_folder: str = '_test_results/current_test',
                 fee: float = 0.001,
                 close_on_time: bool = True,
                 close_map: tuple = ((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30)),
                 window_size: int = 60,
                 normalization: bool = True,
                 save_cores: int = 1,
                 need_plot = False,
                 days_mode = None,
                 slip_stop_delta = 1,
                 strategies_dict = None
                 ):
        
        self.data_folder = data_folder
        self.output_folder = output_folder
        self.fee = fee
        self.close_on_time = close_on_time
        self.close_map = close_map
        self.window_size = window_size
        self.normalization = normalization
        self.save_cores = save_cores
        self.phys_cores = psutil.cpu_count(logical=False)
        self.need_plot = need_plot
        self.days_mode = days_mode
        self.slip_stop_delta = slip_stop_delta
        self.strategies_dict = strategies_dict or {}
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
    def get_ticker_from_key(self, key):
        """Извлекает чистый тикер из ключа (убирает цифры в конце)"""
        # Убираем цифры в конце (AFLT2 -> AFLT, AFLT10 -> AFLT)
        ticker = re.sub(r'\d+$', '', key)
        return ticker
    
    def load_trader(self, ticker):
        """Загружает трейдера для указанного тикера"""
        files = [f for f in os.listdir(self.data_folder) 
                 if os.path.isfile(os.path.join(self.data_folder, f)) and f.startswith(ticker)]
        
        if not files:
            print(f"Data file for {ticker} not found")
            return None
        
        file_path = os.path.join(self.data_folder, files[0])
        
        trader = CheckEGTrader(
            df=file_path,
            ws=None,
            fee=self.fee,
            symbol=ticker,
            close_on_time=self.close_on_time,
            close_map=self.close_map,
            measure_time=False,
            use_tqdm=False,
            window=self.window_size,
            days_mode=self.days_mode,
            slip_stop_delta=self.slip_stop_delta
        )
        
        return trader
    
    def test_single_row(self, row_data, chunk_index, results_list, output_path):
        """
        Тестирует одну стратегию и сразу добавляет результат в файл
        """
        row_name = row_data.get('name', 'unknown')
        try:
            # Извлекаем данные стратегии
            strategy_tuple = row_data.get('strategy_tuple')
            if not strategy_tuple:
                return False
            
            # Распаковываем кортеж: (StrategyClass, params, param1, param2)
            strategy_class = strategy_tuple[0]
            params = strategy_tuple[1] if len(strategy_tuple) > 1 else tuple()
            
            # Получаем тикер из имени стратегии
            ticker = self.get_ticker_from_key(row_name)
            
            # Преобразуем параметры (заменяем строки 'None' на реальный None)
            processed_params = []
            for p in params:
                if isinstance(p, str) and p == 'None':
                    processed_params.append(None)
                else:
                    processed_params.append(p)
            
            # Загружаем трейдера
            trader = self.load_trader(ticker)
            if trader is None:
                print(f"[{os.getpid()}] Trader not loaded for {ticker}, skipping {row_name}")
                return False
            
            # Создаем стратегию
            try:
                strategy = strategy_class(
                    trader.symbol,
                    trader.price_step,
                    1,  # volume
                    None,  # bot может быть None
                    *processed_params
                )
            except Exception as e:
                print(f"[{os.getpid()}] Error creating strategy for {row_name}: {e}")
                return False
            
            trader.ws = strategy
            trader.reload_data()
            
            # БЫСТРЫЙ ТЕСТ
            trader.check_strategy_faster()
            trades_fast, _, _, _, _, _ = trader.process_old_type_result()
            ef_fast = trader.trade_data['step_eq_fee']
            
            # ОКОННЫЙ ТЕСТ
            trader.reload_data()
            trader.check_strategy_window(normalization=self.normalization)
            trades_window, _, _, _, _, _ = trader.process_old_type_result()
            ef_window = trader.trade_data['step_eq_fee']
            
            if self.need_plot:
                img_folder = os.path.join(self.output_folder, 'imgs')
                os.makedirs(img_folder, exist_ok=True)
                full_name_img = os.path.join(img_folder, f"{row_name}.png")
                plt.figure(figsize=(12, 6))
                plt.plot(ef_window, color='red', label='Equity_window')
                plt.plot(ef_fast, color='blue', label='Equity_fast')
                plt.title(f"{row_name}")
                plt.legend()
                plt.savefig(full_name_img, bbox_inches='tight')
                plt.close()
            
            # Формируем результат
            result = {
                'name': row_name,
                'ticker': ticker,
                'strategy': str(strategy_class.__name__),
                'params': str(processed_params),
                # Результаты быстрого теста
                'total_fast': round(trades_fast['total'], 2),
                'count_fast': trades_fast['count'],
                'total_fee_per_fast': round(trades_fast.get('total_fee_per', 0), 2),
                'win_rate_fast': trades_fast.get('win_rate_wf', 0),
                # Результаты оконного теста
                'total_window': round(trades_window['total'], 2),
                'count_window': trades_window['count'],
                'total_fee_per_window': round(trades_window.get('total_fee_per', 0), 2),
                'win_rate_window': trades_window.get('win_rate_wf', 0),
                # Разница
                'diff_total': round(trades_window['total'] - trades_fast['total'], 2),
                'diff_count': trades_window['count'] - trades_fast['count'],
                'diff_total_fee_per': round(trades_window.get('total_fee_per', 0) - trades_fast.get('total_fee_per', 0), 2),
            }
            
            results_list.append(result)
            
            # Сразу сохраняем обновленный файл
            if results_list:
                temp_df = pd.DataFrame(results_list)
                temp_df = temp_df.sort_values('total_fee_per_fast', ascending=False)
                temp_df = temp_df.reset_index(drop=True)
                
                with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                    temp_df.to_excel(writer, sheet_name='results', index=False)
                    worksheet = writer.sheets['results']
                    for i, col in enumerate(temp_df.columns):
                        max_len = max(temp_df[col].astype(str).map(len).max(), len(col))
                        worksheet.set_column(i, i, min(max_len + 2, 50))
                
                print(f"[{os.getpid()}] Chunk {chunk_index}: {len(results_list)} results saved, last: {row_name}")
            
            return True
            
        except Exception as e:
            print(f"[{os.getpid()}] Error testing {row_name}: {e}")
            traceback.print_exc()
            return False
    
    def test_rows_chunk(self, chunk_data, chunk_index):
        """Тестирует чанк стратегий, сохраняя после каждой"""
        print(f"\n[Process {os.getpid()}] Starting chunk {chunk_index} with {len(chunk_data)} rows")
        
        results = []
        output_path = os.path.join(self.output_folder, f'process_{chunk_index}_results.xlsx')
        start_time = time()
        
        if os.path.exists(output_path):
            os.remove(output_path)
        
        for i, row_data in enumerate(chunk_data):
            print(f"[{os.getpid()}] Chunk {chunk_index}: testing row {i+1}/{len(chunk_data)} - {row_data.get('name', 'unknown')}")
            
            success = self.test_single_row(row_data, chunk_index, results, output_path)
            
            if success:
                print(f"[{os.getpid()}] Chunk {chunk_index}: progress {i+1}/{len(chunk_data)} ({len(results)} results so far)")
            else:
                print(f"[{os.getpid()}] Chunk {chunk_index}: FAILED row {i+1}/{len(chunk_data)}")
        
        elapsed = time() - start_time
        print(f"[Process {os.getpid()}] Chunk {chunk_index} completed in {elapsed:.1f}s, got {len(results)} results")
        
        if results:
            print(f"[Process {os.getpid()}] [OK] Chunk {chunk_index}: {len(results)} results saved to {output_path}")
            return True
        else:
            if os.path.exists(output_path):
                os.remove(output_path)
            print(f"[Process {os.getpid()}] [FAIL] Chunk {chunk_index}: no valid results")
            return False
    
    @staticmethod
    def process_chunk_static(data_folder, output_folder, fee, close_on_time, 
                            close_map, window_size, normalization, 
                            chunk_data, chunk_index, need_plot, days_mode, 
                            slip_stop_delta, strategies_dict):
        tester = CurrentTester(
            data_folder=data_folder,
            output_folder=output_folder,
            fee=fee,
            close_on_time=close_on_time,
            close_map=close_map,
            window_size=window_size,
            normalization=normalization,
            save_cores=1,
            need_plot=need_plot,
            days_mode=days_mode,
            slip_stop_delta=slip_stop_delta,
            strategies_dict=strategies_dict
        )
        return tester.test_rows_chunk(chunk_data, chunk_index)
    
    def run_tests(self):
        start_time = time()
        
        # Подготавливаем данные из словаря стратегий
        strategies_list = []
        for name, strategy_tuple in self.strategies_dict.items():
            strategies_list.append({
                'name': name,
                'strategy_tuple': strategy_tuple
            })
        
        print(f"Loaded {len(strategies_list)} strategies from bot_on_ticker")
        
        if not strategies_list:
            print("No strategies to test")
            return
        
        num_processes = max(1, self.phys_cores - self.save_cores)
        num_processes = min(num_processes, len(strategies_list))
        print(f"Using {num_processes} processes...")
        
        chunk_size = max(1, len(strategies_list) // num_processes)
        chunks = []
        for i in range(0, len(strategies_list), chunk_size):
            chunk_data = strategies_list[i:i+chunk_size]
            chunks.append(chunk_data)
        
        num_processes = min(num_processes, len(chunks))
        print(f"Split into {len(chunks)} chunks")
        print(f"Each chunk has ~{chunk_size} strategies")
        print("="*50)
        
        args_list = []
        for i, chunk_data in enumerate(chunks):
            args_list.append((
                self.data_folder,
                self.output_folder,
                self.fee,
                self.close_on_time,
                self.close_map,
                self.window_size,
                self.normalization,
                chunk_data,
                i,
                self.need_plot,
                self.days_mode,
                self.slip_stop_delta,
                self.strategies_dict
            ))
        
        if num_processes > 1:
            with Pool(processes=num_processes) as pool:
                results = pool.starmap(self.process_chunk_static, args_list)
            success_count = sum(results)
        else:
            success_count = 0
            for args in args_list:
                if self.process_chunk_static(*args):
                    success_count += 1
        
        print("\n" + "="*50)
        print("Merging all results...")
        
        all_results = []
        for file in os.listdir(self.output_folder):
            if file.startswith('process_') and file.endswith('_results.xlsx'):
                file_path = os.path.join(self.output_folder, file)
                df_temp = pd.read_excel(file_path)
                all_results.append(df_temp)
                print(f"Found: {file} ({len(df_temp)} rows)")
        
        if all_results:
            final_df = pd.concat(all_results, ignore_index=True)
            final_df = final_df.sort_values('total_fee_per_fast', ascending=False)
            final_df = final_df.reset_index(drop=True)
            
            final_filename = 'current_test_results_' + str(int(time())) + '.xlsx'
            output_path = os.path.join(self.output_folder, final_filename)
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                final_df.to_excel(writer, sheet_name='results', index=False)
                worksheet = writer.sheets['results']
                for i, col in enumerate(final_df.columns):
                    max_len = max(final_df[col].astype(str).map(len).max(), len(col))
                    worksheet.set_column(i, i, min(max_len + 2, 50))
            
            print(f"[OK] Final results saved to: {output_path}")
            print(f"Total rows: {len(final_df)}")
        else:
            print("[FAIL] No results to merge")
        
        elapsed = time() - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        
        print(f"\n{'='*50}")
        print(f"Current test completed!")
        print(f"Chunks processed: {success_count}/{len(chunks)}")
        print(f"Time: {hours}h {minutes}m {seconds}s")
        print(f"{'='*50}")


if __name__ == "__main__":
    DATA_FOLDER = "_data_for_tests/data_stock_5m"
    OUTPUT_FOLDER = "_test_results/current_test"
    from traders.VT.bot_on_ticker import bot_on_ticker

    
    tester = CurrentTester(
        data_folder=DATA_FOLDER,
        output_folder=OUTPUT_FOLDER,
        fee=MAIN_FEE,
        close_on_time=True,
        close_map=((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30)),
        window_size=WINDOW,
        normalization=True,
        save_cores=0,
        need_plot=True,
        days_mode=DAYS_MODE,
        slip_stop_delta=SLIP_STOP_DELTA,
        strategies_dict=bot_on_ticker
    )
    
    tester.run_tests()