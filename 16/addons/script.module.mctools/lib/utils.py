# coding: utf-8
# Name:        utils.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Helper methods
"""
import os
import re
import urllib2
import xbmc
import xbmcgui
from contextlib import closing
from json import loads

import video_info
from constants import *


def add_library(imdb_id=None):
    """
    Add a video to the library using the imdb id from the video
    :param imdb_id: imdb id from video
    :type imdb_id: str or None
    :return:
    """
    if imdb_id:
        if video_info.Video.info(imdb_id):
            if video_info.Video.add_to_library(imdb_id):
                if not video_info.Video.is_movie:
                    video_info.Video.add_subscription(imdb_id)
                if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                    xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information


def magnetizer():
    """
    Run Magnetizer
    :return:
    """
    import contextitem
    contextitem.main()


def check_parser(parser=""):
    """
    Verify the parser's health
    :param parser: name of parser to check
    :type parser: str
    :return: string with the duration and number of collected results
    """
    magnetic_url = "http://%s:%s" % (str(MAGNETIC_SERVICE_HOST), str(MAGNETIC_SERVICE_PORT))
    title = 'simpsons'
    if 'nyaa' in parser:
        title = 'one%20piece'

    if 'yts' in parser:
        title = 'batman%201989'

    url = magnetic_url + "?search=general&title=%s&parser=%s" % (title, parser)
    results = dict()
    try:
        req = urllib2.Request(url, None)
        with closing(urllib2.urlopen(req, timeout=120)) as response:
            results = loads(response.read())

    except Exception as e:
        print "Error checking parser %s: %s" % (parser, repr(e))

    duration = results.get('duration', '[COLOR FFC40401]Error[/COLOR]')
    items = results.get('results', 'zero')
    return " [%s for %s items]" % (duration, items)


def check_group_parser():
    """
    Verify the health of enabled parsers
    """
    magnetic_url = "http://%s:%s" % (str(MAGNETIC_SERVICE_HOST), str(MAGNETIC_SERVICE_PORT))
    title = '12%20monkeys'
    url = magnetic_url + "?search=general&title=%s" % title
    results = dict()
    try:
        req = urllib2.Request(url, None)
        with closing(urllib2.urlopen(req, timeout=120)) as response:
            results = loads(response.read())

    except Exception as e:
        print "Error checking enabled parsers: %s" % (repr(e))

    duration = results.get('duration', '[COLOR FFC40401]Error[/COLOR]')
    items = results.get('results', 'zero')

    return " [%s for %s items]" % (duration, items)


def get_list_parsers():
    """
    Get the list of installed parsers
    :return: list of installed parsers
    """
    results = []
    list_parsers = loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", '
                                             '"method": "Addons.GetAddons", '
                                             '"id": 1, '
                                             '"params": {"type" : "xbmc.python.script", '
                                             '"properties": ["enabled", "name", "thumbnail", "fanart"]}}'))
    for one_parser in list_parsers["result"].get("addons", []):
        if one_parser['addonid'].startswith('script.magnetic.'):
            results.append(one_parser)

    return results


def get_list_parsers_enabled():
    """
    Get the list of enabled parsers
    :return: list of enable parsers
    """

    results = []
    list_parsers = loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", '
                                             '"method": "Addons.GetAddons", '
                                             '"id": 1, '
                                             '"params": {"type" : "xbmc.python.script", '
                                             '"properties": ["enabled", "name"]}}'))
    for one_parser in list_parsers["result"].get("addons", []):
        if one_parser['addonid'].startswith('script.magnetic.') and one_parser['enabled']:
            results.append(one_parser['addonid'])

    return results


def disable_parser(parser):
    """
    Disable a specific parser
    :param parser: parser to disable
    :type parser: str
    """
    xbmc.executeJSONRPC('{"jsonrpc":"2.0",'
                        '"method":"Addons.SetAddonEnabled",'
                        '"id":1,"params":{"addonid":"%s","enabled":false}}' % parser)


def enable_parser(parser):
    """
    Enable a specific parser
    :param parser: parser to enable
    :type parser: str
    """
    xbmc.executeJSONRPC('{"jsonrpc":"2.0",'
                        '"method":"Addons.SetAddonEnabled",'
                        '"id":1,"params":{"addonid":"%s","enabled":true}}' % parser)


def get_setting(key, converter=str, choices=None):
    """
    Read add-on's settings
    # Borrowed from xbmc swift2
    :param key: parameter to read
    :type key: str
    :param converter: type of parameter
    :type converter: object
    :param choices: if the parameter has different values, it could pick one
    :type choices: object
    :return:
    """
    value = ADDON.getSetting(id=key)
    if converter is str:
        return value

    elif converter is unicode:
        return value.decode('utf-8')

    elif converter is bool:
        return value == 'true'

    elif converter is int:
        return int(value)

    elif isinstance(choices, (list, tuple)):
        return choices[int(value)]

    else:
        raise TypeError('Acceptable converters are str, unicode, bool and '
                        'int. Acceptable choices are instances of list '
                        ' or tuple.')


def set_setting(key, value):
    """
    Modify add-on's settings
    :param key: parameter to modify
    :type key: str
    :param value: value of the parameter
    :type value: str
    """
    ADDON.setSetting(key, value)


def get_icon_path():
    """
    Get the path from add-on's icon
    :return: icon's path
    """
    addon_path = xbmcaddon.Addon().getAddonInfo("path")

    return os.path.join(addon_path, 'icon.png')


def string(id_value):
    """
    Internationalisation string
    :param id_value: id value from string.po file
    :type id_value: int
    :return: the translated string
    """
    return xbmcaddon.Addon().getLocalizedString(id_value)


def get_int(text):
    """
    Convert string to integer number
    :param text: string to convert
    :type text: str
    :return: converted string in integer
    """
    return int(get_float(text))


def get_float(text):
    """
    Convert string to float number
    :param text: string to convert
    :type text: str
    :return: converted string in float
    """
    value = 0
    if isinstance(text, (float, long, int)):
        value = float(text)

    elif isinstance(text, str):
        # noinspection PyBroadException
        try:
            text = clean_number(text)
            match = re.search('([0-9]*\.[0-9]+|[0-9]+)', text)
            if match:
                value = float(match.group(0))

        except:
            value = 0

    return value


# noinspection PyBroadException
def size_int(size_txt):
    """
    Convert string with size format to integer
    :param size_txt: string to be converted
    :type size_txt: str
    :return: converted string in integer
    """
    try:
        return int(size_txt)

    except:
        size_txt = size_txt.upper()
        size1 = size_txt.replace('B', '').replace('I', '').replace('K', '').replace('M', '').replace('G', '')
        size = get_float(size1)
        if 'K' in size_txt:
            size *= 1000

        if 'M' in size_txt:
            size *= 1000000

        if 'G' in size_txt:
            size *= 1e9

        return size


def clean_number(text):
    """
    Convert string with a number to USA decimal format
    :param text: string with the number
    :type text: str
    :return: converted number in string
    """
    comma = text.find(',')
    point = text.find('.')
    if comma > 0 and point > 0:
        if comma < point:
            text = text.replace(',', '')

        else:
            text = text.replace('.', '')
            text = text.replace(',', '.')

    return text


def notify(message, image=None):
    """
    Create notification dialog
    :param message: message to notify
    :type message: str
    :param image: path of the image
    :type image: str
    """
    dialog = xbmcgui.Dialog()
    dialog.notification(ADDON_NAME, message, icon=image)
    del dialog


def display_message_cache():
    """
    Create the progress dialog when the cache is used
    """
    p_dialog = xbmcgui.DialogProgressBG()
    p_dialog.create('Magnetic Manager', string(32061))
    xbmc.sleep(250)
    p_dialog.update(25, string(32065))
    xbmc.sleep(250)
    p_dialog.update(50, string(32065))
    xbmc.sleep(250)
    p_dialog.update(75, string(32065))
    xbmc.sleep(250)
    p_dialog.close()
    del p_dialog


def clean_cache():
    """
    Clean all cache
    :return:
    """
    storage_path = os.path.join(xbmc.translatePath("special://temp"), ".storage")
    if os.path.isdir(storage_path):
        for f in os.listdir(storage_path):
            if re.search('.cache', f):
                os.remove(os.path.join(storage_path, f))

    cookies_path = xbmc.translatePath("special://temp")
    if os.path.isdir(cookies_path):
        for f in os.listdir(cookies_path):
            if re.search('.jar', f):
                os.remove(os.path.join(cookies_path, f))


def timedelta_total_seconds(timedelta):
    """
    Count seconds
    :param timedelta:
    :return: seconds
    """
    return (timedelta.microseconds + 0.0 + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def find_imdb(title=None):
    """
    Get imdb from title
    :param title: title of the video
    :type title: str or None
    :return: imdb id
    """
    return video_info.find_imdb(title)
