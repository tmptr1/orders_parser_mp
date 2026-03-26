import re


def get_api_keys():
    # OZON_KEYS = []
    # WB_KEYS = []
    API_KEYS = {'OZON_KEYS': [], 'WB_KEYS': [], 'YA_KEYS': []}

    try:
        with open('config.txt', 'r', encoding='utf-8') as fr:
            data = fr.read()

            api_tg = re.search("TG_API = '.+", data)
            if api_tg:
                api_tg = api_tg.group()
                api_tg = api_tg.split("'")[1]
                API_KEYS['TG_API'] = api_tg

            ozon = re.search(r"OZON_KEYS = \(.+?\)", data, re.DOTALL)
            if ozon:
                ozon = ozon.group()
                # ozon_api = []
                for a in re.findall(r"\[.+?\]", ozon):
                    # a = a.replace('[', '').replace(']', '')
                    a = re.sub(r"[\[\]'\"]", '', a)
                    # OZON_KEYS.append([i.strip() for i in a.split(',')])
                    API_KEYS['OZON_KEYS'].append([i.strip() for i in a.split(',')])
            # for i in ozon_api:
            #     print(i)
            # print('='*20)

            wb = re.search(r"WB_KEYS = \(.+?\)", data, re.DOTALL)
            if wb:
                wb = wb.group()
                # wb_api = []
                for a in re.findall(r"\[.+?\]", wb):
                    # a = a.replace('[', '').replace(']', '')
                    a = re.sub(r"[\[\]'\"]", '', a)
                    # WB_KEYS.append([i.strip() for i in a.split(',')])
                    API_KEYS['WB_KEYS'].append([i.strip() for i in a.split(',')])

            yndx = re.search(r"YA_KEYS = \(.+?\)", data, re.DOTALL)
            if yndx:
                yndx = yndx.group()
                # wb_api = []
                for a in re.findall(r"\[.+?\]", yndx):
                    # a = a.replace('[', '').replace(']', '')
                    a = re.sub(r"[\[\]'\"]", '', a)
                    # WB_KEYS.append([i.strip() for i in a.split(',')])
                    API_KEYS['YA_KEYS'].append([i.strip() for i in a.split(',')])
            # for i in wb_api:
            #     print(i)
        return API_KEYS
    except Exception as ex:
        raise GetApiKeysException

class GetApiKeysException(Exception):
    pass

def get_letters_ignore():
    with open('letters ignore.txt', 'r', encoding='utf-8-sig') as f:
        letters = f.read().replace(';', '')
        return letters