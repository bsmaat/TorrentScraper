# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

# The PirateItem class is a class that contains the information about the possible torrent download
# TODO: add size of file

class PirateItem:

    def __init__(self, name, address, type, seeds, leechers, filesize):
        self.name = name
        self.address = address
        self.type = type
        self.seeds = seeds
        self.leechers = leechers
        self.filesize = filesize

    # Get the magnetic link of this PirateItem
    def getLink(self):
        page = requests.get(self.address);
        if (page.status_code == 200):
            soup = BeautifulSoup(page.content, 'html.parser')
            found = soup.find('div', class_='download')
            magnetLink = found.find('a')
            return magnetLink.get('href')

