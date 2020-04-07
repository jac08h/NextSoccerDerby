from app import db, applogger, redis_client
from app.models import Fixture
from scrapers import scraper

import datetime as dt
from sys import exit

fixtures = Fixture.query.all()
today = dt.datetime.today()


for fixture in fixtures:
    try:
        fixture_info = scraper.extract_data_from_wikipedia_page(fixture.wikipedia_url)
        if fixture_info['date'] - today < dt.timedelta(0):  # scraped date already happened
            fixture.date = None
        else:
            fixture.date = fixture_info['date']

        fixture.competition = fixture_info['competition']
        fixture.team_a = fixture_info['team_a']
        fixture.team_b = fixture_info['team_b']

    except scraper.DateNotFound:
        fixture.date = None  # interpreted as NULL
        fixture.competition = None

    except Exception as e:
        applogger.error(f"{e}\n({fixture.wikipedia_url})")
        exit()

    db.session.add(fixture)

redis_client.set('last_updated', dt.datetime.now().strftime('%B %-d, %Y'))
# %-d represents a day without a leading zero, but it works only on UNIX systems
# on Windows, %#d can be used
db.session.commit()
