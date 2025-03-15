"""Entry point of the network analysis pipeline."""

import seaborn as sns
import structlog

from app.analysis.degree import (
    calculate_degree_stats,
    get_degrees_distribution,
    visualize_degrees_distribution,
)
from app.configs import get_configs
from app.logs import configure_file_logger


def main() -> None:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    configs = get_configs()
    sns.set_theme(style=configs.SEABORD_STYLE)

    graph = configs.DATA_SET.get_data_set_func()
    degrees_distribution = get_degrees_distribution(graph)
    visualize_degrees_distribution(degrees_distribution)

    degree_stats_to = calculate_degree_stats(degrees_distribution)
    logger.info("Degree stats", **degree_stats_to.model_dump())


if __name__ == "__main__":
    configure_file_logger()
    main()
