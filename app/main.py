"""Entry point of the network analysis pipeline."""

import networkx as nx
import seaborn as sns

from graphs import create_ba_graph, create_er_graph, create_ws_graph

from app.analysis import (
    calculate_centrality_analysis,
    calculate_clustering_and_density_analysis,
    calculate_connected_components_analysis,
    calculate_degree_distribution_analysis,
    calculate_path_analysis,
)
from app.configs import get_configs
from app.logs import configure_file_logger
from app.utils import visualize_graph


def calculate_basic_analysis(graph: nx.Graph, graph_name: str | None = None) -> None:
    calculate_degree_distribution_analysis(graph, graph_name)
    calculate_connected_components_analysis(graph, graph_name)
    calculate_path_analysis(graph, graph_name)
    calculate_clustering_and_density_analysis(graph, graph_name)
    calculate_centrality_analysis(graph, graph_name)


def main() -> None:
    configs = get_configs()
    sns.set_theme(style=configs.SEABORD_STYLE)

    graph = configs.DATA_SET.get_data_set_func()
    visualize_graph(graph)
    calculate_basic_analysis(graph)

    n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
    er_graph, ba_graph, ws_graph = (
        create_er_graph(n_nodes, n_edges),
        create_ba_graph(n_nodes, n_edges),
        create_ws_graph(n_nodes, n_edges),
    )

    calculate_basic_analysis(er_graph, "ER graph")
    calculate_basic_analysis(ba_graph, "BA graph")
    calculate_basic_analysis(ws_graph, "WS graph")


if __name__ == "__main__":
    configure_file_logger()
    main()
