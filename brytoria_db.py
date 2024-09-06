import time
from datetime import datetime
import sqlite3
def main():
    today = datetime.today()
    table_name = f'table{today.month}{today.year}'
    #table_name ="table92024"
    db_name = 'database.db'

    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur = cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, service, comment, name, date, price integer, number, avatar)") 
  
    con.commit()

    return table_name
