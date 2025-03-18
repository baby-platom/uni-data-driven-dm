import contextlib
import pickle
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import structlog

from app.configs import get_configs
from app.constants import (
    LARGE_GRAPH_N_NODES,
    SEED_VALUE,
    cache_files_directory,
    saved_plots_directory,
)

config = get_configs()


def process_plot(
    *,
    save_to_file: bool = config.SAVE_PLOTS_TO_FILES,
    file_path: Path | None = None,
) -> Path | None:
    """Processes the current matplotlib figure by either showing it or saving."""
    if not save_to_file:
        plt.show()
        return None

    if file_path is None:
        raise ValueError("`file_path` is not specified")

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    current_figure = plt.gcf()

    file_path = saved_plots_directory / file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    current_figure.savefig(file_path)
    plt.close(current_figure)
    logger.debug(
        "Saved plot to file",
        file_path=str(file_path),
    )

    return file_path


def _get_graph_layout(
    graph: nx.Graph,
    graph_name: str,
) -> dict[Any, Any]:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    cache_files_dir = cache_files_directory / Path("layout")
    cache_files_dir.mkdir(parents=True, exist_ok=True)
    cache_file_path = cache_files_dir / Path(f"{graph_name}_layout.pkl")

    if cache_file_path.exists():
        with contextlib.suppress(Exception), cache_file_path.open("rb") as f:
            logger.info("Using a cached layout", cache_file_path=cache_file_path)
            return pickle.load(f)

    logger.info("Calculating Spring layout")
    pos = nx.spring_layout(graph, seed=SEED_VALUE)

    logger.info("Caching the graph lauout", cache_file_path=cache_file_path)
    with cache_file_path.open("wb") as f:
        pickle.dump(pos, f)

    return pos


def run_base_graph_visualization(
    graph: nx.Graph,
    graph_name: str,
    *,
    node_color: str | Iterable | None = "skyblue",
    edge_color: str = "gray",
) -> tuple[plt.Figure, int]:
    num_nodes: int = graph.number_of_nodes()

    figure = plt.figure(figsize=(70, 60), dpi=150)
    plt.axis("off")

    pos = _get_graph_layout(
        graph,
        graph_name,
    )

    node_size: int = 500
    node_size: int = (
        int(node_size / np.sqrt(num_nodes / LARGE_GRAPH_N_NODES))
        if num_nodes > LARGE_GRAPH_N_NODES
        else node_size
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_color,
        node_size=node_size,
        alpha=0.8,
    )
    nx.draw_networkx_edges(graph, pos, edge_color=edge_color, alpha=0.4, width=0.5)

    if num_nodes <= LARGE_GRAPH_N_NODES:
        nx.draw_networkx_labels(graph, pos, font_size=15)

    return figure, node_size


def visualize_graph(graph: nx.Graph, graph_name: str) -> Path | None:
    run_base_graph_visualization(graph, graph_name)

    title: str = "Graph Visualization"
    plt.title(title, fontsize=100)

    file_path: Path = Path(f"{title}.png")
    if graph_name is not None:
        file_path = Path(graph_name) / file_path

    return process_plot(file_path=file_path)
