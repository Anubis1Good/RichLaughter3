import shutil
import keyboard
import cv2
import pyautogui as pag
import numpy as np
import json
from PyQt5.QtCore import QThread, pyqtSignal,QMutex
from traders.VT.VT7 import VT7 as VT
from traders.VT.sgs import stock_groups
from traders.VT.utils import get_configuration_traiders

error_folder = '_logs\error_logsVT'


class TradeWorker(QThread):
    update_signal = pyqtSignal(str)
    def __init__(self, sg_key,file):
        super().__init__()
        self.sg_key = sg_key  # Сохраняем параметры
        self.file  = file
        self._active = True  # Дополнительный флаг контроля
        self._lock = QMutex()  # Для thread-safe операций

    def stop(self):
        self._lock.lock()
        self._active = False
        self._lock.unlock()
        self.requestInterruption()

    def get_full_config(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            raw_pages = {}
            unique_pages = {}
            for raw_page in data:
                raw_pages[raw_page] = get_configuration_traiders(data, raw_page)
                if raw_page != 'base':
                    pages = raw_page.split('_')
                    for page in pages:
                        unique_pages[int(page)] = raw_page
            return raw_pages,unique_pages

    def run(self,):
        try:
            shutil.rmtree(error_folder)
        except Exception as e:
            pass
        self.work_traders:list[VT] = []
        sg = stock_groups[self.sg_key]
        raw_pages,unique_pages = self.get_full_config()
        # print(raw_pages)
        # print(unique_pages)
        for idx,s in enumerate(sg):
            if idx in unique_pages:
                conf_data = raw_pages[unique_pages[idx]]
            else:
                conf_data = raw_pages['base']
            trader = VT(conf_data,s)
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

            img = np.array(pag.screenshot()) 
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            # cv2.imwrite('test.png',img)
            wt.run(img)
            if keyboard.is_pressed('Esc'):
                print("\nyou pressed Esc, so exiting...")
                self.requestInterruption()  # Устанавливаем флаг прерывания
                return  # Выходим из цикла
                # sys.exit(0)
            keyboard.send('tab') 
            if self.isInterruptionRequested():
                return


