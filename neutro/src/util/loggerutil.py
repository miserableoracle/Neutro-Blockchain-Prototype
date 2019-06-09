"""
utils for logging
"""
import logging
import time
import inspect

from pathlib import Path

log_path = str(Path(__file__).parent.parent.parent) + "/.log/"
Path(log_path).mkdir(parents=True, exist_ok=True)
file_name = time.strftime("%Y-%m-%d", time.gmtime())
string_format = "%(asctime)s [%(levelname)-7.7s]%(message)s\n"

logging.basicConfig(
    level=logging.DEBUG,
    format=string_format,
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(log_path, file_name)),
        # logging.StreamHandler()
    ])


def debug(message: str):
    """wrapper, so that configuration is loaded"""
    logging.getLogger().debug(_format_message(message))


def info(message: str):
    """wrapper, so that configuration is loaded"""
    logging.getLogger().info(_format_message(message))


def warning(message: str):
    """wrapper, so that configuration is loaded"""
    logging.getLogger().warning(_format_message(message))


def error(message: str):
    """wrapper, so that configuration is loaded"""
    logging.getLogger().error(_format_message(message))


def _format_message(message: str)->str:
    stack = inspect.stack()[2]
    return "[{0: <15}]:\n".format(str(stack[1]) + ":" + str(stack[2])) + message
