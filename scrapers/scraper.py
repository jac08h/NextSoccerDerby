from typing import Dict
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from app import applogger


class DateNotFound(Exception):
    pass


def extract_data_from_wikipedia_page(wikipedia_url: str) -> Dict:
    applogger.info(f'Scraping {wikipedia_url}')
    teams_ok = competition_ok = date_ok = False
    r = requests.get(wikipedia_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find Next meeting row
    infobox = soup.find('table', {'class': 'infobox'})
    found_next_meeting = False
    for row in infobox.find_all_next('tr'):
        if 'Next meeting' in row.text:
            found_next_meeting = True
            next_meeting = row.find('td')
            next_meeting_rows = list(next_meeting.childGenerator())
    if not found_next_meeting:
        raise DateNotFound

    # Find teams names
    competition = date = team_a = team_b = None
    try:
        teams = next_meeting_rows[0].text  # as a 'Tag' element
    except AttributeError:
        teams = next_meeting_rows[0]  # as a Text
    teams = teams.replace('v.', 'v')
    teams_pattern = re.compile('.*v*.')
    if re.match(teams_pattern, teams):
        team_a, team_b = [team.strip() for team in teams.split(' v ')]
        teams_ok = True

    # Find date and competition
    date_pattern = re.compile(r"\((.*)\)")
    for i, row in enumerate(next_meeting_rows[1:]):
        if row.name == 'a':
            competition_and_season = row.attrs['title']  # possible to use this in the future
            competition = row.text
            competition_ok = True
            continue

        row = str(row)
        date_search = re.search(date_pattern, row)
        if date_search:
            date_string = date_search.group(1)
            date = datetime.strptime(date_string, "%d %B %Y")
            date_ok = True

    if teams_ok and competition_ok and date_ok:
        match_info = {'team_a': team_a, 'team_b': team_b, 'competition': competition, 'date': date}
        return match_info
    else:
        applogger.error(f'Not all fields were found.\n{soup.title.text}')


if __name__ == '__main__':
    fi = extract_data_from_wikipedia_page('https://en.wikipedia.org/wiki/El_Cl%C3%A1sico')
    print(type(fi['date']))
