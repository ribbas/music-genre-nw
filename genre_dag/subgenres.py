#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from time import sleep
from random import uniform

from config import DATA_PATH
from parsewiki import WikiSubtree
from util import file_exists


class Subgenres(object):

    def __init__(self, root):

        self.parsed = set()
        self.queued = []
        self.root = root

    def get_children_subtrees(self):

        self.queued.append(self.root)

        children = 0
        while children < len(self.queued):
            subgenre = self.queued[children]

            if not file_exists(DATA_PATH + subgenre + ".json"):
                wait = uniform(5.0, 10)
                print("wait", wait, "s")
                sleep(wait)

            if subgenre not in self.parsed:
                subtree = WikiSubtree(endpoint=subgenre)
                subtree.generate_subtree()
                grand_children = list(
                    set(subtree.get_subtree()["children"]) - set(self.queued))
                self.queued.extend(grand_children)
                self.parsed.add(subgenre)
                children += 1
                print("queue", self.queued)
                print(children, len(self.queued))
                print()


if __name__ == '__main__':

    obj = Subgenres("heavy_metal_music")
    obj.get_children_subtrees()
