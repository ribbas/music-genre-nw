#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


class NetworkGraph:
    def __init__(self, wrangled_data: list) -> None:

        self.wrangled_data = wrangled_data
        self.graph = nx.DiGraph()
        self.edges: list = []
        self.pos: dict = {}

    def get_nodes(self) -> list:

        return self.graph.nodes()

    def get_edges(self) -> list:

        return self.graph.edges()

    def get_adjacency(self) -> list:

        return self.graph.adjacency()

    def set_nodes(self) -> None:

        for value in self.wrangled_data:
            self.graph.add_node(value["genre"], name=value["genre"])

    def set_edges(self) -> None:

        for value in self.wrangled_data:
            if "subgenres" in value:
                for genre in value["subgenres"]:
                    self.edges.append((value["genre"], genre))
            if "derivative forms" in value:
                for genre in value["derivative forms"]:
                    self.edges.append((value["genre"], genre))
            if "fusion genres" in value:
                for genre in value["fusion genres"]:
                    self.edges.append((value["genre"], genre))
            if "stylistic origins" in value:
                for genre in value["stylistic origins"]:
                    self.edges.append((genre, value["genre"]))

    def initialize_graph(self) -> None:

        self.set_nodes()
        self.set_edges()
        self.graph.add_edges_from(self.edges)
        self.graph.remove_edges_from(nx.selfloop_edges(self.graph))

    def generate_positions(self) -> dict:

        self.pos = nx.drawing.nx_agraph.graphviz_layout(self.graph, prog="dot")
        return self.pos
