import os
import sqlite3


db = sqlite3.connect(f"{os.getcwd()}/data/db.sqlite")
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY,
            invoice_tag INTEGER
            )""")

db.commit()
db.close()