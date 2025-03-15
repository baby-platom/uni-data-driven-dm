"""Entry point of the network analysis pipeline."""

import seaborn as sns

from app.analysis import (
    calculate_connected_components_analysis,
    calculate_degree_distribution_analysis,
    calculate_path_analysis,
)
from app.configs import get_configs
from app.logs import configure_file_logger


def main() -> None:
    configs = get_configs()
    sns.set_theme(style=configs.SEABORD_STYLE)

    graph = configs.DATA_SET.get_data_set_func()

    calculate_degree_distribution_analysis(graph)
    calculate_connected_components_analysis(graph)
    calculate_path_analysis(graph)


if __name__ == "__main__":
    configure_file_logger()
    main()
