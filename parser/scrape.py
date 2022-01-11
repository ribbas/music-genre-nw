#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


class WikiScraper:
    def __init__(self) -> None:
        pass

    def get_html(self, url: str) -> str:

        return requests.get(url).text

    def get_soup(self, html: str) -> BeautifulSoup:

        return BeautifulSoup(html, "html.parser")

    def scrape_list(self, url: str) -> set:

        html = self.get_html(url)
        elements = self.get_soup(html).find_all(["h2", "h3", "li"])
        genres = set()
        begin_filling = False

        for elem in elements:

            if elem.name == "h2":
                if "Avant-garde" in elem.text:
                    begin_filling = True
                elif "Regional" in elem.text:
                    break

            if begin_filling:

                if elem.name == "li":
                    elem = elem.text.lower().split("\n")
                    for i in elem:
                        genres.add(i)

        return sorted(genres)
