from collections.abc import Callable
from enum import Enum

import networkx as nx


class SupportedDataSets(Enum):
    KARATE = "KARATE", nx.karate_club_graph

    def __init__(
        self,
        data_set_name: str,
        get_data_set_func: Callable[..., nx.Graph],
    ) -> None:
        self.data_set_name = data_set_name
        self.get_data_set_func = get_data_set_func

    @classmethod
    def _missing_(cls, value: str) -> "SupportedDataSets":
        for member in cls:
            if member.data_set_name == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")
