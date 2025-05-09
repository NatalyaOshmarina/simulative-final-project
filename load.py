import os
import configparser
from glob import glob

import pandas as pd

from database import Database

dirname = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'), encoding='utf-8')
path = config['Paths']['SALES_PATH']
database = Database()

files = glob(path + '/*.csv')
for file in files:
    sales_df = pd.read_csv(file)
    database.post(sales_df)
    os.remove(file)

