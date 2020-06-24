from typing import Set
import re
from time import time

import helpers

TOPLEVEL_URLS = {
    'global': 'https://en.wikipedia.org/wiki/List_of_association_football_rivalries',
}

EUROPE_URLS = {
    'global': 'https://en.wikipedia.org/wiki/List_of_association_football_club_rivalries_in_Europe',
    'england': 'https://en.wikipedia.org/wiki/List_of_sports_rivalries_in_the_United_Kingdom#England',
    'france': 'https://en.wikipedia.org/wiki/Category:French_football_derbies',
    'germany': 'https://en.wikipedia.org/wiki/German_football_rivalries',
    'ireland': 'https://en.wikipedia.org/wiki/Derbies_in_the_League_of_Ireland',
    'italy': 'https://en.wikipedia.org/wiki/Category:Italian_football_derbies',
    'poland': 'https://en.wikipedia.org/wiki/List_of_derbies_in_Poland#Association_football',
    'spain': 'https://en.wikipedia.org/wiki/Spanish_football_rivalries',
    'sweden': 'https://en.wikipedia.org/wiki/Football_derbies_in_Sweden',
}

INFOBOX_DERBY_REGEX = re.compile(".*(Next meeting).*")
INFOBOX_DERBY_REGEX_BENEVOLENT = re.compile(".*(Locale|Teams|First meeting|Next meeting|Stadiums).*")


def relative_wiki_url_to_absolute(relative_url: str) -> str:
    return 'https://en.wikipedia.org' + relative_url


def get_wiki_urls_from_wiki_page(toplevel_url: str) -> Set[str]:
    urls = set()
    soup = helpers.make_soup(toplevel_url)
    body = soup.find('div', {'id': 'mw-content-text'})
    hyperlinks = body.find_all('a')  # 3652
    for hyperlink in hyperlinks:
        try:
            url = hyperlink['href']
            if '/wiki/' in url:
                urls.add(relative_wiki_url_to_absolute(url))
        except KeyError:
            pass
    # 1292

    return urls


def check_if_derby_wiki_page(wiki_url: str) -> bool:
    soup = helpers.make_soup(wiki_url)
    infobox = soup.find('table', {'class': 'infobox'})
    try:
        infobox_text = infobox.text
        if re.match(INFOBOX_DERBY_REGEX, infobox_text):
            return True
        else:
            return False
    except AttributeError:
        return False


if __name__ == '__main__':
    a = time()
    list_url = EUROPE_URLS['spain']
    urls = get_wiki_urls_from_wiki_page(list_url)
    for url in urls:
        if check_if_derby_wiki_page(url):
            print(url)

    print(time() - a)
