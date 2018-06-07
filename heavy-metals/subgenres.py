#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from pprint import pprint

from config import DATA_PATH
from parsewiki import WikiSubtree
from util import read_json, file_exists


class Subgenres(object):

    def __init__(self, genre):

        self.parsed = set()
        self.queued = []
        self.root = genre

    def get_children_subtrees(self):

        self.queued.append(self.root)

        children = 0
        while children < len(self.queued):
            subgenre = self.queued[children]
            if subgenre not in self.parsed:
                subtree = WikiSubtree(endpoint=subgenre)
                subtree.generate_subtree()
                grand_children = subtree.get_subtree()["children"]
                self.queued.extend(grand_children)
                self.parsed.add(subgenre)
                children += 1

        pprint(self.parsed)


if __name__ == '__main__':

    obj = Subgenres("heavy_metal_music")
    obj.get_children_subtrees()
