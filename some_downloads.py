from time import time
from datetime import date,timedelta

from loaders.ApiMoexLoader import ApiMoexLoader
from datetime import date,timedelta

today = date.today()
start_date = str(today - timedelta(days=10))
# # start_date = '2025-02-01'

# tickers = ('MTLR','IVAT','SGZH','EUTR','VTBR','RNFT','DATA','RAGR','SPBE','MAGN','VKCO','ASTR','ALRS','RUAL','IRAO','SMLT','T','ENPG','SBER','HYDR','SBERP','SELG','AQUA','AFLT','SFIN','ROSN')
tickers = ('MTLR','IVAT','SGZH','EUTR','VTBR')
# tickers = ('MTLR',)
folder_save = '_data_for_tests\data_stock_1m'
for ticker in tickers:
    # loader = ApiMoexLoader(ticker,'RFUD','forts','futures')
    loader = ApiMoexLoader(ticker)
    loader.save_df(start_date,timeframe=1,sformat='parquet',folder_save=folder_save)
    # loader.save_df(start_date,timeframe=1,sformat='csv',folder_save=folder_save)





