import logging


class Logger:
    def __init__(self):
        logging.basicConfig(
            filename="",
            filemode="a",
            encoding="utf-8",
            format="[%(asctime)s] [%(levelname)s] %(message)s"
        )
