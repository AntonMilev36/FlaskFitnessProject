import paypalrestsdk
from decouple import config
from werkzeug.exceptions import NotFound

from db import db
from models.enums import RoleType
from models.user import UserModel
from services.paypal import PayPalService

AMOUNT = 10.00
CURRENCY = "EUR"


class PaymentManager:
    @staticmethod
    def create_payment(user_pk):
        PayPalService.configure_paypal()

        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": f"{config("CLIENT_URL")}/success?user_pk={user_pk}",
                    "cancel_url": f"{config("CLIENT_URL")}/cancel",
                },
                "transactions": [
                    {
                        "amount": {"total": f"{AMOUNT}", "currency": CURRENCY},
                        "description": "Upgrade to Superuser",
                    }
                ],
            }
        )

        if payment.create():
            return payment
        else:
            errors_info = payment.error
            return errors_info, 400

    @staticmethod
    def upgrade_user_to_superuser(user_pk):
        user = db.session.execute(
            db.select(UserModel).filter_by(pk=user_pk)
        ).scalar_one_or_none()

        if user is None:
            raise NotFound
        user.role = RoleType.super_user
        db.session.flush()
