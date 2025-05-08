from enum import Enum


class RoleType(Enum):
    user = "user"
    super_user = "super user"
    trainer = "trainer"
    admin = "admin"


class ExerciseType(Enum):
    heavy_compound = "Heavy compound"
    isolation_exercise = "Isolation exercise"
