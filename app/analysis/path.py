from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import PathStats
from app.visualize import process_plot


def calculate_path_analysis(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> list[Path]:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    if nx.is_connected(graph):
        visualization_image_file_paths = [_calculate_path_analysis(graph, graph_name)]
    else:
        visualization_image_file_paths = []

        for component_num, component_set in enumerate(nx.connected_components(graph)):
            component = graph.subgraph(component_set).copy()

            visualization_image_file_path = _calculate_path_analysis(
                component,
                graph_name,
                component_num,
            )
            visualization_image_file_paths.append(visualization_image_file_path)

    logger.info(
        "Shortest Path Length Distribution visualization",
        image_file_paths=visualization_image_file_paths,
    )
    return visualization_image_file_paths


def _calculate_path_analysis(
    graph: nx.Graph,
    graph_name: str | None = None,
    component_num: int | None = None,
) -> Path:
    analysis_to = _analyze_component(graph)
    visualization_image_file_path = _visualize_path_length_distribution(
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

    return visualization_image_file_path


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
) -> Path:
    lengths = np.array(list(distribution.keys()))
    frequencies = np.array(list(distribution.values()))

    plt.figure(figsize=(16, 10))

    ax = sns.scatterplot(x=lengths, y=frequencies)
    ax.set_yscale("log")

    title = "Shortest Path Length Distribution"
    if component_num is not None:
        title = f"{title}: Component {component_num}"

    ax.set_title(title)
    ax.set_xlabel("Shortest Path Length")
    ax.set_ylabel("Frequency")

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    return process_plot(file_path=file_path)
