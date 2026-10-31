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

def add_zebra(df,period=50,percent=0.5,n_zebra=3):
    """ add 'mzebra', 'uzebraN', 'dzebraN'"""
    df['mzebra'] = df['close'].rolling(period).mean()
    buff = (df['mzebra'] * percent) / 100
    for i in range(1,n_zebra):
        df['uzebra'+str(i)] = df['mzebra'] + buff * i
        df['dzebra'+str(i)] = df['mzebra'] - buff* i
    return df

def add_zechan(df,*periods):
    """add 'tdcN','ddcN','mdcN'"""
    for i,p in enumerate(periods):
        df['tdc'+str(i)] = df['high'].rolling(p).max()
        df['ddc'+str(i)] = df['low'].rolling(p).min()
        df['mdc'+str(i)] = (df['tdc'+str(i)] + df['ddc'+str(i)]) / 2

    return df

def add_velcro_bb(df,period_check=10):
    '''add "velcro_bb"'''
    df['dbb_h'] = df['bbu'] - df['high']
    df['dbb_l'] = df['low'] - df['bbd']
    df['lis_bb'] = df['dbb_l'].rolling(period_check).mean()
    df['his_bb'] = df['dbb_h'].rolling(period_check).mean()
    df['sis_bb'] = df['lis_bb'] + df['his_bb']
    df['velcro_bb'] = ((df['lis_bb'] / df['sis_bb']) * 100).clip(0, 100)
    return df

def add_ratio_2ext_281026(df, period=70):
    """
    Векторизованная версия.
    Окно period делится пополам:
      left  half = [start, start + half)
      right half = [start + half, start + period)
    В каждой половине — max(high) и min(low).
    """
    n = len(df)
    high = df['high'].to_numpy(dtype=float)
    low = df['low'].to_numpy(dtype=float)
    df_index = df.index.to_numpy()

    half = period // 2
    rlen = period - half

    l_max = np.full(n, np.nan)
    l_min = np.full(n, np.nan)
    r_max = np.full(n, np.nan)
    r_min = np.full(n, np.nan)

    idx_l_max = np.full(n, np.nan)
    idx_l_min = np.full(n, np.nan)
    idx_r_max = np.full(n, np.nan)
    idx_r_min = np.full(n, np.nan)

    if n < period or half == 0 or rlen == 0:
        df['l_max'] = l_max
        df['l_min'] = l_min
        df['r_max'] = r_max
        df['r_min'] = r_min
        df['idx_l_max'] = idx_l_max
        df['idx_l_min'] = idx_l_min
        df['idx_r_max'] = idx_r_max
        df['idx_r_min'] = idx_r_min
        return df

    # Окна: shape (n - period + 1, period)
    win_h = np.lib.stride_tricks.sliding_window_view(high, period)
    win_l = np.lib.stride_tricks.sliding_window_view(low, period)

    lh = win_h[:, :half]
    ll = win_l[:, :half]
    rh = win_h[:, half:]
    rl = win_l[:, half:]

    pl_max = np.argmax(lh, axis=1)
    pl_min = np.argmin(ll, axis=1)
    pr_max = np.argmax(rh, axis=1)
    pr_min = np.argmin(rl, axis=1)

    # Позиция окна k в массиве соответствует бару i = k + period - 1
    rows = np.arange(win_h.shape[0])
    out_i = rows + period - 1

    l_max[out_i] = lh[rows, pl_max]
    l_min[out_i] = ll[rows, pl_min]
    r_max[out_i] = rh[rows, pr_max]
    r_min[out_i] = rl[rows, pr_min]

    idx_l_max[out_i] = df_index[rows + pl_max]
    idx_l_min[out_i] = df_index[rows + pl_min]
    idx_r_max[out_i] = df_index[rows + half + pr_max]
    idx_r_min[out_i] = df_index[rows + half + pr_min]

    df['l_max'] = l_max
    df['l_min'] = l_min
    df['r_max'] = r_max
    df['r_min'] = r_min

    df['idx_l_max'] = idx_l_max
    df['idx_l_min'] = idx_l_min
    df['idx_r_max'] = idx_r_max
    df['idx_r_min'] = idx_r_min

    return df

def add_ratio_2ext_roll_281026(df:pd.DataFrame,period=70):
    half_period = period // 2
    rlen = period - half_period  
    df['r_max'] = df['high'].rolling(rlen).max()
    df['r_min'] = df['low'].rolling(rlen).min()
    df['l_max'] = df['r_max'].shift(half_period)
    df['l_min'] = df['r_min'].shift(half_period)
    return df

def add_per_above_sma(df, period_pts=10, period_sma=30, kind='close'):
    """add 'pas','sma_fpt'"""
    df = df.copy()
    sma = df[kind].rolling(period_sma).mean()
    above = (df[kind] > sma).where(sma.notna())
    df['sma_fpt'] = sma
    df['pas'] = above.rolling(period_pts, min_periods=period_pts).mean() * 100
    return df

def add_diff_ext_channel(df:pd.DataFrame,period_dc=30,period_diff=10,type_roll_diff='mean'):
    """add 'top_dec','bot_dec', 'mean_dec' """
    dch = df['high'].rolling(period_dc).max().shift(1)
    dcl = df['low'].rolling(period_dc).min().shift(1)
    sma = df['close'].rolling(period_dc).mean()
    diff_dch = dch - sma
    diff_dcl = sma - dcl
    roll_diff_dch = diff_dch.rolling(period_diff).agg(type_roll_diff)
    roll_diff_dcl = diff_dcl.rolling(period_diff).agg(type_roll_diff)
    df['top_dec'] = sma + roll_diff_dch
    df['bot_dec'] = sma - roll_diff_dcl
    df['mean_dec'] = (df['top_dec'] + df['bot_dec'])/2
    return df