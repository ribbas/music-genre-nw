#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import json
import os

import requests


def dump_json(file_path, data):

    with open(file_path, "w") as data_file:
        json.dump(data, data_file, indent=2, sort_keys=True)


def read_json(file_path):

    with open(file_path) as data_file:
        return json.load(data_file)


def file_exists(file_path):

    return os.path.isfile(file_path)


def send_request(url, headers):

    req = requests.get(url, headers=headers)
    print(req.url)
    return req.text
