from pathlib import Path

import networkx as nx
import seaborn as sns
import structlog

from app.configs import get_configs
from app.logs import configure_logs
from app.visualize import visualize_graph


def main() -> None:
    configs = get_configs()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    sns.set_theme(style=configs.SEABORD_STYLE)

    data_set = configs.DATA_SET
    graph_name = data_set.data_set_name

    logger.info("Graph in use", name=graph_name)
    graph = data_set.get_data_set_func()

    n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
    logger.info("Nodes and edges numbers", n_nodes=n_nodes, n_edges=n_edges)

    is_connected = nx.is_connected(graph)
    logger.info("Graph connectivity", is_connected=is_connected)

    image_file_path = visualize_graph(graph, graph_name)
    logger.info("Visualized graph", image_file_path=image_file_path)


if __name__ == "__main__":
    logs_file_path = Path("scripts", "logs", "visualize_graph.log")

    configure_logs(logs_file_path=logs_file_path)
    main()
