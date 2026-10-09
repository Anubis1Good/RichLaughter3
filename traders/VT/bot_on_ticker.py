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

    #04.10.26 ?19% -1.6 +0.1 -2.5
    # 'AFLT':(UEG8_SOLDIER,(None,None,15,7,65,0.95,12,0.35,36,1,72,24,15,84,19,48,30,11),1,None),
    #04.10.26 ?19% +3.1 $ -2.6 @
    # 'AFLT2':(PEG18_BLAZE,(None,32,49,7,9,40,12,0,70),3,None),
    #30.09.26 ?18% +7.9 +0.1 $ -0.7 +5.4 $ +5.3 +7.6
    'ALRS':(LEG1_LAKSAe,(None,15,17,9),2,None),
    #04.10.26 ?24% -2.7 @ -4.1
    'ALRS2':(VEG1_EARTH,(None,12,69,0.02,8,0.53,1,0.62,16,1,0,0),1,None),

    #08.10.26 ?30% -3.5
    'ASTR':(WEG8_MOUSE,(None,42,24,2,39,27,52,38,23,73,70,0.37),4,None),
    #08.10.26 ?38% +1.2
    'ASTR2':(WEG7_PARADOX2,(None,None,39,0.6,17,0.7),1,None),
    #30.09.26 ?33% +5.3 -8.8 !23%
    # 'CHMF':(VEG1_EARTH,(None,None,53,0.48,8,0.71,1,0.11,8,0,1,0),1,None),
    #27.09.26 ?22% 
    # 'CHMF2':(UEG8_SOLDIER,(None,None,15,55,0.43,0.95,43,91,58,50,90,36,62,49),1,None),

    # #29.09.26 ?34% -6.4 Y +1.6 $ +1
    # 'FEES':(WEG3_BATYA,(None,None,10,1.6,1,1,1),1,None),
    # #27.09.26 ?37% +4.3 +1.8 $ +2 $ -9.3
    # 'FEES2':(WEG7_PARADOX,(None,21,20,1.8),2,None),
    #04.10.26 ?16% +3.4 +3.5 $ -0.4 +4.9
    'MAGN':(PEG30_ETC2,(17,34,0,23,1,1,28,58,5,62,88,27),3,None),
    #04.10.26 ?11% -18.9
    # 'MAGN2':(PEG17_ZEALOT,(None,7,31,55,40,33,14,70),1,None),

    #08.10.26 ?26% +2.8
    'MTLR':(WEG8_MOUSE,(None,37,38,2,38,2,27,12,33,29,70,0.05),4,None),
    # #04.10.26 ?30% +0.9 -6.5 Зам
    # 'MTLR2':(PEG17_SELENDIS,(None,26,4,13,11,63,37,70),3,None),
    #30.09.26 ?28% +1.4 +7.4 !16% +29.7 -3.4 -8.5 -19.2
    # 'NLMK':(PEG17_PHOENIX,(None,None,15,32,61,6,30,0,70),1,None),
    #04.10.26 ?33% -18.6
    # 'NLMK2':(LEG1_BIBI2,(None,None,21,23,'williams_r',70,7,0.1),1,None),

    #08.10.26 ?35% +1.2
    'RAGR':(WEG7_PARADOX2,(None,23,4,0.4,46,0.6),2,None),
    #04.10.26 ?43% -0.3 -2.9 @ +0.9 +2.8
    'RAGR2':(LEG2_LYNX,(None,30,4,2.5,46,1.9,0),3,None),
    #04.10.26 ?21% -2.1 +2.9 +3.7 -15.4
    'ROSN':(PEG11_KUSURUKEN,(None,None,18,8,55,39,'hl',70),1,None),
    #04.10.26 ?13% +2 -0.5 @ -16.4
    'ROSN2':(UEG4_CANADIAN,(None,16,43,25,3,0.79),2,None),

    #08.10.26 ?19% +2.4
    'RUAL':(WEG7_PARADOX2,(None,14,39,0.3,67,1.8),2,None),
    #30.09.26 ?24% -2.6 +4.7 !26% +17.8 +4.9 +7.5 -2.7
    'RUAL2':(VEG1_EARTH,(None,None,29,0.56,4,0.86,0,0.34,9,0,0,0),1,None),
    #29.09.26 ?9% +2.9 $ 0 -2.9 @ !4% -4.8
    # 'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #04.10.26 ?7% -4.3
    # 'SBER2':(PEG17_TEMPLAR,(None,201,66,9,44,24,0,70),17,None),

    #04.10.26 ?11% -4.7 S +0 @ -1.2 @
    # 'SBERP':(UEG7_CARRIER,(None,None,4,42,4,1,42,13,3,0.69,1.3,0),1,None),
    #27.09.26 ?12% +0.4 +2.4 $ +1.3 $ +2.6 $ -4.5 +1.3 $ +2 +1.9
    'SBERP2':(WEG3_BATYA,(None,None,60,2.9,1,1,1),1,None),
    #27.09.26 ?42% -4 Y +6.5 +4.6 -0.6 @ !34% +3.4 +13.7 -0.4 -3.4
    'SFIN':(UEG7_CANNIBAL,(None,None,54,56,12,5,5,45,19,10,0.14,17),1,None),
    #04.10.26 ?29% +8.1 +14.5 -3.3
    'SFIN2':(UEG9_GRAVY2,(None,None,40,0.91,8,0.47,1.85,1),1,None),

    #27.09.26 ?37% -0.9 S +7.3 +10.6 +4.9 !27% +1.3 $ +2.3 -5.5 -6.1
    'ENPG':(UEG9_GRAVY2,(None,23,30,0.85,10,0.31,1.85,1),2,None),
    #08.10.26 ?28% -9.4
    'ENPG2':(WEG7_PARADOX2,(None,None,12,0.3,8,0.3),1,None),
    #04.10.26 ?13% +6.4 -3.5 -10.3 -11.3
    'SIBN':(UEG8_SOLDIER,(None,20,18,21,40,0.57,4,0.76,24,0,92,2,2,97,75,19,79,43),2,None),
    #30.09.26 ?16% +5.4 +6.1 !16% -0.6 -2.5 +8 +5.2
    'SIBN2':(PEG17_PHOENIX,(None,70,65,35,29,2,37,0,70),6,None),

    #04.10.26 ?12% -1.4 @ -2.1 -0.8
    'IRAO':(UEG8_SOLDIER,(None,30,18,57,48,0.95,10,0.72,30,0,73,21,69,0,90,82,73,95),3,None),
    #30.09.26 ?12% +0.8 +4.9 +1.6 +7.4 -2.4 -7.1
    'IRAO2':(PEG18_ANDUIN,(None,35,54,1.3,45,9,43,7,0,70),3,None),
    #04.10.26 ?18% +1.2 $ +5.6
    'SNGSP':(WEG4_DOG,(None,None,12,23),1,None),
    #04.10.26 ?16% +13.1 +1.2 +0.7
    'SNGSP2':(PEG17_PHOENIX,(None,54,13,58,36,53,22,0,70),5,None),

    #04.10.26 ?25% +5.5 -7 -19.6
    # 'SPBE':(PEG18_ANDUIN,(None,None,5,0.8,44,33,24,5,0,70),1,None),
    #30.09.26 ?33% +5.2 -1.8 !24% -1 +7.1 $ -11.2
    # 'SPBE2':(WEG4_DOG,(None,12,50,36),1,None),
    #04.10.26 ?21% +0.5 $ -3.5 +1.1 -2.8
    'T':(PEG17_PROBIUS,(None,67,30,6,30,26,3,70,2),6,None),
    #29.09.26 ?16% +3.5 +1.7 $ -0.7 +0.2 @ -0.8 -2.3 -1.6
    'T2':(PEG17_PHOENIX,(None,None,18,23,33,2,15,0,60),1,None),

    #04.10.26 ?17% -1.2 @ +1.3 +7.4 +0.2
    'TATN':(PEG17_ZEALOT,(None,None,10,8,45,53,6,70),1,None),
    #04.10.26 ?16% -0.6 @ -1.1 -4
    # 'TATN2':(UEG6_ADVENTURE,(None,14,38,8,68,1.9,1),2,None),
    #04.10.26 ?27% +9 +4.1
    'TATNP':(LEG2_FENNEC,(None,None,21,3.0,8,36,16,1.0,0),1,None),
    #30.09.26 ?33% +8.4 +2.2 !27% +3.8 +4.9 +5 +4.5
    'TATNP2':(UEG8_SOLDIER,(None,None,8,11,35,0.19,6,0.96,41,0,15,80,20,58,23,90,6,84),1,None),
    
    #29.09.26 ?25% -1.6 +4.9 +2.9 !18% -2.2 -7.6 -8.5
    # 'VKCO':(PEG19_ANUBARAK,(None,8,21,10,3,24,38,53,0,60),1,None),
    #04.10.26 ?33% +2.5 $ +1.5 -6.2 @
    # 'VKCO2':(PEG30_ETC2,(None,13,0,9,1,1,34,64,62,57,89,22),1,None),
    #04.10.26 ?13% -7.1 -4.1 @ +1.5 +4.3
    'VTBR':(PEG17_PHOENIX,(None,22,63,26,5,55,11,1,70),2,None),
    #04.10.26 ?20% -15.4
    # 'VTBR2':(UEG7_CANNIBAL,(None,60,9,64,29,12,1,23,32,9,0.46,17),5,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)