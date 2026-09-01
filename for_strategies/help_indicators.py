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

def add_sc_and_buffer(df:pd.DataFrame,top='max_hb',bottom='min_hb',divider=10):
    """add 'spred_channel','buffer'"""
    df['spred_channel'] = df[top] - df[bottom]
    df['buffer'] = df['spred_channel']/divider
    return df

def add_buffer_add(df:pd.DataFrame,top='max_hb',bottom='min_hb',divider=10):
    '''add top_buff, bottom_buff\n
    append outside butter
    '''
    df = add_sc_and_buffer(df,top,bottom,divider)
    df['top_buff'] = df[top]+df['buffer']
    df['bottom_buff'] = df[bottom]-df['buffer']
    return df

def add_buffer_sub(df:pd.DataFrame,top='max_hb',bottom='min_hb',divider=10):
    '''add top_buff, bottom_buff\n
    'append inside butter'
    '''
    df = add_sc_and_buffer(df,top,bottom,divider)
    df['top_buff'] = df[top]-df['buffer']
    df['bottom_buff'] = df[bottom]+df['buffer']
    return df

def add_ideal_pos(df:pd.DataFrame):
    """add 'ideal_enter','ideal_pos' \n
    !!!require add_dzz_peaks!!! \n
    actions = (None,'long_pw','short_pw','close_long_pw','close_short_pw','close_all_pw')
    """
    ideal_pos = df[~pd.isna(df['zigzag_peaks'])]
    ideal_pos = ideal_pos.copy()
    ideal_pos['ideal_enter']= np.where(ideal_pos['zigzag_direction'] == -1,1,2)

    df['ideal_enter'] = ideal_pos['ideal_enter']
    df['ideal_pos'] = df['ideal_enter'].ffill()
    df['ideal_enter'] = df['ideal_enter'].fillna(0)
    return df

