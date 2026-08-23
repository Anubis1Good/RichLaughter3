# run_optimization.py
from optimization.OptimizatorOptuna import OptimizatorOptuna
from optimization.optuna_grops.main_groups import group, max_period
# from optimization.optuna_grops.exp_groups import group, max_period
from testing.test_constants import *
# Time test on VEG1_VENUS
# ⏱ Total time: 0h 0m 37s - 50 trials
use_window = False
# ⏱ Total time: 1h 3m 37s - 50 trials
# use_window = True
# trials = 500
trials = 200
# trials = 100
# trials = 50
save_cores = 0

if __name__ == '__main__':
    optimizer = OptimizatorOptuna(
        test_folder='_data_for_tests/data_stock_5m',
        fee=MAIN_FEE,
        max_period=max_period,
        bottom_limit=80,
        top_limit=1000,
        save_cores=save_cores,
        n_trials=trials,
        need_plot=False,
        use_window_test=use_window,\
        window_size=WINDOW,
        days_mode=DAYS_MODE
    )
    
    optimizer.optimize_multiple_groups(group)