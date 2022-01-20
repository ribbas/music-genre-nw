#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pathlib
from typing import Any


class ConfigTools:
    def __init__(self) -> None:

        # data file paths
        self.base_dir_path: pathlib.Path = pathlib.Path().parent.resolve()
        self.data_dir_path: pathlib.Path = self.base_dir_path / "data"

        self.urls_file_path: pathlib.Path = self.data_dir_path / "urls.json"
        self.genres_file_path: pathlib.Path = self.data_dir_path / "list.json"
        self.checkpoint_file_path: pathlib.Path = self.data_dir_path / "checkpoint.json"
        self.raw_file_path: pathlib.Path = self.data_dir_path / "raw.json"
        self.norm_file_path: pathlib.Path = self.data_dir_path / "normalized.json"

    def make_wiki_url(self, endpoint: str) -> str:

        return self.urls["BASE"] + endpoint.strip().replace(" ", "_")

    @staticmethod
    def read_from_file(file_path: str) -> Any:

        with open(file_path) as fp:
            return json.load(fp)

    @staticmethod
    def dump_to_file(file_path: str, data: Any) -> None:

        with open(file_path, "w") as fp:
            json.dump(data, fp, ensure_ascii=False)

    def init_urls(self) -> None:

        self.urls = self.read_from_file(self.urls_file_path)
        self.genre_list_url = self.make_wiki_url(self.urls["GENRE_LIST"])


class Checkpoint:
    def __init__(self) -> None:

        # database queues
        self.genre_queue: list = []
        self.parsed_data: list = []
        self.successes: set = set()
        self.failures: set = set()

        self.genres_file_path: str = ""
        self.checkpoint_file_path: str = ""
        self.raw_file_path: str = ""

    def add_success(self, genre: str) -> None:

        self.successes.add(genre)

    def add_failure(self, genre: str) -> None:

        self.failures.add(genre)

    def add_parsed_data(self, genre: dict) -> None:

        self.parsed_data.append(genre)

    def get_genre_queue(self) -> list:

        return self.genre_queue

    def set_file_paths(
        self, genres_file_path, checkpoint_file_path, raw_file_path
    ) -> None:

        self.genres_file_path = genres_file_path
        self.checkpoint_file_path = checkpoint_file_path
        self.raw_file_path = raw_file_path

    def get_genres(self) -> list:

        return ConfigTools.read_from_file(self.genres_file_path)

    def get_current_data(self) -> list:

        return ConfigTools.read_from_file(self.raw_file_path)

    def load(self) -> list:

        checkpoint = ConfigTools.read_from_file(self.checkpoint_file_path)
        self.successes = set(checkpoint["successes"])
        self.failures = set(checkpoint["failures"])
        genre_skips = self.successes | self.failures
        all_genre_list = self.get_genres()
        for gd in all_genre_list:
            if gd["key"] not in genre_skips:
                self.genre_queue.append(gd)

    def save(self) -> None:

        checkpoint_data = {
            "successes": sorted(list(self.successes)),
            "failures": sorted(list(self.failures)),
        }
        ConfigTools.dump_to_file(self.checkpoint_file_path, checkpoint_data)

        current_data = self.get_current_data()
        current_data.extend(self.parsed_data)
        ConfigTools.dump_to_file(self.raw_file_path, current_data)
