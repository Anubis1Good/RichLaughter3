import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication,QWidget,QListWidget,QPushButton,QHBoxLayout,QVBoxLayout,QLabel

from traders.VT.utils import get_pages,get_configuration_traiders
from traders.VT.sgs import stock_groups
from traders.VT.tradeVTs import TradeWorker

lines = []
class Overlay(QWidget):
    def __init__(self,conf_data):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |  # Поверх всех окон
            Qt.FramelessWindowHint |   # Без рамки
            Qt.Tool                    # Не показывать в панели задач
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # Прозрачный фон
        self.setGeometry(0, 0, QApplication.desktop().screenGeometry().width(), 
                        QApplication.desktop().screenGeometry().height())
        self.conf_data = conf_data
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Более контрастные цвета для dom'ов
        dom_style = [
            ('clusters', QColor(255, 50, 50)),    # Ярко-красный
            ('tapes', QColor(255, 165, 0)),       # Оранжевый
            ('glasses', QColor(50, 200, 50)),     # Зеленый
            ('poses', QColor(50, 150, 255))       # Синий
        ]
        
        for dom in self.conf_data['doms']:
            for key, color in dom_style:
                if key in dom:
                    painter.setPen(QPen(color, 1))
                    for x1, y1, x2, y2 in dom[key]:
                        painter.drawRect(x1, y1, x2-x1, y2-y1)
        
        for i, chart in enumerate(self.conf_data['charts']):
            hue = (i * 45) % 360  # Шаг 45 градусов: 0, 45, 90, 135, 180, 225, 270, 315
            color = QColor.fromHsv(hue, 200, 200)  # Насыщенность 200, яркость 200
            painter.setPen(QPen(color, 1))
            for x1, y1, x2, y2 in chart:
                painter.drawRect(x1, y1, x2-x1, y2-y1)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('StartVT')
        self.main_layout = QHBoxLayout()
        self.resize(700,500)
        self.setStyleSheet("""
            QWidget {
                background-color: #5CCDC9;
            }
            QListWidget {
                background-color: #FFFFFF;
                border-radius: 5px;
                border: none;

            }
            QListWidget::item {
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 5px;
                margin: 2px;
                background-color: #009B95;
            }
            
            QListWidget::item:selected {
                background-color: #A6A600;;
                border: 1px solid #999;
            }
            QListWidget::item:hover {
                background-color: #6C0AAB;
                border: 1px solid #999;
            }
            QLabel {
                background-color: #009B95;
                qproperty-alignment: 'AlignCenter';
                border-radius: 5px;
                color: white;
                font-size:18px;
            }
            QPushButton {
                background-color: #006561;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size:18px;
            }
            QPushButton:hover {
                background-color: #6C0AAB;
            }
            QPushButton:pressed {
                background-color: #A6A600;
            }
        """)
        self.init_btn_style = """
            QPushButton {
                background-color: #006561;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size:18px;
            }
            QPushButton:hover {
                background-color: #6C0AAB;
            }
            QPushButton:pressed {
                background-color: #A6A600;
            }
        """
        line1 = QVBoxLayout()
        line2 = QVBoxLayout()

        self.list_config = QListWidget()
        self.list_sgs = QListWidget()
        self.list_pages = QListWidget()
        self.config_folder = 'traders\VT\configsVT'
        configs = os.listdir(self.config_folder)
        self.cur_config = configs[0]
        self.list_config.addItems(configs)
        self.list_sgs.addItems(stock_groups)
        self.list_config.setCurrentRow(0)
        self.list_sgs.setCurrentRow(0)
        self.get_pages_config()
        line1.addWidget(self.list_config)
        line1.addWidget(self.list_sgs)
        line1.addWidget(self.list_pages)

        self.cur_sg = tuple(stock_groups.keys())[0]
        self.config_lbl = QLabel(text=self.cur_config)
        self.sg_lbl = QLabel(text=self.cur_sg)
        self.trader_btn = QPushButton(text='StartTrade')
        self.stop_btn = QPushButton(text='StopTrade')
        self.draw_btn = QPushButton(text='DrawWindow')

        line2.addWidget(self.config_lbl)
        line2.addWidget(self.sg_lbl)
        line2.addWidget(self.trader_btn)
        line2.addWidget(self.stop_btn)
        line2.addWidget(self.draw_btn)

        self.main_layout.addLayout(line1,stretch=1)
        self.main_layout.addLayout(line2,stretch=2)
        self.setLayout(self.main_layout)

        self.overlay = None
        self.worker = None

        self.list_config.itemClicked.connect(self.set_config)
        self.list_sgs.itemClicked.connect(self.set_sg)
        self.list_pages.itemClicked.connect(self.set_cur_page)
        self.draw_btn.clicked.connect(self.show_overlay)
        self.trader_btn.clicked.connect(self.toggle_worker)
        self.stop_btn.clicked.connect(self.stop_worker)

    def toggle_worker(self):
        if self.worker and self.worker.isRunning():
            pass
        else:
            file = os.path.join(self.config_folder, self.cur_config)
            lines,price_step= get_configuration_traiders(file)

            self.worker = TradeWorker(self.cur_sg, lines,False,price_step)

            self.worker.finished.connect(self.on_worker_finished)
            self.worker.start()
            print('Trading start')
            self.trader_btn.setText("Trade...")
            self.trader_btn.setStyleSheet('background-color: #A6A600;')
            self.stop_btn.setStyleSheet('background-color: #AA67D5;')
            self.trader_btn.setDisabled(True)

    def on_worker_finished(self):
        """Вызывается при завершении потока"""
        self.trader_btn.setText("StartTrade")
        self.trader_btn.setStyleSheet(self.init_btn_style)
        self.stop_btn.setStyleSheet(self.init_btn_style)
        self.trader_btn.setDisabled(False)
        print('Trading has been stopped')

    def stop_worker(self):
        if self.worker and self.worker.isRunning():
            self.worker.requestInterruption()
            self.worker.quit()
            self.worker.wait(2000)  # Таймаут 2 секунды
    
    def closeEvent(self, event):
        self.stop_worker()
        event.accept()

    def set_config(self):
        self.cur_config = self.list_config.currentItem().text()
        self.config_lbl.setText(self.cur_config)
        self.get_pages_config()

    def set_sg(self):
        self.cur_sg = self.list_sgs.currentItem().text()
        self.sg_lbl.setText(self.cur_sg)

    def set_cur_page(self):
        self.cur_page = self.list_pages.currentItem().text()
        if self.overlay:
            self.overlay.close()
            self.overlay = None 
            self.show_overlay()

    def get_pages_config(self):
        file = os.path.join(self.config_folder, self.cur_config)
        pages = get_pages(file)
        self.list_pages.clear()
        self.list_pages.addItems(pages)
        self.list_pages.setCurrentRow(0)
        self.cur_page = pages[0]

    def show_overlay(self):
        file = os.path.join(self.config_folder,self.cur_config)
        conf_data = get_configuration_traiders(file,self.cur_page)
            
        if not self.overlay:
            self.draw_btn.setText('StopDraw')
            self.draw_btn.setStyleSheet('background-color: #A6A600;')
            self.overlay = Overlay(conf_data)
            self.overlay.show()
        else:
            self.draw_btn.setText('DrawWindow')
            self.overlay.close()
            self.overlay = None 
            self.draw_btn.setStyleSheet(self.init_btn_style)

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()