from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import structlog

from app.configs import get_configs
from app.constants import SEED_VALUE, saved_plots_directory

config = get_configs()


def process_plot(
    *,
    save_to_file: bool = config.SAVE_PLOTS_TO_FILES,
    file_title: str | None = None,
) -> None:
    """Processes the current matplotlib figure by either showing it or saving."""
    if not save_to_file:
        plt.show()
        return

    if file_title is None:
        raise ValueError("`file_title` is not specified")

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    current_figure = plt.gcf()

    saved_plots_directory.mkdir(exist_ok=True)
    file_name = Path(f"{file_title}.png")
    file_path = saved_plots_directory / file_name

    current_figure.savefig(file_path)
    plt.close(current_figure)
    logger.info(
        "Saved plot to file",
        file_name=str(file_name),
        plots_direcotry=str(saved_plots_directory),
    )


def visualize_graph(graph: nx.Graph) -> None:
    plt.figure(figsize=(10, 8))
    plt.axis("off")

    pos = nx.spring_layout(graph, seed=SEED_VALUE)

    nx.draw_networkx_nodes(graph, pos, node_color="skyblue", node_size=500, alpha=0.8)
    nx.draw_networkx_edges(graph, pos, edge_color="gray", alpha=0.5)
    nx.draw_networkx_labels(graph, pos)

    title = "Graph Visualization"
    plt.title(title)

    process_plot(file_title=title)
