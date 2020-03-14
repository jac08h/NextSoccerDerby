from typing import Dict
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from app import applogger


class DateNotFound(Exception):
    pass


def extract_data_from_wikipedia_page(wikipedia_url: str) -> Dict:
    no_meeting_pattern = re.compile(r"unk. |TBA|TBD|To be confirmed")

    applogger.info(f'Scraping {wikipedia_url}')
    set_fields = {field: False for field in ['teams', 'competition', 'date']}

    r = requests.get(wikipedia_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find `Next meeting` row
    infobox = soup.find('table', {'class': 'infobox'})
    found_next_meeting = False
    for row in infobox.find_all_next('tr'):
        if 'Next meeting' in row.text:
            found_next_meeting = True
            next_meeting = row.find('td')
            next_meeting_rows = list(next_meeting.childGenerator())
    if not found_next_meeting or re.search(no_meeting_pattern, next_meeting.text):
        raise DateNotFound

    competition = date = team_a = team_b = None

    date_pattern = re.compile(r"\d\d? \w* \d{4}")
    teams_pattern = re.compile(r".+ v.? .+")
    for row in next_meeting_rows:
        # get text content from row
        try:
            row_text = row.text  # as a 'Tag' element
        except AttributeError:
            row_text = row

        # competition
        if row.name == 'a':
            competition_and_season = row.attrs['title']  # possible to use this in the future
            competition = row.text
            set_fields['competition'] = True
            continue

        # date
        date_search = re.search(date_pattern, row_text)
        if date_search:
            date_string = date_search.group(0)
            date = datetime.strptime(date_string, "%d %B %Y")
            set_fields['date'] = True
            continue
        if re.search(no_meeting_pattern, row_text):  # no date found
            raise DateNotFound

        # teams
        row_text = row_text.replace('v.', 'v')
        if re.match(teams_pattern, row_text):
            team_a, team_b = [team.strip() for team in row_text.split(' v ')]
            set_fields['teams'] = True
            continue

    if all(set_fields.values()):
        match_info = {'team_a': team_a, 'team_b': team_b, 'competition': competition, 'date': date}
        return match_info
    else:
        missing_fields = [field for field, is_set in set_fields.items() if not is_set]
        applogger.error(f"Not all fields were found.\n{soup.title.text}\nMissing fields: {', '.join(missing_fields)}")


if __name__ == '__main__':
    fi = extract_data_from_wikipedia_page('https://en.wikipedia.org/wiki/El_Cl%C3%A1sico')
    print(type(fi['date']))
