from strategies.BaseEG import BaseEG

# bot_on_ticker = (
#     (
#         (BaseEG,tuple()),
#         ('VTBR1','ETLN1','MTLR1','SGZH1','FIXR1','VSEH1','PRMD1','MRKC1'),
#      ),
# )

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
bot_on_ticker = {
    'ETLN1':(BaseEG,tuple(),1),
    'FIXR1':(BaseEG,tuple(),1),
    'MRKC1':(BaseEG,tuple(),1),
    'MTLR1':(BaseEG,tuple(),1),
    'PRMD1':(BaseEG,tuple(),1),
    'SGZH1':(BaseEG,tuple(),1),
    'VSEH1':(BaseEG,tuple(),1),
    'VTBR1':(BaseEG,tuple(),1),
}
# sleep_group = ()

def init_trader(ticker):
    if ticker in bot_on_ticker:
        return bot_on_ticker[ticker]
    return (BaseEG,tuple(),1)