from pathlib import Path

import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import PathStats
from app.utils import process_plot


def calculate_path_analysis(graph: nx.Graph, graph_name: str | None = None) -> None:
    if nx.is_connected(graph):
        _calculate_path_analysis(graph, graph_name)
        return

    for component_num, component in enumerate(nx.connected_components(graph)):
        _calculate_path_analysis(component, graph_name, component_num)


def _calculate_path_analysis(
    graph: nx.Graph,
    graph_name: str | None = None,
    component_num: int | None = None,
) -> None:
    analysis_to = _analyze_component(graph)
    _visualize_path_length_distribution(
        analysis_to.path_length_distribution,
        graph_name,
        component_num,
    )

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    logger.info(
        "Path analysis",
        graph_name=graph_name,
        component_num=component_num,
        average_shortest_path_length=analysis_to.average_shortest_path_length,
        diameter=analysis_to.diameter,
    )


def _analyze_component(graph: nx.Graph) -> PathStats:
    avg_length = nx.average_shortest_path_length(graph)
    diameter = nx.diameter(graph)

    distances = [
        distance
        for src_node, lengths in nx.all_pairs_shortest_path_length(graph)
        for tgt_node, distance in lengths.items()
        if src_node != tgt_node
    ]
    distances = np.array(distances)

    unique_lengths, counts = np.unique(distances, return_counts=True)
    distribution: dict[int, int] = dict(
        zip(
            unique_lengths.tolist(),
            (counts // 2).tolist(),
            strict=False,
        )
    )

    return PathStats(
        average_shortest_path_length=avg_length,
        diameter=diameter,
        path_length_distribution=distribution,
    )


def _visualize_path_length_distribution(
    distribution: dict[int, int],
    graph_name: str | None = None,
    component_num: int | None = None,
) -> None:
    unique_values = set(distribution.keys())
    bins = np.arange(min(unique_values), max(unique_values) + 2) - 0.5

    data = np.repeat(list(distribution.keys()), list(distribution.values()))
    ax = sns.histplot(
        data,
        bins=bins,
        discrete=True,
    )

    title = "Shortest Path Length Distribution"
    if component_num is not None:
        title = f"{title}: Component {component_num}"

    ax.set_title(title)
    ax.set_xlabel("Path Length")
    ax.set_ylabel("Count")

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path
    process_plot(file_path=file_path)
