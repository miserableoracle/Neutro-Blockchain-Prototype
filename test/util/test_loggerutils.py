"""test logging"""
import pytest
import logging

from src.util import loggerutil


logging.getLogger().debug("test_logging_debug")
logging.getLogger().info("test_logging_info")
logging.getLogger().warning("test_logging_warning")
logging.getLogger().error("test_logging_error")
