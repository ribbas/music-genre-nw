#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from bs4 import BeautifulSoup

from config import BASE_URL, DATA_PATH, RAW_DATA_PATH, HEADERS
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


class GenreList(object):

    def __init__(self, endpoint, file_name):

        self.html = send_request(BASE_URL + endpoint, HEADERS)
        self.file_name = file_name
        self.genre_list = set()

    def parse_list(self):

        soup = BeautifulSoup(self.html, "html.parser")
        soup_sections = soup.find_all(
            "div", attrs={"class": "div-col columns column-width"})
        for div in soup_sections:
            for li in div.find_all("li"):
                text = li.text.strip().replace(" ", "_").lower().split("\n")
                self.genre_list.update(set(text))

    def dump_list(self):

        dump_json(self.file_name, {
                  "genres": filter(None, list(self.genre_list))})


class WikiSubtree(object):

    def __init__(self, endpoint):

        self.endpoint = endpoint
        self.file_path = RAW_DATA_PATH + self.endpoint + ".json"
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
                try:
                    self.raw_subtree[key].extend(
                        [i.text.lower() for i in div.find_all("a")])

                except KeyError:
                    print("Issue with scraping table for", self.endpoint)
                    continue

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

            try:

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

            except IndexError:

                print("Could not parse", self.endpoint)
                self.subtree["children"] = []

    def get_subtree(self):

        return self.subtree


if __name__ == '__main__':

    # from sys import argv

    # obj = WikiSubtree(argv[-1])
    # obj.generate_subtree()
    obj = GenreList("List_of_popular_music_genres", DATA_PATH + "genres.json")
    obj.parse_list()
    obj.dump_list()
