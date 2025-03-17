from pathlib import Path

import seaborn as sns
import structlog

from app.analysis import calculate_path_analysis
from app.configs import get_configs
from app.logs import configure_logs


def main() -> None:
    configs = get_configs()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    sns.set_theme(style=configs.SEABORD_STYLE)

    data_set = configs.DATA_SET
    graph_name = data_set.data_set_name

    logger.info("Graph in use", name=graph_name)
    graph = data_set.get_data_set_func()

    calculate_path_analysis(graph, graph_name)


if __name__ == "__main__":
    logs_file_path = Path("scripts", "logs", "path.log")

    configure_logs(logs_file_path=logs_file_path)
    main()
