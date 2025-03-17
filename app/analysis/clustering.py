from pathlib import Path

import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import ClusteringStats
from app.visualize import process_plot


def calculate_clustering_and_density_analysis(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> None:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    _visualize_clustering_coefficient_distribution(graph, graph_name)
    analysis_to = _calculate_analysis(graph)
    logger.info(
        "Clustering and density analysis",
        graph_name=graph_name,
        **analysis_to.model_dump(),
    )


def _calculate_analysis(graph: nx.Graph) -> ClusteringStats:
    global_clustering = nx.transitivity(graph)
    average_clustering = nx.average_clustering(graph)
    density = nx.density(graph)

    return ClusteringStats(
        global_clustering=global_clustering,
        average_clustering=average_clustering,
        density=density,
    )


def _visualize_clustering_coefficient_distribution(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> None:
    clustering_values = list(nx.clustering(graph).values())
    coeff_array = np.array(clustering_values)
    ax = sns.histplot(coeff_array, kde=True)

    title = "Distribution of Node Clustering Coefficients"
    ax.set_title(title)
    ax.set_xlabel("Clustering Coefficient")
    ax.set_ylabel("Frequency")

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    process_plot(file_path=file_path)
