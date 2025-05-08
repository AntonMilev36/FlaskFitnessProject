from flask import jsonify

from config import create_app
from db import db


environment = "config.DevelopmentConfig"
app = create_app(environment)


@app.teardown_request
def commit_transaction_on_teardown(exception=None):
    if exception is None:
        try:
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            return (
                jsonify(
                    {
                        "error": "An error occurred while saving data. Please try again later"
                    }
                ), 500,
            )
    else:
        db.session.rollback()
        return (
            jsonify(
                {
                    "error": "An unexpected error occurred. Please contact if the issue persists"
                }
            ), 500
        )

@app.teardown_appcontext
def shutdown_session(response, exception=None):
    db.session.remove()
    return response
