#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from pprint import pprint
from time import sleep
from random import uniform

from config import RAW_DATA_PATH
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

            if not file_exists(RAW_DATA_PATH + subgenre + ".json"):
                wait = uniform(5.0, 10)
                print("Waiting", str(wait) + "s")
                sleep(wait)

            if subgenre not in self.parsed:
                subtree = WikiSubtree(endpoint=subgenre)
                subtree.generate_subtree()
                grand_children = list(
                    set(subtree.get_subtree()["children"]) - set(self.queued))
                self.queued.extend(grand_children)
                self.parsed.add(subgenre)
                children += 1
                print("Current queue")
                pprint(self.queued[children:])
                print("Processing child:", children,
                      "of queue length:", len(self.queued))
                print()


if __name__ == '__main__':

    obj = Subgenres("Rock_music")
    obj.get_children_subtrees()
