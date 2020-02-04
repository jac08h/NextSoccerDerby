from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Fixture, User
from app.forms import LoginForm, RegistrationForm, UpdateDates, AddDerby
from flask_login import current_user, login_user, logout_user
from scrapers import scraper


@app.route('/')
@app.route('/index')
def index():
    fixtures = Fixture.query.all()
    return render_template('index.html', title='Next Soccer Derby', fixtures=fixtures)


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
def control_panel():
    try:
        if current_user.username != 'jac08h':
            return redirect(url_for('index'))
    except AttributeError:
        return redirect(url_for('index'))

    update_dates_form = UpdateDates()
    add_derby_form = AddDerby()

    # the first boolean in if statement must preceed the second,
    # otherwise the form wouldn't work properly
    # See: https://stackoverflow.com/a/39766205/12580224
    if add_derby_form.submit.data and add_derby_form.validate_on_submit():
        new_derby = Fixture(wikipedia_url=add_derby_form.wikipedia_url.data,
                            title=add_derby_form.title.data,
                            country=add_derby_form.country.data)
        db.session.add(new_derby)
        db.session.commit()

    if update_dates_form.update_dates.data and update_dates_form.validate_on_submit():
        fixtures = Fixture.query.all()
        for fixture in fixtures:
            # TODO: Temporary fix - I'd prefer the logs to come from scraper.extract_data_from_wikipedia_page directly
            app.logger.info(f'Scraping {fixture.wikipedia_url}.')
            fixture_info = scraper.extract_data_from_wikipedia_page(fixture.wikipedia_url)
            fixture.date = fixture_info['date']
            fixture.competition = fixture_info['competition']
            fixture.team_a = fixture_info['team_a']
            fixture.team_b = fixture_info['team_b']

            db.session.add(fixture)
        db.session.commit()

    return render_template('control_panel.html', title='Control Panel', add_derby_form=add_derby_form,
                           update_dates_form=update_dates_form)
