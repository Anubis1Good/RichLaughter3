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

    #18.10.26 ?12% -0.6 -2.1 +7.8 +4.9 д
    'AFLT':(WEG3_BATYA,(None,7,18,1.9,1,1,1),1,None),
    #11.10.26 ?15% +8 +4.7 +5.5 -0.1 +12.1 +6.6 д
    'AFLT2':(UEG6_SURVIVALIST,(None,None,16,9,1.4,1,2.7,26,29,0),1,None),
    #25.10.26 ?28%
    'ALRS':(WEG7_PARADOX2,(None,None,34,0.9,11,1.4),1,None),
    #25.10.26 ?27%
    'ALRS2':(PEG4_U4,(None,None,9,66,63,70,'SC','real_wpedal',4,0.2),1,None),

    #11.10.26 ?31% +5.4 +11.2 -1.8 +8.1 +6.8 +3.4 +3.6 +1.3 д
    'ASTR':(PEG11_RAYMIYAMOTO,(None,None,36,55,1.0,5.0,20,35,'rsi','wpedal',3,70,36,53,18,31,47,15,0,4),1,None),
    #11.10.26 ?29% +4.4 +3.6 +4.5 +5.3 -3.8 +7.3 +5.4 -4.1 д
    'ASTR2':(PEG13_DUNE,(None,None,7,6,70,31,0.35,70,25,0.26),1,None),
    #25.10.26 ?28%
    'CHMF':(PEG26_JUNKRAT,(None,None,59,6,8,10,42,0.2),1,None),
    #25.10.26 ?22%
    'CHMF2':(UEG6_SURVIVALIST,(None,None,25,12,1.3,0,7.1,52,43,0),1,None),


    #25.10.26 ?22%
    # 'FEES':(PEG26_JUNKRAT,(None,None,53,36,9,10,8,0.3),1,None),
    #25.10.26 ?19%
    # 'FEES2':(UEG6_SURVIVALIST,(None,None,19,40,2.0,0,1.2,46,33,0),1,None),
    #18.10.26 ?17% +4.5 +14.9 -7.8 д
    'MAGN':(PEG13_DUNE,(None,None,5,26,63,12,0.01,70,20,0.11),1,None),
    #04.10.26 ?16% +3.4 +3.5 $ -0.4 +4.9 +11.5 +1.8 +7.5 -1.6 +0.8 -1.8 +6.7 -2.2 д
    'MAGN2':(PEG30_ETC2,(17,34,0,23,1,1,28,58,5,62,88,27),3,None),

    #25.10.26 ?23%
    'MTLR':(PEG17_AIUR,(None,26,55,12,31,69,26,1,70,0.6),3,None),
    #25.10.26 ?25%
    'MTLR2':(UEG6_ADVENTURE,(None,27,16,54,48,1.6,0),3,None),
    #13.10.26 -0.8 +3 +5 +4.3 +8.1 +23.8 д
    'NLMK':(PEG30_ETC,(None,8,1,11,1,1,16,7,14,8,5,24),1,None),
    #18.10.26 ?24% -6.4 +6.1 -9.6 С
    # 'NLMK2':(WEG3_BATYA,(None,None,23,1.1,0,1,1),1,None),

    #25.10.26 ?27%
    'RAGR':(UEG9_POLITICIAN,(None,None,66,0.94,4,0.48,0,68,48),1,None),
    #11.10.26 ?18% +4.2 +5.3 +1.3 -6 -0.3 +10.8 +1.9 д
    'RAGR2':(SEG1_LITE,(None,17,61,1.6,0.1,32),2,None),
    #25.10.26 ?28%
    'ROSN':(PEG17_AIUR,(None,None,15,11,67,44,32,0,70,0.4),1,None),
    #11.10.26 ?22% +13.5 +3.3 +2.1 +2 -0.6 +0.3 +9.4 -2.4 д
    'ROSN2':(PEG13_DUNE,(None,None,11,59,70,11,0.15,70,24,0.24),1,None),

    #18.10.26 ?25% +2.1 +4.1 +0.6 д
    'RUAL':(UEG6_SURVIVALIST,(None,None,7,5,2.9,0,4.1,58,9,0),1,None),
    #18.10.26 ?16%c112wr91% +1.7 +0.5 +3.7 +1.3 д
    'RUAL2':(PEG17_PROBIUS,(None,10,58,63,61,26,6,70,49),1,None),
    #29.09.26 ?9% +2.9 $ 0 -2.9 @ !4% -4.8
    # 'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #04.10.26 ?7% -4.3
    # 'SBER2':(PEG17_TEMPLAR,(None,201,66,9,44,24,0,70),17,None),

    #18.10.26 ?9% -5.7 Н
    # 'SBERP':(PEG17_PHOENIX,(None,185,37,24,23,44,23,0,70),16,None),
    #04.10.26 ?11% -4.7 S +0 @ -1.2 @
    # 'SBERP2':(UEG7_CARRIER,(None,None,4,42,4,1,42,13,3,0.69,1.3,0),1,None),
    #25.10.26 ?45%
    'SFIN':(PEG26_JUNKRAT,(None,None,35,36,11,8,35,0.4),1,None),
    #18.10.26 ?40% +0.6 +4.4 +3.3 +7.7 д
    'SFIN2':(UEG6_SURVIVALIST,(None,None,27,42,2.9,0,8.1,67,33,0),1,None),

    #25.10.26 ?23%
    'ENPG':(PEG26_JUNKRAT,(None,None,35,7,18,13,27,0.55),1,None),
    #25.10.26 ?31%
    'ENPG2':(UEG9_GRAVY2,(None,None,22,0.52,12,0.44,1.05,0),1,None),
    #25.10.26 ?18%
    'SIBN':(PEG17_AIUR,(None,None,52,40,56,6,47,1,70,0.4),1,None),
    #18.10.26 ?11%  +2.9 +1.2 +4.3 д
    'SIBN2':(PEG30_ETC2,(None,30,0,47,1,1,19,29,41,51,91,25),3,None),

    #25.10.26 ?18%
    'IRAO':(PEG11_RAYMIYAMOTO,(None,None,41,43,4.8,2.9,20,13,'s','real_wpedal',3,70,41,79,5,7,39,14,0,6),1,None),
    #25.10.26 ?15%
    'IRAO2':(PEG4_U5,(None,None,5,32,70,'VC','real_wpedal',8,38,12),1,None),
    #04.10.26 ?18% +1.2 $ +5.6 -3.3 +3 +1.4 +0.1 +2.7 +3.2 -3.7 +1.8 д
    'SNGSP':(WEG4_DOG,(None,None,12,23),1,None),
    #04.10.26 ?16% +13.1 +1.2 +0.7 +6.9 +8.9 -1.1 +4.6 -0.7 @ -1.4 +1.4 +3.4 д
    'SNGSP2':(PEG17_PHOENIX,(None,54,13,58,36,53,22,0,70),5,None),

    #25.10.26 ?23%
    'SPBE':(LEG2_FENNEC,(None,8,12,2.1,23,40,48,1.2,1),1,None),
    #11.10.26 ?16% +5 +1.8 +7.4 +1.1 -5 +9.4 +7.2 -4.6 д
    'SPBE2':(PEG14_RANGER,(None,5,34,21,32,8,27,47),1,None),
    #25.10.26 ?12%
    'T':(UEG7_LOVERDUCK,(None,121,15,35,8,6,41,53,0),11,None),
    #11.10.26 ?7% +1.5 -0.5 +0.9 -1.9
    # 'T2':(UEG7_LOVERGOOSE,(None,15,10,51,25,10,60,64,1),2,None),

    #25.10.26 ?14%
    'TATN':(UEG7_LOVERGOOSE,(None,None,18,14,10,10,59,24,0),1,None),
    #18.10.26 ?13% +3.5 +15.2 -9.8 с
    'TATN2':(UEG9_POLITICIAN,(None,None,56,0.9,6,0.42,0,64,8),1,None),
    #25.10.26 ?19%
    'TATNP':(PEG11_SAYATAKAGI,(None,36,28,16,4.5,0.5,24,6,'uo','uo',7,70,23,25,39,16,48,0,6),3,None),
    #25.10.26 ?18%
    'TATNP2':(UEG4_CANADIAN,(None,44,13,11,9,0.38),4,None),
    
    #25.10.26 ?30%
    'VKCO':(UEG9_GRAVY2,(None,None,61,0.91,10,0.15,0.5,0),1,None),
    #25.10.26 ?22%
    'VKCO2':(UEG6_SURVIVALIST,(None,None,27,70,3.0,1,9.0,40,30,0),1,None),
    #25.10.26 ?13%
    'VTBR':(PEG17_AIUR,(None,56,65,6,12,66,6,1,70,0.7),5,None),
    #18.10.26 ?14% +5.2 +8.6 +0.6 д
    'VTBR2':(PEG17_PHOENIX,(None,75,13,52,69,62,29,0,70),7,None),
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)