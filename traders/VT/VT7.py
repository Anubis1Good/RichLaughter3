import traceback
import os
import re
from datetime import datetime
import cv2
import pandas as pd
import numpy as np
import numpy.typing as npt
from time import time
from datetime import datetime
import pydirectinput as pdi
from traders.VT.settingsPB import ColorsBtnBGR,TemplateCandle
from strategies.BaseEG import BaseEG
from traders.VT.bot_on_ticker import init_trader



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
        for dom in conf_data['doms']:
            for i, symbol in enumerate(symbols):
                if i < len(dom['glasses']):
                    self.glass_region[symbol].append(dom['glasses'][i])
                    self.position_region[symbol].append(dom['poses'][i])
                    self.tape_region[symbol].append(dom['tapes'][i])
                    self.cluster_region[symbol].append(dom['clusters'][i])
        
        # Распаковка charts
        self.chart_region = {symbol: [] for symbol in symbols}
        self.offset = {symbol: [] for symbol in symbols}

        for chart in conf_data['charts']:
            for i, symbol in enumerate(symbols):
                if i < len(chart):
                    self.chart_region[symbol].append(chart[i])
                    self.offset[symbol].append(None)

        self.price_step = conf_data['price_step']
        self.wss: dict[str, BaseEG] = dict()
        for symbol in self.symbols:
            ws = init_trader(symbol)
            self.wss[symbol] = ws[0](symbol,self.price_step,ws[2],ws[1])
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
            result = np.argwhere(
                (img[region[1]:region[3],region[0]:region[2],0] == color[0])& 
                (img[region[1]:region[3],region[0]:region[2],1] == color[1])& 
                (img[region[1]:region[3],region[0]:region[2],2] == color[2])
            )
            y = -1 if reverse else 0
            if region[0]:
                return result[y,1]+region[0], result[y,0]+region[1]
            return result[y,1],result[y,0]

        except Exception:
            # traceback.print_exc()
            return -1,-1
        
    def _colorarea_search(self,img:npt.ArrayLike, color:tuple[int],region:tuple[int]=(None,None,None,None), y_min=None, y_max=None, reverse_sort=False, skip_m1=True):
        if skip_m1:
            if y_min == -1 or y_max == -1:
                return []
        mask = cv2.inRange(img, color, color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 3. Фильтруем и собираем информацию
        regions_f = []
        used_y_positions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            # Фильтр по площади
            if area < 50:
                continue
            # Вычисляем bounding box
            x, y, w, h = cv2.boundingRect(contour)
            # Центр области
            cx = x + w // 2
            cy = y + h // 2
            if region is not None and region[0] is not None:
                if not region[0] < cx < region[2]:
                    continue
            if y_max is not None:
                if cy > y_max:
                    continue
            if y_min is not None:
                if cy < y_min:
                    continue
            is_duplicate = False
            for used_y in used_y_positions:
                if abs(cy - used_y) <= 10:
                    is_duplicate = True
                    break
            if is_duplicate:
                continue  # Пропускаем дубликат
            # Добавляем новую уникальную область
            used_y_positions.append(cy)
            # Сохраняем информацию
            regions_f.append({
                'cx': cx,
                'cy': cy,
            })
        # 4. Сортируем
        regions_f.sort(key=lambda r: r['cy'],reverse=reverse_sort)
        return regions_f
        
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
    #TODO MUST HAVE
    def _check_price_limit(self,img,symbol,idx):
        ...
    
    def _send_open(self,direction,symbol,idx):
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        pdi.press('f')
        if direction == 'long':
            button = 'a'
        elif direction == 'short':
            button = 's'
        else:
            button = 'f'
        pdi.press(button)

    def _send_close(self,direction,symbol,idx):
        rev_direction = 'long' if direction == 'short' else 'short'
        glass_region = self.glass_region[symbol][idx]
        pdi.moveTo(glass_region[0]+11,glass_region[1]+11)
        pdi.press('z')
        self._send_open(rev_direction,symbol,idx)
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
                for lvl in levels:
                    self._add_level(10,int(-lvl+offset),chart_region)
            if isinstance(levels,dict):
                ...

    def _reset_draw_chart(self,chart_region):
        pdi.moveTo(chart_region[0]+50,chart_region[1]+50)
        pdi.rightClick()
        pdi.moveTo(chart_region[0]+45,chart_region[1]+45)
        pdi.click()
        pdi.moveTo(chart_region[0]+150,chart_region[1]+10)
        pdi.click()


    
    def _send_open_level(self,img,direction,n=1,reverse_pos=False,press_f=True):
        pdi.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        if press_f:
            pdi.press('f')
        # level_color = ColorsBtnBGR.ask_level_1 if direction=='short' else ColorsBtnBGR.bid_level_1
        level_color = ColorsBtnBGR.level_shift_1
        y_min,y_max = None,None
        if direction == 'short':
            x,y_max = self._color_search(img,ColorsBtnBGR.best_ask,self.glass_region,reverse=True)
            reverse_sort = True
        else:
            x,y_min = self._color_search(img,ColorsBtnBGR.best_bid,self.glass_region)
            reverse_sort = False
        regions = self._colorarea_search(img,level_color,self.glass_region,y_min=y_min,y_max=y_max,reverse_sort=reverse_sort)
        n_req = min(n,len(regions))
        print(self.name,regions)
        for i in range(n_req):
            try:
                cx,cy = x,regions[i]['cy']
                if direction == 'short':
                    if reverse_pos and i == 0:
                        pdi.press('z')
                        pdi.rightClick(cx,cy+10)
                        pdi.press('z')
                    pdi.rightClick(cx,cy+10)
                else:
                    if reverse_pos and i == 0:
                        pdi.press('z')
                        pdi.click(cx,cy-10)
                        pdi.press('z')
                    pdi.click(cx,cy-10)
            except Exception as err:
                traceback.print_exc()
                pass

    def _send_open_all_level(self,img,n=1):
        self._send_open_level(img,'long',n,press_f=True)
        self._send_open_level(img,'short',n,press_f=False)

    def _send_close_level(self,img,direction,n=1,use_z=True):
        pdi.moveTo(self.glass_region[0]+11,self.glass_region[1]+11)
        rev_direction = 'long' if direction == 'short' else 'short'
        if use_z:
            pdi.press('z')
            self._send_open_level(img,rev_direction,1)
            pdi.press('z')
        else:
            self._send_open_level(img,rev_direction,n)

    def _get_region_large(self,img,direction,large_open,large_close,symbol,idx):
        level_colors_1= (ColorsBtnBGR.large_value_1,ColorsBtnBGR.large_value_1_level)
        level_colors_2 = (ColorsBtnBGR.large_value_2,ColorsBtnBGR.large_value_2_level)
        y_max = self._get_best_ask(img,symbol,idx)
        y_min = self._get_best_bid(img,symbol,idx)
        regions_open,regions_close = [],[]
        regions_colors_1 = []
        regions_colors_2 = []
        if direction == 'short':
            reverse_sort = True
            for level_color in level_colors_1:
                regions_colors_1 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=None,y_max=y_max,reverse_sort=reverse_sort)
            for level_color in level_colors_2:
                regions_colors_2 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=None,y_max=y_max,reverse_sort=reverse_sort)
        else:
            reverse_sort = False
            for level_color in level_colors_1:
                regions_colors_1 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=y_min,y_max=None,reverse_sort=reverse_sort)
            for level_color in level_colors_2:
                regions_colors_2 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=y_min,y_max=None,reverse_sort=reverse_sort)
        if '1' in large_open:
            regions_open += regions_colors_1
        if '2' in large_open:
            regions_open += regions_colors_2    
        if '1' in large_close:
            regions_close += regions_colors_1
        if '2' in large_close:
            regions_close += regions_colors_2 

        regions_open.sort(key=lambda r: r['cy'],reverse=reverse_sort)
        regions_close.sort(key=lambda r: r['cy'],reverse=reverse_sort)
        return regions_open,regions_close,y_min,y_max

    def _enter_large(self,direction,y_min,y_max,cx,cy):
        if direction == 'short':
            if y_min - cy > self.price_step*2:
                cy += self.price_step
                pdi.rightClick(cx,cy)
                # print(self.name,'mouse')
            else:
                pdi.press('s')
                # print(self.name,'btn')
        else:
            if cy - y_max > self.price_step*2:
                cy -= self.price_step
                # print(self.name,'mouse')
                pdi.click(cx,cy)
            else:
                pdi.press('a')
                # print(self.name,'btn')

    def _send_open_large(self,img,direction,symbol,idx,n=1,reverse_pos=False,press_f=True,large_open='',large_close='',main_large_open=True):
        pdi.moveTo(self.glass_region[symbol][idx][0]+11,self.glass_region[symbol][idx][1]+11)
        if press_f:
            pdi.press('f')
        regions_open,regions_close,y_min,y_max = self._get_region_large(img,direction,large_open,large_close,symbol,idx)
        if main_large_open:
            n_req = min(n,len(regions_open))
            main_region = regions_open
        else:
            n_req = min(n,len(regions_close))
            main_region = regions_close
        if reverse_pos:
            cx,cy = regions_close[0]['cx'],regions_close[0]['cy']
            pdi.press('z')
            self._enter_large(direction,y_min,y_max,cx,cy)
            pdi.press('z')
        # print(self.name,regions,y_max,y_min)
        for i in range(n_req):
            try:
                cx,cy = main_region[i]['cx'],main_region[i]['cy']
                self._enter_large(direction,y_min,y_max,cx,cy)
            except Exception as err:
                traceback.print_exc()
                pass

    def _send_open_all_large(self,img,symbol,idx,n=1,large_open='',large_close=''):
        self._send_open_large(img,'long',symbol,idx,n,press_f=True,large_open=large_open,large_close=large_close)
        self._send_open_large(img,'short',symbol,idx,n,press_f=False,large_open=large_open,large_close=large_close)

    def _send_close_large(self,img,direction,symbol,idx,n=1,use_z=True,large_open='',large_close=''):
        pdi.moveTo(self.glass_region[symbol][idx][0]+11,self.glass_region[symbol][idx][1]+11)
        rev_direction = 'long' if direction == 'short' else 'short'
        if use_z:
            pdi.press('z')
            self._send_open_large(img,rev_direction,symbol,idx,1,large_open=large_open,large_close=large_close,main_large_open=False)
            pdi.press('z')
        else:
            self._send_open_large(img,rev_direction,symbol,idx,n,large_open=large_open,large_close=large_close,main_large_open=False)


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
        self.offset[symbol][idx] = bars['volume'].max() + 1
        for k in ('high','low','volume','middle','open','close'):
            bars[k] = -bars[k] + self.offset[symbol][idx]
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
    
    def _large_init(self,action:str):
        # sample 'all_spred_large_o2_c12_2'
        n = action.split('_')[-1]
        match = re.search(r'o(\d+)', action)
        if match:
            large_open = match.group(1)
        else:
            large_open = ''
        match = re.search(r'c(\d+)', action)
        if match:
            large_close = match.group(1)
        else:
            large_close = ''
        if n.isdigit():
            n = int(n)
        else:
            n = None
        return n,large_open,large_close

    #TODO Отрефакторить
    def _work_large_action(self,action,pos,img,symbol,idx):
        n,large_open,large_close = self._large_init(action)
        # print(self.name,n,large_open,large_close)
        if n is not None:
            use_z = False if 'danger' in action else True
            if 'close' in action:
                if 'long' in action or 'all' in action and pos == 1:
                    self._send_close_large(img,'long',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
                elif 'short' in action or 'all' in action and pos == -1:
                    self._send_close_large(img,'short',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
                else:
                    self._reset_req(symbol,idx)
            elif 'spred' in action:
                if 'long' in action:
                    if pos == -1:
                        self._send_open_large(img,'long',symbol,idx,n,True,large_open=large_open,large_close=large_close)
                    elif pos == 0:
                        self._send_open_large(img,'long',symbol,idx,n,large_open=large_open,large_close=large_close)
                    else:
                        self._send_close_large(img,'long',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
                if 'short' in action:
                    if pos == 1:
                        self._send_open_large(img,'short',symbol,idx,n,True,large_open=large_open,large_close=large_close)
                    elif pos == 0:
                        self._send_open_large(img,'short',symbol,idx,n,large_open=large_open,large_close=large_close)
                    else:
                        self._send_close_large(img,'short',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
            elif 'long' in action:
                if pos == -1:
                    self._send_open_large(img,'long',symbol,idx,n,True,large_open=large_open,large_close=large_close)
                if pos == 0:
                    self._send_open_large(img,'long',symbol,idx,n,large_open=large_open,large_close=large_close)
            elif 'short' in action:
                if pos == 1:
                    self._send_open_large(img,'short',symbol,idx,n,True,large_open=large_open,large_close=large_close)
                if pos == 0:
                    self._send_open_large(img,'short',symbol,idx,n,large_open=large_open,large_close=large_close)
            elif 'all' in action:
                if pos == -1:
                    self._send_open_large(img,'long',symbol,idx,n,True,large_open=large_open,large_close=large_close)
                elif pos == 1:
                    self._send_open_large(img,'short',symbol,idx,n,True,large_open=large_open,large_close=large_close)
                else:
                    self._send_open_all_large(img,symbol,idx,n,large_open=large_open,large_close=large_close)

    def _work_level_action(self,action,pos,img):
        n = action.split('_')[-1]
        if n.isdigit():
            n = int(n)
        else:
            n = None
        if n is not None:
            if 'close' in action:
                use_z = False if 'danger' in action else True
                if 'long' in action or 'all' in action and pos == 1:
                    self._send_close_level(img,'long',n,use_z)
                elif 'short' in action or 'all' in action and pos == -1:
                    self._send_close_level(img,'short',n,use_z)
                else:
                    self._reset_req()
            elif 'long' in action:
                if pos == -1:
                    self._send_open_level(img,'long',n,True)
                if pos == 0:
                    self._send_open_level(img,'long',n)
            elif 'short' in action:
                if pos == 1:
                    self._send_open_level(img,'short',n,True)
                if pos == 0:
                    self._send_open_level(img,'short',n)
            elif 'all' in action:
                if pos == -1:
                    self._send_open_level(img,'long',n,True)
                elif pos == 1:
                    self._send_open_level(img,'short',n,True)
                else:
                    self._send_open_all_level(img,n)
            print(self.name,pos,action)

    def _work_action(self,action,pos,img,symbol,idx):
        # print(self.name,pos,action)
        if 'large' in action:
            self._work_large_action(action,pos,img,symbol,idx)
        elif 'level' in action:
            # self._work_level_action(action,pos,img)
            self._reset_req(symbol,idx)
        elif 'close_long' in action:
            if pos == 1:
                self._send_close('long',symbol,idx)
            else:
                self._reset_req(symbol,idx)
        elif 'close_short' in action:
            if pos == -1:
                self._send_close('short',symbol,idx)
            else:
                self._reset_req(symbol,idx)
        elif 'open_long' in action:
            if pos == -1:
                self._reverse_pos('long',symbol,idx)
            if pos == 0:
                self._send_open('long',symbol,idx)
        elif 'open_short' in action:
            if pos == 1:
                self._reverse_pos('short',symbol,idx)
            if pos == 0:
                self._send_open('short',symbol,idx)
        elif 'close_all' in action:
            if pos == -1:
                self._send_close('short',symbol,idx)
            elif pos == 1:
                self._send_close('long',symbol,idx)
            else:
                self._reset_req(symbol,idx)
        elif 'test' in action:
            ...
            # print(self.glass_region)
            # print(self.chart_region)
            # print(self.position_region)
            # print(self.name)
            # print(self.ws)
            # self._remove_levels()
            # self._add_level(100,100)
        # else:
        #     print('None work')
    def _get_params_for_ws(self,img,symbol,poss,delta_p):
        tdata = {}
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
        return tdata

    def _check_close_on_time(self,action,time_mode):
        if self.close_on_time:
            if time_mode == -1:
                action = 'close_all'
            elif time_mode == -2:
                if action == 'open_long':
                    action = 'close_short'
                elif action == 'open_short':
                    action = 'close_long'
            elif time_mode == -3:
                action = 'close_all'
        return action

    def run(self,img):
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
                self._check_z_tape(img,symbol)

                tdata = self._get_params_for_ws(img,symbol,poss,delta_p)
                pdata = self.wss[symbol].preprocessing(tdata)
                self._add_run_levels(pdata,symbol)

                pos = poss[symbol][0]
                delta = delta_p[symbol][0]
                action = self.wss[symbol](pdata,pos,delta)
                if isinstance(action, str):
                    action = self._check_close_on_time(action,time_mode)
                    if action:
                        self._work_action(action,pos,img,symbol,0)
                    else:
                        self._reset_req(self.glass_region[symbol][0])

                elif isinstance(action,dict):
                    ...

        except Exception as err:
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