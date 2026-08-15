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

# (min, max, step)
max_period = 55
group = (
 (
        PEG22_BERSERK, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (1.5,3,0.1),
            (2, 10, 1),
            (0,0.5,0.1),
            (2, max_period, 1),
            (2, max_period, 1),
            (10,90,1),
            (10,90,1),
        ]
    ),
    (
        PEG23_ULTIMATUM, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, 15, 1),
            (0, 1),
            (2, 10, 1),
            (1.5,3,0.1),
            (2, 10, 1),
            (0,0.5,0.1),
            (0,1,0.1),
            (0, 1),
        ]
    ),
    (
        PEG24_BRIGHTWING, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (0.1, 1, 0.1),
            (0, 1, 0.1),
            (0, 0.5, 0.1),
            (0.5, 10, 0.5),
            (0, 1),
        ]
    ),
    (
        PEG24_DEATHWING, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (0.1, 1, 0.1),
            (0, 1, 0.1),
            (0, 0.5, 0.1),
            (0.5, 10, 0.5),
            (0, 1),
        ]
    ),
    (
        PEG25_TASSADAR, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (0.1, 1, 0.1),
            (0, 1, 0.1),
            (0, 0.5, 0.1),
            (0.5, 10, 0.5),
            (0,max_period,1),
            (0, 1),
        ]
    ),
   (
        SEGML2_NEWAVE, 
        [
            (2, max_period, 1),
            (3,10,1),
            (0.5,10,0.5),
            (10,40,1),
        ]
    ),
    (
        SEGML2_TRENDWAVE, 
        [
            (2, max_period, 1),
            (3,10,1),
            (0.5,10,0.5),
            (10,40,1),
            (10,40,1),
        ]
    ),
    # (
    #     SEGML2_SID, 
    #     [
    #         (2, max_period, 1),
    #         (2,30,1),
    #         (2,30,1),
    #         (10,40,1),
    #         (0.1,1,0.1),
    #     ]
    # ),
    (
        SEGML2b_RAPTOR, 
        [
            (2, max_period, 1),
            (1,15,1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (0, 1),
            (0, 1),
            (1,30,1),
        ]
    ),
   (
        UEG9_BIRDWATCHER, 
        [
            (2, max_period, 1),
            (1.5,10,0.5),
            (2,5,1),
            (0,0.3,0.1),
            (0.25,2,0.25),
            (0,1),
            (0,1),
        ]
    ),
    (
        UEG9_GRAVY, 
        [
            (2, max_period, 1),
            (1.5,10,0.5),
            (2,5,1),
            (0,0.3,0.1),
            (0.25,2,0.25),
            (0,1),
        ]
    ),
    (
        VEG1_MERCURY, 
        [
            (2, max_period, 1),
            (0.5,20,0.5),
            (0,1,0.1),
            (0.1,0.5,0.1),
            (0.5,2,0.1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
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