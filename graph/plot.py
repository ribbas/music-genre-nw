#!/usr/bin/env python
# -*- coding: utf-8 -*-


import plotly.graph_objects as go
import networkx as nx


class GraphPlot:
    def __init__(self, wrangled_data: list) -> None:

        self.wrangled_data = wrangled_data
        self.graph = nx.DiGraph()
        self.nodes = set()
        self.edges: list = []

    def set_nodes(self) -> set():

        for value in self.wrangled_data:
            self.nodes.add(value["genre"])

    def get_nodes(self) -> set():

        return self.nodes

    def set_edges(self) -> set():

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

        self.set_edges()
        self.graph.add_edges_from(self.edges)
        print(nx.is_directed(self.graph))
        print(nx.is_directed_acyclic_graph(self.graph))
        print(self.graph)

    def initialize(self):

        pos = nx.drawing.nx_agraph.graphviz_layout(self.graph, prog="dot")
