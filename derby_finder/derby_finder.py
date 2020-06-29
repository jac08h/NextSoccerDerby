from typing import Set, Iterable
import re
from time import time
from pathlib import Path

import logic
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

if __name__ == '__main__':
    a = time()
    dir_path = Path('derby_finder/found_derbies')

    for key, toplevel_url in EUROPE_URLS.items():
        path = Path(dir_path, key +'.txt')
        if path.exists():
            pass
        else:
            valid_urls = logic.get_valid_derby_urls_from_toplevel_wiki_page(toplevel_url)
            helpers.write_iterable_to_file(valid_urls, path)
            break
