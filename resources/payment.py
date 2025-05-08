from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.payment import PaymentManager
from models import UserModel
from models.enums import RoleType
from utils.decorators import permission_required


class InitiatePayment(Resource):
    @auth.login_required
    @permission_required([RoleType.user])
    def get(self):
        user: UserModel = auth.current_user()
        payment = PaymentManager.create_payment(user.pk)
        approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
        return {"approval_url": approval_url}


class PaymentSuccess(Resource):
    @staticmethod
    def get():
        user_pk = request.args.get("user_pk")
        PaymentManager.upgrade_user_to_superuser(user_pk)
        return {"message": "You have been upgraded to superuser!"}, 202


class PaymentCancel(Resource):
    @staticmethod
    def get():
        return {"message": "Payment was cancelled."}, 402
