"""Simple file logger for admin app."""

import logging
import os

LOG_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "BiblioQ_Admin", "logs")


def get_logger(name: str = "BiblioQAdmin") -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join(LOG_DIR, "admin.log"), encoding="utf-8")
    fh.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(sh)
    return logger

logger = get_logger()
