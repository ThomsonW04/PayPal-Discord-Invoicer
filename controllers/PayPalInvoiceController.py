import requests
import base64

class PayPalInvoiceController:
    def __init__(self, client_id, client_secret, vendor_given_names, vendor_last_names, vendor_email, invoice_prefix, currency_code, dev_mode):
        self.headers = {
            'Authorization': f'Bearer {self.__get_api_token(client_id, client_secret)}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation',
        }
        self.vendor_given_names = vendor_given_names
        self.vendor_last_names = vendor_last_names
        self.vendor_email = vendor_email
        self.invoice_prefix = invoice_prefix
        self.currency_code = currency_code
        if dev_mode == "Y":
            self.invoice_api_url = "https://api-m.sandbox.paypal.com/v2/invoicing/invoices"
        else:
            self.invoice_api_url = "https://api-m.paypal.com/v2/invoicing/invoices"

    def __get_api_token(self, client_id, client_secret):
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        response = requests.post("https://api-m.sandbox.paypal.com/v1/oauth2/token", headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    def create_invoice(self, invoice_id, note, customer_email, item):
        body = {
            "detail": {
                "invoice_number": self.invoice_prefix + str(invoice_id),
                "currency_code": self.currency_code,
                "note": note
            },
            "invoicer": {
                "name": {
                    "given_name": self.vendor_given_names,
                    "surname": self.vendor_last_names
                },
                "email_address": self.vendor_email
            },
            "primary_recipients": [
                {
                    "billing_info": {
                        "email_address": customer_email
                    }
                }
            ],
            "items": [
                {
                    "name": item["name"],
                    "quantity": "1",
                    "unit_amount": {
                        "currency_code": self.currency_code,
                        "value": item['value']
                    }
                }
            ]
        }

        return requests.post(self.invoice_api_url, json=body, headers=self.headers)
    
    def send_invoice(self, invoice_id):
        body = { 
            "send_to_invoicer": True 
        }

        return requests.post(f"{self.invoice_api_url}/{invoice_id}/send", json=body, headers=self.headers)
    
    def get_invoice_details(self, invoice_id):
        return requests.get(f'{self.invoice_api_url}/{invoice_id}', headers=self.headers)

        