import numpy as np

class ColorsBtnBGR:
    ask = (67, 67, 67) #top
    bid = (76, 76, 76) #bottom
    best_ask = (101, 82, 168) #and short pos
    best_bid = (100, 117, 66) #and long pos
    best_ask_level = (136,80,162)
    best_bid_level = (135,103,96)
    
    large_value_1 = (198, 140, 48)
    large_value_2 = (178, 201, 45)
    large_value_1_level = (199,118,84)
    large_value_2_level = (186,158,82)

    color_x = (9,0,255)
    color_x_shadow = (11,11,175)
    color_x_bb = (0,0,255)

    cur_price_1 = (96,118,50)
    cur_price_2 = (75,75,173)

    candle_color_1 = (111,111,111)
    candle_color_2 = (200,200,200)

    volume_color_1 = (92,107,61)
    volume_color_2 = (89,89,128)

    ask_level_1 = (114,71,97)
    bid_level_1 = (119,76,102)

    level_shift_1 = (105,62,88)

    loss_glass = (45,45,186)
    profit_glass = (85,112,30)
    pos_price = (103,74,50)

    z_tape = (118,118,118)


class TemplateCandle:
    candle_top = np.array([
        [0,0,0],
        [0,255,0]
    ],dtype=np.uint8)

    candle_bottom = np.array([
        [0,255,0],
        [0,0,0]
    ],dtype=np.uint8)
    
    candle_close = np.array([
        [0,0],
        [255,0],
        [0,0],
    ],dtype=np.uint8)

    candle_open = np.array([
        [0,0],
        [0,255],
        [0,0],
    ],dtype=np.uint8)

    volume_top = np.array([
        [0,0,0,0],
        [0,255,255,0]
    ],dtype=np.uint8)