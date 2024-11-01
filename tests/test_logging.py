# -*- coding: utf-8 -*-

import logging
import pytest

from stalker import log


@pytest.fixture(scope="function")
def setup_logging():
    """Set up stalker log module."""
    log.loggers = []
    yield
    # clean loggers list after every test
    log.loggers = []


def test_register_logger_simple(setup_logging):
    """register logger adds the given logger to the list."""
    logger = logging.getLogger("test_logger")
    assert logger not in log.loggers
    log.register_logger(logger)
    assert logger in log.loggers


def test_register_logger_called_multiple_times(setup_logging):
    """register logger adds the logger only once."""
    logger = logging.getLogger("test_logger")
    assert logger not in log.loggers
    assert 0 == len(log.loggers)
    log.register_logger(logger)
    assert 1 == len(log.loggers)
    log.register_logger(logger)
    assert 1 == len(log.loggers)
    log.register_logger(logger)
    assert 1 == len(log.loggers)
    log.register_logger(logger)
    assert 1 == len(log.loggers)
    assert logger in log.loggers


def test_register_logger_only_accept_loggers(setup_logging):
    """register_logger raise a TypeError if the logger is not a Logger instance."""
    with pytest.raises(TypeError) as cm:
        log.register_logger("not a logger")

    assert str(cm.value) == (
        "logger should be a logging.Logger instance, not str: 'not a logger'"
    )


def test_register_logger_sets_the_level_to_the_default_level(setup_logging):
    """register_logger set the level to the default level."""
    logger = logging.getLogger("logger1")
    logger.setLevel(logging.WARNING)
    assert log.logging_level != logging.WARNING
    log.register_logger(logger)
    assert logger.level == log.logging_level


def test_set_level_sets_all_logger_levels(setup_logging):
    """set_level sets all logger levels all together."""
    logger1 = logging.getLogger("test_logger1")
    logger2 = logging.getLogger("test_logger2")
    logger3 = logging.getLogger("test_logger3")
    logger4 = logging.getLogger("test_logger4")
    logger1.setLevel(logging.DEBUG)
    logger2.setLevel(logging.DEBUG)
    logger3.setLevel(logging.DEBUG)
    logger4.setLevel(logging.DEBUG)
    log.register_logger(logger1)
    log.register_logger(logger2)
    log.register_logger(logger3)
    log.register_logger(logger4)
    assert logger1.level != logging.WARNING
    assert logger2.level != logging.WARNING
    assert logger3.level != logging.WARNING
    assert logger4.level != logging.WARNING
    log.set_level(logging.WARNING)
    assert logger1.level == logging.WARNING
    assert logger2.level == logging.WARNING
    assert logger3.level == logging.WARNING
    assert logger4.level == logging.WARNING


def test_set_level_level_is_not_an_integer(setup_logging):
    """TypeError raised if the logging level is not an integer."""
    with pytest.raises(TypeError) as cm:
        log.set_level("not a logging level")

    assert str(cm.value) == (
        "level should be an integer value one of [0, 10, 20, 30, 40, 50] or "
        "[NOTSET, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL] of the "
        "logging library, not str: 'not a logging level'"
    )


def test_set_level_level_is_not_a_proper_logging_level(setup_logging):
    """ValueError raised if the logging level is not in correct value."""
    with pytest.raises(ValueError) as cm:
        log.set_level(1000)

    assert str(cm.value) == (
        "level should be an integer value one of [0, 10, 20, 30, 40, 50] or "
        "[NOTSET, DEBUG, INFO, WARN, WARNING, ERROR, FATAL, CRITICAL] of the "
        "logging library, not 1000."
    )


def test_get_logger_name_is_not_a_string(setup_logging):
    """stalker.get_logger() raises a TypeError if the name attribute is not
    a str."""
    with pytest.raises(TypeError) as cm:
        log.get_logger(2123)
    assert str(cm.value) == "A logger name must be a string"


def test_get_logger_creates_a_logger(setup_logging):
    """stalker.log.get_logger() returns a Logger instance."""
    logger = log.get_logger("logger")
    assert isinstance(logger, logging.Logger)


def test_get_logger_registers_the_new_logger_already(setup_logging):
    """stalker.log.get_logger() registers the new logger."""
    logger = log.get_logger("logger")
    assert logger in log.loggers


def test_get_logger_sets_the_logging_level_to_the_default_one(setup_logging):
    """stalker.log.get_logger() sets the logging level to the default one."""
    logger = log.get_logger("logger")
    assert logger.level == log.logging_level
