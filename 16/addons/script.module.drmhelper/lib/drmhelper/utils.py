import re

from drmhelper import config

import xbmc

import xbmcaddon

import xbmcgui


def get_info_label(label, attempts=0):
    """Get XBMC info label

    In some cases, Kodi will return a value of 'Busy' if the value is not
    yet available. Loop a maximum of 10 attempts with a small sleep until
    we get the value, or return nothing.
    """
    if attempts > 10:
        return  # fail after 10 attempts

    value = xbmc.getInfoLabel(label)
    if value == 'Busy':
        xbmc.sleep(100)
        attempts += 1
        return get_info_label(label, attempts=attempts)

    return value


def get_addon_name():
    """Helper function for returning the version of the running add-on"""
    return xbmcaddon.Addon().getAddonInfo('name')


def get_addon_version():
    """Helper function for returning the version of the running add-on"""
    return xbmcaddon.Addon().getAddonInfo('version')


def log(message):
    """Logging helper"""
    xbmc.log("[%s v%s] %s" % (
        get_addon_name(), get_addon_version(), message),
             level=xbmc.LOGNOTICE)


def get_kodi_build():
    """Return the Kodi build version

    In the format of 17.6 Git:20171119-ced5097
    """
    try:
        return get_info_label('System.BuildVersion')
    except Exception:
        return


def get_kodi_version():
    """Return the version number of Kodi

    Also strip off any extra chars, like -ALPHA1
    """
    build = get_kodi_build()
    version = build.split(' ')[0]
    version = version.split('-')[0]
    return version


def get_kodi_major_version():
    """Return the major version number of Kodi"""
    version = get_kodi_version().split('.')[0]
    return int(version)


def get_kodi_name():
    """Returns Kodi codename"""
    version = get_kodi_major_version()
    return config.KODI_NAME.get(version)


def get_kodi_build_date():
    """Return Kodi build date

    Kodi build date is extracted from a build string like:
    17.6 Git:20171119-ced5097
    """
    build_string = get_kodi_build()
    try:
        build_string = build_string.split(' ')[1]
    except IndexError:
        return None

    # Extract date
    match = re.search(r'20\d{6}', build_string)
    if match:
        return match.group(0)
    return match


def get_addon_string():
    return '{0} {1}'.format(get_addon_name(), get_addon_version())


def dialog(*args):
    xbmcgui.Dialog().ok(*args)
    msg = '. '.join(list(args))
    log('DIALOG: {0}'.format(msg))


def dialog_yn(*args, **kwargs):
    val = xbmcgui.Dialog().yesno(*args)
    msg = '. '.join(list(args))
    log('DIALOG Y/N: {0}. Answer: {1}'.format(msg, bool(val)))
    return val
