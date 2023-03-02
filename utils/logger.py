import logging


def get_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler() # optional args: sys.stdout
    ch.setLevel(level)
    formatter = logging.Formatter('[%(asctime)s] - {%(name)s} - [%(filename)s:%(lineno)d, "funcName":%(funcName)s()] - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
