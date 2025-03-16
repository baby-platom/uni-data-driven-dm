import itertools
from functools import partial
from pathlib import Path
from typing import Any

import matplotlib.axes as mpl_axes
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

from app.constants import SEED_VALUE
from app.utils import process_plot

__draw_networkx = partial(
    nx.draw_networkx,
    with_labels=True,
    edge_color="gray",
    node_size=500,
    font_size=10,
)


def detect_communities_louvain(
    graph: nx.Graph,
    graph_name: str | None = None,
) -> None:
    communities: list[set] = nx.algorithms.community.louvain_communities(
        graph,
        seed=SEED_VALUE,
    )

    pos = nx.spring_layout(graph, seed=SEED_VALUE)

    community_index: dict[Any, int] = {}
    for community_id, community in enumerate(communities):
        for node in community:
            community_index[node] = community_id

    palette = sns.color_palette("husl", len(communities))
    node_colors = [palette[community_index[node]] for node in graph.nodes()]

    plt.figure(figsize=(10, 8))
    plt.axis("off")

    __draw_networkx(
        graph,
        pos,
        node_color=node_colors,
    )

    title = "Communities: Louvain"
    plt.title(title)

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

        palette = sns.color_palette("husl", len(partition))
        node_colors = [palette[community_index[node]] for node in graph.nodes()]

        __draw_networkx(
            graph,
            pos,
            ax=axes[i],
            node_color=node_colors,
        )
        axes[i].set_title(f"Partition with {len(partition)} communities")
        axes[i].axis("off")

    plt.tight_layout()

    file_path = Path("Communities: Girvan-Newman.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    process_plot(file_path=file_path)
