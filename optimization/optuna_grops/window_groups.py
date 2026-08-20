from strategies.PEGs.PEG1_9 import *
from strategies.PEGs.PEG10_19 import *
from strategies.PEGs.PEG20_29 import *
from strategies.LEGs.LEG1 import *
from strategies.LEGs.LEG2 import *
from strategies.WEGs.WEG1_9 import *
from strategies.UEGs.UEG1_9 import *
from strategies.SEGs.SEG_CA1_9 import *
from strategies.SEGs.SEG_ML10_19 import *
from strategies.VEGs.VEG1 import *

# (min, max, step)
from optimization.optuna_grops.opt_params import *
group = (




   (
        SEGML2_NEWAVE, 
        [
            (2, max_period, 1),
            (3,10,1),
            (0.5,10,0.5),
            (10,40,1),
        ]
    ),
    (
        SEGML2_TRENDWAVE, 
        [
            (2, max_period, 1),
            (3,10,1),
            (0.5,10,0.5),
            (10,40,1),
            (10,40,1),
        ]
    ),
    # (
    #     SEGML2_SID, 
    #     [
    #         (2, max_period, 1),
    #         (2,30,1),
    #         (2,30,1),
    #         (10,40,1),
    #         (0.1,1,0.1),
    #     ]
    # ),
    # (
    #     SEGML2b_RAPTOR, 
    #     [
    #         (2, max_period, 1),
    #         (1,15,1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (0, 1),
    #         (0, 1),
    #         (1,30,1),
    #     ]
    # ),
#     Traceback (most recent call last):
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\pool.py", line 125, in worker
#     result = (True, func(*args, **kwds))
#                     ^^^^^^^^^^^^^^^^^^^
#   File "e:\Dev\exchange\RichLaughter3\optimization\OptimizatorOptuna.py", line 340, in optimize_trader
#     study.optimize(
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\optuna\study\study.py", line 489, in optimize
#     _optimize(
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\optuna\study\_optimize.py", line 64, in _optimize
#     _optimize_sequential(
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\optuna\study\_optimize.py", line 161, in _optimize_sequential
#     frozen_trial = _run_trial(study, func, catch)
#                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\optuna\study\_optimize.py", line 253, in _run_trial
#     raise func_err
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\optuna\study\_optimize.py", line 201, in _run_trial
#     value_or_values = func(trial)
#                       ^^^^^^^^^^^
#   File "e:\Dev\exchange\RichLaughter3\optimization\OptimizatorOptuna.py", line 341, in <lambda>
#     lambda trial: self.objective(trial, trader, strategy_class, param_options),
#                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "e:\Dev\exchange\RichLaughter3\optimization\OptimizatorOptuna.py", line 189, in objective
#     trader.check_strategy_window(window=self.window_size, normalization=self.normalization)
#   File "e:\Dev\exchange\RichLaughter3\testing\CheckEGTrader.py", line 20, in wrapper
#     result = func(self, *args, **kwargs)
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "e:\Dev\exchange\RichLaughter3\testing\CheckEGTrader.py", line 349, in check_strategy_window
#     pdata = self.ws.preprocessing(tdata)
#             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "e:\Dev\exchange\RichLaughter3\strategies\SEGs\SEG_ML10_19.py", line 194, in preprocessing
#     self.get_model(X_train, y_train)
#   File "e:\Dev\exchange\RichLaughter3\strategies\SEGs\SEG_ML10_19.py", line 142, in get_model
#     self.model.fit(X_train, y_train)
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\sklearn\base.py", line 1473, in wrapper
#     return fit_method(estimator, *args, **kwargs)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\sklearn\tree\_classes.py", line 1009, in fit
#     super()._fit(
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\sklearn\tree\_classes.py", line 252, in _fit
#     X, y = self._validate_data(
#            ^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\sklearn\base.py", line 645, in _validate_data
#     X = check_array(X, input_name="X", **check_X_params)
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\sklearn\utils\validation.py", line 1082, in check_array
#     raise ValueError(
# ValueError: Found array with 0 sample(s) (shape=(0, 8)) while a minimum of 1 is required by DecisionTreeClassifier.
# """

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "e:\Dev\exchange\RichLaughter3\group__optuna_optimization.py", line 23, in <module>
#     optimizer.optimize_multiple_groups(group)
#   File "e:\Dev\exchange\RichLaughter3\optimization\OptimizatorOptuna.py", line 403, in optimize_multiple_groups
#     success = self.process_group(group)
#               ^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "e:\Dev\exchange\RichLaughter3\optimization\OptimizatorOptuna.py", line 381, in process_group
#     results = list(pool.imap_unordered(worker, self.traders))
#               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\pool.py", line 873, in next
#     raise value
# ValueError: Found array with 0 sample(s) (shape=(0, 8)) while a minimum of 1 is required by DecisionTreeClassifier.

    (
        VEG1_MERCURY, 
        [
            (2, max_period, 1),
            (0.5,20,0.5),
            (0,1,0.1),
            (0.1,0.5,0.1),
            (0.5,2,0.1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),

)