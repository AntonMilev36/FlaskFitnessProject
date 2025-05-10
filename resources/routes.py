from resources.auth import RegisterUser, LoginUser
from resources.exercise import CreateExercise, AllExercisesList, SpecificExercise, DeleteExercise
from resources.payment import InitiatePayment, PaymentSuccess, PaymentCancel
from resources.program import CreateProgram, AllProgramsList, SpecificProgram, DeleteProgram
from resources.trainer import CreateTrainer, DeleteTrainer
from resources.user import AddProgramToUser, UserProgramsList, UserSpecificProgram, UserDeleteProgram

routes = (
    (RegisterUser, "/register"),
    (LoginUser, "/login"),
    (CreateExercise, "/trainers/exercise"),
    (CreateProgram, "/trainers/program"),
    (AllExercisesList, "/exercise"),
    (AllProgramsList, "/program"),
    (SpecificExercise, "/exercise/<int:exercise_pk>"),
    (SpecificProgram, "/program/<int:program_pk>"),
    (AddProgramToUser, "/user/add/program/<int:program_pk>"),
    (UserProgramsList, "/user/program"),
    (UserSpecificProgram, "/user/program/<int:program_pk>"),
    (InitiatePayment, "/user/payment"),
    (PaymentSuccess, "/success"),
    (PaymentCancel, "/cancel"),
    (DeleteExercise, "/admin/delete/exercise/<int:exercise_pk>"),
    (CreateTrainer, "/admin/set/trainer/<int:user_pk>"),
    (DeleteTrainer, "/admin/remove/trainer/<int:trainer_pk>"),
    (DeleteProgram, "/admin/delete/program/<int:program_pk>"),
    (UserDeleteProgram, "/user/delete/program/<int:program_pk>")
)
