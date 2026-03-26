import json
import requests
import datetime
import time
import traceback
from zoneinfo import ZoneInfo
import locale
import os
import re
import pandas as pd
import openpyxl
from PySide6.QtCore import QThread, Signal

from utils import get_api_keys, GetApiKeysException, get_letters_ignore

import logging
from logging.handlers import RotatingFileHandler

locale.setlocale(locale.LC_ALL, "ru")

logger = logging.getLogger('logs_orders_selecter.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('logs_orders_selecter.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
# s_handler = logging.StreamHandler()
# s_handler.setFormatter(formater)
logger.addHandler(f_handler)
# logger.addHandler(s_handler)

OZON_URL = r'https://api-seller.ozon.ru'
WB_URL = r'https://common-api.wildberries.ru'
YA_URL = r'https://api.partner.market.yandex.ru'

# exception_letters = ('q', 'z', 'x', 'y', 'Q', 'Z', 'X', 'Y')


class OrdersSelecter(QThread):
    LogAddSignal = Signal(int, str)
    OrdersSignal = Signal(list)

    def __init__(self, since, to):
        QThread.__init__(self)
        self.since = since
        self.to = to

    def run(self):
        # self.OrdersSignal.emit([
        #                         ['[ozon] м1', 43, '#48a7f0'],
        #                         ['[ozon] м2', 22, '#48a7f0'],
        #                         ['[ozon] м3', 58, '#48a7f0'],
        #                         ['[wb] м1', 11, '#d377f7'],
        #                         ['[wb] м2', 74, '#d377f7'],
        #                         ['[wb] м3', 45, '#d377f7'],
        #                         ])
        # self.log('ok')
        # return

        try:
            self.datetime_since = datetime.datetime(year=self.since.date().year(), month=self.since.date().month(), day=self.since.date().day())
            self.datetime_to = datetime.datetime(year=self.to.date().year(), month=self.to.date().month(), day=self.to.date().day())
            self.log(f'Загрузка... {self.datetime_since} - {self.datetime_to}')

            # self.OZON_KEYS, self.WB_KEYS = get_api_keys()
            self.API_KEYS = get_api_keys()

            # colors_for_pie = []
            orders = dict()
            # OZON
            ozon_shops = []
            for shop_name, client_id, api_key in self.API_KEYS.get('OZON_KEYS'):
                cnt, new_orders = self.get_orders_from_ozon(shop_name, client_id, api_key)
                ozon_shops.append([f"[ozon] {shop_name}", cnt, '#48a7f0'])
                # colors_for_pie.append('#48a7f0')
                for article in new_orders:
                    if orders.get(article):
                        orders[article] += new_orders[article]
                    else:
                        orders[article] = new_orders[article]
            # WB
            wb_shops = []
            for shop_name, api_key in self.API_KEYS.get('WB_KEYS'):
                cnt, new_orders = self.get_orders_from_wb(shop_name, api_key)
                wb_shops.append([f"[wb] {shop_name}", cnt, '#d377f7'])
                # colors_for_pie.append('#d377f7')
                for article in new_orders:
                    if orders.get(article):
                        orders[article] += new_orders[article]
                    else:
                        orders[article] = new_orders[article]

            # YANDEX
            ya_shops = []
            for shop_name, business_id, campaignId, api_key in self.API_KEYS.get('YA_KEYS'):
                cnt, new_orders = self.get_orders_from_yndx(shop_name, api_key, business_id, campaignId)
                ya_shops.append([f"[yndx] {shop_name}", cnt, '#F8D854'])
                for article in new_orders:
                    if orders.get(article):
                        orders[article] += new_orders[article]
                    else:
                        orders[article] = new_orders[article]

            self.OrdersSignal.emit(ozon_shops + wb_shops + ya_shops)

            exel_list = pd.read_excel(r'Склад учёт.xlsx', header=0)
            exel_list = exel_list[exel_list['Артикул'].notna()]
            exel_list['Артикул'] = exel_list['Артикул'].apply(lambda x: str(x).strip())
            exel_list['Артикул comp'] = exel_list['Артикул'].apply(str.lower)
            exel_list['Остаток'] = exel_list['Остаток'].astype('str')
            for r in range(len(exel_list)):
                exel_list.loc[r, 'Остаток'] = f'=B{r + 2}-C{r + 2}'

            orders_low = dict()
            for o in orders:
                o_low = str(o).lower()
                if orders_low.get(o_low):
                    orders_low[o_low] += orders[o]
                else:
                    orders_low[o_low] = orders[o]


            cost_week_col = f'Расход неделя ({self.datetime_since.date()} - {self.datetime_to.date()})'
            exel_list[cost_week_col] = exel_list['Артикул comp'].map(orders_low).fillna(0)

            exel_list['Сумма расходов Ozon, WB и Yandex'] = exel_list[
                'Сумма расходов Ozon, WB и Yandex'].astype('str')
            for r in range(len(exel_list)):
                exel_list.loc[r, 'Сумма расходов Ozon, WB и Yandex'] = f'=F{r + 2}+G{r + 2}+H{r + 2}'

            for c in exel_list.columns:
                if str(c).startswith('Ozon - расход за'):
                    self.ozon_cost_col = str(c)
                if str(c).startswith('WB - расход за'):
                    self.wb_cost_col = str(c)
                if str(c).startswith('Yandex - расход за'):
                    self.ya_cost_col = str(c)

            cols = ['Артикул', 'Приход', 'Расход', 'Остаток', cost_week_col, f"{self.ozon_cost_col}",
                    f"{self.wb_cost_col}", f"{self.ya_cost_col}", "Сумма расходов Ozon, WB и Yandex"]


            exel_list.to_excel('Склад учёт.xlsx', columns=cols, index=False, engine='openpyxl')

            self.log('=============================')
            self.log(f"Итого (с {self.datetime_since.date()} по {self.datetime_to.date()}):",
                     html_msg=f"<span style='color:#38b04c;font-weight:bold;'>Итого</span> (с {self.datetime_since.date()} по {self.datetime_to.date()}):")
            for p in orders:
                self.log(f"{p} - [{orders[p]}]")
            self.log('=============================')

            total_count = 0
            if ozon_shops:
                total_count += sum([s[1] for s in ozon_shops])
                shops = ', '.join([f"{s[0]} [{s[1]}]" for s in ozon_shops])
                shops_h = [f"<span style='background-color:hsl(216, 100%, 55%);font-weight:bold;color:white;'>{s[0]}</span> [{s[1]}]" for s in ozon_shops]
                shops_h =', '.join(shops_h)
                self.log(f"Ozon: {shops}", html_msg=f"<span style='color:hsl(216, 100%, 55%)'>Ozon</span>: {shops_h}")

            if wb_shops:
                total_count += sum([s[1] for s in wb_shops])
                shops = ', '.join([f"{s[0]} [{s[1]}]" for s in wb_shops])
                shops_h = [f"<span style='background-color:hsl(288, 100%, 65%);font-weight:bold;color:white;'>{s[0]}</span> [{s[1]}]" for s in wb_shops]
                shops_h =', '.join(shops_h)
                self.log(f"WB: {shops}", html_msg=f"<span style='color:hsl(288, 100%, 65%)'>WB</span>: {shops_h}")

            if ya_shops:
                total_count += sum([s[1] for s in ya_shops])
                shops = ', '.join([f"{s[0]} [{s[1]}]" for s in ya_shops])
                shops_h = [f"<span style='background-color:hsl(58, 100%, 58%);font-weight:bold;'>{s[0]}</span> [{s[1]}]" for s in ya_shops]
                shops_h =', '.join(shops_h)
                self.log(f"Yandex: {shops}", html_msg=f"<span style='color:hsl(48, 100%, 43%)'>Yandex</span>: {shops_h}")

            self.log(f"Итоговое кол-во: {total_count}",
                     html_msg=f"<span style='color:#38b04c;font-weight:bold;'>Итоговое кол-во</span>: {total_count}")


        except GetApiKeysException:
            self.log("Ошибка при считывании API токенов. Проверьте config.txt",
                     html_msg="<span style='color:red;'>Ошибка при считывании API токенов. config.txt</span>")
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


    def log(self, text, error=False, html_msg=None):
        if error:
            logger.error(f"ERROR: {text}")
            self.LogAddSignal.emit(1, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] <span style='color:red;font-weight:bold;'>{text}</span><br>  ")
        elif html_msg:
            logger.log(21, f"{text}")
            self.LogAddSignal.emit(1, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {html_msg}  ")
        else:
            logger.log(21, f"{text}")
            self.LogAddSignal.emit(1, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")



    def get_orders_from_ozon(self, shop_name, CLIENT_ID, API_KEY):
        headers = {
            "Host": "api-seller.ozon.ru",
            'Client-Id': CLIENT_ID,
            'Api-Key': API_KEY,
            'Content-Type': 'application/json'
        }

        since = f"{self.datetime_since.date()}T00:00:00"
        to = f"{self.datetime_to.date()}T00:00:00"

        # return

        self.log(f"===== [ozon] ===== {shop_name} ===== (с {self.datetime_since.date()} по {self.datetime_to.date()}):",
                 html_msg=f"[ozon] <span style='background-color:hsl(216, 100%, 55%);font-weight:bold;color:white;'>{shop_name}</span> (с {self.datetime_since.date()} по {self.datetime_to.date()}):")

        products_dict = dict()
        ozon_count = 0
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
            }

            response = requests.post(url=fr"{OZON_URL}/v3/posting/fbs/list", headers=headers, json=data, timeout=100)
            if response.status_code != 200:
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
                    if products_dict.get(article):
                        products_dict[article] += p_count
                    else:
                        products_dict[article] = p_count

                    ozon_count += p_count
                    # if product['name'] == 'название':
                    #     total_q += product['quantity']
                    #     print(f"{status}, {product['quantity']}, {product['offer_id']}")

        if not products_dict:
            self.log(f"Заказы не найдены!", html_msg=f"<span style='color:#eb712a;'>Заказы не найдены!:</span>")

        for p in products_dict:
            self.log(f"{p} - [{products_dict[p]}]")

        return ozon_count, products_dict



    def get_orders_from_wb(self, shop_name, API_KEY):
        headers = {
            'Authorization': f'{API_KEY}',
            'Content-Type': 'application/json'
        }

        dateFrom = int(self.datetime_since.timestamp())
        dateTo = int(self.datetime_to.timestamp())

        self.log(f"===== [wb] ===== {shop_name} ===== (с {self.datetime_since.date()} по {self.datetime_to.date()}):",
                 html_msg=f"[wb] <span style='background-color:hsl(288, 100%, 65%);font-weight:bold;color:white;'>{shop_name}</span> (с {self.datetime_since.date()} по {self.datetime_to.date()}):")

        wb_count = 0
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
                wb_count += 1

            if wb_limit != len(orders['orders']):
                break
            req_next = int(orders['next'])

        if not products_dict:
            self.log(f"Заказы не найдены", html_msg=f"<span style='color:#eb712a;'>Заказы не найдены</span>")

        for p in products_dict:
            self.log(f"{p} - [{products_dict[p]}]")

        return wb_count, products_dict


    def get_orders_from_yndx(self, shop_name, API_KEY, business_id, campaignId):
        headers = {
            'Api-Key': f"{API_KEY}",
            'Content-Type': 'application/json'
        }

        dateFrom = f"{self.datetime_since.date()}"
        dateTo = f"{self.datetime_to.date()}"

        self.log(f"===== [yndx] ===== {shop_name} ===== (с {self.datetime_since.date()} по {self.datetime_to.date()}):",
                 html_msg=f"[yndx] <span style='background-color:hsl(58, 100%, 58%);font-weight:bold;'>{shop_name}</span> (с {self.datetime_since.date()} по {self.datetime_to.date()}):")

        data = {
            "campaignIds": [campaignId],
            "dates": {
                "creationDateFrom": dateFrom,
                "creationDateTo": dateTo,
            }
        }

        ya_count = 0
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
                for item in order['items']:
                    article = str(item["offerId"]).strip()
                    for i in range(2):  # первые 2 символа
                        if article[0] in get_letters_ignore():
                            article = article[1:]

                    if products_dict.get(article):
                        products_dict[article] += item['count']
                    else:
                        products_dict[article] = item['count']

                    ya_count += item['count']

            next_page_token = res['paging'].get('nextPageToken', None)

        if not products_dict:
            self.log(f"Заказы не найдены", html_msg=f"<span style='color:#eb712a;'>Заказы не найдены</span>")

        for p in products_dict:
            self.log(f"{p} - [{products_dict[p]}]")

        return ya_count, products_dict



class OzonApiResponseException(Exception):
    pass

class WbApiResponseException(Exception):
    pass

class YndxApiResponseException(Exception):
    pass