from . import hashstring
from .logging import CryptoAppLogger, ColoredFormatter

import logging as _logging


# set logger class
_logging.setLoggerClass(CryptoAppLogger)


def new_logger(name: str, *,
               fmt: str = "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
               datefmt: str = "%Y-%m-%d %H:%M:%S",
               level: int = _logging.DEBUG,
               file: str = None) -> _logging.Logger:
    """Create a new logger with the name given.

    Parameters
    ----------
    name : str
        The name of the logger
    fmt : str, optional
        The format of logs
    datefmt : str, optional
        The datetime format for the logs
    level : int, optional
        The level of logger
    file : str, optional
        The path of file to save logs in a file, else None.
        Default: None

    Returns
    -------
    logging.Logger
        The new logger
    """
    logger = _logging.getLogger(name)

    stream_formatter = ColoredFormatter(fmt, datefmt=datefmt)
    file_formatter = _logging.Formatter(fmt, datefmt=datefmt)

    stream_handler = _logging.StreamHandler()
    if file:
        file_handler = _logging.FileHandler(file, mode='a', delay=False)
    else:
        file_handler = None

    stream_handler.setLevel(_logging.DEBUG)
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    if file_handler:
        file_handler.setLevel(_logging.WARNING)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    return logger
