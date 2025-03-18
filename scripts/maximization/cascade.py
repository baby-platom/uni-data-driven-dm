from pathlib import Path

import networkx as nx
import seaborn as sns
import structlog

from app.configs import get_configs
from app.logs import configure_logs
from app.maximization import (
    get_independent_cascade_top_influential_nodes,
    visualize_influential_nodes,
)


def main(n_top_influencial_nodes: int) -> None:
    configs = get_configs()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    sns.set_theme(style=configs.SEABORD_STYLE)

    data_set = configs.DATA_SET
    graph_name = data_set.data_set_name

    logger.info("Graph in use", name=graph_name)
    graph = data_set.get_data_set_func()

    betweenness = nx.betweenness_centrality(graph)
    top50_betweenness = set(sorted(betweenness, key=betweenness.get, reverse=True)[:50])

    pagerank = nx.pagerank(graph)
    top50_pagerank = set(sorted(pagerank, key=pagerank.get, reverse=True)[:50])

    ic_top_influencial_nodes = get_independent_cascade_top_influential_nodes(
        graph,
        n_top_influencial_nodes,
        candidates=(top50_betweenness | top50_pagerank),
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


if __name__ == "__main__":
    logs_file_path = Path("scripts", "logs", "cascade.log")
    configure_logs(logs_file_path=logs_file_path)

    n_top_influencial_nodes = 5
    main(n_top_influencial_nodes)
