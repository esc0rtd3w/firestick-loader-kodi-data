# coding: utf-8
# Name:        magnetic.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Normalization and clear string
"""


# noinspection PyBroadException
def normalize_string(name):
    """
    Normalize a string
    :param name: string to normalize
    "type name: str
    :return: normalized string
    """
    from unicodedata import normalize
    import types
    if types.StringType == type(name):
        unicode_name = unicode(name, 'utf-8', 'ignore')

    else:
        unicode_name = name

    normalize_name = normalize('NFKD', unicode_name).encode('ascii', 'ignore')

    return normalize_name


# noinspection PyBroadException
def clear_string(name):
    """
    Convert all the &# codes to char, remove extra-space and normalize
    :param name: string to convert
    :type name: object
    :return: converted string
    """
    from HTMLParser import HTMLParser
    if type(name) is not unicode:
        name = name.__str__()
    if type(name) is str:
        try:
            name = name.decode('utf-8')

        except:
            name = unicode(name, 'utf-8', errors='replace')

    name = name.replace('<![CDATA[', '').replace(']]', '')
    name = HTMLParser().unescape(name)
    if type(name) is not str:
        name = name.encode('utf-8')

    return name


def safe_name(value):
    """
    Make the name directory and filename safe
    :param value: string to convert
    :type value: str or unicode
    :return: converted string
    """
    from urllib import unquote
    value = unquote(value)
    value = clear_string(value)
    value = value.lower().title()
    keys = {'"': ' ', '*': ' ', '/': ' ', ':': ' ', '<': ' ', '>': ' ', '?': ' ', '|': ' ', '_': ' ',
            "'": '', 'Of': 'of', 'De': 'de', '.': ' ', ')': ' ', '(': ' ', '[': ' ', ']': ' ', '-': ' '}
    for key in keys.keys():
        value = value.replace(key, keys[key])

    value = ' '.join(value.split())

    return value.replace('S H I E L D', 'SHIELD')
