from app import db, applogger, redis_client
from app.models import Fixture
from scrapers import scraper
from datetime import datetime
from sys import exit

fixtures = Fixture.query.all()
for fixture in fixtures:
    try:
        fixture_info = scraper.extract_data_from_wikipedia_page(fixture.wikipedia_url)
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

redis_client.set('last_updated', datetime.now().strftime('%B %-d, %Y'))
# %-d represents a day without a leading zero, but it works only on UNIX systems
# on Windows, %#d can be used
db.session.commit()
