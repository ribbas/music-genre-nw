import json
from pathlib import Path
from typing import Any

from .typealias import DictList, ParsedData, StrColumnDict


class ConfigTools:
    def __init__(self) -> None:

        # data file paths
        self.__base_dir: Path = Path().parent.resolve()
        self.__data_dir: Path = self.__base_dir / "data"
        self.__statics_dir: Path = self.__base_dir / "statics"

        self.urls_file_path: Path = self.__data_dir / "urls.json"
        self.genres_file_path: Path = self.__data_dir / "list.json"
        self.checkpoint_file_path: Path = self.__data_dir / "checkpoint.json"
        self.raw_file_path: Path = self.__data_dir / "raw.json"
        self.wrangled_file_path: Path = self.__data_dir / "wrangled.json"
        self.wrangled_min_file_path: Path = self.__data_dir / "wrangled.min.json"
        self.graph_pos_file_path: Path = self.__data_dir / "graphpos.json"

        self.figure_path: Path = self.__statics_dir / "graph.svg"

    def make_wiki_url(self, endpoint: str) -> str:

        return self.urls["BASE"] + endpoint.strip().replace(" ", "_")

    @staticmethod
    def read_from_file(file_path: Path) -> Any:

        with open(file_path) as fp:
            return json.load(fp)

    @staticmethod
    def dump_to_file(file_path: Path, data: Any, pretty: bool = False) -> None:

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
        self.genre_queue: DictList[str] = []
        self.parsed_data: DictList[ParsedData] = []
        self.successes: set[str] = set()
        self.failures: set[str] = set()

        self.genres_file_path: Path = Path()
        self.checkpoint_file_path: Path = Path()
        self.raw_file_path: Path = Path()

    def add_success(self, genre: str) -> None:

        self.successes.add(genre)

    def add_failure(self, genre: str) -> None:

        self.failures.add(genre)

    def add_parsed_data(self, genre: dict[str, ParsedData]) -> None:

        self.parsed_data.append(genre)

    def get_genre_queue(self) -> DictList[str]:

        return self.genre_queue

    def set_file_paths(self, configs: ConfigTools) -> None:

        self.genres_file_path = configs.genres_file_path
        self.checkpoint_file_path = configs.checkpoint_file_path
        self.raw_file_path = configs.raw_file_path

    def get_genres(self) -> DictList[str]:

        return ConfigTools.read_from_file(self.genres_file_path)

    def get_current_data(
        self,
    ) -> DictList[ParsedData]:

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

        checkpoint_data: StrColumnDict = {
            "successes": sorted(list(self.successes)),
            "failures": sorted(list(self.failures)),
        }
        ConfigTools.dump_to_file(self.checkpoint_file_path, checkpoint_data)

        current_data: DictList[ParsedData] = self.get_current_data()
        current_data.extend(self.parsed_data)
        ConfigTools.dump_to_file(self.raw_file_path, current_data)
