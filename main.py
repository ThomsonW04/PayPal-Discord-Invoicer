from controllers.DataBaseController import DataBaseContoller
from controllers.PayPalInvoiceController import PayPalInvoiceController
from dotenv import load_dotenv
import os
import discord
from discord import app_commands

load_dotenv()

class PayPalHandler:
    def __init__(self):
        self.database = DataBaseContoller()
        self.invoice_manager = PayPalInvoiceController(client_id = os.getenv("PAYPAL_CLIENT_ID"), 
                                                       client_secret = os.getenv("PAYPAL_CLIENT_SECRET"), 
                                                       vendor_given_names = os.getenv("VENDOR_GIVEN_NAMES"), 
                                                       vendor_last_names = os.getenv("VENDOR_LAST_NAMES"), 
                                                       vendor_email = os.getenv("VENDOR_EMAIL"), 
                                                       invoice_prefix = os.getenv("INVOICE_PREFIX"), 
                                                       currency_code = os.getenv("CURRENCY_CODE"),
                                                       dev_mode = os.getenv("DEV_MODE"))

    def create_local_invoice(self):
        last_tag = self.database.get_last_created_invoice()
        if last_tag is None:
            new_tag = 1
        else:
            new_tag = last_tag[0] + 1
        self.database.insert_new_invoice(new_tag)
        return new_tag

    def create_draft_invoice(self, invoice_tag, note, customer_email, item):
        response = self.invoice_manager.create_invoice(invoice_tag, note, customer_email, item)
        if response.status_code == 201:
            self.database.set_paypal_invoice_id(response.json()['id'], invoice_tag)
            return response.json()
        else:
            self.database.delete_invoice(invoice_tag)
            return response.json()
        
    def send_invoice(self, invoice_id):
        return self.invoice_manager.send_invoice(invoice_id).json()
    
    def get_invoice_information(self, invoice_id):
        return self.invoice_manager.get_invoice_details(invoice_id).json()
    
class DiscordBot(discord.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
    
def main():
    pass

if __name__ == "__main__":
    main()