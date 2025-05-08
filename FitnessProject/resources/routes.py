from resources.auth import RegisterUser, LoginUser
from resources.exercise import CreateExercise, AllExercisesList, SpecificExercise
# from resources.program import CreateProgram, AllProgramsList, SpecificProgram

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateExercise, "/trainers/exercise"),
    # (CreateProgram, "/trainers/program"),
    (AllExercisesList, "/exercise"),
    # (AllProgramsList, "/program"),
    (SpecificExercise, "/exercise/<int:exercise_pk>"),
    # (SpecificProgram, "/program/<int:program_pk>"),
)
