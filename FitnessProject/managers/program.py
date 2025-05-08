# from flask_restful import Resource
# from werkzeug.exceptions import NotFound
#
# from db import db
# from models import ProgramExercise, ExerciseModel
# from models.program import ProgramModel
#
#
# class ProgramManager(Resource):
#     @staticmethod
#     def create_program(program_data):
#         program = ProgramModel(**program_data)
#         db.session.add(program)
#         db.session.flush()
#
#     @staticmethod
#     def get_all_programs():
#         return db.session.execute(db.select(ProgramModel)).scalars().all()
#
#     @staticmethod
#     def get_program(program_pk):
#         program = db.session.execute(db.select(ProgramModel).filter_by(pk=program_pk)).scalar_one_or_none()
#         if program is None:
#             raise NotFound
#         return program
#