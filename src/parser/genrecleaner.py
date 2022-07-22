class GenreCleaner:

    genre_exceptions: set[str] = {
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

    exception_translations: dict[str, tuple[str, ...] | str] = {
        "(gangsta rap": "gangsta rap",
        "acid rock · raga rock · space rock": ("acid rock", "raga rock", "space rock"),
        "alternative metal funk metal": ("alternative metal", "funk metal"),
        "blackened death metal melodic black death": (
            "blackened death metal",
            "melodic black death",
        ),
        "chillout": "chill out",
        "coldwave": "cold wave",
        "euro disco": "eurodisco",
        "extreme metal black metal": ("extreme metal", "black metal"),
        "hip hop fusion genres": "hip hop",
        "lofi": "lo fi",
        "post-industrial": "industrial",
        "regional edm": "ethnic electronica",
        "rhythm and blues": "r&b",
        "rock n roll": "rock and roll",
        "ska core": "skacore",
        "synthpop": "synth pop",
        "west coastfunky breaks": ("west coast", "funky breaks"),
    }

    @staticmethod
    def normalize_genre_name(genre_name: str) -> str:

        return genre_name.split("\n")[0]

    @staticmethod
    def normalize_genre_key(genre_key: str) -> str:

        return GenreCleaner.normalize_genre_name(genre_key).lower().strip()

    @staticmethod
    def replace_special_chars(genre_key: str) -> str:

        return genre_key.replace(" ", "_").replace("-", "_")

    def replace_genre_exceptions(self, genre_key: str) -> tuple[str, ...] | str:

        for k, v in GenreCleaner.exception_translations.items():
            if k in genre_key:
                return v

        return genre_key

    def strip_genre_exception(self, genre_key: str) -> tuple[str, ...] | None:

        replaced_genre_key = self.replace_genre_exceptions(genre_key)
        if replaced_genre_key:
            if isinstance(replaced_genre_key, tuple):
                return replaced_genre_key

            genre_key = replaced_genre_key

        if genre_key not in GenreCleaner.genre_exceptions:
            return (genre_key,)

    def normalize_genre_values(self, genre_values_list: list[str]) -> list[str]:

        cleaned_genre_list: list[str] = []

        for genre in genre_values_list:

            genre = self.normalize_genre_key(genre)
            stripped_genre: tuple[str, ...] | None = self.strip_genre_exception(genre)
            if stripped_genre:
                special_chars_replaced_genre: list[str] = [
                    self.replace_special_chars(i) for i in stripped_genre
                ]
                cleaned_genre_list.extend(special_chars_replaced_genre)

        return cleaned_genre_list
