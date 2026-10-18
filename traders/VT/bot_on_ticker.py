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

    #18.10.26 ?12%
    'AFLT':(WEG3_BATYA,(None,7,18,1.9,1,1,1),1,None),
    #11.10.26 ?15% +8 +4.7
    'AFLT2':(UEG6_SURVIVALIST,(None,None,16,9,1.4,1,2.7,26,29,0),1,None),
    #18.10.26 ?29%
    'ALRS':(VEG1_MOON,(None,18,19,51,0.77,6,0.33,1,1,0,0),2,None),
    #11.10.26 ?28% +21.4 +7.7 -0.7 +0.2
    'ALRS2':(PEG30_ETC2,(None,12,1,7,1,1,34,14,29,26,95,33),1,None),

    #11.10.26 ?31% +5.4 +11.2 -1.8 +8.1
    'ASTR':(PEG11_RAYMIYAMOTO,(None,None,36,55,1.0,5.0,20,35,'rsi','wpedal',3,70,36,53,18,31,47,15,0,4),1,None),
    #11.10.26 ?29% +4.4 +3.6 +4.5 +5.3
    'ASTR2':(PEG13_DUNE,(None,None,7,6,70,31,0.35,70,25,0.26),1,None),
    #18.10.26 ?23%
    'CHMF':(PEG30_ETC,(None,10,1,5,1,1,11,6,37,15,14,65),1,None),
    #11.10.26 ?23% -1.1 +0.3 +11.5 -0.7
    'CHMF2':(PEG17_PHOENIX,(None,None,37,47,36,6,44,0,70),1,None),


    #11.10.26 ?15%
    # 'FEES':(SEG3_FORCE,(None,None,49,1.8,1,28,10,43,0.5),1,None),
    # #27.09.26 ?37% +4.3 +1.8 $ +2 $ -9.3
    # 'FEES2':(WEG7_PARADOX,(None,21,20,1.8),2,None),
    #18.10.26 ?31%
    'MAGN':(VEG1_MOON,(None,None,13,64,0.98,12,0.07,0,1,0,0),1,None),
    #04.10.26 ?16% +3.4 +3.5 $ -0.4 +4.9 +11.5 +1.8 +7.5 -1.6
    'MAGN2':(PEG30_ETC2,(17,34,0,23,1,1,28,58,5,62,88,27),3,None),

    #18.10.26 ?36%
    'MTLR':(UEG8_SOLDIER,(None,38,10,63,27,0.21,4,0.31,11,0,74,41,46,62,87,80,64,44),4,None),
    #18.10.26 ?31%
    'MTLR2':(UEG6_SURVIVALIST,(None,None,16,12,2.0,0,2.4,32,36,0),1,None),
    #18.10.26 ?24%
    'NLMK':(WEG3_BATYA,(None,None,23,1.1,0,1,1),1,None),
    #13.10.26 -0.8 +3
    'NLMK2':(PEG30_ETC,(None,8,1,11,1,1,16,7,14,8,5,24),1,None),

    #18.10.26 ?41%
    'RAGR':(UEG9_POLITICIAN,(None,None,64,1.0,4,0.41,0,19,9),1,None),
    #11.10.26 ?18% +4.2 +5.3 +1.3
    'RAGR2':(SEG1_LITE,(None,17,61,1.6,0.1,32),2,None),
    #11.10.26 ?22% +13.5 +3.3 +2.1 +2
    'ROSN':(PEG13_DUNE,(None,None,11,59,70,11,0.15,70,24,0.24),1,None),
    #18.10.26 ?26%
    'ROSN2':(PEG13_DUNE,(None,None,11,20,63,13,0.1,70,54,0.27),1,None),

    #18.10.26 ?26%с461wr76%
    'RUAL':(UEG6_PIGEON,(None,47,13,5,70,5,5,0.26,2.9,0),4,None),
    #18.10.26 ?16%c112wr91%
    'RUAL2':(PEG17_PROBIUS,(None,10,58,63,61,26,6,70,49),1,None),
    #29.09.26 ?9% +2.9 $ 0 -2.9 @ !4% -4.8
    # 'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #04.10.26 ?7% -4.3
    # 'SBER2':(PEG17_TEMPLAR,(None,201,66,9,44,24,0,70),17,None),

    #18.10.26 ?9%
    'SBERP':(PEG17_PHOENIX,(None,185,37,24,23,44,23,0,70),16,None),
    #04.10.26 ?11% -4.7 S +0 @ -1.2 @
    # 'SBERP2':(UEG7_CARRIER,(None,None,4,42,4,1,42,13,3,0.69,1.3,0),1,None),
    #18.10.26 ?42%
    'SFIN':(PEG11_RAYMIYAMOTO,(None,None,51,48,4.6,0.6,28,17,'uo','mfi',8,70,67,85,41,50,48,42,1,14),1,None),
    #18.10.26 ?40%
    'SFIN2':(UEG6_SURVIVALIST,(None,None,27,42,2.9,0,8.1,67,33,0),1,None),

    #18.10.26 ?33%
    'ENPG':(VEG1_MOON,(None,None,8,30,0.3,4,0.21,0,0,1,0),1,None),
    #18.10.26 ?38%
    'ENPG2':(VEG1_EARTH,(None,59,65,0.68,8,0.54,0,0.56,9,0,0,0),5,None),
    #30.09.26 ?16% +5.4 +6.1 !16% -0.6 -2.5 +8 +5.2 +6.5 $ +3.2 -11.3
    'SIBN':(PEG17_PHOENIX,(None,70,65,35,29,2,37,0,70),6,None),
    #18.10.26 ?11%
    'SIBN2':(PEG30_ETC2,(None,30,0,47,1,1,19,29,41,51,91,25),3,None),

    #18.10.26 ?15%
    'IRAO':(PEG13_DUNE,(20,None,6,31,65,49,0.33,70,62,0.19),2,None),
    #18.10.26 ?15%
    'IRAO2':(PEG17_PHOENIX,(None,22,56,15,67,5,23,0,70),2,None),
    #04.10.26 ?18% +1.2 $ +5.6 -3.3 +3 +1.4 +0.1
    'SNGSP':(WEG4_DOG,(None,None,12,23),1,None),
    #04.10.26 ?16% +13.1 +1.2 +0.7 +6.9 +8.9 -1.1 +4.6
    'SNGSP2':(PEG17_PHOENIX,(None,54,13,58,36,53,22,0,70),5,None),

    #18.10.26 ?15%
    'SPBE':(PEG14_REGAL,(None,6,8,10,31,11,18,61,70),1,None),
    #11.10.26 ?16% +5 +1.8 +7.4 +1.1
    'SPBE2':(PEG14_RANGER,(None,5,34,21,32,8,27,47),1,None),
    #11.10.26 ?11% +1.5 +5.3 -4.1 -1.3
    # 'T':(LEG1_IGOGOSHA2,(None,None,49,47,'ultimate_oscillator',3,0.09,27,70),1,None),
    #11.10.26 ?7% +1.5 -0.5 +0.9 -1.9
    # 'T2':(UEG7_LOVERGOOSE,(None,15,10,51,25,10,60,64,1),2,None),

    #04.10.26 ?17% -1.2 @ +1.3 +7.4 +0.2 +25 $ +6.8 -4.2
    'TATN':(PEG17_ZEALOT,(None,None,10,8,45,53,6,70),1,None),
    #11.10.26 ?25% +28.7 -0.2 -2.6
    'TATN2':(PEG14_RENEGADE,(None,None,9,35,11,6,12,70),1,None),
    #04.10.26 ?27% +9 +4.1 +8.4 +7.7 -6.4
    'TATNP':(LEG2_FENNEC,(None,None,21,3.0,8,36,16,1.0,0),1,None),
    #30.09.26 ?33% +8.4 +2.2 !27% +3.8 +4.9 +5 +4.5 -3.4 +5.7 -5.5
    'TATNP2':(UEG8_SOLDIER,(None,None,8,11,35,0.19,6,0.96,41,0,15,80,20,58,23,90,6,84),1,None),
    
    #18.10.26 ?15%
    'VKCO':(PEG17_PROBIUS,(None,9,24,7,46,43,43,70,12),1,None),
    #04.10.26 ?33% +2.5 $ +1.5 -6.2 @
    # 'VKCO2':(PEG30_ETC2,(None,13,0,9,1,1,34,64,62,57,89,22),1,None),
    #18.10.26 ?24%
    'VTBR':(UEG7_DETECTIVE,(None,103,24,51,18,6,2.1),9,None),
    #11.10.26 ?17% -1.2 +1.7
    'VTBR2':(PEG17_SELENDIS,(None,45,53,20,39,55,26,70),4,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)