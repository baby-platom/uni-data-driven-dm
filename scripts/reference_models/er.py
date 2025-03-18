from pathlib import Path

import networkx as nx
import seaborn as sns
import structlog

from app.analysis import (
    calculate_centrality_analysis,
    calculate_clustering_and_density_analysis,
    calculate_connected_components_analysis,
    calculate_degree_distribution_analysis,
    calculate_path_analysis,
)
from app.configs import get_configs
from app.graphs import create_er_graph
from app.logs import configure_logs


def calculate_basic_analysis(graph: nx.Graph, graph_name: str | None = None) -> None:
    calculate_degree_distribution_analysis(graph, graph_name)
    calculate_connected_components_analysis(graph, graph_name)
    calculate_path_analysis(graph, graph_name)
    calculate_clustering_and_density_analysis(graph, graph_name)
    calculate_centrality_analysis(graph, graph_name)


def main() -> None:
    configs = get_configs()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    sns.set_theme(style=configs.SEABORD_STYLE)

    data_set = configs.DATA_SET
    graph_name = data_set.data_set_name

    logger.info("Graph in use", name=graph_name)
    graph = data_set.get_data_set_func()

    n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
    er_graph = create_er_graph(n_nodes, n_edges)
    calculate_basic_analysis(er_graph, "ER graph")


if __name__ == "__main__":
    logs_file_path = Path("scripts", "logs", "er.log")
    configure_logs(logs_file_path=logs_file_path)

    main()
