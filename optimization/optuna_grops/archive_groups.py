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
        PEG8_LOBSTER, 
        [
            (2,max_period,1),
            (0.5,3,0.1),   
        ]
    ),
    (
        LEG1_BORSCH, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        LEG1_PHOBO, 
        [
            (2, max_period, 1),
            (0.5,4,0.1),
            (max_period, ),
        ]
    ),
    (
        LEG1_PHOGA, 
        [
            (2, max_period, 1),
            (0.5,4,0.1),
            (2, max_period, 1),
            (max_period, ),
        ]
    ),
    (
        LEG2_MONSTER, 
        [
            (2, max_period, 1),
            (10,90,1),
            (2, max_period, 1),
            (0,max_period,1),
            (2, half_max_period, 1),
            (max_period,)
        ]
    ),


)