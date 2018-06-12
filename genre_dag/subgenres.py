#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from pprint import pprint
from time import sleep
from random import uniform

from config import DATA_PATH, RAW_DATA_PATH
from parsewiki import WikiSubtree
from util import file_exists, dump_json, read_json


class Subgenres(object):

    def __init__(self, root, failed):

        self.parsed = set()
        self.queued = []
        self.failed = failed
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
                if not grand_children:
                    self.failed.add(subgenre)
                self.queued.extend(grand_children)
                # self.queued = list(set(self.queued) - self.failed)
                self.parsed.add(subgenre)
                children += 1
                print("Current queue")
                pprint(self.queued[children:])
                print("Processing child:", children,
                      "of queue length:", len(self.queued))
                print()


if __name__ == '__main__':

    failed = set(read_json(DATA_PATH + "failed.json")["genres"])
    genre_list = set(read_json(DATA_PATH + "genres.json")["genres"]) - failed

    for genre in genre_list:

        try:

            obj = Subgenres(genre, failed)
            obj.get_children_subtrees()
            failed.update(obj.failed)

        except KeyboardInterrupt:

            print("\b\bSCRAPING CANCELED\n")
            break

    print("FAILED QUEUE")
    failed = sorted(list(failed))
    pprint(failed)
    dump_json(DATA_PATH + "failed.json", {"genres": failed})
