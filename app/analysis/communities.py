import contextlib
import itertools
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Any

import matplotlib.axes as mpl_axes
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns

from app.analysis.dtos import CommunitiesInternalEvaluation
from app.constants import LARGE_GRAPH_N_NODES, SEED_VALUE
from app.visualize import get_graph_layout, process_plot

__draw_networkx = partial(
    nx.draw_networkx,
    with_labels=True,
    edge_color="gray",
)


def detect_communities_louvain(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> None:
    communities: list[set] = nx.algorithms.community.louvain_communities(
        graph,
        seed=SEED_VALUE,
    )

    pos = get_graph_layout(graph, graph_name)

    community_index: dict[Any, int] = {}
    for community_id, community in enumerate(communities):
        for node in community:
            community_index[node] = community_id

    internal_evaluation_to = _evaluate_communities(graph, community_index)

    palette = sns.color_palette("husl", len(communities))
    node_colors = [palette[community_index[node]] for node in graph.nodes()]

    plt.figure(figsize=(70, 60), dpi=150)
    plt.axis("off")

    num_nodes = graph.number_of_nodes()
    node_size: int = 500
    node_size: int = (
        int(node_size / np.sqrt(num_nodes / LARGE_GRAPH_N_NODES))
        if num_nodes > LARGE_GRAPH_N_NODES
        else node_size
    )

    __draw_networkx(
        graph,
        pos,
        node_color=node_colors,
        node_size=node_size,
    )

    evaluation_text: str = "\n".join(
        f"{key}: {value}" for key, value in internal_evaluation_to.model_dump().items()
    )
    plt.gcf().text(
        0.75,
        0.5,
        evaluation_text,
        fontsize=100,
        bbox={"facecolor": "white", "alpha": 0.7},
        verticalalignment="center",
    )

    title = "Communities: Louvain"
    plt.title(title, fontsize=100)

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    process_plot(file_path=file_path)


def detect_communities_girvan_newman(
    graph: nx.Graph,
    limit: int = 3,
    graph_name: str | None = None,
) -> None:
    """Visualize community partitions detected by the Girvan-Newman algorithm.

    Parameters:
        graph (nx.Graph): The input graph.
        limit (int): The number of community splits to visualize.
    """

    communities = nx.algorithms.community.girvan_newman(graph)
    partitions = list(itertools.islice(communities, limit))

    pos = nx.spring_layout(graph, seed=SEED_VALUE)

    axes: list[mpl_axes.Axes]
    _, axes = plt.subplots(1, limit, figsize=(5 * limit, 5))

    if limit == 1:
        axes = [axes]

    for i, partition in enumerate(partitions):
        community_index: dict[Any, int] = {}
        for community_id, community in enumerate(partition):
            for node in community:
                community_index[node] = community_id

        internal_evaluation_to = _evaluate_communities(graph, community_index)

        palette = sns.color_palette("husl", len(partition))
        node_colors = [palette[community_index[node]] for node in graph.nodes()]

        __draw_networkx(
            graph,
            pos,
            ax=axes[i],
            node_color=node_colors,
        )

        evaluation_text: str = "\n".join(
            f"{key}: {value}"
            for key, value in internal_evaluation_to.model_dump().items()
        )
        axes[i].text(
            0.75,
            0.5,
            evaluation_text,
            fontsize=10,
            bbox={"facecolor": "white", "alpha": 0.7},
            verticalalignment="center",
        )

        axes[i].set_title(f"Partition with {len(partition)} communities")
        axes[i].axis("off")

    plt.tight_layout()

    file_path = Path("Communities: Girvan-Newman.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    process_plot(file_path=file_path)


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
