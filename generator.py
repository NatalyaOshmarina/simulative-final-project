from datetime import datetime
from random import choice, randint, uniform, random
import string
import configparser
import os

dirname = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'), encoding='utf-8')

def generate_timestamp_id(today: datetime, prefics) -> list:
    """генерация ID вида '20230101A' (дата + случайные буквы)"""
    doc_id = list()
    for _ in range(50):
        date_part = today.strftime("%Y%m%d")
        random_part = ''.join(choice(string.ascii_uppercase) for _ in range(1))
        doc_id.append(f'{prefics}{date_part}{random_part}')
    return doc_id

def generate_product() -> tuple:
    """генерация товаров"""
    categories = eval(config['Sales']['CATEGORIES'])
    products = config['Sales']['PRODUCTS'].split('[')

    dict_products = dict(zip(categories, products))
    random_categories = list()
    random_items = list()
    for _ in range(50):
        category = choice(list(dict_products.keys()))
        random_categories.append(category)
        item = choice(dict_products[category].split(','))
        random_items.append(item)

    return random_categories, random_items

def generate_int(start: int, end: int) -> list:
    """генерация количества"""
    return [randint(start, end) for _ in range(50)]

def generate_float(start: float, end: float) -> list:
    """генерация цены"""
    return [round(uniform(start, end), 2) for _ in range(50)]

def generate_discount(start: int, end: int, p=0.4) -> list:
    """генерация скидки с заданной вероятностью для нулевого значения"""
    return [0 if random() < p else randint(start, end) for _ in range(50)]





