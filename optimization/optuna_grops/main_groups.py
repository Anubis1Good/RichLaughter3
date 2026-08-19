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
half_max_period = max_period // 2
max_percent_threshold = 1
group = (
    (
        PEG2_SDDCr, 
        [
            (2,max_period,1),
            (2,max_period,1),
            (max_period,),
        ]
    ),
    (
        PEG4_UNIVERSAL, 
        [
            (2,max_period,1),
            (2,max_period,1),
            (5,45,1),
            (5,45,1),
            ["DC","VG","BB","VC","WC"],
            ["rsi","rsi_tw","mfi","s","uo"],      
        ]
    ),
    (
        PEG4_U3, 
        [
            (2,max_period,1),
            (2,max_period,1),
            (2,half_max_period,1),
            (max_period,),
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
            (max_period,),
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
            (2, half_max_period, 1),
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
            (2, half_max_period, 1),
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
            (max_period,),
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
    # (
    #     PEG16_LEORIC, 
    #     [
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #     ]
    # ),
    # (
    #     PEG16_CHEN, 
    #     [
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #     ]
    # ),
    # (
    #     PEG16_ARTANIS, 
    #     [
    #         (2, max_period, 1),
    #         (2, max_period, 1),
    #     ]
    # ),
    (
        PEG17_PHOENIX, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (0, 1),
            (max_period,),
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
            (max_period,),
        ]
    ),
    (
        PEG18_DIABLO, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (0,1),
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
            (0,1),
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
        PEG18_VARIAN, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (0,1),
        ]
    ),
    (
        PEG19_JOHANNA, 
        [
            (2, max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (0,1),
            (max_period,),
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
            (max_period,),
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
            (max_period,),
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
            (0,max_period,1),
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
            (0,max_period,1),
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
            (max_period,),
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
            (2, half_max_period, 1),
            (max_period,),
            (1.5,3,0.1),
            (2, 4, 1),
            (0,0.5,0.1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG21_MALTHAEL, 
        [
            (2, max_period, 1),
            (2, 15, 1),
            (max_period,),
            (0.1,max_percent_threshold,0.1),
            (0,1),
        ]
    ),
    (
        PEG21_WHITEMANE, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, half_max_period, 1),
            (max_period,),
            (1.5,3,0.1),
            (2, 4, 1),
            (0,0.5,0.1),
            (0,1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG22_BERSERK, 
        [
            (2, half_max_period, 1),
            (2, half_max_period, 1),
            (max_period,),
            (1.5,3,0.1),
            (2, 4, 1),
            (0,0.5,0.1),
            (2, max_period, 1),
            (2, max_period, 1),
            (10,90,1),
            (10,90,1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG22_SONYA, 
        [
            (2, half_max_period, 1),
            (2, 15, 1),
            (max_period,),
            (2, 4, 1),
            (0,0.5,0.1),
            (2, max_period, 1),
            (2, max_period, 1),
            (10,90,1),
            (10,90,1),
            (0.1,max_percent_threshold,0.1), #Если на крупных тф надо увеличивать
        ]
    ),
    (
        PEG23_ULTIMATUM, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, half_max_period, 1),
            (0, 1),
            (max_period,),
            (1.5,3,0.1),
            (2, 4, 1),
            (0,0.5,0.1),
            (0,1,0.1),
            (0, 1),
            (2, max_period, 1),
        ]
    ),
    (
        PEG24_BRIGHTWING, 
        [
            (2, max_period, 1),
            (2, half_max_period, 1),
            (max_period,),
            (0.1, max_percent_threshold, 0.1),
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
            (2, half_max_period, 1),
            (max_period,),
            (0.1, max_percent_threshold, 0.1),
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
            (2, half_max_period, 1),
            (max_period,),
            (0.1, max_percent_threshold, 0.1),
            (0, 1, 0.1),
            (0, 0.5, 0.1),
            (0.5, 10, 0.5),
            (0,40,1),
            (0, 1),
        ]
    ),
    (
        PEG26_UNKNOWN, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (5, 40, 1),
            (5, 40, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (max_period,),
            (0, 1),
        ]
    ),

    (
        LEG1_BIBI, 
        [
            (2, max_period, 1),
            (3,half_max_period,1),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'),
            (max_period, ),
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
        LEG1_CC, 
        [
            (2, max_period, 1),
            (2, half_max_period, 1),
            (max_period, ),
            (2, 14, 1),
            (2, max_period, 1),
            (0.5, 3, 0.1),
            (0, 1),
            (0, 1),
        ]
    ),
    (
        LEG1_IGOGOSHA, 
        [
            (2, max_period, 1),
            (4,half_max_period,1),
            (max_period, ),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'),
        ]
    ),
    (
        LEG1_IRONANNY, 
        [
            (2, max_period, 1),
            (4,half_max_period,1),
            (max_period, ),
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
            (2, max_period, 1),
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
            (0,max_period,1),
            (2, half_max_period, 1),
            (max_period,)
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
            (max_period,)
        ]
    ),
    (
        SEG2_FAST, 
        [
            (2, half_max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (10,90,1),
        ]
    ),
    (
        SEG2_ULTRA, 
        [
            (2, half_max_period, 1),
            (3,10,1),
            (2, max_period, 1),
            (10,90,1),
            (2, max_period, 1),
            (max_period,)
        ]
    ),
    (
        SEG3_FORCE, 
        [
            (2, max_period, 1),
            (0.5,3,0.1),
            (1,5,1),
            (2, half_max_period, 1),
            (10,90,1),
            (2, max_period, 1),
            (0.1, 1, 0.1),
        ]
    ),
 
    (
        UEG2_GGD, 
        [
            (max_period,),
            (2,half_max_period,1),
        ]
    ),
    (
        UEG2_DUCK, 
        [
            (2,half_max_period,1),
            (2,5,1),
        ]
    ),
    (
        UEG2_GOOSE, 
        [
            (2,half_max_period,1),
            (2,5,1),
        ]
    ),
    (
        UEG3_REVAN, 
        [
            (2, max_period, 1),
            (2,20,1),
        ]
    ),
    (
        UEG3_ZEUS, 
        [
            (0.1,max_percent_threshold,0.1),
        ]
    ),
    (
        UEG4_FALCON, 
        [
            (2,half_max_period,1),
            (1,5,1),
            (0,1,0.01)
        ]
    ),
    (
        UEG4_PELICAN, 
        [
            (2, half_max_period, 1),
            (1,5,1),
            (0,1,0.01)
        ]
    ),
    (
        UEG5_HAWK, 
        [
            (2, max_period, 1),
            (2,half_max_period,1),
            (1,5,1),
            (2, max_period, 1),
            (0,1),
            (max_period, ),
            (1,10,0.1),
            (2, 4, 1),
            (0,max_percent_threshold,0.1),
            (0,1,0.01),
            (0,1)
        ]
    ),
    (
        UEG6_ADVENTURE, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (0.1,3,0.1),
            (0,1)
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
            (2, max_period, 1),
            (2, max_period, 1),
            (2, max_period, 1),
            (2,half_max_period,1),
            (1,5,1),
            (0,1,0.01),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG6_SHERIFF, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (0.1,3,0.1),
        ]
    ),
    (
        UEG6_VULTURE, 
        [
            (2, max_period, 1),
            (2, max_period, 1),
            (10,70,1),
            (2, max_period, 1),
            (2,half_max_period,1),
            (1,5,1),
            (0,1,0.01),
            (2, half_max_period, 1),
        ]
    ),
    (
        UEG7_ADVENTURE, 
        [
            (2, max_period, 1),
            (2,half_max_period,1),
            (max_period,),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG7_DODO, 
        [
            (2, half_max_period, 1),
            (2, half_max_period, 1),
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
            (2, half_max_period, 1),
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
            (2, half_max_period, 1),
            (max_period,),
            (2, half_max_period, 1),
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
            (2,half_max_period,1),
            (max_period,),
            (0.1,3,0.1),
        ]
    ),
    (
        UEG7_VULTURE, 
        [
            (2, max_period, 1),
            (10,70,1),
            (2, half_max_period, 1),
            (2,5,1),
            (2, half_max_period, 1),
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
        VEG1_VENUS, 
        [
            (0.1,max_percent_threshold,0.1),
            (0,1,0.1),
            (0.1,0.5,0.1),
            (0.5,2,0.1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
    (
        WEG3_DS, 
        [
            (2, max_period, 1),
        ]
    ),
    (
        WEG4_DOG, 
        [
            (2, max_period, 1),
            (10, 40, 1),
        ]
    ),
    (
        WEG4_PUPPY, 
        [
            (2, max_period, 1),
            (10, 40, 1),
            (10, 40, 1),
        ]
    ),
    (
        WEG4_RAT, 
        [
            (2, max_period, 1),
            (3,half_max_period,1),
            (max_period,),
        ]
    ),
    (
        WEG7_PARADOX, 
        [
            (2, max_period, 1),
            (0.3,3,0.1),
        ]
    ),
)
