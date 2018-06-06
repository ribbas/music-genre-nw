#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from parsewiki import WikiSubtree


class Subgenre(object):

    def __init__(self, genre):

        self.genre = genre
        self.root = None

    def set_root(self):

        subtree = WikiSubtree(endpoint=self.genre)
        subtree.generate_subtree()
        self.root = subtree.get_subtree()

    def get_children(self, subtree):

        return subtree["subgenres"] + subtree["fusion genres"]


if __name__ == '__main__':

    from pprint import pprint

    obj = Subgenre("death_metal")
    obj.set_root()
    pprint(obj.get_children(obj.root))
