#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from platformdirs import annotations

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

annotation_re = re.compile(r"^[^\[]+", re.I)


class Normalizer:
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
    def strip_annotations(category_values_list: str) -> list:

        filtered_category_values_list = []
        for category_value in category_values_list:
            filtered_category_values_list.append(
                annotation_re.match(category_value).group()
            )

        return filtered_category_values_list

    @staticmethod
    def normalize_stylistic_origins():
        pass

    @staticmethod
    def normalize_cultural_origins():
        pass

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
            if category_value not in category_keys:
                filtered_category_value_list.append(category_value)

        return filtered_category_value_list

    @staticmethod
    def normalize_category_data(genre_data: dict) -> dict:

        normalized_category_data = {}
        for category_key, category_value_list in genre_data.items():

            category_value_list = Normalizer.remove_category_keys(category_value_list)
            category_value_list = Normalizer.strip_annotations(category_value_list)

            # if category is a genre category
            if category_key in genre_categories:
                genres = []
                for genre in category_value_list:
                    genres.append(Normalizer.normalize_genre_key(genre))
                category_value_list = genres

            normalized_category_data[category_key.lower()] = category_value_list

        return normalized_category_data


class TableNormalizer:
    def __init__(self) -> None:

        self.raw_file_data: list = []

    def read_raw_data(self, raw_file_data) -> None:

        self.raw_file_data = raw_file_data

    def normalize(self) -> None:

        for data in self.raw_file_data:
            print(data)
            genre_key, genre_values_list = next(iter(data.items()))
            print({genre_key: Normalizer.normalize_category_data(genre_values_list)})
