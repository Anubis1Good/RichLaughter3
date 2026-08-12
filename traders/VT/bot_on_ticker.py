from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG
from strategies.PEGs.PEG1_9 import PEG2_DDCrWork
from strategies.PEGs.PEG30_39 import PEG30_MURKY, PEG31_HYPERION

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
    """stop=None, take=None, min_spred=3, work_direction = 0, work_trend=True, large_open=100,large_close=50, n_order=1, min_step=3, period_adx=14, period_chop=14, period_sma_l=30, period_sma_s=15, thr_adx=25, thr_chop=40"""
    'ETLN1':(PEG31_HYPERION,(3,1,0,0,True,100,20,2,10),1,None),
    'FIXR1':(PEG31_HYPERION,(4,2,2,0,True,30,10,1),1,None),
    'VSEH1':(PEG31_HYPERION,(5,3,3,1,True,40,10,1),1,None),
    'PRMD1':(PEG31_HYPERION,(5,5,5,1,True,30,10,1),1,None),
    'MRKC1':(PEG31_HYPERION,(3,2,2,0,True,20,5,1),1,None),
    # 'FIXR1':(PEG30_MURKY,(5,1),1,0),
    # 'MRKC1':(PEG30_MURKY,(5,1),1,0),
    # # 'MTLR1':(PEG2_DDCrWork,(30,25,20),2,0),
    # 'PRMD1':(PEG30_MURKY,(5,1),1,0),
    # 'SGZH1':(PEG30_RAYNOR,(5,1),1,0),
    # 'VSEH1':(PEG30_MURKY,(5,1,True,3,True,False),1,0),
    # 'NKNCP':(PEG30_MURKY,(3,1,True,2,True,True),1,0), #-
    # 'APTK':(PEG30_MURKY,(3,2,True,3,True,True),1,0), #-
    # 'PRMD':(PEG30_MURKY,(5,4,True,4,True,True),1,0), #-
    # 'ROLO':(PEG30_MURKY,(3,1,True,2,True,True),1,0), #-
    # 'OGKB':(PEG30_MURKY,(3,1,True,2,True,True),1,0), #+
    # 'GLRX':(PEG30_MURKY,(5,3,True,3,True,False),1,0), #+
    # 'ENPG':(PEG30_MURKY,(5,3,True,3,True,True),1,0), #-
    # 'TGKA':(PEG30_MURKY,(4,2,True,2,True,True),1,0), #0
    # 'VSEH':(PEG30_MURKY,(5,3,True,3,True,True),1,0), #+
    # 'BTBR':(PEG30_MURKY,(4,2,True,2,True,False),5,0), #-
    # 'MGKL':(PEG30_MURKY,(4,3,True,3,True,True),1,0), #-
    # 'GECO':(PEG30_MURKY,(3,1,True,2,True,True),1,0), #-
    # 'FIXR':(PEG30_MURKY,(5,3,True,3,True,True),1,0), #+
    # 'MRKC':(PEG30_MURKY,(4,2,True,2,True,True),1,0), #+
    # 'GEMC':(PEG30_MURKY,(5,3,True,3,True,True),2,0), #+
    # 'ELFV':(PEG30_MURKY,(3,1,True,2,True,True),1,0), #-
    # 'ETLN':(PEG30_RAYNOR,(3,1),1,0), #-
    # 'HYDR':(PEG30_RAYNOR,(6,2),1,0), #-
    # 'SVAV':(PEG30_RAYNOR,(3,1),1,0), #-
    # 'DATA':(PEG30_RAYNOR,(6,2),2,0), #0
    # 'DELI':(PEG30_RAYNOR,(3,1),1,0), #-
    # 'MVID':(PEG30_RAYNOR,(3,1),1,0), #+
    # 'ABIO':(PEG30_RAYNOR,(6,2),1,0), #0
    # 'RTKMP':(PEG30_RAYNOR,(3,1),1,0), #+
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1,None)