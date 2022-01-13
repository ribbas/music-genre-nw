#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from bs4 import BeautifulSoup
import requests


class WikiScraper:
    def __init__(self) -> None:
        pass

    def get_html(self, url: str) -> str:

        req = requests.get(url)
        return req.text

    def get_soup(self, html: str) -> BeautifulSoup:

        return BeautifulSoup(html, "html.parser")

    def scrape_list_page(self, url: str) -> set:

        html = self.get_html(url)
        elements = self.get_soup(html).find_all(["h2", "li"])
        genres = {}
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
                        genre_href = genre_href["href"].split("/")[-1]
                        genre_key = element.text.split("\n")[0].lower()
                        genres[genre_key] = genre_href

        return genres

    def scrape_genre_page(self, genre_list: list):

        for genre_url in genre_list:
            print(genre_url)
            wait = random.uniform(1.0, 3.0)
            # time.sleep(wait)
            genre_html = self.get_html(genre_url)
            table_soup = self.get_soup(genre_html).find(
                "table", {"class": "infobox nowraplinks"}
            )
            # print(table_soup.prettify())
            wiki_table_data = {}
            category_key = ""
            data = []
            for elem in table_soup.find_all("tr"):
                category_title = elem.findChildren("th")
                if category_title:
                    category_key = category_title[0].text
                    wiki_table_data[category_key] = []
                    # print("title", category_title[0].text)

                category_list = elem.findChildren("li")
                if category_list:
                    for li_elem in category_list:
                        wiki_table_data[category_key].append(li_elem.text)
                        # print("list", li_elem.text)
                else:
                    wiki_table_data[category_key].append(elem.text)
                    # print(elem.text)

            from pprint import pprint

            pprint(wiki_table_data)
