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
    except Exception as e:
        applogger.error(f"{e}\n({fixture.wikipedia_url})")
        exit()
    db.session.add(fixture)

redis_client.set('last_updated', datetime.now().strftime('%Y-%m-%d %H:%M'))
db.session.commit()