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

    # 30.09.2026 +1.2
    'APTK0':(PEG31_HYPERION,(None,2,2,0,1,20,5,1,10, 29,21,44,23,15,6),1,'fg'),
    # 30.09.2026 +0.2
    'DELI0':(PEG31_HYPERION,(None,8,2,0,0,30,1,1,10, 32,67,8,29,86,17),1,'fg'), 
    # 30.09.2026 -0.8
    'ETLN0':(PEG31_HYPERION,(None,None,2,0,0,30,10,1,10, 21,55,31,47,88,6),1,'fg'),
    # 30.09.2026 -2.6
    'FIXR0':(PEG31_HYPERION,(None,None,2,0,1,10,1,1,10, 8,58,68,25,73,19),1,'fg'),
    # 30.09.2026 -3.8
    'HYDR0':(PEG31_HYPERION,(None,6,8,0,0,15,5,1,10, 26,68,66,36,31,11),1,'fg'),
    # 30.09.2026 +0.4
    'SOFL0':(PEG31_HYPERION,(None,6,3,0,1,15,5,1,10, 25,41,4,17,50,9),1,'fg'),
    # 30.09.2026 +0.4
    'TGKA0':(PEG31_HYPERION,(None,None,5,0,1,20,2,1,10, 18,6,40,68,23,16),1,'fg'),
    # 30.09.2026 -2.5
    'VSEH0':(PEG31_HYPERION,(None,None,4,0,1,10,1,1,10, 32,4,2,31,5,74),1,'fg'),


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

    #11.10.26 ?16%
    'AFLT':(PEG11_ALICEMARASATO,(None,20,9,66,1.6,3.3,24,7,'uo','s',6,70,9,52,26,27,12,0,2,0),2,None),
    #11.10.26 ?10%
    'AFLT2':(PEG13_DUNE,(None,9,4,28,60,54,0.32,70,18,0.14),1,None),
    #11.10.26 ?28%
    'ALRS':(PEG30_ETC2,(None,12,1,7,1,1,34,14,29,26,95,33),1,None),
    #30.09.26 ?18% +7.9 +0.1 $ -0.7 +5.4 $ +5.3 +7.6
    'ALRS2':(LEG1_LAKSAe,(None,15,17,9),2,None),

    #11.10.26 ?31%
    'ASTR':(PEG11_RAYMIYAMOTO,(None,None,36,55,1.0,5.0,20,35,'rsi','wpedal',3,70,36,53,18,31,47,15,0,4),1,None),
    #11.10.26 ?29%
    'ASTR2':(PEG13_DUNE,(None,None,7,6,70,31,0.35,70,25,0.26),1,None),
    #11.10.26 ?23%
    'CHMF':(PEG17_PHOENIX,(None,None,37,47,36,6,44,0,70),1,None),
    #11.10.26 ?27%
    # 'CHMF2':(UEG8_SOLDIER,(None,30,10,55,23,0.52,6,0.65,26,0,31,91,41,16,41,6,82,9),3,None),


    #11.10.26 ?15%
    # 'FEES':(SEG3_FORCE,(None,None,49,1.8,1,28,10,43,0.5),1,None),
    # #27.09.26 ?37% +4.3 +1.8 $ +2 $ -9.3
    # 'FEES2':(WEG7_PARADOX,(None,21,20,1.8),2,None),
    #11.10.26 ?28%
    'MAGN':(VEG1_MOON,(None,None,15,64,0.95,12,0.41,0,0,0,0),1,None),
    #04.10.26 ?16% +3.4 +3.5 $ -0.4 +4.9
    'MAGN2':(PEG30_ETC2,(17,34,0,23,1,1,28,58,5,62,88,27),3,None),

    #11.10.26 ?30%
    'MTLR':(UEG8_SOLDIER,(None,None,19,45,37,0.22,4,0.91,46,0,77,92,6,15,46,59,60,61),1,None),
    #11.10.26 ?30%
    'MTLR2':(LEG2_FENNEC,(None,33,25,2.4,10,38,19,1.7,0),3,None),
    #11.10.26 ?27%
    'NLMK':(LEG1_BIBI2,(None,None,9,28,'williams_r',70,4,0.05),1,None),
    #11.10.26 ?28%
    # 'NLMK2':(PEG30_ETC,(None,None,1,11,1,1,16,7,14,8,5,24),1,None),

    #11.10.26 ?42%
    'RAGR':(UEG9_POLITICIAN,(None,None,63,0.9,6,0.43,0,51,25),1,None),
    #04.10.26 ?43% -0.3 -2.9 @ +0.9 +2.8
    'RAGR2':(LEG2_LYNX,(None,30,4,2.5,46,1.9,0),3,None),
    #11.10.26 ?22%
    'ROSN':(PEG13_DUNE,(None,None,11,59,70,11,0.15,70,24,0.24),1,None),
    #04.10.26 ?13% +2 -0.5 @ -16.4
    # 'ROSN2':(UEG4_CANADIAN,(None,16,43,25,3,0.79),2,None),

    #11.10.26 ?30%
    'RUAL':(SEG3_FORCE,(None,None,63,2.2,2,26,27,46,0.2),1,None),
    #30.09.26 ?24% -2.6 +4.7 !26% +17.8 +4.9 +7.5 -2.7
    'RUAL2':(VEG1_EARTH,(None,None,29,0.56,4,0.86,0,0.34,9,0,0,0),1,None),
    #29.09.26 ?9% +2.9 $ 0 -2.9 @ !4% -4.8
    # 'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #04.10.26 ?7% -4.3
    # 'SBER2':(PEG17_TEMPLAR,(None,201,66,9,44,24,0,70),17,None),

    #27.09.26 ?12% +0.4 +2.4 $ +1.3 $ +2.6 $ -4.5 +1.3 $ +2 +1.9
    'SBERP':(WEG3_BATYA,(None,None,60,2.9,1,1,1),1,None),
    #04.10.26 ?11% -4.7 S +0 @ -1.2 @
    # 'SBERP2':(UEG7_CARRIER,(None,None,4,42,4,1,42,13,3,0.69,1.3,0),1,None),
    #11.10.26 ?49%
    'SFIN':(PEG11_RAYMIYAMOTO,(None,None,57,54,1.2,2.8,32,48,'real_pedal','rsi',7,70,67,81,18,36,24,27,1,7),1,None),
    #11.10.26 ?35%
    'SFIN2':(UEG9_GRAVY2,(None,19,46,0.98,8,0.48,1.95,0),2,None),

    #11.10.26 ?23%
    'ENPG':(PEG14_REGAL,(None,None,3,2,44,7,57,13,70),1,None),
    #11.10.26 ?23%
    'ENPG2':(VEG1_MOON,(None,None,4,31,0.93,6,0.22,0,0,1,0),1,None),
    #30.09.26 ?16% +5.4 +6.1 !16% -0.6 -2.5 +8 +5.2
    'SIBN':(PEG17_PHOENIX,(None,70,65,35,29,2,37,0,70),6,None),
    #11.10.26 ?12%
    # 'SIBN2':(LEG2_HOTS,(None,98,46,2.1,9,29,15,1),9,None),

    #11.10.26 ?19%
    'IRAO':(WEG8_MOUSE,(None,None,3,18,44,64,52,8,29,17,70,0.18),1,None),
    #30.09.26 ?12% +0.8 +4.9 +1.6 +7.4 -2.4 -7.1
    # 'IRAO2':(PEG18_ANDUIN,(None,35,54,1.3,45,9,43,7,0,70),3,None),
    #04.10.26 ?18% +1.2 $ +5.6
    'SNGSP':(WEG4_DOG,(None,None,12,23),1,None),
    #04.10.26 ?16% +13.1 +1.2 +0.7
    'SNGSP2':(PEG17_PHOENIX,(None,54,13,58,36,53,22,0,70),5,None),

    #11.10.26 ?33%
    'SPBE':(VEG1_EARTH,(None,None,21,0.62,4,0.15,0,0.25,12,0,1,0),1,None),
    #11.10.26 ?16%
    'SPBE2':(PEG14_RANGER,(None,5,34,21,32,8,27,47),1,None),
    #11.10.26 ?11%
    'T':(LEG1_IGOGOSHA2,(None,None,49,47,'ultimate_oscillator',3,0.09,27,70),1,None),
    #11.10.26 ?7%
    'T2':(UEG7_LOVERGOOSE,(None,15,10,51,25,10,60,64,1),2,None),

    #04.10.26 ?17% -1.2 @ +1.3 +7.4 +0.2
    'TATN':(PEG17_ZEALOT,(None,None,10,8,45,53,6,70),1,None),
    #11.10.26 ?25%
    'TATN2':(PEG14_RENEGADE,(None,None,9,35,11,6,12,70),1,None),
    #04.10.26 ?27% +9 +4.1
    'TATNP':(LEG2_FENNEC,(None,None,21,3.0,8,36,16,1.0,0),1,None),
    #30.09.26 ?33% +8.4 +2.2 !27% +3.8 +4.9 +5 +4.5
    'TATNP2':(UEG8_SOLDIER,(None,None,8,11,35,0.19,6,0.96,41,0,15,80,20,58,23,90,6,84),1,None),
    
    #11.10.26 ?31%
    'VKCO':(LEG1_IRONANNY2,(None,None,9,7,70,6,5,0.13),1,None),
    #04.10.26 ?33% +2.5 $ +1.5 -6.2 @
    # 'VKCO2':(PEG30_ETC2,(None,13,0,9,1,1,34,64,62,57,89,22),1,None),
    #11.10.26 ?27%
    'VTBR':(UEG7_DETECTIVE,(None,95,65,56,17,8,2.5),8,None),
    #11.10.26 ?17%
    'VTBR2':(PEG17_PHOENIX,(None,33,37,41,59,22,18,0,70),3,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)