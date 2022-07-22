from .genrecleaner import GenreCleaner
from .text import TextProcessor


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
    }

    text_proc: TextProcessor = TextProcessor()

    def __init__(self) -> None:

        self.raw_file_data: list[dict[str, dict[str, list[str]]]] = []
        self.wrangled_data: list[
            dict[str, str | list[str] | dict[str, dict[str, int] | list[str]]]
        ] = []
        self.gc: GenreCleaner = GenreCleaner()

    def load_raw_data(
        self, raw_file_data: list[dict[str, dict[str, list[str]]]]
    ) -> None:

        self.raw_file_data = raw_file_data

    def get_wrangled_data(
        self,
    ) -> list[dict[str, str | list[str] | dict[str, dict[str, int] | list[str]]]]:

        return self.wrangled_data

    def normalize(self) -> None:

        genre_key: str
        genre_values_list: dict[str, list[str]]
        normalized_values: dict[str, list[str] | dict[str, dict[str, int] | list[str]]]
        self.text_proc.initialize()
        for data in self.raw_file_data:
            genre_key, genre_values_list = next(iter(data.items()))
            genre_key, normalized_values = self.normalize_category_data(
                genre_key, genre_values_list
            )
            self.wrangled_data.append({"genre": genre_key, **normalized_values})

    def normalize_category_data(
        self, genre_key: str, genre_data: dict[str, list[str]]
    ) -> tuple[str, dict[str, list[str] | dict[str, dict[str, int] | list[str]]]]:

        normalized_category_data: dict[
            str, list[str] | dict[str, dict[str, int] | list[str]]
        ] = {}
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

            # if category is a genre category
            if category_key in self.genre_categories:
                category_values_list = self.gc.normalize_genre_values(
                    category_values_list
                )

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
                category_values_list = self.gc.normalize_genre_values(
                    category_values_list
                )

            else:
                continue

            # category_values_list = sorted(category_values_list)
            normalized_category_data[category_key.lower()] = category_values_list

        stripped_genre_key: list = DataCleaner.strip_annotations([genre_key])
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
    def strip_annotations(category_values_list: list[str]) -> list:

        for ix in range(len(category_values_list)):
            category_values_list[ix] = "".join(
                s.split("]")[-1] for s in category_values_list[ix].split("[")
            )
            category_values_list[ix] = "".join(
                s.split(")")[-1] for s in category_values_list[ix].split("(")
            )
        return category_values_list

    @staticmethod
    def split_csv(category_values_list: list[str]) -> list:

        if len(category_values_list) == 1 and "," in category_values_list[0]:
            category_values_list = category_values_list[0].split(",")

        return category_values_list

    @staticmethod
    def normalize_scenes(category_values_list: list[str]) -> list:

        origin_geolocs: set = set()
        for category_value in category_values_list:
            origin_geolocs |= DataCleaner.text_proc.parse_geoloc(category_value)

        return list(origin_geolocs)

    @staticmethod
    def consolidate_origin_dates(
        origin_date_list: set[tuple[int, int]], ix: int
    ) -> int:

        comp_func = min if not ix else max
        return comp_func(origin_date_list, key=lambda x: x[ix])[ix]

    @staticmethod
    def normalize_cultural_origins(
        category_values_list: list[str],
    ) -> dict[str, dict[str, int] | list[str]]:

        origin_date_list: set[tuple[int, int]] = set()
        origin_geoloc_groups: set = set()
        for category_value in category_values_list:

            origin_date_list |= DataCleaner.text_proc.parse_dates(category_value)
            origin_geoloc_groups |= DataCleaner.text_proc.parse_geoloc(category_value)

        origin_date_groups: dict[str, int] = {"begin": -1, "end": -1}
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
