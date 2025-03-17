from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import gridspec

from app.constants import SEED_VALUE
from app.utils import process_plot


def visualize_influential_nodes(
    graph: nx.Graph,
    influential_nodes: list[Any],
    analysis_method: str,
    graph_name: str | None = None,
) -> None:
    pos: dict[Any, Any] = nx.spring_layout(graph, seed=SEED_VALUE)

    figure = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

    ax_graph = figure.add_subplot(gs[0])
    ax_text = figure.add_subplot(gs[1])

    ax_graph.axis("off")
    ax_text.axis("off")

    node_colors = []
    node_sizes = []
    for node in graph.nodes():
        if node in influential_nodes:
            node_colors.append("red")
            node_sizes.append(300)
        else:
            node_colors.append("skyblue")
            node_sizes.append(100)

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax_graph,
        node_color=node_colors,
        node_size=node_sizes,
    )
    nx.draw_networkx_edges(graph, pos, ax=ax_graph)
    nx.draw_networkx_labels(graph, pos, ax=ax_graph, font_size=8)

    title = f"{analysis_method.capitalize()}: Highlighted Influential Nodes"
    ax_graph.set_title("Highlighted Influential Nodes")

    text_lines = ["Influential Nodes (Ordered):"]
    for index, node in enumerate(influential_nodes):
        text_lines.append(f"{index}. {node}")
    sidebar_text = "\n".join(text_lines)

    ax_text.text(0.05, 0.95, sidebar_text, va="top", ha="left", fontsize=10)

    plt.tight_layout()

    file_path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    process_plot(file_path=file_path)
