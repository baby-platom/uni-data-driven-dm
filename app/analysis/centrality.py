import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns

from app.analysis.dtos import CentralityStats
from app.utils import process_plot


def calculate_centrality_analysis(graph: nx.Graph) -> None:
    analysis_to = _calculate(graph)
    _visualize_centrality_distributions(analysis_to)


def _calculate(graph: nx.Graph) -> CentralityStats:
    eigenvector = nx.eigenvector_centrality(graph)
    pagerank = nx.pagerank(graph)
    katz = nx.katz_centrality(graph)
    closeness = nx.closeness_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)

    return CentralityStats(
        eigenvector=eigenvector,
        pagerank=pagerank,
        katz=katz,
        closeness=closeness,
        betweenness=betweenness,
    )


def _visualize_centrality_distributions(centralities_to: CentralityStats) -> None:
    centralities = centralities_to.model_dump()
    num_measures = len(centralities)

    _, axs = plt.subplots(num_measures, 1, figsize=(8, 4 * num_measures))

    for ax, (measure, values) in zip(axs, centralities.items(), strict=False):
        data = np.array(list(values.values()))

        sns.histplot(data, kde=True, ax=ax)
        ax.set_title(f"{measure.capitalize()} Centrality Distribution")
        ax.set_xlabel("Centrality Value")
        ax.set_ylabel("Frequency")

    plt.tight_layout()
    process_plot(file_title="Centrality Analysis")
