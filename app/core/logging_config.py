import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

custom_theme = Theme(
    {
        "logging.level.info": "bold green",
        "logging.level.debug": "bold bright_cyan",
        "logging.level.warning": "bold dark_orange",
        "logging.level.error": "bold red",
        "logging.level.critical": "bold red on white",
    }
)


def setup_logger(
    name: str = "app", level: int = logging.INFO, log_file: Optional[str] = None
) -> logging.Logger:
    FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

    console = Console(stderr=True, theme=custom_theme)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []

    rich_handler = RichHandler(
        console=console,
        markup=True,
        rich_tracebacks=True,
        show_path=False,
        log_time_format="%Y-%m-%d %H:%M:%S",
    )
    rich_handler.setFormatter(logging.Formatter(FORMAT))

    logger.addHandler(rich_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(file_handler)

    return logger
