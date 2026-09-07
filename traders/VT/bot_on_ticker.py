from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG,CloseAllEG
from strategies.all_egs import *
# from strategies.PEGs.PEG1_9 import PEG2_DDCrWork
# from strategies.PEGs.PEG30_39 import PEG30_MURKY, PEG31_HYPERION

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
    'CLOSEALL':(CloseAllEG,tuple(),1,None),
    # 'ETLN1':(TestEG,tuple(),1,None),
    # 'FIXR1':(TestEG,tuple(),1,None),
    # 'MRKC1':(TestEG,tuple(),1,None),
    # 'MTLR1':(TestEG,tuple(),1,None),
    # 'PRMD1':(TestEG,tuple(),1,None),
    # 'SGZH1':(TestEG,tuple(),1,None),
    # 'VSEH1':(TestEG,tuple(),1,None),
    # 'VTBR1':(TestEG,tuple(),1,None),
    # 'ETLN1':(PEG31_HYPERION,(3,1,0,0,True,100,20,2,10),1,None),
    # 'FIXR1':(PEG31_HYPERION,(4,2,2,0,True,30,10,1),1,None),
    # 'VSEH1':(PEG31_HYPERION,(5,3,3,1,True,40,10,1),1,None),
    # 'PRMD1':(PEG31_HYPERION,(5,5,5,1,True,30,10,1),1,None),
    # 'MRKC1':(PEG31_HYPERION,(3,2,2,0,True,20,5,1),1,None),
    # 'FIXR1':(PEG30_MURKY,(5,1),1,0),
    # 'MRKC1':(PEG30_MURKY,(5,1),1,0),
    # # 'MTLR1':(PEG2_DDCrWork,(30,25,20),2,0),
    # 'PRMD1':(PEG30_MURKY,(5,1),1,0),
    # 'SGZH1':(PEG30_RAYNOR,(5,1),1,0),
    # 'VSEH1':(PEG30_MURKY,(5,1,True,3,True,False),1,0),
    # """stop=None, take=None, min_spred=3, work_direction = 0, work_trend=True, large_open=100,large_close=50, n_order=1, min_step=3, period_adx=14, period_chop=14, period_sma_l=30, period_sma_s=15, thr_adx=25, thr_chop=40"""
    # 'NKNCP':(PEG31_HYPERION,(10,2,2,0,True,10,5,1),1,None), #-
    # 'APTK':(PEG31_HYPERION,(10,2,2,0,True,50,10,1),1,None), #-
    # 'PRMD':(PEG31_HYPERION,(10,4,4,0,True,30,5,1),1,None), #-
    # 'ROLO':(PEG31_HYPERION,(10,2,2,0,True,30,5,1),1,None), #-
    # 'OGKB':(PEG31_HYPERION,(10,2,2,0,True,30,5,1),1,None), #+
    # 'GLRX':(PEG31_HYPERION,(10,2,2,1,True,1,1,1),1,None), #+
    # 'ENPG':(PEG31_HYPERION,(10,3,3,0,True,50,8,1),1,None), #-
    # 'TGKA':(PEG31_HYPERION,(10,2,2,0,True,10,5,1),1,None), #0
    # 'VSEH':(PEG31_HYPERION,(10,3,3,0,True,10,1,1),1,None), #+
    # 'BTBR':(PEG31_HYPERION,(10,2,2,1,True,10,5,1),1,None), #-
    # 'MGKL':(PEG31_HYPERION,(10,2,2,0,True,10,2,1),1,None), #-
    # 'GECO':(PEG31_HYPERION,(10,2,2,0,True,30,10,1),1,None), #-
    # 'FIXR':(PEG31_HYPERION,(10,2,2,0,True,10,1,1),1,None), #+
    # 'MRKC':(PEG31_HYPERION,(10,2,2,0,True,20,1,1),1,None), #+
    # 'GEMC':(PEG31_HYPERION,(10,3,3,0,True,10,1,1),1,None), #+
    # 'ELFV':(PEG31_HYPERION,(10,2,2,0,True,10,5,1),1,None), #-

    # 'ETLN':(PEG31_HYPERION,(10,1,2,0,True,30,10,2,5),1,None), #-
    # 'HYDR':(PEG31_HYPERION,(10,2,2,0,True,100,20,1),1,None), #-
    # 'SVAV':(PEG31_HYPERION,(10,1,2,0,True,30,10,1),1,None), #-
    # 'DATA':(PEG31_HYPERION,(10,2,3,0,True,50,10,1),1,None), #0
    # 'DELI':(PEG31_HYPERION,(10,1,2,0,True,30,1,2,5),1,None), #-
    # 'MVID':(PEG31_HYPERION,(10,1,2,0,True,10,1,2,5),1,None), #+
    # 'ABIO':(PEG31_HYPERION,(10,1,2,0,True,20,1,1),1,None), #0
    # 'RTKMP':(PEG31_HYPERION,(10,1,2,0,True,30,5,1),1,None), #+

    #+1 +10 +10 !(35%) +0.4
    'AFLT':(PEG17_PHOENIX,(None,29,29,12,54,42,6,0,55),3,None), 
    #06.09.26 -0.8
    # 'AFLT2':(LEG2_HOTS,(None,None,43,2.7,6,40,14,0),1,None), 
    # +16 +0 -0 +5 !(44%) -1.4
    'ALRS':(LEG2_DRINKER,(None,16,5,2.1,5,31,16,0),2,None),
    #06.09.26 -2.3
    # 'ALRS2':(LEG1_CC2,(None,8,5,19,55,5,0.6,0,0,3,0.24),1,None),

    #-4 +11 +8 +1 !(40%) +3.1
    'ASTR':(WEG3_BATYA,(None,40,21,2.1,1,1,1),4,None), 
    #06.09.26 -4.2
    # 'ASTR2':(PEG17_PHOENIX,(None,29,10,5,7,35,13,1,55),3,None),
    # +5 -5 +13 +1 !(38%) -2.2
    'CHMF':(VEG1_VENUS,(None,None,0.3,0.8,0.1,2.0,1,0,0),1,None), 
    #06.09.26
    # 'CHMF2':(PEG18_UTER2,(None,None,51,3.3,6,37,45,85,2,0,55,1,0),1,None),

    #06.09.26 -10
    'FEES':(PEG18_UTER2,(None,None,50,2.4,8,27,45,90,19,0,55,1,1),1,None), #из-за оптимизации по сути тупо WDDCr
    #06.09.26 -5.3
    'FEES2':(LEG1_PIN,(None,13,5,2,28,3),2,None),
    #06.09.26 +0.3
    'MAGN':(PEG18_DIABLO2,(None,None,14,2.0,29,26,0,55),1,None),
    #06.09.26
    # 'MAGN2':(PEG18_UTER2,(None,None,7,3.7,37,16,20,62,6,0,55,1,0),1,None),

    #+9 +7 -3 !(29%) +0.6
    'MTLR':(PEG11_KUSURUKEN,(None,None,44,8,51,36,'c',55),1,None), 
    #06.09.26
    # 'MTLR2':(PEG18_REXXAR2,(None,None,3,1.3,39,31,12,0,55),1,None),
    #06.09.26
    # 'NLMK':(LEG2_HOTS,(None,None,30,2.4,3,33,22,0),1,None), 
    #06.09.26
    # 'NLMK2':(LEG1_PIN,(None,13,4,4,40,3),2,None),

    #06.09.26 -1.9
    'RAGR':(LEG1_BIBI2,(None,None,20,20,'cci',55,4,0.37),1,None),
    #06.09.26
    # 'RAGR2':(LEG1_IGOGOSHA2,(None,31,54,12,'williams_r',4,0.24,14,55),3,None),
    #06.09.26 +0.4
    'ROSN':(PEG17_PHOENIX,(None,None,8,50,30,48,5,1,55),1,None),
    #+5 +2 !(33%) -1.3
    'ROSN2':(PEG14_RENEGADE,(None,None,16,38,52,6,49,30),1,None), 

    #06.09.26 +0.9
    'RUAL':(PEG18_UTER,(None,34,19,3,4,39,62,13,1),3,None),
    #06.09.26 -2.1
    # 'RUAL2':(PEG17_PHOENIX,(None,None,4,6,9,47,12,0,55),1,None),
    #06.09.26 -1
    # 'SBER':(LEG2_HOTS,(None,118,13,3.0,8,33,25,0),10,None),
    #06.09.26 +1.2
    'SBER2':(PEG14_RANGER,(None,227,22,33,6,9,8,86),19,None),

    #06.09.26 +1.7
    'SBERP':(UEG6_PIGEON,(None,124,9,20,37,5,3,0.66,2.4,0),11,None),
    #06.09.26 +3.2
    'SBERP2':(PEG17_PHOENIX,(None,164,29,11,48,27,15,1,55),14,None),
    #+22 +6 -9 !(65%) -1.8
    'SFIN':(LEG2_DRINKER,(None,None,42,2.0,4,26,11,0),1,None),
    #+11 -1 !(89%) -3
    'SFIN2':(LEG1_PIN,(None,None,4,6,26,3),1,None), 

    #06.09.26 -2.5
    'ENPG':(LEG1_IRONANNY2,(None,59,40,7,55,5,4,0.4),5,None),
    #06.09.26 -3.9
    # 'ENPG2':(UEG6_VULTURE,(None,None,25,7,57,52,4,1,0.96,11),1,None),
    #06.09.26 -1.3
    # 'SIBN':(PEG18_ANDUIN,(None,None,2,1.7,28,24,5,19,0,55),1,None),
    #06.09.26 +0.8
    'SIBN2':(PEG17_PHOENIX,(None,None,45,35,5,29,7,0,55),1,None),

    #06.09.26 +2.3
    'IRAO':(PEG19_ANUBARAK,(None,None,17,3,11,39,43,91,0,55),1,None),
    #06.09.26 -2.2
    'IRAO2':(LEG1_CC2,(None,None,51,7,55,6,1.6,0,1,2,0.03),1,None),
    #06.09.26 +1.8
    'SNGSP':(LEG1_CC2,(None,74,6,48,55,3,0.5,0,0,2,0.16),7,None),
    #06.09.26 -2.4
    'SNGSP2':(PEG4_UNIVERSAL,(None,72,18,3,23,42,'VC','rsi_tw',6),6,None),

    #+7 +2 +5 !(54%) +5.2
    'SPBE':(PEG11_KUSURUKEN,(None,None,53,8,29,37,'c',55),1,None), 
    #06.09.26 +4.2
    'SPBE2':(UEG6_VULTURE,(None,None,7,32,69,47,3,1,0.07,12),1,None),
    #06.09.26 -1.2
    'T':(UEG6_ADVENTURE,(None,None,55,55,22,1.6,1),1,None), #полдня стоял в боковике и на этом не заработал
    #06.09.26
    # 'T2':(UEG7_ADVENTURE,(None,122,54,4,55,1.6,1),11,None),

    #+5 +9 +11 !(14%) +3.4
    'TATN':(LEG1_PIN,(20,None,48,3,39,3),2,None), 
    #+7 +9 +4 +7 !(9%) +5.5
    'TATN2':(WEG4_PUPPY,(None,None,41,39,11),1,None), 
    #06.09.26 +2.4
    'TATNP':(WEG3_BATYA,(None,None,10,1.9,1,1,1),1,None),
    #+6 +2 +7 !(24%) -2.6
    'TATNP2':(SEG3_FORCE,(None,None,14,3.0,3,9,53,43,0.5),1,None), 
    
    #+14 +10 +2 !(46%) -3
    'VKCO':(PEG17_PHOENIX,(None,None,9,12,50,43,26,0,55),1,None), 
    #06.09.26 -5.6
    # 'VKCO2':(PEG17_PHOENIX,(None,24,5,6,13,35,19,1,55),2,None),
    #06.09.26 +5
    'VTBR':(LEG2_FENNEC,(None,83,54,3.0,7,40,24,1.5,0),7,None),
    #06.09.26 +0.9
    'VTBR2':(WEG3_BATYA,(None,None,16,2.1,1,1,1),1,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)