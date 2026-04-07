import json
import requests
import datetime
import time
import traceback
from zoneinfo import ZoneInfo
import locale
import copy
import os
import re
import shutil
import pandas as pd
import openpyxl
from PySide6.QtCore import QThread, Signal
# from PySide6.QtGui import QTextCursor

from utils import get_api_keys, GetApiKeysException, get_letters_ignore

import logging
from logging.handlers import RotatingFileHandler

locale.setlocale(locale.LC_ALL, "ru")

logger = logging.getLogger('logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
# s_handler = logging.StreamHandler()
# s_handler.setFormatter(formater)
logger.addHandler(f_handler)
# logger.addHandler(s_handler)

OZON_URL = r'https://api-seller.ozon.ru'
WB_URL = r'https://common-api.wildberries.ru'
YA_URL = r'https://api.partner.market.yandex.ru'

# exception_letters = ('q', 'z', 'x', 'y', 'Q', 'Z', 'X', 'Y', 'х', 'Х', 'у', 'У')

# headers = {
#     "Host": "api-seller.ozon.ru",
#     'Client-Id': CLIENT_ID,
#     'Api-Key': API_KEY,
#     'Content-Type': 'application/json'
# }

class OrdersLoader(QThread):
    PauseSignal = Signal(bool)
    LogAddSignal = Signal(int, str)
    SetBadArticleSignal = Signal(int)
    SetApiDataSignal = Signal(str)
    Set = Signal(str)
    isPause = False
    wait_sec = 10

    def __init__(self):
        QThread.__init__(self)
        # self.log_tb = log

    def run(self):
        self.log('Старт')

        while not self.isPause:
            start_cycle_time = datetime.datetime.now()
            try:
                with open('last_check_time.txt', 'r') as fr:
                    last_check_time = datetime.datetime.strptime(fr.read(), '%Y-%m-%d %H:%M:%S')

                if self.update_table(last_check_time):
                    if last_check_time.date() != datetime.datetime.now().date():
                        self.API_KEYS = get_api_keys()
                        self.set_token_date_to()
                        self.del_files_from_archive()

            except GetApiKeysException:
                self.log("Ошибка при считывании API токенов. Проверьте config.txt", html_msg="<span style='color:red;'>Ошибка при считывании API токенов. Проверьте config.txt</span>")
                time.sleep(60)
            except OzonApiResponseException:
                self.log("Ozon API не отвечает", html_msg="<span style='color:#eb712a;'>Ozon API не отвечает</span>")
                time.sleep(60)
            except WbApiResponseException:
                self.log("WB API не отвечает", html_msg="<span style='color:#eb712a;'>WB API не отвечает</span>")
                time.sleep(60)
            except YndxApiResponseException:
                self.log("Yandex API не отвечает", html_msg="<span style='color:#eb712a;'>Yandex API не отвечает</span>")
                time.sleep(60)
            except Exception as ex:
                ex_text = traceback.format_exc()
                self.log(ex_text, error=True)
                time.sleep(60)

            finish_cycle_time = datetime.datetime.now()
            if self.wait_sec > (finish_cycle_time - start_cycle_time).seconds:
                for _ in range(self.wait_sec - (finish_cycle_time - start_cycle_time).seconds):
                    if self.isPause:
                        break
                    time.sleep(1)
        else:
            self.log('Пауза')
            self.PauseSignal.emit(True)


    def update_table(self, last_check_time):
        self.cur_time = datetime.datetime.now()
        # if cur_time.hour <= 0:
        #     return

        # if cur_time.date() == last_check_time.date():
        #     return False

        if self.cur_time.date() == last_check_time.date() and self.cur_time.hour == last_check_time.hour:
            return False

        if self.excel_is_open():
            return False

        self.API_KEYS = get_api_keys()

        if not self.API_KEYS.get('OZON_KEYS') and not self.API_KEYS.get('WB_KEYS'):
            self.log("Не указаны API токены. Проверьте config.txt",
                     html_msg="<span style='color:red;'>Не указаны API токены. config.txt</span>")
            return False

        self.last_check_date = last_check_time  #.date()
        self.cur_check_datetime = datetime.datetime.now(tz=ZoneInfo('Europe/Moscow'))

        # yesterday = (datetime.datetime.now().date() - datetime.timedelta(days=1)).strftime('%d.%m.%Y (%a)')

        self.log(f'Загрузка данных начиная с {self.last_check_date} ...', html_msg=f"Загрузка данных начиная с <span style='font-weight:bold;'>{self.last_check_date}</span> ...")
        # dateFrom = datetime.datetime(year=self.last_check_date.year, month=self.last_check_date.month,
        #                              day=self.last_check_date.day,
        #                              tzinfo=ZoneInfo('Europe/Moscow'))
        # return

        # self.log("test css:", html_msg="<span style='background-color:hsl(216, 100%, 55%);font-weight:bold;color:white;'>Ozon:</span>")
        # self.log("test css:", html_msg="<span style='background-color:hsl(288, 100%, 65%);font-weight:bold;color:white;'>Wb:</span>")
        # return
        # Артикул, Расход, Магазин
        self.exel_list = self.get_excel_list()
        self.report_excel = self.get_report_excel()

        self.miss_orders_check = False

        orders = dict()
        # OZON
        ozon_shops = []
        for shop_name, client_id, api_key in self.API_KEYS.get('OZON_KEYS'):
            self.ozon_count = 0
            self.products_price_dict = dict()
            new_orders = self.get_orders_from_ozon(shop_name, client_id, api_key)
            # print(shop_name)
            # print(f"{self.products_price_dict=}")
            if self.products_price_dict:
                self.update_price_report(shop_name, client_id, api_key)
            self.add_to_report_excel(new_orders, f"[ozon] {shop_name}")  # Добавление в отчёт
            ozon_shops.append([shop_name, self.ozon_count])
            for article in new_orders:
                if orders.get(article):
                    orders[article] += new_orders[article]
                else:
                    orders[article] = new_orders[article]

            # products_price_dict = dict()
            # products_price_dict[article] = {'price':, 'id':}
        # # WB
        wb_shops = []
        for shop_name, api_key in self.API_KEYS.get('WB_KEYS'):
            self.wb_count = 0
            new_orders = self.get_orders_from_wb(shop_name, api_key)
            self.add_to_report_excel(new_orders, f"[wb] {shop_name}")  # Добавление в отчёт
            wb_shops.append([shop_name, self.wb_count])
            for article in new_orders:
                if orders.get(article):
                    orders[article] += new_orders[article]
                else:
                    orders[article] = new_orders[article]

        # YANDEX
        ya_shops = []
        for shop_name, business_id, campaignId, api_key in self.API_KEYS.get('YA_KEYS'):
            self.ya_count = 0
            new_orders = self.get_orders_from_yndx(shop_name, api_key, business_id, campaignId)
            self.add_to_report_excel(new_orders, f"[yndx] {shop_name}")  # Добавление в отчёт
            ya_shops.append([shop_name, self.ya_count])
            for article in new_orders:
                if orders.get(article):
                    orders[article] += new_orders[article]
                else:
                    orders[article] = new_orders[article]

        # self.orders_for_period()
        # return
        for c in self.exel_list.columns:
            if str(c).startswith('Ozon - расход за'):
                self.ozon_cost_col = str(c)
            if str(c).startswith('WB - расход за'):
                self.wb_cost_col = str(c)
            if str(c).startswith('Yandex - расход за'):
                self.ya_cost_col = str(c)

        # Получение заказов за выбранных период
        set_ozon_orders_p_count = self.orders_for_period_ozon()
        set_wb_orders_p_count = self.orders_for_period_wb()
        set_yndx_orders_p_count = self.orders_for_period_yndx()

        self.log('=============================')
        self.log("Итого:", html_msg="<span style='color:#38b04c;font-weight:bold;'>Итого:</span>")
        for p in orders:
            self.log(f"{p} - [{orders[p]}]")
        self.log('=============================')

        if ozon_shops:
            shops = ', '.join([f"{s[0]} [{s[1]}]" for s in ozon_shops])
            shops_h = [f"<span style='background-color:hsl(216, 100%, 55%);font-weight:bold;color:white;'>{s[0]}</span> [{s[1]}]" for s in ozon_shops]
            shops_h =', '.join(shops_h)
            self.log(f"Ozon: {shops}", html_msg=f"<span style='color:hsl(216, 100%, 55%)'>Ozon</span>: {shops_h}")

        if wb_shops:
            shops = ', '.join([f"{s[0]} [{s[1]}]" for s in wb_shops])
            shops_h = [f"<span style='background-color:hsl(288, 100%, 65%);font-weight:bold;color:white;'>{s[0]}</span> [{s[1]}]" for s in wb_shops]
            shops_h =', '.join(shops_h)
            self.log(f"WB: {shops}", html_msg=f"<span style='color:hsl(288, 100%, 65%)'>WB</span>: {shops_h}")

        if ya_shops:
            shops = ', '.join([f"{s[0]} [{s[1]}]" for s in ya_shops])
            shops_h = [f"<span style='background-color:hsl(58, 100%, 58%);font-weight:bold;'>{s[0]}</span> [{s[1]}]" for s in ya_shops]
            shops_h =', '.join(shops_h)
            self.log(f"Yandex: {shops}", html_msg=f"<span style='color:hsl(48, 100%, 43%)'>Yandex</span>: {shops_h}")

        # Потерянные артикулы
        # articles = {*self.exel_list['Артикул']}
        # miss_articles = orders.keys() - articles
        # miss_articles = set()
        # orders_low = {str(k).lower() for k in orders}
        # for a in orders.keys() - articles:
        #     if a.lower() not in orders_low:
        #         miss_articles.add(a)

        orders_low = dict()
        for o in orders:
            o_low = str(o).lower()
            if orders_low.get(o_low):
                orders_low[o_low] += orders[o]
            else:
                orders_low[o_low] = orders[o]

        # self.exel_list['Расход'] = self.exel_list['Расход'] + self.exel_list['Артикул'].map(orders).fillna(0)
        self.exel_list['Расход'] = self.exel_list['Расход'] + self.exel_list['Артикул comp'].map(orders_low).fillna(0)

        self.exel_list['Остаток'] = self.exel_list['Остаток'].astype('str')
        for r in range(len(self.exel_list)):
            self.exel_list.loc[r, 'Остаток'] = f'=B{r + 2}-C{r + 2}'

        # exel_list.to_csv('res.csv', sep=';', index=False, encoding='utf-8-sig')  # windows-1251 # utf-8 # utf-8-sig # cp1251
        # shutil.copy('res.csv', f"archive/res {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.csv")
        #
        for c in self.exel_list.columns:
            if str(c).startswith('Расход неделя'):
                cost_week_col = str(c)
                break

        # Сумма Ozon расход + WB расход (за выбранное время)
        self.exel_list['Сумма расходов Ozon, WB и Yandex'] = self.exel_list['Сумма расходов Ozon, WB и Yandex'].astype('str')
        for r in range(len(self.exel_list)):
            self.exel_list.loc[r, 'Сумма расходов Ozon, WB и Yandex'] = f'=F{r + 2}+G{r + 2}+H{r + 2}'

        cols = ['Артикул', 'Приход', 'Расход', 'Остаток', cost_week_col, f"{self.ozon_cost_col}", f"{self.wb_cost_col}",
                f"{self.ya_cost_col}", "Сумма расходов Ozon, WB и Yandex"]

        self.exel_list = self.exel_list.sort_values('Артикул')
        self.exel_list.to_excel('Склад учёт.xlsx', columns=cols, index=False, engine='openpyxl')  # windows-1251 # utf-8 # utf-8-sig # cp1251
        shutil.copy('Склад учёт.xlsx', f"archive/Склад учёт {datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.xlsx")

        self.report_excel.to_excel('Потерянные артикулы.xlsx', columns=['Артикул', 'Расход', 'Магазин'],
                                   index=False, engine='openpyxl')

        if set_ozon_orders_p_count:
            self.log(f"Ozon - расход за {self.period_msg} добавлен",
                     html_msg=f"<span style='color:hsl(216, 100%, 55%)'>Ozon</span> расход за <span style='font-weight:bold;'>{self.period_msg}</span> добавлен")

        if set_wb_orders_p_count:
            self.log(f"WB - расход за {self.period_msg} добавлен",
                     html_msg=f"<span style='color:hsl(288, 100%, 65%)'>WB</span> расход за <span style='font-weight:bold;'>{self.period_msg}</span> добавлен")

        if set_yndx_orders_p_count:
            self.log(f"Yandex - расход за {self.period_msg} добавлен",
                     html_msg=f"<span style='color:hsl(48, 100%, 43%)'>Yandex</span> расход за <span style='font-weight:bold;'>{self.period_msg}</span> добавлен")

        with open('last_check_time.txt', 'w') as f:
            f.write(f"{self.cur_check_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

        self.SetBadArticleSignal.emit(len(self.report_excel))
        if self.miss_orders_check:
            self.log("Есть потерянные артикулы!", html_msg="<span style='color:red;'>Есть потерянные артикулы!</span>")

        self.log("Данные обновлены", html_msg="<span style='color:#38b04c;'>Данные обновлены</span>")

        return True


    def excel_is_open(self):
        try:
            files = ['Склад учёт.xlsx', 'Потерянные артикулы.xlsx', 'Цены.xlsx', 'Цены заказов.xlsx']

            for f in files:
                with open(f, 'a'):
                    pass

            return False

        except PermissionError as pe:
            self.log("Не удалось получить доступ к эксель файлу! (Зайройте его, если он открыт)",
                     html_msg="<span style='color:red;font-weight:bold;'>Не удалось получить доступ к эксель файлу! (Зайройте его, если он открыт)</span>")
            return True

    def orders_for_period_ozon(self):
        with open('daily_check_time.txt', 'r') as fr:
            daily_check_times = fr.read().split()[:2]
            self.daily_check_times = [datetime.datetime.strptime(t, '%H:%M').time() for t in daily_check_times]
        # if daily_check_times[0] < daily_check_times[1]:
        #     self.log(f"Указан некорректный промежуток времени", html_msg=f"<span style='color:#eb712a;'>Указан некорректный промежуток времени</span>")
        #     return

        if not (self.last_check_date.time() < self.daily_check_times[1] and self.cur_time.time() > self.daily_check_times[1]):
            return False

        orders = dict()

        ozon_shops = []
        for shop_name, client_id, api_key in self.API_KEYS.get('OZON_KEYS'):
            self.ozon_count = 0
            new_orders = self.get_orders_from_ozon(shop_name, client_id, api_key, default_check=False)
            ozon_shops.append([shop_name, self.ozon_count])
            for article in new_orders:
                if orders.get(article):
                    orders[article] += new_orders[article]
                else:
                    orders[article] = new_orders[article]
        # WB
        # wb_shops = []
        #
        # for shop_name, api_key in self.API_KEYS.get('WB_KEYS'):
        #     self.wb_count = 0
        #     new_orders = self.get_orders_from_wb(shop_name, api_key, default_check=False)
        #     wb_shops.append([shop_name, self.wb_count])
        #     for article in new_orders:
        #         if orders.get(article):
        #             orders[article] += new_orders[article]
        #         else:
        #             orders[article] = new_orders[article]

        self.period_msg = f"{(self.cur_time - datetime.timedelta(days=1)).date()} {str(self.daily_check_times[0])[:5]} - {self.cur_time.date()} {str(self.daily_check_times[1])[:5]}"

        self.log('=============================')
        self.log(f"[ozon] Итого (За {self.period_msg}):",
                 html_msg=f"<span style='color:hsl(216, 100%, 55%)'>Ozon</span> "
                          f"<span style='color:#38b04c;font-weight:bold;'>Итого</span> (За {self.period_msg}):")
        for p in orders:
            self.log(f"{p} - [{orders[p]}]")
        self.log('=============================')
        self.log('')

        new_col_name = f"Ozon - расход за {self.period_msg}"
        self.exel_list = self.exel_list.rename(columns={self.ozon_cost_col: new_col_name})
        self.ozon_cost_col = new_col_name

        orders_low = dict()
        for o in orders:
            o_low = str(o).lower()
            if orders_low.get(o_low):
                orders_low[o_low] += orders[o]
            else:
                orders_low[o_low] = orders[o]
        orders = orders_low

        self.exel_list[new_col_name] = self.exel_list['Артикул comp'].map(orders).fillna(0)

        return True


    def orders_for_period_wb(self):
        with open('daily_check_time.txt', 'r') as fr:
            daily_check_times = fr.read().split()[2:4]
            self.daily_check_times = [datetime.datetime.strptime(t, '%H:%M').time() for t in daily_check_times]
        # if daily_check_times[0] < daily_check_times[1]:
        #     self.log(f"Указан некорректный промежуток времени", html_msg=f"<span style='color:#eb712a;'>Указан некорректный промежуток времени</span>")
        #     return

        if not (self.last_check_date.time() < self.daily_check_times[1] and self.cur_time.time() > self.daily_check_times[1]):
            return False

        orders = dict()

        # ozon_shops = []
        # for shop_name, client_id, api_key in self.API_KEYS.get('OZON_KEYS'):
        #     self.ozon_count = 0
        #     new_orders = self.get_orders_from_ozon(shop_name, client_id, api_key, default_check=False)
        #     ozon_shops.append([shop_name, self.ozon_count])
        #     for article in new_orders:
        #         if orders.get(article):
        #             orders[article] += new_orders[article]
        #         else:
        #             orders[article] = new_orders[article]
        # WB
        wb_shops = []

        for shop_name, api_key in self.API_KEYS.get('WB_KEYS'):
            self.wb_count = 0
            new_orders = self.get_orders_from_wb(shop_name, api_key, default_check=False)
            wb_shops.append([shop_name, self.wb_count])
            for article in new_orders:
                if orders.get(article):
                    orders[article] += new_orders[article]
                else:
                    orders[article] = new_orders[article]

        self.period_msg = f"{(self.cur_time - datetime.timedelta(days=1)).date()} {str(self.daily_check_times[0])[:5]} - {self.cur_time.date()} {str(self.daily_check_times[1])[:5]}"

        self.log('=============================')
        self.log(f"[wb] Итого (За {self.period_msg}):",
                 html_msg=f"<span style='color:hsl(288, 100%, 65%)'>WB</span> "
                          f"<span style='color:#38b04c;font-weight:bold;'>Итого</span> (За {self.period_msg}):")
        for p in orders:
            self.log(f"{p} - [{orders[p]}]")
        self.log('=============================')
        self.log('')

        new_col_name = f"WB - расход за {self.period_msg}"
        self.exel_list = self.exel_list.rename(columns={self.wb_cost_col: new_col_name})
        self.wb_cost_col = new_col_name

        orders_low = dict()
        for o in orders:
            o_low = str(o).lower()
            if orders_low.get(o_low):
                orders_low[o_low] += orders[o]
            else:
                orders_low[o_low] = orders[o]
        orders = orders_low

        self.exel_list[new_col_name] = self.exel_list['Артикул comp'].map(orders).fillna(0)

        return True


    def orders_for_period_yndx(self):
        with open('daily_check_time.txt', 'r') as fr:
            daily_check_times = fr.read().split()[4:]
            self.daily_check_times = [datetime.datetime.strptime(t, '%H:%M').time() for t in daily_check_times]
        # if daily_check_times[0] < daily_check_times[1]:
        #     self.log(f"Указан некорректный промежуток времени", html_msg=f"<span style='color:#eb712a;'>Указан некорректный промежуток времени</span>")
        #     return
        if not (self.last_check_date.time() < self.daily_check_times[1] and self.cur_time.time() > self.daily_check_times[1]):
        #     # print('skip')
        #     # print(self.last_check_date.time() < self.daily_check_times[1] and self.cur_time.time() > self.daily_check_times[1])
        #     # print(self.last_check_date.time(), '<', self.daily_check_times[1], self.last_check_date.time() < self.daily_check_times[1])
        #     # print(self.cur_time.time(), '>', self.daily_check_times[1], self.cur_time.time() > self.daily_check_times[1])
            return False

        orders = dict()

        # WB
        # wb_shops = []
        #
        # for shop_name, api_key in self.API_KEYS.get('WB_KEYS'):
        #     self.wb_count = 0
        #     new_orders = self.get_orders_from_wb(shop_name, api_key, default_check=False)
        #     wb_shops.append([shop_name, self.wb_count])
        #     for article in new_orders:
        #         if orders.get(article):
        #             orders[article] += new_orders[article]
        #         else:
        #             orders[article] = new_orders[article]

        # YANDEX
        ya_shops = []
        for shop_name, business_id, campaignId, api_key in self.API_KEYS.get('YA_KEYS'):
            self.ya_count = 0
            new_orders = self.get_orders_from_yndx(shop_name, api_key, business_id, campaignId, default_check=False)
            ya_shops.append([shop_name, self.ya_count])
            for article in new_orders:
                if orders.get(article):
                    orders[article] += new_orders[article]
                else:
                    orders[article] = new_orders[article]


        self.period_msg = f"{(self.cur_time - datetime.timedelta(days=1)).date()} {str(self.daily_check_times[0])[:5]} - {self.cur_time.date()} {str(self.daily_check_times[1])[:5]}"

        self.log('=============================')
        self.log(f"[yndx] Итого (За {self.period_msg}):",
                 html_msg=f"<span style='color:hsl(48, 100%, 43%)'>Yandex</span> "
                          f"<span style='color:#38b04c;font-weight:bold;'>Итого</span> (За {self.period_msg}):")
        for p in orders:
            self.log(f"{p} - [{orders[p]}]")
        self.log('=============================')
        self.log('')

        new_col_name = f"Yandex - расход за {self.period_msg}"
        self.exel_list = self.exel_list.rename(columns={self.ya_cost_col: new_col_name})
        self.ya_cost_col = new_col_name

        orders_low = dict()
        for o in orders:
            o_low = str(o).lower()
            if orders_low.get(o_low):
                orders_low[o_low] += orders[o]
            else:
                orders_low[o_low] = orders[o]
        orders = orders_low

        self.exel_list[new_col_name] = self.exel_list['Артикул comp'].map(orders).fillna(0)

        return True


    def get_orders_from_ozon(self, shop_name, CLIENT_ID, API_KEY, default_check=True):
        headers = {
            "Host": "api-seller.ozon.ru",
            'Client-Id': CLIENT_ID,
            'Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }

        # today = datetime.datetime.now()
        # yesterday = today - datetime.timedelta(days=1)
        # since_date = self.last_check_date
        msg = ''
        if default_check:
            since = f"{self.last_check_date.date()}T{self.last_check_date.time()}"
            to = f"{self.cur_check_datetime.date()}T{self.cur_check_datetime.time()}"
        else:
            since = f"{(self.cur_time-datetime.timedelta(days=1)).date()}T{self.daily_check_times[0]}"
            to = f"{self.cur_time.date()}T{self.daily_check_times[1]}"
            msg = f" (За {since} - {to})".replace('T', ' ')
        # return

        self.log(f"===== [ozon] ===== {shop_name} ====={msg}:",
                 html_msg=f"[ozon] <span style='background-color:hsl(216, 100%, 55%);font-weight:bold;color:white;'>{shop_name}</span>{msg}:")

        products_dict = dict()
        sku_article_dict = dict()
        cont = True
        loaded = 0
        limit = 500

        while cont:
            data = {
                "filter": {
                    "since": f"{since}+03:00",  # 2026-02-17
                    "to": f"{to}+03:00",
                },
                "limit": limit,
                "offset": loaded,
                "with": {
                    "financial_data": default_check,
                },
            }

            response = requests.post(url=fr"{OZON_URL}/v3/posting/fbs/list", headers=headers, json=data, timeout=100)
            if response.status_code != 200:
                # self.log("API не отвечает", html_msg="<span style='color:#eb712a;'>API не отвечает</span>")
                raise OzonApiResponseException

            orders = response.json()

            cont = orders['result']['has_next']
            loaded += limit

            # print(len(orders['result']['postings']), 'PST')
            for p in orders['result']['postings']:
                # status = p['status']
                # if status == 'cancelled':
                #     continue
                for product in p['products']:
                    article = str(product['offer_id'])
                    p_count = product['quantity']
                    for i in range(2):  # первые 2 символа
                        if article[0] in get_letters_ignore():
                            article = article[1:]
                    sku_article_dict[product['sku']] = product['offer_id']

                    if products_dict.get(article):
                        products_dict[article] += p_count
                    else:
                        products_dict[article] = p_count
                    if default_check:
                        self.ozon_count += p_count

                # Последние цены заказов
                if default_check:
                    for product in p['financial_data']['products']:
                        art = sku_article_dict[product['product_id']]  # sku
                        if not art:
                            continue
                        new_price = product['customer_price']
                        price = self.products_price_dict.get(art, -1)
                        if price > new_price:
                            self.products_price_dict[art] = new_price
                        else:
                            self.products_price_dict[art] = new_price

                    # if product['name'] == 'Зеркало для ванной с LED подсветкой 55х75см (320Св)':
                    #     total_q += product['quantity']
                    #     print(f"{status}, {product['quantity']}, {product['offer_id']}")

        if not products_dict:
            self.log(f"Заказы не найдены!", html_msg=f"<span style='color:#eb712a;'>Заказы не найдены!:</span>")

        for p in products_dict:
            self.log(f"{p} - [{products_dict[p]}]")

        return products_dict


    def get_orders_from_wb(self, shop_name, API_KEY, default_check=True):
        headers = {
            'Authorization': f'{API_KEY}',
            'Content-Type': 'application/json'
        }
        ## yesterday = (today - datetime.timedelta(days=1))

        # today = datetime.datetime.now().date()
        # today = datetime.datetime(year=today.year, month=today.month, day=today.day, tzinfo=ZoneInfo('Europe/Moscow'))
        # yesterday = datetime.datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day, tzinfo=ZoneInfo('Europe/Moscow'))
        # dateFrom = datetime.datetime(year=self.last_check_date.year, month=self.last_check_date.month, day=self.last_check_date.day,
        #                              tzinfo=ZoneInfo('Europe/Moscow'))
        msg = ''
        if default_check:
            dateFrom = int(self.last_check_date.timestamp())
            dateTo = int(self.cur_check_datetime.timestamp())
        else:
            dateFrom = datetime.datetime.strptime(f"{(self.cur_time-datetime.timedelta(days=1)).date()} {self.daily_check_times[0]}",
                                                      '%Y-%m-%d %H:%M:%S')
            dateTo = datetime.datetime.strptime(f"{self.cur_time.date()} {self.daily_check_times[1]}",
                                                      '%Y-%m-%d %H:%M:%S')
            msg = f" (За {dateFrom} - {dateTo})"
            dateFrom = int(dateFrom.timestamp())
            dateTo = int(dateTo.timestamp())

        self.log(f"===== [wb] ===== {shop_name} ====={msg}:",
                 html_msg=f"[wb] <span style='background-color:hsl(288, 100%, 65%);font-weight:bold;color:white;'>{shop_name}</span>{msg}:")


        products_dict = dict()

        wb_limit = 500
        req_next = 0

        while True:
            data = {
                "limit": wb_limit,
                "next": req_next,
                "dateFrom": dateFrom,
                "dateTo": dateTo,
            }

            response = requests.get(url=fr"https://marketplace-api.wildberries.ru/api/v3/orders", headers=headers,
                                    params=data, timeout=100)
            if response.status_code != 200:
                raise WbApiResponseException

            orders = response.json()

            for p in orders['orders']:
                # if p['scanPrice'] is None:
                #     continue

                article = str(p['article']).strip()

                for i in range(2):  # первые 2 символа
                    if article[0] in get_letters_ignore():
                        article = article[1:]

                if products_dict.get(article):
                    products_dict[article] += 1
                else:
                    products_dict[article] = 1
                if default_check:
                    self.wb_count += 1

            if wb_limit != len(orders['orders']):
                break
            req_next = int(orders['next'])

        if not products_dict:
            self.log(f"Заказы не найдены", html_msg=f"<span style='color:#eb712a;'>Заказы не найдены</span>")

        for p in products_dict:
            self.log(f"{p} - [{products_dict[p]}]")

        return products_dict


    def get_orders_from_yndx(self, shop_name, API_KEY, business_id, campaignId, default_check=True):
        headers = {
            'Api-Key': f"{API_KEY}",
            'Content-Type': 'application/json'
        }

        msg = ''
        if default_check:
            # timeFrom = f"{self.cur_check_datetime.date()}T{self.cur_check_datetime.time()}"
            timeFrom = f"{self.last_check_date.date()}T{self.last_check_date.time()}"
            timeTo = f"{self.cur_time.date()}T{self.cur_time.time()}"
            dateFrom = f"{self.last_check_date.date()}"
            dateTo = f"{self.cur_time.date()}"
        else:
            # timeFrom = f"{self.cur_check_datetime.date()}T{self.cur_check_datetime.time()}"
            # timeTo = f"{self.cur_time.date()}T{self.cur_time.time()}"
            dateFrom = f"{(self.cur_time-datetime.timedelta(days=1)).date()}"
            dateTo = f"{self.cur_time.date()}"
            timeFrom = f"{dateFrom}T{self.daily_check_times[0]}"
            timeTo = f"{dateTo}T{self.daily_check_times[1]}"

            msg = f" (За {dateFrom} {self.daily_check_times[0]} - {dateTo} {self.daily_check_times[1]})"

        # if default_check:
        #     dateFrom = int(self.last_check_date.timestamp())
        #     dateTo = int(self.cur_check_datetime.timestamp())
        # else:
        #     dateFrom = datetime.datetime.strptime(f"{(self.cur_time-datetime.timedelta(days=1)).date()} {self.daily_check_times[0]}",
        #                                               '%Y-%m-%d %H:%M:%S')
        #     dateTo = datetime.datetime.strptime(f"{self.cur_time.date()} {self.daily_check_times[1]}",
        #                                               '%Y-%m-%d %H:%M:%S')
        #     msg = f" (За {dateFrom} - {dateTo})"
        #     dateFrom = int(dateFrom.timestamp())
        #     dateTo = int(dateTo.timestamp())

        data = {
            "campaignIds": [campaignId],
            "dates": {
                "creationDateFrom": dateFrom,
                "creationDateTo": dateTo,
            }
        }

        self.log(f"===== [yndx] ===== {shop_name} ====={msg}:",
                 html_msg=f"[yndx] <span style='background-color:hsl(58, 100%, 58%);font-weight:bold;'>{shop_name}</span>{msg}:")


        products_dict = dict()
        next_page_token = ''
        while next_page_token or next_page_token == '':
            response = requests.post(url=f"{YA_URL}/v1/businesses/{business_id}/orders", headers=headers, json=data,
                                     params={"limit": 50, "pageToken": next_page_token}, timeout=100)
            # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
            if response.status_code != 200:
                raise YndxApiResponseException

            res = response.json()
            orders = res['orders']

            for order in orders:
                creationTime = order['creationDate'][:19]
                if default_check:
                    # print(creationTime, '<', timeFrom, creationTime < timeFrom)
                    # print(creationTime, '>', timeTo, creationTime > timeTo)
                    if creationTime < timeFrom or creationTime > timeTo:  # creationTime > timeFrom
                        continue

                for item in order['items']:
                    article = str(item["offerId"]).strip()
                    for i in range(2):  # первые 2 символа
                        if article[0] in get_letters_ignore():
                            article = article[1:]

                    if products_dict.get(article):
                        products_dict[article] += item['count']
                    else:
                        products_dict[article] = item['count']
                    if default_check:
                        self.ya_count += item['count']

            next_page_token = res['paging'].get('nextPageToken', None)


        if not products_dict:
            self.log(f"Заказы не найдены", html_msg=f"<span style='color:#eb712a;'>Заказы не найдены</span>")

        for p in products_dict:
            self.log(f"{p} - [{products_dict[p]}]")

        return products_dict


    def update_price_report(self, shop_name, CLIENT_ID, API_KEY):
        try:
            headers = {
                "Host": "api-seller.ozon.ru",
                'Client-Id': CLIENT_ID,
                'Api-Key': API_KEY,
                'Content-Type': 'application/json'
            }

            arts = [*self.products_price_dict.keys()]
            # print(f'{arts=}')
            price_info_data = {
                "filter": {
                    "visibility": "ALL",
                    "offer_id": arts
                },
                "limit": 999
            }

            response = requests.post(url=fr"{OZON_URL}/v5/product/info/prices", headers=headers, json=price_info_data,
                                     timeout=100)
            if response.status_code != 200:
                self.log("Ошибка запроса на получение id", html_msg="<span style='color:red;'>Ошибка запроса на получение id</span>")
                return
            orders = response.json()
            # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
            orders_id = dict()
            for order in orders['items']:
                # article = str(order['offer_id']).strip()
                # for i in range(2):  # первые 2 символа
                #     if article[0] in get_letters_ignore():
                #         article = article[1:]
                orders_id[order['offer_id']] = str(order['product_id'])

            # print(f"{orders_id=}")

            min_price_df = pd.read_excel(r'Цены.xlsx', header=0)
            min_price_df = min_price_df[min_price_df['Артикул'].notna()]
            min_price_df['Артикул'] = min_price_df['Артикул'].astype('str')
            min_price_df['Артикул comp'] = min_price_df['Артикул'].apply(get_comp_article)

            df = pd.read_excel(r'Цены заказов.xlsx', header=0)
            df = df[df['Артикул'].notna()]
            str_cols = ['Артикул', 'Исправлено', 'Время добавления в таблицу', 'Ссылка']
            for c in str_cols:
                df[c] = df[c].astype('str')
            df['Время добавления в таблицу'] = df['Время добавления в таблицу'].astype('str')
            df['Артикул comp'] = df['Артикул'].apply(get_comp_article)

            now_dt = datetime.datetime.now().strftime('%H:%M:%S %d.%m.%Y')
            # price_dict = {k: orders[k]['price'] for k in orders}
            # id_dict = {k: orders[k]['id'] for k in orders}

            new_products = self.products_price_dict.keys() - {*df.loc[df['Магазин'] == shop_name, 'Артикул']}
            # print(f"{new_products=}")
            #
            for a in new_products:
                df = pd.concat([df, pd.DataFrame(
                    {'Артикул': [a], 'Артикул comp': [get_comp_article(a)], 'Магазин': shop_name,
                     'Цена последнего заказа': self.products_price_dict[a],
                     'Время добавления в таблицу': now_dt})], ignore_index=True)

            df['Мин цена'] = df['Артикул comp'].map(min_price_df.set_index('Артикул comp')['Мин цена'])

            df.loc[(df['Магазин'] == shop_name) & (df['Артикул'].isin(self.products_price_dict)), ['Цена последнего заказа',
                                                                                     'Время добавления в таблицу',
                                                                                     'Исправлено']] = (
                pd.DataFrame(
                    {'Цена последнего заказа': df['Артикул'].map(self.products_price_dict), 'Время добавления в таблицу': now_dt,
                     'Исправлено': None}))


            df.loc[(df['Магазин'] == shop_name) & (df['Время добавления в таблицу'] == now_dt), ['Процент изменения', 'Ссылка']] = (
                pd.DataFrame(
                    {'Процент изменения': (df['Цена последнего заказа'] - df['Мин цена']) / df['Мин цена'] * 100,
                     'Ссылка': r'https://seller.ozon.ru/app/prices/manager/' + df['Артикул'].map(orders_id).astype(str) + r'/prices'}))
                     # 'Ссылка': r'https://seller.ozon.ru/app/prices/manager/' + df['Артикул'].map(orders_id).astype(str) + r'/1prices'}))

            cols = ['Артикул', 'Магазин', 'Мин цена', 'Цена последнего заказа', 'Процент изменения',
                    'Время добавления в таблицу',
                    'Исправлено', 'Ссылка']

            df = df.sort_values('Процент изменения', ascending=True)
            df.loc[df['Исправлено'].notna(), 'Исправлено'] = 'да'
            df = df.sort_values('Исправлено', na_position='first')
            df['Процент изменения'] = df['Процент изменения'].round(1)
            # print(df[['Артикул', 'Процент изменения', 'Ссылка']])

            df.to_excel('Цены заказов.xlsx', columns=cols, index=False, engine='openpyxl')


        except Exception as price_ex:
            self.log("Ошибка обновлении цены:", html_msg="<span style='color:red;'>Ошибка обновлении цены:</span>")
            ex_text = traceback.format_exc()
            self.log(ex_text, error=True)


    def get_excel_list(self):
        df = pd.read_excel(r'Склад учёт.xlsx', header=0)
        # df = pd.read_csv(r'res.csv', sep=';', encoding='utf-8-sig', header=0)
        # df['Артикул'] = df['Артикул'].astype('str')
        df = df[df['Артикул'].notna()]
        df['Артикул'] = df['Артикул'].apply(lambda x: str(x).strip())
        df['Артикул comp'] = df['Артикул'].apply(str.lower)
        return df

    def get_report_excel(self):
        df = pd.read_excel(r'Потерянные артикулы.xlsx', header=0)
        # print(len(df))
        df = df[df['Артикул'].notna()]
        df['Артикул'] = df['Артикул'].astype('str')
        df['Артикул comp'] = df['Артикул'].apply(lambda x: str(x).lower())
        # print(len(df))
        return df

    def add_to_report_excel(self, new_orders: dict, shop_name):
        # print(shop_name)
        articles = {*self.exel_list['Артикул comp']}

        new_orders_low = dict()
        for o in new_orders:
            o_low = str(o).lower()
            if new_orders_low.get(o_low):
                new_orders_low[o_low] += new_orders[o]
            else:
                new_orders_low[o_low] = new_orders[o]
        new_orders = new_orders_low


        miss_articles = new_orders.keys() - articles
        miss_orders = {a: new_orders[a] for a in miss_articles}

        if miss_orders:
            self.miss_orders_check = True

        # print(f"{miss_orders=}")
        if miss_orders:
            self.log(f"------ Артикулы не совпали ------", html_msg=f"--- <span style='color:#eb712a;'>Артикулы не совпали</span> ---")
            for o in miss_orders:
                self.log(f"{o} - [{miss_orders[o]}]")
            self.log('')

        # print(self.report_excel)
        # self.report_excel['Расход'], self.report_excel['Магазин'] = self.report_excel['Расход'] + self.report_excel['Артикул'].apply(lambda art: miss_orders.get(art, 0)), shop_name
        self.report_excel.loc[(self.report_excel['Магазин'] == shop_name) & (self.report_excel['Артикул comp'].map(miss_orders)), 'Расход'] = (
                self.report_excel['Расход'] + self.report_excel['Артикул comp'].map(miss_orders))

        new_positions = miss_articles - {*self.report_excel.loc[self.report_excel['Магазин'] == shop_name, 'Артикул comp']}
        # print(f"{new_positions=}")


        # print('-R---')
        # print(self.report_excel)
        # if new_positions:
            # print('R', len(self.report_excel))
        for a in new_positions:
            # print('new', len(self.report_excel))
            # self.report_excel.loc[len(self.report_excel)] = {'Артикул': a, 'Расход': miss_orders[a], 'Магазин': shop_name}
            self.report_excel = pd.concat([self.report_excel, pd.DataFrame({'Артикул': [a], 'Расход': [miss_orders[a]], 'Магазин': [shop_name]})],
                                          ignore_index=True)
            # print('new+', len(self.report_excel))
        # print(self.report_excel)
        # print('=R===\n')

    def set_token_date_to(self):
        dates = []
        for i in range(len(self.API_KEYS.get('OZON_KEYS'))):
            headers = {
                "Host": "api-seller.ozon.ru",
                'Client-Id': self.API_KEYS.get('OZON_KEYS')[i][1],
                'Api-Key': self.API_KEYS.get('OZON_KEYS')[i][2],
                'Content-Type': 'application/json'
            }
            response = requests.post(url=fr"{OZON_URL}/v1/roles", headers=headers, timeout=100)
            res = response.json()
            date = '.'.join(res['expires_at'][:10].split('-')[::-1])
            dates.append(date)
        min_date = min(dates)

        if (datetime.datetime.now() + datetime.timedelta(days=7)).date() > datetime.datetime.strptime(min_date, '%d.%m.%Y').date():
            min_date_html = f"<span style='color:red;font-weight:bold;'>{min_date}</span>"
        else:
            min_date_html = f"<span style='font-weight:bold;'>{min_date}</span>"
        # self.log(f"API токены действительны до {min_date}", html_msg=f"API токены действительны до {min_date_html}")
        self.SetApiDataSignal.emit(f"API токены действительны до {min_date_html}")


    def del_files_from_archive(self):
        try:
            del_dt = datetime.datetime.now() - datetime.timedelta(days=7)

            for f in os.listdir('archive/'):
                last_dt = re.search(r'Склад учёт \d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}', f)
                if last_dt:
                    last_dt = last_dt.group()
                    last_dt = datetime.datetime.strptime(last_dt[11:], '%Y-%m-%d %H-%M-%S')
                    if last_dt < del_dt:
                        # print('D', f, last_dt)
                        os.remove(fr'archive/{f}')
        except:
            pass


    def log(self, text, error=False, html_msg=None):
        if error:
            logger.error(f"ERROR: {text}")
            # self.log_tb.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            #                    f"<span style='color:red;font-weight:bold;'>{text}</span><br>  ")
            self.LogAddSignal.emit(0, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] <span style='color:red;font-weight:bold;'>{text}</span><br>  ")
        elif html_msg:
            logger.log(21, f"{text}")
            # self.log_tb.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {html_msg}  ")
            self.LogAddSignal.emit(0, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {html_msg}  ")
            # self.log_tb.moveCursor(QTextCursor.End)
        else:
            logger.log(21, f"{text}")
            # self.log_tb.append(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")
            self.LogAddSignal.emit(0, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")


def get_comp_article(article):
    article = str(article)
    for i in range(2):  # первые 2 символа
        if article[0] in get_letters_ignore():
            article = article[1:]
    return article.lower()

class OzonApiResponseException(Exception):
    pass

class WbApiResponseException(Exception):
    pass

class YndxApiResponseException(Exception):
    pass
