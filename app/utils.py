from pathlib import Path

import matplotlib.pyplot as plt
import structlog

from app.configs import get_configs
from app.constants import saved_plots_directory

config = get_configs()


def process_plot(
    *,
    save_to_file: bool = config.SAVE_PLOTS_TO_FILES,
    file_title: str | None = None,
) -> None:
    """Processes the current matplotlib figure by either showing it or saving."""
    if not save_to_file:
        plt.show()
        return

    if file_title is None:
        raise ValueError("`file_title` is not specified")

    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    current_figure = plt.gcf()

    saved_plots_directory.mkdir(exist_ok=True)
    file_name = Path(f"{file_title}.png")
    file_path = saved_plots_directory / file_name

    current_figure.savefig(file_path)
    plt.close(current_figure)
    logger.info(
        "Saved plot to file",
        file_name=str(file_name),
        plots_direcotry=str(saved_plots_directory),
    )
