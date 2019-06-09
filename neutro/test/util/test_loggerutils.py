"""test logging"""
from neutro.src.util import loggerutil


def test_logger():
    loggerutil.debug("test_logging_debug")
    loggerutil.info("test_logging_info")
    loggerutil.warning("test_logging_warning")
    loggerutil.error("test_logging_error")
