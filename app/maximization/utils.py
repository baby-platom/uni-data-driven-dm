from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import structlog
from matplotlib import gridspec

from app.constants import LARGE_GRAPH_N_NODES
from app.visualize import get_graph_layout, process_plot


def visualize_influential_nodes(
    graph: nx.Graph,
    influential_nodes: list[Any],
    analysis_method: str,
    graph_name: str | None = None,
) -> Path:
    pos = get_graph_layout(graph, graph_name)

    figure = plt.figure(figsize=(70, 60), dpi=150)
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

    ax_graph = figure.add_subplot(gs[0])
    ax_text = figure.add_subplot(gs[1])

    ax_graph.axis("off")
    ax_text.axis("off")

    num_nodes = graph.number_of_nodes()

    node_size: int = 500
    node_size: int = (
        int(node_size / np.sqrt(num_nodes / LARGE_GRAPH_N_NODES))
        if num_nodes > LARGE_GRAPH_N_NODES
        else node_size
    )

    node_colors = []
    node_sizes = []
    for node in graph.nodes():
        if node in influential_nodes:
            node_colors.append("red")
            node_sizes.append(node_size * 2)
        else:
            node_colors.append("skyblue")
            node_sizes.append(node_size)

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax_graph,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.8,
    )
    nx.draw_networkx_edges(graph, pos, ax=ax_graph, alpha=0.4, width=0.5)

    title = f"{analysis_method.capitalize()}: Highlighted Influential Nodes"
    ax_graph.set_title("Highlighted Influential Nodes", fontsize=100)

    text_lines = ["Influential Nodes (Ordered):"]
    for index, node in enumerate(influential_nodes):
        text_lines.append(f"{index}. {node}")
    sidebar_text = "\n".join(text_lines)

    ax_text.text(0.05, 0.95, sidebar_text, va="top", ha="left", fontsize=75)

    plt.tight_layout()

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    image_file_path = process_plot(file_path=file_path)

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    logger.info(
        "Influential Nodes visualization",
        analysis_method=analysis_method,
        image_file_path=image_file_path,
    )
    return image_file_path
