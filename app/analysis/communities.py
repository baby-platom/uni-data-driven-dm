import contextlib
from collections import defaultdict
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
import structlog

from app.analysis.dtos import CommunitiesInternalEvaluation
from app.constants import SEED_VALUE
from app.visualize import process_plot, run_base_graph_visualization


def detect_communities_louvain(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> Path:
    communities: list[set] = nx.algorithms.community.louvain_communities(
        graph,
        seed=SEED_VALUE,
    )

    community_index: dict[Any, int] = {}
    for community_id, community in enumerate(communities):
        for node in community:
            community_index[node] = community_id

    internal_evaluation_to = _evaluate_communities(graph, community_index)

    palette = sns.color_palette("husl", len(communities))
    node_colors = [palette[community_index[node]] for node in graph.nodes()]

    run_base_graph_visualization(graph, graph_name, node_color=node_colors)

    evaluation_text: str = "\n".join(
        f"{key}: {value}" for key, value in internal_evaluation_to.model_dump().items()
    )
    plt.gcf().text(
        0.8,
        0.6,
        evaluation_text,
        fontsize=50,
        bbox={"facecolor": "white", "alpha": 0.7},
        verticalalignment="center",
    )

    title = "Communities: Louvain"
    plt.title(title, fontsize=100)

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    image_file_path = process_plot(file_path=file_path)

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    logger.info(
        "Communities: Louvain visualization",
        image_file_path=image_file_path,
    )
    return image_file_path


def detect_communities_asyn_lpa(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> Path:
    communities: list[set] = list(
        nx.algorithms.community.asyn_lpa_communities(graph, seed=SEED_VALUE)
    )

    community_index: dict[Any, int] = {}
    for community_id, community in enumerate(communities):
        for node in community:
            community_index[node] = community_id

    internal_evaluation_to = _evaluate_communities(graph, community_index)

    palette = sns.color_palette("husl", len(communities))
    node_colors = [palette[community_index[node]] for node in graph.nodes()]

    run_base_graph_visualization(graph, graph_name, node_color=node_colors)

    evaluation_text: str = "\n".join(
        f"{key}: {value}" for key, value in internal_evaluation_to.model_dump().items()
    )
    plt.gcf().text(
        0.8,
        0.6,
        evaluation_text,
        fontsize=50,
        bbox={"facecolor": "white", "alpha": 0.7},
        verticalalignment="center",
    )

    title = "Communities: Async LPA"
    plt.title(title, fontsize=100)

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    image_file_path = process_plot(file_path=file_path)

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    logger.info(
        "Communities: Async LPA visualization",
        image_file_path=image_file_path,
    )
    return image_file_path


def _evaluate_communities(
    graph: nx.Graph,
    community_index: dict[Any, int],
) -> CommunitiesInternalEvaluation:
    """Conduct internal communities evaluation.

    Metrics:
      - Internal Edge Density
      - Average Node Degree
      - Modularity
      - Conductance
    """
    communities_dict: dict[int, set] = defaultdict(set)
    for node, comm_id in community_index.items():
        communities_dict[comm_id].add(node)

    communities = list(communities_dict.values())

    densities = []
    avg_degrees = []
    conductances = []

    for community in communities:
        n_nodes = len(community)
        subgraph: nx.Graph = graph.subgraph(community)
        internal_edges = subgraph.number_of_edges()

        match n_nodes:
            case 0 | 1:
                densities.append(0.0)
                avg_degrees.append(0.0)
            case _:
                max_possible_edges = n_nodes * (n_nodes - 1) / 2
                density = internal_edges / max_possible_edges
                densities.append(density)

                avg_degree = (2 * internal_edges) / n_nodes
                avg_degrees.append(avg_degree)

        community_conductance = 0.0
        with contextlib.suppress(Exception):
            community_conductance = nx.algorithms.cuts.conductance(graph, community)
        conductances.append(community_conductance)

    avg_internal_density = float(np.mean(densities)) if densities else 0.0
    avg_node_degree = float(np.mean(avg_degrees)) if avg_degrees else 0.0
    avg_conductance = float(np.mean(conductances)) if conductances else 0.0

    modularity = nx.algorithms.community.quality.modularity(graph, communities)

    return CommunitiesInternalEvaluation(
        internal_edge_density=avg_internal_density,
        average_node_degree=avg_node_degree,
        modularity=modularity,
        conductance=avg_conductance,
    )
