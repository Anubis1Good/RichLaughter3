from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
# import numpy as np

@dataclass
class OrderCords:
    """
    type_order:
        'send_cords' - отправляет заявку в определенные координаты в стакане
        'send_simple' - отправяет заявку по лучшей цене
        'send_smart' - отправляет заявку по лучшей цене перед заявкой больше smart_per
        'reset_cords' - снимает заявку в определенных координатах
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

    def __str__(self):
        return f"{self.type_order}, y={self.y}, lb={self.left_btn}, pf={self.press_f}, pz={self.press_z}"


class OrderManager:
    def __init__(self):
        pass

    def translate_old_action(self,action,smart_per=10,idx_chart=0):
        new_actions = []
        if action is not None:
            if 'open' in action:
                if 'long' in action:
                    new_actions.append(OrderCords(type_order='send_smart',press_f=True,smart_per=smart_per,idx_chart=idx_chart))
                elif 'short' in action:
                    new_actions.append(OrderCords(type_order='send_smart',press_f=True,smart_per=smart_per,idx_chart=idx_chart,left_btn=False))
                elif 'all' in action:
                    new_actions.append(OrderCords(type_order='send_smart',press_f=True,smart_per=smart_per,idx_chart=idx_chart))
                    new_actions.append(OrderCords(type_order='send_smart',press_f=False,smart_per=smart_per,idx_chart=idx_chart,left_btn=False))
            elif 'close' in action:
                if 'long' in action:
                    new_actions.append(OrderCords(type_order='send_smart',press_f=True,smart_per=smart_per,idx_chart=idx_chart,left_btn=False,is_open=False,press_z=True))
                elif 'short' in action:
                    new_actions.append(OrderCords(type_order='send_smart',press_f=True,smart_per=smart_per,idx_chart=idx_chart,left_btn=True,is_open=False,press_z=True))
                elif 'all' in action:
                    new_actions.append(OrderCords(type_order='send_smart',press_f=True,smart_per=smart_per,idx_chart=idx_chart,left_btn=False,is_open=False,press_z=True))
                    new_actions.append(OrderCords(type_order='send_smart',press_f=False,smart_per=smart_per,idx_chart=idx_chart,left_btn=True,is_open=False,press_z=True))
        else:
            new_actions.append(OrderCords(type_order='no_action'))
        return new_actions

    def get_spred_orders(
        self,
        fg: pd.DataFrame,
        direction: int = 0,  # 0 - both, 1 - long, -1 - short
        min_spred: int = 10,
        large_open: int = 100,
        large_close: int = 30,
        n_orders: int = 1,
        min_step: int = 1,
        chart_idx: int = 0,
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
            n_orders, min_step
        )
        
        if not planned_orders:
            return [OrderCords(type_order='no_action')]
        
        # 2. Проверяем текущие заявки в стакане
        current_orders = self._get_current_order_positions(fg)

        # Определяем, какие заявки нужно снять, а какие оставить
        reset_orders, keep_orders = self._get_reset_orders(current_orders, planned_orders)

        # Добавляем заявки на снятие
        if reset_orders:
            if len(reset_orders) == len(current_orders):
                orders.append(OrderCords(type_order='reset_simple', is_open=False))
            else:
                for y in reset_orders:
                    orders.append(OrderCords(type_order='reset_cords', y=y, is_open=False))

        # Убираем из planned_orders те, что уже есть в current_orders (их не нужно выставлять)
        planned_orders = [p for p in planned_orders if p[0] not in keep_orders]
        
        # 3. Добавляем оставшиеся заявки
        for order_info in planned_orders:
            y, is_buy, is_close, is_best_price = order_info
            
            if is_close:
                # Заявка на закрытие
                orders.append(OrderCords(
                    type_order='send_simple' if is_best_price else 'send_cords',
                    y=y,
                    left_btn=is_buy,
                    press_z=True,
                    is_open=False,
                    idx_chart=chart_idx
                ))

            else:
                # Заявка на открытие
                orders.append(OrderCords(
                    type_order='send_simple' if is_best_price else 'send_cords',
                    y=y,
                    left_btn=is_buy,
                    is_open=True,
                    idx_chart=chart_idx
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
        min_step: int
    ) -> List[Tuple[int, bool, bool, bool]]:
        """
        Вычисляет места для заявок
        
        Returns:
            List[Tuple[int, bool, bool, bool]]: [(y, is_buy, is_close, is_best_price), ...]
            is_buy: True - покупка, False - продажа
            is_close: True - заявка на закрытие
            is_best_price: True - заявка по лучшей цене (send_simple/close_all_simple)
        """
        planned = []
        
        # Получаем позиции крупных заявок в зависимости от type_spred
        open_positions, close_positions = self._get_spred_positions(fg, direction, large_open, large_close,n_orders,min_step,min_spred)
        
        if not open_positions and not close_positions:
            return planned
        
        # Добавляем заявки на открытие
        for y, is_buy, is_best, _ in open_positions:
            planned.append((y, is_buy, False, is_best))
        
        # Добавляем заявки на закрытие
        for y, is_buy, is_best, _ in close_positions:
            planned.append((y, is_buy, True, is_best))
        
        return planned

    def _is_best_price(self, fg: pd.DataFrame, idx: int) -> bool:
        """Проверяет, является ли позиция лучшей ценой (bask или bbid)"""
        if idx is None or idx < 0 or idx >= len(fg):
            return False
        row = fg.loc[idx]
        return row['type_cell'] in ['bask', 'bbid']
    
    def _get_spred_positions(
        self,
        fg: pd.DataFrame,
        direction: int,
        large_open: int,
        large_close: int,
        n_orders: int,
        min_step: int,
        min_spred:int
    ) -> Tuple[List[Tuple[int, bool, bool]], List[Tuple[int, bool, bool]]]:
        """
        Получает позиции (между large_open и large_close) с учетом min_step
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
        
        # Получаем close_idx (ближайшую к спреду заявку на закрытие)
        close_idx_ask = max(ask_close_indices) if ask_close_indices else None
        close_idx_bid = min(bid_close_indices) if bid_close_indices else None

        # Фильтруем ask индексы по min_spred (отбрасываем слишком близкие к close)
        if direction <= 0:
            if close_idx_bid is not None:
                ask_large_indices = [idx for idx in ask_large_indices if abs(idx - close_idx_bid) >= min_spred]
            # Фильтруем по min_step
            ask_large_indices = self._filter_indices_by_min_step(ask_large_indices, min_step, reverse=True)
            # Ограничиваем количество
            ask_large_indices = ask_large_indices[:n_orders]
        
        if direction >= 0:
            if close_idx_ask is not None:
                bid_large_indices = [idx for idx in bid_large_indices if abs(idx - close_idx_ask) >= min_spred]
            # Фильтруем по min_step
            bid_large_indices = self._filter_indices_by_min_step(bid_large_indices, min_step, reverse=False)
            # Ограничиваем количество
            bid_large_indices = bid_large_indices[:n_orders]
        
        # Аналогично для close индексов (их фильтруем только по min_step, без min_spred)
        ask_close_indices = self._filter_indices_by_min_step(ask_close_indices, min_step, reverse=True)[:1]
        bid_close_indices = self._filter_indices_by_min_step(bid_close_indices, min_step, reverse=False)[:1]
        
        # Формируем позиции
        if direction == 0 or direction == 1:
            # Открытие лонга - покупаем по bid (левая кнопка)
            for idx in bid_large_indices:  # <-- должно быть bid, а не ask!
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = self._is_best_price(fg, idx)
                    open_positions.append((y, True, is_best,idx))
            
            # Закрытие лонга - продаем по ask (правая кнопка)
            for idx in ask_close_indices:  # <-- должно быть ask, а не bid!
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = self._is_best_price(fg, idx)
                    close_positions.append((y, False, is_best,idx))

        if direction == 0 or direction == -1:
            # Открытие шорта - продаем по ask (правая кнопка)
            for idx in ask_large_indices:  # <-- должно быть ask, а не bid!
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = self._is_best_price(fg, idx)
                    open_positions.append((y, False, is_best,idx))
            
            # Закрытие шорта - покупаем по bid (левая кнопка)
            for idx in bid_close_indices:  # <-- должно быть bid, а не ask!
                y = self._get_order_y(fg, idx)
                if y is not None:
                    is_best = self._is_best_price(fg, idx)
                    close_positions.append((y, True, is_best,idx))

        return open_positions, close_positions


    def _filter_indices_by_min_step(
        self,
        indices: List[int],
        min_step: int,
        reverse: bool = False
    ) -> List[int]:
        """
        Фильтрует индексы по минимальному шагу (в пунктах)
        
        Args:
            indices: список индексов
            min_step: минимальный шаг в пунктах
            reverse: True - сортировка от большего к меньшему (для ask),
                    False - сортировка от меньшего к большему (для bid)
        """
        if not indices or min_step <= 1:
            return indices
        
        # Сортируем индексы
        indices_sorted = sorted(indices, reverse=reverse)
        
        filtered = []
        last_idx = None
        
        for idx in indices_sorted:
            if last_idx is None or abs(idx - last_idx) >= min_step:
                filtered.append(idx)
                last_idx = idx
        
        return filtered

    def _get_order_y(self, fg: pd.DataFrame, idx: int) -> Optional[int]:
        """Получает y-координату для установки заявки перед указанным индексом"""
        if idx is None or idx < 0 or idx >= len(fg):
            return None
        
        row = fg.loc[idx]
        
        # Если это bask или bbid - возвращаем None, чтобы использовать send_simple
        if row['type_cell'] in ['bask', 'bbid']:
            return row['middle']
        
        if row['type_cell'] in ['ask']:
            next_idx = idx + 1
            if next_idx < len(fg):
                return fg.loc[next_idx, 'middle']
        else:
            prev_idx = idx - 1
            if prev_idx >= 0:
                return fg.loc[prev_idx, 'middle']
        
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
    ) -> Tuple[List[int], List[int]]:
        """
        Определяет, какие текущие заявки нужно снять, а какие оставить
        
        Returns:
            (reset_orders, keep_orders)
            reset_orders: заявки, которые нужно снять
            keep_orders: заявки, которые уже стоят и совпадают с planned
        """
        if not current_orders:
            return [], []
        
        planned_y = [p[0] for p in planned_orders]
        
        reset_orders = []   # заявки, которые нужно снять (есть в current, нет в planned)
        keep_orders = []    # заявки, которые нужно оставить (есть и в current, и в planned)
        
        for y in current_orders:
            if y in planned_y:
                keep_orders.append(y)
            else:
                reset_orders.append(y)
        
        return reset_orders, keep_orders

