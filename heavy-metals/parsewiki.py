#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import copy
import json

from bs4 import BeautifulSoup
import requests

from config import BASE_URL, CATEGORIES, TREE


def send_request(url):

    req = requests.get(url)
    print(req.url)
    return req.text


def get_table_soup(html):

    return BeautifulSoup(html, "html.parser").find_all(
        "table", attrs={"class": "infobox nowraplinks"})[0]


class Subtree(object):

    def __init__(self, endpoint):

        self.sub_tree = copy.deepcopy(TREE)
        html = send_request(BASE_URL + endpoint)
        self.soup = get_table_soup(html)

    def generate_subtree(self):

        from pprint import pprint

        root = True
        key = ""

        for div in self.soup.find_all(["th", "td"]):

            text = div.text.strip().lower()

            if root:
                self.sub_tree["root"] = text
                root = False

            elif text not in CATEGORIES:
                self.sub_tree[key].extend([i.text for i in div.find_all("a")])

            # special cases of hyperlinks with portions of text divided among
            # tags
            elif text == "cultural origins":
                key = text
                div = div.find_next("td")
                self.sub_tree[key].append(div.text)

            else:
                key = text

        pprint(self.sub_tree)

    def get_subtree(self):

        return self.sub_tree


if __name__ == '__main__':

    obj = Subtree("nu_metal")
    obj.generate_subtree()
