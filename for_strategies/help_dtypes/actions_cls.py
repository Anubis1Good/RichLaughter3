from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
# import numpy as np

@dataclass
class OrderCords:
    """
    type_order:
        'send_cords' - отправляет заявку в определенные координаты в стакане
        'reset_cords' - снимает заявку в определенных координатах
        'send_simple' - отправяет заявку по лучшей цене
        'send_smart' - отправляет заявку по лучшей цене перед заявкой больше smart_per
        'reset_simple' - снимает все заявки в стакане  
        'close_all_simple' - закрывает все позиции по лучшей цене
        'close_all_smart' - закрывает все позиции по лучшей цене перед заявкой больше smart_per
        'no_action' - ничего не делать
    """
    type_order:str 
    y:Optional[int]=None #150
    left_btn:bool=True
    press_f:bool=False
    press_z:bool=False
    is_open:bool = True
    smart_per:int = 50
    idx_chart:int = 0


class OrderManager:
    def __init__(self):
        pass

    def get_spred_orders(
        self,
        fg: pd.DataFrame,
        direction: int = 0,  # 0 - both, 1 - long, -1 - short
        min_spred: int = 10,
        large_open: int = 100,
        large_close: int = 30,
        n_orders: int = 1,
        type_spred: int = 1,  # 0 - между bbid и bask, 1 - между large_open и large_close
        min_step: int = 1
    ) -> List[OrderCords]:
        """
        Формирует заявки для работы со спредом между крупными заявками
        
        Returns:
            List[OrderCords]: список заявок
        """
        orders = []
        
        # 1. Определяем места для заявок
        planned_orders = self._calculate_planned_orders(
            fg, direction, min_spred, large_open, large_close, 
            n_orders, type_spred, min_step
        )
        
        if not planned_orders:
            return [OrderCords(type_order='no_action')]
        
        # 2. Проверяем текущие заявки в стакане
        current_orders = self._get_current_order_positions(fg)
        
        # Определяем, какие заявки нужно снять
        reset_orders = self._get_reset_orders(current_orders, planned_orders)
        
        # Добавляем заявки на снятие
        if reset_orders:
            if len(reset_orders) == len(current_orders):
                # Все заявки не совпадают - снимаем все через reset_simple
                orders.append(OrderCords(
                    type_order='reset_simple',
                    is_open=False
                ))
            else:
                # Снимаем только конкретные заявки
                for y in reset_orders:
                    orders.append(OrderCords(
                        type_order='reset_cords',
                        y=y,
                        is_open=False
                    ))
            
            # Убираем снятые заявки из planned_orders
            planned_orders = [p for p in planned_orders if p[0] not in reset_orders]
        
        # 3. Добавляем оставшиеся заявки
        for order_info in planned_orders:
            y, is_open_side, is_close_side, is_best_price = order_info
            
            if is_close_side:
                # Заявка на закрытие
                if is_best_price:
                    # Если закрытие по лучшей цене
                    orders.append(OrderCords(
                        type_order='close_all_simple' if is_best_price else 'send_cords',
                        is_open=False
                    ))
                else:
                    orders.append(OrderCords(
                        type_order='send_cords',
                        y=y,
                        left_btn=not is_open_side,
                        press_z=True,
                        is_open=False
                    ))
            else:
                # Заявка на открытие
                if is_best_price:
                    # Если открытие по лучшей цене - используем send_simple
                    orders.append(OrderCords(
                        type_order='send_simple',
                        left_btn=is_open_side,  # True - покупка, False - продажа
                        is_open=True
                    ))
                else:
                    orders.append(OrderCords(
                        type_order='send_cords',
                        y=y,
                        left_btn=is_open_side,
                        is_open=True
                    ))
        
        return orders

    def _calculate_planned_orders(
        self,
        fg: pd.DataFrame,
        direction: int,
        min_spred: int,
        large_open: int,
        large_close: int,
        n_orders: int,
        type_spred: int,
        min_step: int
    ) -> List[Tuple[int, bool, bool, bool]]:
        """
        Вычисляет места для заявок
        
        Returns:
            List[Tuple[int, bool, bool, bool]]: [(y, is_open_side, is_close_side, is_best_price), ...]
            is_open_side: True - покупка, False - продажа
            is_close_side: True - заявка на закрытие
            is_best_price: True - заявка по лучшей цене (send_simple/close_all_simple)
        """
        planned = []
        
        # Получаем позиции крупных заявок в зависимости от type_spred
        if type_spred == 0:
            open_positions, close_positions = self._get_spred_positions_type0(fg, direction, large_open, large_close)
        else:
            open_positions, close_positions = self._get_spred_positions_type1(fg, direction, large_open, large_close)
        
        if not open_positions and not close_positions:
            return planned
        
        # Фильтруем позиции по min_spred
        if close_positions:
            filtered_open = []
            for open_y, open_side, is_best in open_positions:
                for close_y, close_side, _ in close_positions:
                    if abs(open_y - close_y) >= min_spred:
                        filtered_open.append((open_y, open_side, is_best))
                        break
            open_positions = filtered_open
        
        # Применяем min_step к позициям открытия
        open_positions = self._filter_by_min_step(open_positions, min_step)
        
        # Ограничиваем количество заявок на открытие
        open_positions = open_positions[:n_orders]
        
        # Если есть close_positions - берем только первую
        close_positions = close_positions[:1] if close_positions else []
        
        # Добавляем заявки на открытие
        for y, side, is_best in open_positions:
            planned.append((y, side, False, is_best))
        
        # Добавляем заявки на закрытие
        for y, side, is_best in close_positions:
            planned.append((y, side, True, is_best))
        
        return planned

    def _get_spred_positions_type0(
        self,
        fg: pd.DataFrame,
        direction: int,
        large_open: int,
        large_close: int
    ) -> Tuple[List[Tuple[int, bool, bool]], List[Tuple[int, bool, bool]]]:
        """
        Получает позиции для type_spred = 0 (между bbid и bask)
        
        Returns:
            (open_positions, close_positions)
            open_positions: [(y, is_buy, is_best_price), ...]
        """
        open_positions = []
        close_positions = []
        
        # Находим bbid
        bbid_mask = fg['type_cell'] == 'bbid'
        if bbid_mask.any():
            bbid_idx = fg[bbid_mask].index[0]
            bbid_y = fg.loc[bbid_idx, 'middle']
            
            # Находим bask
            bask_mask = fg['type_cell'] == 'bask'
            if bask_mask.any():
                bask_idx = fg[bask_mask].index[0]
                bask_y = fg.loc[bask_idx, 'middle']
                
                if direction == 0:
                    # Открытие на bbid - используем send_simple (лучшая цена)
                    open_positions.append((bbid_y, True, True))  # is_best_price = True
                    # Открытие на bask - используем send_simple
                    open_positions.append((bask_y, False, True))
                    
                    # Закрытие тоже по лучшей цене
                    # close_positions.append((bbid_y, True, True))  # пример
                    
                elif direction == 1:
                    open_positions.append((bbid_y, True, True))
                    
                else:  # direction == -1
                    open_positions.append((bask_y, False, True))
        
        return open_positions, close_positions

    def _get_spred_positions_type1(
        self,
        fg: pd.DataFrame,
        direction: int,
        large_open: int,
        large_close: int
    ) -> Tuple[List[Tuple[int, bool, bool]], List[Tuple[int, bool, bool]]]:
        """
        Получает позиции для type_spred = 1 (между large_open и large_close)
        """
        open_positions = []
        close_positions = []
        
        # Находим крупные ask
        ask_large_mask = (fg['type_cell'].isin(['ask', 'bask'])) & (fg['vol_per'] >= large_open)
        ask_large_indices = fg[ask_large_mask].index.tolist()
        
        # Находим крупные bid
        bid_large_mask = (fg['type_cell'].isin(['bid', 'bbid'])) & (fg['vol_per'] >= large_open)
        bid_large_indices = fg[bid_large_mask].index.tolist()
        
        # Находим крупные ask для закрытия
        ask_close_mask = (fg['type_cell'].isin(['ask', 'bask'])) & (fg['vol_per'] >= large_close)
        ask_close_indices = fg[ask_close_mask].index.tolist()
        
        # Находим крупные bid для закрытия
        bid_close_mask = (fg['type_cell'].isin(['bid', 'bbid'])) & (fg['vol_per'] >= large_close)
        bid_close_indices = fg[bid_close_mask].index.tolist()
        
        # Проверяем, является ли позиция лучшей ценой (bask или bbid)
        def is_best_price(fg, idx):
            row = fg.loc[idx]
            return row['type_cell'] in ['bask', 'bbid']
        
        if direction == 0:
            # Открытие лонга перед крупным ask
            for idx in ask_large_indices[:1]:
                y = self._get_order_y(fg, idx)
                if y is not None:
                    # Проверяем, не является ли это bask
                    is_best = is_best_price(fg, idx)
                    open_positions.append((y, True, is_best))
            
            # Открытие шорта перед крупным bid
            for idx in reversed(bid_large_indices[:1]):
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    open_positions.append((y, False, is_best))
            
            # Закрытие через large_close
            for idx in reversed(bid_close_indices[:1]):
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    close_positions.append((y, False, is_best))
            
            for idx in ask_close_indices[:1]:
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    close_positions.append((y, True, is_best))
        
        elif direction == 1:
            # Открытие лонга
            for idx in ask_large_indices[:1]:
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    open_positions.append((y, True, is_best))
            
            # Закрытие лонга
            for idx in reversed(bid_close_indices[:1]):
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    close_positions.append((y, False, is_best))
        
        else:  # direction == -1
            # Открытие шорта
            for idx in reversed(bid_large_indices[:1]):
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    open_positions.append((y, False, is_best))
            
            # Закрытие шорта
            for idx in ask_close_indices[:1]:
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = is_best_price(fg, idx)
                    close_positions.append((y, True, is_best))
        
        return open_positions, close_positions

    def _get_order_y(self, fg: pd.DataFrame, idx: int) -> Optional[int]:
        """Получает y-координату для установки заявки перед указанным индексом"""
        if idx is None or idx < 0 or idx >= len(fg):
            return None
        
        row = fg.loc[idx]
        
        # Если это bask или bbid - возвращаем None, чтобы использовать send_simple
        if row['type_cell'] in ['bask', 'bbid']:
            return None
        
        if row['type_cell'] in ['ask', 'bask']:
            prev_idx = idx - 1
            if prev_idx >= 0:
                return fg.loc[prev_idx, 'middle']
        else:
            next_idx = idx + 1
            if next_idx < len(fg):
                return fg.loc[next_idx, 'middle']
        
        return None

    def _get_current_order_positions(self, fg: pd.DataFrame) -> List[int]:
        """Получает y-координаты текущих заявок в стакане"""
        order_mask = fg['have_order'] == True
        if order_mask.any():
            return fg[order_mask]['middle'].tolist()
        return []

    def _get_reset_orders(
        self, 
        current_orders: List[int], 
        planned_orders: List[Tuple[int, bool, bool, bool]]
    ) -> List[int]:
        """Определяет, какие текущие заявки нужно снять"""
        if not current_orders:
            return []
        
        planned_y = [p[0] for p in planned_orders if p[0] is not None]
        reset_orders = [y for y in current_orders if y not in planned_y]
        
        return reset_orders

    def _filter_by_min_step(
        self, 
        positions: List[Tuple[int, bool, bool]], 
        min_step: int
    ) -> List[Tuple[int, bool, bool]]:
        """Фильтрует позиции по минимальному шагу"""
        if not positions or min_step <= 1:
            return positions
        
        # Сортируем по y
        sorted_positions = sorted(positions, key=lambda x: x[0])
        
        filtered = []
        last_y = None
        
        for y, side, is_best in sorted_positions:
            if last_y is None or abs(y - last_y) >= min_step:
                filtered.append((y, side, is_best))
                last_y = y
        
        return filtered