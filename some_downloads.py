from time import time
from datetime import date,timedelta

from loaders.ApiMoexLoader import ApiMoexLoader
from datetime import date,timedelta

today = date.today()
start_date = str(today - timedelta(days=30))
# # start_date = '2025-02-01'


tickers = (
    'SBER','VTBR','T','ROSN','NLMK','CHMF',
    'TATN','SNGSP','SIBN','MTLR','MAGN','ALRS',
    'SBERP','TATNP','AFLT','FEES','RUAL','VKCO',
    'ENPG','IRAO','SFIN','RAGR','SPBE','ASTR',
    )
# tickers = ('MTLR',)
folder_save = '_data_for_tests\data_stock_1m'
for ticker in tickers:
    # loader = ApiMoexLoader(ticker,'RFUD','forts','futures')
    loader = ApiMoexLoader(ticker)
    loader.save_df(start_date,timeframe=1,sformat='parquet',folder_save=folder_save)
    # loader.save_df(start_date,timeframe=1,sformat='csv',folder_save=folder_save)





