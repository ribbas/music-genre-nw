#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import ConfigTools
from .scrape import WikiScraper

configs = ConfigTools()
configs.init_urls()

wiki_scraper = WikiScraper()
genres = wiki_scraper.scrape_list(configs.genre_list_url)
configs.dump_to_file(configs.genres_file, genres)
