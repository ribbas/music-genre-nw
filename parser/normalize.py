#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import spacy


class Normalizer:

    nlp = spacy.load("en_core_web_lg")
    category_keys = {
        "Cultural origins",
        "Derivative forms",
        "Fusion genres",
        "Local scenes",
        "Other topics",
        "Regional scenes",
        "Stylistic origins",
        "Subgenres",
        "Typical instruments",
    }

    genre_categories = {
        "Derivative forms",
        "Fusion genres",
        "Stylistic origins",
        "Subgenres",
    }

    annotation_re = re.compile("^[^\[]+", re.I)
    cultural_origins_date_re = re.compile(
        "((early|mid|late|early.*mid|mid.*late)?[\s|-]?(\d{4}|\d{2}(st|th)\s(century)))",
        re.I | re.M,
    )

    @staticmethod
    def normalize_genre_name(genre_name: str) -> str:

        return genre_name.split("\n")[0]

    @staticmethod
    def normalize_genre_key(genre_key: str) -> str:

        return Normalizer.normalize_genre_name(genre_key).lower()

    @staticmethod
    def normalize_category_key(category_key: str) -> str:

        return category_key.lower().replace(" ", "_")

    @staticmethod
    def strip_annotations(category_values_list: list) -> list:

        filtered_category_values_list = []
        for category_value in category_values_list:
            filtered_category_values_list.append(
                Normalizer.annotation_re.match(category_value).group()
            )

        return filtered_category_values_list

    @staticmethod
    def normalize_genre_values(category_values_list: list):

        filtered_category_values_list = []
        for genre in category_values_list:
            filtered_category_values_list.append(Normalizer.normalize_genre_key(genre))

        return filtered_category_values_list

    @staticmethod
    def normalize_origin_dates(cultural_origin_value: str):

        origin_date_groups = Normalizer.cultural_origins_date_re.findall(
            cultural_origin_value
        )
        if origin_date_groups:
            origin_date_groups = max(origin_date_groups[0], key=lambda x: len(x))
            return origin_date_groups

        return ""

    @staticmethod
    def normalize_origin_geoloc(cultural_origin_value: str):

        origin_geoloc_groups = set()
        doc = Normalizer.nlp(cultural_origin_value)
        for ent in doc.ents:
            if ent.label_ in {"GPE", "LOC"}:
                origin_geoloc_groups.add(ent.text)

        return origin_geoloc_groups

    @staticmethod
    def normalize_cultural_origins(category_values_list: list):

        filtered_category_values_list = []
        origin_date_groups = set()
        origin_geoloc_groups = set()
        for category_value in category_values_list:

            category_value = category_value.replace("Cultural origins", "")

            origin_date_groups.add(Normalizer.normalize_origin_dates(category_value))

            origin_geoloc_groups |= Normalizer.normalize_origin_geoloc(category_value)

        filtered_category_values_list.append(
            {"dates": origin_date_groups, "geoloc": origin_geoloc_groups}
        )
        return filtered_category_values_list

    @staticmethod
    def normalize_typical_instruments():
        pass

    @staticmethod
    def normalize_local_scenes():
        pass

    @staticmethod
    def normalize_other_topics():
        pass

    @staticmethod
    def remove_category_keys(category_value_list):

        filtered_category_value_list = []
        for category_value in category_value_list:
            if category_value not in Normalizer.category_keys:
                filtered_category_value_list.append(category_value)

        return filtered_category_value_list

    @staticmethod
    def normalize_category_data(genre_data: dict) -> dict:

        normalized_category_data = {}
        for category_key, category_value_list in genre_data.items():

            category_value_list = filter(None, category_value_list)
            category_value_list = Normalizer.remove_category_keys(category_value_list)
            category_value_list = Normalizer.strip_annotations(category_value_list)

            # if category is a genre category
            if category_key in Normalizer.genre_categories:
                category_value_list = Normalizer.normalize_genre_values(
                    category_value_list
                )

            elif category_key == "Cultural origins":
                category_value_list = Normalizer.normalize_cultural_origins(
                    category_value_list
                )
                print(category_value_list)

            normalized_category_data[category_key.lower()] = category_value_list

        return normalized_category_data


class TableNormalizer:
    def __init__(self) -> None:

        self.raw_file_data: list = []

    def read_raw_data(self, raw_file_data) -> None:

        self.raw_file_data = raw_file_data

    def normalize(self) -> None:

        for data in self.raw_file_data:
            # print(data)
            genre_key, genre_values_list = next(iter(data.items()))
            print(genre_key)
            normalized_values = Normalizer.normalize_category_data(genre_values_list)
            # print({genre_key: normalized_values})
