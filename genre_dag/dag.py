#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from config import DATA_PATH, RAW_DATA_PATH
from util import dump_json, ls_dir, read_json


class GenreDAG(object):

    def __init__(self, data):

        self.data = data
        self.nodes = set()
        self.edges = set()
        self.subgenres = {}

    def build_edges(self):

        for genre in self.data:
            for child in genre["children"]:
                self.edges.add((genre["root"], child.replace("_", " ")))
            for parent in genre["parents"]:
                self.edges.add((parent.replace("_", " "), genre["root"]))

    def include_data(self):

        for genre in self.data:
            children = genre["children"]
            self.subgenres[genre["root"]] = {
                "children": [i.replace("_", " ").title() for i in children],
                "num_children": len(children),
                "instruments": genre["instruments"]
            }

    def get_edges(self):

        return list(self.edges)

    def get_nodes(self):

        for edge in self.edges:
            self.nodes.update(edge)

        return list(self.nodes)

    def dump_dag(self):

        dump_json(
            DATA_PATH + "data.json",
            {
                "edges": self.get_edges(),
                "nodes": self.get_nodes(),
                "subgenres": self.subgenres
            }
        )


if __name__ == '__main__':

    data = ls_dir(RAW_DATA_PATH)
    data = [read_json(i) for i in data]

    obj = GenreDAG(data=data)
    obj.build_edges()
    obj.include_data()
    obj.dump_dag()
