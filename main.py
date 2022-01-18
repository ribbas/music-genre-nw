#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

import parser

if __name__ == "__main__":

    configs = parser.ConfigTools()
    configs.init_urls()

    wiki_scraper = parser.WikiScraper()
    # genres = wiki_scraper.scrape_list_page(configs.genre_list_url)
    # configs.dump_to_file(configs.genres_file_path, genres)

    genres = configs.get_genres()
    configs.load_checkpoint()
    # genres = [{**i, "url": configs.make_wiki_url(i["url"])} for i in genres]

    # test_data = []
    # for i in genres:
    #     if any(g == i["key"] for g in {"hardcore", "2-step garage", "chamber pop"}):
    #         test_data.append(i)

    # print(test_data)
    # test_data = wiki_scraper.scrape_genre_pages(test_data)
    # pprint(test_data)
