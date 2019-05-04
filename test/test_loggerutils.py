"""test logging"""
import pytest
import logging

from src.util import loggerutils  # I DONT KNOW HOW THAT IS SUPPOSED TO WORK.


def test_logging():
    logging.getLogger().info("test_logging_info")
    logging.getLogger().debug("test_logging_debug")
    logging.getLogger().warning("test_logging_warning")
    logging.getLogger().error("test_logging_error")
