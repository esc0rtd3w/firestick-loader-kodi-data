# coding: utf-8
from os import path
from re import sub, findall
from urlparse import urlparse

import xbmcaddon

from utils import get_int, get_float

__author__ = 'Mancuniancol'


# read provider xbmcaddon.Addon()
class MetaSettings(type):
    @classmethod
    def __setitem__(mcs, item, value):
        mcs.value[item] = value

    @classmethod
    def __getitem__(mcs, item):
        # default values
        if item is "max_magnets":
            return get_int(mcs.value.get(item, "10"))
        elif item is "separator":
            return mcs.value.get(item, "%20")
        elif item is "time_noti":
            return get_int(mcs.value.get(item, "750"))
        elif item.endswith("accept"):
            temp = mcs.value.get(item, "{*}")
            return "{*}" if temp is "" else temp
        elif item.endswith("max_size"):
            return get_float(mcs.value.get(item, "10"))
        elif item.endswith("min_size"):
            return get_float(mcs.value.get(item, "0"))
        else:
            return mcs.value.get(item, "")

    # General information
    id_addon = xbmcaddon.Addon().getAddonInfo('ID')  # gets name
    icon = xbmcaddon.Addon().getAddonInfo('icon')
    fanart = xbmcaddon.Addon().getAddonInfo('fanart')
    path_folder = xbmcaddon.Addon().getAddonInfo('path')
    name = xbmcaddon.Addon().getAddonInfo('name')  # gets name
    clean_name = sub('.COLOR (.*?)]', '', name.replace('[/COLOR]', ''))
    value = {}  # it contains all the settings from xml file
    file_name = path.join(path_folder, "resources", "settings.xml")
    if path.isfile(file_name):
        with open(file_name, 'r') as fp:
            data = fp.read()
        for key in findall('id="(\w+)"', data):
            value[key] = xbmcaddon.Addon().getSetting(key)  # reading the values from xbmcaddon.Addon().xml
    temp = urlparse(value.get('general_url', ""))
    url = '%s://%s' % (temp.scheme, temp.netloc)


class Settings(object):
    def __init__(self):
        pass

    __metaclass__ = MetaSettings
    pass

    @staticmethod
    def string(id_value):
        return xbmcaddon.Addon().getLocalizedString(id_value)

    @classmethod
    def get_icon_path(cls):
        return path.join(cls.path_folder, 'icon.png')

    # Borrowed from xbmcswift2
    @staticmethod
    def get_setting(key, converter=str, choices=None):
        value = xbmcaddon.Addon().getSetting(id=key)
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

    # Borrowed from xbmcswift2
    @staticmethod
    def set_setting(key, val):
        return xbmcaddon.Addon().setSetting(id=key, value=val)

    # Borrowed from xbmcswift2
    @staticmethod
    def open_settings():
        """"Opens the settings dialog within KODI"""
        xbmcaddon.Addon().openSettings()

    # open the images from /resources/images
    @staticmethod
    def dir_images(value):
        image_file = path.join(Settings.path_folder, 'resources', 'images', value)
        if not path.isfile(image_file):
            image_file = Settings.icon
        return image_file
