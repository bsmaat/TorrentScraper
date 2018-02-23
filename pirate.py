# -*- coding: utf-8 -*-
import click

from pirateparser import PirateParser
from bcolors import bcolors
from subprocess import call
import itertools

@click.command()
@click.option('--search','-s', prompt='Search string', help='The search string')
@click.option('--webpage','-w', default='https://tpb.tw', help='The pirate bay site')
def start(search, webpage):
    strIntro = "PirateBay Downloader, by TheFreePhysicist"

    pirate = PirateParser(webpage)

    items = []

    pageNumber = 0

    click.echo(strIntro)
    click.echo("URL: " + pirate.webpage)

    click.echo("Search term: " + search)

    success = True
    while (True):
        if (success):
            newItems = pirate.searchPage(search, pageNumber)
            items.extend(newItems)
            printResults(items)

        index = getSearchIndex()
        if (index == InputResult.Next):
            success = True
            pageNumber = pageNumber + 1
            continue
        elif (index == InputResult.Search):
            items.clear()
            pageNumber = 0
            search = getSearchInput()
            continue
        elif (index == InputResult.Exit):
            exitProgram()

        try:
            downloadId = int(index)
            magnetLink = items[downloadId].getLink()
            call(["deluge-console", "add", magnetLink])
        except ValueError:
            print "Incorrect index!"
            success = False
            continue

class InputResult(object):
    Exit = 0
    Next = 1
    Search = 2

def getSearchInput():
    consoleInput = raw_input("Enter search string: ")
    return checkInput(consoleInput)

def checkInput(consoleInput):
    if (consoleInput == "exit"):
        return InputResult.Exit
        #return InputResult.Exit
    elif (consoleInput == "next"):
        return InputResult.Next
    elif (consoleInput == "search"):
        return InputResult.Search
    else:
        return consoleInput

def printResults(items):
    data = []
    for i in range(0, len(items)):
        row = [items[i].name, items[i].type[0], items[i].seeds, items[i].leechers]
        data.append(row)

    widths = [max(map(len, col)) for col in zip(*data)]

    headers = ["ID", "Name", "Type", "Seeds", "Leechers"]
    idWidth = 10;

    widths.insert(0, idWidth)

    print "  ".join(itertools.chain((bcolors.BOLD + val.ljust(width) + bcolors.ENDC for val, width in zip(headers, widths))))

    for i in range(0, len(items)):
        theStr = (bcolors.OKGREEN + ('[' + str(i) + ']').ljust(idWidth) + bcolors.ENDC)
        iterch = itertools.chain([theStr], data[i])
        print "  ".join((val.ljust(width) for val, width in zip(iterch, widths)))

def getSearchIndex():
    consoleInput = raw_input("Enter id: ")
    return checkInput(consoleInput)

def exitProgram():
    print "Exiting..."
    exit()

if __name__ == '__main__':
    start()