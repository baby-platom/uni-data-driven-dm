from pathlib import Path

import seaborn as sns
import structlog

from app.analysis.communities import detect_communities_asyn_lpa
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

    detect_communities_asyn_lpa(graph, graph_name)


if __name__ == "__main__":
    logs_file_path = Path("scripts", "logs", "asyn_lpa.log")
    configure_logs(logs_file_path=logs_file_path)

    main()
