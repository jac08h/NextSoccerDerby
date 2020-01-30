import pytest
from scrapers.scraper import *


@pytest.mark.offline
def test_offline_data_extraction():
    fields = ['teams', 'competition', 'date']

    el_clasico_filename = 'scrapers/el_clasico.html'
    el_clasico_content = read_website_from_file(el_clasico_filename)
    el_clasico_info = extract_data_from_wikipedia_page(el_clasico_content)

    derby_ditalia_filename = 'scrapers/derby_ditalia.html'
    derby_ditalia_content = read_website_from_file(derby_ditalia_filename)
    derby_ditalia_info = extract_data_from_wikipedia_page(derby_ditalia_content)

    for field in fields:
        assert field in el_clasico_info
        assert field in derby_ditalia_info

