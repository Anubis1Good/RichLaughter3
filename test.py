import keyboard
import numpy as np
import pyautogui as pag
import cv2
from time import sleep
sleep(3)
img2 = np.array(pag.screenshot()) 
img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2BGR)
cv2.imwrite('_logs\_test_imgs\_before.png',img2)
keyboard.send('tab')
sleep(0.5)
img = np.array(pag.screenshot()) 
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
cv2.imwrite('_logs\_test_imgs\_after.png',img)