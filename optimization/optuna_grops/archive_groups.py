from strategies.all_egs import *

# (min, max, step)
from optimization.optuna_grops.opt_params import *
group = (
    (
        PEG2_DDCrWork, 
        [
            (2,max_period,1),
        ]
    ),

    (
        UEG3_REVAN, 
        [
            (2, max_period, 1),
            (2,20,1),
        ]
    ),
    (
        UEG3_ZEUS, 
        [
            (0.1,max_percent_threshold,0.1),
        ]
    ),
    (
        WEG3_DS, 
        [
            (2, max_period, 1),
            (0.5, 3, 0.1),
        ]
    ),

)