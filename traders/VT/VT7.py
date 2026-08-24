import traceback
import os
import re
from datetime import datetime
import cv2
import pandas as pd
import numpy as np
import numpy.typing as npt
from datetime import datetime
from time import time
import pydirectinput as pdi
from traders.VT.settingsPB import ColorsBtnBGR,TemplateCandle,large_value_1_colors,large_value_2_colors
from strategies.BaseEG import BaseEG
from traders.VT.bot_on_ticker import init_trader
from for_strategies.help_dtypes.actions_cls import OrderCords
# from utils.drawing.chart import draw_bars_chart


class VT7:
    def __init__(
            self,
            conf_data:dict,
            symbols:list[str],
            close_on_time:bool=True,
            close_map:tuple=((22,30),(22,30),(22,30),(22,30),(22,30),(17,30),(17,30),)
            ):
        
        self.can_work = True
        self.symbols = symbols
        self.amount = conf_data['amount']
        if self.amount != len(symbols):
            self.can_work = False
            print('VT7 insufficient data',symbols)
            raise ValueError(f"VT7 insufficient data: {symbols}")
        
        self.glass_region = {symbol: [] for symbol in symbols}
        self.position_region = {symbol: [] for symbol in symbols}
        self.tape_region = {symbol: [] for symbol in symbols}
        self.cluster_region = {symbol: [] for symbol in symbols}

        self.fgs = {symbol: [] for symbol in symbols}

        for dom in conf_data['doms']:
            for i, symbol in enumerate(symbols):
                if i < len(dom['glasses']):
                    self.glass_region[symbol].append(dom['glasses'][i])
                    self.position_region[symbol].append(dom['poses'][i])
                    self.tape_region[symbol].append(dom['tapes'][i])
                    self.cluster_region[symbol].append(dom['clusters'][i])

                    self.fgs[symbol].append(None)
        
        # Распаковка charts
        self.chart_region = {symbol: [] for symbol in symbols}
        self.offset = {symbol: [] for symbol in symbols}
        self.candle_max = {symbol: [] for symbol in symbols}

        for chart in conf_data['charts']:
            for i, symbol in enumerate(symbols):
                if i < len(chart):
                    self.chart_region[symbol].append(chart[i])
                    self.offset[symbol].append(None)
                    self.candle_max[symbol].append(None)

        self.price_step = conf_data['price_step']
        self.wss: dict[str, BaseEG] = dict()
        for symbol in self.symbols:
            ws = init_trader(symbol)
            self.wss[symbol] = ws[0](symbol,self.price_step,ws[2],ws[3],*ws[1])
        now = datetime.now()
        cwd = now.weekday()
        self.close_on_time = close_on_time
        self.close_time = close_map[cwd]
        self.trader_name = 'VT7'
        folder_error = '_logs/error_logs_VT7'
        if not os.path.exists(folder_error):
            os.makedirs(folder_error)
        self.error_log = dict()
        for symbol in self.symbols:
            self.error_log[symbol] = os.path.join(folder_error,self.trader_name + '_' + symbol + '.txt')
        self.time_mode = None


    def _color_search(self,img:npt.ArrayLike,color:tuple[int],region:tuple[int]=(None,None,None,None),reverse:bool=False):
        try:
            roi = img[region[1]:region[3], region[0]:region[2]] #смотри не перепутай координаты региона 1 < 3 && 0 < 2, иначе будет пусть roi
            result = np.argwhere(
                (roi[:,:,0] == color[0]) & (roi[:,:,1] == color[1]) & (roi[:,:,2] == color[2])
            )

            if len(result) == 0:
                return -1, -1
            
            y = -1 if reverse else 0
            if region[0]:
                return result[y,1]+region[0], result[y,0]+region[1]
            return result[y,1],result[y,0]

        except Exception:
            traceback.print_exc()
            return -1,-1
             
    def _check_time(self):
        now = datetime.now()
        chour = now.hour
        cminute = now.minute
        if chour >= 7:
            if chour >= self.close_time[0] - 1:
                if cminute > self.close_time[1]:
                    if chour >= self.close_time[0]:
                        return -1
                    else:
                        return -2
                elif chour == self.close_time[0]:
                    return -2
                elif chour > self.close_time[0]:
                    return -1
            return 1
        return 0
    
    def _check_position(self,img,pos_region) -> int:
        x,y = self._color_search(img,ColorsBtnBGR.best_bid,pos_region)
        if x >= 0:
            return 1
        x,y = self._color_search(img,ColorsBtnBGR.best_ask,pos_region)
        if x >= 0:
            return -1
        return 0
    
    def _check_z_tape(self,img,symbol):
        for i in range(len(self.glass_region[symbol])):
            tape_region = self.tape_region[symbol][i]
            glass_region = self.glass_region[symbol][i]
            tape_img = self._get_region(img, region=tape_region).copy()
            mask = cv2.inRange(tape_img, ColorsBtnBGR.z_tape, ColorsBtnBGR.z_tape)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                # Фильтр по площади
                if area > 100:
                    pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
                    pdi.press('z')
                    break

    def _check_price_limit(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        x,y = self._color_search(img,ColorsBtnBGR.price_limit_bid,glass_region)
        if x >= 0:
            return 1
        x,y = self._color_search(img,ColorsBtnBGR.price_limit_ask,glass_region)
        if x >= 0:
            return -1
        _,fbid = self._color_search(img,ColorsBtnBGR.bid,glass_region)
        _,fask = self._color_search(img,ColorsBtnBGR.ask,glass_region,reverse=True)
        if fbid == -1:
            return -1
        if fask == -1:
            return 1
        return 0
    
    def _check_order(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        _,y = self._color_search(img,ColorsBtnBGR.color_x,glass_region)
        if y >= 0:
            return y
        _,y = self._color_search(img,ColorsBtnBGR.color_x_shadow,glass_region)
        if y >= 0:
            return y
        return None
    
    def _update_order(self,img,direction,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        order = self._check_order(img,symbol,idx)
        if order is None:
            return True
        if direction == 'long':
            bbid = self._get_best_bid(img,symbol,idx)
            delta_order = order - bbid
            if delta_order > 0 and delta_order < self.price_step:
                _, bid = self._color_search(img,ColorsBtnBGR.bid,glass_region)
                if bid < 0:
                    return True
                delta_bid = bid - bbid
                if delta_bid > 0 and delta_bid < self.price_step*1.5:
                    return False
        elif direction == 'short':
            bask = self._get_best_ask(img,symbol,idx)
            delta_order = bask - order
            if delta_order > 0 and delta_order < self.price_step:
                _, ask = self._color_search(img,ColorsBtnBGR.ask,glass_region,reverse=True)
                if ask < 0:
                    return True
                delta_ask = ask - bask
                if delta_ask > 0 and delta_ask < self.price_step*1.5:
                    return False
        return True
    
    def _send_open(self,direction,symbol,idx,img):
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        if direction == 'long':
            button = 'a'
        elif direction == 'short':
            button = 's'
        else:
            button = 'f'
        # need_update = self._update_order(img,direction,symbol,idx)
        # # print(symbol,need_update)
        # if not need_update:
        #     return
        pdi.press('f')
        pdi.press(button)
        if direction == 'all':
            pdi.press('a')
            pdi.press('s')

    def _send_close(self,direction,symbol,idx,img):
        rev_direction = 'long' if direction == 'short' else 'short'
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        pdi.press('z')
        self._send_open(rev_direction,symbol,idx,img)
        pdi.press('z')

    def _reverse_pos(self,direction,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        pdi.press('f')
        if direction == 'long':
            button = 'a'
        elif direction == 'short':
            button = 's'
        else:
            button = 'f'
        pdi.press('z')
        pdi.press(button)
        pdi.press('z')
        pdi.press(button)

    def _reset_req(self,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        pdi.press('f')

    def _send_by_simple(self,symbol,idx,left_btn:bool,press_f=False,press_z=False):
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        if press_f:
            pdi.press('f')
        if press_z:
            pdi.press('z')
        btn = 'a' if left_btn else 's'
        pdi.press(btn)
        if press_z:
            pdi.press('z')

    def _send_by_cords(self,symbol,idx,y:int,left_btn:bool,press_f=False,press_z=False):
        y = int(y)
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        if press_f:
            pdi.press('f')
        if press_z:
            pdi.press('z')
        btn = 'left' if left_btn else 'right'
        pdi.click(glass_region[0]+10,y,button=btn)
        if press_z:
            pdi.press('z')
    
    def _send_by_smart(self,symbol,idx,left_btn:bool,press_f=False,press_z=False,smart_per=30):
        fg = self.fgs[symbol][idx]
        if left_btn:
            bid_large_mask = (fg['type_cell'].isin(['bid', 'bbid'])) & (fg['vol_per'] >= smart_per)
            bid_large_indices = fg[bid_large_mask].index.tolist()[:1]
            if bid_large_indices:
                smart_bid = fg.iloc[bid_large_indices[0]]
                if smart_bid['type_cell'] == 'bbid':
                    self._send_by_simple(symbol,idx,left_btn,press_f,press_z)
                else:
                    self._send_by_cords(symbol,idx,smart_bid['middle'],left_btn,press_f,press_z)
        else:
            ask_large_mask = (fg['type_cell'].isin(['ask', 'bask'])) & (fg['vol_per'] >= smart_per)
            ask_large_indices = fg[ask_large_mask].index.tolist()[-1:]
            if ask_large_indices:
                smart_ask = fg.iloc[ask_large_indices[0]]
                if smart_ask['type_cell'] == 'bask':
                    self._send_by_simple(symbol,idx,left_btn,press_f,press_z)
                else:
                    self._send_by_cords(symbol,idx,smart_ask['middle'],left_btn,press_f,press_z)
    
    def _reset_by_cords(self,symbol,idx,y:int,left_btn:bool):
        y = int(y)
        glass_region = self.glass_region[symbol][idx]
        btn = 'left' if left_btn else 'right'
        pdi.click(glass_region[2]-5,y,button=btn)
        
    # new_methods
    def _add_level(self,dx,dy,chart_region):
        pdi.moveTo(chart_region[0]+69,chart_region[1]+10)
        pdi.click()
        pdi.moveTo(chart_region[0]+dx,chart_region[1]+dy)
        pdi.click()

    def _remove_levels(self,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        pdi.press('o')

    def _add_run_levels(self,pdata,symbol):
        if 'levels' in pdata:
            levels = pdata['levels']
            if isinstance(levels,list):
                chart_region = self.chart_region[symbol][0]
                self._remove_levels(symbol,0)
                offset = self.offset[symbol][0]
                candle_max = self.candle_max[symbol][0]
                for lvl in levels:
                    self._add_level(10,int(-lvl*candle_max+offset),chart_region)
            if isinstance(levels,dict):
                ...

    def _reset_draw_chart(self,chart_region):
        pdi.moveTo(chart_region[0]+50,chart_region[1]+50)
        pdi.rightClick()
        pdi.moveTo(chart_region[0]+45,chart_region[1]+45)
        pdi.click()
        pdi.moveTo(chart_region[0]+150,chart_region[1]+10)
        pdi.click()

    def _get_region(self,img,region):
        chart = img[
        region[1]:region[3],
        region[0]:region[2]]
        return chart
    
    def _get_mask(self,chart:npt.ArrayLike,color) -> npt.ArrayLike:
        mask = cv2.inRange(chart,color,color)
        return mask
    
    def _get_candle_mask(self,chart:npt.ArrayLike) -> npt.ArrayLike:
        mask1 = self._get_mask(chart,ColorsBtnBGR.candle_color_1)
        mask2 = self._get_mask(chart,ColorsBtnBGR.candle_color_2)
        mask = cv2.add(mask1,mask2)
        return mask

    def _get_volume_mask(self,chart:npt.ArrayLike) -> npt.ArrayLike:
        mask1 = self._get_mask(chart,ColorsBtnBGR.volume_color_1)
        mask2 = self._get_mask(chart,ColorsBtnBGR.volume_color_2)
        mask = cv2.add(mask1,mask2)
        kernel = np.ones((1, 2), np.uint8)  # 1 строка x 2 столбца
        mask = cv2.dilate(mask, kernel, iterations=1)
        return mask
    
    def _get_filtred_x(self,mask):
        mask = mask.copy()
        kernel = np.ones((3, 1), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        res_top = cv2.matchTemplate(mask,TemplateCandle.candle_top,cv2.TM_CCOEFF_NORMED)
        res_top = np.argwhere(res_top >= 0.9)
        res_bot = cv2.matchTemplate(mask,TemplateCandle.candle_bottom,cv2.TM_CCOEFF_NORMED)
        res_bot = np.argwhere(res_bot >= 0.9)
        res_x = np.concatenate((res_top,res_bot))
        unique_x = np.unique(res_x[:, 1])
        unique_x = np.sort(unique_x)
        distances = np.diff(unique_x)
        step = int(np.median(distances))
        mask = np.concatenate([[True], distances >= step / 2])
        filtered_x = unique_x[mask]
        full_x = []
        for i in range(len(filtered_x) - 1):
            full_x.append(filtered_x[i])
            gap = filtered_x[i + 1] - filtered_x[i]
            if gap > step * 1.5:
                # Добавляем промежуточные бары
                num_missing = int(np.round(gap / step)) - 1
                for j in range(1, num_missing + 1):
                    full_x.append(int(np.round(filtered_x[i] + j * step)))
        full_x.append(filtered_x[-1])
        filtered_x = np.array(full_x)
        return filtered_x, int(step)
       
    def _clear_bars(self,bars:pd.DataFrame,symbol,idx):
        bars = bars.astype(float)
        bars['middle'] = (bars['low'] +bars['high']) // 2
        bars['open'] = bars['open'].fillna(bars['close'].shift(1))
        bars['close'] = bars['close'].fillna(bars['open'].shift(-1))
        bars['volume'] = bars['volume'].fillna(bars['volume'].max())
        bars['open'] = bars['open'].fillna(bars['middle'])
        bars['close'] = bars['close'].fillna(bars['middle'])
        bars['direction'] = np.where(bars['open'] >= bars['close'],1,-1)
        bars['high'] = np.where(bars['high'] > bars['open'],bars['open'],bars['high'])
        bars['high'] = np.where(bars['high'] > bars['close'],bars['close'],bars['high'])
        bars['low'] = np.where(bars['low'] < bars['open'],bars['open'],bars['low'])
        bars['low'] = np.where(bars['low'] < bars['close'],bars['close'],bars['low'])
        numeric_cols = bars.select_dtypes(include=['float', 'int']).columns
        bars[numeric_cols] = bars[numeric_cols].astype(int)
        self.offset[symbol][idx] = bars['volume'].max()
        for k in ('high','low','volume','middle','open','close'):
            bars[k] = -bars[k] + self.offset[symbol][idx]
        bars['volume'] = bars['volume'] + 1
        # нормализация к значениям 0 - 1
        candle_max = bars['high'].max()
        if candle_max > 0:
            bars['volume'] = bars['volume'] / bars['volume'].max() if bars['volume'].max() > 0 else 0
            bars['close'] = bars['close'] / candle_max
            bars['open'] = bars['open'] / candle_max
            bars['low'] = bars['low'] / candle_max
            bars['high'] = bars['high'] / candle_max
            bars['middle'] = bars['middle'] / candle_max
        self.candle_max[symbol][idx] = candle_max
        return bars
    
    def _get_df(self,img,symbol,idx) -> pd.DataFrame:
        chart_region = self.chart_region[symbol][idx]
        chart = self._get_region(img,chart_region)
        volume_mask = self._get_volume_mask(chart)
        volume_cords = np.argwhere(volume_mask == 255)
        candle_mask = self._get_candle_mask(chart)
        candle_cords = np.argwhere(candle_mask == 255)
        filtered_x, step = self._get_filtred_x(candle_mask)
        bars = []
        radius = int(step * 0.45)
        for x in filtered_x:
            mask = (candle_cords[:, 1] >= x - radius) & (candle_cords[:, 1] <= x + radius)
            points = candle_cords[mask]
            if len(points) > 0:
                unique_x, counts = np.unique(points[:, 1], return_counts=True)
                real_x = unique_x[np.argmax(counts)]
                best_line = points[points[:, 1] == real_x]
                high_bar = best_line[:, 0].min()
                low_bar = best_line[:, 0].max()
            volume = volume_cords[np.where(volume_cords[:,1] == real_x)]
            volume_bar = volume[:,0].min()
            close_line = candle_cords[np.where(candle_cords[:,1] == real_x+1)]
            if close_line.size == 0:
                close_bar = None
            else:
                close_bar = close_line[:,0].max()
            open_line = candle_cords[np.where(candle_cords[:,1] == real_x-1)]
            if open_line.size == 0:
                open_bar = None
            else:
                open_bar = open_line[:,0].max()
            bars.append([x,high_bar,low_bar,open_bar,close_bar,volume_bar])
        bars = pd.DataFrame(bars,columns=['x','high','low','open','close','volume'])
        bars = self._clear_bars(bars,symbol,idx)
        return bars
    
    def _get_combined_mask(self, roi, colors):
        """Создает объединенную маску для списка цветов"""
        combined_mask = np.zeros(roi.shape[:2], dtype=bool)
        
        for color in colors:
            mask = (roi[:,:,0] == color[0]) & \
                (roi[:,:,1] == color[1]) & \
                (roi[:,:,2] == color[2])
            combined_mask = combined_mask | mask
        
        return combined_mask

    def _get_full_glass(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        start_tape = self.tape_region[symbol][idx][0]
        end_tape = self.tape_region[symbol][idx][2]
        bbid = self._get_best_bid(img,symbol,idx)
        bask = self._get_best_ask(img,symbol,idx)
        if bbid == -1 or bask == -1:
            return pd.DataFrame(columns=['type_cell', 'top', 'bottom', 'vol_per', 'have_order', 'have_level', 'large2', 'middle'])
        start_glass = glass_region[0]
        end_glass,_ = self._color_search(img,ColorsBtnBGR.large_value_1,glass_region,reverse=True)
        full_end_glass = glass_region[2]
        if end_glass == -1:
            return pd.DataFrame(columns=['type_cell', 'top', 'bottom', 'vol_per', 'have_order', 'have_level', 'large2', 'middle'])
        width_glass = end_glass - start_glass
        high_glass = glass_region[1]
        low_glass = glass_region[3]
        bid_len = (low_glass - bbid) // self.price_step
        ask_len = (bask - high_glass) // self.price_step
        spred_len = (bbid - bask) // self.price_step
        bids = [bbid + self.price_step * i for i in range(bid_len)]
        asks = [bask - self.price_step * i for i in range(ask_len)]
        spreds = []
        if spred_len > 0:
            spreds = [bbid - self.price_step * i for i in range(spred_len)]
        total_levels = bid_len + ask_len + spred_len
        if total_levels == 0:
            return pd.DataFrame(columns=['type_cell', 'top', 'bottom', 'vol_per', 'have_order', 'have_level', 'large2', 'middle'])
        df = pd.DataFrame({
            'type_cell': np.zeros(total_levels, dtype=object),
            'top': np.zeros(total_levels, dtype=np.int16),
            'bottom': np.zeros(total_levels, dtype=np.int16),
            'vol_per': np.zeros(total_levels, dtype=np.uint8),
        })
        
        # Заполняем биды
        idx = 0
        for bid_top in bids:
            df.loc[idx, 'type_cell'] = 'bid'
            df.loc[idx, 'top'] = bid_top
            df.loc[idx, 'bottom'] = bid_top + self.price_step

            idx += 1
        for spred_bottom in spreds:
            df.loc[idx, 'type_cell'] = 'spred'
            df.loc[idx, 'top'] = spred_bottom - self.price_step
            df.loc[idx, 'bottom'] = spred_bottom
            idx += 1
        # Заполняем аски
        for ask_bottom in asks:
            df.loc[idx, 'type_cell'] = 'ask'
            df.loc[idx, 'top'] = ask_bottom - self.price_step
            df.loc[idx, 'bottom'] = ask_bottom
            idx += 1

        df = df.sort_values('top').reset_index(drop=True)
        vol_per = np.zeros(len(df), dtype=np.uint8)
        have_order = np.full(len(df), False, dtype=bool)
        have_level = np.full(len(df), False, dtype=bool)
        
        # Преобразуем DataFrame в numpy массивы для быстрого доступа
        tops = df['top'].values.astype(int)
        bottoms = df['bottom'].values.astype(int)
        # Создаем массив всех ROI
        # Вместо поиска в каждом ROI отдельно - ищем все сразу
        for idx in range(len(df)):
            # Используем срез изображения напрямую
            top = tops[idx]+1
            bottom = bottoms[idx]-1
            roi = img[top:bottom, start_glass:end_glass]  
            # print(roi.shape)
            # Ищем цвет в ROI
            mask = self._get_combined_mask(roi, large_value_1_colors)

            if np.any(mask):
                # Находим самую правую точку (reverse=True)
                y_coords = np.where(mask)[1]  # колонки
                if len(y_coords) > 0:
                    x = y_coords[0] + start_glass  # самая левая
                    vol_per[idx] = ((end_glass - x) * 100) // width_glass
            
            mask = self._get_combined_mask(roi,large_value_2_colors)
            if np.any(mask):
                # Если есть цвет из группы 2 - ставим 100%
                vol_per[idx] = 100

            roi = img[top:bottom, end_glass:full_end_glass]
            mask = self._get_combined_mask(roi,(ColorsBtnBGR.color_x,ColorsBtnBGR.color_x_shadow))
            if np.any(mask):
                have_order[idx] = True

            roi = img[top:bottom, start_tape:end_tape]
            mask = self._get_combined_mask(roi,(ColorsBtnBGR.level_shift_1,))
            if np.any(mask):
                have_level[idx] = True

        df['vol_per'] = vol_per
        df['have_order'] = have_order
        df['have_level'] = have_level
        df['large2'] = df['vol_per'] > 99
        df['middle'] = (df['bottom'] + df['top']) // 2
        df.loc[df[df['type_cell'] == 'ask'].index[-1], 'type_cell'] = 'bask'
        df.loc[df[df['type_cell'] == 'bid'].index[0], 'type_cell'] = 'bbid'
        return df
  
    
    def _get_profit(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        _,p_max = self._color_search(img,ColorsBtnBGR.profit_glass,glass_region,reverse=True)
        _,p_min = self._color_search(img,ColorsBtnBGR.profit_glass,glass_region,reverse=False)
        return p_max,p_min
    
    def _get_loss(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        _,l_max = self._color_search(img,ColorsBtnBGR.loss_glass,glass_region,reverse=True)
        _,l_min = self._color_search(img,ColorsBtnBGR.loss_glass,glass_region,reverse=False)
        return l_max,l_min
    
    def _get_best_ask(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        _,y_max = self._color_search(img,ColorsBtnBGR.best_ask,glass_region,reverse=True)
        _,y_max_level = self._color_search(img,ColorsBtnBGR.best_ask_level,glass_region,reverse=True)
        _,y_test = self._color_search(img,ColorsBtnBGR.ask,glass_region,reverse=True)
        if y_max_level >= 0:
            return y_max_level
        if y_max >= 0:
            if y_max > y_test:
                return y_max
        return y_test
            
    def _get_best_bid(self,img,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        _,y_min = self._color_search(img,ColorsBtnBGR.best_bid,glass_region)
        _,y_min_level = self._color_search(img,ColorsBtnBGR.best_bid_level,glass_region)
        _,y_test = self._color_search(img,ColorsBtnBGR.bid,glass_region)
        if y_min_level >= 0:
            return y_min_level
        if y_min >= 0:
            if y_min < y_test:
                return y_min
        return y_test
    
    def _get_delta_p(self,img,symbol,idx,poss):
        ps = self.price_step
        pos = poss[symbol][idx]
        y_bask = self._get_best_ask(img,symbol,idx)
        y_bbid = self._get_best_bid(img,symbol,idx)
        p_max,p_min = self._get_profit(img,symbol,idx)
        l_max,l_min = self._get_loss(img,symbol,idx)
        if pos == 1: #long
            if y_bask > 0:
                if p_max != -1:
                    enter_price = p_max
                elif l_min != -1:
                    enter_price = l_min
                else:
                    return None
                delta_p = (enter_price - y_bask) // ps
                return delta_p
            else:
                return None
        elif pos == -1: #short
            if y_bbid > 0:
                if p_min != -1:
                    enter_price = p_min
                elif l_max != -1:
                    enter_price = l_max
                else:
                    return None
                delta_p = (y_bbid - enter_price) // ps
                return delta_p
            else:
                return None
        else:
            return None
    
    def _work_action(self,action,pos,img,symbol,idx):
        # print(self.name,pos,action) 
        if 'close_long' in action:
            if pos == 1:
                self._send_close('long',symbol,idx,img)
            else:
                self._reset_req(symbol,idx)
        elif 'close_short' in action:
            if pos == -1:
                self._send_close('short',symbol,idx,img)
            else:
                self._reset_req(symbol,idx)
        elif 'open_long' == action:
            if pos == -1:
                self._reverse_pos('long',symbol,idx)
            elif pos == 0:
                self._send_open('long',symbol,idx,img)
        elif 'open_short' == action:
            if pos == 1:
                self._reverse_pos('short',symbol,idx)
            elif pos == 0:
                self._send_open('short',symbol,idx,img)
        elif 'close_all' in action:
            if pos == -1:
                self._send_close('short',symbol,idx,img)
            elif pos == 1:
                self._send_close('long',symbol,idx,img)
            else:
                self._reset_req(symbol,idx)
        elif 'open_all' == action:
            if pos == -1:
                self._reverse_pos('long',symbol,idx)
            elif pos == 1:
                self._reverse_pos('short',symbol,idx)
            else:
                self._send_open('all',symbol,idx,img)
        elif 'test' == action:
            # print(self.symbols)
            # print(symbol,pos)
            ...

    def _work_action_OC(self,action:OrderCords,pos,img,symbol,idx):
        type_order = action.type_order
        left_btn = action.left_btn
        # Общее условие для отправки заявок
        # Разрешаем: открытие при пустой позиции, закрытие лонга, закрытие шорта
        can_send = (pos == 0 and action.is_open) or (pos == 1 and not left_btn) or (pos == -1 and left_btn)
        if type_order == 'send_cords':
            if can_send:
                self._send_by_cords(symbol, idx, action.y, left_btn, action.press_f, action.press_z)
        elif type_order == 'send_simple':
            if can_send:
                self._send_by_simple(symbol,idx,left_btn,action.press_f,action.press_z)
        elif type_order == 'send_smart':
            if can_send:
                self._send_by_smart(symbol,idx,left_btn,action.press_f,action.press_z,action.smart_per)
        elif type_order == 'reset_cords':
            self._reset_by_cords(symbol,idx,action.y,left_btn)
        elif type_order == 'reset_simple':
            self._reset_req(symbol,idx)
        elif type_order == 'close_all_simple':
            if pos > 0:
                # Закрываем лонг - продажа
                self._send_by_simple(symbol, idx, False, True, True)
            elif pos < 0:
                # Закрываем шорт - покупка
                self._send_by_simple(symbol, idx, True, True, True)
        elif type_order == 'close_all_smart':
            if pos > 0:
                self._send_by_smart(symbol, idx, False, True, True, action.smart_per)
            elif pos < 0:
                self._send_by_smart(symbol, idx, True, True, True, action.smart_per)
        


    def _check_close_on_time(self,action,time_mode):
        if self.close_on_time:
            if time_mode == -1:
                action = 'close_all'
            elif time_mode == -2:
                if action is not None:
                    if action == 'open_long':
                        action = 'close_short'
                    elif action == 'open_short':
                        action = 'close_long'
        return action
    
    def _check_close_on_time_OC(self,action:OrderCords,time_mode):
        change_action = False
        if self.close_on_time:
            if time_mode == -1:
                action = OrderCords('close_all_simple')
                change_action = True
            elif time_mode == -2:
                if action is not None:
                    if action.is_open: 
                        action = OrderCords('close_all_smart')
                        change_action = True
        return action, change_action

    def _get_params_for_ws(self,img,symbol,poss,delta_p):
        tdata = {}
        fg = None
        needs_info = self.wss[symbol].needs_info
        if needs_info is not None:
            if 'chart' in needs_info:
                tdata['chart'] = self._get_df(img,symbol,0)
            if 'charts' in needs_info:
                tdata['charts'] = {}
                for s in needs_info['charts']:
                    tdata['charts'][s] = []
                    for i in range(len(self.chart_region[s])):
                        df = self._get_df(img,s,i)
                        tdata['charts'][s].append(df)    
            if 'spred' in needs_info:
                bbid = self._get_best_bid(img,symbol,0)
                bask = self._get_best_ask(img,symbol,0)
                spred = (bbid - bask)// self.price_step
                tdata['spred'] = spred
            if 'full_glass' in needs_info:
                fg = self._get_full_glass(img,symbol,0)
                self.fgs[symbol][0] = fg
                tdata['fg'] = fg.copy()
        if fg is None and self.wss[symbol].mode is not None:
            mode = self.wss[symbol].mode
            if isinstance(mode,str):
                if 'fg' in mode:
                    fg = self._get_full_glass(img,symbol,0)
                    self.fgs[symbol][0] = fg
        
        return tdata
    
    def _processing_str_action(self,img,symbol,pos,time_mode,action):
        action = self._check_close_on_time(action,time_mode)
        price_limit = self._check_price_limit(img,symbol,0)
        if price_limit != 0:
            if pos != 0:
                action = 'close_all'
            else:
                action = None
        if action:
            self._work_action(action,pos,img,symbol,0)
        else:
            self._reset_req(symbol,0)
        return action

    def _processing_OC_action(self,img,symbol,pos,time_mode,action):
        go_next = True
        action, change_action = self._check_close_on_time_OC(action,time_mode)
        if change_action:
            go_next = False
        price_limit = self._check_price_limit(img,symbol,0)
        if price_limit != 0:
            go_next = False
            if pos != 0:
                action = OrderCords('close_all_simple')
            else:
                action = None
        if action:
            self._work_action_OC(action,pos,img,symbol,0)
        return action, go_next
    
    def _error_processing(self,symbol,err):
        print(self.symbols)
        print(f"!!!! {type(err).__name__}: {err} !!!!")
        if symbol is not None:
            print(symbol)
            for chart_region in self.chart_region[symbol]:
                self._reset_draw_chart(chart_region)
            with open(self.error_log[symbol],'a',encoding="utf-8") as f:
                f.write(str(datetime.now()) + "\n")
                f.write('\n')
                f.write(traceback.format_exc() + "\n")

    def prev_screen_reset(self):
        """Сбрасывает заявки для символов без режима перед скриншотом"""
        for symbol in self.symbols:
            if self.wss[symbol].mode is None:
                for i in range(len(self.glass_region[symbol])):
                    self._reset_req(symbol,i)

    def run(self,img):
        if not self.can_work:
            return
        symbol = None
        try:
            time_mode = self._check_time()
            if time_mode == 0:
                return
            
            poss = {symbol: [self._check_position(img, region) for region in regions] 
                for symbol, regions in self.position_region.items()}
            delta_p = {symbol: [self._get_delta_p(img, symbol, idx, poss) 
                                for idx in range(len(regions))]
                for symbol, regions in self.position_region.items()}
            
            for symbol in self.symbols:
                try:
                    self._check_z_tape(img,symbol)
                    tdata = self._get_params_for_ws(img,symbol,poss,delta_p)
                    pdata = self.wss[symbol].preprocessing(tdata)
                    self._add_run_levels(pdata,symbol)

                    pos = poss[symbol][0]
                    delta = delta_p[symbol][0]
                    action = self.wss[symbol](pdata,pos,delta)
                    # print(symbol,action)    
                    if isinstance(action, str) or action is None:
                        action = self._processing_str_action(img,symbol,pos,time_mode,action)
                    elif isinstance(action,dict):
                        ...
                    elif isinstance(action, (tuple, list)):
                        new_action = []
                        for act in action:
                            if isinstance(act, OrderCords):
                                act,go_next = self._processing_OC_action(img,symbol,pos,time_mode,act)
                                new_action.append(act)
                                if not go_next:
                                    break
                        action = new_action
                    # print(symbol,action,pos)

                except Exception as err:
                    print(symbol,'inner Error!')
                    self._error_processing(symbol,err)

        except Exception as err:
            print(symbol,'outer Error!')
            self._error_processing(symbol,err)