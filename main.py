#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

import parser

if __name__ == "__main__":

    configs = parser.ConfigTools()
    configs.init_urls()

    genre_list_parser = parser.ParseGenreList(configs.genre_list_url)
    genres = genre_list_parser.parse()
    print(genres)
    configs.dump_to_file(configs.genres_file_path, genres["genres"])

    checkpoint = parser.Checkpoint()
    checkpoint.set_file_paths(configs.genres_file_path, configs.checkpoint_file_path)
    genres = checkpoint.get_genres()
    checkpoint.load()

    genres = [{**i, "url": configs.make_wiki_url(i["url"])} for i in genres]
    test_data = []
    for i in genres:
        if any(g == i["key"] for g in {"hardcore", "2-step garage", "chamber pop"}):
            test_data.append(i)

    print(test_data)
    genre_table_parser = parser.ParseGenreTable(test_data)
    test_data = genre_table_parser.parse()
    pprint(test_data)
