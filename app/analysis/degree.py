import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import DegreeStats
from app.utils import process_plot


def calculate_degree_distribution_analysis(graph: nx.Graph) -> None:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    degrees_distribution = _get_degree_distribution(graph)
    _visualize_degree_distribution(degrees_distribution)

    stats_to = _calculate_degree_stats(degrees_distribution)
    logger.info("Degree distribution analysis", **stats_to.model_dump())


def _get_degree_distribution(graph: nx.Graph) -> dict[int, int]:
    degrees = np.array([deg for _, deg in graph.degree()])
    bincount = np.bincount(degrees)
    return {degree: int(count) for degree, count in enumerate(bincount) if count > 0}


def _visualize_degree_distribution(degree_distribution: dict[int, int]) -> None:
    plt.figure(figsize=(8, 5))

    ax = sns.barplot(
        x=degree_distribution.keys(),
        y=degree_distribution.values(),
    )

    title = "Degree Distribution"
    ax.set_title(title)
    ax.set_xlabel("Degree")
    ax.set_ylabel("Frequency")

    process_plot(file_title=title)


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
