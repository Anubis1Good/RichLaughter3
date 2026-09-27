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

    #27.09.26 ?28% 
    'AFLT':(UEG7_CARRIER,(None,None,34,11,3,2,31,15,6,0.14,2.4,0),1,None),
    #20.09.26 +3.3 !(29%) Y
    'AFLT2':(LEG1_PIN,(None,19,2,4,19,4),2,None),
    #27.09.26 ?34% 
    'ALRS':(UEG7_CELEBRITY,(None,None,9,45,10,1,1.6,1),1,None),
    #27.09.26 ?30% 
    'ALRS2':(LEG2_LYNX,(None,11,22,2.8,6,1.7,1),1,None),

    #27.09.26 ?39% 
    'ASTR':(VEG1_MOON,(None,43,3,35,0.26,0.48,1,1,0,0),4,None),
    #20.09.26 +2.4 +3.2 +5.4 +9.6 !21% Y
    'ASTR2':(PEG4_UNIVERSAL,(None,19,13,12,29,18,'WC','mfi',5),2,None),
    #27.09.26 ?31% 
    'CHMF':(UEG4_PELICAN2,(None,None,57,7,10,0.61),1,None),
    #27.09.26 ?22% 
    # 'CHMF2':(UEG8_SOLDIER,(None,None,15,55,0.43,0.95,43,91,58,50,90,36,62,49),1,None),

    #27.09.26 ?32% 
    'FEES':(UEG8_SOLDIER,(None,None,4,11,0.0,0.3,52,97,70,91,30,39,86,43),1,None),
    #27.09.26 ?37% 
    'FEES2':(WEG7_PARADOX,(None,21,20,1.8),2,None),
    #20.09.26 -4.6 !26% S
    # 'MAGN':(PEG11_KUSURUKEN,(None,None,20,4,38,19,'c',55),1,None),
    #20.09.26
    # 'MAGN2':(LEG1_BIBI2,(None,None,2,5,'%d',55,5,0.01),1,None),

    #27.09.26 ?34% 
    'MTLR':(UEG8_SOLDIER,(None,None,3,31,0.02,0.78,92,61,94,43,9,46,68,37),1,None),
    #20.09.26 +8 +6 +2.2 +2.2 !23% Y
    'MTLR2':(SEG1_LITE,(None,37,31,2.7,0.2,11),4,None),
    #27.09.26 ?33% 
    # 'NLMK':(UEG7_VULTURE,(None,None,56,41,2,3,2,60,0.3,4),1,None),
    #27.09.26 ?27% 
    # 'NLMK2':(LEG1_CC2,(None,None,25,12,60,9,0.7,0,1,6,0.12),1,None),

    #20.09.26 -0.1 +15 +0.6 +0.7 !28%  Y
    'RAGR':(LEG1_BIBI2,(None,None,6,50,'williams_r',55,2,0.21),1,None),
    #27.09.26 ?47% 
    'RAGR2':(UEG6_ADVENTURE,(None,None,11,22,21,1.8,0),1,None),
    #27.09.26 ?27% 
    'ROSN':(UEG8_SOLDIER,(None,None,6,36,0.28,0.76,96,71,75,16,29,2,78,25),1,None),
    #27.09.26 ?27% 
    'ROSN2':(UEG9_GRAVY2,(None,None,54,0.27,6,0.46,0.2,0),1,None),

    #27.09.26 ?31% 
    'RUAL':(UEG9_GRAVY2,(None,None,20,0.64,20,0.14,2.0,0),1,None),
    #27.09.26 ?31% 
    'RUAL2':(PEG17_PHOENIX,(None,None,54,38,4,33,9,1,60),1,None),
    #27.09.26 ?_% 
    # 'SBER':(LEG1_IGOGOSHA2,(None,245,10,52,'rsi_tw',4,0.01,34,60),21,None),
    #27.09.26 ?_% 
    # 'SBER2':(UEG6_DODO,(None,None,27,28,32,55),1,None),

    #27.09.26 ?14% 
    'SBERP':(LEG2_DRG,(None,159,11,1.9,7,34,25,0),14,None),
    #27.09.26 ?12% 
    'SBERP2':(WEG3_BATYA,(None,None,60,2.9,1,1,1),1,None),
    #27.09.26 ?42% 
    'SFIN':(UEG7_CANNIBAL,(None,None,54,56,12,5,5,45,19,10,0.14,17),1,None),
    #27.09.26 ?34% 
    # 'SFIN2':(UEG8_SOLDIER,(None,21,4,20,0.74,0.51,83,12,87,36,87,58,31,16),2,None),

    #27.09.26 ?37% 
    'ENPG':(UEG9_GRAVY2,(None,23,30,0.85,10,0.31,1.85,1),2,None),
    #27.09.26 ?32% 
    'ENPG2':(PEG17_PHOENIX,(None,None,28,46,29,56,5,0,60),1,None),
    #20.09.26 +9.2 +0.6 +6 +4.5 !16% S
    'SIBN':(LEG2_LYNX,(None,55,10,2.8,55,1.0,1),5,None),
    #20.09.26 +7.9 +1.4 +1.3 +0.4 !15% S
    'SIBN2':(PEG4_UNIVERSAL,(None,54,35,30,34,6,'BB','s',4),5,None),

    #27.09.26 ?17% 
    'IRAO':(UEG7_LOVERGOOSE,(None,None,17,43,3,4,36,48,0),1,None),
    #27.09.26 ?17% 
    # 'IRAO2':(PEG4_UNIVERSAL,(None,None,28,33,21,23,'BB','s',6),1,None),
    #20.09.26 +1.2 +5.6 +2.4 +3 !17% S
    'SNGSP':(LEG2_LOGAN,(None,81,12,30,18),7,None),
    #27.09.26 ?24% 
    'SNGSP2':(WEG3_BATYA,(None,None,22,2.8,1,1,1),1,None),

    #20.09.26 +1.6 +1.3 +0.5 +3.3 !30% S
    'SPBE':(LEG2_DRINKER,(None,7,6,1.8,33,39,38,0),1,None),
    #27.09.26 ?33% 
    'SPBE2':(PEG4_UNIVERSAL,(None,9,40,50,37,22,'WC','s',7),1,None),
    #27.09.26 ?23% 
    'T':(UEG7_CELEBRITY,(None,94,49,45,4,6,2.3,1),8,None),
    #27.09.26 ?12% 
    # 'T2':(LEG2_LOGAN,(None,112,43,52,21),10,None),

    #27.09.26 ?22% 
    'TATN':(UEG6_ADVENTURE,(None,None,39,52,4,3.0,0),1,None),
    #27.09.26 ?17% 
    # 'TATN2':(WEG4_PUPPY,(None,None,38,40,14),1,None),
    #27.09.26 ?33% 
    'TATNP':(UEG9_BIRDWATCHER2,(None,None,20,1.0,16,0.45,2.0,0.04,1,1),1,None),
    #27.09.26 ?26% 
    'TATNP2':(WEG3_BATYA,(None,31,56,1.6,1,1,1),3,None),
    
    #20.09.26 -0.4 +1 +14.3 +3 !36% S
    'VKCO':(WEG3_BATYA,(None,None,45,1.8,1,1,1),1,None),
    #+14 +10 +2 !(46%) -3 -3.1 +2.5 +14.6 +7.5 +4.4 +11.9 +1.7 +5.6 !17% Y
    'VKCO2':(PEG17_PHOENIX,(None,None,9,12,50,43,26,0,55),1,None), 
    #27.09.26 ?22% 
    'VTBR':(VEG1_MOON,(None,None,18,28,0.38,0.47,0,0,1,1),1,None),
    #20.09.26 +1.4 +8.5 +4.1 +5.5 !14% Y
    'VTBR2':(LEG2_LYNX,(None,None,47,2.7,7,2.0,0),1,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)