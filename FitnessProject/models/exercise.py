from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import db
from models.enums import ExerciseType
from models.program import ProgramModel


class ExerciseModel(db.Model):
    __tablename__ = "exercises"
    pk: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(db.String, nullable=False)
    video_tutorial: Mapped[str] = mapped_column(db.String, nullable=True)
    exercise_type: Mapped[ExerciseType] = mapped_column(db.Enum(ExerciseType),
                                                        server_default="heavy_compound",
                                                        default=ExerciseType.heavy_compound.name)
    author: Mapped[str] = mapped_column(db.String(201), nullable=False)

    programs: Mapped["ProgramModel"] = relationship("ProgramModel")