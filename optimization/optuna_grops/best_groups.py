from strategies.all_egs import *

from optimization.optuna_grops.opt_params import *
# (min, max, step)

group = (
    (
        PEG17_PHOENIX, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (0, 1),
            (max_period,),
        ]
    ),
    (
        PEG11_KUSURUKEN, 
        [
            (5, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),    
            ('c', 'hl'),    
            (max_period,),
        ]
    ),
    (
        PEG14_RENEGADE, 
        [
            (2, half_max_period, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 100, 1),
            (5, 100, 1),
        ]
    ),
    (
        PEG19_ANUBARAK, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 50, 1),
            (0, 100, 1),
            (0,1),
            (max_period, ),
        ]
    ),
    (
        LEG1_LAKSAe, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        LEG1_PIN, 
        [
            (2, max_period, 1),
            (2, max_period//8, 1),
            (11,50,1),
            (3,7,1)
        ]
    ),
    (
        LEG1_IGOGOSHA2, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'),
            (2,period2s_max,1),
            (0.01, 0.4, 0.01),
            (2, max_period, 1),
            (max_period, ),
        ]
    ),
    (
        LEG2_FENNEC, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (11,40,1),
            (11,40,1),
            (0.5,2,0.1),
            (0,1)
        ]
    ),
    (
        LEG2_LYNX, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (0.5,2,0.1),
            (0,1)
        ]
    ),
    (
        LEG2_DRINKER, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (11,40,1),
            (11,40,1),
            (0,1)
        ]
    ),
    (
        LEG2_HOTS, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (11,40,1),
            (11,40,1),
            (0,1)
        ]
    ),
    (
        UEG6_ADVENTURE, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG6_SHERIFF, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (0.1,3,0.1),
        ]
    ),
    (
        WEG3_BATYA, 
        [
            (2, max_period, 1),
            (0.5, 3, 0.1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
    (
        WEG4_PUPPY, 
        [
            (2, max_period, 1),
            (10, 40, 1),
            (10, 40, 1),
        ]
    ),
    (
        SEG1_LITE, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (0.1,1,0.1),
            (2, max_period, 1),
        ]
    ),
)