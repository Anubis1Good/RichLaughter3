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

    'OGKB0':(PEG31_HYPERION,(10,3,3,0,1,20,5,1),1,'fg'),
    'ETLN0':(PEG31_HYPERION,(5,1,3,0,1,100,20,2,5),1,'fg'),
    'TGKA0':(PEG30_MURKY,(10,3),1,'fg'),
    'DELI0':(PEG31_HYPERION,(5,1,3,0,1,30,10,2,7),1,'fg'),

    'FIXR0':(PEG31_HYPERION,(7,2,2,0,1,10,1,1),1,'fg'),
    # 'VSEH0':(PEG31_HYPERION,(5,3,3,1,1,40,10,1),1,'fg'),
    'PRMD0':(PEG31_HYPERION,(10,4,4,0,1,20,1,1),1,'fg'),
    'BTBR0':(PEG31_HYPERION,(5,2,2,1,1,30,1,1),1,'fg'),

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

    #+1 +10 +10 !(35%) +0.4 +3.7 +2.4 -2.2 -0.5
    'AFLT':(PEG17_PHOENIX,(None,29,29,12,54,42,6,0,55),3,None), 
    #20.09.26
    # 'AFLT2':(LEG1_PIN,(None,19,2,4,19,4),2,None),
    #20.09.26
    'ALRS':(PEG18_BLAZE,(None,9,34,11,54,29,23,0,55),1,None),
    #20.09.26
    # 'ALRS2':(LEG2_FENNEC,(None,None,3,2.0,23,38,20,1.8,1),1,None),

    #20.09.26
    'ASTR':(PEG18_UTER2,(None,40,7,3.9,4,15,14,59,10,0,55,1,0),4,None),
    #20.09.26
    'ASTR2':(PEG4_UNIVERSAL,(None,19,13,12,29,18,'WC','mfi',5),2,None),
    # +5 -5 +13 +1 !(38%) -2.2 -17.1 +3.5 +1.7 -9
    # 'CHMF':(VEG1_VENUS,(None,None,0.3,0.8,0.1,2.0,1,0,0),1,None), 
    #06.09.26
    # 'CHMF2':(PEG18_UTER2,(None,None,51,3.3,6,37,45,85,2,0,55,1,0),1,None),

    #20.09.26
    'FEES':(LEG1_IGOGOSHA2,(None,7,12,42,'rsi_tw',6,0.06,41,55),1,None),
    #20.09.26
    # 'FEES2':(WEG3_BATYA,(None,None,14,1.5,1,1,1),1,None),
    #20.09.26
    'MAGN':(PEG26_UNKNOWN,(None,None,2,40,28,12,3,34,9,55,0),1,None),
    #20.09.26
    # 'MAGN2':(LEG1_BIBI2,(None,None,2,5,'%d',55,5,0.01),1,None),

    #+9 +7 -3 !(29%) +0.6 +1.3 +1.6 +4.3 +3.7
    'MTLR':(PEG11_KUSURUKEN,(None,None,44,8,51,36,'c',55),1,None), 
    #20.09.26
    'MTLR2':(SEG1_LITE,(None,37,31,2.7,0.2,11),4,None),
    #20.09.26
    # 'NLMK':(PEG17_PHOENIX,(None,None,37,16,12,9,18,0,55),1,None),
    #20.09.26
    # 'NLMK2':(LEG2_LYNX,(None,None,47,1.0,49,1.3,0),1,None),

    #20.09.26
    'RAGR':(LEG1_BIBI2,(None,None,6,50,'williams_r',55,2,0.21),1,None),
    #20.09.26
    # 'RAGR2':(PEG18_UTER2,(None,None,7,0.6,4,21,42,89,14,1,55,1,1),1,None),
    #20.09.26
    'ROSN':(UEG6_ADVENTURE,(None,None,30,47,16,2.5,0),1,None),
    #06.09.26 +0.4 -1.2 +3 +4.4 +1.2
    'ROSN2':(PEG17_PHOENIX,(None,None,8,50,30,48,5,1,55),1,None),

    #20.09.26
    'RUAL':(UEG6_PIGEON,(None,None,55,3,38,3,4,0.5,2.5,0),1,None),
    #20.09.26
    # 'RUAL2':(LEG1_IRONANNY2,(None,29,47,6,55,4,6,0.24),3,None),
    #20.09.26
    'SBER':(UEG6_ADVENTURE,(None,260,7,48,21,2.0,1),22,None),
    #20.09.26
    'SBER2':(UEG6_PIGEON,(None,227,8,48,3,5,1,0.38,2.0,0),19,None),

    #20.09.26
    'SBERP':(PEG4_UNIVERSAL,(None,None,13,3,27,19,'VC','s',3),1,None),
    #20.09.26
    'SBERP2':(UEG7_PIGEON,(None,None,7,2,55,3,2,0.75,2.1,1),1,None),
    #20.09.26
    'SFIN':(LEG2_ALKASH,(None,None,2,2.5,8,0),1,None),
    #20.09.26
    # 'SFIN2':(LEG2_LOGAN,(None,23,12,8,19),2,None),

    #20.09.26
    'ENPG':(PEG4_U3,(None,39,11,3,3,55,'VC','rsi_tw',5),4,None),
    #20.09.26
    # 'ENPG2':(LEG1_OKROSHKA,(None,32,5,26),3,None),
    #20.09.26
    'SIBN':(LEG2_LYNX,(None,55,10,2.8,55,1.0,1),5,None),
    #20.09.26
    'SIBN2':(PEG4_UNIVERSAL,(None,54,35,30,34,6,'BB','s',4),5,None),

    #20.09.26
    'IRAO':(LEG2_FENNEC,(None,None,30,2.8,6,38,11,1.2,0),1,None),
    #06.09.26 -2.2 -4.2
    # 'IRAO2':(LEG1_CC2,(None,None,51,7,55,6,1.6,0,1,2,0.03),1,None),
    #20.09.26
    'SNGSP':(LEG2_LOGAN,(None,81,12,30,18),7,None),
    #20.09.26
    'SNGSP2':(PEG17_PHOENIX,(None,None,7,34,24,54,7,1,55),1,None),

    #20.09.26
    'SPBE':(LEG2_DRINKER,(None,7,6,1.8,33,39,38,0),1,None),
    #20.09.26
    'SPBE2':(UEG6_VULTURE,(None,9,39,46,54,43,2,3,0.32,7),1,None),
    #20.09.26
    'T':(UEG6_ADVENTURE,(None,None,50,51,42,2.6,1),1,None),
    #20.09.26
    # 'T2':(PEG4_U3,(None,None,46,44,5,55,'BB','mfi',4),1,None),

    #+5 +9 +11 !(14%) +3.4 -2.2 +7.6 -2.2 +0
    'TATN':(LEG1_PIN,(20,None,48,3,39,3),2,None), 
    #20.09.26
    # 'TATN2':(PEG4_UNIVERSAL,(None,49,22,13,42,16,'WC','rsi',4),5,None),
    #20.09.26
    'TATNP':(UEG6_SHERIFF,(None,None,48,50,2.8),1,None),
    #20.09.26
    'TATNP2':(PEG17_PHOENIX,(None,None,16,45,40,49,5,0,55),1,None),
    
    #20.09.26
    'VKCO':(WEG3_BATYA,(None,None,45,1.8,1,1,1),1,None),
    #+14 +10 +2 !(46%) -3 -3.1 +2.5 +14.6 +7.5
    'VKCO2':(PEG17_PHOENIX,(None,None,9,12,50,43,26,0,55),1,None), 
    #20.09.26
    'VTBR':(LEG2_LYNX,(None,None,47,2.7,7,2.0,0),1,None),
    #06.09.26 +5 +4.4 +4.8 -5 +0.5
    'VTBR2':(LEG2_FENNEC,(None,83,54,3.0,7,40,24,1.5,0),7,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)