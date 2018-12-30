import htmlentitydefs
import os
import re
import sys
import traceback
import unicodedata
import urllib
import xbmc
import xbmcaddon
import xbmcgui

# This import is to deal with a python bug with strptime:
#   ImportError: Failed to import _strptime because the import lockis
#   held by another thread.
import _strptime  # noqa: F401

ADDON = xbmcaddon.Addon()

# Used for fetching latest version information about the add-on
GITHUB_ORG = 'aussieaddons'

# HTML code escape
PATTERN = re.compile("&(\w+?);")


def get_addon_id():
    """Helper function for returning the version of the running add-on"""
    return ADDON.getAddonInfo('id')


def get_addon_name():
    """Helper function for returning the version of the running add-on"""
    return ADDON.getAddonInfo('name')


def get_addon_version():
    """Helper function for returning the version of the running add-on"""
    return ADDON.getAddonInfo('version')


def descape_entity(m, defs=htmlentitydefs.entitydefs):
    """Translate one entity to its ISO Latin value"""
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)  # use as is


def descape(string):
    """Translate html chars and ensure ascii"""
    string = ensure_ascii(string)
    string = PATTERN.sub(descape_entity, string)
    return string


def get_url(s):
    """Build a dict from a given Kodi add-on URL"""
    dict = {}
    pairs = s.lstrip("?").split("&")
    for pair in pairs:
        if len(pair) < 3:
            continue
        kv = pair.split("=", 1)
        k = kv[0]
        v = urllib.unquote_plus(kv[1])
        dict[k] = v
    return dict


def make_url(d):
    """Build a URL suitable for a Kodi add-on from a dict"""
    pairs = []
    for k, v in d.iteritems():
        k = urllib.quote_plus(k)
        v = ensure_ascii(v)
        v = urllib.quote_plus(v)
        pairs.append("%s=%s" % (k, v))
    return "&".join(pairs)


def ensure_ascii(s):
    """Force a string to acsii

    This is especially useful for Kodi menu items which will barf if given
    anything other than ascii
    """
    if not isinstance(s, unicode):
        s = str(s)
        s = s.decode("utf-8")
    return unicodedata.normalize('NFC', s).encode('ascii', 'ignore')


def get_file_dir():
    """Get our add-on working directory

    Make our add-on working directory if it doesn't exist and
    return it.
    """
    filedir = os.path.join(
        xbmc.translatePath('special://temp/'), get_addon_id())
    if not os.path.isdir(filedir):
        os.mkdir(filedir)
    return filedir


def log(s):
    """Logging helper"""
    xbmc.log("[%s v%s] %s" % (get_addon_name(), get_addon_version(),
                              ensure_ascii(s)), level=xbmc.LOGNOTICE)


def format_error_summary():
    """Format error summary

    From the traceback, generate a nicely formatted string showing the
    error message.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return "%s (%d) - %s: %s" % (
        os.path.basename(exc_traceback.tb_frame.f_code.co_filename),
        exc_traceback.tb_lineno, exc_type.__name__,
        ', '.join(exc_value.args))


def log_error(message=None):
    """Logging helper for exceptions"""
    try:
        xbmc.log("[%s v%s] ERROR: %s" %
                 (get_addon_name(), get_addon_version(),
                  format_error_summary()), level=xbmc.LOGERROR)
        xbmc.log(traceback.print_exc(), level=xbmc.LOGERROR)
    except Exception:
        pass


def format_dialog_message(msg, title=None):
    """Format a message suitable for a Kodi dialog box

    Valid input for msg is either a string (supporting newline chars) or a
    list of lines, with an optional title.
    """
    if title:
        content = [title]
    else:
        content = ["%s v%s" % (get_addon_name(), get_addon_version())]

    # Force unicode to str
    if type(msg) in [str, unicode]:
        msg = str(msg).split('\n')

    return content + msg


def format_dialog_error(msg=None):
    """Format an error message suitable for a Kodi dialog box"""
    title = "%s v%s ERROR" % (get_addon_name(), get_addon_version())
    error = format_error_summary()
    return format_dialog_message(error, title=title)


def dialog_message(msg, title=None):
    """Helper function for a simple 'OK' dialog"""
    content = format_dialog_message(msg, title)
    xbmcgui.Dialog().ok(*content)


def get_platform():
    """Get platform

    Work through a list of possible platform types and return the first
    match. Ordering of items is important as some match more than one type.

    E.g. Android will match both Android and Linux
    """
    platforms = [
        "Android",
        "Linux.RaspberryPi",
        "Linux",
        "XBOX",
        "Windows",
        "ATV2",
        "IOS",
        "OSX",
        "Darwin",
    ]

    for platform in platforms:
        if xbmc.getCondVisibility('System.Platform.'+platform):
            return platform
    return "Unknown"


def get_kodi_build():
    """Return the Kodi build version"""
    try:
        return xbmc.getInfoLabel("System.BuildVersion")
    except Exception:
        return


def get_kodi_version():
    """Return the version number of Kodi"""
    build = get_kodi_build()
    version = build.split(' ')[0]
    return version


def get_kodi_major_version():
    """Return the major version number of Kodi"""
    version = get_kodi_version().split('.')[0]
    return int(version)


def log_kodi_platform_version():
    """Log our Kodi version and platform for debugging"""
    version = get_kodi_version()
    platform = get_platform()
    log("Kodi %s running on %s" % (version, platform))


def is_valid_country(connection_info, message=None):
    if not message:
        message = format_dialog_message('Issue report denied.')

    import issue_reporter
    valid_country = issue_reporter.valid_country(connection_info)
    blacklisted_hostname = issue_reporter.blacklisted_hostname(connection_info)

    if not valid_country:
        country_code = connection_info.get('country')
        if country_code:
            import countries
            country_name = countries.countries.get(country_code, country_code)
            message.append('Your country is reported as %s, but this service '
                           'is probably geo-blocked to Australia.' %
                           country_name)
            xbmcgui.Dialog().ok(*message)
            return False

    if blacklisted_hostname:
        message.append('VPN/proxy detected that has been blocked by this '
                       'content provider.')
        xbmcgui.Dialog().ok(*message)
        return False

    return True


def user_report():
    send_report('User initiated report', user_initiated=True)


def send_report(title, trace=None, connection_info=None, user_initiated=False):
    try:
        import issue_reporter
        log("Reporting issue to GitHub")

        if not connection_info:
            connection_info = issue_reporter.get_connection_info()

        if user_initiated:
            if not is_valid_country(connection_info):
                return

        # Show dialog spinner, and close afterwards
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        report_url = issue_reporter.report_issue(title, trace, connection_info)

        split_url = report_url.replace('/issue-reports', ' /issue-reports')
        dialog_message(['Thanks! Your issue has been reported to: ',
                       split_url])
        return report_url
    except Exception:
        traceback.print_exc()
        log('Failed to send report')
    finally:
        xbmc.executebuiltin("Dialog.Close(busydialog)")


def handle_error(message):
    """Issue reporting handler

    This function should be called in the exception part of a try/catch block
    and provides the user (in some cases) the ability to send an error report.

    Tests are performed to ensure we don't accept some user network type
    errors (like timeouts, etc), any errors from old versions of an add-on or
    any duplicate reports from a user.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()

    # Don't show any dialogs when user cancels
    if exc_type.__name__ == 'SystemExit':
        return

    trace = traceback.format_exc()
    log(trace)

    # AttributeError: global name 'foo' is not defined
    error = '%s: %s' % (exc_type.__name__,
                        ', '.join(str(e) for e in exc_value.args))

    message = format_dialog_error(message)

    import issue_reporter

    connection_info = issue_reporter.get_connection_info()

    if not is_valid_country(connection_info, message):
        return

    is_reportable = issue_reporter.is_reportable(exc_type,
                                                 exc_value,
                                                 exc_traceback)

    # If already reported, or a non-reportable error, just show the error
    if not issue_reporter.not_already_reported(error) or not is_reportable:
        xbmcgui.Dialog().ok(*message)
        return

    github_repo = '%s/%s' % (GITHUB_ORG, get_addon_id())
    latest = issue_reporter.get_latest_version(github_repo)
    version = get_addon_version()

    if issue_reporter.is_not_latest_version(version, latest):
        message.append('Your version of this add-on (v%s) is outdated. Please '
                       'upgrade to the latest version: '
                       'v%s' % (version, latest))
        xbmcgui.Dialog().ok(*message)
        return

    if is_reportable:
        message.append('Would you like to automatically '
                       'report this error?')
        if xbmcgui.Dialog().yesno(*message):
            issue_url = send_report(error, trace=trace,
                                    connection_info=connection_info)
            if issue_url:
                issue_reporter.save_last_error_report(error)
