import shutil
# import os
# import sys
import keyboard
import cv2
import pyautogui as pag
import numpy as np
# from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal,QMutex
# from Traders.VT.VT5 import VT5
from traders.VT.VT7 import VT7 as VT
from traders.VT.bot_on_ticker import init_trader
from traders.VT.sgs import stock_groups

error_folder = '_logs\error_logsVT'


class TradeWorker(QThread):
    update_signal = pyqtSignal(str)
    def __init__(self, sg_key,param_bots,file_istxt,price_step):
        super().__init__()
        self.sg_key = sg_key  # Сохраняем параметры
        self.price_step = price_step
        self.param_bots = param_bots
        self.grid = not file_istxt
        self._active = True  # Дополнительный флаг контроля
        self._lock = QMutex()  # Для thread-safe операций
    def stop(self):
        self._lock.lock()
        self._active = False
        self._lock.unlock()
        self.requestInterruption()

    def run(self,):
        try:
            shutil.rmtree(error_folder)
        except Exception as e:
            pass
        if self.grid:
            self.work_traders:list[list[VT]]=[]
        else:
            self.work_traders:list[VT] = []
        sg = stock_groups[self.sg_key]
            
        for s in sg:
            if self.grid:
                traders = []
                for i in range(len(s)):
                    ws,close18 = init_trader(s[i])
                    glass:tuple = self.param_bots[0+5*i]
                    chart:tuple = self.param_bots[1+5*i]
                    position:tuple = self.param_bots[2+5*i]
                    tape:tuple = self.param_bots[3+5*i]
                    cluster:tuple = self.param_bots[4+5*i]
                    price_step = self.price_step
                    trader = VT(glass,chart,position,tape,cluster,price_step,s[i],ws)
                    traders.append(trader)
                self.work_traders.append(traders)
            else:
                ws,close18 = init_trader(s)
                # if self.sg_key == 'TS':
                #     s = s[:-1]
                trader = VT(*self.param_bots,s,ws)
                self.work_traders.append(trader)
        self.msleep(3000)
        while not self.isInterruptionRequested():
            self._lock.lock()
            active = self._active
            self._lock.unlock()
            
            if not active:
                break
            self.execute_trade_cycle()
            self.msleep(50)

    def execute_trade_cycle(self):
        for wt in self.work_traders:
            for _ in range(20):  # 20 * 100мс = 2 секунды
                if self.isInterruptionRequested():
                    return
                self.msleep(100)
            if self.isInterruptionRequested():
                return
            keyboard.send('shift')
            if self.isInterruptionRequested():
                return
            # pag.screenshot('Traders\VT\Screen.png')
            # img = cv2.imread('Traders\VT\Screen.png')
            # if self.grid:
            #     for _wt in wt:
            #         _wt._reset_draw_chart()
            # else:
            #     wt._reset_draw_chart()
            img = np.array(pag.screenshot()) 
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            # cv2.imwrite('test.png',img)
            if self.grid:
                for _wt in wt:
                    _wt.run(img)
                    pag.moveTo(_wt.glass_region[0]+10,_wt.glass_region[1]+10)
            else:
                wt.run(img)
                pag.moveTo(wt.glass_region[0]+10,wt.glass_region[1]+10)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                self.requestInterruption()  # Устанавливаем флаг прерывания
                return  # Выходим из цикла
                # sys.exit(0)
            keyboard.send('tab') 
            if self.isInterruptionRequested():
                return


