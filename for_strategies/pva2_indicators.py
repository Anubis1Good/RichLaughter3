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

def add_perchan_sma(df,period=50,percent=0.5):
    """ add 'mline_pcs', 'uline_pcs', 'dline_pcs'"""
    df['mline_pcs'] = df['close'].rolling(period).mean()
    buff = (df['mline_pcs'] * percent) / 100
    df['uline_pcs'] = df['mline_pcs'] + buff
    df['dline_pcs'] = df['mline_pcs'] - buff
    return df
def add_perchan_mid(df,percent=0.5):
    """ add 'mline_pcm', 'uline_pcm', 'dline_pcm'"""
    df['mline_pcm'] = df['middle'].shift(1)
    buff = (df['mline_pcm'] * percent) / 100
    df['uline_pcm'] = df['mline_pcm'] + buff
    df['dline_pcm'] = df['mline_pcm'] - buff
    return df

def add_two_perchan(df,fast_period=5,slow_period=50,fast_percent=0.5,slow_percent=1):
    """ add 'mline_fast', 'uline_fast', 'dline_fast','mline_slow', 'uline_slow', 'dline_slow'"""
    df['mline_fast'] = df['middle'].rolling(fast_period).mean()
    buff = (df['mline_fast'] * fast_percent) / 100
    df['uline_fast'] = df['mline_fast'] + buff
    df['dline_fast'] = df['mline_fast'] - buff
    df['mline_slow'] = df['middle'].rolling(slow_period).mean()
    buff = (df['mline_fast'] * slow_percent) / 100
    df['uline_slow'] = df['mline_slow'] + buff
    df['dline_slow'] = df['mline_slow'] - buff
    return df