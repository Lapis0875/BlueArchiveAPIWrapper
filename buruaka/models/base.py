from abc import ABCMeta
from typing import Final

import attr

from buruaka.models.abc import JsonObject


@attr.s
class BlueArchiveObject(JsonObject, metaclass=ABCMeta):
    """
    Abstract Base class for all Blue Archive objects.
    """
    id: Final[int] = attr.field()

