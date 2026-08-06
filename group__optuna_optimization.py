# run_optimization.py
from optimization.OptimizatorOptuna import OptimizatorOptuna
from optimization.optuna_grops.main_groups import group, max_period

if __name__ == '__main__':
    optimizer = OptimizatorOptuna(
        test_folder='_data_for_tests/data_stock_5m',
        fee=0.001,
        max_period=max_period,
        bottom_limit=100,
        top_limit=1000,
        n_trials=10,
        need_plot=True
    )
    
    optimizer.optimize_multiple_groups(group)