from strategies.PEGs.PEG1_9 import *

max_period = 55
group = (
    (
        PEG2_DDCrWork, 
        [
            (1,3,1000),
            (1,3,1000),
            (2,3,max_period),
        ]
    ),
)