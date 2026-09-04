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
    # (
    #     PEG19_JOHANNA, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (5, 40, 1),
    #         (5, 40, 1),
    #         (0,1),
    #         (max_period,),
    #     ]
    # ),
    # (
    #     PEG19_CASSIA, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (5, 40, 1),
    #         (5, 40, 1),
    #         (0,1),
    #         (max_period,),
    #     ]
    # ),
    # (
    #     PEG19_IMPERIUS, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (5, 40, 1),
    #         (5, 40, 1),
    #         (0,1),
    #         (max_period,),
    #     ]
    # ),
    # (
    #     PEG19_VALEERA, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (5, 40, 1),
    #         (5, 40, 1),
    #         (0,max_period,1),
    #         (0,1),
    #     ]
    # ),
    # (
    #     PEG19_YREL, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (5, 40, 1),
    #         (5, 40, 1),
    #         (0,max_period,1),
    #         (0,1),
    #     ]
    # ),
    # (
    #     PEG19_ZERATUL, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (5, 40, 1),
    #         (5, 40, 1),
    #         (0,1),
    #         (max_period,),
    #     ]
    # ),
        # (
    #     PEG21_AURIEL, 
    #     [
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (1.5,3,0.1),
    #         (2, 4, 1),
    #         (0,0.5,0.1),
    #         (2, max_period, 1),
    #     ]
    # ),
    # (
    #     PEG21_MALTHAEL, 
    #     [
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (0.1,max_percent_threshold,0.1),
    #         (0,1),
    #     ]
    # ),
    # (
    #     PEG21_WHITEMANE, 
    #     [
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (1.5,3,0.1),
    #         (2, 4, 1),
    #         (0,0.5,0.1),
    #         (0,1),
    #         (2, max_period, 1),
    #     ]
    # ),
    # (
    #     PEG22_BERSERK, 
    #     [
    #         (2, half_max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (1.5,3,0.1),
    #         (2, 4, 1),
    #         (0,0.5,0.1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (10,90,1),
    #         (10,90,1),
    #         (2, max_period, 1),
    #     ]
    # ),
    # (
    #     PEG22_SONYA, 
    #     [
    #         (2, half_max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (2, 4, 1),
    #         (0,0.5,0.1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (10,90,1),
    #         (10,90,1),
    #         (0.1,max_percent_threshold,0.1), #Если на крупных тф надо увеличивать
    #     ]
    # ),
    # (
    #     PEG23_ULTIMATUM, 
    #     [
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (0, 1),
    #         (max_period,),
    #         (1.5,3,0.1),
    #         (2, 4, 1),
    #         (0,0.5,0.1),
    #         (0,1,0.1),
    #         (0, 1),
    #         (2, max_period, 1),
    #     ]
    # ),
    # (
    #     PEG24_BRIGHTWING, 
    #     [
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (0.1, max_percent_threshold, 0.1),
    #         (0, 1, 0.1),
    #         (0, 0.5, 0.1),
    #         (0.5, 10, 0.5),
    #         (0, 1),
    #     ]
    # ),
    # (
    #     PEG24_DEATHWING, 
    #     [
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (0.1, max_percent_threshold, 0.1),
    #         (0, 1, 0.1),
    #         (0, 0.5, 0.1),
    #         (0.5, 10, 0.5),
    #         (0, 1),
    #     ]
    # ),
    # (
    #     PEG25_TASSADAR, 
    #     [
    #         (2, max_period, 1),
    #         (2, period_fractal_max, 1),
    #         (max_period,),
    #         (0.1, max_percent_threshold, 0.1),
    #         (0, 1, 0.1),
    #         (0, 0.5, 0.1),
    #         (0.5, 10, 0.5),
    #         (0,40,1),
    #         (0, 1),
    #     ]
    # ),
    # # (
    # #     PEG16_LEORIC, 
    # #     [
    # #         (2, max_period, 1),
    # #         (2, max_period, 1),
    # #     ]
    # # ),
    # # (
    # #     PEG16_CHEN, 
    # #     [
    # #         (2, max_period, 1),
    # #         (2, max_period, 1),
    # #     ]
    # # ),
    # # (
    # #     PEG16_ARTANIS, 
    # #     [
    # #         (2, max_period, 1),
    # #         (2, max_period, 1),
    # #     ]
    # # ),

        # (
    #     SEG2, 
    #     [
    #         (2, max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (max_period,)
    #     ]
    # ),
    # (
    #     SEG2_FAST, 
    #     [
    #         (2, half_max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (10,90,1),
    #     ]
    # ),
    # (
    #     SEG2_ULTRA, 
    #     [
    #         (2, half_max_period, 1),
    #         (3,10,1),
    #         (2, max_period, 1),
    #         (10,90,1),
    #         (2, max_period, 1),
    #         (max_period,)
    #     ]
    # ),
        # (
    #     UEG5_HAWK, 
    #     [
    #         (2, max_period, 1),
    #         (2,period_fractal_max,1),
    #         (1,5,1),
    #         (2, max_period, 1),
    #         (0,1),
    #         (max_period, ),
    #         (1,10,0.1),
    #         (2, 4, 1),
    #         (0,max_percent_threshold,0.1),
    #         (0,1,0.01),
    #         (0,1)
    #     ]
    # ),
)