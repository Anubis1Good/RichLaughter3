from strategies.BaseEG import BaseEG
from strategies.helpEGs.helpEG import TestEG
from strategies.PEGs.PEG1_9 import PEG2_DDCrWork

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
    'ETLN1':(TestEG,tuple(),1),
    'FIXR1':(TestEG,tuple(),1),
    'MRKC1':(TestEG,tuple(),1),
    # 'MTLR1':(PEG2_DDCrWork,(30,25,20),2),
    'MTLR1':(TestEG,tuple(),1),
    'PRMD1':(TestEG,tuple(),1),
    'SGZH1':(TestEG,tuple(),1),
    'VSEH1':(TestEG,tuple(),1), 
    'VTBR1':(TestEG,tuple(),1),
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1)