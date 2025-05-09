import configparser
import psycopg2
import os

dirname = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))


class Database:
    """
    Класс для экспорта данных о продажах в PostgreSQL (Singlton)
    """
    HOST = config['Access']['HOST_SQL']
    PORT = 5432
    DATABASE = config['Access']['BASE_SQL']
    USER = config['Access']['USER_SQL']
    PASSWORD = config['Access']['PASSWORD_SQL']

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, autocommit=False):
        try:
            self.connection = psycopg2.connect(
                host=Database.HOST,
                port=Database.PORT,
                database=Database.DATABASE,
                user=Database.USER,
                password=Database.PASSWORD,
                client_encoding='UTF8'
            )

            if autocommit:
                self.connection.autocommit = True

            self.cursor = self.connection.cursor()
        except Exception as err:
            print(f'Ошибка инициализации БД: {err}')
            raise

    @staticmethod
    def ensure_utf8(value):
        if isinstance(value, str):
            return value.encode('utf-8', 'ignore').decode('utf-8')
        elif isinstance(value, bytes):
            return value.decode('utf-8', 'ignore')
        return value

    def select(self, query, vars):
        self.cursor.execute(query, vars)
        res = self.cursor.fetchall()
        return res

    def post(self, df):
        if df.empty:
            print('Нет данных для загрузки.')
            return

        values = [tuple(self.ensure_utf8(v) for v in row) for _, row in df.iterrows()]
        query = f"INSERT INTO sales ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
        print(f"Выполняется запрос: {query}")
        print(f"Первая строка значений: {values[0]}")

        try:
            self.cursor.executemany(query, values)  # Вставка всех строк сразу
            if not self.connection.autocommit:
                self.connection.commit()
        except Exception as err:
            self.connection.rollback()
            raise