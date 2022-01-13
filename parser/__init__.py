#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import ConfigTools
from .scrape import WikiScraper

configs = ConfigTools()
configs.init_urls()

wiki_scraper = WikiScraper()
genres = wiki_scraper.scrape_list_page(configs.genre_list_url)
print(genres)
configs.dump_to_file(configs.genres_file, genres)

# genres = configs.read_from_file(configs.genres_file)
# genres = [configs.make_wiki_url(x) for x in genres]
# wiki_scraper.scrape_genre_page(
#     ["https://en.wikipedia.org/wiki/Hardcore_(electronic_dance_music_genre)"]
# )
# wiki_scraper.scrape_genre_page(["https://en.wikipedia.org/wiki/2-step_garage"])
