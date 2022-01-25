#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DirectedAcyclicGraph:
    def __init__(self, wrangled_data: list) -> None:

        self.wrangled_data = wrangled_data
        self.graph = {}
        self.vertices = set()
        self.edges = set()

    def set_vertices(self) -> set():

        for value in self.wrangled_data:
            self.vertices.add(value["genre"])

    def get_vertices(self) -> set():

        return self.vertices
