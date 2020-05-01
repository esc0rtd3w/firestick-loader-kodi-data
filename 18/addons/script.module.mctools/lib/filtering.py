# coding: utf-8
# Name:        filtering.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Filtering code for results in Magnetic
"""
import logger
from browser import Magnet
from utils import get_float


def apply_filters(results_list):
    """
    Filter the results
    :param results_list: values to filter
    :type results_list: list
    :return: list of filtered results
    """
    logger.debug(results_list)
    results_list = cleanup_results(results_list)
    logger.debug(results_list)
    results_list = sort_by_quality(results_list)
    logger.debug(results_list)

    return results_list


def cleanup_results(results_list):
    """
    Remove dupes and sort by seeds
    :param results_list: values to filter
    :type results_list: list
    :return: list of cleaned results
    """
    # nothing found
    if len(results_list) == 0:
        return []

    filtered_list = []
    for result in results_list:
        # check parser returns seeds
        # get_int(result['seeds'])
        # append hash
        result['hash'] = Magnet(result['uri']).info_hash.upper()
        logger.debug(result['hash'])
        # remove dupes
        # noinspection PyTypeChecker
        if len([item for item in filtered_list if item['hash'].upper() == result['hash'].upper()]) == 0 or len(
                result['hash']) == 0:
            # append item to results
            filtered_list.append(result)

    return sorted(filtered_list, key=lambda r: (get_float(r['seeds'])), reverse=True)


def check_quality(text=""):
    """
    Get the quality values from string
    :param text: string with the name of the file
    :type text: str
    :return:
    """
    text = text.lower()
    quality = "480p"

    if "480p" in text:
        quality = "480p"

    if "720p" in text:
        quality = "720p"

    if "1080p" in text:
        quality = "1080p"

    if "3d" in text:
        quality = "1080p"

    if "4k" in text:
        quality = "2160p"

    return quality


def sort_by_quality(results_list):
    """
    Apply sorting based on seeds and quality
    :param results_list: list of values to be sorted
    :type results_list: list
    :return: list of sorted results
    """
    logger.debug("Applying quality sorting")
    for result in results_list:
        # hd streams
        quality = check_quality(result['name'])
        if "1080p" in quality:
            result['quality'] = 3
            result['hd'] = 1

        elif "720p" in quality:
            result['quality'] = 2
            result['hd'] = 1

        else:
            result['quality'] = 1
            result['hd'] = 0

    return sorted(results_list, key=lambda r: (r["seeds"], r['hd'], r['quality'], r["peers"]), reverse=True)
