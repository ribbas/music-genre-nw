#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pprint import pprint

import parser

if __name__ == "__main__":

    configs = parser.ConfigTools()
    configs.init_urls()

    if sys.argv[-1][0] == "s":

        if "l" in sys.argv[-1]:

            genre_list_parser = parser.ParseGenreList(configs.genre_list_url)
            genre_list_parser.set_configs(configs)
            genres = genre_list_parser.parse()
            configs.dump_to_file(configs.genres_file_path, genres["genres"])

        if "t" in sys.argv[-1]:

            checkpoint = parser.Checkpoint()
            checkpoint.set_file_paths(configs)

            genre_table_parser = parser.ParseGenreTable()
            genre_table_parser.set_checkpoint(checkpoint)
            genre_table_parser.parse()

    elif sys.argv[-1][0] == "c":

        table_normalizer = parser.TableNormalizer()
        raw_file_data = configs.read_from_file(configs.raw_file_path)
        print(len(raw_file_data))
        table_normalizer.read_raw_data(raw_file_data)
        table_normalizer.normalize()
