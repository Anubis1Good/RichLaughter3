import cv2
from traders.VT.settingsPB import ColorsBtnBGR

img = cv2.imread('_data_for_tests\screens\planks2.png')
color = ColorsBtnBGR.price_limit_ask
mask = cv2.inRange(img,color,color)

cv2.imshow('mask',mask)
cv2.waitKey(0)