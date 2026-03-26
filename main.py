import datetime
import time
import os
import sys
from main_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import Qt, QTime
# from PySide6.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import random
import numpy as np

from OrdersLoader import OrdersLoader
from OrdersSelecter import OrdersSelecter
# from PriceChecker import PriceChecker
from TgBotStarter import TgBotStarter

MAX_LOGS_ROW = 300

if not os.path.exists('archive'):
    os.mkdir('archive')

if not os.path.exists('last_check_time.txt'):
    with open('last_check_time.txt', 'w') as f:
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if not os.path.exists('daily_check_time.txt'):
    with open('daily_check_time.txt', 'w') as f:
        f.write(f"18:00\n07:00\n18:00\n07:00\n18:00\n07:00")

# if not os.path.exists('price_last_check_time.txt'):
#     with open('price_last_check_time.txt', 'w') as f:
#         f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if not os.path.exists('letters ignore.txt'):
    with open('letters ignore.txt', 'w') as f:
        f.write('')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.OrdersLoader = OrdersLoader()
        self.OrdersSelecter = OrdersSelecter(self.dateEdit_1, self.dateEdit_2)
        self.TgBotStarter = TgBotStarter()
        # self.PriceChecker = PriceChecker()

        self.Logs_pushButton.setToolTip('Открыть файл с логами')
        self.Logs_pushButton_2.setToolTip('Открыть файл с логами')
        # self.Logs_pushButton_3.setToolTip('Открыть файл с логами')
        self.Logs_pushButton_4_.setToolTip('Открыть файл с логами')
        self.OpenFileFolderButton.setToolTip('Открыть папку с эксель файлом')
        self.Log_textBrowser.document().setMaximumBlockCount(MAX_LOGS_ROW)
        self.Log_textBrowser_2.document().setMaximumBlockCount(MAX_LOGS_ROW)
        # self.Log_textBrowser_3.document().setMaximumBlockCount(MAX_LOGS_ROW)
        self.Log_textBrowser_4.document().setMaximumBlockCount(MAX_LOGS_ROW)
        self.dateEdit_2.setDate(datetime.datetime.now())
        self.dateEdit_1.setDate(datetime.datetime.now() - datetime.timedelta(days=7))

        # self.Log_textBrowser.insertHtml()
        self.logs = [self.Log_textBrowser, self.Log_textBrowser_2, self.Log_textBrowser_4]  # self.Log_textBrowser_3,
        logs_txt = ['logs.log', 'logs_orders_selecter.log', 'tg_logs.log']  # 'price_logs.log',
        for i, lg in enumerate(logs_txt):
            with open(lg, 'r') as log_file:
                last_log_rows = log_file.readlines()[-MAX_LOGS_ROW:]
                if last_log_rows:
                    self.logs[i].append('\n'.join(l.replace('\n', '') for l in last_log_rows))

            self.logs[i].append("<hr><br>")

        try:
            with open('daily_check_time.txt', 'r') as f:
                times = f.read().split()
                # print(times)
                self.ozon_extra_col_timeEdit.setTime(QTime(*map(int, times[0].split(':'))))
                self.ozon_extra_col_timeEdit_2.setTime(QTime(*map(int, times[1].split(':'))))
                self.wb_extra_col_timeEdit.setTime(QTime(*map(int, times[2].split(':'))))
                self.wb_extra_col_timeEdit_2.setTime(QTime(*map(int, times[3].split(':'))))
                self.ya_extra_col_timeEdit.setTime(QTime(*map(int, times[4].split(':'))))
                self.ya_extra_col_timeEdit_2.setTime(QTime(*map(int, times[5].split(':'))))
        except:
            self.Log_textBrowser.append("Некорректное время в daily_check_time.txt")

        # try:
        #     with open('price_check_hours.txt', 'r') as f:
        #         hour = int(f.read())
        #         self.PriceUpdate_spinBox.setValue(hour)
        # except:
        #     self.Log_textBrowser_3.append("Некорректное значение в price_check_hours.txt")


        self.Start_Button.clicked.connect(self.main_loop)
        self.Pause_checkBox.checkStateChanged.connect(lambda s: self.set_pause_status(self.OrdersLoader, s))
        # self.Pause_checkBox_3.checkStateChanged.connect(lambda s: self.set_pause_status(self.PriceChecker, s))
        self.Logs_pushButton.clicked.connect(lambda: os.startfile(logs_txt[0]))
        self.Logs_pushButton_2.clicked.connect(lambda: os.startfile(logs_txt[1]))
        # self.Logs_pushButton_3.clicked.connect(lambda: os.startfile(logs_txt[2]))
        self.Logs_pushButton_4_.clicked.connect(lambda: os.startfile(logs_txt[2]))
        self.OpenArchiveDirButton.clicked.connect(lambda: os.startfile('archive'))
        self.OpenFileFolderButton.clicked.connect(lambda: os.startfile(''))
        self.OpenResButton.clicked.connect(lambda: os.startfile('Склад учёт.xlsx'))
        self.OpenPriceFileButton.clicked.connect(lambda: os.startfile('Цены заказов.xlsx'))
        self.OpenReportButton.clicked.connect(lambda: os.startfile('Потерянные артикулы.xlsx'))

        self.ozon_extra_col_timeEdit.timeChanged.connect(self.save_time)
        self.ozon_extra_col_timeEdit_2.timeChanged.connect(self.save_time)
        self.wb_extra_col_timeEdit.timeChanged.connect(self.save_time)
        self.wb_extra_col_timeEdit_2.timeChanged.connect(self.save_time)
        self.ya_extra_col_timeEdit.timeChanged.connect(self.save_time)
        self.ya_extra_col_timeEdit_2.timeChanged.connect(self.save_time)
        # self.extra_col_timeEdit.time()

        self.OrdersLoader.PauseSignal.connect(lambda _: self.set_pause_on(self.Pause_checkBox, self.Start_Button))
        self.OrdersLoader.LogAddSignal.connect(lambda i, t: self.log_add(i, t))
        self.OrdersLoader.SetBadArticleSignal.connect(lambda x: self.set_bad_article_count(x))
        self.OrdersLoader.SetApiDataSignal.connect(lambda x: self.ApiData_label.setText(x))

        self.OrdersSelecter.LogAddSignal.connect(lambda i, t: self.log_add(i, t))
        self.OrdersSelecter.OrdersSignal.connect(lambda x: self.show_graph(x))
        self.autoData_pushButton.clicked.connect(self.auto_select_date)

        self.Start_Button_2.clicked.connect(self.load_orders)

        # Price Checker
        # self.Start_Button_3.clicked.connect(self.price_checker_start)
        # self.PriceUpdate_spinBox.valueChanged.connect(self.save_price_time)
        # self.OpenPriceFileButton.clicked.connect(lambda _: os.startfile('Цены.xlsx'))
        # self.PriceChecker.LogAddSignal.connect(lambda i, t: self.log_add(i, t))
        # self.PriceChecker.PauseSignal.connect(lambda _: self.set_pause_on(self.Pause_checkBox_3, self.Start_Button_3))
        # self.PriceChecker.SetItemsSignal.connect(self.set_items_in_table)
        # self.PriceChecker.SetLastTimeUpdate.connect(lambda x: self.lastPriceUpdate_label.setText(f"Последнее обновлеие: {x}"))

        # self.price_model = QStandardItemModel()
        # self.price_model.setHorizontalHeaderLabels(['Артикул', 'Магазин', 'Изменение %', 'Ссылка'])
        # self.Price_tableView.setModel(self.price_model)
        # self.Price_tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        # TG bot
        self.Start_tg_Button_4.clicked.connect(self.tg_start)
        if os.path.exists('autostart_tg.txt'):
            self.tg_start()
        self.Stop_tg_Button_4.clicked.connect(self.tg_stop)

        self.TgBotStarter.RestartTgSignal.connect(lambda t: self.TgStatus_label.setText(t))
        self.TgBotStarter.LogAddSignal.connect(lambda i, t: self.log_add(i, t))

        self.canvas = QVBoxLayout(self.widget)


    def save_time(self):
        with open('daily_check_time.txt', 'w') as f:
            f.write(f"{self.ozon_extra_col_timeEdit.time().hour()}:{self.ozon_extra_col_timeEdit.time().minute()}\n"
                    f"{self.ozon_extra_col_timeEdit_2.time().hour()}:{self.ozon_extra_col_timeEdit_2.time().minute()}\n"
                    f"{self.wb_extra_col_timeEdit.time().hour()}:{self.wb_extra_col_timeEdit.time().minute()}\n"
                    f"{self.wb_extra_col_timeEdit_2.time().hour()}:{self.wb_extra_col_timeEdit_2.time().minute()}\n"
                    f"{self.ya_extra_col_timeEdit.time().hour()}:{self.ya_extra_col_timeEdit.time().minute()}\n"
                    f"{self.ya_extra_col_timeEdit_2.time().hour()}:{self.ya_extra_col_timeEdit_2.time().minute()}")
        # print(self.extra_col_timeEdit.time().hour(), self.extra_col_timeEdit.time().minute())

    # def save_price_time(self):
    #     with open('price_check_hours.txt', 'w') as f:
    #         f.write(str(self.PriceUpdate_spinBox.value()))

    def main_loop(self):
        if not self.OrdersLoader.isRunning():
            self.Start_Button.setEnabled(False)
            self.OrdersLoader.start()

    def load_orders(self):
        if not self.OrdersSelecter.isRunning():
            self.OrdersSelecter.start()

    # def price_checker_start(self):
    #     if not self.PriceChecker.isRunning():
    #         self.Start_Button_3.setEnabled(False)
    #         self.PriceChecker.start()


    # def set_items_in_table(self, items):
    #     # print(items)
    #     while self.price_model.rowCount() > 0:
    #         self.price_model.removeRow(self.price_model.rowCount() - 1)
    #
    #     for item in items:
    #         item = [QStandardItem(i) for i in item]
    #         self.price_model.appendRow(item)




    def tg_start(self):
        if not self.TgBotStarter.isRunning():
            # self.TgStatus_label.setText("Статус: <span style='color:#38b04c;'>Работает</span>")
            self.TgBotStarter.start()
        # self.thread = QThread()
        # self.worker = TgBotStarter()
        #
        # self.worker.moveToThread(self.thread)
        #
        # self.thread.started.connect(self.worker.start)
        # self.worker.finished.connect(self.thread.quit)
        #
        # self.thread.start()

    def tg_stop(self):
        # self.TgStatus_label.setText("Статус: <span style='font-weight:bold;'>Остановка...</span>")
        self.TgBotStarter.stop()
        # self.worker.stop()
        # self.TgStatus_label.setText("Статус: <span style='color:#eb712a;'>Остановлен</span>")


    def auto_select_date(self):
        self.dateEdit_2.setDate(datetime.datetime.now())
        self.dateEdit_1.setDate(datetime.datetime.now() - datetime.timedelta(days=7))

    def set_pause_status(self, module_obj, status):
        module_obj.isPause = status == Qt.CheckState.Checked

    def set_pause_on(self, Pause_CB, Start_btn):
        Pause_CB.setChecked(False)
        Start_btn.setEnabled(True)

    def set_bad_article_count(self, x):
        x = x and f"<span style='font-weight:bold;color:red;'>{x}</span>"
        self.BadArticleCountLabel.setText(f"Потерянные артикулы: {x}")

    def show_graph(self, order_list):
        # print(order_list)
        fig = plt.figure()
        # plt.plot([random.randrange(1,10) for _ in range(5)])
        # x = np.random.randint(-10, 10, 55)
        # x2 = np.random.randint(-10, 10, 55)
        # x1 = np.random.randint(-10, 10, 55)
        # x2 = np.random.randint(-10, 10, 55)
        # w = 0.5
        # plt.bar(3, height=3, width=w)
        # plt.bar(5, height=5, width=w)
        # id = 0
        # for color, name, val in order_list:
        #     name = str(name).replace('[ozon]', '-').replace('[wb]', '=')
        #     plt.bar(name, height=val, color=color)
        #     plt.plot(id, val)
        #     id += 1
        # plt.bar("[ozon] м1", height=12, color='#444')
        # plt.barh('[wb] м1', width=15)
        # plt.barh('[ozon] м2', width=8)
        # plt.barh('[wb] м2', width=13)
        # labels = ['[ozon] м1', '[ozon] м2', '[ozon] м3', '[wb] м1', '[wb] м2', '[wb] м3']
        # values = [random.randrange(1,20) for _ in range(len(labels))]
        # colors = ['#48a7f0', '#48a7f0', '#48a7f0', '#d377f7', '#d377f7', '#d377f7']
        labels = [o[0] for o in order_list]
        values = [o[1] for o in order_list]
        colors = [o[2] for o in order_list]
        total = sum(values)
        # print(colors)
        # print(labels)
        # print(values)
        plt.pie(values, labels=labels, autopct=lambda x: '{:.0f}'.format(x*total/100), explode=[0.07] * len(labels), colors=colors)
        # plt.plot(0, 12, 'r--o')
        # self.widget.updateGeometry()
        # self.widget.
        # plt.xticks(rotation=25)
        self.canvas.takeAt(0)
        self.canvas.addWidget(FigureCanvasQTAgg(fig))


    def log_add(self, log_id, txt):
        self.logs[log_id].append(f"{txt}")
    # def log(self, text, error=False, html_msg=None):
    #     if error:
    #         logger.error(f"ERROR: {text}")
    #         self.Log_textBrowser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
    #                                     f"<span style='color:red;font-weight:bold;'>{text}</span><br>")
    #     elif html_msg:
    #         logger.log(21, f"{text}")
    #         self.Log_textBrowser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {html_msg}")
    #     else:
    #         logger.log(21, f"{text}")
    #         self.Log_textBrowser.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")




def app_start():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    # main()
    app_start()
    # from fdo
