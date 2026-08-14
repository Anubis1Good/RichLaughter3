import pandas as pd
import numpy as np

def add_over_bb(df:pd.DataFrame):
    '''add over_bbu and over_bbd'''
    df['over_bbu'] = df['bbu'] < df['low']
    df['over_bbd'] = df['bbd'] > df['high']
    return df

def get_attached_bb(row,df:pd.DataFrame):
    bbu_attached = False
    bbd_attached = False
    if row.name > 1:
        prev = df.loc[row.name-1]
        if row['high'] > row['bbu'] or prev['high'] > prev['bbu']:
            bbu_attached = True
        if row['low'] < row['bbd'] or prev['low'] < prev['bbd']:
            bbd_attached = True
    return np.array([bbu_attached,bbd_attached])

def get_change_attached_bb(row,df:pd.DataFrame):
    attached_change = False
    if row.name > 1:
        prev = df.iloc[row.name-1]
        if row['bbu_attached'] != prev['bbu_attached']:
            attached_change = True
        if row['bbd_attached'] != prev['bbd_attached']:
            attached_change = True
    return attached_change

def add_attached_bb(df:pd.DataFrame):
    """add bbu_attached, bbd_attached, attached_change"""
    points = df.apply(lambda row: get_attached_bb(row,df),axis=1)
    points = np.stack(points.values)
    df['bbu_attached'] = pd.Series(points[:,0])
    df['bbd_attached'] = pd.Series(points[:,1])
    df['attached_change'] = df.apply(lambda row: get_change_attached_bb(row,df),axis=1)
    return df

def add_big_volume(df:pd.DataFrame,period=20,multiplier=1):
    """add sma_volume, is_big """
    df['sma_volume'] = df['volume'].rolling(period).mean()
    df['is_big'] = df['volume']*multiplier > df['sma_volume']
    return df