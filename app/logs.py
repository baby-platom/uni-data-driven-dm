import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

import structlog

from app.configs import get_configs


def configure_logs(
    contextvars: dict[str, Any] | None = None,
    logs_file_path: Path | None = None,
) -> None:
    """Configurates logging specific to `structlog`."""

    if contextvars is None:
        contextvars = {}

    structlog.contextvars.clear_contextvars()
    configs = get_configs()

    handlers = (logging.StreamHandler(),)
    processors = (structlog.dev.ConsoleRenderer(),)
    if logs_file_path is not None:
        handlers = (logging.handlers.FileHandler(logs_file_path),)
        processors = (structlog.processors.KeyValueRenderer(key_order=("event",)),)

    logging.basicConfig(
        level=configs.LOG_LEVEL.upper(),
        format="%(message)s",
        handlers=handlers,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            *processors,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    structlog.contextvars.bind_contextvars(**contextvars)


def configure_file_logger(
    local_logs_file_path: Path = Path("logs", "logs.log"),
) -> None:
    main_file_path = Path(sys.modules.get("__main__").__file__)
    current_directory = main_file_path.parent.resolve()

    logs_file_path = Path(current_directory / local_logs_file_path)
    configure_logs(logs_file_path=logs_file_path)
