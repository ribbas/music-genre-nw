from .genrecleaner import GenreCleaner
from .text import TextProcessor

from ..util.typealias import DictList, StrColumnDict, IntTuple, AnyColumnDict


class DataCleaner:

    category_keys: set[str] = {
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

    genre_categories: set[str] = {
        "Derivative forms",
        "Fusion genres",
        "Stylistic origins",
        "Subgenres",
        "Other names",
    }

    text_proc: TextProcessor = TextProcessor()

    def __init__(self) -> None:

        self.raw_file_data: DictList[StrColumnDict] = []
        self.wrangled_data: list[AnyColumnDict] = []
        self.gc: GenreCleaner = GenreCleaner()

    def normalize_genre_name(self, genre_name: str) -> str:

        return self.gc.normalize_genre_name(genre_name)

    def normalize_genre_key(self, genre_key: str) -> str:

        return self.gc.normalize_genre_key(genre_key)

    def load_raw_data(self, raw_file_data: DictList[StrColumnDict]) -> None:

        self.raw_file_data = raw_file_data

    def get_wrangled_data(self) -> list[AnyColumnDict]:

        return self.wrangled_data

    def normalize(self) -> None:

        genre_key: str
        genre_values_list: StrColumnDict
        normalized_values: AnyColumnDict

        self.text_proc.initialize()
        for data in self.raw_file_data:
            genre_key, genre_values_list = next(iter(data.items()))
            genre_key, normalized_values = self.normalize_category_data(
                genre_key, genre_values_list
            )
            self.wrangled_data.append({"genre": [genre_key], **normalized_values})

    def normalize_category_data(
        self, genre_key: str, genre_data: StrColumnDict
    ) -> tuple[str, AnyColumnDict]:

        normalized_category_data: AnyColumnDict = {}
        for category_key, category_values_list in genre_data.items():

            # replace specific punctuations
            category_values_list = self.clean_misc(category_values_list)
            category_values_list = self.remove_category_value(category_values_list)
            category_values_list = self.remove_category_keys(
                category_key, category_values_list
            )
            category_values_list = self.split_csv(category_values_list)
            category_values_list = self.strip_annotations(category_values_list)
            category_values_list = [i for i in category_values_list if i]

            if category_key == "Cultural origins":
                normalized_category_data[
                    "origin_geoloc"
                ] = self.normalize_cultural_origins(category_values_list)
                normalized_category_data["origin_dates"] = self.normalize_origin_dates(
                    category_values_list
                )
                continue

            # if category is a genre category
            elif category_key in self.genre_categories:
                category_values_list = self.gc.normalize_genre_values(
                    category_values_list
                )

            elif category_key in {"Regional scenes", "Local scenes"}:
                category_values_list = self.normalize_scenes(category_values_list)

            else:
                continue

            normalized_category_data[
                self.normalize_category_key(category_key)
            ] = category_values_list

        stripped_genre_key: list[str] = DataCleaner.strip_annotations([genre_key])
        genre_key = self.gc.normalize_genre_values(stripped_genre_key)[0]

        return genre_key, normalized_category_data

    @staticmethod
    def normalize_category_key(category_key: str) -> str:
        """
        Normalize category keys:
            "A b c" -> "a_b_c"
        """
        return category_key.lower().replace(" ", "_")

    @staticmethod
    def strip_annotations(category_values_list: list[str]) -> list[str]:

        for ix in range(len(category_values_list)):
            category_values_list[ix] = "".join(
                s.split("]")[-1] for s in category_values_list[ix].split("[")
            )
            category_values_list[ix] = "".join(
                s.split(")")[-1] for s in category_values_list[ix].split("(")
            )
        return category_values_list

    @staticmethod
    def split_csv(category_values_list: list[str]) -> list[str]:

        if len(category_values_list) == 1 and "," in category_values_list[0]:
            category_values_list = category_values_list[0].split(",")

        return category_values_list

    @staticmethod
    def normalize_scenes(category_values_list: list[str]) -> list[str]:

        origin_geolocs: set[str] = set()
        for category_value in category_values_list:
            origin_geolocs |= DataCleaner.text_proc.parse_geoloc(category_value)

        return list(origin_geolocs)

    @staticmethod
    def normalize_origin_dates(category_values_list: list[str]) -> list[int]:

        origin_date_list: set[IntTuple] = set()
        for category_value in category_values_list:
            origin_date_list |= DataCleaner.text_proc.parse_dates(category_value)

        origin_date_groups: list[int] = [-1, -1]
        if origin_date_list:
            origin_date_groups[0] = min(origin_date_list, key=lambda x: x[0])[0]
            origin_date_groups[1] = max(origin_date_list, key=lambda x: x[1])[1]

        return origin_date_groups

    @staticmethod
    def normalize_cultural_origins(category_values_list: list[str]) -> list[str]:

        origin_geoloc_groups: set[str] = set()
        for category_value in category_values_list:
            origin_geoloc_groups |= DataCleaner.text_proc.parse_geoloc(category_value)

        return list(origin_geoloc_groups)

    @staticmethod
    def remove_category_keys(
        category_key: str, category_value_list: list[str]
    ) -> list[str]:

        return [c.replace(category_key, "") for c in category_value_list]

    @staticmethod
    def remove_category_value(category_value_list: list[str]) -> list[str]:

        return [c for c in category_value_list if c not in DataCleaner.category_keys]

    @staticmethod
    def clean_misc(category_value_list: list[str]) -> list[str]:

        for ix in range(len(category_value_list)):
            for punc in {"•", "/"}:
                category_value_list[ix] = category_value_list[ix].replace(punc, "")
            category_value_list[ix] = category_value_list[ix].replace("-", " ")

        return category_value_list
