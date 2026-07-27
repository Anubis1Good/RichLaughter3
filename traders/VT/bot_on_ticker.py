from strategies.BaseEG import BaseEG


# wss_u = []
# configs = generate_combinations((
#     (6,11),
#     (6,11),
#     (30,60),
#     (30,60),
#     ('DC',),
#     ("rsi",),
#     (0,1),
#     (0,1)
# ))
# for conf in configs:
#     wss_u.append((PTA4_UNIVERSAL,conf))

bot_on_ticker = (
    ((BaseEG,tuple()),
     ('VTBR1','ETLN1','MTLR1','SGZH1','FIXR1','VSEH1','PRMD1','MRKC1'),
     ),
)

# sleep_group = ()

def init_trader(ticker):
    for bt in  bot_on_ticker:
        if ticker in bt[1]:
            return bt[0]
    return (BaseEG,tuple())