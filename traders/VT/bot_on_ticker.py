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

    #08.11.26 ?16% 
    'AFLT':(UEG9_TRACKER,(None,None,13,7.5,0.14,66,30,70,46),1,None),
    #08.11.26 ?12% 
    'AFLT2':(PEG4_U4,(None,11,37,41,57,70,'VG','rsi',7,0.01),1,None),
    #08.11.26 ?41% 
    'ALRS':(UEG9_MEDIUM,(None,None,15,3.9,0.2,35,55,70,24),1,None),
    #08.11.26 ?30% 
    'ALRS2':(LEG2_FENNEC,(None,19,69,2.9,26,43,22,2.0,0),2,None),

    #08.11.26 ?34% 
    'ASTR':(PEG11_RAYMIYAMOTO,(None,None,63,29,0.5,4.4,70,36,'rsi','velcro',5,70,36,82,6,15,44,27,0,0),1,None),
    #08.11.26 ?27% 
    'ASTR2':(LEG2_FENNEC,(None,23,42,2.8,12,39,41,1.9,0),2,None),
    #25.10.26 ?28% +4.5 +7.2 -0.5 -11.2
    # 'CHMF':(PEG26_JUNKRAT,(None,None,59,6,8,10,42,0.2),1,None),
    #25.10.26 ?22% -3.2 +7.6 +7.2 -4.3
    # 'CHMF2':(UEG6_SURVIVALIST,(None,None,25,12,1.3,0,7.1,52,43,0),1,None),


    #25.10.26 ?22%
    # 'FEES':(PEG26_JUNKRAT,(None,None,53,36,9,10,8,0.3),1,None),
    #25.10.26 ?19%
    # 'FEES2':(UEG6_SURVIVALIST,(None,None,19,40,2.0,0,1.2,46,33,0),1,None),
    #18.10.26 ?17% +4.5 +14.9 -7.8 д -0.9 н
    # 'MAGN':(PEG13_DUNE,(None,None,5,26,63,12,0.01,70,20,0.11),1,None),
    #04.10.26 ?16% +3.4 +3.5 $ -0.4 +4.9 +11.5 +1.8 +7.5 -1.6 +0.8 -1.8 +6.7 -2.2 д +1.1 -3.5 нс n
    # 'MAGN2':(PEG30_ETC2,(17,34,0,23,1,1,28,58,5,62,88,27),3,None),

    #08.11.26 ?18% 
    'MTLR':(PEG17_AIUR,(None,22,51,46,68,45,16,1,70,0.0),2,None),
    #08.11.26 ?24% 
    'MTLR2':(PEG11_RAYMIYAMOTO,(None,20,36,58,3.0,4.8,27,46,'wpedal','real_pedal',6,70,41,83,24,16,28,38,0,0),2,None),
    #08.11.26 ?17% 
    # 'NLMK':(PEG11_RAYMIYAMOTO,(None,31,25,46,1.1,1.5,61,47,'velcro','pedal',5,70,31,53,46,50,3,23,0,4),3,None),
    #08.11.26 ?18% 
    # 'NLMK2':(LEG2_DRINKER,(None,25,51,2.5,13,42,28,0),3,None),

    #25.10.26 ?27% +7.8 +0.8 +2 +1.7 +7.1 s
    'RAGR':(UEG9_POLITICIAN,(None,None,66,0.94,4,0.48,0,68,48),1,None),
    #11.10.26 ?18% +4.2 +5.3 +1.3 -6 -0.3 +10.8 +1.9 д +4.4 +0.1 +3.5 -1.1 +2.5 s
    'RAGR2':(SEG1_LITE,(None,17,61,1.6,0.1,32),2,None),
    #08.11.26 ?21% 
    'ROSN':(LEG2_LYNX,(None,None,22,2.2,20,1.7,1),1,None),
    #08.11.26 ?20% 
    'ROSN2':(PEG17_PHOENIX,(None,None,10,16,61,45,17,1,70),1,None),

    #08.11.26 ?21% 
    'RUAL':(LEG2_HOTS,(None,None,48,1.8,8,49,5,0),1,None),
    #08.11.26 ?14% 
    'RUAL2':(SEG1_LITE,(None,46,22,2.6,0.5,8),4,None),
    #29.09.26 ?9% +2.9 $ 0 -2.9 @ !4% -4.8
    # 'SBER':(WEG3_BATYA,(None,None,33,2.8,1,1,1),1,None),
    #04.10.26 ?7% -4.3
    # 'SBER2':(PEG17_TEMPLAR,(None,201,66,9,44,24,0,70),17,None),

    #18.10.26 ?9% -5.7 Н
    # 'SBERP':(PEG17_PHOENIX,(None,185,37,24,23,44,23,0,70),16,None),
    #04.10.26 ?11% -4.7 S +0 @ -1.2 @
    # 'SBERP2':(UEG7_CARRIER,(None,None,4,42,4,1,42,13,3,0.69,1.3,0),1,None),
    #08.11.26 ?32% 
    'SFIN':(UEG9_ASTRAL,(None,None,44,9.8,0.1),1,None),
    #08.11.26 ?23% 
    'SFIN2':(PEG17_AIUR,(None,10,8,43,43,59,14,1,70,1.0),1,None),

    #08.11.26 ?28% 
    'ENPG':(UEG6_SURVIVALIST,(None,None,44,7,3.0,1,1.1,10,10,0),1,None),
    #08.11.26 ?23% 
    'ENPG2':(PEG17_PHOENIX,(None,None,7,10,31,41,3,0,70),1,None),
    #25.10.26 ?12% +7.4 нс нс -4.6 n
    # 'SIBN':(PEG30_ETC2,(None,13,0,40,1,1,32,55,58,44,53,29),3,None),
    #18.10.26 ?11%  +2.9 +1.2 +4.3 д +1.4 -3.6 нс +1.9 -5.2 n
    # 'SIBN2':(PEG30_ETC2,(None,30,0,47,1,1,19,29,41,51,91,25),3,None),

    #08.11.26 ?15% 
    'IRAO':(PEG11_SAYATAKAGI,(None,22,53,64,1.5,1.0,47,54,'real_wpedal','rsi',3,70,7,35,22,10,30,0,15),2,None),
    #08.11.26 ?18% 
    'IRAO2':(PEG17_AIUR,(None,None,63,7,42,18,21,1,70,1.0),1,None),
    #08.11.26 ?15% 
    'SNGSP':(UEG9_TRACKER,(None,78,14,8.0,0.1,28,11,70,17),7,None),
    #08.11.26 ?15% 
    'SNGSP2':(PEG17_AIUR,(None,39,13,28,59,14,36,1,70,0.6),4,None),

    #08.11.26 ?33% 
    'SPBE':(UEG9_ASTRAL,(None,13,68,8.4,0.23),2,None),
    #08.11.26 ?23% 
    'SPBE2':(UEG6_SURVIVALIST,(None,7,54,43,1.5,1,1.1,69,41,0),1,None),
    #25.10.26 ?12% -2.5 н
    # 'T':(UEG7_LOVERDUCK,(None,121,15,35,8,6,41,53,0),11,None),
    #11.10.26 ?7% +1.5 -0.5 +0.9 -1.9
    # 'T2':(UEG7_LOVERGOOSE,(None,15,10,51,25,10,60,64,1),2,None),

    #25.10.26 ?10% +11.8 -1.6 -13 n
    # 'TATN':(PEG30_ETC,(None,55,1,18,1,1,12,13,5,40,95,13),5,None),
    #25.10.26 ?11% +4.4 +10.4 -4.2 -12.3 n
    # 'TATN2':(PEG17_AIUR,(None,27,23,16,6,29,16,0,70,0.4),3,None),
    #25.10.26 ?19% -5.5 +16.8 +3.8 -2.8 -12.5 n
    # 'TATNP':(PEG11_SAYATAKAGI,(None,36,28,16,4.5,0.5,24,6,'uo','uo',7,70,23,25,39,16,48,0,6),3,None),
    #25.10.26 ?17% +5 +12.6 -2 -15.9 n
    # 'TATNP2':(UEG9_GRAVY2,(None,59,54,0.9,10,0.24,2.0,1),5,None),
    
    #25.10.26 ?30% +2.7 -3.4
    # 'VKCO':(UEG9_GRAVY2,(None,None,61,0.91,10,0.15,0.5,0),1,None),
    #25.10.26 ?22% +1.9 -6.9
    # 'VKCO2':(UEG6_SURVIVALIST,(None,None,27,70,3.0,1,9.0,40,30,0),1,None),
    #25.10.26 ?13% +0 -2.7 +3.2 -2.9 +5.5 n
    # 'VTBR':(PEG17_AIUR,(None,56,65,6,12,66,6,1,70,0.7),5,None),
    #01.11.26 ?16% -7 n
    # 'VTBR2':(PEG17_PHOENIX,(None,109,18,59,60,60,33,0,70),10,None),


    #26.10.26 ?38% +5.3 +3.4 +3.3 +3.1 y
    'AQUA':(UEG9_POLITICIAN,(None,None,20,0.91,10,0.26,0,32,48),1,None),
    #26.10.26 ?32% +6 +6 +1.7 +1.1 -1.5 y
    'AQUA2':(PEG17_AIUR,(None,None,5,8,51,48,24,0,70,0.5),1,None),
    #08.11.26 ?30% 
    'DATA':(PEG30_ETC2,(None,22,1,29,1,1,6,4,38,8,71,19),2,None),
    #08.11.26 ?25% 
    'DATA2':(LEG2_HOTS,(None,40,31,3.0,11,35,35,0),4,None),

    #08.11.26 ?42% 
    'FESH':(UEG9_TRACKER,(None,None,56,5.1,0.15,55,43,70,3),1,None),
    #08.11.26 ?41% 
    'FESH2':(PEG17_AIUR,(None,None,22,12,61,39,14,1,70,0.2),1,None),
    #08.11.26 ?22% 
    'HYDR':(PEG17_PHOENIX,(None,34,54,12,40,35,22,1,70),3,None),
    #08.11.26 ?21% 
    'HYDR2':(PEG14_REGAL,(None,39,16,7,49,62,54,23,70),4,None),

    #08.11.26 ?41% 
    'IVAT':(PEG11_SHIZUKAMARIKAWA,(None,10,26,57,1.4,3.1,7,12,'pedal','pedal',4,70,32,26,49,46,17,0,10,1),1,None),
    #08.11.26 ?51% 
    'IVAT2':(LEG2_DRINKER,(None,None,39,2.6,14,37,18,0),1,None),
    #26.10.26 ?31% -13.7 н
    # 'LSRG':(PEG11_RAYMIYAMOTO,(None,None,60,27,2.9,1.6,18,10,'rsi','rsi',2,70,65,84,16,3,50,20,1,1),1,None),
    #26.10.26 ?36% -15.2 н
    # 'LSRG2':(PEG17_PHOENIX,(None,13,16,7,69,17,14,1,70),2,None),

    #01.11.26 ?29% -4.8
    # 'OGKB':(PEG17_ZEALOT,(None,None,60,5,54,57,4,70),1,None),
    #01.11.26 ?33% -3.8
    # 'OGKB2':(PEG11_RAYMIYAMOTO,(None,13,22,54,1.2,0.5,39,11,'mfi','velcro',4,70,40,73,20,12,35,23,0,11),1,None),
    #26.10.26 ?15% +4.8 +0.3 +1.2 нс -6.7 s
    'OZPH':(PEG30_ETC,(None,13,0,15,1,1,24,65,66,12,80,34),1,None),
    #08.11.26 ?17% 
    'OZPH2':(LEG3a_LOTR,(None,15,23,35,50,70),2,None),

    #08.11.26 ?26% 
    'RNFT':(PEG17_ALDERA,(None,13,41,9,68,67,2,70,36,30),2,None),
    #08.11.26 ?37% 
    'RNFT2':(PEG17_PHOENIX,(None,None,34,22,14,25,23,1,70),1,None),
    #01.11.26 ?25% +4.3
    # 'SELG':(PEG14_REGAL,(None,None,7,57,48,18,50,19,70),1,None),
    #01.11.26 ?26% -28.1
    # 'SELG2':(UEG6_SURVIVALIST,(None,None,6,64,2.6,1,1.4,17,35,0),1,None),

    #26.10.26 ?25%
    # 'RTKM':(LEG2_DRG,(None,None,10,3.0,5,41,36,1),1,None),
    #26.10.26 ?21%
    # 'RTKM2':(PEG26_UNKNOWN,(None,24,52,10,47,40,13,5,34,70,0),2,None),
    #01.11.26 ?14% -0.7 n
    # 'RTKMP':(UEG9_ASTRAL,(None,5,5,2.6,0.16),1,None),
    #26.10.26 ?15%
    # 'RTKMP2':(PEG11_SAYATAKAGI,(None,6,40,70,0.5,3.2,57,42,'pedal','uo',3,70,58,11,48,49,38,0,5),1,None),
    

}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)