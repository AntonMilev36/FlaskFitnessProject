from sqlalchemy.orm import Mapped, mapped_column

from db import db


class ProgramExercise(db.Model):
    __tablename__ = "programs_exercises"
    # pk: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    program_pk: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("programs.pk"), primary_key=True)
    exercise_pk: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("exercises.pk"), primary_key=True)


class UserProgram(db.Model):
    __tablename__ = "users_programs"
    user_pk: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.pk"), primary_key=True)
    program_pk: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("programs.pk"), primary_key=True)
