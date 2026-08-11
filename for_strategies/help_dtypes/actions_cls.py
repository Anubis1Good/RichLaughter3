from dataclasses import dataclass

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
    """
    type_order:str # 'send_cords','reset_cords','send_simple','send_smart','reset_simple', 'close_all_simple', 'close_all_smart'
    y:int=None #150
    left_btn:bool=True
    press_f:bool=False
    press_z:bool=False
    is_open:bool = True
    smart_per:int = 50
    idx_chart:int = 0