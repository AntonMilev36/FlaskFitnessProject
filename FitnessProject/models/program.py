from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.exercise import ExerciseModel


class ProgramModel(db.Model):
    __tablename__ = "programs"
    pk: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String, nullable=False)

    exercises: Mapped["ExerciseModel"] = relationship("ExerciseModel")