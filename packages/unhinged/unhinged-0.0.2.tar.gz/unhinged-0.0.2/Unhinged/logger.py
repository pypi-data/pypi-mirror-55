import logging
import pathlib

# Logging Initialization

LOG_LEVEL = 0


def set_logger(verbosity: int):
    """sets the root logging level"""
    if verbosity is None:
        verbosity = 0

    LOG_LEVEL = logging.DEBUG
    if verbosity == 0:
        LOG_LEVEL = logging.ERROR
    elif verbosity == 1:
        LOG_LEVEL = logging.WARNING
    elif verbosity == 2:
        LOG_LEVEL = logging.INFO

    logging.getLogger().setLevel(LOG_LEVEL)


def set_file_handler(file_path: str)->pathlib.Path:
    """adds a file handler to the root logger"""
    
    # Initialize path
    abs_file_path = pathlib.Path(__file__).parent / file_path
    abs_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure
    file_formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler(abs_file_path)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(file_formatter)

    logging.getLogger().addHandler(file_handler)
    return abs_file_path


def set_console_handler():
    """ adds a console handler to the root logger"""

    # Configure
    console_formatter = logging.Formatter(
        '%(levelname)s:%(name)s:%(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    logging.getLogger().addHandler(console_handler)
