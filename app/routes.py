from app import app, db, applogger, redis_client
from app.models import Fixture, User, Article
from app.forms import LoginForm, RegistrationForm, AddDerby, PostArticleForm, EditArticleForm

from flask import render_template, flash, redirect, url_for, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
import datetime as dt


@app.route('/')
@app.route('/index')
def index():
    last_updated = redis_client.get('last_updated')
    return render_template('index.html', last_updated=last_updated)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')


@app.route('/credits')
def credits():
    return render_template('credits.html', title='Credits')


@app.route('/all_fixtures')
def all_fixtures():
    fixtures = Fixture.query.all()
    fixtures_info = []
    for fixture in fixtures:
        if fixture.is_active:
            if fixture.date is None:
                fixtures_info.append((fixture.title, False))
            else:
                fixtures_info.append((fixture.title, True))

    return render_template('all_fixtures.html', title='All Fixtures', fixtures_info=sorted(fixtures_info))


@app.route('/fixtures', methods=['GET', 'POST'])
def fixtures():
    fixtures = Fixture.query.all()
    fixtures_data = []
    for fixture in fixtures:
        if (fixture.date is not None) and (fixture.is_active is None or fixture.is_active):
            fixtures_data.append(
                {
                    'date': fixture.get_date(),
                    'competition': fixture.get_competition(),
                    'country': fixture.get_country(),
                    'title': fixture.title,
                    'teams': fixture.get_teams(),
                    'wikipedia_url': fixture.get_wikipedia_url(),
                })
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


@app.route('/add_derby', methods=['GET', 'POST'])
@login_required
def add_derby():
    if current_user.username != 'jac08h':
        return redirect(url_for('index'))

    add_derby_form = AddDerby()

    # See here for multiple forms on page: https://stackoverflow.com/a/39766205/12580224
    if add_derby_form.validate_on_submit():
        new_derby = Fixture(wikipedia_url=add_derby_form.wikipedia_url.data,
                            country=add_derby_form.country.data)
        db.session.add(new_derby)
        db.session.commit()
        return redirect(url_for('add_derby'))

    return render_template('add_derby.html', title='Add Derby', add_derby_form=add_derby_form)

# @app.route('/edit_article/<article_id>', methods=['GET', 'POST'])
# def edit_article(article_id):
#     article = Article.query.filter_by(id=article_id).first_or_404()
#     if not (current_user.is_authenticated and (current_user.is_admin() or current_user is article.author)):
#         return render_template('403.html'), 403
#     form = EditArticleForm()
#     if form.validate_on_submit():
#         article.title = form.title.data
#         article.subtitle = form.subtitle.data
#         article.body = form.body.data
#         article.edited_timestamp = dt.datetime.now()
#         db.session.commit()
#         flash('Saved')
#         return redirect(url_for('edit_article', article_id=article.id))
#     elif request.method == 'GET':
#         form.title.data = article.title
#         form.subtitle.data = article.subtitle
#         form.body.data = article.body
#
#     return render_template('edit_article.html', form=form)

@app.route('/post_article', methods=['GET', 'POST'])
@login_required
def post_article():
    post_article_form = PostArticleForm()
    if post_article_form.validate_on_submit():
        new_article = Article(title=post_article_form.title.data,
                              body=post_article_form.body.data,
                              user_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('article', article_id=new_article.id))

    return render_template('post_article.html', title='Post Article', form=post_article_form)


@app.route('/articles')
def articles():
    articles = Article.query.filter_by(is_public=True).order_by(Article.timestamp.desc())
    return render_template('articles.html', title='Articles', articles=articles)


@app.route('/article/<article_id>')
def article(article_id):
    article = Article.query.filter_by(id=article_id).first_or_404()
    if not article.is_public and current_user != article.author:
        return render_template('404.html'), 404
    return render_template('article.html', article=article)


@app.route('/edit_article/<article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    article = Article.query.filter_by(id=article_id).first_or_404()
    if not (current_user.is_authenticated and (current_user.is_admin() or current_user is article.author)):
        return render_template('403.html'), 403
    form = EditArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.subtitle = form.subtitle.data
        article.body = form.body.data
        article.edited_timestamp = dt.datetime.now()
        db.session.commit()
        flash('Saved')
        return redirect(url_for('edit_article', article_id=article.id))
    elif request.method == 'GET':
        form.title.data = article.title
        form.subtitle.data = article.subtitle
        form.body.data = article.body

    return render_template('edit_article.html', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.is_journalist():
        return render_template('user.html', user=user)

    else:
        return render_template('404.html'), 404
