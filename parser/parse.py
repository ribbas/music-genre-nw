#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time

from bs4 import BeautifulSoup, element
import requests


class WikiParser:
    def __init__(self) -> None:

        self.html: str = ""
        self.soup: element.ResultSet = None
        self.page_list: list = []

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

    def set_pages(self, page_list: list) -> None:

        self.page_list = page_list

    def parse(self) -> None:

        parsed_pages_data = {}

        for page_args in self.page_list:

            try:

                wait = random.uniform(1.0, 3.0)
                time.sleep(wait)

                self.set_html(page_args["url"])
                self.set_soup()

                parsed_pages_data[page_args["key"]] = self.iterate_page(page_args)
                print("done")

            except KeyboardInterrupt:
                break

        return parsed_pages_data
