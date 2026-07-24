import os
from time import time
import requests
import apimoex
import pandas as pd
import numpy as np

class ApiMoexLoader:
    def __init__(self,symbol,board: str = "TQBR",market:str="shares", engine:str = "stock"):
        self.symbol = symbol
        self.board = board
        self.market = market
        self.engine = engine
    
    def load_data(self,start,end=None,timeframe=1):
        """K-line particle size
            1 - 1 минута
            10 - 10 минут
            60 - 1 час
            24 - 1 день
            7 - 1 неделя
            31 - 1 месяц
            4 - 1 квартал
        """
        with requests.Session() as session:
            data = apimoex.get_board_candles(session, self.symbol,timeframe,start,end,board=self.board,market=self.market,engine=self.engine)
            df = pd.DataFrame(data)

        return df

    def processing_df(self, df: pd.DataFrame):
        df = df.copy()
        
        # Переименование и вычисления
        df = df.rename(columns={'value': "vol_coin", 'begin': 'ms'})
        df['ms'] = pd.to_datetime(df['ms'])
        df['weekday'] = df['ms'].dt.dayofweek
        df['hour'] = df['ms'].dt.hour
        df['minute'] = df['ms'].dt.minute
        df['direction'] = np.where(df['open'] < df['close'], 1, -1)
        df['middle'] = (df['high'] + df['low']) / 2
        df = df.reset_index(drop=True)
        df['x'] = df.index
        
        # Умный downcast для всех числовых колонок
        for col in df.select_dtypes(include=[np.number]).columns:
            # Проверяем, содержит ли колонка только целые числа
            if pd.api.types.is_integer_dtype(df[col]) or (df[col] % 1 == 0).all():
                df[col] = pd.to_numeric(df[col], downcast='integer')
            else:
                df[col] = pd.to_numeric(df[col], downcast='float')
        
        return df
    
    def save_df(self,start,end=None,timeframe=1,folder_save='_data_for_tests/data_from_moex',sformat='parquet'):
        """K-line particle size
        1 - 1 минута
        10 - 10 минут
        60 - 1 час
        24 - 1 день
        7 - 1 неделя
        31 - 1 месяц
        4 - 1 квартал
        """
        df = self.load_data(start,end,timeframe)
        df = self.processing_df(df)
        if not os.path.exists(folder_save):
            os.makedirs(folder_save)
        path = os.path.join(folder_save,self.symbol+"_"+str(timeframe)+'_'+str(time()).split(".")[0])
        if sformat == 'parquet':
            path += '.parquet'
            df.to_parquet(path)
        else:
            path +='.csv'
            df.to_csv(path)
        print('Датафрейм сохранен в', path)


# class ISSMoexLoader:
#     def __init__(self,board: str = "TQBR",market:str="shares", engine:str = "stock"):
#         self.board = board
#         self.market = market
#         self.engine = engine

#     def get_all_tickers(self):
#         data = requests.get(f'https://iss.moex.com/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}/securities.json')
#         data = data.json()['securities']
#         columns_data = data['columns']
#         main_data = data['data']
#         df = pd.DataFrame(main_data,columns=columns_data)
#         return df

#     def get_candels(self,symbol,start,end=None,timeframe=24):
#         """K-line particle size
#             1 - 1 минута
#             10 - 10 минут
#             60 - 1 час
#             24 - 1 день
#             7 - 1 неделя
#             31 - 1 месяц
#             4 - 1 квартал
#         """
#         candels = requests.get(f'https://iss.moex.com/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}//securities/{symbol}/candles.json?from={start}&interval={timeframe}')
#         candels = candels.json()['candles']
#         col_candels = candels['columns']
#         data_candels = candels['data']
#         df = pd.DataFrame(data_candels,columns=col_candels)

#         return df

#     def processing_df_candels(self, df: pd.DataFrame):
#         df = df.copy()
        
#         # Переименование и вычисления
#         df = df.rename(columns={'value': "vol_coin", 'begin': 'ms'})
#         df['ms'] = pd.to_datetime(df['ms'])
#         df['weekday'] = df['ms'].dt.dayofweek
#         df['hour'] = df['ms'].dt.hour
#         df['minute'] = df['ms'].dt.minute
#         df['direction'] = np.where(df['open'] < df['close'], 1, -1)
#         df['middle'] = (df['high'] + df['low']) / 2
#         df = df.reset_index(drop=True)
#         df['x'] = df.index
        
#         # Умный downcast для всех числовых колонок
#         for col in df.select_dtypes(include=[np.number]).columns:
#             # Проверяем, содержит ли колонка только целые числа
#             if pd.api.types.is_integer_dtype(df[col]) or (df[col] % 1 == 0).all():
#                 df[col] = pd.to_numeric(df[col], downcast='integer')
#             else:
#                 df[col] = pd.to_numeric(df[col], downcast='float')
        
#         return df
    
#     def save_df_candels(self,symbol,start,end=None,timeframe=1,folder_save='data_for_tests/data_from_moex',sformat='parquet'):
#         """K-line particle size
#         1 - 1 минута
#         10 - 10 минут
#         60 - 1 час
#         24 - 1 день
#         7 - 1 неделя
#         31 - 1 месяц
#         4 - 1 квартал
#         """
#         df = self.get_candels(symbol,start,end,timeframe)
#         df = self.processing_df_candels(df)
#         if not os.path.exists(folder_save):
#             os.makedirs(folder_save)
#         path = os.path.join(folder_save,self.symbol+"_"+str(timeframe)+'_'+str(time()).split(".")[0])
#         if sformat == 'parquet':
#             path += '.parquet'
#             df.to_parquet(path)
#         else:
#             path +='.csv'
#             df.to_csv(path)
#         print('Датафрейм сохранен в', path)