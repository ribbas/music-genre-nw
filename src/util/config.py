import json
import pathlib
from typing import Any


class ConfigTools:
    def __init__(self) -> None:

        # data file paths
        self.base_dir_path: pathlib.Path = pathlib.Path().parent.resolve()
        self.data_dir_path: pathlib.Path = self.base_dir_path / "data"
        self.statics_dir_path: pathlib.Path = self.base_dir_path / "statics"

        self.urls_file_path: pathlib.Path = self.data_dir_path / "urls.json"
        self.genres_file_path: pathlib.Path = self.data_dir_path / "list.json"
        self.checkpoint_file_path: pathlib.Path = self.data_dir_path / "checkpoint.json"
        self.raw_file_path: pathlib.Path = self.data_dir_path / "raw.json"
        self.wrangled_min_file_path: pathlib.Path = (
            self.data_dir_path / "wrangled.min.json"
        )
        self.wrangled_file_path: pathlib.Path = self.data_dir_path / "wrangled.json"
        self.graph_pos_file_path: pathlib.Path = self.data_dir_path / "graphpos.json"

        self.figure_path: pathlib.Path = self.statics_dir_path / "graph.svg"

    def make_wiki_url(self, endpoint: str) -> str:

        return self.urls["BASE"] + endpoint.strip().replace(" ", "_")

    @staticmethod
    def read_from_file(file_path: pathlib.Path) -> Any:

        with open(file_path) as fp:
            return json.load(fp)

    @staticmethod
    def dump_to_file(file_path: pathlib.Path, data: Any, pretty: bool = False) -> None:

        with open(file_path, "w") as fp:
            json.dump(data, fp, ensure_ascii=False, **ConfigTools.dump_pretty(pretty))

    @staticmethod
    def dump_pretty(pretty: bool) -> dict[str, int | bool]:

        return {"indent": 4, "sort_keys": True} if pretty else {}

    def init_urls(self) -> None:

        self.urls = self.read_from_file(self.urls_file_path)
        self.genre_list_url = self.make_wiki_url(self.urls["GENRE_LIST"])


class Checkpoint:
    def __init__(self) -> None:

        # database queues
        self.genre_queue: list[dict[str, str]] = []
        self.parsed_data: list[
            dict[str, dict[str, list[str | dict[str, str]]] | None]
        ] = []
        self.successes: set[str] = set()
        self.failures: set[str] = set()

        self.genres_file_path: pathlib.Path = pathlib.Path()
        self.checkpoint_file_path: pathlib.Path = pathlib.Path()
        self.raw_file_path: pathlib.Path = pathlib.Path()

    def add_success(self, genre: str) -> None:

        self.successes.add(genre)

    def add_failure(self, genre: str) -> None:

        self.failures.add(genre)

    def add_parsed_data(
        self, genre: dict[str, dict[str, list[str | dict[str, str]]] | None]
    ) -> None:

        self.parsed_data.append(genre)

    def get_genre_queue(self) -> list[dict[str, str]]:

        return self.genre_queue

    def set_file_paths(self, configs: ConfigTools) -> None:

        self.genres_file_path = configs.genres_file_path
        self.checkpoint_file_path = configs.checkpoint_file_path
        self.raw_file_path = configs.raw_file_path

    def get_genres(self) -> list[dict[str, str]]:

        return ConfigTools.read_from_file(self.genres_file_path)

    def get_current_data(
        self,
    ) -> list[dict[str, dict[str, list[str | dict[str, str]]] | None]]:

        return ConfigTools.read_from_file(self.raw_file_path)

    def load(self) -> None:

        checkpoint = ConfigTools.read_from_file(self.checkpoint_file_path)
        self.successes = set(checkpoint["successes"])
        self.failures = set(checkpoint["failures"])
        genre_skips = self.successes | self.failures
        all_genre_list = self.get_genres()
        for gd in all_genre_list:
            if gd["key"] not in genre_skips:
                self.genre_queue.append(gd)

    def save(self) -> None:

        checkpoint_data: dict[str, list[str]] = {
            "successes": sorted(list(self.successes)),
            "failures": sorted(list(self.failures)),
        }
        ConfigTools.dump_to_file(self.checkpoint_file_path, checkpoint_data)

        current_data: list[
            dict[str, dict[str, list[str | dict[str, str]]] | None]
        ] = self.get_current_data()
        current_data.extend(self.parsed_data)
        ConfigTools.dump_to_file(self.raw_file_path, current_data)
