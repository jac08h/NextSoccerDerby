import pytest
import re
from scrapers.scraper import *


class TestDataExtraction:
    @pytest.fixture(scope='module')
    def matches_info(self):
        matches_info = []
        with open('tests/derby_urls.txt') as fp:
            for line in fp.readlines()[:3]:
                url = line.strip()
                match_info = extract_data_from_wikipedia_page(url)
                matches_info.append(match_info)
        return matches_info

    def test_presence_of_fields(self, matches_info):
        fields = ['teams', 'competition', 'date']
        for match_info in matches_info:
            for field in fields:
                assert field in match_info

    def test_correctness_of_fields(self, matches_info):
        teams_pattern = re.compile(r".*v*.")  # Team A v Team B
        date_pattern = re.compile(r"\d* \w* \d*")  # 20 February 2020

        for match_info in matches_info:
            assert re.search(teams_pattern, match_info['teams'])
            assert re.search(date_pattern, match_info['date'])
