import os
import matplotlib.pyplot as plt
import pandas as pd
import optuna
import psutil
from multiprocessing import Pool
from functools import partial
from testing.CheckEGTrader import CheckEGTrader

optuna.logging.set_verbosity(optuna.logging.CRITICAL)
phys_cores = psutil.cpu_count(logical=False)

class OptimizatorOptuna:
    def __init__(self, 
                 test_folder: str,
                 main_folder: str = '_test_results/optuna',
                 fee: float = 0.0002,
                 max_period: int = 100,
                 close_on_time: bool = True,
                 close_map: tuple = ((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30)),
                 bottom_limit: int = 100,
                 top_limit: int = 1000,
                 n_trials: int = 100,
                 n_jobs: int = 1,
                 need_plot: bool = False,
                 save_cores: int = 1,
                 measure_time: bool = False,
                # Параметры SL/TP в процентах
                 sl_min_pct: float = 0.1,
                 sl_max_pct: float = 1.0,
                 tp_min_pct: float = 0.1,
                 tp_max_pct: float = 2.0
                 ):
        
        self.test_folder = test_folder
        self.main_folder = main_folder
        self.fee = fee
        self.max_period = max_period + 1
        self.close_on_time = close_on_time
        self.close_map = close_map
        self.bottom_limit = bottom_limit
        self.top_limit = top_limit
        self.n_trials = n_trials
        self.n_jobs = n_jobs
        self.need_plot = need_plot
        self.save_cores = save_cores
        self.measure_time = measure_time
        self.phys_cores = psutil.cpu_count(logical=False)
        # Параметры SL/TP
        self.sl_min_pct = sl_min_pct
        self.sl_max_pct = sl_max_pct
        self.tp_min_pct = tp_min_pct
        self.tp_max_pct = tp_max_pct
        self.traders = []
        
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)
        
        optuna.logging.disable_default_handler()
        optuna.logging.set_verbosity(optuna.logging.ERROR)
    
    def load_traders(self):
        files = [os.path.join(self.test_folder, f) for f in os.listdir(self.test_folder) 
                 if os.path.isfile(os.path.join(self.test_folder, f))]
        
        print(f"Loading {len(files)} files...")
        
        for file in files:
            ticker = os.path.basename(file).split('_')[0]
            trader = CheckEGTrader(
                df=file,
                ws=None,
                fee=self.fee,
                symbol=ticker,
                close_on_time=self.close_on_time,
                close_map=self.close_map,
                measure_time=self.measure_time,
                use_tqdm=False
            )
            self.traders.append(trader)
        
        print(f"Loaded {len(self.traders)} traders")

    def get_sl_tp_params(self, trader):
        """
        Рассчитывает параметры SL/TP для конкретного инструмента.
        Шаг всегда = 1 (один шаг цены)
        """
        price_step_per = trader.price_step_per  # уже в процентах!
        
        # Минимальное и максимальное количество шагов для SL
        min_steps_sl = int(self.sl_min_pct / price_step_per)
        max_steps_sl = int(self.sl_max_pct / price_step_per)
        
        # Минимальное и максимальное количество шагов для TP
        min_steps_tp = int(self.tp_min_pct / price_step_per)
        max_steps_tp = int(self.tp_max_pct / price_step_per)
        
        # Гарантируем минимум 1 шаг
        min_steps_sl = max(1, min_steps_sl)
        min_steps_tp = max(1, min_steps_tp)
        
        # Если максимум меньше минимума - корректируем
        max_steps_sl = max(min_steps_sl, max_steps_sl)
        max_steps_tp = max(min_steps_tp, max_steps_tp)
        
        return {
            'sl': (min_steps_sl, max_steps_sl),  # шаг всегда 1
            'tp': (min_steps_tp, max_steps_tp)   # шаг всегда 1
        }
    
    def objective(self, trial, trader, strategy_class, param_options):
        # Получаем параметры SL/TP для этого инструмента
        sl_tp_params = self.get_sl_tp_params(trader)
        
        # Стратегические параметры
        params = []
        for i, options in enumerate(param_options):
            param_name = f"param_{i}"
            
            # Категориальные параметры (строки)
            if isinstance(options[0], str):
                params.append(trial.suggest_categorical(param_name, options))
                continue
            
            # Формат: (min, max, step)
            if len(options) == 3:
                min_val, max_val, step_val = options
                
                # Проверяем валидность
                if min_val >= max_val:
                    raise ValueError(f"min ({min_val}) must be less than max ({max_val}) for param_{i}")
                if step_val <= 0:
                    raise ValueError(f"step ({step_val}) must be positive for param_{i}")
                
                # Определяем тип и предлагаем
                if isinstance(step_val, int) and all(isinstance(x, int) for x in [min_val, max_val]):
                    params.append(trial.suggest_int(param_name, min_val, max_val, step=step_val))
                else:
                    params.append(trial.suggest_float(param_name, min_val, max_val, step=step_val))
            
            # Формат: (min, max) - шаг по умолчанию 1
            elif len(options) == 2:
                min_val, max_val = options
                
                if min_val >= max_val:
                    raise ValueError(f"min ({min_val}) must be less than max ({max_val}) for param_{i}")
                
                if all(isinstance(x, int) for x in [min_val, max_val]):
                    params.append(trial.suggest_int(param_name, min_val, max_val))
                else:
                    params.append(trial.suggest_float(param_name, min_val, max_val))
            
            # Список значений
            else:
                if all(isinstance(x, int) for x in options):
                    params.append(trial.suggest_int(param_name, min(options), max(options)))
                else:
                    params.append(trial.suggest_float(param_name, min(options), max(options)))
                # SL и TP - шаг всегда 1
        sl_min, sl_max = sl_tp_params['sl']
        tp_min, tp_max = sl_tp_params['tp']
        
        sl_value = trial.suggest_int('sl', sl_min, sl_max, step=1)
        tp_value = trial.suggest_int('tp', tp_min, tp_max, step=1)

        strategy = strategy_class(
            trader.symbol, 
            trader.price_step,
            1,
            None,
            sl_value,
            tp_value, 
            *params
        )
        
        trader.ws = strategy
        trader.reload_data()
        trader.check_strategy_fast(history_bars=self.max_period)
        
        trades, eq, eq_f, _, _, _ = trader.process_old_type_result()
        
        if not self.bottom_limit <= trades['count'] <= self.top_limit:
            raise optuna.TrialPruned()
        
        return trades['total_abs_fee']
    
    def get_results_table(self, study, trader, strategy_class, param_options):
        results = []
        name_bot = strategy_class.__name__
        ticker = trader.symbol
        
        images_folder = os.path.join(self.main_folder, name_bot, ticker, 'Images')
        file_folder = os.path.join(self.main_folder, name_bot, ticker)
        
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)
        
        completed_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
        n_top = min(25, len(completed_trials))
        top_trials = sorted(completed_trials, key=lambda x: x.value, reverse=True)[:n_top]
        
        if not top_trials:
            return pd.DataFrame()
        
        for trial in top_trials:
            params = []
            param_values = []
            for i, options in enumerate(param_options):
                param_name = f"param_{i}"
                param_value = trial.params[param_name]
                if isinstance(param_value, float):
                    param_value = round(param_value, 2)
                params.append(param_value)
                param_values.append(str(param_value))
                        # SL и TP
            sl_value = trial.params['sl']
            tp_value = trial.params['tp']
            
            # Все параметры
            all_params = [sl_value, tp_value] + params
            all_param_values = [str(sl_value), str(tp_value)] + param_values

            strategy = strategy_class(ticker, trader.price_step, 1, None, *all_params)
            
            trader.ws = strategy
            trader.reload_data()
            trader.check_strategy_fast(history_bars=self.max_period)
            
            trades, eq, eq_f, _, _, _ = trader.process_old_type_result()
            
            name_doc = f"{ticker}_{name_bot}"
            name_file = f"{name_doc}_{'_'.join(all_param_values)}"
            params_tuple = f"({name_bot},({','.join(all_param_values)},)),"
            price_step_per = trader.price_step_per  # в процентах
            result_row = {
                "name": name_file,
                "ws": params_tuple,
                "amount_sl": trader.ws.amount_sl,
                "amount_tp": trader.ws.amount_tp,
                "sl/tp": round(sl_value / tp_value,2),
                "sl_pct": round(sl_value * price_step_per, 2),   # SL в процентах
                "tp_pct": round(tp_value * price_step_per, 2),   # TP в процентах
            }
            result_row = result_row | trades
            
            result_row['origin'] = ticker
            for i, param_value in enumerate(params):
                result_row[f"Param_{i}"] = param_value
            results.append(result_row)
            
            if self.need_plot:
                full_name_img = os.path.join(images_folder, f"{name_file}.png")
                plt.figure(figsize=(12, 6))
                plt.plot(eq, color='red', label='Equity')
                plt.plot(eq_f, color='blue', label='Equity with Fees')
                plt.title(f"{name_bot} (Trial {trial.number})")
                plt.legend()
                plt.savefig(full_name_img, bbox_inches='tight')
                plt.close()
        
        df_results = pd.DataFrame(results).sort_values('total_abs_fee', ascending=False)
        df_results = df_results.drop_duplicates(subset=['total_abs_fee'])
        df_results = df_results.reset_index(drop=True)
        
        full_name_doc = os.path.join(file_folder, name_doc + '.xlsx')
        with pd.ExcelWriter(full_name_doc, engine='xlsxwriter') as writer:
            df_results.to_excel(writer, sheet_name='total')
            worksheet = writer.sheets['total']
            for i, col in enumerate(df_results.columns, start=1):
                width = max(df_results[col].apply(lambda x: len(str(x))).max(), len(col))
                worksheet.set_column(i, i, width)
        
        return df_results
    
    def optimize_trader(self, trader, strategy_config):
        ticker = trader.symbol
        strategy_class, param_options = strategy_config
        
        print(f"  {ticker}...", end=" ", flush=True)
        
        study = optuna.create_study(direction="maximize")
        study.optimize(
            lambda trial: self.objective(trial, trader, strategy_class, param_options),
            n_trials=self.n_trials,
            n_jobs=self.n_jobs
        )
        
        results = self.get_results_table(study, trader, strategy_class, param_options)
        
        if results is not None and not results.empty:
            best_result = results.iloc[0]
            print(f"✓ (best: {best_result['total_abs_fee']:.2f}, trades: {best_result['count']})")
        else:
            print("✗")
        
        return results
    
    def process_group(self, strategy_config, n_trials=None, n_jobs=None, need_plot=None):
        if n_trials is not None:
            self.n_trials = n_trials
        if n_jobs is not None:
            self.n_jobs = n_jobs
        if need_plot is not None:
            self.need_plot = need_plot
        
        if not self.traders:
            self.load_traders()
        
        strategy_name = strategy_config[0].__name__
        print(f"\nTesting strategy: {strategy_name}")
        print(f"Files to test: {len(self.traders)}")
        print("-" * 50)
        
        num_processes = min(max(1, self.phys_cores - self.save_cores), len(self.traders))
        
        if num_processes > 1:
            print(f"Using {num_processes} processes...")
            worker = partial(self.optimize_trader, strategy_config=strategy_config)
            
            with Pool(processes=num_processes) as pool:
                results = list(pool.imap_unordered(worker, self.traders))
        else:
            print("Processing sequentially...")
            results = [self.optimize_trader(trader, strategy_config) for trader in self.traders]
        
        success_count = sum(1 for r in results if r is not None and not r.empty)
        
        print("-" * 50)
        print(f"Completed: {success_count}/{len(self.traders)}")
        return success_count
    
    def optimize_multiple_groups(self, groups):
        total_success = 0
        for i, group in enumerate(groups):
            success = self.process_group(group)
            total_success += success
        
        print(f"\n{'='*50}")
        print(f"Total: {total_success} successful")
        print(f"{'='*50}")