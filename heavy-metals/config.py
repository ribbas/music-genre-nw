#!/usr/bin/env python
# -*- coding: utf-8 -*-

BASE_URL = "https://en.wikipedia.org/wiki/"
CATEGORIES = (
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

TREE = {key: [] for key in CATEGORIES}
