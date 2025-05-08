from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db


class ProgramModel(db.Model):
    __tablename__ = "programs"
    pk: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)

    exercises = relationship("ExerciseModel",
                             secondary="programs_exercises",
                             back_populates="programs")
    users = relationship("UserModel",
                         secondary="users_programs",
                         back_populates="programs")
