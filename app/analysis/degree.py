import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns

from app.analysis.dtos import DegreeStats


def get_degrees_distribution(graph: nx.Graph) -> dict[int, int]:
    degrees = np.array([deg for _, deg in graph.degree()])
    bincount = np.bincount(degrees)
    return {degree: int(count) for degree, count in enumerate(bincount) if count > 0}


def visualize_degrees_distribution(degree_distribution: dict[int, int]) -> None:
    plt.figure(figsize=(8, 5))

    ax = sns.barplot(
        x=degree_distribution.keys(),
        y=degree_distribution.values(),
    )
    ax.set_title("Degree Distribution")
    ax.set_xlabel("Degree")
    ax.set_ylabel("Frequency")

    plt.show()


def calculate_degree_stats(
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
