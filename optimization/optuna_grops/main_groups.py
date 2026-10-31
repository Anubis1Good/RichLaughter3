from strategies.all_egs import *

from optimization.optuna_grops.opt_params import *
# (min, max, step)

# 13.10.2026 каждется надо ввести еще параметр min_period. Ибо 2 - это очень маленький период. Надо хотя бы 5
group = (

    (
        PEG4_U4, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
            ("DC","VG","BB","VC","WC","SC"),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","diff_pedals","real_pedal", "real_wpedal", "real_diff_pedals"),
            (2,period2s_max,1),
            (0.01, 0.5, 0.01),
        ]
    ),
    (
        PEG4_U5, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
            ("DC","VG","BB","VC","WC","SC"),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            (2,period2s_max,1),
            (1,50,1),
            (1,50,1),
        ]
    ),
    (
        PEG4_U6, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
            ("DC","VG","BB","VC","WC"),
            ("rsi","mfi","s","uo","pedal","wpedal","real_pedal", "real_wpedal"),
            (2,period2s_max,1),
            (1,50,1),
            (1,50,1),
            (1,50,1),
            (min_period,max_period,1),
        ]
    ),
    (
        PEG11_KUSURUKEN, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),    
            ('c', 'hl'),    
            (max_period,),
        ]
    ),
        (
        PEG11_RAYMIYAMOTO,
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.5,5,0.1),
            (0.5,5,0.1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            (2,period2s_max,1),
            (max_period,),
            (min_period,max_period,1),
            (10,90,1),
            (1,50,1),
            (1,50,1),
            (1,50,1),
            (1,50,1),
            (0,1),
            (0,20,1),
        ]
    ),
    (
        PEG11_SAYATAKAGI,
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.5,5,0.1),
            (0.5,5,0.1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            (2,period2s_max,1),
            (max_period,),
            (min_period,max_period,1),
            (10,90,1),
            (1,50,1),
            (1,50,1),
            (1,50,1),
            (0,1),
            (0,20,1),
        ]
    ),
    (
        PEG11_ALICEMARASATO,
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.5,5,0.1),
            (0.5,5,0.1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            (2,period2s_max,1),
            (max_period,),
            (min_period,max_period,1),
            (10,90,1),
            (1,50,1),
            (1,50,1),
            (1,50,1),
            (0,1),
            (0,20,1),
            (0,1),
        ]
    ),
    (
        PEG11_SHIZUKAMARIKAWA,
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.5,5,0.1),
            (0.5,5,0.1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            ("rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"),
            (2,period2s_max,1),
            (max_period,),
            (min_period,max_period,1),
            (10,90,1),
            (1,50,1),
            (1,50,1),
            (1,50,1),
            (0,1),
            (0,20,1),
            (0,1),
        ]
    ),

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
    (
        PEG14_RWDDCr, 
        [
            (min_period,max_period,1),
            (1,50,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
        ]
    ),
    (
        PEG14_REGAL, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (1,50,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
        ]
    ),
    (
        PEG14_RANGER, 
        [
            (2, half_max_period, 1),
            (1,50,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (5, 100, 1),
            (5, 100, 1),
        ]
    ),
    (
        PEG14_RENEGADE, 
        [
            (2, half_max_period, 1),
            (1,50,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (5, 100, 1),
            (5, 100, 1),
        ]
    ),

    (
        PEG17_PHOENIX, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (0, 1),
            (max_period,),
        ]
    ),
    (
        PEG17_ZEALOT, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (max_period,),
        ]
    ),
    (
        PEG17_AIUR, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (0, 1),
            (max_period,),
            (0, 1, 0.1),
        ]
    ),
    (
        PEG17_SELENDIS, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (max_period,),
            (min_period,max_period,1),
        ]
    ),
    (
        PEG17_ALDERA, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (max_period,),
            (min_period,max_period,1),
            (0, 50, 1),
        ]
    ),


    (
        PEG26_UNKNOWN, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0, 50, 1),
            (0, 50, 1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
            (0, 1),
        ]
    ),
    (
        PEG26_JUNKRAT, 
        [
            (min_period,max_period,1),
            (0, 50, 1),
            (0, 50, 1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.05, 1 , 0.05),
        ]
    ),
        (
        PEG26_GAZLOWE, 
        [
            (min_period,max_period,1),
            (0, 50, 1),
            (0, 50, 1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0,50,1),
        ]
    ),
    (
        PEG30_ETC, 
        [   
            (0,1),
            (2,200,1),
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
    (
        PEG30_ETC2, 
        [   
            (0,1),
            (2,200,1),
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



    (
        LEG1_IGOGOSHA2, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            ('cmo','rsi','rsi_tw','williams_r','mfi','ultimate_oscillator','cci','%d'),
            (2,period2s_max,1),
            (0.01, 0.4, 0.01),
            (min_period,max_period,1),
            (max_period, ),
        ]
    ),

    (
        LEG1_LAKSAe, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
        ]
    ),


    (
        LEG1_PIN, 
        [
            (min_period,max_period,1),
            (2, max_period//8, 1),
            (1,50,1),
            (3,7,1)
        ]
    ),

    (
        LEG2_DRG, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (min_period,max_period,1),
            (1,50,1),
            (1,50,1),
            (0,1)
        ]
    ),
    (
        LEG2_DRINKER, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (min_period,max_period,1),
            (1,50,1),
            (1,50,1),
            (0,1)
        ]
    ),
    (
        LEG2_FENNEC, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (min_period,max_period,1),
            (1,50,1),
            (1,50,1),
            (0.5,2,0.1),
            (0,1)
        ]
    ),
    (
        LEG2_HOTS, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (min_period,max_period,1),
            (1,50,1),
            (1,50,1),
            (0,1)
        ]
    ),
    (
        LEG2_LOGAN, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (10,90,1),
        ]
    ),
    (
        LEG2_LYNX, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (min_period,max_period,1),
            (0.5,2,0.1),
            (0,1)
        ]
    ),
    (
        LEG3a_LOTR, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0,50,1),
            (max_period,),
   
        ]
    ),
    (
        SEG1_LITE, 
        [
            (min_period,max_period,1),
            (0.5,3,0.1),
            (0.1,1,0.1),
            (min_period,max_period,1),
        ]
    ),

    (
        SEGML2_TUNNELER, 
        [
            (min_period,max_period,1),
            ["std","maxdev","pct"],
            (0.1,10,0.1),
            (0,0.5,0.001),
   
        ]
    ),
    (
        UEG4_CANADIAN, 
        [
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (0,1,0.01)
        ]
    ),
    (
        UEG6_ADVENTURE, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.1,3,0.1),
            (0,1)
        ]
    ),
    (
        UEG6_SURVIVALIST, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (0.1,3,0.1),
            (0,1),
            (0.1,10,0.1),
            (min_period,max_period,1),
            (5,50,1),
            (0,1),
        ]
    ),

   (
        UEG7_LOVERGOOSE, 
        [
            (2, half_max_period, 1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (10,70,1),
            (10,70,1),
            (0,1),
        ]
    ),
    (
        UEG7_LOVERDUCK, 
        [
            (2, half_max_period, 1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (10,70,1),
            (min_period,max_period,1),
            (0,1),
        ]
    ),
    (
        UEG7_CANNIBAL, 
        [
            (min_period,max_period,1),
            (10,70,1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (10, max_period, 1),
            (2, half_max_period, 1),
            (1,10,1),
            (0,1,0.01),
            (2, half_max_period, 1),
        ]
    ),

    (
        UEG9_GRAVY2, 
        [
            (20,max_period,1),
            (0,1,0.01),
            (4,12,2),
            (0,0.5,0.01),
            (0.1,2,0.05),
            (0,1),
        ]
    ),
    
    (
        UEG9_POLITICIAN, 
        [
            (20,max_period,1),
            (0,1,0.01),
            (4,12,2),
            (0,0.5,0.01),
            (0,1),
            (min_period,max_period,1),
            (5,50,1),
        ]
    ),
    (
        UEG9_ASTRAL, 
        [
            (min_period,max_period,1),
            (0,10,0.1),
            (0.05,1,0.01),
        ]
    ),
    (
        UEG9_MEDIUM, 
        [
            (min_period,max_period,1),
            (0,10,0.1),
            (0.05,1,0.01),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
            (0,50,1),
        ]
    ),
    (
        UEG9_TRACKER, 
        [
            (min_period,max_period,1),
            (0,10,0.1),
            (0.05,1,0.01),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (max_period,),
            (0,50,1),
        ]
    ),
    (
        WEG3_BATYA, 
        [
            (min_period,max_period,1),
            (0.5, 3, 0.1),
            (0,1),
            (0,1),
            (0,1),
        ]
    ),
    (
        WEG4_DOG, 
        [
            (min_period,max_period,1),
            (1, 50, 1),
        ]
    ),
    (
        WEG4_PUPPY, 
        [
            (min_period,max_period,1),
            (1, 50, 1),
            (1, 50, 1),
        ]
    ),

    (
        WEG7_PARADOX2, 
        [
            (min_period,max_period,1),
            (0.3,3,0.1),
            (min_period,max_period,1),
            (0.3,3,0.1),
        ]
    ),
    (
        WEG8_MOUSE, 
        [
            (min_period,max_period,1),
            (min_period,max_period,1),
            (1, 50, 1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period,max_period,1),
            (min_period, half_max_period, 1),
            (5, 80, 1),
            (max_period,),
            (0.01, 0.4, 0.01),

        ]
    ),
)
