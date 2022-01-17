#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pathlib
from typing import Any


class ConfigTools:
    def __init__(self) -> None:

        self.base_path = pathlib.Path().parent.resolve()
        self.data_path = self.base_path / "data"
        self.urls_file = self.data_path / "urls.json"
        self.genres_file = self.data_path / "genres.json"
        self.checkpoint = self.data_path / "checkpoint.json"
        self.raw_data = self.data_path / "raw.json"

    def make_wiki_url(self, endpoint: str) -> str:
        return self.urls["BASE"] + endpoint.strip().replace(" ", "_")

    def read_from_file(self, file_path: str) -> Any:

        with open(file_path) as fp:
            return json.load(fp)

    def dump_to_file(self, file_path: str, data: Any) -> None:

        with open(file_path, "w") as fp:
            json.dump(data, fp, ensure_ascii=False)

    def init_urls(self) -> None:

        self.urls = self.read_from_file(self.urls_file)
        self.genre_list_url = self.make_wiki_url(self.urls["GENRE_LIST"])
        self.checkpoint = []

    def load_checkpoint(self) -> list:

        checkpoint_data = self.read_from_file(self.checkpoint)
        successes = checkpoint_data["successes"]
        failures = checkpoint_data["failures"]
        queue = self.read_from_file(self.genres_file)

    def save_checkpoint(self, data: list) -> None:

        pass
