from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import CentralityStats
from app.constants import centrality_plots_folder
from app.visualize import process_plot


def calculate_centrality_analysis(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> list[Path]:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    analysis_to = _calculate(graph)
    image_file_paths = _visualize_centrality_distributions(analysis_to, graph_name)

    logger.info(
        "Centrality Analysis visualization",
        image_file_paths=image_file_paths,
    )
    return image_file_paths


def _calculate(graph: nx.Graph) -> CentralityStats:
    eigenvector = nx.eigenvector_centrality(graph)
    pagerank = nx.pagerank(graph)
    katz = nx.katz_centrality(
        graph,
        alpha=0.005,
        beta=1,
        max_iter=5000,
    )
    closeness = nx.closeness_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)

    return CentralityStats(
        eigenvector=eigenvector,
        pagerank=pagerank,
        katz=katz,
        closeness=closeness,
        betweenness=betweenness,
    )


def _visualize_centrality_distributions(
    centralities_to: CentralityStats,
    graph_name: str | None = None,
) -> list[Path]:
    centralities = centralities_to.model_dump()
    image_file_paths: list[Path] = []

    for measure, values in centralities.items():
        data = np.array(sorted(values.values(), reverse=True))
        ranks = np.arange(1, data.size + 1)

        plt.figure(figsize=(16, 10))
        ax = sns.scatterplot(x=ranks, y=data)

        ax.set_xscale("log")
        ax.set_yscale("log")

        ax.set_title(f"{measure.capitalize()} Centrality Distribution")
        ax.set_xlabel("Centrality Value")
        ax.set_ylabel("Frequency")

        file_path = centrality_plots_folder / Path(
            f"{measure.capitalize()} Distribution.png"
        )
        if graph_name is not None:
            file_path = Path(graph_name) / file_path

        image_file_path = process_plot(file_path=file_path)
        image_file_paths.append(image_file_path)

    return image_file_paths
