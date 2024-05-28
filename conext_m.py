import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_params = {
    'database': os.getenv('database'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
}

class ConnectDB:
    def __init__(self, db_params: dict):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        self.cur = self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        if self.conn:
            self.cur.close()
            self.conn.close()

    def commit(self):
        self.conn.commit()



class Product:

    def __init__(self, conn):
        self.conn = conn

    def save_product(self, name, price):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
            self.conn.commit()

    def get_products(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            return cursor.fetchall()

    def save(self):
        with ConnectDB(db_params) as conn:
            product_manager = Product(conn)
            product_manager.save_product(name='Laptop', price=1000)
            products = product_manager.get_products()
            for product in products:
                print(product)


product = Product.save_product



