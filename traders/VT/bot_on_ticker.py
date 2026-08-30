from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG
from strategies.all_egs import *
# from strategies.PEGs.PEG1_9 import PEG2_DDCrWork
# from strategies.PEGs.PEG30_39 import PEG30_MURKY, PEG31_HYPERION

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
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


    # 'AFLT':(LEG2_FENNEC,(16, 22, 8, 2.2, 7, 17, 37, 1.2, 0),2,None), # -1
    # # 'AFLT2':(PEG4_UNIVERSAL,(32, 14, 11, 11, 27, 34, 'DC', 's', 5),3,None), #+2
    # 'ALRS':(PEG14_RWDDCr,(10, 13, 26, 37, 44, 20, 55),2,None), #-1 -1
    # 'ALRS2':(PEG20_HOGGER,(8, 2, 50, 7, 2.0, 1.3, 38, 25),1,None),#+1
    # 'ASTR':(PEG14_RWDDCr,(18, 24, 7, 15, 32, 45, 55),2,None), #+0 +3
    # 'ASTR2':(LEG2_DRINKER,(6, 36, 9, 2.9, 7, 14, 37, 1),3,None), #-3 -1
    'CHMF':(VEG1_VENUS,(None,None,0.3,0.8,0.1,2.0,1,0,0),1,None), #
    'CHMF2':(UEG7_PIGEON,(None,None,53,5,55,4,3,0.04,0.4,0),1,None), #
    # 'FEES':(PEG14_RWDDCr,(18, 24, 7, 15, 32, 45, 55),2,None), #
    # 'FEES2':(LEG2_DRINKER,(6, 36, 9, 2.9, 7, 14, 37, 1),3,None), #
    # # 'MAGN':(WEG4_DOG,(39,59,4,26,),5,None), #-2
    # 'MAGN2':(VEG1_VENUS,(7, 17, 0.5, 0.9, 0.1, 2.0, 0, 0, 0),2,None),#+10 +1
    # 'MTLR':(WEG4_PUPPY,(13, 10, 23, 28, 16),2,None), # +1
    # 'MTLR2':(PEG18_BLAZE,(14, 27, 54, 5, 30, 25, 25, 0, 55),3,None), #-2 +5
    'NLMK':(LEG2_LYNX,(None,None,4,1.8,2,1.4,0),1,None), #
    'NLMK2':(PEG18_BLAZE,(None,None,22,4,14,32,28,0,55),1,None), #
    # 'RAGR':(LEG2_LYNX,(33, 61, 19, 2.4, 24, 0.5, 1),6,None), #
    # 'RAGR2':(PEG15_ANNA,(17, 23, 20, 36),2,None), #
    'ROSN':(LEG2_FENNEC,(None,58,27,2.6,17,39,33,1.4,0),5,None), #
    'ROSN2':(PEG14_RENEGADE,(None,None,16,38,52,6,49,30),1,None), #
    # 'RUAL':(PEG8_DOBBY,(20, 51, 50, 1.9),5,None), #-2 -3 
    # 'RUAL2':(PEG15_SILVANA,(22, 43, 51, 36, 4),4,None), #-2 -4
    'SBER':(PEG14_RENEGADE,(None,None,19,39,31,25,12,46),1,None), #
    'SBER2':(PEG4_U3,(112,None,53,23,2,55,'BB','mfi',4),10,None), #
    # 'SBERP':(LEG2_HOTS,(67, 78, 53, 2.4, 17, 36, 18, 1),7,None), #
    # 'SBERP2':(PEG26_UNKNOWN,(124, 130, 7, 52, 14, 39, 23, 19, 37, 55, 0),11,None), #
    # 'SFIN':(LEG2_HOTS,(67, 78, 53, 2.4, 17, 36, 18, 1),7,None), #
    # 'SFIN2':(PEG26_UNKNOWN,(124, 130, 7, 52, 14, 39, 23, 19, 37, 55, 0),11,None), #
    # 'SGZH':(LEG2_HOTS,(67, 78, 53, 2.4, 17, 36, 18, 1),7,None), #
    # 'SGZH2':(PEG26_UNKNOWN,(124, 130, 7, 52, 14, 39, 23, 19, 37, 55, 0),11,None), #
    # 'SIBN':(LEG2_DRG,(45, 64, 45, 0.5, 23, 13, 37, 0),6,None), # -6
    # 'SIBN2':(PEG26_UNKNOWN,(36, 93, 38, 29, 26, 26, 9, 24, 4, 55, 1),8,None), #+6 -2
    # 'SMLT':(LEG2_DRG,(45, 64, 45, 0.5, 23, 13, 37, 0),6,None), #
    # 'SMLT2':(PEG26_UNKNOWN,(36, 93, 38, 29, 26, 26, 9, 24, 4, 55, 1),8,None), #
    # 'SNGSP':(PEG4_UNIVERSAL,(38, 57, 29, 3, 27, 9, 'VG', 'mfi', 4),5,None), #+3 -4
    # 'SNGSP2':(WEG3_BATYA,(40, 48, 32, 2.9, 1, 1, 1),4,None), #+2 +3
    # 'SPBE':(PEG4_UNIVERSAL,(38, 57, 29, 3, 27, 9, 'VG', 'mfi', 4),5,None), #
    # 'SPBE2':(WEG3_BATYA,(40, 48, 32, 2.9, 1, 1, 1),4,None), #
    'T':(LEG2_LYNX,(None,None,53,1.5,32,0.5,0),1,None), #
    'T2':(PEG11_KUSURUKEN,(None,None,47,7,23,8,'c',55),1,None), #
    # # 'TATN':(SEG3_FORCE,(125,98,55,1.8,3,2,15,25,0.7,),10,None), #
    # # 'TATN2':(UEG6_VULTURE,(120,112,54,22,46,5,2,1,0.43,6,),10,None), #
    # # 'TATNP':(SEG3_FORCE,(125,98,55,1.8,3,2,15,25,0.7,),10,None), #
    # # 'TATNP2':(UEG6_VULTURE,(120,112,54,22,46,5,2,1,0.43,6,),10,None), #
    # # 'VKCO':(LEG1_IRONANNY,(28, 25, 5, 2, 55, 7, 5),3,None), #+10
    # # 'VKCO2':(LEG2_HOTS,(12, 24, 54, 2.2, 5, 20, 14, 0),2,None), # -10
    # 'VTBR':(WEG3_BATYA,(43, 105, 28, 1.9, 1, 1, 1),9,None), #+4 +0
    # 'VTBR2':(PEG14_RWDDCr,(38, 40, 17, 39, 2, 40, 55),4,None), # +1
    
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)