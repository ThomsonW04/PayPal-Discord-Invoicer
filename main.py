from controllers.DataBaseController import DataBaseContoller
from controllers.PayPalInvoiceController import PayPalInvoiceController
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord import app_commands, Intents, Interaction

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
    
class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=Intents.default(), help_command=None, command_prefix=None)
        self.MAIN_GUILD = discord.Object(os.getenv("GUILD_ID"))
    
def main():
    bot = DiscordBot()
    paypal = PayPalHandler()

    @bot.event
    async def on_ready():
        print(f"Bot is online as {bot.user}!")
        await bot.tree.sync(guild=bot.MAIN_GUILD)

    @bot.tree.command(name="create_invoice", description="Generate a PayPal invoice.", guild=bot.MAIN_GUILD)
    @app_commands.describe(email="The email of the account holder to send an invoice to", item_name="Name of the item", item_price="Price of the item (e.g. 3.49, 50.00, 1.99)", note="Optional note to the customer")
    async def create_invoice(interaction: Interaction, email: str, item_name: str, item_price: float, note: str = "Thank you for being an amazing customer!"):
        local_tag = paypal.create_local_invoice()
        invoice_id = paypal.create_draft_invoice(local_tag, note, email, {"name": item_name, "value": item_price})['id']
        response = paypal.send_invoice(invoice_id)
        await interaction.response.send_message(str(response))
    
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    main()