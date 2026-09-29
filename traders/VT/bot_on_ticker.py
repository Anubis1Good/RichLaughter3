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

    #29.09.26 ?25% -9.9 N
    # 'AFLT':(PEG19_ANUBARAK,(None,28,59,11,5,32,29,90,0,60),3,None),
    #20.09.26 +3.3 !(29%) Y +1.8 -11.4
    # 'AFLT2':(LEG1_PIN,(None,19,2,4,19,4),2,None),
    #27.09.26 ?34% -2.2 S -1
    'ALRS':(UEG7_CELEBRITY,(None,None,9,45,10,1,1.6,1),1,None),
    #27.09.26 ?30% +2.4 -5.7 @
    # 'ALRS2':(LEG2_LYNX,(None,11,22,2.8,6,1.7,1),1,None),

    #29.09.26 ?42% +6.3 $
    'ASTR':(PEG11_KUSURUKEN,(None,None,27,16,12,11,'c',60),1,None),
    #20.09.26 +2.4 +3.2 +5.4 +9.6 !21% Y -5.2 +6.4
    'ASTR2':(PEG4_UNIVERSAL,(None,19,13,12,29,18,'WC','mfi',5),2,None),
    #29.09.26 ?14% -2.5 S
    'CHMF':(SEG1_LITE,(None,None,49,2.1,0.6,6),1,None),
    #27.09.26 ?22% 
    # 'CHMF2':(UEG8_SOLDIER,(None,None,15,55,0.43,0.95,43,91,58,50,90,36,62,49),1,None),

    #29.09.26 ?34% -6.4 Y
    'FEES':(WEG3_BATYA,(None,None,10,1.6,1,1,1),1,None),
    #27.09.26 ?37% +4.3 +1.8 $
    'FEES2':(WEG7_PARADOX,(None,21,20,1.8),2,None),
    #29.09.26 ?40% -5.5 N
    # 'MAGN':(PEG11_KUSURUKEN,(None,None,37,39,24,12,'c',60),1,None),
    #20.09.26
    # 'MAGN2':(LEG1_BIBI2,(None,None,2,5,'%d',55,5,0.01),1,None),

    #29.09.26 ?27% -12.1 N
    # 'MTLR':(LEG2_HOTS,(None,None,56,1.3,8,39,17,0),1,None),
    #20.09.26 +8 +6 +2.2 +2.2 !23% Y +7.7 -7.6
    # 'MTLR2':(SEG1_LITE,(None,37,31,2.7,0.2,11),4,None),
    #29.09.26 ?28% -17.2 @ N
    # 'NLMK':(LEG2_LYNX,(None,None,45,1.3,31,1.3,0),1,None),
    #29.09.26 ?28%
    # 'NLMK2':(WEG3_BATYA,(None,None,50,1.4,1,1,1),1,None),

    #20.09.26 -0.1 +15 +0.6 +0.7 !28%  Y +9.8 +13.6
    'RAGR':(LEG1_BIBI2,(None,None,6,50,'williams_r',55,2,0.21),1,None),
    #27.09.26 ?47%  +9.9 +2
    'RAGR2':(UEG6_ADVENTURE,(None,None,11,22,21,1.8,0),1,None),
    #29.09.26 ?38% -8 @ N
    # 'ROSN':(LEG2_FENNEC,(None,None,12,3.0,2,16,13,1.8,0),1,None),
    #27.09.26 ?27% -6.1 S -6.1
    # 'ROSN2':(UEG9_GRAVY2,(None,None,54,0.27,6,0.46,0.2,0),1,None),

    #29.09.26 ?32% +0.8 $
    'RUAL':(WEG4_PUPPY,(None,None,14,27,19),1,None),
    #27.09.26 ?31% +5.3 -15.7
    # 'RUAL2':(PEG17_PHOENIX,(None,None,54,38,4,33,9,1,60),1,None),
    #29.09.26 ?9% +2.9 $
    'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #27.09.26 ?_% 
    # 'SBER2':(UEG6_DODO,(None,None,27,28,32,55),1,None),

    #27.09.26 ?14% -0.2 +0.2 $
    'SBERP':(LEG2_DRG,(None,159,11,1.9,7,34,25,0),14,None),
    #27.09.26 ?12% +0.4 +2.4 $
    'SBERP2':(WEG3_BATYA,(None,None,60,2.9,1,1,1),1,None),
    #27.09.26 ?42% -4 Y +6.5
    'SFIN':(UEG7_CANNIBAL,(None,None,54,56,12,5,5,45,19,10,0.14,17),1,None),
    #29.09.26 ?48% +16.5
    'SFIN2':(PEG14_RENEGADE,(None,None,20,40,13,14,39,49),1,None),

    #27.09.26 ?37% -0.9 S +7.3
    'ENPG':(UEG9_GRAVY2,(None,23,30,0.85,10,0.31,1.85,1),2,None),
    #27.09.26 ?32% +1.5 +2.7
    'ENPG2':(PEG17_PHOENIX,(None,None,28,46,29,56,5,0,60),1,None),
    #20.09.26 +9.2 +0.6 +6 +4.5 !16% S +3.7 -8.8 S
    'SIBN':(LEG2_LYNX,(None,55,10,2.8,55,1.0,1),5,None),
    #20.09.26 +7.9 +1.4 +1.3 +0.4 !15% S +3.2 -10.5 S
    'SIBN2':(PEG4_UNIVERSAL,(None,54,35,30,34,6,'BB','s',4),5,None),

    #27.09.26 ?17% +0.5 -0.2
    'IRAO':(UEG7_LOVERGOOSE,(None,None,17,43,3,4,36,48,0),1,None),
    #29.09.26 ?16%
    # 'IRAO2':(PEG14_RENEGADE,(None,None,4,31,11,8,14,77),1,None),
    #20.09.26 +1.2 +5.6 +2.4 +3 !17% S +1.7 +1.5
    'SNGSP':(LEG2_LOGAN,(None,81,12,30,18),7,None),
    #27.09.26 ?24% -0.9 +5 $
    'SNGSP2':(WEG3_BATYA,(None,None,22,2.8,1,1,1),1,None),

    # #20.09.26 +1.6 +1.3 +0.5 +3.3 !30% S -3.7
    # 'SPBE':(LEG2_DRINKER,(None,7,6,1.8,33,39,38,0),1,None),
    # #27.09.26 ?33% -6.1
    # 'SPBE2':(PEG4_UNIVERSAL,(None,9,40,50,37,22,'WC','s',7),1,None),
    #27.09.26 ?23%  -3 S -4
    # 'T':(UEG7_CELEBRITY,(None,94,49,45,4,6,2.3,1),8,None),
    #29.09.26 ?16% +3.5
    'T2':(PEG17_PHOENIX,(None,None,18,23,33,2,15,0,60),1,None),

    #27.09.26 ?22% +10.2 -8.6
    # 'TATN':(UEG6_ADVENTURE,(None,None,39,52,4,3.0,0),1,None),
    #27.09.26 ?17% 
    # 'TATN2':(WEG4_PUPPY,(None,None,38,40,14),1,None),
    #29.09.26 ?25%  +3
    'TATNP':(PEG17_PHOENIX,(None,None,17,16,23,21,10,0,60),1,None),
    #27.09.26 ?26% +13.1 -9.4
    # 'TATNP2':(WEG3_BATYA,(None,31,56,1.6,1,1,1),3,None),
    
    #29.09.26 ?25% -1.6
    'VKCO':(PEG19_ANUBARAK,(None,8,21,10,3,24,38,53,0,60),1,None),
    #29.09.26 ?35%  -10.7 N
    # 'VKCO2':(PEG17_PHOENIX,(None,None,9,14,60,40,35,0,60),1,None),
    #29.09.26 ?18% -9.7
    # 'VTBR':(LEG2_FENNEC,(None,None,33,1.8,14,40,36,1.7,0),1,None),
    #20.09.26 +1.4 +8.5 +4.1 +5.5 !14% Y -1.9 -1.4 
    'VTBR2':(LEG2_LYNX,(None,None,47,2.7,7,2.0,0),1,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)