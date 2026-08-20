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

from optimization.optuna_grops.opt_params import *
group = (    
    (
        PEG4_UNIVERSAL, 
        [
            (2,max_period,1),
            (2,max_period,1),
            (5,95,1),
            (5,95,1),
            ["DC","VG","BB","VC","WC"],
            ["rsi","rsi_tw","mfi","s","uo"],      
        ]
    ),
)