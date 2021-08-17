import yaml
from scripts.database import Database


def connect_db() -> Database:
    with open('config/config.yml', 'r') as f:
        config = yaml.safe_load(f)

    mysql_pw = config['user']['mysql_password']
    db_name = 'us_stock'
    table_name = 'stock_list'

    try:
        db = Database(mysql_pw, db_name, table_name)
        return db
    except Exception as e:
        print(e)
