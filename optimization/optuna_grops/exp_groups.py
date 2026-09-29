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
    # (
    #     PEG30_ETC, 
    #     [   
    #         (0,1),
    #         (2,200,1),
    #         (1,),
    #         (1,),
    #         (2,half_max_period,1),
    #         (2,max_period,1),
    #         (2,max_period,1),
    #         (2,max_period,1),
    #         (5,95,1),
    #         (5,95,1),  
    #     ]
    # ),
   (
        UEG8_SOLDIER, 
        [
            (1,20,1),
            (2,max_period,1),
            (12,max_period,1),
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


)