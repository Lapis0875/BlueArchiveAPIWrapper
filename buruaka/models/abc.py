from abc import abstractmethod, ABCMeta

from buruaka.types import JSON


class JsonObject(metaclass=ABCMeta):
    """
    Abstract Base Class to implement json serialization / deserialization.
    """
    @classmethod
    @abstractmethod
    def from_json(cls, data: JSON) -> "JsonObject":   ...

    @abstractmethod
    def to_json(self) -> JSON:  ...