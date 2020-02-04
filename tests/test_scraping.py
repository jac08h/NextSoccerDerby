import pytest
from scrapers.scraper import *


class TestDataExtraction:
    @pytest.fixture(scope='module')
    def matches_info(self):
        matches_info = []
        with open('tests/derby_urls.txt') as fp:
            for line in fp.readlines()[:5]:
                url = line.strip()
                match_info = extract_data_from_wikipedia_page(url)
                matches_info.append(match_info)
        return matches_info

    def test_presence_of_fields(self, matches_info):
        fields = ['team_a', 'team_b', 'competition', 'date']
        for match_info in matches_info:
            for field in fields:
                assert field in match_info
                assert match_info[field] is not None

    def test_date_valid(self, matches_info):
        for match_info in matches_info:
            assert isinstance(match_info['date'], datetime)
