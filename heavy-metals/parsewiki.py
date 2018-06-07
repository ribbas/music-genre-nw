#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from bs4 import BeautifulSoup

from config import BASE_URL, DATA_PATH, HEADERS
from parsers import filter_lists, parse_origin_dates
from util import dump_json, file_exists, send_request, read_json

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
        self.file_path = DATA_PATH + self.endpoint + ".json"
        self.raw_subtree = {key: [] for key in RAW_CATEGORIES}

        self.exists = False
        if not file_exists(self.file_path):
            self.html = send_request(BASE_URL + self.endpoint, HEADERS)
            self.subtree = {}
        else:
            print(self.endpoint, "exists")
            self.exists = True
            self.subtree = read_json(self.file_path)

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

        if not self.exists:

            self.parse_wiki_table()

            self.subtree["root"] = self.raw_subtree["root"]

            # self.subtree["origins"] = parse_origin_dates(
            #     self.raw_subtree["cultural origins"][0])

            self.subtree["parents"] = filter_lists(
                set(self.raw_subtree["stylistic origins"]))

            self.subtree["children"] = filter_lists(
                self.raw_subtree["fusion genres"] +
                self.raw_subtree["subgenres"] +
                self.raw_subtree["derivative forms"]
            )

            self.subtree["instruments"] = filter_lists(
                set(self.raw_subtree["typical instruments"]))

            dump_json(file_path=self.file_path,
                      data=self.subtree)

    def get_subtree(self):

        return self.subtree


if __name__ == '__main__':

    obj = WikiSubtree("death_'n'_roll")
    obj.generate_subtree()
