import factory
from factory.base import T
from werkzeug.security import generate_password_hash

from db import db
from models import UserModel, RoleType, ExerciseModel, ExerciseType, ProgramModel


class BaseFactory(factory.Factory):

    @classmethod
    def create(cls, **kwargs) -> T:
        factory_object = super().create(**kwargs)

        if hasattr(factory_object, "password"):
            pass_obj = factory_object.password
            factory_object.password = generate_password_hash(
                pass_obj,
                method="pbkdf2:sha256"
            )

        db.session.add(factory_object)
        db.session.flush()
        return factory_object


class UserFactory(BaseFactory):

    class Meta:
        model = UserModel

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = RoleType.user


class ExerciseFactory(BaseFactory):
    class Meta:
        model = ExerciseModel

    name = factory.Faker("word")
    description = ("Some description about the exercise "
                   "that is longer than 50 characters")
    photo_tutorial = "photo_url"
    video = "video_url"
    exercise_type = ExerciseType.heavy_compound
    author = factory.Faker("first_name")


class ProgramFactory(BaseFactory):
    class Meta:
        model = ProgramModel

    title = "Full Body"


    @factory.post_generation
    def exercise(self, create, extended=None, **kwargs):
        if not create:
            return

        #self.exercises is the ProgramModel attribute
        self.exercises.append(
            ExerciseFactory()
        )

        if extended is not None:
            for curr_exercise in extended:
                self.exercises.append(curr_exercise)
