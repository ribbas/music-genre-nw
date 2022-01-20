#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

import parser

if __name__ == "__main__":

    configs = parser.ConfigTools()
    configs.init_urls()

    genre_list_parser = parser.ParseGenreList(configs.genre_list_url)
    genre_list_parser.set_configs(configs)
    genres = genre_list_parser.parse()
    configs.dump_to_file(configs.genres_file_path, genres["genres"])

    checkpoint = parser.Checkpoint()
    checkpoint.set_file_paths(
        configs.genres_file_path, configs.checkpoint_file_path, configs.raw_file_path
    )

    genre_table_parser = parser.ParseGenreTable()
    genre_table_parser.set_checkpoint(checkpoint)
    genre_tables = genre_table_parser.parse()
    configs.dump_to_file(configs.raw_file_path, genre_tables)
    pprint(genre_tables)
