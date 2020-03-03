from app import app, db, applogger, redis_client
from app.models import Fixture, User
from app.forms import LoginForm, RegistrationForm, AddDerby

from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
def index():
    last_updated = redis_client.get('last_updated')
    return render_template('index.html', title='Next Soccer Derby', last_updated=last_updated)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/credits')
def credits():
    return render_template('credits.html')


@app.route('/fixtures', methods=['GET', 'POST'])
def fixtures():
    fixtures = Fixture.query.all()
    fixtures_data = []
    for fixture in fixtures:
        fixtures_data.append(
            (fixture.title, fixture.get_date(), fixture.get_competition(), fixture.get_team_a(), fixture.get_team_b(), fixture.get_country())
        )

    applogger.info('fixtures')
    return jsonify({"data": fixtures_data})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/control_panel', methods=['GET', 'POST'])
@login_required
def control_panel():
    if current_user.username != 'jac08h':
        return redirect(url_for('index'))

    add_derby_form = AddDerby()

    # See here for multiple forms on page: https://stackoverflow.com/a/39766205/12580224
    if add_derby_form.validate_on_submit():
        new_derby = Fixture(wikipedia_url=add_derby_form.wikipedia_url.data,
                            title=add_derby_form.title.data,
                            country=add_derby_form.country.data)
        db.session.add(new_derby)
        db.session.commit()

    return render_template('control_panel.html', title='Control Panel', add_derby_form=add_derby_form)
