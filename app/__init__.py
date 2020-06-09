from flask import Flask, abort
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap
from flask_redis import FlaskRedis
from flask_compress import Compress
import logging

app = Flask(__name__)
Compress(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
applogger = app.logger
applogger.setLevel(logging.INFO)
bootstrap = Bootstrap(app)
redis_client = FlaskRedis(app, decode_responses=True)

# used in models, probably a wrong place to initialize it
NULL_REPRESENTATION = '?'

from app import routes, models, errors


class MyIndexView(AdminIndexView):
    def is_accessible(self):
        try:
            is_admin = (current_user.username == 'jac08h')
        except AttributeError:  # no user logged in
            is_admin = False
        return is_admin

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)


admin = Admin(app, name='nextsoccerderby', template_mode='bootstrap3', index_view=MyIndexView())
admin.add_view(ModelView(models.Fixture, db.session))
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Role, db.session))
admin.add_view(ModelView(models.Article, db.session))
admin.add_view(ModelView(models.Tag, db.session))
