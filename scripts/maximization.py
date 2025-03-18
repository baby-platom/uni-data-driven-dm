from pathlib import Path
from typing import Any

import networkx as nx
import seaborn as sns
import structlog

from app.configs import get_configs
from app.logs import configure_logs
from app.maximization import (
    get_independent_cascade_top_influential_nodes,
    get_linear_threshold_top_influential_nodes,
    visualize_influential_nodes,
)


def _get_candidates(graph: nx.Graph, n_candidates: int = 50) -> set[Any]:
    top_n = n_candidates // 2

    betweenness = nx.betweenness_centrality(graph)
    top_n_betweenness = set(
        sorted(betweenness, key=betweenness.get, reverse=True)[:top_n]
    )

    pagerank = nx.pagerank(graph)
    top_n_pagerank = set(sorted(pagerank, key=pagerank.get, reverse=True)[:top_n])

    return top_n_betweenness | top_n_pagerank


def main(n_top_influencial_nodes: int) -> None:
    configs = get_configs()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    sns.set_theme(style=configs.SEABORD_STYLE)

    data_set = configs.DATA_SET
    graph_name = data_set.data_set_name

    logger.info("Graph in use", name=graph_name)
    graph = data_set.get_data_set_func()

    candidates = _get_candidates(graph)

    ic_top_influencial_nodes = get_independent_cascade_top_influential_nodes(
        graph,
        n_top_influencial_nodes,
        candidates,
    )
    logger.info(
        "Independent Cascade: Top influencial nodes",
        nodes=ic_top_influencial_nodes,
    )
    visualize_influential_nodes(
        graph,
        ic_top_influencial_nodes,
        "Independent Cascade",
        graph_name,
    )

    lt_top_influencial_nodes = get_linear_threshold_top_influential_nodes(
        graph,
        n_top_influencial_nodes,
        candidates,
    )
    logger.info(
        "Linear Threshold: Top influencial nodes",
        nodes=lt_top_influencial_nodes,
    )
    visualize_influential_nodes(
        graph,
        lt_top_influencial_nodes,
        "Linear Threshold",
        graph_name,
    )


if __name__ == "__main__":
    logs_file_path = Path("scripts", "logs", "maximization.log")
    configure_logs(logs_file_path=logs_file_path)

    n_top_influencial_nodes = 10
    main(n_top_influencial_nodes)
