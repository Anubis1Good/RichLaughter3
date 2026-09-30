from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG,CloseAllEG
from strategies.all_egs import *
# from strategies.PEGs.PEG1_9 import PEG2_DDCrWork
# from strategies.PEGs.PEG30_39 import PEG30_MURKY, PEG31_HYPERION

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
    'CLOSEALL1':(CloseAllEG,tuple(),1,None),
    'CLOSEALL2':(CloseAllEG,tuple(),1,None),
    'CLOSEALL3':(CloseAllEG,tuple(),1,None),
    'CLOSEALL4':(CloseAllEG,tuple(),1,None),
    # 'ETLN1':(TestEG,tuple(),1,None),
    # 'FIXR1':(TestEG,tuple(),1,None),
    # 'MRKC1':(TestEG,tuple(),1,None),
    # 'MTLR1':(TestEG,tuple(),1,None),
    # 'PRMD1':(TestEG,tuple(),1,None),
    # 'SGZH1':(TestEG,tuple(),1,None),
    # 'VSEH1':(TestEG,tuple(),1,None),
    # 'VTBR1':(TestEG,tuple(),1,None),

    # 'OGKB0':(PEG31_HYPERION,(10,3,3,0,1,20,5,1),1,'fg'),
    # 'ETLN0':(PEG31_HYPERION,(5,1,3,0,1,100,20,2,5),1,'fg'),
    # 'TGKA0':(PEG30_MURKY,(10,3),1,'fg'),
    # 'DELI0':(PEG31_HYPERION,(5,1,3,0,1,30,10,2,7),1,'fg'),

    # 'FIXR0':(PEG31_HYPERION,(7,2,2,0,1,10,1,1),1,'fg'),
    # # 'VSEH0':(PEG31_HYPERION,(5,3,3,1,1,40,10,1),1,'fg'),
    # 'PRMD0':(PEG31_HYPERION,(10,4,4,0,1,20,1,1),1,'fg'),
    # 'BTBR0':(PEG31_HYPERION,(5,2,2,1,1,30,1,1),1,'fg'),

    # 'NKNCP':(PEG31_HYPERION,(10,2,2,0,True,10,5,1),1,None), #-
    # 30.09.2026
    'APTK0':(PEG31_HYPERION,(None,2,2,0,1,20,5,1,1,
                            29,21,44,23,15,6),1,'fg'),
    # 30.09.2026
    'DELI0':(PEG31_HYPERION,(None,8,2,0,0,30,1,1,1,
                            32,67,8,29,86,17),1,'fg'), #при 30 выбрал самый верхний аск, хотя внизу было много предложений
    # 'DELI':(PEG30_ETC,(None,8,0,2,1,1,32,67,8,29,86,17),1,'fg'),
    # 30.09.2026
    'ETLN0':(PEG31_HYPERION,(None,None,2,0,0,30,10,1,1,
                            21,55,31,47,88,6),1,'fg'), #имея ордер клацнул еще один ниже, хотя знал про него
    # 'ETLN':(PEG30_ETC,(None,None,0,2,1,1,21,55,31,47,88,6),1,'fg'),
    # 30.09.2026
    'FIXR0':(PEG31_HYPERION,(None,None,2,0,1,10,1,1,1,
                            8,58,68,25,73,19),1,'fg'),
    # 'FIXR':(PEG30_ETC,(None,None,1,14,1,1,8,58,68,25,73,19),1,'fg'),
    # 30.09.2026
    'HYDR0':(PEG30_ETC,(None,34,1,4,1,1,33,37,54,40,55,92),3,'fg'),
    # 30.09.2026
    'SOFL0':(PEG31_HYPERION,(None,6,3,0,1,15,5,1,1,
                            25,41,4,17,50,9),1,'fg'),
    # 'SOFL':(PEG30_ETC,(None,6,1,11,1,1,25,41,4,17,50,9),1,'fg'),
    # 30.09.2026
    'TGKA0':(PEG31_HYPERION,(None,None,5,0,1,20,2,1,1,
                            18,6,40,68,23,16),1,'fg'),
    # 'TGKA':(PEG30_ETC,(None,None,1,7,1,1,18,6,40,68,23,16),1,'fg'),
    # 30.09.2026
    'VSEH0':(PEG31_HYPERION,(None,None,4,0,1,10,1,1,1,
                            32,4,2,31,5,74),1,'fg'),
    # 'VSEH':(PEG30_ETC,(None,49,1,20,1,1,32,4,2,31,5,74),5,'fg'),

    # 'PRMD':(PEG31_HYPERION,(10,4,4,0,True,30,5,1),1,None), #-
    # 'ROLO':(PEG31_HYPERION,(10,2,2,0,True,30,5,1),1,None), #-
    # 'OGKB':(PEG31_HYPERION,(10,2,2,0,True,30,5,1),1,None), #+
    # 'GLRX':(PEG31_HYPERION,(10,2,2,1,True,1,1,1),1,None), #+
    # 'BTBR':(PEG31_HYPERION,(10,2,2,1,True,10,5,1),1,None), #-
    # 'MGKL':(PEG31_HYPERION,(10,2,2,0,True,10,2,1),1,None), #-
    # 'GECO':(PEG31_HYPERION,(10,2,2,0,True,30,10,1),1,None), #-
    # 'MRKC':(PEG31_HYPERION,(10,2,2,0,True,20,1,1),1,None), #+
    # 'GEMC':(PEG31_HYPERION,(10,3,3,0,True,10,1,1),1,None), #+
    # 'ELFV':(PEG31_HYPERION,(10,2,2,0,True,10,5,1),1,None), #-

    # 'SVAV':(PEG31_HYPERION,(10,1,2,0,True,30,10,1),1,None), #-
    # 'DATA':(PEG31_HYPERION,(10,2,3,0,True,50,10,1),1,None), #0
    # 'MVID':(PEG31_HYPERION,(10,1,2,0,True,10,1,2,5),1,None), #+
    # 'ABIO':(PEG31_HYPERION,(10,1,2,0,True,20,1,1),1,None), #0
    # 'RTKMP':(PEG31_HYPERION,(10,1,2,0,True,30,5,1),1,None), #+

    #30.09.26 ?33% +0.9
    'AFLT':(VEG1_MOON,(None,None,16,33,0.94,12,0.3,1,0,0,0),1,None),
    #30.09.26 ?27% +4.4
    'AFLT2':(UEG7_LOVERGOOSE,(None,None,8,22,5,8,42,66,0),1,None),
    #30.09.26 ?18% +7.9
    'ALRS':(LEG1_LAKSAe,(None,15,17,9),2,None),
    #30.09.26 ?31% -2 @
    'ALRS2':(UEG7_CARRIER,(None,None,6,39,9,6,40,20,6,0.49,1.2,0),1,None),

    #29.09.26 ?42% +6.3 $ -1.1
    'ASTR':(PEG11_KUSURUKEN,(None,None,27,16,12,11,'c',60),1,None),
    #30.09.26 ?33% +0.9
    'ASTR2':(LEG1_PIN,(None,None,6,5,37,5),1,None),
    #30.09.26 ?33% +5.3
    'CHMF':(VEG1_EARTH,(None,None,53,0.48,8,0.71,1,0.11,8,0,1,0),1,None),
    #27.09.26 ?22% 
    # 'CHMF2':(UEG8_SOLDIER,(None,None,15,55,0.43,0.95,43,91,58,50,90,36,62,49),1,None),

    #29.09.26 ?34% -6.4 Y +1.6 $
    'FEES':(WEG3_BATYA,(None,None,10,1.6,1,1,1),1,None),
    #27.09.26 ?37% +4.3 +1.8 $ +2 $
    'FEES2':(WEG7_PARADOX,(None,21,20,1.8),2,None),
    #30.09.26 ?17%
    # 'MAGN':(PEG30_ETC,(19,28,1,24,1,1,8,38,6,20,69,8),3,None),
    #20.09.26
    # 'MAGN2':(LEG1_BIBI2,(None,None,2,5,'%d',55,5,0.01),1,None),

    #30.09.26 ?32% +2.5
    'MTLR':(UEG7_CANNIBAL,(None,None,66,37,32,7,2,67,18,5,0.74,21),1,None),
    #30.09.26 ?24% -5.8 N
    # 'MTLR2':(SEG1_LITE,(None,33,31,2.7,0.3,11),3,None),
    #30.09.26 ?28% +1.4
    'NLMK':(PEG17_PHOENIX,(None,None,15,32,61,6,30,0,70),1,None),
    #29.09.26 ?28%
    # 'NLMK2':(WEG3_BATYA,(None,None,50,1.4,1,1,1),1,None),

    #20.09.26 -0.1 +15 +0.6 +0.7 !28%  Y +9.8 +13.6 +3.1
    'RAGR':(LEG1_BIBI2,(None,None,6,50,'williams_r',55,2,0.21),1,None),
    #30.09.26 ?54% -0.9 N @
    # 'RAGR2':(VEG1_MOON,(None,None,15,25,0.71,8,0.56,1,0,1,1),1,None),
    #30.09.26 ?25%
    # 'ROSN':(PEG30_ETC,(None,65,1,28,1,1,22,21,31,63,81,57),6,None),
    #30.09.26 ?24% +2
    'ROSN2':(UEG7_DETECTIVE,(None,38,15,55,27,9,2.1),4,None),

    #29.09.26 ?32% +0.8 $ -7.9 @
    'RUAL':(WEG4_PUPPY,(None,None,14,27,19),1,None),
    #30.09.26 ?24% -2.6
    'RUAL2':(VEG1_EARTH,(None,None,29,0.56,4,0.86,0,0.34,9,0,0,0),1,None),
    #29.09.26 ?9% +2.9 $ 0
    'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #30.09.26 ?7% +0.6 $
    'SBER2':(SEG1_LITE,(None,None,39,2.9,0.8,2),1,None),

    #30.09.26 ?11% -2.2
    'SBERP':(PEG18_ANDUIN,(None,134,38,4.0,47,22,7,12,0,70),12,None),
    #27.09.26 ?12% +0.4 +2.4 $ +1.3 $
    'SBERP2':(WEG3_BATYA,(None,None,60,2.9,1,1,1),1,None),
    #27.09.26 ?42% -4 Y +6.5 +4.6
    'SFIN':(UEG7_CANNIBAL,(None,None,54,56,12,5,5,45,19,10,0.14,17),1,None),
    #29.09.26 ?48% +16.5 +0.7
    'SFIN2':(PEG14_RENEGADE,(None,None,20,40,13,14,39,49),1,None),

    #27.09.26 ?37% -0.9 S +7.3 +10.6
    'ENPG':(UEG9_GRAVY2,(None,23,30,0.85,10,0.31,1.85,1),2,None),
    #27.09.26 ?32% +1.5 +2.7 +3
    'ENPG2':(PEG17_PHOENIX,(None,None,28,46,29,56,5,0,60),1,None),
    #30.09.26 ?19% -3.2
    'SIBN':(VEG1_MOON,(None,86,20,57,0.62,8,0.61,0,0,0,0),8,None),
    #30.09.26 ?16% +5.4
    'SIBN2':(PEG17_PHOENIX,(None,70,65,35,29,2,37,0,70),6,None),

    #30.09.26 ?12% +0.8
    'IRAO':(PEG18_ANDUIN,(None,35,54,1.3,45,9,43,7,0,70),3,None),
    #29.09.26 ?16%
    # 'IRAO2':(PEG14_RENEGADE,(None,None,4,31,11,8,14,77),1,None),
    #20.09.26 +1.2 +5.6 +2.4 +3 !17% S +1.7 +1.5 +5
    'SNGSP':(LEG2_LOGAN,(None,81,12,30,18),7,None),
    #27.09.26 ?24% -0.9 +5 $ -3.6 @
    'SNGSP2':(WEG3_BATYA,(None,None,22,2.8,1,1,1),1,None),

    #30.09.26 ?41% -9.1 N @
    # 'SPBE':(VEG1_EARTH,(None,None,17,0.78,4,0.59,0,0.27,3,0,0,0),1,None),
    #30.09.26 ?33% +5.2
    'SPBE2':(WEG4_DOG,(None,12,50,36),1,None),
    #30.09.26 ?17% +0.8
    'T':(LEG2_LOGAN,(None,99,51,56,26),9,None),
    #29.09.26 ?16% +3.5 +1.7 $
    'T2':(PEG17_PHOENIX,(None,None,18,23,33,2,15,0,60),1,None),

    #30.09.26 ?27% -3.3
    'TATN':(LEG1_BIBI2,(None,None,67,64,'rsi',70,4,0.2),1,None),
    #27.09.26 ?17% 
    # 'TATN2':(WEG4_PUPPY,(None,None,38,40,14),1,None),
    #29.09.26 ?25%  +3 -0.9
    'TATNP':(PEG17_PHOENIX,(None,None,17,16,23,21,10,0,60),1,None),
    #30.09.26 ?33% +8.4
    'TATNP2':(UEG8_SOLDIER,(None,None,8,11,35,0.19,6,0.96,41,0,15,80,20,58,23,90,6,84),1,None),
    
    #29.09.26 ?25% -1.6 +4.9
    'VKCO':(PEG19_ANUBARAK,(None,8,21,10,3,24,38,53,0,60),1,None),
    #30.09.26 ?34% +1.3
    'VKCO2':(UEG6_SHERIFF,(None,None,14,3,2.3),1,None),
    #30.09.26 ?16% +1.6
    'VTBR':(PEG18_BLAZE,(None,97,36,9,27,39,37,0,70),9,None),
    #20.09.26 +1.4 +8.5 +4.1 +5.5 !14% Y -1.9 -1.4 +9.1
    'VTBR2':(LEG2_LYNX,(None,None,47,2.7,7,2.0,0),1,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)