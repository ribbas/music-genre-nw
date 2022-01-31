#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union

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

    text_proc = TextProcessor()

    def __init__(self) -> None:

        self.raw_file_data: list = []
        self.wrangled_data: list = []
        self.gc = GenreCleaner()

    def read_raw_data(self, raw_file_data) -> None:

        self.raw_file_data = raw_file_data

    def get_wrangled_data(self) -> list:

        return self.wrangled_data

    def normalize(self) -> None:

        self.text_proc.initialize()
        for data in self.raw_file_data:
            genre_key, genre_values_list = next(iter(data.items()))
            genre_key, normalized_values = self.normalize_category_data(
                genre_key, genre_values_list
            )
            self.wrangled_data.append({"genre": genre_key, **normalized_values})

    def normalize_category_data(self, genre_key: str, genre_data: dict) -> dict:

        normalized_category_data: dict = {}
        for category_key, category_values_list in genre_data.items():

            category_values_list = self.clean_misc(category_values_list)
            category_values_list = self.remove_category_value(category_values_list)
            category_values_list = self.remove_category_keys(
                category_key, category_values_list
            )
            category_values_list = self.split_csv(category_values_list)
            category_values_list = self.strip_annotations(category_values_list)
            category_values_list = [i for i in category_values_list if i]

            # if category is a genre category
            if category_key in self.genre_categories | {"Typical instruments"}:
                prev = category_values_list
                category_values_list = self.gc.normalize_genre_values(
                    category_values_list
                )
                if (
                    category_key == "Stylistic origins"
                    and category_values_list
                    and len(category_values_list[0]) == 1
                ):
                    print(prev, category_values_list)

            elif category_key == "Cultural origins":
                category_values_list = self.normalize_cultural_origins(
                    category_values_list
                )

            elif category_key in {
                "Regional scenes",
                "Local scenes",
            }:
                category_values_list = self.normalize_scenes(category_values_list)

            elif category_key == "Other names":
                aliases = self.gc.normalize_genre_values(category_values_list)
                self.gc.aliases.add_alias(genre_key, aliases)

                continue

            else:
                continue

            normalized_category_data[category_key.lower()] = category_values_list

        genre_key = self.gc.clean_genre_key(genre_key)

        return genre_key, normalized_category_data

    @staticmethod
    def normalize_category_key(category_key: str) -> str:
        """
        Normalize category keys:
            "A b c" -> "a_b_c"
        """
        return category_key.lower().replace(" ", "_")

    @staticmethod
    def strip_annotations(category_values_list: list) -> list:

        for ix in range(len(category_values_list)):
            category_values_list[ix] = "".join(
                s.split("]")[-1] for s in category_values_list[ix].split("[")
            )
            category_values_list[ix] = "".join(
                s.split(")")[-1] for s in category_values_list[ix].split("(")
            )
        return category_values_list

    @staticmethod
    def split_csv(category_values_list: list) -> list:

        if len(category_values_list) == 1 and "," in category_values_list[0]:
            category_values_list = category_values_list[0].split(",")

        return category_values_list

    @staticmethod
    def normalize_scenes(category_values_list: list) -> list:

        origin_geolocs: set = set()
        for category_value in category_values_list:
            origin_geolocs |= DataCleaner.text_proc.parse_geoloc(category_value)

        return list(origin_geolocs)

    @staticmethod
    def consolidate_origin_dates(origin_date_list: list, ix: int) -> int:

        comp_func = min if not ix else max
        return comp_func(origin_date_list, key=lambda x: x[ix])[ix]

    @staticmethod
    def normalize_cultural_origins(category_values_list: list) -> dict:

        origin_date_list: set = set()
        origin_geoloc_groups: set = set()
        for category_value in category_values_list:

            origin_date_list |= DataCleaner.text_proc.parse_dates(category_value)
            origin_geoloc_groups |= DataCleaner.text_proc.parse_geoloc(category_value)

        origin_date_groups = {"begin": -1, "end": -1}
        if origin_date_list:
            origin_date_groups["begin"] = DataCleaner.consolidate_origin_dates(
                origin_date_list, 0
            )
            origin_date_groups["end"] = DataCleaner.consolidate_origin_dates(
                origin_date_list, 1
            )

        return {
            "dates": origin_date_groups,
            "geoloc": list(origin_geoloc_groups),
        }

    @staticmethod
    def remove_category_keys(category_key: str, category_value_list: list) -> list:

        return [c.replace(category_key, "") for c in category_value_list]

    @staticmethod
    def remove_category_value(category_value_list: list) -> list:

        return [c for c in category_value_list if c not in DataCleaner.category_keys]

    @staticmethod
    def clean_misc(category_value_list: list) -> list:

        cleaned_category_value_list = []

        for value in category_value_list:
            for punc in {"•", "/"}:
                value = value.replace(punc, "")
            value = value.replace("-", " ")
            cleaned_category_value_list.append(value)

        return cleaned_category_value_list


class GenreCleaner:

    genre_exceptions = {
        "1950s pop",
        "1980s pop",
        "1980s pop music",
        "1980s film soundtracks",
        "american 1960s r&b and soul music.",
        "ballads of the french-speaking acadians of canada",
        "comedy andor satire music",
        "eroguro kei  oshare kei",
        "soul music with a greater emphasis on the beats and rhythms of an arrangement",
        "influences from r&b and jazz",
        "list of mexican composers of classical music",
        "list of mexican operas",
        "music of africamusic of west africavarious blues styles",
        "other forms of electronic dance music",
        "other indian forms of music",
        "sertanejo raiz or música caipira  sertanejo romântico   sertanejo universitário   funknejo",
    }

    def __init__(self) -> None:
        self.aliases = AliasManager()

    @staticmethod
    def normalize_genre_name(genre_name: str) -> str:

        return genre_name.split("\n")[0]

    @staticmethod
    def normalize_genre_key(genre_key: str) -> str:

        return GenreCleaner.normalize_genre_name(genre_key).lower().strip()

    def strip_genre_exception(self, genre_key: str) -> Union[list, tuple]:

        if "(gangsta rap" in genre_key:
            genre_key = genre_key.replace("(gangsta rap", "gangsta rap")

        if "rhythm and blues" in genre_key:
            genre_key = genre_key.replace("rhythm and blues", "r&b")

        if "rock n roll" in genre_key:
            return ("rock and roll",)

        if "blackened death metal melodic black-death" in genre_key:
            return "blackened death metal", "melodic black-death"

        if "extreme metal black metal" in genre_key:
            return "extreme metal", "black metal"

        if "alternative metal funk metal" in genre_key:
            return "alternative metal", "funk metal"

        if "acid rock · raga rock · space rock" in genre_key:
            return "acid rock", "raga rock", "space rock"

        if "west coastfunky breaks" in genre_key:
            return "west coast", "funky breaks"

        # genre_key = self.aliases.get_genre_key(genre_key)
        if genre_key not in GenreCleaner.genre_exceptions:
            return [genre_key]

    def normalize_genre_values(self, category_values_list: list) -> list:

        cleaned_genre_list = []

        for genre in category_values_list:

            genre = self.normalize_genre_key(genre)
            genre = self.strip_genre_exception(genre)
            if genre:
                cleaned_genre_list.extend(genre)

        return cleaned_genre_list

    def clean_genre_key(self, genre_key: str) -> str:

        if "rhythm and blues" in genre_key:
            return "r&b"

        elif "hip hop fusion genres" in genre_key:
            return "hip hop"

        elif "/" in genre_key:
            if "post-industrial" in genre_key:
                return "industrial"

            elif "regional edm" in genre_key:
                return "ethnic electronica"

        genre_key = DataCleaner.strip_annotations([genre_key])[0]
        # genre_key = self.aliases.get_genre_key(genre_key)
        return genre_key


class AliasManager:
    def __init__(self) -> None:

        self.aliases: dict = {}

    def add_alias(self, genre_key: str, aliases: list) -> None:

        for alias_key in aliases:

            self.aliases[alias_key] = genre_key

    def get_genre_key(self, genre_key: str) -> str:

        if genre_key in self.aliases:
            print("found alias", genre_key, "/", self.aliases[genre_key])

        return self.aliases.get(genre_key, genre_key)
