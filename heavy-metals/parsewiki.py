#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from bs4 import BeautifulSoup

from config import BASE_URL, DATA_PATH
from parsers import filter_lists, parse_origin_dates
from util import dump_json, file_exists, send_request

RAW_CATEGORIES = (
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

CATEGORIES = (
    "stylistic origins",
    "cultural origins",
    "typical instruments",
    "derivative forms",
    "subgenres",
    "fusion genres",
)


class WikiSubtree(object):

    def __init__(self, endpoint):

        self.endpoint = endpoint
        self.raw_subtree = {key: [] for key in RAW_CATEGORIES}
        self.html = send_request(BASE_URL + self.endpoint)
        self.subtree = {}

    def get_table_soup(self, html):

        return BeautifulSoup(html, "html.parser").find_all(
            "table", attrs={"class": "infobox nowraplinks"})[0]

    def parse_wiki_table(self):

        root = True
        key = ""
        soup = self.get_table_soup(self.html)

        for div in soup.find_all(["th", "td"]):

            text = div.text.strip().lower()

            if root:
                self.raw_subtree["root"] = text
                root = False

            elif text not in RAW_CATEGORIES:
                self.raw_subtree[key].extend(
                    [i.text.lower() for i in div.find_all("a")])

            # special cases of hyperlinks with portions of text divided among
            # tags
            elif text == "cultural origins":
                key = text
                div = div.find_next("td")
                self.raw_subtree[key].append(div.text)

            else:
                key = text

    def generate_subtree(self):

        self.parse_wiki_table()

        self.subtree["root"] = self.raw_subtree["root"]

        self.subtree["origins"] = parse_origin_dates(
            self.raw_subtree["cultural origins"][0])

        self.subtree["parents"] = filter_lists(
            set(self.raw_subtree["stylistic origins"]))

        self.subtree["children"] = filter_lists(
            self.raw_subtree["fusion genres"] +
            self.raw_subtree["subgenres"] +
            self.raw_subtree["derivative forms"]
        )

        self.subtree["instruments"] = filter_lists(
            set(self.raw_subtree["typical instruments"]))

        dump_json(file_path=DATA_PATH + self.endpoint + ".json",
                  data=self.subtree)

    def get_subtree(self):

        return self.subtree


if __name__ == '__main__':

    obj = WikiSubtree("deathcore")
    obj.generate_subtree()
