from app import db, login, NULL_REPRESENTATION
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class Fixture(db.Model):
    __tablename__ = 'fixtures'
    id = db.Column(db.Integer, primary_key=True)
    wikipedia_url = db.Column(db.String(200), index=True, nullable=False, unique=True)
    title = db.Column(db.String(100), index=True, unique=True)
    country = db.Column(db.String(50), index=True, unique=False)
    team_a = db.Column(db.String(100), index=True, unique=False)
    team_b = db.Column(db.String(100), index=True, unique=False)

    date = db.Column(db.DateTime, index=True, unique=False)
    competition = db.Column(db.String(100), index=True, unique=False)

    is_active = db.Column(db.Boolean, default=True)

    def get_country(self):
        if self.country is None:
            return NULL_REPRESENTATION
        return self.country

    def get_team_a(self):
        if self.team_a is None:
            return NULL_REPRESENTATION
        return self.team_a

    def get_team_b(self):
        if self.team_b is None:
            return NULL_REPRESENTATION
        return self.team_b

    def get_date(self):
        if self.date is None:
            return NULL_REPRESENTATION
        return self.date.strftime('%Y-%m-%d')

    def get_competition(self):
        if self.competition is None:
            return NULL_REPRESENTATION
        return self.competition

    def get_teams(self):
        return f'{self.team_a} - {self.team_b}'

    def get_wikipedia_url(self):
        return f"<a href= {self.wikipedia_url} target='_blank'>{self.title} - Wikipedia</a>"

    def __repr__(self):
        return f"{self.title} - next match: {self.date}"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
