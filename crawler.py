# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json


class TwitterTVTrafficCrawler(object):

    url = 'https://www.quantcast.com/twitch.tv/traffic'
    results = {}

    def get_data(self):
        if not self.results:
            self.get_country_list()
            for country in self.country_list:
                page = self.get_page_for_country(country)
                info = self.get_info_from_page(page)
                self.results[country] = info
        return self.results

    def get_country_list(self):
        raw_page = requests.get(self.url, data={'country': 'CN'})
        page = BeautifulSoup(raw_page.text, 'html.parser')
        raw_country_list_string = page.find(key='countryList').contents[0]
        raw_country_list = json.loads(raw_country_list_string)
        self.country_list = [country['code'] for country in raw_country_list]

    def get_page_for_country(self, country):
        raw_page = requests.get(self.url, data={'country': country})
        page = BeautifulSoup(raw_page.text, 'html.parser')
        return page

    def get_info_from_page(self, page):
        raw_metric = page.find(key='profileSummary').contents[0]
        return json.loads(raw_metric).get('metrics')

if __name__ == '__main__':
    crawler = TwitterTVTrafficCrawler()
    with open('metrics.json', 'w') as f:
        data = crawler.get_data()
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
