import os
from datetime import datetime, timedelta

import pandas as pd

from generator import *

dirname = os.path.dirname(__file__)
folder = os.path.join(dirname, 'data')
# Создаем папку для чеков и продаж (если не существует)
os.makedirs(folder, exist_ok=True)
today = datetime.today()

if 0 <= today.weekday() <= 5:
    for shop in range(1, 4):
        shop_num = shop
        for cash in range(1, 5):
            cash_num = cash
            name_file = str(shop_num) + '_' + str(cash_num) + '.csv'
            name_id = str(shop_num) + '_' + str(cash_num)
            # Полный путь к файлу продаж
            file_path = os.path.join(folder, name_file)
            # Полный путь к файлу продаж
            file_path = os.path.join(folder, name_file)
            category, item = generate_product()
            doc_id = generate_timestamp_id(today, name_id)
            amount = generate_int(1, 3)
            price = generate_float(100.0, 250.0)
            discount = generate_discount(0, 20)
            dt = {
                'ymd': [today.strftime('%Y-%m-%d')] * 50,
                'doc_id': doc_id,
                'item': item,
                'category': category,
                'amount': amount,
                'price': price,
                'discount': discount
            }

            df = pd.DataFrame(dt)
            df.to_csv(file_path, index=False)


