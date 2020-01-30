from typing import Dict
import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)


def get_page_content(url: str) -> bytes:
    r = requests.get(url)
    return r.content


def extract_data_from_wikipedia_page(page_content: bytes) -> Dict:
    teams_ok = competition_ok = date_ok = False
    soup = BeautifulSoup(page_content, 'html.parser')
    infobox = soup.find('table', {'class': 'infobox'})
    next_meeting = None
    for row in infobox.find_all_next('tr'):
        if 'Next meeting' in row.text:
            next_meeting = row.find('td')
    if not next_meeting:
        logger.error(f'No `Next meeting` info found.')
        return {}  # raise exception
    next_meeting_rows = list(next_meeting.childGenerator())

    try:
        teams = next_meeting_rows[0].text  # as a 'Tag' element
    except AttributeError:
        teams = next_meeting_rows[0]  # as a Text
    teams = teams.replace('v.', 'v')
    teams_pattern = re.compile('.*v*.')
    if re.match(teams_pattern, teams):
        teams_ok = True

    competition = date = None
    date_pattern = re.compile("\((.*)\)")
    for i, row in enumerate(next_meeting_rows[1:]):
        if row.name == 'a':
            competition_and_season = row.attrs['title']
            competition = row.text
            competition_ok = True
            continue

        row = str(row)
        date_search = re.search(date_pattern, row)
        if date_search:
            date = date_search.group(1)
            date_ok = True

    if teams_ok and competition_ok and date_ok:
        match_info = {'teams': teams, 'competition': competition, 'date': date}
        return match_info
    else:
        logger.error(f'Not all fields were found.\n{soup.title.text}')

    """
    competition - text in a hyperlink
    date - enclosed with parens
    """


def read_website_from_file(filename: str):
    with open(filename, 'rb') as fp:
        file_contents = fp.read()
    return file_contents


if __name__ == '__main__':
    urls = []
    with open('derby_urls.txt') as fp:
        for line in fp.readlines():
            url = line.strip()
            urls.append(url)

    el_clasico_content = read_website_from_file('el_clasico.html')
    derby_ditalia_content = read_website_from_file('derby_ditalia.html')
    for url in urls:
        mi = extract_data_from_wikipedia_page(get_page_content(url))
        print(mi)
