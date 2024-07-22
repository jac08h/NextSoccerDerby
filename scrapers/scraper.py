import csv
from datetime import datetime
from pathlib import Path
import re
from typing import Dict

from bs4 import BeautifulSoup
import requests

from app import applogger
from app import db
from app.models import Fixture


class DateNotFound(Exception):
    pass


no_meeting_pattern = re.compile(r"unk. |TBA|TBD|To be confirmed")
date_pattern = re.compile(r"\d\d? \w* \d{4}")
teams_pattern = re.compile(r"(.*)( - | v | (vs) )(.*)")


def extract_data_from_wikipedia_page(wikipedia_url: str) -> Dict:
    applogger.info(f'Scraping {wikipedia_url}')

    match_info = {}

    r = requests.get(wikipedia_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    match_info['title'] = soup.find('h1', {'id': 'firstHeading'}).text

    # Find `Next meeting` row
    infobox = soup.find('table', {'class': 'infobox'})
    found_next_meeting = False
    for row in infobox.find_all_next('tr'):
        if 'Next meeting' in row.text:
            found_next_meeting = True
            next_meeting = row.find('td')
            next_meeting_rows = list(next_meeting.childGenerator())
    if not found_next_meeting or re.search(no_meeting_pattern, next_meeting.text):
        return match_info

    for row in next_meeting_rows:
        # get text content from row
        try:
            row_text = row.text  # as a 'Tag' element
        except AttributeError:
            row_text = row

        # competition
        if row.name == 'a':
            match_info['competition'] = row.text
            continue

        # date
        date_search = re.search(date_pattern, row_text)
        if date_search:
            date_string = date_search.group(0)
            match_info['date'] = datetime.strptime(date_string, "%d %B %Y")
            continue

        # teams
        row_text = row_text.replace('v.', 'v')
        match = re.match(teams_pattern, row_text)
        if match:
            match_info['team_a'] = match.group(1)
            match_info['team_b'] = match.group(4)
            continue

    return match_info


def update_db(matches_csv: Path) -> None:
    with open(matches_csv, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)  # Read all lines into a list

    for row in rows[1:]:  # Skip the header
        url, country = row
        fixture = Fixture.query.filter_by(wikipedia_url=url).first()
        if fixture:  # If the URL is not present in the database
            continue
        try:
            match_info = extract_data_from_wikipedia_page(url)

            if any(key not in match_info for key in ['team_a', 'team_b', 'competition', 'title']):
                applogger.error(f"One or more required keys missing for {url}")
                continue

            if 'date' not in match_info:
                match_info['date'] = None

            new_fixture = Fixture(
                wikipedia_url=url,
                country=country,
                team_a=match_info['team_a'],
                team_b=match_info['team_b'],
                competition=match_info['competition'],
                date=match_info['date'],
                title=match_info['title']
            )
            db.session.add(new_fixture)
            applogger.info(f"Added {new_fixture.title}")

        except Exception as e:
            applogger.error(f"Other error: {e} for {url}")
    db.session.commit()


if __name__ == '__main__':
    import datetime as dt

    today = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    update_db(Path('derby_urls.txt'))
