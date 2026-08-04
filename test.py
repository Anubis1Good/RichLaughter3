# import cv2
# from traders.VT.settingsPB import ColorsBtnBGR

# img = cv2.imread('_data_for_tests\screens\Screenshot_52.png')
# color = ColorsBtnBGR.color_x_shadow
# # color = (0,0,255)
# mask = cv2.inRange(img,color,color)

# cv2.imshow('mask',mask)
# cv2.waitKey(0)

import pandas as pd
import matplotlib.pyplot as plt
from for_strategies.zigzag_indicators import add_dzz_peaks


df = pd.read_parquet('_data_for_tests\data_stock_1m\MTLR_1_1785854631.parquet')

