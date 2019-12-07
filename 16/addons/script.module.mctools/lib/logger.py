# coding: utf-8
# Name:        logger.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Create entry in Kodi's log
"""
import logging
import xbmc
import xbmcaddon

from normalize import clear_string


class XBMCHandler(logging.StreamHandler):
    xbmc_levels = {
        'DEBUG': 0,
        'INFO': 2,
        'WARNING': 3,
        'ERROR': 4,
        'LOGCRITICAL': 5,
    }

    def emit(self, record):
        xbmc_level = self.xbmc_levels.get(record.levelname)
        xbmc.log(self.format(record), xbmc_level)


def _get_logger():
    logger = logging.getLogger(xbmcaddon.Addon().getAddonInfo("id"))
    logger.setLevel(logging.DEBUG)
    handler = XBMCHandler()
    handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    logger.addHandler(handler)
    return logger


log = _get_logger()


def debug(message=''):
    """
    Call Logger debug
    :param message: message to the log
    :type message: object
    :return:
    """
    try:
        if xbmcaddon.Addon().getSetting("mode_debug") not in 'false':
            log.info(clear_string(message))

    except Exception as e:
        print "Error logger: %s" % repr(e)


def error(message=''):
    """
    Call Logger error
    :param message: message to the log
    :type message: object
    :return:
    """
    try:
        log.error(clear_string(message))

    except Exception as e:
        print "Error logger: %s" % repr(e)


def info(message=''):
    """
    Call Logger info
    :param message: message to the log
    :type message: object
    :return:
    """
    try:
        log.info(clear_string(message))

    except Exception as e:
        print "Error logger: %s" % repr(e)


def warning(message=''):
    """
    Call Logger warning
    :param message: message to the log
    :type message: object
    :return:
    """
    try:
        log.warning(clear_string(message))

    except Exception as e:
        print "Error logger: %s" % repr(e)
