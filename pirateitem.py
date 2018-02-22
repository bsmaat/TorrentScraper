# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

class PirateItem:

    def __init__(self, name, address, type, seeds, leechers ):
        self.name = name
        self.address = address
        self.type = type
        self.seeds = seeds
        self.leechers = leechers

    def getLink(self):
        page = requests.get(self.address);
        if (page.status_code == 200):
            soup = BeautifulSoup(page.content, 'html.parser')
            found = soup.find('div', class_='download')
            magnetLink = found.find('a')
            return magnetLink.get('href')

