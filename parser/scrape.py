#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from .normalize import (
    normalize_category_data,
    normalize_category_key,
    normalize_category_values,
    normalize_genre_key,
    normalize_genre_name,
)

from bs4 import BeautifulSoup
import requests


class WikiScraper:
    def get_html(self, url: str) -> str:

        req = requests.get(url)
        return req.text

    def get_soup(self, html: str) -> BeautifulSoup:

        return BeautifulSoup(html, "html.parser")

    def scrape_list_page(self, url: str) -> set:

        html = self.get_html(url)
        elements = self.get_soup(html).find_all(["h2", "li"])
        genres = []
        genre_keys = set()
        begin_filling = False

        for element in elements:

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

    def scrape_genre_pages(self, genre_list: list):

        scraped_wiki_tables = {}

        for genre_data in genre_list:

            try:

                wait = random.uniform(1.0, 3.0)
                time.sleep(wait)

                wiki_table_data = self.scrape_genre_page(
                    genre_data["url"], genre_data["name"]
                )

                scraped_wiki_tables[genre_data["key"]] = wiki_table_data
                print("done")

            except KeyboardInterrupt:
                break

        return scraped_wiki_tables

    def scrape_genre_page(self, url: str, name: str):

        genre_html = self.get_html(url)
        table_soup = self.get_soup(genre_html).find(
            "table", {"class": "infobox nowraplinks"}
        )

        wiki_table_data = {}
        category_key = ""
        for elem in table_soup.find_all("tr"):

            if elem.text is not name:
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
