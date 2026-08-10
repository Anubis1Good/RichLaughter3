from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG
from strategies.PEGs.PEG1_9 import PEG2_DDCrWork
from strategies.PEGs.PEG30_39 import PEG30_RAYNOR,PEG30_MURKY

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
    'ETLN1':(TestEG,tuple(),1),
    'FIXR1':(TestEG,tuple(),1),
    'MRKC1':(TestEG,tuple(),1),
    'MTLR1':(TestEG,tuple(),1),
    'PRMD1':(TestEG,tuple(),1),
    'SGZH1':(TestEG,tuple(),1),
    'VSEH1':(TestEG,tuple(),1),
    'VTBR1':(TestEG,tuple(),1),

    # 'ETLN1':(PEG30_RAYNOR,(5,1),1),
    # 'FIXR1':(PEG30_MURKY,(5,1),1),
    # 'MRKC1':(PEG30_MURKY,(5,1),1),
    # # 'MTLR1':(PEG2_DDCrWork,(30,25,20),2),
    # 'PRMD1':(PEG30_MURKY,(5,1),1),
    # 'SGZH1':(PEG30_RAYNOR,(5,1),1),
    # 'VSEH1':(PEG30_MURKY,(5,1,True,3,True,False),1),
    'NKNCP':(PEG30_MURKY,(3,1,True,2,True,True),1), #-
    'APTK':(PEG30_MURKY,(3,2,True,3,True,True),1), #-
    'PRMD':(PEG30_MURKY,(5,4,True,4,True,True),1), #-
    'ROLO':(PEG30_MURKY,(3,1,True,2,True,True),1), #-
    'OGKB':(PEG30_MURKY,(3,1,True,2,True,True),1), #+
    'GLRX':(PEG30_MURKY,(5,3,True,3,True,False),1), #+
    'ENPG':(PEG30_MURKY,(5,3,True,3,True,True),1), #-
    'TGKA':(PEG30_MURKY,(4,2,True,2,True,True),1), #0
    'VSEH':(PEG30_MURKY,(5,3,True,3,True,True),1), #+
    'BTBR':(PEG30_MURKY,(4,2,True,2,True,False),5), #-
    'MGKL':(PEG30_MURKY,(4,3,True,3,True,True),1), #-
    'GECO':(PEG30_MURKY,(3,1,True,2,True,True),1), #-
    'FIXR':(PEG30_MURKY,(5,3,True,3,True,True),1), #+
    'MRKC':(PEG30_MURKY,(4,2,True,2,True,True),1), #+
    'GEMC':(PEG30_MURKY,(5,3,True,3,True,True),2), #+
    'ELFV':(PEG30_MURKY,(3,1,True,2,True,True),1), #-
    'ETLN':(PEG30_RAYNOR,(3,1),1), #-
    'HYDR':(PEG30_RAYNOR,(6,2),1), #-
    'SVAV':(PEG30_RAYNOR,(3,1),1), #-
    'DATA':(PEG30_RAYNOR,(6,2),2), #0
    'DELI':(PEG30_RAYNOR,(3,1),1), #-
    'MVID':(PEG30_RAYNOR,(3,1),1), #+
    'ABIO':(PEG30_RAYNOR,(6,2),1), #0
    'RTKMP':(PEG30_RAYNOR,(3,1),1), #+
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1)