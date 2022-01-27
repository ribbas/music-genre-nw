#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import le
import sys
from pprint import pprint

import parser
import graph

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
        table_normalizer.read_raw_data(raw_file_data)
        table_normalizer.normalize()
        normalized_data = table_normalizer.get_normalized_data()

        if "p" in sys.argv[-1]:
            configs.dump_to_file(
                configs.wrangled_file_path, normalized_data, pretty=True
            )

        else:
            configs.dump_to_file(configs.wrangled_min_file_path, normalized_data)

    elif sys.argv[-1][0] == "g":

        wrangled_file_data = configs.read_from_file(configs.wrangled_min_file_path)

        nw = graph.NetworkGraph(wrangled_file_data)
        nw.initialize_graph()

        nodes = nw.get_nodes()
        edges = nw.get_edges()
        adjacency = nw.get_adjacency()

        positions: dict = {}

        if "p" in sys.argv[-1]:

            positions = nw.generate_positions()
            configs.dump_to_file(configs.graph_pos_file_path, positions)

        if "d" in sys.argv[-1]:

            positions = configs.read_from_file(configs.graph_pos_file_path)
            plot = graph.PlotDraw(positions, nodes, edges, adjacency)
            plot.draw()
