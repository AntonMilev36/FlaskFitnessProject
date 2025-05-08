import paypalrestsdk

from decouple import config


class PayPalService:
    @staticmethod
    def configure_paypal():
        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": config("CLIENT_ID"),
            "client_secret": config("PAYPAL_SECRET")
        })
