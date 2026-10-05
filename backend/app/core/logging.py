import logging
import sys


def setup_logging(debug: bool = True) -> logging.Logger:
    """
    Configure application-wide structured logging.
    """
    level = logging.DEBUG if debug else logging.INFO
    log_format = "%(asctime)s | %(levelname)-7s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger("campusai")
    logger.setLevel(level)
    return logger


logger = setup_logging()
