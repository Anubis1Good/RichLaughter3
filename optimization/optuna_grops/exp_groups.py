from strategies.all_egs import *

from optimization.optuna_grops.opt_params import *
group = (    
    # (
    #     PEG4_UNIVERSAL, 
    #     [
    #         (2,max_period,1),
    #         (2,max_period,1),
    #         (5,95,1),
    #         (5,95,1),
    #         ["DC","VG","BB","VC","WC"],
    #         ["rsi","rsi_tw","mfi","s","uo"],      
    #     ]
    # ),

    (
        PEG13_DUNE, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.01,0.4,0.01),
            (max_period,),
            (min_period,max_period,1),
            (0,0.3,0.01),
        ]
    ),

)