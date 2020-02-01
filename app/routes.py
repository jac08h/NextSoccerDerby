from flask import render_template
from app import app, db
from app.models import Fixture


@app.route('/')
@app.route('/index')
def index():
    fixtures = Fixture.query.all()
    return render_template('index.html', title='Next Soccer Derby', fixtures=fixtures)

