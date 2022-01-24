#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .text import TextProcessor


class DataCleaner:

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

    @staticmethod
    def normalize_genre_name(genre_name: str) -> str:

        return genre_name.split("\n")[0]

    @staticmethod
    def normalize_genre_key(genre_key: str) -> str:

        return DataCleaner.normalize_genre_name(genre_key).lower().strip()

    @staticmethod
    def normalize_category_key(category_key: str) -> str:

        return category_key.lower().replace(" ", "_")

    @staticmethod
    def strip_annotations(category_values_list: list) -> list:

        return [
            TextProcessor.annotation_re.match(c).group() for c in category_values_list
        ]

    @staticmethod
    def normalize_genre_values(category_values_list: list) -> list:

        if len(category_values_list) == 1 and "," in category_values_list[0]:
            category_values_list = category_values_list[0].split(",")

        return [DataCleaner.normalize_genre_key(c) for c in category_values_list]

    @staticmethod
    def normalize_scenes(category_values_list: list) -> list:

        origin_geolocs: set = set()
        for category_value in category_values_list:
            origin_geolocs |= TextProcessor.parse_geoloc(category_value)

        return list(origin_geolocs)

    @staticmethod
    def normalize_cultural_origins(category_values_list: list) -> list:

        cultural_origins: list = []
        for category_value in category_values_list:

            origin_date_groups = TextProcessor.parse_dates(category_value)
            origin_geoloc_groups = TextProcessor.parse_geoloc(category_value)

            cultural_origins.append(
                {
                    "dates": list(origin_date_groups),
                    "geoloc": list(origin_geoloc_groups),
                }
            )

        return cultural_origins

    @staticmethod
    def remove_category_keys(category_key: str, category_value_list: list) -> list:

        return [c.replace(category_key, "") for c in category_value_list]

    @staticmethod
    def remove_category_value(category_value_list: list) -> list:

        return [c for c in category_value_list if c not in DataCleaner.category_keys]

    @staticmethod
    def clean_misc(category_value_list: list) -> list:

        cleaned_category_value_list = []
        # - "•" was replaced with ""
        # - "(Gangsta rap" was replace with "Gangsta rap"
        for value in category_value_list:
            if "(Gangsta rap" in value:
                value = value.replace("(Gangsta rap", "Gangsta rap")
            if "•" in value:
                value = value.replace("•", "")
            cleaned_category_value_list.append(value)

        return cleaned_category_value_list

    @staticmethod
    def normalize_category_data(genre_data: dict) -> dict:

        normalized_category_data: dict = {}
        for category_key, category_values_list in genre_data.items():

            category_values_list = filter(None, category_values_list)
            category_values_list = DataCleaner.clean_misc(category_values_list)
            category_values_list = DataCleaner.remove_category_value(
                category_values_list
            )
            category_values_list = DataCleaner.remove_category_keys(
                category_key, category_values_list
            )
            category_values_list = DataCleaner.strip_annotations(category_values_list)

            # if category is a genre category
            if category_key in DataCleaner.genre_categories:
                category_values_list = DataCleaner.normalize_genre_values(
                    category_values_list
                )

            elif category_key == "Cultural origins":
                category_values_list = DataCleaner.normalize_cultural_origins(
                    category_values_list
                )

            elif category_key in {
                "Regional scenes",
                "Local scenes",
            }:
                category_values_list = DataCleaner.normalize_scenes(
                    category_values_list
                )

            elif category_key == "Typical instruments":
                category_values_list = [i.lower() for i in category_values_list]

            else:
                continue

            normalized_category_data[category_key.lower()] = category_values_list

        return normalized_category_data
