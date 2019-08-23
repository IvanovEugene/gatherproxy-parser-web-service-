# encoding: utf-8
# TODO: migrate to aiologger
import sys
import logging


class Logging:
    @staticmethod
    def get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        # Stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.addFilter(lambda entry: entry.levelno <= logging.INFO)
        stdout_handler.setFormatter(logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s [%(name)s] %(message)s'))
        logger.addHandler(stdout_handler)
        # Stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.addFilter(lambda entry: entry.levelno > logging.INFO)
        stderr_handler.setFormatter(logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s [%(name)s] %(message)s'))
        logger.addHandler(stderr_handler)

        return logger
