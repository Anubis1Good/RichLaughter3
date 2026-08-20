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
    'ALRS':(PEG4_U3,(5,37,18,3,23,55,'DC','rsi',),2,None),
    'ALRS2':(WEG4_PUPPY,(16,37,8,11,37,),2,None),
    'IRAO':(VEG1_VENUS,(34,98,0.6,0.8,0.1,0.9,0,1,0,),5,None),
    'IRAO2':(PEG14_RENEGADE,(37,74,14,39,40,17,42,56,),5,None),
    'MAGN':(UEG8_AVENGER,(39,54,20,0.4,0.2,0.4,7.0,0,),3,None),
    'MAGN2':(UEG4_PELICAN,(37,23,4,5,0.95,),3,None),
    'MTLR':(WEG3_DS,(33,71,42,),5,None),
    'MTLR2':(LEG1_PIN,(22,64,8,46,24,3,),5,None),
    'RUAL':(PEG4_UNIVERSAL,(49,61,6,37,41,25,'WC','s',),3,None),
    'RUAL2':(PEG11_KUSURUKEN,(45,65,49,4,31,15,'c',55,),3,None),
    'VTBR':(PEG11_KUSURUKEN,(77,202,36,4,49,25,'c',55,),10,None),
    'VTBR2':(WEG4_PUPPY,(110,83,55,39,26,),7,None),
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)