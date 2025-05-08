from sqlalchemy.orm import Mapped, mapped_column

from db import db


class ProgramExercise(db.Model):
    __tablename__ = "programs_exercises"
    pk: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    program_pk = None
    exercise_pk = None
