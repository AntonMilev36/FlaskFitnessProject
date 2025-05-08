from flask_restful import Resource

from managers.auth import auth
from managers.trainer import TrainerManager
from models import RoleType
from utils.decorators import permission_required


class CreateTrainer(Resource):
    @auth.login_required
    @permission_required([RoleType.admin])
    def put(self, user_pk):
        TrainerManager.change_role(user_pk)
        return 204
