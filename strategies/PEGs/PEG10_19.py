import numpy as np
from strategies.BaseEG import BaseEG
from for_strategies.classic_indicators import add_rsi,add_chop,add_awesome_oscillator,add_donchan_channel,add_adx,add_supertrend,add_mfi,add_stochastic,add_ultimate_oscillator
from for_strategies.pva_indicators import add_kusuruken_channel,add_velcro_indicator,add_quantile_params,add_benefit,get_all_enter_exit_DC,get_all_lup,add_pc_stair_fast,add_integrity_index,add_assessment_motion_index,add_hope_channel,add_cascade_channel,add_kusuruken_bb
from for_strategies.pva2_indicators import add_perdirlong,add_real_perdirlong
from for_strategies.other_indicators import add_vangerchik
from for_strategies.fix_params import fix_supertrend_params,fix_two_periods_hm,fix_three_periods_hm

# скорее всего сильно чувствтителен к смене тренда
# 05.10.2026 сделать версию без открытий по:            
# if row[self.kind_enter_l] <= row['avarege2']:
    # return 'open_long'
# из-за этого может открывать на самом дне.
class PEG11_KUSURUKEN(BaseEG):
    """stop=None, take=None, period=55, period2=10, period3=20, threshold=20, kind_enter='hl',max_period=55 \n
    kind_enter -> hl | c
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, period2=10, period3=20, threshold=20, kind_enter='hl',max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        can_period = max_period // 3
        self.period3 = min(can_period,period3)
        max_total = can_period * 2
        total = self.period3 + period2

        if total > max_total:
            ratio = max_total / total
            self.period3 = int(self.period3 * ratio)
            self.period2 = int(period2 * ratio)
        else:
            self.period2 = period2

        self.threshold = threshold
        self.kind_enter_l = 'low' if kind_enter == 'hl' else 'close'
        self.kind_enter_s = 'high' if kind_enter == 'hl' else 'close'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_channel(df, self.period2, self.period)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # trend_context
        if row['sma'] > row['sma2']:
            # long_context
            if row["avarege"] > row['avarege2']:
                if row['rsi'] > 100 - self.threshold + 10:
                    return 'close_long'
                if row[self.kind_enter_l] <= row['avarege2']:
                    return 'open_long'
            # short_context
            else:
                if row['rsi'] < self.threshold - 10:
                    return 'close_short'
                if row[self.kind_enter_s] >= row['avarege2']:
                    return 'open_short'
        # range_context
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not nearest_long and row['rsi'] > 100 - self.threshold:
                return 'open_short'

# 13.10.2026 кажется бывает слишком сложно закрыть позицию
# 13.10.2026 бывает перетягивает сделки
class PEG11_RAYMIYAMOTO(BaseEG):
    """stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=50,thresh_chop=60,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_enter=30,thresh_rb_exit=40,use_safe=1,offset_chop=10
    \n
    kind_rsi in ["rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"]
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=50,thresh_chop=60,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_enter=30,thresh_rb_exit=40,use_safe=1,offset_chop=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bkb = period_bkb
        self.period_skb = period_skb
        self.mult_bkb = mult_bkb
        self.mult_skb = mult_skb
        self.period_rsi_big = period_rsi_big
        self.period_rsi_small = period_rsi_small
        self.period_chop = period_chop
        if kind_rsi_big == 'velcro' and self.period_rsi_big*2 > max_period:
            self.period_rsi_big = max_period // 2
        if kind_rsi_small == 'velcro' and self.period_rsi_small*2 > max_period:
            self.period_rsi_small = max_period // 2

        self.kind_rsi_big = kind_rsi_big
        self.kind_rsi_small = kind_rsi_small
        self.period2s = period2s
        self.thresh_chop = thresh_chop
        self.thresh_rs_enter = thresh_rs_enter
        self.thresh_rs_exit = thresh_rs_exit
        self.thresh_rb_enter = thresh_rb_enter
        self.thresh_rb_exit = thresh_rb_exit
        self.use_safe = use_safe
        self.offset_chop = offset_chop

    def add_rsi(self, df, kind_rsi, period_rsi, rename):
        if kind_rsi == 'velcro':
            df['max_hb'] = df['high'].rolling(period_rsi).max()
            df['min_hb'] = df['low'].rolling(period_rsi).min()
            df = add_velcro_indicator(df,period_rsi)
            df = df.rename({'velcro': rename}, axis=1)
        elif kind_rsi == 'pedal':
            df = add_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'pedal': rename}, axis=1)
        elif kind_rsi == 'wpedal':
            df = add_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'wpedal': rename}, axis=1)
        elif kind_rsi == 'real_pedal':
            df = add_real_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'real_pedal': rename}, axis=1)
        elif kind_rsi == 'real_wpedal':
            df = add_real_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'real_wpedal': rename}, axis=1)
        elif kind_rsi == 'mfi':
            df = add_mfi(df, period_rsi)
            df = df.rename({'mfi': rename}, axis=1)
        elif kind_rsi == 's':
            df = add_stochastic(df, period_rsi, self.period2s)
            df = df.rename({'%d': rename}, axis=1)
        elif kind_rsi == 'uo':
            df = add_ultimate_oscillator(df, period_rsi // 3, period_rsi // 2, period_rsi)
            df = df.rename({'ultimate_oscillator': rename}, axis=1)
        else:
            df = add_rsi(df, period_rsi)
            df = df.rename({'rsi': rename}, axis=1)
        return df
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_bb(df, self.period_bkb,self.period_skb,self.mult_bkb,self.mult_skb)
        df = self.add_rsi(df,self.kind_rsi_big,self.period_rsi_big,'rsi_big')
        df = self.add_rsi(df,self.kind_rsi_small,self.period_rsi_small,'rsi_small')
        df = add_chop(df, self.period_chop)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # trend_context
        if row['chop'] < self.thresh_chop-self.offset_chop:
            if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_enter:
                return 'open_short'
            if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_exit:
                return 'close_long'
            if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_enter:
                return 'open_long'
            if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_exit:
                return 'close_short'
            # long_context
            if row["sma_small"] > row['sma_big']:
                if row['close'] <= row["sma_small"]:
                    return 'open_long'
            # short_context
            else:
                if row['close'] >= row["sma_small"]:
                    return 'open_short'
        # range_context
        elif row['chop'] >= self.thresh_chop+self.offset_chop:
            if row['close'] >= row['bbu_big']:
                if not self.use_safe:
                    return 'open_short'
            if row['close'] <= row['bbd_big']:
                if not self.use_safe:
                    return 'open_long'
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_enter:
                    return 'open_short' 
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_enter:
                    return 'open_long' 
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
        else:
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
            if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_exit:
                return 'close_long'
            if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_exit:
                return 'close_short'
            
class PEG11_SHIZUKAMARIKAWA(BaseEG):
    """stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=10,thresh_chop=30,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_exit=40,use_safe=1,offset_chop=10,close_trend=1
    \n
    kind_rsi in ["rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"]
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=10,thresh_chop=30,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_exit=40,use_safe=1,offset_chop=10,close_trend=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bkb = period_bkb
        self.period_skb = period_skb
        self.mult_bkb = mult_bkb
        self.mult_skb = mult_skb
        self.period_rsi_big = period_rsi_big
        self.period_rsi_small = period_rsi_small
        self.period_chop = period_chop
        if kind_rsi_big == 'velcro' and self.period_rsi_big*2 > max_period:
            self.period_rsi_big = max_period // 2
        if kind_rsi_small == 'velcro' and self.period_rsi_small*2 > max_period:
            self.period_rsi_small = max_period // 2

        self.kind_rsi_big = kind_rsi_big
        self.kind_rsi_small = kind_rsi_small
        self.period2s = period2s
        self.thresh_chop = thresh_chop
        self.thresh_rs_enter = thresh_rs_enter
        self.thresh_rs_exit = thresh_rs_exit
        self.thresh_rb_exit = thresh_rb_exit
        self.use_safe = use_safe
        self.offset_chop = offset_chop
        self.close_trend = close_trend

    def add_rsi(self, df, kind_rsi, period_rsi, rename):
        if kind_rsi == 'velcro':
            df['max_hb'] = df['high'].rolling(period_rsi).max()
            df['min_hb'] = df['low'].rolling(period_rsi).min()
            df = add_velcro_indicator(df,period_rsi)
            df = df.rename({'velcro': rename}, axis=1)
        elif kind_rsi == 'pedal':
            df = add_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'pedal': rename}, axis=1)
        elif kind_rsi == 'wpedal':
            df = add_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'wpedal': rename}, axis=1)
        elif kind_rsi == 'real_pedal':
            df = add_real_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'real_pedal': rename}, axis=1)
        elif kind_rsi == 'real_wpedal':
            df = add_real_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'real_wpedal': rename}, axis=1)
        elif kind_rsi == 'mfi':
            df = add_mfi(df, period_rsi)
            df = df.rename({'mfi': rename}, axis=1)
        elif kind_rsi == 's':
            df = add_stochastic(df, period_rsi, self.period2s)
            df = df.rename({'%d': rename}, axis=1)
        elif kind_rsi == 'uo':
            df = add_ultimate_oscillator(df, period_rsi // 3, period_rsi // 2, period_rsi)
            df = df.rename({'ultimate_oscillator': rename}, axis=1)
        else:
            df = add_rsi(df, period_rsi)
            df = df.rename({'rsi': rename}, axis=1)
        return df
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_bb(df, self.period_bkb,self.period_skb,self.mult_bkb,self.mult_skb)
        df = self.add_rsi(df,self.kind_rsi_big,self.period_rsi_big,'rsi_big')
        df = self.add_rsi(df,self.kind_rsi_small,self.period_rsi_small,'rsi_small')
        df = add_chop(df, self.period_chop)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # trend_context
        if row['chop'] < self.thresh_chop-self.offset_chop:
            if self.close_trend:
                if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_exit:
                    return 'close_long'
                if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_exit:
                    return 'close_short'
            # long_context
            if row["sma_small"] > row['sma_big']:
                if row['close'] <= row["sma_small"]:
                    return 'close_short'
            # short_context
            else:
                if row['close'] >= row["sma_small"]:
                    return 'close_long'
        # range_context
        elif row['chop'] >= self.thresh_chop+self.offset_chop:
            if row['close'] >= row['bbu_big']:
                if not self.use_safe:
                    return 'open_short'
            if row['close'] <= row['bbd_big']:
                if not self.use_safe:
                    return 'open_long'
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_enter:
                    return 'open_short' 
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_enter:
                    return 'open_long' 
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
        else:
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
            if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_exit:
                return 'close_long'
            if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_exit:
                return 'close_short'
            
class PEG11_SAYATAKAGI(BaseEG):
    """stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=50,thresh_chop=60,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_exit=40,use_safe=1,offset_chop=10
    \n
    kind_rsi in ["rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"]
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=50,thresh_chop=60,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_exit=40,use_safe=1,offset_chop=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bkb = period_bkb
        self.period_skb = period_skb
        self.mult_bkb = mult_bkb
        self.mult_skb = mult_skb
        self.period_rsi_big = period_rsi_big
        self.period_rsi_small = period_rsi_small
        self.period_chop = period_chop
        if kind_rsi_big == 'velcro' and self.period_rsi_big*2 > max_period:
            self.period_rsi_big = max_period // 2
        if kind_rsi_small == 'velcro' and self.period_rsi_small*2 > max_period:
            self.period_rsi_small = max_period // 2

        self.kind_rsi_big = kind_rsi_big
        self.kind_rsi_small = kind_rsi_small
        self.period2s = period2s
        self.thresh_chop = thresh_chop
        self.thresh_rs_enter = thresh_rs_enter
        self.thresh_rs_exit = thresh_rs_exit
        self.thresh_rb_exit = thresh_rb_exit
        self.use_safe = use_safe
        self.offset_chop = offset_chop

    def add_rsi(self, df, kind_rsi, period_rsi, rename):
        if kind_rsi == 'velcro':
            df['max_hb'] = df['high'].rolling(period_rsi).max()
            df['min_hb'] = df['low'].rolling(period_rsi).min()
            df = add_velcro_indicator(df,period_rsi)
            df = df.rename({'velcro': rename}, axis=1)
        elif kind_rsi == 'pedal':
            df = add_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'pedal': rename}, axis=1)
        elif kind_rsi == 'wpedal':
            df = add_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'wpedal': rename}, axis=1)
        elif kind_rsi == 'real_pedal':
            df = add_real_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'real_pedal': rename}, axis=1)
        elif kind_rsi == 'real_wpedal':
            df = add_real_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'real_wpedal': rename}, axis=1)
        elif kind_rsi == 'mfi':
            df = add_mfi(df, period_rsi)
            df = df.rename({'mfi': rename}, axis=1)
        elif kind_rsi == 's':
            df = add_stochastic(df, period_rsi, self.period2s)
            df = df.rename({'%d': rename}, axis=1)
        elif kind_rsi == 'uo':
            df = add_ultimate_oscillator(df, period_rsi // 3, period_rsi // 2, period_rsi)
            df = df.rename({'ultimate_oscillator': rename}, axis=1)
        else:
            df = add_rsi(df, period_rsi)
            df = df.rename({'rsi': rename}, axis=1)
        return df
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_bb(df, self.period_bkb,self.period_skb,self.mult_bkb,self.mult_skb)
        df = self.add_rsi(df,self.kind_rsi_big,self.period_rsi_big,'rsi_big')
        df = self.add_rsi(df,self.kind_rsi_small,self.period_rsi_small,'rsi_small')
        df = add_chop(df, self.period_chop)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # trend_context
        if row['chop'] < self.thresh_chop-self.offset_chop:
            # long_context
            if row['close'] >= row["bbu_small"] and row['rsi_small'] < 100 - self.thresh_rs_enter:
                return 'open_long'
            # short_context
            if row['close'] <= row["bbd_small"] and row['rsi_small'] > self.thresh_rs_enter:
                return 'open_short'
            
        # range_context
        elif row['chop'] >= self.thresh_chop+self.offset_chop:
            if row['close'] >= row['bbu_big']:
                if not self.use_safe:
                    return 'open_short'
            if row['close'] <= row['bbd_big']:
                if not self.use_safe:
                    return 'open_long'
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_enter:
                    return 'open_short' 
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_enter:
                    return 'open_long' 
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
        else:
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
            if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_exit:
                return 'close_long'
            if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_exit:
                return 'close_short'
            
class PEG11_ALICEMARASATO(BaseEG):
    """stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=50,thresh_chop=60,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_exit=40,use_safe=1,offset_chop=10,go_on_trend=0
    \n
    kind_rsi in ["rsi","mfi","s","uo","velcro","pedal","wpedal","real_pedal", "real_wpedal"]
    """
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_bkb=55, period_skb=10, mult_bkb=3,mult_skb=1.5, period_rsi_big=10, period_rsi_small=20, kind_rsi_big='rsi',kind_rsi_small='rsi',period2s=3,max_period=70,period_chop=50,thresh_chop=60,thresh_rs_enter=30,thresh_rs_exit=40,thresh_rb_exit=40,use_safe=1,offset_chop=10,go_on_trend=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_bkb = period_bkb
        self.period_skb = period_skb
        self.mult_bkb = mult_bkb
        self.mult_skb = mult_skb
        self.period_rsi_big = period_rsi_big
        self.period_rsi_small = period_rsi_small
        self.period_chop = period_chop
        if kind_rsi_big == 'velcro' and self.period_rsi_big*2 > max_period:
            self.period_rsi_big = max_period // 2
        if kind_rsi_small == 'velcro' and self.period_rsi_small*2 > max_period:
            self.period_rsi_small = max_period // 2

        self.kind_rsi_big = kind_rsi_big
        self.kind_rsi_small = kind_rsi_small
        self.period2s = period2s
        self.thresh_chop = thresh_chop
        self.thresh_rs_enter = thresh_rs_enter
        self.thresh_rs_exit = thresh_rs_exit
        self.thresh_rb_exit = thresh_rb_exit
        self.use_safe = use_safe
        self.offset_chop = offset_chop
        self.go_on_trend = go_on_trend

    def add_rsi(self, df, kind_rsi, period_rsi, rename):
        if kind_rsi == 'velcro':
            df['max_hb'] = df['high'].rolling(period_rsi).max()
            df['min_hb'] = df['low'].rolling(period_rsi).min()
            df = add_velcro_indicator(df,period_rsi)
            df = df.rename({'velcro': rename}, axis=1)
        elif kind_rsi == 'pedal':
            df = add_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'pedal': rename}, axis=1)
        elif kind_rsi == 'wpedal':
            df = add_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'wpedal': rename}, axis=1)
        elif kind_rsi == 'real_pedal':
            df = add_real_perdirlong(df,period_rsi,use_v=False)
            df = df.rename({'real_pedal': rename}, axis=1)
        elif kind_rsi == 'real_wpedal':
            df = add_real_perdirlong(df,period_rsi,use_s=False)
            df = df.rename({'real_wpedal': rename}, axis=1)
        elif kind_rsi == 'mfi':
            df = add_mfi(df, period_rsi)
            df = df.rename({'mfi': rename}, axis=1)
        elif kind_rsi == 's':
            df = add_stochastic(df, period_rsi, self.period2s)
            df = df.rename({'%d': rename}, axis=1)
        elif kind_rsi == 'uo':
            df = add_ultimate_oscillator(df, period_rsi // 3, period_rsi // 2, period_rsi)
            df = df.rename({'ultimate_oscillator': rename}, axis=1)
        else:
            df = add_rsi(df, period_rsi)
            df = df.rename({'rsi': rename}, axis=1)
        return df
    
    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_kusuruken_bb(df, self.period_bkb,self.period_skb,self.mult_bkb,self.mult_skb)
        df = self.add_rsi(df,self.kind_rsi_big,self.period_rsi_big,'rsi_big')
        df = self.add_rsi(df,self.kind_rsi_small,self.period_rsi_small,'rsi_small')
        df = add_chop(df, self.period_chop)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        # trend_context
        if row['chop'] < self.thresh_chop-self.offset_chop:
            # long_context
            if row['close'] >= row["bbu_small"] and row['rsi_small'] < 100 - self.thresh_rs_enter:
                if not self.go_on_trend and row["bbu_small"] < row['sma_big']:
                    return 'open_long'
                if self.go_on_trend and row["bbu_small"] > row['sma_big']:
                    return 'open_long'
            # short_context
            if row['close'] <= row["bbd_small"] and row['rsi_small'] > self.thresh_rs_enter:
                if not self.go_on_trend and row["bbd_small"] > row['sma_big']:
                    return 'open_short'
                if self.go_on_trend and row["bbd_small"] < row['sma_big']:
                    return 'open_short'
        # range_context
        elif row['chop'] >= self.thresh_chop+self.offset_chop:
            if row['close'] >= row['bbu_big']:
                if not self.use_safe:
                    return 'open_short'
            if row['close'] <= row['bbd_big']:
                if not self.use_safe:
                    return 'open_long'
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_enter:
                    return 'open_short' 
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_enter:
                    return 'open_long' 
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
        else:
            if row['close'] >= row['bbu_small']:
                if row['rsi_small'] >= 100 - self.thresh_rs_exit:
                    return 'close_long' 
            if row['close'] <= row['bbd_small']:
                if row['rsi_small'] <= self.thresh_rs_exit:
                    return 'close_short'
            if row['close'] >= row['bbu_big'] and row['rsi_big'] >= 100 - self.thresh_rb_exit:
                return 'close_long'
            if row['close'] <= row['bbd_big'] and row['rsi_big'] <= self.thresh_rb_exit:
                return 'close_short'
            


class PEG13_DWDDCr(BaseEG):
    """stop=None, take=None, period=60, threshold=30, period2=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, threshold=30, period2=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        df = add_awesome_oscillator(df, long_period=self.period)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold:
            if row['ao'] > 0:
                return 'open_long'
            else:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long and row['rsi'] > 100 - self.threshold:
            if row['ao'] < 0:
                return 'open_short'
            else:
                return 'close_long'

# 12.10.2026 надо соединить с GRAVY2, а то не подстраивается под волатильность немного. 
# 19.10.2026 почему-то не закрыл +1.5% сделку и тупо ждал отката.
class PEG13_DUNE(BaseEG):
    """stop=None, take=None, period_dc=55, period_ao=20,period_rsi=20,period_q=20,quantile=0.2,max_period=70,period_ao_roll=20,offset_range=0.1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_dc=55, period_ao=20,period_rsi=20,period_q=20,quantile=0.2,max_period=70,period_ao_roll=20,offset_range=0.1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_dc = period_dc
        self.period_rsi,self.period_q = fix_two_periods_hm(period_rsi,period_q,max_period)
        self.quantile = quantile
        self.period_ao,self.period_ao_roll = fix_two_periods_hm(period_ao,period_ao_roll,max_period)
        self.offset_range = offset_range

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_awesome_oscillator(df, long_period=self.period_ao)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df,self.period_q,'rsi',self.quantile)
        ao_roll = df['ao'].rolling(self.period_ao_roll)
        df['top_range'] = ao_roll.quantile(0.5+self.offset_range)
        df['bottom_range'] = ao_roll.quantile(0.5-self.offset_range)
        df['nl'] = df['high'] - df['close'] > df['close'] - df['low']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['ao'] > row['top_range']: #long
            if row['low'] <= row['min_hb'] and row['nl'] and row['rsi'] < row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not row['nl'] and row['rsi'] > row['top_q']:
                return 'close_long'
        elif row['ao'] < row['bottom_range']:
            if row['low'] <= row['min_hb'] and row['nl'] and row['rsi'] < row['bottom_q']:
                return 'close_short'
            if row['high'] >= row['max_hb'] and not row['nl'] and row['rsi'] > row['top_q']:
                return 'open_short'
        else:
            if row['low'] <= row['min_hb'] and row['nl'] and row['rsi'] < row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not row['nl'] and row['rsi'] > row['top_q']:
                return 'open_short'

        

class PEG14_RWDDCr(BaseEG):
    """stop=None, take=None, period=20, threshold=30, period2=10, period3=20,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30, period2=10, period3=20,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        can_period = max_period // 3
        self.period3 = min(can_period,period3)
        max_total = can_period * 2
        total = self.period3 + period2

        if total > max_total:
            ratio = max_total / total
            self.period3 = int(self.period3 * ratio)
            self.period2 = int(period2 * ratio)
        else:
            self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = add_chop(df, self.period3)
        df['sma'] = df['chop'].rolling(window=self.period3).mean()
        df['sma2'] = df['chop'].rolling(window=self.period2).mean()
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['sma'] > row['sma2']:
            return 'close_all'
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not nearest_long and row['rsi'] > 100 - self.threshold:
                return 'open_short'
            
class PEG14_REGAL(BaseEG):
    """stop=None, take=None, period_dc=20, period_rsi=20, threshold=30, period_chop=30, period_sc1=10,period_sc2=20,max_period=70"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_dc=20, period_rsi=20, threshold=30, period_chop=30, period_sc1=10,period_sc2=20,max_period=70):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_dc = period_dc
        self.period_rsi = period_rsi
        self.threshold = threshold
        self.period_chop,self.period_sc1,self.period_sc2 = fix_three_periods_hm(period_chop,period_sc1,period_sc2,max_period)
        if self.period_sc1 == self.period_sc2:
            self.period_sc2 -= 1

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_rsi(df, self.period_rsi)
        df = add_chop(df, self.period_chop)
        df['sma_chop1'] = df['chop'].rolling(window=self.period_sc1).mean()
        df['sma_chop2'] = df['chop'].rolling(window=self.period_sc2).mean()
        df['nl'] = df['high'] - df['close'] > df['close'] - df['low']
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        if row['sma_chop1'] > row['sma_chop2']:
            if row['low'] <= row['min_hb'] and row['nl']:
                return 'close_short'
            if row['high'] >= row['max_hb'] and not row['nl']:
                return 'close_long'
        else:            
            if row['low'] <= row['min_hb'] and row['nl'] and row['rsi'] < self.threshold:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not row['nl'] and row['rsi'] > 100 - self.threshold:
                return 'open_short'
        


class PEG14_RANGER(BaseEG):
    """stop=None, take=None, period_adx=55, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=55, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_adx = period_adx
        self.threshold_rsi = threshold_rsi
        self.threshold_chop = threshold_chop
        self.threshold_adx = threshold_adx
        self.period2 = period2
        self.period3 = period3

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period3)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period2)
        df = add_adx(df, self.period_adx)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        ranger = row['chop'] > self.threshold_chop and row['adx'] < self.threshold_adx
        if not ranger:
            return 'close_all'
        else:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold_rsi:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold_rsi:
                return 'open_short'
            
        
#     'ROSN2':(PEG14_RENEGADE,(None,None,16,38,52,6,49,30),1,None), опять странные закртия
class PEG14_RENEGADE(BaseEG):
    """stop=None, take=None, period_adx=27, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_adx=27, threshold_rsi=30, period2=55, period3=20, threshold_chop=50, threshold_adx=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}

        self.period_adx = period_adx
        self.threshold_rsi = threshold_rsi
        self.threshold_chop = threshold_chop
        self.threshold_adx = threshold_adx
        self.period2 = period2
        self.period3 = period3

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period3)
        df = add_rsi(df, self.period3)
        df = add_chop(df, self.period2)
        df = add_adx(df, self.period_adx)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        ranger = row['chop'] > self.threshold_chop and row['adx'] < self.threshold_adx
        if ranger:
            nearest_long = row['high'] - row['close'] > row['close'] - row['low']
            
            if row['low'] <= row['min_hb'] and nearest_long and row['rsi'] < self.threshold_rsi:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] > 100 - self.threshold_rsi:
                return 'open_short'
        
        return None

class PEG15_ANNA(BaseEG):
    """stop=None, take=None, period=20, threshold=30"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df, self.period)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if not np.isnan(row['end_down']):
            if nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            else:
                return 'close_short'
        
        if not np.isnan(row['end_up']):
            if not nearest_long and row['rsi'] > 100 - self.threshold:
                return 'open_short'
            else:
                return 'close_long'
        
        return None

class PEG15_SILVANA(BaseEG):
    """stop=None, take=None, period=20, threshold=30, period2=20"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=20, threshold=30, period2=20):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.threshold = threshold
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df = add_rsi(df, self.period2)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if not np.isnan(row['end_down']):
            if nearest_long and row['rsi'] < self.threshold:
                return 'open_long'
            else:
                return 'close_short'
        
        if not np.isnan(row['end_up']):
            if not nearest_long and row['rsi'] > 100 - self.threshold:
                return 'open_short'
            else:
                return 'close_long'
        
        if row['low'] < row['min_hb']:
            return 'close_long'
        if row['high'] > row['max_hb']:
            return 'close_short'
        



#Долгий, но использовать можно
# TODO решить проблему с индикаторами. Заглядывают слишком сильнов историю
# 02.10.2026, что если поробоать из него сделать ходячий оптимизатор? Каждое окно он будет оптимизацией выбирать из нескольких стратегий и выбирать лучший результат?
class PEG16_LEORIC(BaseEG):
    """stop=None, take=None, period=30, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=50, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'DCr', self.period)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'avarege')
        df = add_benefit(df, all_starts, all_ends, 'DCmaxa', self.period)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'avarege', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'DCmina', self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata

    def get_bests(self, row):
        target_indices_long = ['bl_DCr', 'bl_DCmaxa', 'bl_DCmina']
        target_indices_short = ['bs_DCr', 'bs_DCmaxa', 'bs_DCmina']
        filtered_l = row[target_indices_long]
        filtered_s = row[target_indices_short]
        best_l = filtered_l.idxmax()
        best_s = filtered_s.idxmax()
        if best_l == 'bl_DCr':
            kind_l = 'min_hb'
            kind_cl = 'max_hb'
        if best_l == 'bl_DCmaxa':
            kind_l = 'avarege'
            kind_cl = 'max_hb'
        if best_l == 'bl_DCmina':
            kind_l = 'min_hb'
            kind_cl = 'avarege'
        if best_s == 'bs_DCr':
            kind_s = 'max_hb'
            kind_cs = 'min_hb'
        if best_s == 'bs_DCmaxa':
            kind_s = 'max_hb'
            kind_cs = 'avarege'
        if best_s == 'bs_DCmina':
            kind_s = 'avarege'
            kind_cs = 'min_hb'
        return best_l, best_s, kind_l, kind_s, kind_cl, kind_cs

    def _get_action_from_row(self, row):
        best_l, best_s, kind_l, kind_s, kind_cl, kind_cs = self.get_bests(row)
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row[best_l] > 0 and row['low'] <= row[kind_l] and nearest_long:
            return 'open_long'
        
        if row[best_s] > 0 and not nearest_long and row['high'] >= row[kind_s]:
            return 'open_short'
        
        if row['low'] <= row[kind_cs] and not nearest_long:
            return 'close_short'
        
        if row['high'] >= row[kind_cl] and nearest_long:
            return 'close_long'
        
        return None

#Быстрый товарищ
# TODO решить проблему с индикаторами. Заглядывают слишком сильнов историю
class PEG16_CHEN(BaseEG):
    """stop=None, take=None, period=30, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=30, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        all_starts, all_ends = get_all_enter_exit_DC(df, 'max_hb', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'DCr', self.period)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        best_l = 'bl_DCr'
        best_s = 'bs_DCr'
        kind_l = 'min_hb'
        kind_s = 'max_hb'
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row[best_l] > 0 and row['low'] <= row[kind_l] and nearest_long:
            return 'open_long'
        
        if row[best_s] > 0 and not nearest_long and row['high'] >= row[kind_s]:
            return 'open_short'
        
        if row['low'] <= row[kind_l] and nearest_long:
            return 'close_short'
        
        if row['high'] >= row[kind_s] and not nearest_long:
            return 'close_long'
        
        if row[best_l] < 0:
            return 'close_long'
        
        if row[best_s] < 0:
            return 'close_short'
        
        return None
        
#Быстрый товарищ     
# TODO решить проблему с индикаторами. Заглядывают слишком сильнов историю
class PEG16_ARTANIS(BaseEG):
    """stop=None, take=None, period=30, period2=10"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=30, period2=10):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.period2 = period2

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df['max_hb'] = df['high'].rolling(self.period).max()
        df['min_hb'] = df['low'].rolling(self.period).min()
        all_starts, all_ends = get_all_lup(df, 'max_hb', 'min_hb')
        df = add_benefit(df, all_starts, all_ends, 'EDCr', self.period)
        df['max_hb'] = df['max_hb'].shift(1)
        df['min_hb'] = df['min_hb'].shift(1)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df, period=self.period)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        best_l = 'bl_EDCr'
        best_s = 'bs_EDCr'
        
        if not np.isnan(row['end_up']):
            if row[best_s] > 0:
                return 'open_short'
            else:
                return 'close_long'
        
        if not np.isnan(row['end_down']):
            if row[best_l] > 0:
                return 'open_long'
            else:
                return 'close_short'
        
        if row[best_l] < 0:
            return 'close_long'
        
        if row[best_s] < 0:
            return 'close_short'
        
        return None

# Возможно нужна вариация с более простым выходом
# 30.09.26 мне не нравится моменты со входами в хаях. Надо подумать над вариацией без этого. Скорее всего дело в работе по тренду. У нас там он смотри на low, а надо на close хотя бы
# 05.10.2026 сделать версию с входом по low
# 07.10.2026 при малом периоде велкро может творить жесть. Открыл в хаях, закрыл в лоях 'T2':(PEG17_PHOENIX,(None,None,18,23,33,2,15,0,60),1,None),
# 11.10.2026 нажна версия с только закрытием в тренде
# 14.10.2026 ну вход с середины в тренде - это явно не лучшая фишка феникса. Порой заходит прям на дне
# 19.10.2026 V-образный разворо == смерть
# 19.10.2026 надо добавить nearest_long!!!
class PEG17_PHOENIX(BaseEG):
    """stop=None, take=None, period=100, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, use_stop=0, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, use_stop=0, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.use_stop = use_stop
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)
        self.period_quantile,self.period_rsi = fix_two_periods_hm(period_quantile,period_rsi,max_period)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df, self.period_quantile)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    # Изучи этот. Тут есть странные подозрения
    def _get_action_from_row(self, row):
        if row['velcro'] > 100 - self.threshold_velcro:  # long
            if row['low'] <= row["avarege"]:
                return 'open_long'
            else:
                if self.use_stop:
                    return 'close_short'

        elif row['velcro'] < self.threshold_velcro:  # short
            if row['high'] >= row["avarege"]:
                return 'open_short'
            else:
                if self.use_stop:
                    return 'close_long'
        else:  # range
            if row['low'] <= row['min_hb'] and row['rsi'] <= row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] >= row['top_q']:
                return 'open_short'
            
class PEG17_PROBIUS(BaseEG):
    """stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55,thersh_rsi_trend=15"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55,thersh_rsi_trend=15):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.thersh_rsi_trend = thersh_rsi_trend
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)
        self.period_quantile,self.period_rsi = fix_two_periods_hm(period_quantile,period_rsi,max_period)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df, self.period_quantile)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    def _get_action_from_row(self, row):
        if row['velcro'] > 100 - self.threshold_velcro:  # long
            if row['high'] >= row['max_hb'] and row['rsi'] >= 100-self.thersh_rsi_trend:
                return 'open_short'

        elif row['velcro'] < self.threshold_velcro:  # short
            if row['low'] <= row['min_hb'] and row['rsi'] <= self.thersh_rsi_trend:
                return 'open_long'
        else:  # range
            if row['low'] <= row['min_hb'] and row['rsi'] <= row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] >= row['top_q']:
                return 'open_short'

# 12.10.2026 надо сделать версию с закрытием вне боковика
# 19.10.2026 в v-образном кроется слишком рано
class PEG17_ZEALOT(BaseEG):
    """stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)
        self.period_quantile,self.period_rsi = fix_two_periods_hm(period_quantile,period_rsi,max_period)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df, self.period_quantile)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    def _get_action_from_row(self, row):
        if self.threshold_velcro < row['velcro'] < 100 - self.threshold_velcro:  # long
            if row['low'] <= row['min_hb'] and row['rsi'] <= row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] >= row['top_q']:
                return 'open_short'

# 05.10.2026 пока большые вопросы. Кажется одного велкро для входа не достаочно. Может зайти и в локальном хае   
class PEG17_TEMPLAR(BaseEG):
    """stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)
        self.period_quantile,self.period_rsi = fix_two_periods_hm(period_quantile,period_rsi,max_period)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df, self.period_quantile)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    def _get_action_from_row(self, row):
        if row['velcro'] > 100 - self.threshold_velcro:  # long
            return 'open_short'

        elif row['velcro'] < self.threshold_velcro:  # short
            return 'open_long'
        else:  # range
            if row['low'] <= row['min_hb'] and row['rsi'] <= row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] >= row['top_q']:
                return 'open_short'
            
class PEG17_ARCHON(BaseEG):
    """stop=None, take=None,  period_dc=20, period_velcro=50, threshold_velcro=30, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,  period_dc=20, period_velcro=50, threshold_velcro=30, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    def _get_action_from_row(self, row):
        if row['velcro'] > 100 - self.threshold_velcro:  # long
            return 'open_short'
        if row['velcro'] < self.threshold_velcro:  # short
            return 'open_long'

# 05.10.2026 надо подумать над трендовой частью. Из-за нее порой открывает странные сделки в хаях
class PEG17_SELENDIS(BaseEG):
    """stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_quantile=55, period_dc=20, period_rsi=20, period_velcro=50, threshold_velcro=30, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_velcro = threshold_velcro
        self.period_dc,self.period_velcro = fix_two_periods_hm(period_dc,period_velcro,max_period)
        self.period_quantile,self.period_rsi = fix_two_periods_hm(period_quantile,period_rsi,max_period)

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_velcro_indicator(df, self.period_velcro)
        df = add_rsi(df, self.period_rsi)
        df = add_quantile_params(df, self.period_quantile)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['high'] < df['max_hb']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['low'] > df['min_hb']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        if row['velcro'] > 100 - self.threshold_velcro:  # long
            if not np.isnan(row['end_down']):
                if nearest_long:
                    return 'open_long'
        elif row['velcro'] < self.threshold_velcro:  # short
            if not np.isnan(row['end_up']):
                if not nearest_long:
                    return 'open_short'
        else:  # range
            if row['low'] <= row['min_hb'] and row['rsi'] <= row['bottom_q']:
                return 'open_long'
            if row['high'] >= row['max_hb'] and row['rsi'] >= row['top_q']:
                return 'open_short'

class PEG18_REXXAR2(BaseEG):
    """stop=None, take=None, period=10, mult_st=3, period_st=10, threshold_enter=40, threshold_exit=20, use_stop=0,max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, mult_st=1.5, period_st=55, threshold_enter=40, threshold_exit=20, use_stop=0,max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.mult_st = mult_st
        self.period_st = fix_supertrend_params(period_st,mult_st,max_period)
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        # df = add_pc_stair_fast(df, self.n_stairs, self.period2)
        df = add_supertrend(df,self.period_st,self.mult_st)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['in_uptrend']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        
        if row['high'] >= row['max_hb']:
            if not nearest_long:
                if not can_long and row['rsi'] > 100 - self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
        
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'

class PEG18_UTER(BaseEG):
    """stop=None, take=None, period=55, n_stairs=3, period2=10, threshold=30, threshold_adx=40, period_adx=30, use_stop=0"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold=30, threshold_adx=40, period_adx=30, use_stop=0):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.period_adx = period_adx
        self.threshold_adx = threshold_adx
        self.threshold = threshold
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_pc_stair_fast(df, self.n_stairs, self.period)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_adx(df, self.period_adx)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['adx'] > self.threshold_adx:
            can_long = row['close'] > row['stair']
            
            if row['low'] <= row['min_hb'] and nearest_long:
                if can_long:
                    return 'open_long'
                if row['rsi'] < self.threshold:
                    return 'close_short'
            
            if row['high'] >= row['max_hb'] and not nearest_long:
                if not can_long:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold:
                    return 'close_long'
            
            if self.use_stop:
                if can_long:
                    return 'close_short'
                else:
                    return 'close_long'
        else:
            if row['low'] <= row['min_hb'] and nearest_long:
                return 'open_long'
            if row['high'] >= row['max_hb'] and not nearest_long:
                return 'open_short'
        
        return None
    
class PEG18_UTER2(BaseEG):
    """stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold_enter=30, threshold_exit=40, threshold_adx=40, period_adx=30, use_stop=0, max_period=55, wddcr_trend=1, wddcr_flat=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold_enter=30, threshold_exit=40, threshold_adx=40, period_adx=30, use_stop=0, max_period=55, wddcr_trend=1, wddcr_flat=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.mult_st = mult_st
        self.period_st = fix_supertrend_params(period_st,mult_st,max_period)
        self.period2 = period2
        self.period_adx = period_adx
        self.threshold_adx = threshold_adx
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        self.wddcr_trend = wddcr_trend
        self.wddcr_flat = wddcr_flat
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        # df = add_pc_stair_fast(df, self.n_stairs, self.period)
        df = add_supertrend(df,self.period_st,self.mult_st)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_adx(df, self.period_adx)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        if row['adx'] > self.threshold_adx:
            can_long = row['in_uptrend']
            
            if row['low'] <= row['min_hb'] and nearest_long:
                long_cond = row['rsi'] < self.threshold_enter if self.wddcr_trend else True
                if can_long and long_cond:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
            
            if row['high'] >= row['max_hb'] and not nearest_long:
                short_cond = row['rsi'] > 100 - self.threshold_exit if self.wddcr_trend else True
                if not can_long and short_cond:
                    return 'open_short'
                if row['rsi'] > 100 - self.threshold_exit:
                    return 'close_long'
            
            if self.use_stop:
                if can_long:
                    return 'close_short'
                else:
                    return 'close_long'
        else:
            long_cond = row['rsi'] < self.threshold_enter if self.wddcr_flat else True
            if row['low'] <= row['min_hb'] and nearest_long and long_cond:
                return 'open_long'
            short_cond = row['rsi'] > 100 - self.threshold_exit if self.wddcr_flat else True
            if row['high'] >= row['max_hb'] and not nearest_long and short_cond:
                return 'open_short'
        
        return None

class PEG18_DIABLO2(BaseEG):
    """stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold=30,use_stop=0, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold=30,use_stop=0, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.mult_st = mult_st
        self.period_st = fix_supertrend_params(period_st,mult_st,max_period)
        self.period2 = period2
        self.threshold = threshold
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_supertrend(df,self.period_st,self.mult_st)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['in_uptrend']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['close'] <= row['avarege'] and nearest_long and can_long:
            return 'open_long'
        
        if row['close'] >= row['avarege'] and not nearest_long and not can_long:
            return 'open_short'
        
        if row['rsi'] < self.threshold and row['low'] <= row['min_hb']:
            return 'close_short'
        
        if row['rsi'] > 100 - self.threshold and row['high'] >= row['max_hb']:
            return 'close_long'
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'
        
class PEG18_VARIAN2(BaseEG):
    """stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold=30, threshold_ii=25, period_ii=10, use_stop=0, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold=30, threshold_ii=25, period_ii=10, use_stop=0, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.mult_st = mult_st
        self.period_st = fix_supertrend_params(period_st,mult_st,max_period)
        self.period2 = period2
        self.threshold = threshold
        self.threshold_ii = threshold_ii
        self.use_stop = use_stop
        self.period_ii = period_ii
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_supertrend(df,self.period_st,self.mult_st)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_integrity_index(df, self.period_ii)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['in_uptrend']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if nearest_long and can_long:
            if row['close'] <= row['avarege'] and row['ii'] > self.threshold_ii:
                return 'open_long'
            if row['low'] <= row['min_hb']:
                return 'open_long'
        
        if not nearest_long and not can_long:
            if row['close'] >= row['avarege'] and row['ii'] < -self.threshold_ii:
                return 'open_short'
            if row['high'] >= row['max_hb']:
                return 'open_short'
        
        if row['rsi'] < self.threshold and row['low'] <= row['min_hb']:
            return 'close_short'
        
        if row['rsi'] > 100 - self.threshold and row['high'] >= row['max_hb']:
            return 'close_long'
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'

# 'SIBN':(PEG18_ANDUIN,(None,None,2,1.7,28,24,5,19,0,55),1,None), заходит в хаях закрывает в лоях (иногда)
# плохо работает на разворотах тренда
# 05.10.2026 попробовать сделать без avarege
class PEG18_ANDUIN(BaseEG):
    """stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold=30, threshold_adx=30, period_adx=10, use_stop=0, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period_st=55, mult_st=3, period2=10, threshold=30, threshold_adx=30, period_adx=10, use_stop=0, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.mult_st = mult_st
        self.period_st = fix_supertrend_params(period_st,mult_st,max_period)
        self.period2 = period2
        self.threshold = threshold
        self.threshold_adx = threshold_adx
        self.use_stop = use_stop
        self.period_adx = period_adx
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_supertrend(df,self.period_st,self.mult_st)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = add_adx(df, self.period_adx)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['in_uptrend']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if nearest_long and can_long:
            if row['close'] <= row['avarege'] and row['adx'] > self.threshold_adx:
                return 'open_long'
            if row['low'] <= row['min_hb']:
                return 'open_long'
        
        if not nearest_long and not can_long:
            if row['close'] >= row['avarege'] and row['adx'] > self.threshold_adx:
                return 'open_short'
            if row['high'] >= row['max_hb']:
                return 'open_short'
        
        if row['rsi'] < self.threshold and row['low'] <= row['min_hb']:
            return 'close_short'
        
        if row['rsi'] > 100 - self.threshold and row['high'] >= row['max_hb']:
            return 'close_long'
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'
            
# скорее всего его выносит смена тенденции
class PEG18_BLAZE(BaseEG):
    """stop=None, take=None, period=75, period2=75, period3=75, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=75, period2=75, period3=75, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        self.period,self.period2 = fix_two_periods_hm(period,period2,max_period)
        self.period,self.period2,self.period3 = fix_three_periods_hm(period,period2,period3,max_period)
        if self.period < self.period3:
            self.period3 = self.period

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period2)
        df = add_assessment_motion_index(df, self.period, self.period3)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['ami'] > row['ami_filter']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if not can_long and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if can_long:
                return 'close_short'
            else:
                return 'close_long'
        
        return None

    # 'IRAO':(PEG19_ANUBARAK,(None,None,17,3,11,39,43,91,0,55),1,None), тоже самое закрывает сделки в хаях плохие
class PEG19_ANUBARAK(BaseEG):
    """stop=None, take=None,period_ami1=10,period_dc=10,period_rsi=10,threshold_enter=30,threshold_exit=40,threshold_ami=50,use_stop=0, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None,period_ami1=10,period_dc=10,period_rsi=10,threshold_enter=30,threshold_exit=40,threshold_ami=50,use_stop=0, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period_dc, self.period_ami1 = fix_two_periods_hm(period_dc,period_ami1,max_period)
        self.period_rsi = period_rsi
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.threshold_ami = threshold_ami
        self.use_stop = use_stop

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_donchan_channel(df, self.period_dc)
        df = add_assessment_motion_index(df, self.period_ami1, self.period_ami1)
        df = add_rsi(df, self.period_rsi)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata

    def _get_action_from_row(self, row):
        can_long = row['ami'] > -self.threshold_ami
        can_short = row['ami'] < self.threshold_ami
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        if row['high'] >= row['max_hb'] and not nearest_long:
            if can_short and row['rsi'] > 100-self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100-self.threshold_exit:
                return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'        

class PEG19_YREL(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_hope_channel(df, self.n_stairs, self.period2, self.shift)
        df = add_donchan_channel(df, self.period2)
        df = add_rsi(df, self.period2)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_VALEERA(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=10, threshold_enter=40, threshold_exit=20, shift=10, use_stop=1):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.period2 = period2
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.shift = shift
        self.use_stop = use_stop
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_hope_channel(df, self.n_stairs, self.period, self.shift)
        df = add_donchan_channel(df, self.period2)
        df = add_vangerchik(df)
        df = add_rsi(df, self.period2)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['close'] < df['max_vg']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['close'] > df['min_vg']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        
        if not np.isnan(row['end_up']):
            if not can_long:
                return 'open_short'
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if not np.isnan(row['end_down']):
            if not can_short:
                return 'open_long'
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_ZERATUL(BaseEG):
    """stop=None, take=None, period=55, n_stairs=3, period2=55, period3=55, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=55, n_stairs=3, period2=55, period3=55, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_vangerchik(df)
        df = add_rsi(df, self.period)
        df['end_up'] = np.where((df['high'].shift(1) >= df['max_hb'].shift(1)) & (df['close'] < df['max_vg']), df['high'], np.nan)
        df['end_down'] = np.where((df['low'].shift(1) <= df['min_hb'].shift(1)) & (df['close'] > df['min_vg']), df['low'], np.nan)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        
        if not np.isnan(row['end_up']):
            if not can_long:
                return 'open_short'
            if can_short and row['rsi'] > 100 - self.threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - self.threshold_exit:
                return 'close_long'
        
        if not np.isnan(row['end_down']):
            if not can_short:
                return 'open_long'
            if can_long and row['rsi'] < self.threshold_enter:
                return 'open_long'
            if row['rsi'] < self.threshold_exit:
                return 'close_short'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_JOHANNA(BaseEG):
    """stop=None, take=None, period=10,n_stairs=3,period2=10,period3=20,threshold_enter=40,threshold_exit=20,use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10,n_stairs=3,period2=10,period3=20,threshold_enter=40,threshold_exit=20,use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low'] 
        if row['low'] <= row['min_hb']:
            if nearest_long:
                if can_long and row['rsi'] < self.threshold_enter:
                    return 'open_long'
                if row['rsi'] < self.threshold_exit:
                    return 'close_short'
        if row['high'] >= row['max_hb']:
            if not nearest_long :
                if can_short and row['rsi'] > 100-self.threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100-self.threshold_exit:
                    return 'close_long'
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'

class PEG19_CASSIA(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.threshold_middle = (threshold_enter + threshold_exit) // 2
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        threshold_enter = self.threshold_middle if can_long and can_short else self.threshold_enter
        threshold_exit = self.threshold_middle if can_long and can_short else self.threshold_exit
        
        if row['low'] <= row['min_hb'] and nearest_long:
            if can_long and row['rsi'] < threshold_enter:
                return 'open_long'
            if row['rsi'] < threshold_exit:
                return 'close_short'
        
        if row['high'] >= row['max_hb'] and not nearest_long:
            if can_short and row['rsi'] > 100 - threshold_enter:
                return 'open_short'
            if row['rsi'] > 100 - threshold_exit:
                return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None

class PEG19_IMPERIUS(BaseEG):
    """stop=None, take=None, period=100, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55"""
    def __init__(self, symbol='Test', price_step=None, mult_ps=1, mode=None, stop=None, take=None, period=10, n_stairs=3, period2=10, period3=20, threshold_enter=40, threshold_exit=20, use_stop=1, max_period=55):
        super().__init__(symbol, price_step, mult_ps, mode, stop, take)
        self.needs_info = {'chart': self.symbol}
        self.period = period
        self.n_stairs = n_stairs
        self.threshold_enter = threshold_enter
        self.threshold_exit = threshold_exit
        self.threshold_middle = (threshold_enter + threshold_exit) // 2
        self.use_stop = use_stop
        max_total = (max_period // 3) * 2
        total = period2 + period3

        if total > max_total:
            ratio = max_total / total
            self.period2 = int(period2 * ratio)
            self.period3 = int(period3 * ratio)
        else:
            self.period2 = period2
            self.period3 = period3
        self.problems = 'Mcfly'

    def preprocessing(self, tdata):
        pdata = {}
        df = tdata['chart']
        df = add_cascade_channel(df, self.n_stairs, self.period2, self.period3)
        df = add_donchan_channel(df, self.period)
        df = add_rsi(df, self.period)
        df = self.add_slice_df(df)
        pdata['chart'] = df
        return pdata
    
    def _get_action_from_row(self, row):
        can_long = row['close'] > row['bottom_line']
        can_short = row['close'] < row['top_line']
        nearest_long = row['high'] - row['close'] > row['close'] - row['low']
        
        threshold_enter = self.threshold_middle if can_long and can_short else self.threshold_enter
        threshold_exit = self.threshold_middle if can_long and can_short else self.threshold_exit
        
        if nearest_long:
            if can_long and not can_short and row['close'] <= row['avarege']:
                return 'open_long'
            if row['low'] <= row['min_hb']:
                if can_long and row['rsi'] < threshold_enter:
                    return 'open_long'
                if row['rsi'] < threshold_exit:
                    return 'close_short'
        
        if not nearest_long:
            if can_short and not can_long and row['close'] >= row['avarege']:
                return 'open_short'
            if row['high'] >= row['max_hb']:
                if can_short and row['rsi'] > 100 - threshold_enter:
                    return 'open_short'
                if row['rsi'] > 100 - threshold_exit:
                    return 'close_long'
        
        if self.use_stop:
            if not can_short:
                return 'close_short'
            if not can_long:
                return 'close_long'
        
        return None