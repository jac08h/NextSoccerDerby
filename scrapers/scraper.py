from typing import Dict
import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)


def scrape_wikipedia(wikipedia_url: str) -> Dict:
    r = requests.get(wikipedia_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    infobox = soup.find('table', {'class': 'infobox'})
    next_meeting = None
    for row in infobox.find_all_next('tr'):
        if 'Next meeting' in row.text:
            next_meeting = row.find('td')
    if not next_meeting:
        logger.error(f'No `Next meeting` info found. ({wikipedia_url},')
        return {}  # raise exception

    next_meeting_rows = list(next_meeting.childGenerator())
    try:
        teams = next_meeting_rows[0].text  # as a 'Tag' element
    except AttributeError:
        teams = next_meeting_rows[0]  # as a Text
    teams = teams.replace('v.', 'v')


if __name__ == '__main__':
    urls = ['https://en.wikipedia.org/wiki/El_Cl%C3%A1sico',
            'https://en.wikipedia.org/wiki/El_Viejo_Cl%C3%A1sico',
            'https://en.wikipedia.org/wiki/Seville_derby',
            'https://en.wikipedia.org/wiki/Athletic%E2%80%93Barcelona_cl%C3%A1sico']

    for url in urls:
        match_info = scrape_wikipedia(url)
        print(match_info)
