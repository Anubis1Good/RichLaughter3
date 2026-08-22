from strategies.all_egs import *

# (min, max, step)
from optimization.optuna_grops.opt_params import *
group = (
    (
        UEG9_BIRDWATCHER, 
        [
            (0.1,max_percent_threshold,0.1),
            (2,5,1),
            (0,0.3,0.1),
            (0.25,2,0.05),
            (0,1),
            (0,1),
        ]
    ),
    (
        UEG9_GRAVY, 
        [
            (0.1,max_percent_threshold,0.1),
            (2,5,1),
            (0,0.3,0.1),
            (0.25,2,0.05),
            (0,1),
        ]
    ),
    (
        WEG4_RAT, 
        [
            (2, max_period, 1),
            (2,period_fractal_max,1),
            (max_period,),
        ]
    ),

)