from typing import TypeAlias

IntTuple: TypeAlias = tuple[int, int]
DictList: TypeAlias = list[dict[str, str]]
ColumnDict: TypeAlias = dict[str, list[str]]
ScrapedPage: TypeAlias = dict[str, DictList]
WrangledData: TypeAlias = list[str] | dict[str, list[str] | dict[str, int]]
