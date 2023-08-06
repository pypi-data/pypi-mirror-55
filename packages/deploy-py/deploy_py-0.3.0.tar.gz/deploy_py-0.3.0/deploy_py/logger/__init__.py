import logging as stdlogging
import sys


def get_logger(name: str = "deploy.logger", level: int = 1):
    _logger = stdlogging.getLogger(name)
    log_formatter = stdlogging.Formatter('%(levelname)s\t%(asctime)s\t%(name)20s:\t%(message)s')

    if len(_logger.handlers) == 0:
        ch = stdlogging.StreamHandler(sys.stderr)
        ch.setFormatter(log_formatter)
        _logger.addHandler(ch)

    log_level = {
        0: stdlogging.WARNING,
        1: stdlogging.INFO,
        2: stdlogging.DEBUG,
    }.get(level, stdlogging.DEBUG)

    _logger.setLevel(log_level)
    return _logger
