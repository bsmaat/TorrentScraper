# -*- coding: utf-8 -*-

import requests
import urllib
from bs4 import BeautifulSoup
from pirateitem import PirateItem

# The pirate parser searches a pirate bay link and parses the results

class PirateParser:

    webpage = "https://tpb.tw"

    def __init__(self, piratelink):
        self.webpage = piratelink

    def __getSearchPage(self, strSearch, pageNumber):
        dicSearch = {"q": strSearch, "page": pageNumber, "orderby": "99"}
        encodedUrl = urllib.urlencode(dicSearch)
        url = self.webpage + "/s/?" + encodedUrl
        page = requests.get(url)
        return page

    def searchPage(self, strSearch, pageNumber):

        page = self.__getSearchPage(strSearch, pageNumber)
        items = []

        if (page.status_code == 200):
            soup = BeautifulSoup(page.content, 'html.parser')

            lstTdTypes = []
            # loop through each table and then each row
            for table in soup.find_all("table", id="searchResult"):
                for tr in table.find_all("tr"):
                    # find the td with the type
                    tdTypes = tr.find_all(class_="vertTh")
                    if tdTypes:
                        for td in tdTypes:
                            typeLinks = tr.find_all("a")
                            for typeLink in typeLinks:
                                lstTdTypes.append(typeLink.text)

                    tds = tr.find_all('td', {'align': 'right'})
                    if tds:
                        seeds = tds[0].text
                        leechers = tds[1].text

                    # find the div with the title of the download
                    div = tr.find(class_="detName")
                    if div:
                        link = div.find("a")
                        linkAddress = self.webpage + link.get("href")
                        item = PirateItem(link.get_text(), linkAddress, lstTdTypes, seeds, leechers)
                        items.append(item)


        else:
            print "Bad error code: " + page.status_code

        return items

    def getMagnetLink(self, url):
        page = requests.get(url)

        if (page.status_code == 200):
            soup = BeautifulSoup(page.content, 'html.parser')
            downloadDiv = soup.find('div', class_='download')
            magnetLink = downloadDiv.find('a')
            return magnetLink.get('href')
