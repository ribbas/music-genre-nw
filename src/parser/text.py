from typing import Any
import re


class TextProcessor:
    def __init__(self) -> None:

        self.nlp: Any = None
        self.cultural_origins_date_re: Any = None
        self.century_date_re: Any = None
        self.year_re: Any = None
        self.early_mid_re: Any = None
        self.mid_late_re: Any = None

    def initialize(self) -> None:

        import spacy

        self.nlp = spacy.load("en_core_web_lg")
        self.cultural_origins_date_re = re.compile(
            r"((early|mid|late|early.*mid|mid.*late)?[\s|-]?(\d{4}|\d{2}(st|th)\s(century)))",
            re.I | re.M,
        )
        self.century_date_re = re.compile(r"\d{2}", re.I | re.M)
        self.year_re = re.compile(r"\d{4}", re.I | re.M)
        self.early_mid_re = re.compile(r"early.*mid", re.I | re.M)
        self.mid_late_re = re.compile(r"mid.*late", re.I | re.M)

    def normalize_date(self, origin_date: str) -> tuple[int, int]:

        date_est: int = 0
        begin_offset: int = 0
        end_offset: int = 9

        origin_date = origin_date.strip().lower().replace("-", " ")

        if self.early_mid_re.findall(origin_date):
            end_offset = 5

        elif self.mid_late_re.findall(origin_date):
            begin_offset = 5
            end_offset = 9

        elif "early" in origin_date:
            end_offset = 3

        elif "mid" in origin_date:
            begin_offset = 3
            end_offset = 6

        elif "late" in origin_date:
            begin_offset = 6

        if "century" in origin_date:
            match: str = self.century_date_re.findall(origin_date)[0]
            date_est = (int(match) - 1) * 100
            begin_offset *= 11
            end_offset *= 11

        else:
            match: str = self.year_re.findall(origin_date)[0]
            date_est = int(match)

        return date_est + begin_offset, date_est + end_offset

    def parse_dates(self, origin_date: str) -> set[tuple[int, int]]:

        origin_date_groups: set = set()
        matches = self.cultural_origins_date_re.finditer(origin_date)

        for found_group in matches:
            origin_date_groups.add(self.normalize_date(found_group.group()))

        return origin_date_groups

    def parse_geoloc(self, geoloc_value: str) -> set[str]:

        if "Internet" in geoloc_value:
            return {"Internet"}

        doc = self.nlp(geoloc_value)
        return set(i.text for i in doc.ents if i.label_ in {"GPE", "LOC"})
