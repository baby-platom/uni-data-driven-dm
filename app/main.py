"""Entry point of the network analysis pipeline."""

import networkx as nx
import seaborn as sns
import structlog

from graphs import create_ba_graph, create_er_graph, create_ws_graph

from app.analysis import (
    calculate_centrality_analysis,
    calculate_clustering_and_density_analysis,
    calculate_connected_components_analysis,
    calculate_degree_distribution_analysis,
    calculate_path_analysis,
    detect_communities_girvan_newman,
    detect_communities_louvain,
)
from app.configs import get_configs
from app.constants import saved_plots_directory
from app.logs import configure_file_logger
from app.maximization import (
    get_independent_cascade_top_influential_nodes,
    get_linear_threshold_top_influential_nodes,
    visualize_influential_nodes,
)
from app.visualize import visualize_graph


def calculate_basic_analysis(graph: nx.Graph, graph_name: str | None = None) -> None:
    calculate_degree_distribution_analysis(graph, graph_name)
    calculate_connected_components_analysis(graph, graph_name)
    calculate_path_analysis(graph, graph_name)
    calculate_clustering_and_density_analysis(graph, graph_name)
    calculate_centrality_analysis(graph, graph_name)


def analize_reference_model_graphs(n_nodes: int, n_edges: int) -> None:
    er_graph, ba_graph, ws_graph = (
        create_er_graph(n_nodes, n_edges),
        create_ba_graph(n_nodes, n_edges),
        create_ws_graph(n_nodes, n_edges),
    )

    calculate_basic_analysis(er_graph, "ER graph")
    calculate_basic_analysis(ba_graph, "BA graph")
    calculate_basic_analysis(ws_graph, "WS graph")


def analize_influential_nodes(graph: nx.Graph, n_top_influencial_nodes: int) -> None:
    lt_top_influencial_nodes = get_linear_threshold_top_influential_nodes(
        graph,
        n_top_influencial_nodes,
    )
    visualize_influential_nodes(graph, lt_top_influencial_nodes, "Linear Threshold")

    ic_top_influencial_nodes = get_independent_cascade_top_influential_nodes(
        graph,
        n_top_influencial_nodes,
    )
    visualize_influential_nodes(graph, ic_top_influencial_nodes, "Independent Cascade")


def main(n_top_influencial_nodes: int) -> None:
    configs = get_configs()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    sns.set_theme(style=configs.SEABORD_STYLE)

    data_set = configs.DATA_SET
    graph_name = data_set.data_set_name

    logger.info("Graph in use", name=graph_name)
    graph = data_set.get_data_set_func()

    visualize_graph(graph, graph_name)
    calculate_basic_analysis(graph)

    n_nodes, n_edges = graph.number_of_nodes(), graph.number_of_edges()
    analize_reference_model_graphs(n_nodes, n_edges)

    detect_communities_louvain(graph)
    detect_communities_girvan_newman(graph)

    analize_influential_nodes(graph, n_top_influencial_nodes)
    logger.info(
        "Review the visualized result in the folder",
        folder_name=saved_plots_directory,
    )


if __name__ == "__main__":
    configure_file_logger()

    n_top_influencial_nodes = 5
    main(n_top_influencial_nodes)
