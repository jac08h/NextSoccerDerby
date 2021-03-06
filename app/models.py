from app import db, login, NULL_REPRESENTATION
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from typing import List
import datetime as dt


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


user_roles = db.Table('user_roles',
                      db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
                      )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(), unique=True, index=True)

    def __repr__(self):
        return f"{self.role_name}"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                            backref=db.backref('members', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role_name in role.role_name:
                return True
        return False

    def is_journalist(self):
        return self.check_role('journalist')

    def is_admin(self):
        return self.check_role('admin')


article_tags = db.Table('article_tags',
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                        db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
                        )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True)

    def __repr__(self):
        return self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True)
    subtitle = db.Column(db.String(280))
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edited_timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    tags = db.relationship('Tag', secondary=article_tags, lazy='subquery',
                           backref=db.backref('articles', lazy=True))
    is_public = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    def get_article_paragraphs(self) -> List[str]:
        paragraphs = [p for p in self.body.split('\n')]
        return paragraphs

    def has_subtitle(self) -> bool:
        if self.subtitle is not None and len(self.subtitle) > 0:
            return True

    def get_posted_date(self):
        return self.format_date(self.timestamp)

    def get_edited_date(self) -> str or None:
        if self.edited_timestamp is not None:
            return self.format_datetime(self.edited_timestamp)
        else:
            return None

    def format_date(self, date:dt.datetime) -> str:
        return date.strftime('%B %-d, %Y')

    def format_datetime(self, date:dt.datetime) -> str:
        return date.strftime('%B %-d, %Y %H:%M')



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
