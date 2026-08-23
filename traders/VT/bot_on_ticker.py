from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG
from strategies.all_egs import *
# from strategies.PEGs.PEG1_9 import PEG2_DDCrWork
# from strategies.PEGs.PEG30_39 import PEG30_MURKY, PEG31_HYPERION

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
    'ETLN1':(TestEG,tuple(),1,None),
    'FIXR1':(TestEG,tuple(),1,None),
    'MRKC1':(TestEG,tuple(),1,None),
    'MTLR1':(TestEG,tuple(),1,None),
    'PRMD1':(TestEG,tuple(),1,None),
    'SGZH1':(TestEG,tuple(),1,None),
    'VSEH1':(TestEG,tuple(),1,None),
    'VTBR1':(TestEG,tuple(),1,None),
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
    'ALRS':(WEG7_PARADOX,(20,19,28,1.4,),2,None), #
    'ALRS2':(UEG6_VULTURE,(20,15,50,55,43,30,4,5,0.28,15,),2,None), #+
    'MAGN':(WEG4_DOG,(39,59,4,26,),5,None), #
    'MAGN2':(LEG2_DRINKER,(39,75,46,2.7,4,23,11,1,),6,None),#
    'IRAO':(LEG1_IRONANNY,(41,57,10,3,55,7,),5,None), #+
    'IRAO2':(PEG17_PHOENIX,(49,49,27,9,16,41,15,1,55,),4,None), #+
    'MTLR':(UEG4_FALCON,(33,75,4,2,0.32,),6,None), #
    'MTLR2':(WEG3_DS,(37,49,44,),4,None), #
    'RUAL':(PEG18_BLAZE,(49,91,24,4,49,34,37,0,55,),7,None), #
    'RUAL2':(PEG4_U3,(46,96,44,21,2,55,'BB','mfi',),7,None), #
    'VTBR':(PEG11_KUSURUKEN,(109,213,23,6,23,15,'hl',55,),16,None), #
    'VTBR2':(LEG2_FENNEC,(97,157,30,2.0,5,38,14,0.6,0,),11,None), #-

    'ASTR':(WEG4_DOG,(39,78,7,30,),6,None), #
    'ASTR2':(LEG2_DRINKER,(34,68,23,2.9,6,31,17,1,),5,None), #
    'ROSN':(PEG4_UNIVERSAL,(66,47,27,5,35,12,'DC','mfi',4,),5,None), #-
    'ROSN2':(UEG8_AVENGER,(61,116,19,0.0,1.0,1.0,9.5,0,),9,None), #-
    'SBER':(LEG1_PIN,(209,338,5,16,23,4,),25,None), #-
    'SBER2':(PEG14_RENEGADE,(267,440,16,39,48,18,28,54,),32,None), #+
    'SIBN':(LEG1_PHOGA,(85,173,3,1.1,7,),14,None), #
    'SIBN2':(PEG26_UNKNOWN,(86,173,54,42,27,37,29,9,15,55,0,),14,None), #
    'SNGSP':(PEG4_UNIVERSAL,(78,128,31,27,43,8,'VC','s',6,),10,None), #+
    'SNGSP2':(LEG1_CC,(51,97,16,5,55,10,53,1.1,0,1,),7,None), #+
    'T':(SEG3_FORCE,(125,98,55,1.8,3,2,15,25,0.7,),10,None), #
    'T2':(UEG6_VULTURE,(120,112,54,22,46,5,2,1,0.43,6,),10,None), #

    'AFLT':(WEG3_BATYA,(18, 18, 6, 1.1, 1, 0, 1),2,None), #
    'AFLT2':(PEG4_UNIVERSAL,(32, 14, 11, 11, 27, 34, 'DC', 's', 5),3,None), #
    'HYDR':(WEG3_BATYA,(29, 9, 45, 1.2, 1, 1, 1),3,None), #
    'HYDR2':(PEG4_UNIVERSAL,(11, 15, 18, 7, 5, 11, 'VC', 's', 3),2,None), #
    'OGKB':(UEG6_DODO,(11, 18, 10, 2, 59, 67),2,None), #
    'OGKB2':(UEG4_PELICAN,(21, 6, 2, 2, 0.18),2,None), #
    'RTKM':(UEG4_PELICAN,(40, 36, 5, 2, 0.35),4,None), #
    'RTKM2':(PEG4_UNIVERSAL,(42, 42, 6, 21, 38, 19, 'VC', 's', 3),4,None), #
    'TGKA':(PEG4_UNIVERSAL,(22, 8, 2, 2, 41, 38, 'VG', 'rsi_tw', 4),2,None), #
    'TGKA2':(UEG4_PELICAN,(22, 3, 2, 5, 0.14),2,None), #
    'VKCO':(LEG1_IRONANNY,(28, 25, 5, 2, 55, 7, 5),3,None), #
    'VKCO2':(LEG2_HOTS,(26, 27, 29, 2.0, 5, 27, 37, 1),3,None), #
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)