import logging
import sys

def init():
    log_formatter = logging.Formatter("%(message)s")
    logger = logging.getLogger()
    logger.setLevel('INFO')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    return logger

LOGGER = init()

def get_logger() -> logging.Logger:
    return LOGGER