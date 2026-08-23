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

class WindowTester:
    def __init__(self,
                 data_folder: str,
                 results_excel: str,
                 output_folder: str = '_test_results/window_test',
                 tickers: list = None,
                 fee: float = 0.001,
                 close_on_time: bool = True,
                 close_map: tuple = ((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30)),
                 window_size: int = 60,
                 normalization: bool = True,
                 save_cores: int = 1,
                 need_plot = False,
                 days_mode = None
                 ):
        
        self.data_folder = data_folder
        self.results_excel = results_excel
        self.output_folder = output_folder
        self.tickers = tickers
        self.fee = fee
        self.close_on_time = close_on_time
        self.close_map = close_map
        self.window_size = window_size
        self.normalization = normalization
        self.save_cores = save_cores
        self.phys_cores = psutil.cpu_count(logical=False)
        self.need_plot = need_plot
        self.days_mode = days_mode
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # if self.need_plot:
        #     self.img_folder = os.path.join(output_folder,'imgs',str(int(time())))
        #     os.makedirs(self.img_folder,exist_ok=True)
    
    def load_trader(self, ticker):
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
            days_mode=self.days_mode
        )
        
        return trader
    
    def test_single_row(self, row_data, chunk_index, results_list, output_path):
        """
        Тестирует одну строку и сразу добавляет результат в файл
        """
        row_name = row_data.get('name', 'unknown')
        try:
            ticker = row_data['origin']
            ws_str = row_data['ws']
            
            # Очищаем строку
            ws_str = ws_str.strip()
            original_ws = ws_str
            
            if ws_str.endswith('),'):
                ws_str = ws_str[:-2] + ')'
            
            match = re.search(r'\(([^)]+)\)', ws_str)
            if match:
                params_part = match.group(1)
                while params_part.endswith(','):
                    params_part = params_part[:-1]
                ws_str = ws_str[:match.start(1)] + params_part + ws_str[match.end(1):]
            
            ws_tuple = eval(ws_str)
            
            if not isinstance(ws_tuple, tuple) or len(ws_tuple) != 2:
                return False
            
            strategy_class = ws_tuple[0]
            params = ws_tuple[1]
            
            trader = self.load_trader(ticker)
            if trader is None:
                return False
            
            strategy = strategy_class(
                trader.symbol,
                trader.price_step,
                1,
                None,
                *params
            )
            
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
                full_name_img = os.path.join(self.img_folder, f"{row_name}.png")
                plt.figure(figsize=(12, 6))
                plt.plot(ef_window, color='red', label='Equity_window')
                plt.plot(ef_fast, color='blue', label='Equity_fast')
                plt.title(f"{row_name}")
                plt.legend()
                plt.savefig(full_name_img, bbox_inches='tight')
                plt.close()
            # Берем реальные значения SL/TP из стратегии
            # amount_sl = trader.ws.amount_sl if hasattr(trader.ws, 'amount_sl') else 0
            # amount_tp = trader.ws.amount_tp if hasattr(trader.ws, 'amount_tp') else 0
            
            # # Считаем sl/tp, sl_pct, tp_pct
            # sl_tp_ratio = round(amount_sl / amount_tp, 2) if amount_tp > 0 else 0
            # sl_pct = round(amount_sl * trader.price_step_per, 2)
            # tp_pct = round(amount_tp * trader.price_step_per, 2)
            
            result = {
                'origin': ticker,
                'name': row_name,
                'ws': original_ws,
                # 'amount_sl': amount_sl,
                # 'amount_tp': amount_tp,
                # 'sl/tp': sl_tp_ratio,
                # 'sl_pct': sl_pct,
                # 'tp_pct': tp_pct,
            }
            
            # Результаты быстрого теста
            result['total_fast'] = round(trades_fast['total'], 2)
            result['count_fast'] = trades_fast['count']
            result['total_fee_per_fast'] = round(trades_fast.get('total_fee_per', 0), 2)
            result['win_rate_fast'] = trades_fast.get('win_rate_wf', 0)
            
            # Результаты оконного теста
            result['total_window'] = round(trades_window['total'], 2)
            result['count_window'] = trades_window['count']
            result['total_fee_per_window'] = round(trades_window.get('total_fee_per', 0), 2)
            result['win_rate_window'] = trades_window.get('win_rate_wf', 0)
            
            # Разница
            result['diff_total'] = round(trades_window['total'] - trades_fast['total'], 2)
            result['diff_count'] = trades_window['count'] - trades_fast['count']
            result['diff_total_fee_per'] = round(trades_window.get('total_fee_per', 0) - trades_fast.get('total_fee_per', 0), 2)
            
            # Добавляем результат в список
            results_list.append(result)
            
            # Сразу сохраняем обновленный файл
            if results_list:
                temp_df = pd.DataFrame(results_list)
                temp_df = temp_df.sort_values('total_fee_per_fast', ascending=False)
                temp_df = temp_df.reset_index(drop=True)
                
                # Сохраняем с расширенными колонками
                with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                    temp_df.to_excel(writer, sheet_name='results', index=False)
                    worksheet = writer.sheets['results']
                    # Растягиваем колонки для удобного чтения
                    for i, col in enumerate(temp_df.columns):
                        max_len = max(temp_df[col].astype(str).map(len).max(), len(col))
                        worksheet.set_column(i, i, min(max_len + 2, 50))
                
                print(f"[{os.getpid()}] Chunk {chunk_index}: {len(results_list)} results saved, last: {row_name}")
            
            return True
            
        except Exception as e:
            print(f"[{os.getpid()}] Error testing {row_name}: {e}")
            return False
    
    def test_rows_chunk(self, chunk_data, chunk_index):
        """Тестирует чанк строк, сохраняя после каждой стратегии"""
        print(f"\n[Process {os.getpid()}] Starting chunk {chunk_index} with {len(chunk_data)} rows")
        
        results = []
        output_path = os.path.join(self.output_folder, f'process_{chunk_index}_results.xlsx')
        start_time = time()
        
        # Удаляем старый файл если есть
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
            # Удаляем пустой файл
            if os.path.exists(output_path):
                os.remove(output_path)
            print(f"[Process {os.getpid()}] [FAIL] Chunk {chunk_index}: no valid results")
            return False
    
    @staticmethod
    def process_chunk_static(data_folder, results_excel, output_folder, tickers, fee, 
                            close_on_time, close_map, window_size, normalization, 
                            chunk_data, chunk_index, need_plot, img_folder, days_mode):
        tester = WindowTester(
            data_folder=data_folder,
            results_excel=results_excel,
            output_folder=output_folder,
            tickers=tickers,
            fee=fee,
            close_on_time=close_on_time,
            close_map=close_map,
            window_size=window_size,
            normalization=normalization,
            save_cores=1,
            need_plot=need_plot,
            days_mode=days_mode
        )
        # Используем общую папку
        if need_plot and img_folder:
            tester.img_folder = img_folder
        return tester.test_rows_chunk(chunk_data, chunk_index)
    
    def run_tests(self):
        start_time = time()
        
        df = pd.read_excel(self.results_excel)
        print(f"Loaded {len(df)} rows from {self.results_excel}")
        
        if self.tickers:
            df = df[df['origin'].isin(self.tickers)]
            print(f"Filtered to {len(df)} rows for tickers: {self.tickers}")
        
        if df.empty:
            print("No rows to test")
            return
        
        num_processes = max(1, self.phys_cores - self.save_cores)
        num_processes = min(num_processes, len(df))
        print(f"Using {num_processes} processes...")
        
        chunk_size = max(1, len(df) // num_processes)
        chunks = []
        for i in range(0, len(df), chunk_size):
            chunk_df = df.iloc[i:i+chunk_size]
            chunk_data = chunk_df.to_dict('records')
            chunks.append(chunk_data)
        
        num_processes = min(num_processes, len(chunks))
        print(f"Split into {len(chunks)} chunks")
        print(f"Each chunk has ~{chunk_size} rows")
        print(f"Files will be updated after EACH successful strategy test")
        print(f"First result will appear in ~21 seconds (1 strategy)")
        print("="*50)
        if self.need_plot:
            img_folder = os.path.join(self.output_folder, 'imgs', str(int(time())))
            os.makedirs(img_folder, exist_ok=True)
        else:
            img_folder = None
    
        args_list = []
        for i, chunk_data in enumerate(chunks):
            args_list.append((
                self.data_folder,
                self.results_excel,
                self.output_folder,
                self.tickers,
                self.fee,
                self.close_on_time,
                self.close_map,
                self.window_size,
                self.normalization,
                chunk_data,
                i,
                self.need_plot,
                img_folder,
                self.days_mode  # передаем общую папку
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
            
            final_filename = 'window_test_results' + str(int(time())) + '.xlsx'
            output_path = os.path.join(self.output_folder, final_filename)
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                final_df.to_excel(writer, sheet_name='results', index=False)
                worksheet = writer.sheets['results']
                # Растягиваем колонки для удобного чтения
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
        print(f"Window test completed!")
        print(f"Chunks processed: {success_count}/{len(chunks)}")
        print(f"Time: {hours}h {minutes}m {seconds}s")
        print(f"{'='*50}")


if __name__ == "__main__":
    DATA_FOLDER = "_data_for_tests/_before_opt"
    RESULTS_EXCEL = "_test_results/optuna/total_optuna.xlsx"
    OUTPUT_FOLDER = "_test_results/window_test"
    
    # TICKERS = ["ASTR","MAGN","MTLR"]
    TICKERS = []
    
    tester = WindowTester(
        data_folder=DATA_FOLDER,
        results_excel=RESULTS_EXCEL,
        output_folder=OUTPUT_FOLDER,
        tickers=TICKERS,
        fee=MAIN_FEE,
        close_on_time=True,
        close_map=((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30)),
        window_size=WINDOW,
        normalization=True,
        save_cores=0,
        need_plot=True,
        days_mode=DAYS_MODE
    )
    
    tester.run_tests()