# encoding: utf-8
import sys
import logging


class Logging:
    @staticmethod
    def init_root_logger(level=logging.DEBUG, log_file_path: str = None) ->\
            None:
        root_logger = logging.root
        root_logger.handlers.clear()
        root_logger.setLevel(level)
        # Stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.addFilter(lambda entry: entry.levelno <= logging.INFO)
        stdout_handler.setFormatter(
            logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s '
                              '[%(name)s] %(message)s')
        )
        root_logger.addHandler(stdout_handler)
        # Stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.addFilter(lambda entry: entry.levelno > logging.INFO)
        stderr_handler.setFormatter(
            logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s '
                              '[%(name)s] %(message)s')
        )
        root_logger.addHandler(stderr_handler)
        # File handler
        if log_file_path:
            file_handler = logging.FileHandler(filename=log_file_path)
            file_handler.setFormatter(
                logging.Formatter('[%(levelname)s] [%(asctime)s] %(module)s '
                                  '[%(name)s] %(message)s')
            )
            root_logger.addHandler(file_handler)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.propagate = True

        return logger
