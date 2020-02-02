from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Fixture(db.Model):
    __tablename__ = 'fixtures'
    id = db.Column(db.Integer, primary_key=True)
    wikipedia_url = db.Column(db.String(200), index=True, nullable=False, unique=True)
    title = db.Column(db.String(100), index=True, nullable=False, unique=True)
    country = db.Column(db.String(50), index=True, nullable=False, unique=False)
    team_a = db.Column(db.String(100), index=True, nullable=False, unique=False)
    team_b = db.Column(db.String(100), index=True, nullable=False, unique=False)

    date = db.Column(db.DateTime, index=True, unique=False, nullable=True)
    competition = db.Column(db.String(100), index=True, nullable=False, unique=False)

    def __repr__(self):
        return f"{self.title} - next match: {self.date}"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
