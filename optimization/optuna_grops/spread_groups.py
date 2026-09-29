from strategies.all_egs import *

from optimization.optuna_grops.opt_params import *
group = (    
    (
        PEG30_ETC, 
        [   
            (0,1),
            (2,50,1),
            (1,),
            (1,),
            (2,half_max_period,1),
            (2,max_period,1),
            (2,max_period,1),
            (2,max_period,1),
            (5,95,1),
            (5,95,1),  
        ]
    ),



)