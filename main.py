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

        dc = parser.DataCleaner()
        raw_file_data = configs.read_from_file(configs.raw_file_path)
        dc.read_raw_data(raw_file_data)
        dc.normalize()
        normalized_data = dc.get_wrangled_data()
        # dc.consolidate_aliases()

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
        print(nw.graph)
        for i in adjacency:
            if i[0] == "trip_hop":
                print(i)
            if i[0] == "lo_fi_hip_hop":
                print(i)
            if i[0] == "lofi_hip_hop":
                print(i)
            if i[0] == "downtempo":
                print(i)

        for i in nodes:
            if len(i) < 3:
                print(i)
            # if "_" in i and i.replace("_", "") in nodes:
            #     print(i)
            # print(i, [j for j in nw.graph.neighbors(i)])
            # print(i, [j[i] for j in adjacency])

        positions: dict = {}

        if "p" in sys.argv[-1]:

            positions = nw.generate_positions()
            configs.dump_to_file(configs.graph_pos_file_path, positions)

        if "d" in sys.argv[-1]:

            positions = configs.read_from_file(configs.graph_pos_file_path)
            plot = graph.PlotDraw(positions, nodes, edges, adjacency)
            plot.draw()

    # class AliasManager:
    #     def __init__(self) -> None:

    #         self.aliases: dict = {}

    #     def add_alias(self, genre_key: str, aliases: list) -> None:

    #         for alias_key in aliases:

    #             self.aliases[alias_key] = genre_key

    #     def get_genre_key(self, genre_key: str) -> str:

    #         if genre_key in self.aliases:
    #             print("found alias", genre_key, "/", self.aliases[genre_key])

    #         return self.aliases.get(genre_key, genre_key)

    # aliases = AliasManager()
    # aliases.add_alias("rock", ["a", "b", "c"])
    # aliases.add_alias("a", ["a", "b", "c"])
    # aliases.add_alias("pop", ["1", "2", "3"])
    # print(aliases.get_genre_key("rock"))
    # print(aliases.get_genre_key("a"))
    # print(aliases.get_genre_key("3"))
