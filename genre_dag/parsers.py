#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

import re

year_range_re = re.compile(r"(early|mid|late)(\W\d{4}s?)?|\d{4}s?", re.I)


def parse_origin_dates(text):

    matches = year_range_re.finditer(text)

    ranges = 0
    origin_range = {"begin": "", "end": ""}
    for num_match, match in enumerate(matches):
        ranges += 1
        key = "begin" if not num_match else "end"
        origin_range[key] = list(match.groups())

    if ranges == 1:

        origin_range["end"] = origin_range["begin"]

    else:

        if not origin_range["begin"][-1]:
            origin_range["begin"][-1] = origin_range["end"][-1]

    for k, v in origin_range.iteritems():
        origin_range[k] = "-".join(
            [v[0].lower(), v[-1].replace("-", "").replace(" ", "")]
        )

    return origin_range


def filter_lists(container):

    container = (i.replace(" ", "_") for i in container if
                 ("[" not in i and
                  len(i) > 2 and
                  i != "complete list")
                 )

    return filter(None, set(container))
