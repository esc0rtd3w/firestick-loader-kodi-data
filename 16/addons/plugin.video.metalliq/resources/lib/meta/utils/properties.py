from xbmcswift2 import xbmcgui
from meta import plugin

def get_property(name):
    home = xbmcgui.Window(10000)
    return home.getProperty(__get_property_name(name))

def set_property(name, value):
    home = xbmcgui.Window(10000)
    home.setProperty(__get_property_name(name), str(value))

def clear_property(name):
    home = xbmcgui.Window(10000)
    home.clearProperty(__get_property_name(name))

def __get_property_name(name):
    if "." not in name:
        name = plugin.id + "." + name
    return name
