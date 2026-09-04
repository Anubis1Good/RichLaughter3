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


    'AFLT':(PEG17_PHOENIX,(None,29,29,12,54,42,6,0,55),3,None), #+1 +10 +10 !
    'AFLT2':(PEG13_DWDDCr,(None,None,17,31,9),1,None), #+2 -1 .
    'ALRS':(LEG2_DRINKER,(None,16,5,2.1,5,31,16,0),2,None), # +16 +0 -0 +5 !
    'ALRS2':(UEG6_VULTURE,(None,18,51,42,18,6,3,3,0.81,12),2,None),#-2 -0 -4 .

    'ASTR':(WEG3_BATYA,(None,40,21,2.1,1,1,1),4,None), #-4 +11 +8 +1 !
    'ASTR2':(LEG1_LAKSAe,(None,35,26,6),3,None), #+1 +4 +1 .
    'ASTR2':(PEG17_PHOENIX,(None,None,16,30,47,21,38,1,55),1,None), #
    'CHMF':(VEG1_VENUS,(None,None,0.3,0.8,0.1,2.0,1,0,0),1,None), # +5 -5 +13 +1 !
    'CHMF2':(UEG4_PELICAN,(None,17,4,3,0.03),2,None), #+0 -7 .

    'FEES':(PEG11_KUSURUKEN,(None,None,25,55,35,9,'c',55),1,None), #-2 +4 -1 .
    'FEES2':(WEG4_PUPPY,(None,None,16,16,12),1,None), #+1 0 -5 -0 .
    'MAGN':(PEG18_BLAZE,(None,None,43,10,54,38,20,0,55),1,None), #-3 +3 -3 -15 .
    'MAGN2':(VEG1_VENUS,(7, 17, 0.5, 0.9, 0.1, 2.0, 0, 0, 0),2,None),#+10 +1 +1 -12 -1 -5 .

    'MTLR':(PEG11_KUSURUKEN,(None,None,44,8,51,36,'c',55),1,None), #+9 +7 -3 !
    'MTLR2':(LEG2_LYNX,(None,17,33,2.0,5,0.6,0),2,None), #-10 НБС .
    'NLMK':(PEG18_BLAZE,(None,None,22,4,14,32,28,0,55),1,None), #-2 -6 -13 .
    'NLMK2':(LEG2_LYNX,(None,None,4,1.8,2,1.4,0),1,None), #+1 .

    'RAGR':(UEG4_FALCON,(None,None,3,4,0.74),1,None), # -7 -5 .
    'RAGR2':(UEG4_PELICAN,(None,None,3,2,0.34),1,None), #+6 -4 +2 .
    'ROSN':(LEG2_FENNEC,(None,58,27,2.6,17,39,33,1.4,0),5,None), #-1 -2 +1 +6  .
    'ROSN2':(PEG14_RENEGADE,(None,None,16,38,52,6,49,30),1,None), #+5 +2 !

    'RUAL':(VEG1_VENUS,(None,None,0.3,1.0,0.1,0.5,0,1,1),1,None), #-6 -3 +6 .
    'RUAL2':(LEG2_DRG,(None,None,12,2.7,4,15,11,1),1,None), #-3 +1 -10 .
    'SBER':(PEG14_RENEGADE,(None,None,19,39,31,25,12,46),1,None), #+0 -0 .
    'SBER2':(PEG4_U3,(112,None,53,23,2,55,'BB','mfi',4),10,None), #+1 +2 +2 +1 !

    'SBERP':(PEG11_KUSURUKEN,(None,None,36,38,45,10,'c',55),1,None), #-1 -1 -1 -1 .
    'SBERP2':(PEG26_UNKNOWN,(None,None,46,33,23,39,8,20,4,55,0),1,None), #+1 -1 .
    'SFIN':(LEG2_DRINKER,(None,None,42,2.0,4,26,11,0),1,None), #+22 +6 -9 !
    'SFIN2':(LEG1_PIN,(None,None,4,6,26,3),1,None), #+11 -1 !

    # 'ENPG':(UEG6_DODO,(None,None,27,9,42,66),1,None),#
    # 'ENPG2':(PEG17_PHOENIX,(None,12,10,10,17,36,10,0,55),1,None), #
    'SIBN':(WEG3_BATYA,(None,None,18,1.3,0,1,1),1,None), #+1 +3 +1 +0 .
    'SIBN2':(LEG1_PHOGA,(None,None,2,1.1,18),1,None), #-6 .

    # 'IRAO':(VEG1_VENUS,(None,None,0.2,0.8,0.1,0.7,1,1,1),1,None), #
    # 'IRAO2':(UEG6_PIGEON,(None,None,30,3,2,2,4,0.64,2.0,0),1,None), #
    'SNGSP':(LEG2_FENNEC,(None,None,9,2.5,2,31,19,1.8,1),1,None), #+1 +1 -1 +1 .
    'SNGSP2':(WEG3_BATYA,(40, 48, 32, 2.9, 1, 1, 1),4,None), #+2 +3 +5 -3 +3 +2 !


    'SPBE':(PEG11_KUSURUKEN,(None,None,53,8,29,37,'c',55),1,None), #+7 +2 +5 !
    'SPBE2':(PEG18_BLAZE,(None,None,47,12,40,37,33,0,55),1,None), #+5 0 +6 -12 .
    'T':(LEG2_LYNX,(None,None,53,1.5,32,0.5,0),1,None), #+0 -1 .
    'T2':(PEG11_KUSURUKEN,(None,None,47,7,23,8,'c',55),1,None), #-3 -0 -2 0 .

    'TATN':(LEG1_PIN,(20,None,48,3,39,3),2,None), #+5 +9 +11 !
    'TATN2':(WEG4_PUPPY,(None,None,41,39,11),1,None), #+7 +9 +4 +7 !
    'TATNP':(LEG2_LYNX,(None,None,5,2.0,6,0.8,0),1,None), #-3 +3 -4 +2 .
    'TATNP2':(SEG3_FORCE,(None,None,14,3.0,3,9,53,43,0.5),1,None), #+6 +2 +7 !
    
    'VKCO':(PEG17_PHOENIX,(None,None,9,12,50,43,26,0,55),1,None), #+14 +10 +2 !
    'VKCO2':(PEG11_KUSURUKEN,(None,None,21,13,47,20,'c',55),1,None), #+4 -7 +1 -17 .
    'VTBR':(WEG3_BATYA,(None,None,15,2.0,1,1,1),1,None), #-3 +4 -4 -1 .
    'VTBR2':(PEG4_UNIVERSAL,(None,None,23,13,12,36,'VG','s',6),1,None), #-2 +1 .
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)