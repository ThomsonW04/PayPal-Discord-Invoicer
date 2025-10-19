import os
import sqlite3

db = sqlite3.connect(f"{os.getcwd()}/data/db.sqlite")
cur = db.cursor()


try:
    cur.execute("ALTER TABLE invoices ADD COLUMN paypal_invoice_id TEXT")
except sqlite3.OperationalError:
    pass

db.commit()
db.close()
