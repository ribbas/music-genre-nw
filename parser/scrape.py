#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import Checkpoint
from .normalize import (
    normalize_category_data,
    normalize_category_key,
    normalize_category_values,
    normalize_genre_key,
    normalize_genre_name,
)
from .parse import WikiParser


class ParseGenreList(WikiParser):
    def __init__(self, url: str) -> None:

        super().set_pages([{"key": "genres", "url": url}])

    def set_soup(self):

        self.soup = self.get_soup(self.html).find_all(["h2", "li"])

    def iterate_page(self, args: dict = None) -> dict:

        genres = []
        genre_keys = set()
        begin_filling = False

        for element in self.soup:

            if element.name == "h2":
                if "Avant-garde" in element.text:
                    begin_filling = True
                elif "Regional" in element.text:
                    break

            if begin_filling:

                if element.name == "li":
                    genre_href = element.find("a", href=True)
                    if genre_href:

                        url = genre_href["href"].split("/")[-1]
                        name = normalize_genre_name(element.text)
                        key = normalize_genre_key(element.text)

                        if key not in genre_keys:

                            genre_keys.add(key)
                            genre_data = {
                                "url": url,
                                "name": name,
                                "key": key,
                            }
                            genres.append(genre_data)

        return sorted(genres, key=lambda k: k["key"])


class ParseGenreTable(WikiParser):
    def __init__(self, genre_list: list) -> None:

        super().set_pages(genre_list)

    def set_soup(self):

        self.soup = self.get_soup(self.html).find(
            "table", {"class": "infobox nowraplinks"}
        )

    def iterate_page(self, args: dict = None) -> dict:

        wiki_table_data = {}
        category_key = ""
        for elem in self.soup.find_all("tr"):

            if elem.text is not args["name"]:
                category_title = elem.findChildren(
                    "th", {"class": ["infobox-header", "infobox-label"]}
                )
                if category_title:
                    category_key = category_title[0].text
                    wiki_table_data[category_key] = []

            if category_key:
                category_list = elem.findChildren("li")
                if category_list:
                    for li_elem in category_list:
                        wiki_table_data[category_key].append(li_elem.text)
                else:
                    wiki_table_data[category_key].append(elem.text)

        return wiki_table_data
