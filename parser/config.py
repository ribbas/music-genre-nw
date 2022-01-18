#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pathlib
from typing import Any


class ConfigTools:
    def __init__(self) -> None:

        # data file paths
        self.base_dir_path = pathlib.Path().parent.resolve()
        self.data_dir_path = self.base_dir_path / "data"
        self.urls_file_path = self.data_dir_path / "urls.json"
        self.genres_file_path = self.data_dir_path / "genres.json"
        self.checkpoint_file_path = self.data_dir_path / "checkpoint.json"
        self.raw_data = self.data_dir_path / "raw.json"

        # database queues
        self.genre_queue = []
        self.successes = set()
        self.failures = set()

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

    def get_genres(self) -> list:

        return self.read_from_file(self.genres_file_path)

    def load_checkpoint(self) -> list:

        checkpoint = self.read_from_file(self.checkpoint_file_path)
        self.successes = set(checkpoint["successes"])
        self.failures = set(checkpoint["failures"])
        genre_skips = self.successes | self.failures
        all_genre_list = self.get_genres()
        for gd in all_genre_list:
            if gd["key"] not in genre_skips:
                self.genre_queue.append(gd)

        print(self.genre_queue)

    def save_checkpoint(self, successes: list, failures: list) -> None:

        checkpoint = {
            "last_genre": "",
            "last_genre_index": 0,
            "failures": ["hardcore", "2-step garage"],
            "successes": ["chamber pop"],
        }
