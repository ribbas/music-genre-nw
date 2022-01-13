#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from .config import ConfigTools
from .scrape import WikiScraper

configs = ConfigTools()
configs.init_urls()

wiki_scraper = WikiScraper()
# genres = wiki_scraper.scrape_list_page(configs.genre_list_url)
# configs.dump_to_file(configs.genres_file, genres)

genres = configs.read_from_file(configs.genres_file)
genres = [{**i, "url": configs.make_wiki_url(i["url"])} for i in genres]

test_data = []
for i in genres:
    if i["key"] == "hardcore" or i["key"] == "2-step garage":
        test_data.append(i)

print(test_data)
lol = wiki_scraper.scrape_genre_page(test_data)
pprint(lol)
