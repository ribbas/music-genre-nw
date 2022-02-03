#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


class AliasGraph:
    def __init__(self) -> None:

        self.aliases: nx.Graph = nx.Graph()

    def add_alias(self, genre_key: str, aliases: list) -> None:

        # self.aliases.add_node(genre_key)
        for alias_key in aliases:
            self.aliases.add_edge(genre_key, alias_key)

        # print("aliases", self.aliases.edges())

    def get_genre_key(self, genre_key: str) -> str:

        for node in self.aliases.adjacency():
            if node[0] == genre_key:
                print(node)

        return "fake"

        # for component in nx.weakly_connected_components(self.aliases):
        #     G_sub = self.aliases.subgraph(component)
        # print([n for n, d in G_sub.in_degree() if d == 0])

        # search_key = genre_key
        # while search_key in self.aliases.keys():
        #     print("found alias", search_key, "/", self.aliases[search_key])
        #     if search_key != self.aliases[search_key]:
        #         search_key = self.aliases[search_key]
        #     else:
        #         break
        # # else:
        # print("finally", search_key, "/", search_key)

        # return self.aliases.get(genre_key, genre_key)
