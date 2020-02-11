from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
from flask_redis import FlaskRedis
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name='nextsoccerderby')
login = LoginManager(app)
applogger = app.logger
applogger.setLevel(logging.INFO)
bootstrap = Bootstrap(app)
redis_client = FlaskRedis(app, decode_responses=True)

from app import routes, models


class ModelViewModified(ModelView):
    def is_accessible(self):
        try:
            is_admin = (current_user.username == 'jac08h')
        except AttributeError:
            is_admin = False
        return is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


admin.add_view(ModelViewModified(models.Fixture, db.session))
admin.add_view(ModelViewModified(models.User, db.session))
