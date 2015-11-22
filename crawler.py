# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json


class TwitterTVTrafficCrawler(object):

    url = 'https://www.quantcast.com/twitch.tv/traffic'

    def get_data(self):
        country_list = self._get_country_list()
        results = {}
        for country in country_list:
            results[country] = self._get_info_of_country(country)
        return results

    def _get_country_list(self):
        page = self._get_page_for_country('CN')
        raw_country_list = page.find(key='countryList').contents[0]
        country_list = json.loads(raw_country_list)
        return [country.get('code') for country in country_list]

    def _get_info_of_country(self, country):
        page = self._get_page_for_country(country)
        raw_metrics = page.find(key='profileSummary').contents[0]
        return json.loads(raw_metrics).get('metrics')

    def _get_page_for_country(self, country):
        raw_page = requests.get(self.url, params={'country': country})
        return BeautifulSoup(raw_page.text, 'html.parser')

if __name__ == '__main__':
    crawler = TwitterTVTrafficCrawler()
    with open('metrics.json', 'w') as f:
        data = crawler.get_data()
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
