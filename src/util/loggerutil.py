"""
utils for logging
"""
import time
import logging

from pathlib import Path

log_path = str(Path(__file__).parent.parent.parent) + "/log/"
Path(log_path).mkdir(parents=True, exist_ok=True)
file_name = time.strftime("%Y-%m-%d", time.gmtime())
string_format = "%(asctime)s [%(levelname)-7.7s][%(pathname)s %(funcName)s %(lineno)d]:\n%(message)s\n"

logging.basicConfig(
    level=logging.DEBUG,
    format=string_format,
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(log_path, file_name)),
        logging.StreamHandler()
    ])


# TODO put in test.
def test_logger():
    logging.getLogger().debug("test_logging_debug")
    logging.getLogger().info("test_logging_info")
    logging.getLogger().warning("test_logging_warning")
    logging.getLogger().error("test_logging_error")

    logging.getLogger().info("test\nmultiline\nlogging")
