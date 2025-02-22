import os
from enum import Enum


class ESIndex(Enum):
    BATTING = os.getenv("ES_BATTING_INDEX_NAME")
    BOWLING = os.getenv("ES_BOWLING_INDEX_NAME")

    @classmethod
    def get_index(cls, name: str):
        try:
            return cls[name.upper()].value
        except KeyError:
            raise ValueError(f"Invalid index name: {name}")
