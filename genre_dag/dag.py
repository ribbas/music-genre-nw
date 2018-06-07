#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from bs4 import BeautifulSoup

from config import DATA_PATH
from util import dump_json, ls_dir, read_json


class GenreDAG(object):

    def __init__(self, data):

        self.data = data
        self.nodes = set()
        self.edges = []

    def build_edges(self):

        for genre in self.data:
            for node in genre["children"]:
                self.edges.append([genre["root"], node.replace("_", " ")])
            for node in genre["parents"]:
                self.edges.append([node.replace("_", " "), genre["root"]])

    def get_edges(self):

        return self.edges

    def get_nodes(self):

        for edge in self.edges:
            self.nodes.add(edge[0])
            self.nodes.add(edge[-1])

        return list(self.nodes)

    def dump_dag(self):

        dump_json(
            DATA_PATH + "data.json",
            {"edges": self.get_edges(), "nodes": self.get_nodes()}
        )


if __name__ == '__main__':

    data = ls_dir(DATA_PATH)
    data = [read_json(i) for i in data]

    obj = GenreDAG(data=data)
    obj.build_edges()
    obj.dump_dag()
