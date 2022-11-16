from typing import Literal

JSON_VALUES = int | str | float | bool | list | dict | None
JSON = dict[str, JSON_VALUES]
Stars = Literal[1, 2, 3, 4, 5]
