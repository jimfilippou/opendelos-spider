# -*- coding: utf-8 -*-

import argparse
import json

import requests
from bs4 import BeautifulSoup
from yaspin import yaspin

data = {'lectures': []}


def main(args):
    with yaspin(text="Crawling 🕸", color="yellow") as spinner:
        pages = [requests.get("{}&sa={}".format(args.link, i + 1)) for i in range(args.pages)]
        soups = [BeautifulSoup(x.content, 'lxml') for x in pages]
        for soup in soups:
            container = soup.find("div", {"id": "detailed_view"})
            courses_wrappers = container.findChildren("div", recursive=False)
            for item in courses_wrappers:
                try:
                    title = item.find("a", {"class": "lecture-title"}).text.strip()
                    author = "Τουμπής Σταύρος"
                    code = item.find("a", {"class": "lecture-title"}).attrs['href'].split('rid=')[1]
                    data['lectures'].append({
                        'title': title,
                        'author': author,
                        'code': code
                    })
                except AttributeError:
                    break
        dump(data)
        spinner.ok("✅ ")
        spinner.write("Done!")


def dump(what):
    with open('data.txt', 'w', encoding='utf-8') as outfile:
        json.dump(what, outfile, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawler for the opendelos project.')
    parser.add_argument('--link', type=str, help='the page to crawl')
    parser.add_argument('--pages', type=int, help="how many pages to crawl")
    args = parser.parse_args()
    main(args)
