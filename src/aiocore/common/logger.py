import logging


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def info(message: str):
        logging.info(message)

    @staticmethod
    def warning(message: str):
        logging.warning(message)

    @staticmethod
    def error(message: str):
        logging.error(message)

    @staticmethod
    def critical(message: str):
        logging.critical(message)
