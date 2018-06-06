#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from bs4 import BeautifulSoup

from config import BASE_URL, DATA_PATH
from parsers import parse_origin_dates
from util import dump_json, send_request

CATEGORIES = (
    "other names",
    "stylistic origins",
    "cultural origins",
    "typical instruments",
    "derivative forms",
    "subgenres",
    "fusion genres",
    "regional scenes",
    "local scenes",
    "other topics",
)


class WikiSubtree(object):

    def __init__(self, endpoint):

        self.endpoint = endpoint
        self.subtree = {key: [] for key in CATEGORIES}
        self.html = send_request(BASE_URL + self.endpoint)

    def get_table_soup(self, html):

        return BeautifulSoup(html, "html.parser").find_all(
            "table", attrs={"class": "infobox nowraplinks"})[0]

    def get_origins(self):

        pass

    def parse_wiki_table(self):

        root = True
        key = ""
        soup = self.get_table_soup(self.html)

        for div in soup.find_all(["th", "td"]):

            text = div.text.strip().lower()

            if root:
                self.subtree["root"] = text
                root = False

            elif text not in CATEGORIES:
                self.subtree[key].extend(
                    [i.text.lower() for i in div.find_all("a")])

            # special cases of hyperlinks with portions of text divided among
            # tags
            elif text == "cultural origins":
                key = text
                div = div.find_next("td")
                self.subtree[key].append(div.text)

            else:
                key = text

    def generate_subtree(self):

        self.parse_wiki_table()

        self.subtree["cultural origins"] = parse_origin_dates(
            self.subtree["cultural origins"][0])

        dump_json(file_path=DATA_PATH + self.endpoint + ".json",
                  data=self.subtree)

    def get_subtree(self):

        return self.subtree


if __name__ == '__main__':

    obj = WikiSubtree("heavy_metal_music")
    obj.generate_subtree()
