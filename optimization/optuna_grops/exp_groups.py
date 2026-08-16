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

max_period = 55
group = (    
    (
        VEG1_VENUS, 
        [
            (2, max_period, 1),
            (0.1,1,0.1),
            (0,1,0.1),
            (0.1,0.5,0.1),
            (0.5,2,0.1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
)