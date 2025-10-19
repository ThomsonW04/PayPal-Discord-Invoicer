import os
import sqlite3

class DataBaseContoller:
    def __init__(self):
        self.database = sqlite3.connect(f"{os.getcwd()}/data/db.sqlite")
        self.cursor = self.database.cursor()

    def __del__(self):
        self.database.close()

    def insert_new_invoice(self, invoice_tag):
        self.cursor.execute("INSERT INTO invoices (invoice_tag) VALUES (?)", (invoice_tag,))
        self.database.commit()

    def get_last_created_invoice(self):
        self.cursor.execute("SELECT * FROM invoices ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchone()
    
    def get_paypal_id_from_local_id(self, invoice_tag):
        self.cursor.execute("SELECT paypal_invoice_id FROM invoices WHERE invoice_tag = ?", (invoice_tag, ))
        return self.cursor.fetchone()
    
    def set_paypal_invoice_id(self, paypal_invoice_id, invoice_tag):
        self.cursor.execute("UPDATE invoices SET paypal_invoice_id = ? WHERE invoice_tag = ?", (paypal_invoice_id, invoice_tag,))
        self.database.commit()

    def delete_invoice(self, invoice_tag):
        self.cursor.execute("DELETE FROM invoices WHERE invoice_tag = ?", (invoice_tag,))
        self.database.commit()