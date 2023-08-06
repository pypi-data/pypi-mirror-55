import logging
import merchant
from fishbase.fish_logger import logger


def log_info(info):
    if logging.INFO == merchant.log_level:
        logger.info(merchant.log_tag + '{}'.format(info))


def log_warning(warning_info):
    if merchant.log_level in [logging.INFO, logging.WARNING]:
        logger.warning(merchant.log_tag + '{}'.format(warning_info))


def log_error(error_info):
    if merchant.log_level in [logging.INFO, logging.WARNING, logging.ERROR]:
        logger.error(merchant.log_tag + '{}'.format(error_info))
