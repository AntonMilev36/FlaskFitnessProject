from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
CORS(app)

@app.teardown_appcontext
def close_request(response):
    db.session.commit()
    return response

[api.add_resource(*route) for route in routes]
