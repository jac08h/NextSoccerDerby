from app import db


class Fixture(db.Model):
    __tablename__ = 'fixtures'
    id = db.Column(db.Integer, primary_key=True)
    wikipedia_url = db.Column(db.String(200), index=True, nullable=False, unique=True)
    title = db.Column(db.String(100), index=True, nullable=False, unique=True)
    country = db.Column(db.String(50), index=True, nullable=False, unique=False)
    team_a = db.Column(db.String(100), index=True, nullable=False, unique=False)
    team_b = db.Column(db.String(100), index=True, nullable=False, unique=False)

    date = db.Column(db.DateTime, index=True, unique=False, nullable=True)
    competition = db.Column(db.String(100), index=True, nullable=False, unique=True)

    def __repr__(self):
        return f"{self.title} - next match: {self.date}"
