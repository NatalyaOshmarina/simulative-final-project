import os
import configparser
from glob import glob

import pandas as pd

from database import Database

dirname = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'), encoding='utf-8')
path = config['Paths']['SALES_PATH']
SALES_PATH = os.path.join(dirname, raw_path) # определяем абсолютный путь

database = Database()

files = glob(SALES_PATH + '/*.csv')
for file in files:
    sales_df = pd.read_csv(file)
    database.post(sales_df)
    os.remove(file)

