import os
from tinydb import TinyDB

os.makedirs('data', exist_ok=True)

db_path = os.path.join('data', 'products.json')
db = TinyDB(db_path)

products_table = db.table('products')