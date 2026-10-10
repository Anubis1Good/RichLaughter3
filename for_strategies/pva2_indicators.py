import pandas as pd
import numpy as np

def add_perdirlong(df:pd.DataFrame, period:int=20,use_s=True,use_v=True):
    "add 'pedal', 'wpedal', 'diff_pedals'"
    df['spred'] = (df['high'] - df['low'])
    if use_s:
        df['dirlong'] = np.where(df['direction'] == 1,df['spred'],0)
        df['totalsum'] = df['spred'].rolling(period).sum()
        df['dirlongsum'] = df['dirlong'].rolling(period).sum()
        df['pedal'] = (df['dirlongsum'] / df['totalsum']) * 100
    if use_v:
        df['spred_vol'] = df['spred']*df['volume']
        df['dirlong_vol'] = np.where(df['direction'] == 1,df['spred_vol'],0)
        df['totalsum_vol'] = df['spred_vol'].rolling(period).sum()
        df['dirlongsum_vol'] = df['dirlong_vol'].rolling(period).sum()
        df['wpedal'] = (df['dirlongsum_vol'] / df['totalsum_vol']) * 100
    if use_v and use_s:
        df['diff_pedals'] = df['wpedal'] - df['pedal']
    return df

def add_real_perdirlong(df:pd.DataFrame, period:int=20,use_s=True,use_v=True):
    "add 'real_pedal', 'real_wpedal', 'real_diff_pedals'"
    df['spred'] = (df['high'] - df['low'])
    df['real_dir'] = np.where(df['middle'] < df['middle'].shift(1),-1,1)
    if use_s:
        df['dirlong'] = np.where(df['real_dir'] == 1,df['spred'],0)
        df['totalsum'] = df['spred'].rolling(period).sum()
        df['dirlongsum'] = df['dirlong'].rolling(period).sum()
        df['real_pedal'] = (df['dirlongsum'] / df['totalsum']) * 100
    if use_v:
        df['spred_vol'] = df['spred']*df['volume']
        df['dirlong_vol'] = np.where(df['real_dir'] == 1,df['spred_vol'],0)
        df['totalsum_vol'] = df['spred_vol'].rolling(period).sum()
        df['dirlongsum_vol'] = df['dirlong_vol'].rolling(period).sum()
        df['real_wpedal'] = (df['dirlongsum_vol'] / df['totalsum_vol']) * 100
    if use_v and use_s:
        df['real_diff_pedals'] = df['real_wpedal'] - df['real_pedal']
    return df