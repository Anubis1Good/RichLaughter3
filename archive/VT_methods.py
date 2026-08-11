# class VT7:    
#     def _get_full_glass(self,img,symbol,idx):
#         glass_region = self.glass_region[symbol][idx]
#         bbid = self._get_best_bid(img,symbol,idx)
#         bask = self._get_best_ask(img,symbol,idx)
#         if bbid == -1 or bask == -1:
#             return
#         start_glass = glass_region[0]
#         end_glass,_ = self._color_search(img,ColorsBtnBGR.ask,glass_region)
#         end_glass -= 2
#         full_end_glass = glass_region[2]
#         if end_glass == -1:
#             return
#         width_glass = end_glass - start_glass
#         high_glass = glass_region[1]
#         low_glass = glass_region[3]
#         bid_len = (low_glass - bbid) // self.price_step
#         ask_len = (bask - high_glass) // self.price_step
#         spred_len = (bbid - bask) // self.price_step
#         bids = [bbid + self.price_step * i for i in range(bid_len)]
#         asks = [bask - self.price_step * i for i in range(ask_len)]
#         spreds = []
#         if spred_len > 0:
#             spreds = [bbid - self.price_step * i for i in range(spred_len)]
#         total_levels = bid_len + ask_len + spred_len
#         if total_levels == 0:
#             return
#         df = pd.DataFrame({
#             'type_cell': np.zeros(total_levels, dtype=object),
#             'top': np.zeros(total_levels, dtype=np.int16),
#             'bottom': np.zeros(total_levels, dtype=np.int16),
#             'vol_per': np.zeros(total_levels, dtype=np.uint8),
#             # 'l1': np.zeros(total_levels, dtype=bool),
#             # 'l2': np.zeros(total_levels, dtype=bool),
#             # 'lvl': np.zeros(total_levels, dtype=bool),
#             # 'have_order': np.zeros(total_levels, dtype=bool)
#         })
        
#         # Заполняем биды
#         idx = 0
#         for bid_top in bids:
#             df.loc[idx, 'type_cell'] = 'bid'
#             df.loc[idx, 'top'] = bid_top
#             df.loc[idx, 'bottom'] = bid_top + self.price_step

#             idx += 1
#         for spred_bottom in spreds:
#             df.loc[idx, 'type_cell'] = 'spred'
#             df.loc[idx, 'top'] = spred_bottom - self.price_step
#             df.loc[idx, 'bottom'] = spred_bottom
#             idx += 1
#         # Заполняем аски
#         for ask_bottom in asks:
#             df.loc[idx, 'type_cell'] = 'ask'
#             df.loc[idx, 'top'] = ask_bottom - self.price_step
#             df.loc[idx, 'bottom'] = ask_bottom
#             idx += 1

#         df = df.sort_values('top').reset_index(drop=True)
#         vol_per = np.full(len(df), 100, dtype=np.uint8)
#         have_order = np.full(len(df), False, dtype=bool)
        
#         # Преобразуем DataFrame в numpy массивы для быстрого доступа
#         tops = df['top'].values.astype(int)
#         bottoms = df['bottom'].values.astype(int)
#         color_x = ColorsBtnBGR.color_x
#         color_x_shadow = ColorsBtnBGR.color_x_shadow
#         # Создаем массив всех ROI
#         # Вместо поиска в каждом ROI отдельно - ищем все сразу
#         for idx in range(len(df)):
#             # Используем срез изображения напрямую
#             roi = img[tops[idx]:bottoms[idx], start_glass:end_glass]  
#             # print(roi.shape)
#             # Ищем цвет в ROI
#             mask = (roi[:,:,0] == ColorsBtnBGR.vacuum_glass[0]) & \
#                 (roi[:,:,1] == ColorsBtnBGR.vacuum_glass[1]) & \
#                 (roi[:,:,2] == ColorsBtnBGR.vacuum_glass[2])
            
#             if np.any(mask):
#                 # Находим самую правую точку (reverse=True)
#                 y_coords = np.where(mask)[1]  # колонки
#                 if len(y_coords) > 0:
#                     x = y_coords[-1] + start_glass+1  # самая правая
#                     vol_per[idx] = ((end_glass - x) * 100) // width_glass

#             roi = img[tops[idx]:bottoms[idx], end_glass:full_end_glass]
#             mask = ((roi[:,:,0] == color_x[0]) & (roi[:,:,1] == color_x[1]) & (roi[:,:,2] == color_x[2])) | \
#             ((roi[:,:,0] == color_x_shadow[0]) & (roi[:,:,1] == color_x_shadow[1]) & (roi[:,:,2] == color_x_shadow[2]))
#             if np.any(mask):
#                 have_order[idx] = True

                    

#         df['vol_per'] = vol_per
#         df['have_order'] = have_order
#         print(symbol)
#         print(df)
#         # img_copy = img.copy()
#         # path_img = '_logs/imgs/'
#         # os.makedirs(path_img,exist_ok=True)
#         # filename = os.path.join(path_img,symbol + str(int(time()*1000)) + '.png')
#         # x1 = glass_region[0]
#         # x2 = glass_region[2]
#         # for bid in bids:
#         #     cv2.line(img_copy,(x1,bid),(x2,bid),(0,255,255))
#         # for ask in asks:
#         #     cv2.line(img_copy,(x1,ask),(x2,ask),(255,255,0))
#         # cv2.imwrite(filename,img_copy)

# =================================================
      # print(symbol)
        # print(df)
        # img_copy = img.copy()
        # path_img = '_logs/imgs/'
        # os.makedirs(path_img,exist_ok=True)
        # filename = os.path.join(path_img,symbol + str(int(time()*1000)) + '.png')
        # x1 = glass_region[0]
        # x2 = glass_region[2]
        # for idx, row in df.iterrows():
        #     middle_y = row['middle']
        #     vol = row['vol_per']
            
        #     # Размер точки зависит от vol_per (чем больше, тем больше точка)
        #     radius = 1 + (vol // 20)  # 1-6 пикселей
            
        #     # Цвет в зависимости от типа и vol_per
        #     if row['type_cell'] == 'bid':
        #         if vol > 50:
        #             color = (0, 0, 255)  # красный для больших бидов
        #         else:
        #             color = (255, 0, 0)  # синий для маленьких бидов
        #     elif row['type_cell'] == 'ask':
        #         if vol > 50:
        #             color = (255, 0, 0)  # синий для больших асков
        #         else:
        #             color = (0, 0, 255)  # красный для маленьких асков
        #     else:
        #         color = (0, 255, 255)  # желтый для спреда
            
        #     cv2.circle(img_copy, (x1 + 30, middle_y), radius, color, -1)
        # cv2.imwrite(filename,img_copy)

# ======================
        # filtered_df = df[df['have_order']]
        # for idx, row in filtered_df.iterrows():
        #     middle = row['middle']
        #     btn = row['type_cell'] == 'bid'
        #     self._reset_by_cords(symbol,0,middle,btn)

# =======================

        # path_img = '_logs/charts/'
        # os.makedirs(path_img,exist_ok=True)
        # filename = os.path.join(path_img,symbol + str(int(time()*1000)) + '.png')
        # fig = draw_bars_chart(bars)
        # fig.savefig(filename)
        # print(symbol,'save')
        # print(bars)

# old method large, level, other

#     def _colorarea_search(self,img:npt.ArrayLike, color:tuple[int],region:tuple[int]=(None,None,None,None), y_min=None, y_max=None, reverse_sort=False, skip_m1=True):
#         if skip_m1:
#             if y_min == -1 or y_max == -1:
#                 return []
#         mask = cv2.inRange(img, color, color)
#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         # 3. Фильтруем и собираем информацию
#         regions_f = []
#         used_y_positions = []
#         for contour in contours:
#             area = cv2.contourArea(contour)
#             # Фильтр по площади
#             if area < 20:
#                 continue
#             # Вычисляем bounding box
#             x, y, w, h = cv2.boundingRect(contour)
#             # Центр области
#             cx = x + w // 2
#             cy = y + h // 2
#             if region is not None and region[0] is not None:
#                 if not region[0] < cx < region[2]:
#                     continue
#             if y_max is not None:
#                 if cy > y_max:
#                     continue
#             if y_min is not None:
#                 if cy < y_min:
#                     continue
#             is_duplicate = False
#             for used_y in used_y_positions:
#                 if abs(cy - used_y) <= 10:
#                     is_duplicate = True
#                     break
#             if is_duplicate:
#                 continue  # Пропускаем дубликат
#             # Добавляем новую уникальную область
#             used_y_positions.append(cy)
#             # Сохраняем информацию
#             regions_f.append({
#                 'cx': cx,
#                 'cy': cy,
#             })
#         # 4. Сортируем
#         regions_f.sort(key=lambda r: r['cy'],reverse=reverse_sort)
#         return regions_f

#  #TODO можно подумать над btn возле bests, а так же об сохранении заявок, если их не нужно менять
#     def _send_open_level(self,img,direction,symbol,idx,n=1,reverse_pos=False,press_f=True):
#         glass_region = self.glass_region[symbol][idx]
#         x = glass_region[0] + 11
#         pdi.moveTo(x,glass_region[1]+11)
#         if press_f:
#             pdi.press('f')
#         level_color = ColorsBtnBGR.level_shift_1
#         y_min,y_max = None,None
#         if direction == 'short':
#             y_max = self._get_best_ask(img,symbol,idx)
#             reverse_sort = True
#         else:
#             y_min = self._get_best_bid(img,symbol,idx)
#             reverse_sort = False
#         regions = self._colorarea_search(img,level_color,self.tape_region[symbol][idx],y_min=y_min,y_max=y_max,reverse_sort=reverse_sort)
#         n_req = min(n,len(regions))
#         print(symbol,regions)
#         for i in range(n_req):
#             try:
#                 cx,cy = x,regions[i]['cy']
#                 if direction == 'short':
#                     if reverse_pos and i == 0:
#                         pdi.press('z')
#                         pdi.rightClick(cx,cy)
#                         pdi.press('z')
#                     pdi.rightClick(cx,cy)
#                 else:
#                     if reverse_pos and i == 0:
#                         pdi.press('z')
#                         pdi.click(cx,cy)
#                         pdi.press('z')
#                     pdi.click(cx,cy)
#             except Exception as err:
#                 traceback.print_exc()
#                 pass
            
#     def _send_open_all_level(self,img,symbol,idx,n=1):
#         self._send_open_level(img,'long',symbol,idx,n,press_f=True)
#         self._send_open_level(img,'short',symbol,idx,n,press_f=False)

#     def _send_close_level(self,img,direction,symbol,idx,n=1,use_z=True):
#         glass_region = self.glass_region[symbol][idx]
#         pdi.moveTo(glass_region+11,glass_region+11)
#         rev_direction = 'long' if direction == 'short' else 'short'
#         if use_z:
#             pdi.press('z')
#             self._send_open_level(img,rev_direction,symbol,idx,1)
#             pdi.press('z')
#         else:
#             self._send_open_level(img,rev_direction,symbol,idx,n)

#     def _get_region_large(self,img,direction,large_open,large_close,symbol,idx):
#         level_colors_1= (ColorsBtnBGR.large_value_1,ColorsBtnBGR.large_value_1_level)
#         level_colors_2 = (ColorsBtnBGR.large_value_2,ColorsBtnBGR.large_value_2_level)
#         y_max = self._get_best_ask(img,symbol,idx)
#         y_min = self._get_best_bid(img,symbol,idx)
#         regions_open,regions_close = [],[]
#         regions_colors_1 = []
#         regions_colors_2 = []
#         if direction == 'short':
#             reverse_sort = True
#             for level_color in level_colors_1:
#                 regions_colors_1 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=None,y_max=y_max,reverse_sort=reverse_sort)
#             for level_color in level_colors_2:
#                 regions_colors_2 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=None,y_max=y_max,reverse_sort=reverse_sort)
#         else:
#             reverse_sort = False
#             for level_color in level_colors_1:
#                 regions_colors_1 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=y_min,y_max=None,reverse_sort=reverse_sort)
#             for level_color in level_colors_2:
#                 regions_colors_2 += self._colorarea_search(img,level_color,self.glass_region[symbol][idx],y_min=y_min,y_max=None,reverse_sort=reverse_sort)
#         if '1' in large_open:
#             regions_open += regions_colors_1
#         if '2' in large_open:
#             regions_open += regions_colors_2    
#         if '1' in large_close:
#             regions_close += regions_colors_1
#         if '2' in large_close:
#             regions_close += regions_colors_2 

#         regions_open.sort(key=lambda r: r['cy'],reverse=reverse_sort)
#         regions_close.sort(key=lambda r: r['cy'],reverse=reverse_sort)
#         return regions_open,regions_close,y_min,y_max

#     def _enter_large(self,direction,y_min,y_max,cx,cy):
#         if direction == 'short':
#             if y_min - cy > self.price_step*2:
#                 cy += self.price_step
#                 pdi.rightClick(cx,cy)
#                 # print(self.name,'mouse')
#             else:
#                 pdi.press('s')
#                 # print(self.name,'btn')
#         else:
#             if cy - y_max > self.price_step*2:
#                 cy -= self.price_step
#                 # print(self.name,'mouse')
#                 pdi.click(cx,cy)
#             else:
#                 pdi.press('a')
#                 # print(self.name,'btn')

#     def _send_open_large(self,img,direction,symbol,idx,n=1,reverse_pos=False,press_f=True,large_open='',large_close='',main_large_open=True):
#         pdi.moveTo(self.glass_region[symbol][idx][0]+11,self.glass_region[symbol][idx][1]+11)
#         if press_f:
#             pdi.press('f')
#         regions_open,regions_close,y_min,y_max = self._get_region_large(img,direction,large_open,large_close,symbol,idx)
#         if main_large_open:
#             n_req = min(n,len(regions_open))
#             main_region = regions_open
#         else:
#             n_req = min(n,len(regions_close))
#             main_region = regions_close
#         if reverse_pos:
#             cx,cy = regions_close[0]['cx'],regions_close[0]['cy']
#             pdi.press('z')
#             self._enter_large(direction,y_min,y_max,cx,cy)
#             pdi.press('z')
#         # print(self.name,regions,y_max,y_min)
#         for i in range(n_req):
#             try:
#                 cx,cy = main_region[i]['cx'],main_region[i]['cy']
#                 self._enter_large(direction,y_min,y_max,cx,cy)
#             except Exception as err:
#                 traceback.print_exc()
#                 pass

#     def _send_open_all_large(self,img,symbol,idx,n=1,large_open='',large_close=''):
#         self._send_open_large(img,'long',symbol,idx,n,press_f=True,large_open=large_open,large_close=large_close)
#         self._send_open_large(img,'short',symbol,idx,n,press_f=False,large_open=large_open,large_close=large_close)

#     def _send_close_large(self,img,direction,symbol,idx,n=1,use_z=True,large_open='',large_close=''):
#         pdi.moveTo(self.glass_region[symbol][idx][0]+11,self.glass_region[symbol][idx][1]+11)
#         rev_direction = 'long' if direction == 'short' else 'short'
#         if use_z:
#             pdi.press('z')
#             self._send_open_large(img,rev_direction,symbol,idx,1,large_open=large_open,large_close=large_close,main_large_open=False)
#             pdi.press('z')
#         else:
#             self._send_open_large(img,rev_direction,symbol,idx,n,large_open=large_open,large_close=large_close,main_large_open=False)

#     def _large_init(self,action:str):
#         # sample 'all_spred_large_o2_c12_2'
#         n = action.split('_')[-1]
#         match = re.search(r'o(\d+)', action)
#         if match:
#             large_open = match.group(1)
#         else:
#             large_open = ''
#         match = re.search(r'c(\d+)', action)
#         if match:
#             large_close = match.group(1)
#         else:
#             large_close = ''
#         if n.isdigit():
#             n = int(n)
#         else:
#             n = None
#         return n,large_open,large_close

#     #TODO Отрефакторить
#     def _work_large_action(self,action,pos,img,symbol,idx):
#         n,large_open,large_close = self._large_init(action)
#         # print(self.name,n,large_open,large_close)
#         if n is not None:
#             use_z = False if 'danger' in action else True
#             if 'close' in action:
#                 if 'long' in action or 'all' in action and pos == 1:
#                     self._send_close_large(img,'long',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
#                 elif 'short' in action or 'all' in action and pos == -1:
#                     self._send_close_large(img,'short',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
#                 else:
#                     self._reset_req(symbol,idx)
#             elif 'spred' in action:
#                 if 'long' in action:
#                     if pos == -1:
#                         self._send_open_large(img,'long',symbol,idx,n,True,large_open=large_open,large_close=large_close)
#                     elif pos == 0:
#                         self._send_open_large(img,'long',symbol,idx,n,large_open=large_open,large_close=large_close)
#                     else:
#                         self._send_close_large(img,'long',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
#                 if 'short' in action:
#                     if pos == 1:
#                         self._send_open_large(img,'short',symbol,idx,n,True,large_open=large_open,large_close=large_close)
#                     elif pos == 0:
#                         self._send_open_large(img,'short',symbol,idx,n,large_open=large_open,large_close=large_close)
#                     else:
#                         self._send_close_large(img,'short',symbol,idx,n,use_z,large_open=large_open,large_close=large_close)
#             elif 'long' in action:
#                 if pos == -1:
#                     self._send_open_large(img,'long',symbol,idx,n,True,large_open=large_open,large_close=large_close)
#                 if pos == 0:
#                     self._send_open_large(img,'long',symbol,idx,n,large_open=large_open,large_close=large_close)
#             elif 'short' in action:
#                 if pos == 1:
#                     self._send_open_large(img,'short',symbol,idx,n,True,large_open=large_open,large_close=large_close)
#                 if pos == 0:
#                     self._send_open_large(img,'short',symbol,idx,n,large_open=large_open,large_close=large_close)
#             elif 'all' in action:
#                 if pos == -1:
#                     self._send_open_large(img,'long',symbol,idx,n,True,large_open=large_open,large_close=large_close)
#                 elif pos == 1:
#                     self._send_open_large(img,'short',symbol,idx,n,True,large_open=large_open,large_close=large_close)
#                 else:
#                     self._send_open_all_large(img,symbol,idx,n,large_open=large_open,large_close=large_close)

#     def _work_level_action(self,action:str,pos,img,symbol,idx):
#         n = action.split('_')[-1]
#         if n.isdigit():
#             n = int(n)
#         else:
#             n = None
#         if n is not None:
#             if 'close' in action: #закрытие на уровне
#                 use_z = False if 'danger' in action else True
#                 if 'long' in action or 'all' in action and pos == 1:
#                     self._send_close_level(img,'long',symbol,idx,n,use_z)
#                 elif 'short' in action or 'all' in action and pos == -1:
#                     self._send_close_level(img,'short',symbol,idx,n,use_z)
#                 else:
#                     self._reset_req(symbol,idx)
#             elif 'long' in action: #открытие на уровне
#                 if pos == -1:
#                     self._send_open_level(img,'long',symbol,idx,n,True)
#                 if pos == 0:
#                     self._send_open_level(img,'long',symbol,idx,n)
#             elif 'short' in action:
#                 if pos == 1:
#                     self._send_open_level(img,'short',symbol,idx,n,True)
#                 if pos == 0:
#                     self._send_open_level(img,'short',symbol,idx,n)
#             elif 'all' in action:
#                 if pos == -1:
#                     self._send_open_level(img,'long',symbol,idx,n,True)
#                 elif pos == 1:
#                     self._send_open_level(img,'short',symbol,idx,n,True)
#                 else:
#                     self._send_open_all_level(img,symbol,idx,n)
#             print(symbol,pos,action)
# 	def _work_action(self,action,pos,img,symbol,idx):
#         if 'large' in action:
#             self._work_large_action(action,pos,img,symbol,idx)
#         elif 'level' in action:
#             self._work_level_action(action,pos,img,symbol,idx)
            
#  	def _check_close_on_time(self,action,time_mode):
#         ...
#         elif time_mode == -2:
# 			elif 'large' in action:
# 				action = re.sub(r'o\d+', 'o0', action)