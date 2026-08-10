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