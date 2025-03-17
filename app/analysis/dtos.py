"""Analysis data transfer objects."""

from typing import Any

from app.dtos import CustomBaseModel


class DegreeStats(CustomBaseModel):
    mean: float
    variance: float
    skewness: float
    kurtosis: float


class ConnectedComponentsStats(CustomBaseModel):
    n_components: int
    component_sizes: tuple[int]
    largest_component_size: int
    average_size: float
    std_size: float


class PathStats(CustomBaseModel):
    average_shortest_path_length: float
    diameter: int
    path_length_distribution: dict[int, int]


class ClusteringStats(CustomBaseModel):
    global_clustering: float
    average_clustering: float
    density: float


class CentralityStats(CustomBaseModel):
    eigenvector: dict[Any, float]
    pagerank: dict[Any, float]
    katz: dict[Any, float]
    closeness: dict[Any, float]
    betweenness: dict[Any, float]


class CommunitiesInternalEvaluation(CustomBaseModel):
    internal_edge_density: float
    average_node_degree: float
    modularity: float
    conductance: float
