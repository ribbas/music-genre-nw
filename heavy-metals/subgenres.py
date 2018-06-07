#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from pprint import pprint
from time import sleep
from random import uniform

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
            wait = uniform(0.0, 2)
            sleep(wait)
            if subgenre not in self.parsed:
                subtree = WikiSubtree(endpoint=subgenre)
                subtree.generate_subtree()
                grand_children = list(
                    set(subtree.get_subtree()["children"]) - set(self.queued))
                self.queued.extend(grand_children)
                # self.queued = list(set(self.queued))
                self.parsed.add(subgenre)
                children += 1
                print("queue", self.queued)
                print(children, len(self.queued))
                print()

        pprint(self.parsed)


if __name__ == '__main__':

    obj = Subgenres("heavy_metal_music")
    obj.get_children_subtrees()
