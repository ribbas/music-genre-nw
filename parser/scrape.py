#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from bs4 import BeautifulSoup, element
import requests

from .config import Checkpoint, ConfigTools
from .cleaners import DataCleaner


class WikiParser:
    def __init__(self) -> None:

        self.html: str = ""
        self.soup: element.ResultSet = None
        self.page_list: list = []
        self.checkpoint: Checkpoint = None

    @staticmethod
    def get_html(url: str) -> str:

        req = requests.get(url)

        return req.text

    @staticmethod
    def get_soup(html: str) -> BeautifulSoup:

        return BeautifulSoup(html, "html.parser")

    def set_html(self, url: str) -> None:

        self.html = self.get_html(url)

    def set_soup(self) -> None:
        pass

    def iterate_page(self) -> dict:
        pass

    def set_checkpoint(self, checkpoint: Checkpoint) -> None:

        self.checkpoint = checkpoint

    def set_configs(self, configs: ConfigTools) -> None:

        self.configs = configs

    def set_pages(self, page_list: list) -> None:

        self.page_list = page_list

    def parse(self) -> None:

        if self.checkpoint:
            self.checkpoint.load()
            self.page_list = self.checkpoint.get_genre_queue()

        parsed_pages_data = {}

        for page_args in self.page_list:

            try:

                wait = random.uniform(1.0, 2.0)
                print(
                    f"Parsing '{page_args['key']}' in {wait}s... ", end="", flush=True
                )
                time.sleep(wait)

                self.set_html(page_args["url"])
                self.set_soup()

                try:
                    parsed_data = self.iterate_page(page_args)

                except AttributeError:
                    if self.checkpoint:
                        self.checkpoint.add_failure(page_args["key"])
                    print(f"failed")

                else:
                    parsed_pages_data[page_args["key"]] = parsed_data
                    if self.checkpoint:
                        self.checkpoint.add_success(page_args["key"])
                        self.checkpoint.add_parsed_data({page_args["key"]: parsed_data})
                    print("done")

            except KeyboardInterrupt:
                break

        if self.checkpoint:
            print("Saving...")
            self.checkpoint.save()

        return parsed_pages_data


class ParseGenreList(WikiParser):
    def __init__(self, url: str = None) -> None:

        super().__init__()
        super().set_pages([{"key": "genres", "url": url}])

    def set_soup(self) -> None:

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

                        url = self.configs.make_wiki_url(
                            genre_href["href"].split("/")[-1]
                        )
                        name = DataCleaner.normalize_genre_name(element.text)
                        key = DataCleaner.normalize_genre_key(element.text)

                        if key not in genre_keys:

                            genre_keys.add(key)
                            genre_data = {
                                "url": url,
                                "name": name,
                                "key": key,
                            }
                            genres.append(genre_data)

        sorted_genre_list = sorted(genres, key=lambda k: k["key"])
        return sorted_genre_list


class ParseGenreTable(WikiParser):
    def __init__(self, url: str = None) -> None:

        super().__init__()
        super().set_pages([])

    def set_checkpoint(self, checkpoint: Checkpoint) -> None:

        super().set_checkpoint(checkpoint)

    def set_soup(self) -> None:

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
