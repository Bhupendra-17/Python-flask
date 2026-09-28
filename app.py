import os

from flask import Flask

from models import db
from models.user import User
from routes.user_routes import users

def create_app():
    app = Flask(__name__, template_folder="template")
    database_url = os.getenv("DATABASE_URL")
    if database_url.startswith("mysql://"):
        database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(users)

    return app


app = create_app()