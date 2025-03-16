"""Entry point of the network analysis pipeline."""

import seaborn as sns

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


def main() -> None:
    configs = get_configs()
    sns.set_theme(style=configs.SEABORD_STYLE)

    graph = configs.DATA_SET.get_data_set_func()
    visualize_graph(graph)

    calculate_degree_distribution_analysis(graph)
    calculate_connected_components_analysis(graph)
    calculate_path_analysis(graph)
    calculate_clustering_and_density_analysis(graph)
    calculate_centrality_analysis(graph)


if __name__ == "__main__":
    configure_file_logger()
    main()
