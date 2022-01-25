#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import spacy

nlp = spacy.load("en_core_web_lg")


class TextProcessor:

    cultural_origins_date_re = re.compile(
        "((early|mid|late|early.*mid|mid.*late)?[\s|-]?(\d{4}|\d{2}(st|th)\s(century)))",
        re.I | re.M,
    )
    century_date_re = re.compile("\d{2}", re.I | re.M)
    year_re = re.compile("\d{4}", re.I | re.M)
    early_mid_re = re.compile("early.*mid", re.I | re.M)
    mid_late_re = re.compile("mid.*late", re.I | re.M)

    @staticmethod
    def normalize_date(origin_date: str) -> set:

        date_est: int = 0
        begin_offset: int = 0
        end_offset: int = 9

        origin_date = origin_date.strip().lower().replace("-", " ")

        if TextProcessor.early_mid_re.findall(origin_date):
            end_offset = 5

        elif TextProcessor.mid_late_re.findall(origin_date):
            begin_offset = 5
            end_offset = 9

        elif "early" in origin_date:
            end_offset = 3

        elif "mid" in origin_date:
            begin_offset = 3
            end_offset = 6

        elif "late" in origin_date:
            begin_offset = 6

        if "century" in origin_date:
            match = TextProcessor.century_date_re.findall(origin_date)[0]
            date_est = (int(match) - 1) * 100
            begin_offset *= 11
            end_offset *= 11

        else:
            match = TextProcessor.year_re.findall(origin_date)[0]
            date_est = int(match)

        return date_est + begin_offset, date_est + end_offset

    @staticmethod
    def parse_dates(origin_date: str) -> set:

        origin_date_groups: set = set()
        matches = TextProcessor.cultural_origins_date_re.finditer(origin_date)

        for found_group in matches:
            origin_date_groups.add(TextProcessor.normalize_date(found_group.group()))

        return origin_date_groups

    @staticmethod
    def parse_geoloc(geoloc_value: str) -> set:

        if "Internet" in geoloc_value:
            return {"Internet"}

        doc = nlp(geoloc_value)
        return set(i.text for i in doc.ents if i.label_ in {"GPE", "LOC"})
