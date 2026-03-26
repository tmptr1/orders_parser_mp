import datetime
import time
import os
from PySide6.QtCore import QThread, Signal
import telebot
from telebot import types
import locale
import traceback

from utils import get_api_keys, GetApiKeysException

import logging
from logging.handlers import RotatingFileHandler

locale.setlocale(locale.LC_ALL, "ru")

logger = logging.getLogger('tg_logs.log')
logger.setLevel(21)
formater = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

f_handler = RotatingFileHandler('tg_logs.log', maxBytes=5 * 1024 * 1024, backupCount=2, errors='ignore',)
f_handler.setFormatter(formater)
# s_handler = logging.StreamHandler()
# s_handler.setFormatter(formater)
logger.addHandler(f_handler)
# logger.addHandler(s_handler)


# @bot.message_handler(content_types=['text'])
# def get_file_command(message: types.Message):
#     try:
#         # file_names = ['Склад учёт', 'Потерянные артикулы', 'Цены']
#         # if message.text in file_names:
#         #     file_name = message.text
#         #     last_update = datetime.datetime.fromtimestamp(os.path.getmtime(file_name)).strftime("%Y-%m-%d %H:%M:%S")
#         #     with open(file_name, 'rb') as f:
#         #         bot.send_document(message.chat.id, caption=f"Последнее изменение файла: {last_update}", document=f)
#     except Exception as ex:
#         print(ex)


class TgBotStarter(QThread):
    RestartTgSignal = Signal(str)
    LogAddSignal = Signal(int, str)
    running = True

    def __init__(self):
        super().__init__()
        self.set_up_tg_commands()
    # def terminate(self):
    #     QThread.terminate(self)
    #     bot.stop_polling()
    #     print('del')

    def set_up_tg_commands(self):
        self.API_KEYS = get_api_keys()
        self.bot = telebot.TeleBot(self.API_KEYS['TG_API'])

        @self.bot.message_handler(commands=['start', 'help', 'info'])
        def start_command(message):
            try:
                with open(r"users id.txt", 'r') as f:
                    users = [int(user_id.strip()) for user_id in f.readlines()]
                status = '(Уже добавлен в систему)' if message.chat.id in users else '(Не добавлен в систему)'
                self.bot.send_message(message.chat.id, f"Привет, твой ID: {message.chat.id} {status}\nКоманда для выбора таблиц: /list")
                self.log(f"/start {message.chat.id}")
                # (print(f"Привет, твой ID: {message.chat.id}")
            except Exception as ex:
                ex_text = traceback.format_exc()
                self.log(ex_text, error=True)

        @self.bot.message_handler(commands=['list'])
        @self.user_id_check
        def get_list_command(message):
            try:
                keyboard = types.ReplyKeyboardMarkup(row_width=1)
                btn1 = types.KeyboardButton('Склад учёт')
                btn2 = types.KeyboardButton('Потерянные артикулы')
                btn3 = types.KeyboardButton('Цены заказов')
                keyboard.add(btn1, btn2, btn3)
                self.bot.send_message(message.chat.id, 'Выберите файл для скачивания:', reply_markup=keyboard)
            except Exception as ex:
                ex_text = traceback.format_exc()
                self.log(ex_text, error=True)

        @self.bot.message_handler(content_types=['text'])
        @self.user_id_check
        def get_file_command(message: types.Message):
            try:
                # if not self.allow_user_id(message.chat.id):
                #     return

                file_names = ['Склад учёт', 'Потерянные артикулы', 'Цены заказов']
                if message.text in file_names:
                    file_name = f"{message.text}.xlsx"
                    self.log(f"Загрузка {file_name}")
                    last_update = datetime.datetime.fromtimestamp(os.path.getmtime(file_name)).strftime("%Y-%m-%d %H:%M:%S")
                    with open(file_name, 'rb') as f:
                        self.bot.send_document(message.chat.id, caption=f"Последнее изменение файла: {last_update}", document=f)
                    return

                log_files = ['logs.log', 'logs_orders_selecter.log', 'tg_logs.log']
                if message.text in [f'log {i}'for i in range(len(log_files))]:
                    log_id = int(message.text[4])
                    self.log(f"Загрузка лога {log_files[log_id]}")
                    with open(log_files[log_id], 'rb') as f:
                        self.bot.send_document(message.chat.id, document=f)

            except Exception as ex:
                ex_text = traceback.format_exc()
                self.log(ex_text, error=True)

    # def allow_user_id(self, id):
    #     with open(r"users id.txt", 'r') as f:
    #         users = [int(user_id.strip()) for user_id in f.readlines()]
    #         return id in users

    def user_id_check(self, fnc):
        try:
            def f_check(*args, **kwargs):
                message = args[0]
                with open(r"users id.txt", 'r') as f:
                    users = [int(user_id.strip()) for user_id in f.readlines()]

                if message.chat.id in users:
                    return fnc(*args, **kwargs)
                return

            return f_check
        except Exception as ex:
            ex_text = traceback.format_exc()
            self.log(ex_text, error=True)
            return

    def run(self):
        self.running = True

        while self.running:
            try:
                self.RestartTgSignal.emit("Статус: <span style='color:#38b04c;'>Работает</span>")
                self.log('Старт', html_msg="<span style='color:#38b04c;'>Старт</span>")

                self.bot.polling(non_stop=True, timeout=30, long_polling_timeout=10)


            except GetApiKeysException:
                self.log("Ошибка при считывании API токенов. Проверьте config.txt",
                         html_msg="<span style='color:red;'>Ошибка при считывании API токенов. config.txt</span>")
                time.sleep(60)
            except Exception as ex:
                ex_text = traceback.format_exc()
                self.log(ex_text, error=True)
                time.sleep(60)
            # print('run finish')
            # self.RestartTgSignal.emit("Статус: <span style='font-weight:bold;'>...</span>")
            # self.log('Конец итерации')


    def stop(self):
        try:
            # self.RestartTgSignal.emit("Статус: <span style='font-weight:bold;'>Остановка...</span>")
            self.RestartTgSignal.emit("Статус: <span style='color:#eb712a;'>Остановлен</span>")
            self.log('Остановка...')
            self.bot.stop_polling()
            self.quit()
            self.running = False
            self.wait()
            self.log('Бот остановлен', html_msg="<span style='color:#eb712a;'>Бот остановлен</span>")
        except Exception as ex:
            ex_text = traceback.format_exc()
            self.log(ex_text, error=True)
            return

    def log(self, text, error=False, html_msg=None):
        if error:
            logger.error(f"ERROR: {text}")
            self.LogAddSignal.emit(2, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] <span style='color:red;font-weight:bold;'>{text}</span><br>  ")
        elif html_msg:
            logger.log(21, f"{text}")
            self.LogAddSignal.emit(2, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {html_msg}  ")
        else:
            logger.log(21, f"{text}")
            self.LogAddSignal.emit(2, f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

