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
    'ALRS':(PEG14_RWDDCr,(10, 13, 26, 37, 44, 20, 55),2,None), #-1
    'ALRS2':(PEG20_HOGGER,(8, 2, 50, 7, 2.0, 1.3, 38, 25),1,None),#
    # 'MAGN':(WEG4_DOG,(39,59,4,26,),5,None), #-2
    'MAGN2':(VEG1_VENUS,(7, 17, 0.5, 0.9, 0.1, 2.0, 0, 0, 0),2,None),#+10

    'IRAO':(PEG4_UNIVERSAL,(22, 34, 15, 6, 42, 41, 'WC', 'uo', 6),3,None), #+19
    'IRAO2':(SEG1_LITE,(21, 40, 53, 1.5, 0.7, 43),4,None), #
    'MTLR':(WEG4_PUPPY,(13, 10, 23, 28, 16),2,None), #
    'MTLR2':(PEG18_BLAZE,(14, 27, 54, 5, 30, 25, 25, 0, 55),3,None), #-2

    'RUAL':(PEG8_DOBBY,(20, 51, 50, 1.9),5,None), #-2
    'RUAL2':(PEG15_SILVANA,(22, 43, 51, 36, 4),4,None), #-2
    'VTBR':(WEG3_BATYA,(43, 105, 28, 1.9, 1, 1, 1),9,None), #+4
    'VTBR2':(PEG14_RWDDCr,(38, 40, 17, 39, 2, 40, 55),4,None), #

    'ASTR':(PEG14_RWDDCr,(18, 24, 7, 15, 32, 45, 55),2,None), #+0
    'ASTR2':(LEG2_DRINKER,(6, 36, 9, 2.9, 7, 14, 37, 1),3,None), #-3
    'ROSN':(LEG2_LYNX,(33, 61, 19, 2.4, 24, 0.5, 1),6,None), #-2
    'ROSN2':(PEG15_ANNA,(17, 23, 20, 36),2,None), #

    'SBER':(LEG2_HOTS,(67, 78, 53, 2.4, 17, 36, 18, 1),7,None), #-0
    'SBER2':(PEG26_UNKNOWN,(124, 130, 7, 52, 14, 39, 23, 19, 37, 55, 0),11,None), #
    'SIBN':(LEG2_DRG,(45, 64, 45, 0.5, 23, 13, 37, 0),6,None), #
    'SIBN2':(PEG26_UNKNOWN,(36, 93, 38, 29, 26, 26, 9, 24, 4, 55, 1),8,None), #+6

    'SNGSP':(PEG4_UNIVERSAL,(38, 57, 29, 3, 27, 9, 'VG', 'mfi', 4),5,None), #+3
    'SNGSP2':(WEG3_BATYA,(40, 48, 32, 2.9, 1, 1, 1),4,None), #+2
    # 'T':(SEG3_FORCE,(125,98,55,1.8,3,2,15,25,0.7,),10,None), #+2
    'T2':(PEG14_RWDDCr,(60, 75, 24, 34, 31, 21, 55),7,None), #+1
    # 'T':(SEG3_FORCE,(125,98,55,1.8,3,2,15,25,0.7,),10,None), #+2
    # 'T2':(UEG6_VULTURE,(120,112,54,22,46,5,2,1,0.43,6,),10,None), #+7

    'AFLT':(LEG2_FENNEC,(16, 22, 8, 2.2, 7, 17, 37, 1.2, 0),2,None), #
    # 'AFLT2':(PEG4_UNIVERSAL,(32, 14, 11, 11, 27, 34, 'DC', 's', 5),3,None), #+2
    'HYDR':(WEG3_BATYA,(15, 22, 24, 2.5, 1, 1, 1),2,None), #
    'HYDR2':(LEG2_FENNEC,(14, 32, 7, 1.9, 27, 38, 27, 2.0, 0),3,None), #

    'OGKB':(PEG26_UNKNOWN,(8, 18, 50, 10, 34, 31, 4, 13, 26, 55, 1),2,None), #
    # 'OGKB2':(UEG4_PELICAN,(21, 6, 2, 2, 0.18),2,None), #-8
    # 'RTKM':(UEG4_PELICAN,(40, 36, 5, 2, 0.35),4,None), #-0 пиздит
    'RTKM2':(LEG2_HOTS,(8, 39, 39, 2.3, 16, 38, 13, 0),4,None), #
    
    'TGKA':(PEG26_UNKNOWN,(11, 4, 52, 11, 23, 9, 28, 6, 19, 55, 0),1,None),#
    # 'TGKA2':(UEG4_PELICAN,(22, 3, 2, 5, 0.14),2,None), #-8
    # 'VKCO':(LEG1_IRONANNY,(28, 25, 5, 2, 55, 7, 5),3,None), #+10
    'VKCO2':(LEG2_HOTS,(12, 24, 54, 2.2, 5, 20, 14, 0),2,None), #
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)