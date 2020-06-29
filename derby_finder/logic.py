from typing import Set, Iterable
import re

import helpers

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


def get_valid_derby_urls_from_toplevel_wiki_page(toplevel_url: str) -> Set[str]:
    valid_urls = set()
    urls_list = toplevel_url
    urls = get_wiki_urls_from_wiki_page(urls_list)

    print(len(urls))
    for (i, url) in enumerate(urls):
        print(i)
        try:
            if check_if_derby_wiki_page(url):
                valid_urls.add(url)
        except Exception as e:
            print(url, e)

    return valid_urls
