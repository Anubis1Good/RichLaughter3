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
    # (
    #     PEG2_DDCrWork, 
    #     [
    #         (2,max_period,1),
    #     ]
    # ),
    (
        PEG2_SDDCr, 
        [
            (2,max_period,1),
            (2,max_period,1),
        ]
    ),
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
    (
        PEG4_U3, 
        [
            (2,max_period,1),
            (2,max_period,1),
            (2,15,1),
            (2,15,1),
            ("DC","VG","BB","VC","WC"),
            ("rsi","rsi_tw","mfi","s","uo"),    
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
        PEG8_LOBSTER, 
        [
            (2,max_period,1),
            (0.5,3,0.1),   
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
        ]
    ),
    (
        PEG13_DWDDCr, 
        [
            (2, max_period, 1),
            (5, 40, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG14_RANGER, 
        [
            (2, max_period, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 100, 1),
            (5, 100, 1),
        ]
    ),
    (
        PEG14_RENEGADE, 
        [
            (2, max_period, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 100, 1),
            (5, 100, 1),
        ]
    ),
    (
        PEG14_RWDDCr, 
        [
            (2, max_period, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG15_ANNA, 
        [
            (2, max_period, 1),
            (5, 40, 1),
        ]
    ),
    (
        PEG15_SILVANA, 
        [
            (2, max_period, 1),
            (5, 40, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG16_LEORIC, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG16_CHEN, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG16_ARTANIS, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG17_PHOENIX, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (0, 1),
        ]
    ),
    (
        PEG18_BLAZE, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0, 1),
        ]
    ),
    (
        PEG18_DIABLO, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
        ]
    ),
    (
        PEG18_REXXAR, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
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
            (2, max_period, 1),
        ]
    ),
    (
        PEG18_VARIAN, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
        ]
    ),
    (
        PEG19_CASSIA, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,1),
        ]
    ),
    (
        PEG19_IMPERIUS, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,1),
        ]
    ),
    (
        PEG19_VALEERA, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,30,1),
            (0,1),
        ]
    ),
    (
        PEG19_YREL, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,30,1),
            (0,1),
        ]
    ),
    (
        PEG19_ZERATUL, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,1),
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
        PEG21_AURIEL, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (1.5,3,0.1),
            (2, 10, 1),
            (0,0.5,0.1),
        ]
    ),
    (
        PEG21_MALTHAEL, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (0,0.5,0.1),
            (0,1),
        ]
    ),
    (
        PEG21_WHITEMANE, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, 15, 1),
            (2, 10, 1),
            (1.5,3,0.1),
            (2, 10, 1),
            (0,0.5,0.1),
            (0,1)
        ]
    ),
    # (
    #     PEG22_BERSERK, 
    #     [
    #         (2, max_period, 1),
    #         (2, 15, 1),
    #         (2, 10, 1),
    #         (1.5,3,0.1),
    #         (2, 10, 1),
    #         (0,0.5,0.1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (10,90,1),
    #         (10,90,1),
    #     ]
    # ),
    # (
    #     PEG23_ULTIMATUM, 
    #     [
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #         (2, 15, 1),
    #         (0, 1),
    #         (2, 10, 1),
    #         (1.5,3,0.1),
    #         (2, 10, 1),
    #         (0,0.5,0.1),
    #         (0,1,0.1),
    #         (0, 1),
    #     ]
    # ),
    # (
    #     PEG24_BRIGHTWING, 
    #     [
    #         (2, max_period, 1),
    #         (2, 15, 1),
    #         (2, 10, 1),
    #         (0.1, 1, 0.1),
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
    #         (2, 15, 1),
    #         (2, 10, 1),
    #         (0.1, 1, 0.1),
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
    #         (2, 15, 1),
    #         (2, 10, 1),
    #         (0.1, 1, 0.1),
    #         (0, 1, 0.1),
    #         (0, 0.5, 0.1),
    #         (0.5, 10, 0.5),
    #         (0,max_period,1),
    #         (0, 1),
    #     ]
    # ),
    (
        PEG26_UNKNOWN, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
        ]
    ),

    (
        LEG1_BIBI, 
        [
            (2, max_period, 1),
            (3,15,1),
            (2,30,1),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d')
        ]
    ),
    (
        LEG1_BORSCH, 
        [
            (2, max_period, 1),
        ]
    ),
    (
        LEG1_CC, 
        [
            (2, max_period, 1),
            (2, 20, 1),
            (2, 20, 1),
            (2, 14, 1),
            (2, 10, 1),
            (0.5, 3, 0.1),
            (0, 1),
            (0, 1),
        ]
    ),
    (
        LEG1_IGOGOSHA, 
        [
            (2, max_period, 1),
            (4,15,1),
            (2,30,1),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d')
        ]
    ),
    (
        LEG1_IRONANNY, 
        [
            (2, max_period, 1),
            (4,15,1),
            (2,30,1),
            (2,7,1)
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
        LEG1_OKROSHKA, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
        ]
    ),
    (
        LEG1_PHOBO, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
        ]
    ),
    (
        LEG1_PHOGA, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
        ]
    ),
    (
        LEG1_PIN, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (11,50,1),
            (3,7,1)
        ]
    ),
    (
        LEG2_ALKASH, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (0,30,1),
            (0,1)
        ]
    ),
    (
        LEG2_DRG, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (11,40,1),
            (11,40,1),
            (0,30,1),
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
            (0,30,1),
            (0,1)
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
            (0,30,1),
            (0.5,2,0.1),
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
            (0,30,1),
            (0,1)
        ]
    ),
    (
        LEG2_LOGAN, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (10,50,1),
        ]
    ),
    (
        LEG2_LYNX, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (2, max_period, 1),
            (0,30,1),
            (0.5,2,0.1),
            (0,1)
        ]
    ),
    (
        LEG2_MONSTER, 
        [
            (2, max_period, 1),
            (10,90,1),
            (2, max_period, 1),
            (0,30,1),
            (2, max_period, 1),
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
    (
        SEG2, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
        ]
    ),
    (
        SEG2_FAST, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (10,90,1),
        ]
    ),
    (
        SEG2_ULTRA, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (10,90,1),
        ]
    ),
    (
        SEG3_FORCE, 
        [
            (2, max_period, 1),
            (3,9,1),
            (1,5,1),
            (2,9,1),
            (2, max_period, 1),
            (10,40,1),
            (2, max_period, 1),
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
)
