from dataclasses import dataclass

@dataclass
class OrderCords:
    type_order:str # 'send','reset'
    y:int #150
    left_btn:bool
    press_f:bool
    press_z:bool