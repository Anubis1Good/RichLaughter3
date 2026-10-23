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

        (
        PEG8_DOBBY, 
        [
            (2,max_period,1),
            (0.5,3,0.1),   
        ]
    ),
        (
        PEG13_DWDDCr, 
        [
            (min_period,max_period,1),
            (5, 45, 1),
            (min_period,max_period,1),
        ]
    ),
        (
        PEG15_ANNA, 
        [
            (min_period,max_period,1),
            (5, 45, 1),
        ]
    ),
    (
        PEG15_SILVANA, 
        [
            (min_period,max_period,1),
            (5, 45, 1),
            (min_period,max_period,1),
        ]
    ),
        (
        PEG17_PROBIUS, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (max_period,),
            (0, 50, 1),
        ]
    ),
        (
        PEG17_TEMPLAR, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (max_period,),
        ]
    ),
        (
        PEG17_ARCHON, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (max_period,),
        ]
    ),
        (
        PEG18_BLAZE, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (5, 40, 1),
            (5, 40, 1),
            (0, 1),
            (max_period,),
        ]
    ),

    (
        PEG18_ANDUIN, 
        [
            (min_period,max_period,1),
            (0.5,4,0.1),
            (min_period,max_period,1),
            (5, 40, 1),
            (5, 70, 1),
            (2, half_max_period, 1),
            (0,1),
            (max_period, ),
        ]
    ),
    (
        PEG19_ANUBARAK, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (5, 40, 1),
            (5, 50, 1),
            (0, 100, 1),
            (0,1),
            (max_period, ),
        ]
    ),
        (
        PEG18_REXXAR2, 
        [
            (2, max_period, 1),
            (0.5,4,0.1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,1),
            (max_period, ),
        ]
    ),
    (
        PEG18_UTER, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 90, 1),
            (2, half_max_period, 1),
            (0,1),
        ]
    ),
        (
        PEG18_UTER2, 
        [
            (2, max_period, 1),
            (0.5,4,0.1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 45, 1),
            (5, 90, 1),
            (2, half_max_period, 1),
            (0,1),
            (max_period, ),
            (0,1),
            (0,1),
        ]
    ),
        (
        PEG18_VARIAN2, 
        [
            (2, max_period, 1),
            (0.5,4,0.1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (0,1),
            (max_period, ),
        ]
    ),
        (
        PEG18_DIABLO2, 
        [
            (2, max_period, 1),
            (0.5,4,0.1),
            (2, max_period, 1),
            (5, 40, 1),
            (0,1),
            (max_period, ),
        ]
    ),
        (
        PEG20_HOGGER, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (0.5,3,0.1),
            (0.5,3,0.1),
            (5, 40, 1),
            (5, 40, 1),

        ]
    ),
        (
        LEG2_ALKASH, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (0,1)
        ]
    ),
        (
        LEG1_CC2, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period, ),
            (2, 13, 1),
            (0.5, 3, 0.1),
            (0, 1),
            (0, 1),
            (2,period2s_max,1),
            (0.01, 0.4, 0.01),
        ]
    ),
        (
        LEG1_BIBI2, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'),
            (max_period, ),
            (2,period2s_max,1),
            (0.01, 0.4, 0.01),
        ]
    ),
        (
        LEG1_IRONANNY2, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period, ),
            (2,8,1),
            (2,period2s_max,1),
            (0.01, 0.4, 0.01),
        ]
    ),
        (
        LEG1_OKROSHKA, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
        ]
    ),
        (
        SEG3_FORCE, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (1,5,1),
            (2, half_max_period, 1),
            (10,90,1),
            (min_period,max_period,1),
            (0.1, max_percent_threshold, 0.1),
        ]
    ),
        (
        UEG6_DODO, 
        [
            (2, half_max_period, 1),
            (2, max_period, 1),
            (10,70,1),
            (10,70,1),
        ]
    ),
    (
        UEG6_DUELDODO, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (10,70,1),
            (2, max_period, 1),
            (0,1),
            (2, half_max_period, 1),
        ]
    ),
        (
        UEG6_PIGEON, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (2,period_fractal_max,1),
            (1,5,1),
            (0,1,0.01),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG6_SHERIFF, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.1,3,0.1),
        ]
    ),
    (
        UEG6_VULTURE, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (10,70,1),
            (min_period,max_period,1),
            (2,period_fractal_max,1),
            (1,5,1),
            (0,1,0.01),
            (2, half_max_period, 1),
        ]
    ),
        (
        UEG7_CELEBRITY, 
        [
            (min_period,max_period,1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG7_CARRIER, 
        [
            (min_period,max_period,1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (0,1,0.01),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG7_DETECTIVE, 
        [
            (min_period,max_period,1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (0.1,3,0.1),
        ]
    ),
        (
        UEG7_ADVENTURE, 
        [
            (2, max_period, 1),
            (2,period_fractal_max,1),
            (max_period,),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG7_DODO, 
        [
            (2, half_max_period, 1),
            (2, period_fractal_max, 1),
            (max_period,),
            (10,70,1),
            (10,70,1),
            (0,1),
        ]
    ),
    (
        UEG7_DUELDODO, 
        [
            (2, half_max_period, 1),
            (2, period_fractal_max, 1),
            (max_period,),
            (10,70,1),
            (2, max_period, 1),
            (0,1)
        ]
    ),
    (
        UEG7_PIGEON, 
        [
            (2, max_period, 1),
            (2, period_fractal_max, 1),
            (max_period,),
            (2, period_fractal_max, 1),
            (1,5,1),
            (0,1,0.01),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG7_SHERIFF, 
        [
            (2, max_period, 1),
            (2,period_fractal_max,1),
            (max_period,),
            (0.1,3,0.1),
        ]
    ),
    (
        UEG7_VULTURE, 
        [
            (2, max_period, 1),
            (10,70,1),
            (2, period_fractal_max, 1),
            (2,5,1),
            (2, period_fractal_max, 1),
            (max_period,),
            (0,1,0.01),
            (2, half_max_period, 1),
        ]
    ),
        (
        UEG8_AVENGER, 
        [
            (2,20,1),
            (0,max_percent_threshold,0.1),
            (0,1,0.1),
            (0.1,1,0.1),
            (0.5,10,0.5),
            (0,1)
        ]
    ),
       (
        UEG8_SOLDIER, 
        [
            (1,20,1),
            (min_period,max_period,1),
            (20,max_period,1),
            (0,1,0.01),
            (4,12,2),
            (0,1,0.01),
            (10,50,1),
            (0,1),
            (0,99,1),
            (0,99,1),
            (0,99,1),
            (0,99,1),
            (0,99,1),
            (0,99,1),
            (0,99,1),
            (0,99,1),
        ]
    ),
        (
        UEG9_BIRDWATCHER2, 
        [
            (30,max_period,1),
            (0,1,0.01),
            (4,12,2),
            (0,0.5,0.01),
            (0.1,2,0.05),
            (0,1,0.01),
            (0,1),
            (0,1),
        ]
    ),
    
        (
        WEG10_sleep, 
        [
            (2,max_period,1),
            (0.5,3,0.1),
            (2,max_period,1),
            (max_period,),
            (0,1),

        ]
    ),
    # (
    #     WEG10_sonny, 
    #     [
    #         (2,max_period,1),
    #         (0.5,3,0.1),
    #         (2,max_period,1),
    #         (max_period,),
    #         (0,1),
    #         (0.01, 0.99, 0.01),
    #     ]
    # ),
        (
        VEG1_MOON, 
        [
            (2,20,1),
            (20,max_period,1),
            (0,1,0.01),
            (4,12,2),
            (0,1,0.01),
            (0,1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
        (
        VEG1_EARTH, 
        [   
            (20,max_period,1),
            (0,1,0.01),
            (4,12,2),
            (0,1,0.01),
            (0,1),
            (0,1,0.01),
            (2,20,1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
)