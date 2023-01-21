# -*- coding: utf-8 -*-
"""This module allows registering any number of logger so that it is possible to update
the logging level all together at runtime (without relaying on weird hacks.)"""
import logging

logging.basicConfig()
logging_level = logging.INFO
loggers = []


def register_logger(logger):
    """Registers logger.

    Args:
        logger (logging.Logger): A logging.Logger instance.
    """
    if not isinstance(logger, logging.Logger):
        raise TypeError(
            "logger should be a logging.Logger instance, not {}".format(
                logger.__class__.__name__
            )
        )

    if logger not in loggers:
        loggers.append(logger)


def set_level(level):
    """Update all registered loggers to the given level.

    Args:
        level (int): The logging level. The value should be valid with the
            logging library and should be one of [NOTSET, DEBUG, INFO, WARN, WARNING,
            ERROR, FATAL, CRITICAL] of the logging library (or anything that is
        registered as a proper logging level).

    Raises:
        TypeError: If level is not an integer.
        ValueError: If level is not a valid value for the logging library.
    """
    if not isinstance(level, int):
        raise TypeError(
            "logging_level should be an integer value one of [0, 10, 20, 30, 40, 50] "
            "or [NOTSET, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL] of the "
            "logging library, not {}.".format(level.__class__.__name__)
        )

    if level not in logging._levelToName:
        raise ValueError(
            "logging_level should be an integer value one of [0, 10, 20, 30, 40, 50] "
            "or [NOTSET, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL] of the "
            "logging library, not {}.".format(level)
        )

    for logger in loggers:
        logger.setLevel(level)
