#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .clean import DataCleaner


class TableNormalizer:
    def __init__(self) -> None:

        self.raw_file_data: list = []
        self.normalized_data: list = []

    def read_raw_data(self, raw_file_data) -> None:

        self.raw_file_data = raw_file_data

    def get_normalized_data(self) -> list:

        return self.normalized_data

    def normalize(self) -> None:

        for data in self.raw_file_data:
            genre_key, genre_values_list = next(iter(data.items()))
            normalized_values = DataCleaner.normalize_category_data(genre_values_list)
            self.normalized_data.append({"genre": genre_key, **normalized_values})

    def stats(self) -> None:

        for i in self.normalized_data:
            try:
                print(i["genre"], i["cultural origins"])
            except KeyError:
                continue
