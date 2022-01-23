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

        return [Normalizer.annotation_re.match(c).group() for c in category_values_list]

    @staticmethod
    def normalize_genre_values(category_values_list: list) -> list:

        return [Normalizer.normalize_genre_key(c) for c in category_values_list]

    @staticmethod
    def normalize_dates(origin_date: str) -> set:

        origin_date_groups: set = set()
        matches = Normalizer.cultural_origins_date_re.finditer(origin_date)
        for found_group in matches:
            origin_date_groups.add(found_group.group().strip())

        return origin_date_groups

    @staticmethod
    def normalize_geoloc(geoloc_value: str) -> set:

        origin_geoloc_groups: list = set()

        doc = Normalizer.nlp(geoloc_value)
        for ent in doc.ents:
            if ent.label_ in {"GPE", "LOC"}:
                origin_geoloc_groups.add(ent.text)

        return origin_geoloc_groups

    @staticmethod
    def normalize_scenes(category_values_list: list) -> set:

        origin_geolocs: set = set()
        for category_value in category_values_list:
            origin_geolocs |= Normalizer.normalize_geoloc(category_value)

        return list(origin_geolocs)

    @staticmethod
    def normalize_cultural_origins(category_values_list: list) -> list:

        cultural_origins: list = []
        for category_value in category_values_list:

            origin_date_groups = Normalizer.normalize_dates(category_value)
            origin_geoloc_groups = Normalizer.normalize_geoloc(category_value)

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

        return [c for c in category_value_list if c not in Normalizer.category_keys]

    @staticmethod
    def normalize_category_data(genre_data: dict) -> dict:

        normalized_category_data: dict = {}
        for category_key, category_values_list in genre_data.items():

            category_values_list = filter(None, category_values_list)
            category_values_list = Normalizer.remove_category_value(
                category_values_list
            )
            category_values_list = Normalizer.remove_category_keys(
                category_key, category_values_list
            )
            category_values_list = Normalizer.strip_annotations(category_values_list)

            # if category is a genre category
            if category_key in Normalizer.genre_categories:
                category_values_list = Normalizer.normalize_genre_values(
                    category_values_list
                )

            elif category_key == "Cultural origins":
                category_values_list = Normalizer.normalize_cultural_origins(
                    category_values_list
                )

            elif category_key in {
                "Regional scenes",
                "Local scenes",
            }:
                category_values_list = Normalizer.normalize_scenes(category_values_list)

            elif category_key == "Typical instruments":
                category_values_list = [i.lower() for i in category_values_list]

            else:
                continue

            normalized_category_data[category_key.lower()] = category_values_list

        return normalized_category_data


class TableNormalizer:
    def __init__(self) -> None:

        self.raw_file_data: list = []

    def read_raw_data(self, raw_file_data) -> None:

        self.raw_file_data = raw_file_data

    def normalize(self) -> list:

        normalize_data: list = []

        for data in self.raw_file_data:
            genre_key, genre_values_list = next(iter(data.items()))
            normalized_values = Normalizer.normalize_category_data(genre_values_list)
            normalize_data.append({genre_key: normalized_values})

        return normalize_data
