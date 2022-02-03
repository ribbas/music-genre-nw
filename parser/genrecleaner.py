#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union

from .alias import AliasGraph


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
        self.aliases = AliasGraph()

    @staticmethod
    def normalize_genre_name(genre_name: str) -> str:

        return genre_name.split("\n")[0]

    @staticmethod
    def normalize_genre_key(genre_key: str) -> str:

        return GenreCleaner.normalize_genre_name(genre_key).lower().strip()

    @staticmethod
    def replace_special_chars(genre_key: str) -> str:

        return genre_key.replace(" ", "_").replace("-", "_")

    def replace_genre_exceptions(self, genre_key: str) -> Union[tuple, str]:

        if "rhythm and blues" in genre_key:
            return "r&b"

        elif "hip hop fusion genres" in genre_key:
            return "hip hop"

        elif "/" in genre_key:
            if "post-industrial" in genre_key:
                return "industrial"

            elif "regional edm" in genre_key:
                return "ethnic electronica"

        if "(gangsta rap" in genre_key:
            return genre_key.replace("(gangsta rap", "gangsta rap")

        if "lofi" in genre_key:
            return genre_key.replace("lofi", "lo fi")

        if "coldwave" in genre_key:
            return genre_key.replace("coldwave", "cold wave")

        if "ska core" in genre_key:
            return genre_key.replace("ska core", "skacore")

        if "synthpop" in genre_key:
            return genre_key.replace("synthpop", "synth pop")

        if "chillout" in genre_key:
            return genre_key.replace("chillout", "chill out")

        if "euro disco" in genre_key:
            return genre_key.replace("euro disco", "eurodisco")

        if "rock n roll" in genre_key:
            return "rock and roll"

        if "blackened death metal melodic black death" in genre_key:
            return "blackened death metal", "melodic black death"

        if "extreme metal black metal" in genre_key:
            return "extreme metal", "black metal"

        if "alternative metal funk metal" in genre_key:
            return "alternative metal", "funk metal"

        if "acid rock · raga rock · space rock" in genre_key:
            return "acid rock", "raga rock", "space rock"

        if "west coastfunky breaks" in genre_key:
            return "west coast", "funky breaks"

        return genre_key

    def strip_genre_exception(self, genre_key: str) -> tuple:

        replaced_genre_key = self.replace_genre_exceptions(genre_key)
        if replaced_genre_key:
            if isinstance(replaced_genre_key, tuple):
                return replaced_genre_key

            genre_key = replaced_genre_key

        if genre_key not in GenreCleaner.genre_exceptions:
            return (genre_key,)

    def normalize_genre_values(self, genre_values_list: Union[list, str]) -> list:

        if isinstance(genre_values_list, list):

            cleaned_genre_list = []

            for genre in genre_values_list:

                genre = self.normalize_genre_key(genre)
                genre = self.strip_genre_exception(genre)
                if genre:
                    genre = [self.replace_special_chars(i) for i in genre]
                    cleaned_genre_list.extend(genre)

            return cleaned_genre_list

        else:
            genre = self.normalize_genre_key(genre_values_list)
            genre = self.strip_genre_exception(genre)
            genre = [self.replace_special_chars(i) for i in genre]

            return genre[0]
