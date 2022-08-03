from .special import SPECIAL_CASE_GENRES, SPECIAL_CASE_TRANSLATIONS


class GenreCleaner:
    @staticmethod
    def normalize_genre_name(genre_name: str) -> str:

        return genre_name.split("\n")[0]

    @staticmethod
    def normalize_genre_key(genre_key: str) -> str:

        return GenreCleaner.normalize_genre_name(genre_key).lower().strip()

    @staticmethod
    def replace_delim(genre_key: str) -> str:

        return genre_key.replace(" ", "_").replace("-", "_")

    def replace_genre_special_cases(self, genre_key: str) -> tuple[str, ...]:

        for k, v in SPECIAL_CASE_TRANSLATIONS.items():
            if k in genre_key:
                return v

        return (genre_key,)

    def strip_genre_exception(self, genre_key: str) -> tuple[str, ...] | None:

        replaced_genre_key = self.replace_genre_special_cases(genre_key)

        if not (
            len(replaced_genre_key) == 1
            and replaced_genre_key[0] in SPECIAL_CASE_GENRES
        ):
            return replaced_genre_key

    def normalize_genre_values(self, genre_values_list: list[str]) -> list[str]:

        cleaned_genre_list: list[str] = []

        for genre in genre_values_list:

            genre = self.normalize_genre_key(genre)
            stripped_genre: tuple[str, ...] | None = self.strip_genre_exception(genre)
            if stripped_genre:
                delim_replaced_genre: list[str] = [
                    self.replace_delim(i) for i in stripped_genre
                ]
                cleaned_genre_list.extend(delim_replaced_genre)

        return cleaned_genre_list
