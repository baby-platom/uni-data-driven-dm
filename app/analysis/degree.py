from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import DegreeStats
from app.visualize import process_plot


def calculate_degree_distribution_analysis(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> Path:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    degrees_distribution = _get_degree_distribution(graph)
    visualize_image_file_path = _visualize_degree_distribution(
        degrees_distribution, graph_name
    )

    stats_to = _calculate_degree_stats(degrees_distribution)
    logger.info(
        "Degree distribution analysis",
        graph_name=graph_name,
        **stats_to.model_dump(),
    )

    logger.info(
        "Degree Distribution visualization",
        image_file_path=visualize_image_file_path,
    )
    return visualize_image_file_path


def _get_degree_distribution(graph: nx.Graph) -> dict[int, int]:
    degrees = np.array([deg for _, deg in graph.degree()])
    bincount = np.bincount(degrees)
    return {degree: int(count) for degree, count in enumerate(bincount) if count > 0}


def _visualize_degree_distribution(
    degree_distribution: dict[int, int],
    graph_name: str | None = None,
) -> Path:
    degrees = np.array(list(degree_distribution.keys()))
    frequencies = np.array(list(degree_distribution.values()))

    plt.figure(figsize=(16, 10))

    ax = sns.scatterplot(x=degrees, y=frequencies)
    ax.set_xscale("log")
    ax.set_yscale("log")

    title = "Degree Distribution"
    ax.set_title(title)
    ax.set_xlabel("Degree")
    ax.set_ylabel("Frequency")

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    return process_plot(file_path=file_path)


def _calculate_degree_stats(
    degree_freq: dict[int, int],
) -> DegreeStats:
    degrees = np.array(list(degree_freq.keys()), dtype=float)
    freqs = np.array(list(degree_freq.values()), dtype=float)
    n_freq = freqs.sum()

    mean = np.sum(degrees * freqs) / n_freq

    variance = np.sum(freqs * (degrees - mean) ** 2) / n_freq
    std_dev = np.sqrt(variance)

    if std_dev == 0:
        skewness = 0.0
        kurtosis = -3.0
    else:
        skewness = np.sum(freqs * (degrees - mean) ** 3) / (n_freq * std_dev**3)
        kurtosis = np.sum(freqs * (degrees - mean) ** 4) / (n_freq * std_dev**4) - 3

    return DegreeStats(
        mean=mean,
        variance=variance,
        skewness=skewness,
        kurtosis=kurtosis,
    )
