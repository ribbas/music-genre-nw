from typing import TypeAlias, TypeVar

IntTuple: TypeAlias = tuple[int, int]
ParsedData: TypeAlias = dict[str, list[dict[str, str]]]
StrColumnDict: TypeAlias = dict[str, list[str]]
AnyColumnDict: TypeAlias = dict[str, list[str] | list[int]]

DictList_T = TypeVar("DictList_T", str, ParsedData, StrColumnDict)
DictList: TypeAlias = list[dict[str, DictList_T]]
