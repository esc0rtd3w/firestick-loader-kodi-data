import json
import os
import re
import sys
import traceback
import urllib2
import xbmc

from aussieaddonscommon import utils

from distutils.version import LooseVersion


GITHUB_API_URL = 'https://api.github.com/repos/aussieaddons/issue-reports'
GITHUB_API_TOKEN = 'ab181e16a94e918bf81' + '7d86778599926126e0e30'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
GIST_API_URL = 'https://api.github.com/gists'
ORG_API_URL= 'https://api.github.com/orgs/aussieaddons/repos'


# Filter out username and passwords from log files
LOG_FILTERS = (
    ('//.+?:.+?@', '//[FILTERED_USER]:[FILTERED_PASSWORD]@'),
    ('<user>.+?</user>', '<user>[FILTERED_USER]</user>'),
    ('<pass>.+?</pass>', '<pass>[FILTERED_PASSWORD]</pass>'),
)


def make_request(url):
    """Make our JSON request to GitHub"""
    return urllib2.Request(url, headers={
        "Authorization": "token %s" % GITHUB_API_TOKEN,
        "Content-Type": "application/json",
    })


def get_connection_info():
    """Get connection details

    Fetch the details for the users Internet connection for logging
    and filtering by country
    """
    try:
        utils.log('Fetching connection information...')
        result = urllib2.urlopen('http://ipinfo.io/json', timeout=5)
        return json.loads(result.read())
    except Exception:
        utils.log(traceback.format_exc())
        utils.log('Failed to fetch connection information')
    return None


def get_kodi_log():
    """Get XBMC log

    Fetch and read the Kodi log
    """
    log_path = xbmc.translatePath('special://logpath')

    if os.path.isfile(os.path.join(log_path, 'kodi.log')):
        log_file_path = os.path.join(log_path, 'kodi.log')
    elif os.path.isfile(os.path.join(log_path, 'xbmc.log')):
        log_file_path = os.path.join(log_path, 'xbmc.log')
    else:
        # No log file found
        return None

    utils.log("Reading log file from \"%s\"" % log_file_path)
    with open(log_file_path, 'r') as f:
        log_content = f.read()
    for pattern, repl in LOG_FILTERS:
        log_content = re.sub(pattern, repl, log_content)
    return log_content


def fetch_tags(github_repo):
    """Fetch GitHub tags

    Given a GitHub repo, in the format of username/repository, fetch the list
    of git tags via the API
    """
    api_url = 'https://api.github.com/repos/%s/tags' % github_repo
    return json.load(urllib2.urlopen(api_url))


def get_versions(github_repo):
    """Get versions from tags

    Assemble a list of versions from the tags and strip any leading 'v'
    """
    tags = fetch_tags(github_repo)
    versions = map(lambda tag: tag['name'].lstrip('v'), tags)
    return versions


def get_latest_version(github_repo):
    """Get latest version number

    Sort the list of versions, and get the latest version
    """
    versions = get_versions(github_repo)
    latest_version = sorted(versions, reverse=True, key=LooseVersion)[0]
    return latest_version


def is_not_latest_version(current_version, latest_version):
    """Is not latest version

    Compare current_version and latest_version as x.x.x strings
    """
    return LooseVersion(current_version) < LooseVersion(latest_version)


def not_already_reported(error):
    """Is the user allowed to send this error?

    Check to see if our new error message is different from the last
    successful error report. If it is, or the file doesn't exist, then
    we'll return True
    """
    try:
        rfile = os.path.join(utils.get_file_dir(), 'last_report_error.txt')

        if not os.path.isfile(rfile):
            return True
        else:
            f = open(rfile, 'r')
            report = f.read()
            if report != error:
                return True
    except Exception as e:
        utils.log("Error checking error report file: %s" % str(e))
        return False

    utils.log("Not allowing error report. Last report matches this one")
    return False


def save_last_error_report(error):
    """Save a copy of our last error report"""
    try:
        rfile = os.path.join(utils.get_file_dir(), 'last_report_error.txt')
        with open(rfile, 'w') as f:
            f.write(error)
    except Exception:
        utils.log("Error writing error report file")


def get_org_repos():
    data = json.loads(urllib2.urlopen(ORG_API_URL).read())
    listing = []
    for repo in data:
        listing.append(repo.get('name'))
    return listing


def is_supported_addon():
    if utils.get_addon_id() in get_org_repos():
        return True


def is_reportable(exc_type, exc_value, exc_traceback):
    """Can we send an error report

    Based on a set of criteria, return a boolean determining whether the user
    should be allowed to send an error report.

    We prevent error reports being sent if:
      * The same report has already been sent
      * The error isn't blacklisted (mostly user networking issues)
    """

    # AttributeError: global name 'foo' is not defined
    error = '%s: %s' % (
        exc_type.__name__, ', '.join(
            utils.ensure_ascii(x) for x in exc_value.args))

    # Don't show any dialogs when user cancels
    if exc_type.__name__ == 'SystemExit':
        return False

    # Work out if we should allow an error report
    if not not_already_reported(error):
        return False

    # Some transient network errors we don't want any reports about
    blacklist_errors = ['The read operation timed out',
                        'IncompleteRead',
                        'getaddrinfo failed',
                        'No address associated with hostname',
                        'Connection reset by peer',
                        'HTTP Error 404: Not Found']

    if any(s in exc_type.__name__ for s in blacklist_errors):
        return False

    # If it's one of our custom exceptions, and it has reportable = False
    # set, then we'll honour that here.
    try:
        if not exc_value.is_reportable():
            return False
    except AttributeError:
        pass

    return True


def valid_country(connection_info):
    """Check user is in supported country before submitting error report"""
    whitelist = ['AU']

    if not connection_info:
        return False

    if connection_info.get('country') in whitelist:
        return True

    return False


def blacklisted_hostname(connection_info):
    """Check users hostname against a blacklist

    Some VPNs/proxys are known to content providers and will return 403
    responses. Blacklisting these to avoid issues reports caused by this.
    """
    org_blacklist = ['highwinds',
                     'softlayer',
                     'micfo',
                     'total server solutions',  # PIA
                     'host universal pty ltd',  # NordVPN
                     'AS45671']  # serversaustralia.com.au

    hostname_blacklist = ['ipvanish',
                          'zoogvpn',
                          'sl-reverse']

    if not connection_info:
        return False

    org = connection_info.get('org')
    if org:
        for item in org_blacklist:
            if item in org.lower():
                return True

    hostname = connection_info.get('hostname')
    if hostname:
        for item in hostname_blacklist:
            if item in hostname:
                return True

    return False


def generate_report(title, log_url=None, trace=None, connection_info={}):
    """Build our formatted GitHub issue string"""
    try:
        # os.uname() is not available on Windows
        uname = os.uname()
        os_string = ' (%s %s %s)' % (uname[0], uname[2], uname[4])
    except AttributeError:
        os_string = ''

    content = [
        "*Automatic bug report from end-user.*",
        "\n## Environment\n",
        "**Add-on Name:** %s" % utils.get_addon_name(),
        "**Add-on ID:** %s" % utils.get_addon_id(),
        "**Add-on Version:** %s" % utils.get_addon_version(),
        "**Add-on URL:** %s" % sys.argv[2],
        "**Kodi Version:** %s" % utils.get_kodi_version(),
        "**Python Version:** %s" % sys.version.replace('\n', ''),
        "**IP Address:** %s" % connection_info.get('ip', 'N/A'),
        "**Hostname:** %s" % connection_info.get('hostname', 'N/A'),
        "**Country:** %s" % connection_info.get('country', 'N/A'),
        "**ISP:** %s" % connection_info.get('org', 'N/A'),
        "**Operating System:** %s %s" % (sys.platform, os_string),
        "**Platform:** %s" % utils.get_platform(),
        "**Python Path:**\n```\n%s\n```" % '\n'.join(sys.path),
    ]

    if trace:
        content.append("\n## Traceback\n```\n%s\n```" % trace)

    if log_url:
        content.append("\n[Full log](%s)" % log_url)

    short_id = utils.get_addon_id().split('.')[-1]
    title = '[%s] %s' % (short_id, title)
    # Github throws HTTP 422 if title is too long
    report = {
        'title': title[:255],
        'body': '\n'.join(content)
    }

    return report


def upload_report(report):
    try:
        response = urllib2.urlopen(make_request(ISSUE_API_URL),
                                   json.dumps(report))
    except urllib2.HTTPError as e:
        utils.log("Failed to report issue: HTTPError %s\n %s" % (
            e.code, e.read()))
        return False
    except urllib2.URLError as e:
        utils.log("Failed to report issue: URLError %s" % e.reason)
        return False

    try:
        return json.load(response)["html_url"]
    except Exception:
        utils.log("Failed to parse API response: %s" % response.read())


def upload_log():
    """Upload our full Kodi log as a GitHub gist"""
    try:
        log_content = get_kodi_log()
    except Exception as e:
        utils.log("Failed to read log: %s" % e)
        return

    utils.log('Sending log file...')
    try:
        data = {
            "files": {
                "kodi.log": {
                    "content": log_content
                }
            }
        }
        response = urllib2.urlopen(make_request(GIST_API_URL),
                                   json.dumps(data))
    except urllib2.HTTPError as e:
        utils.log("Failed to save log: HTTPError %s" % e.code)
        return False
    except urllib2.URLError as e:
        utils.log("Failed to save log: URLError %s" % e.reason)
        return False
    try:
        return json.load(response)['html_url']
    except Exception:
        utils.log("Failed to parse API response: %s" % response.read())


def report_issue(title, trace=None, connection_info=None):
    """Report our issue to GitHub"""
    log_url = None
    try:
        log_url = upload_log()
    except Exception:
        utils.log(traceback.format_exc())
        raise Exception('Failed to upload log file')

    utils.log('Sending report...')
    try:
        report = generate_report(title, log_url=log_url, trace=trace,
                                 connection_info=connection_info)
        report_url = upload_report(report)
        utils.log('Report URL: %s' % report_url)
        return report_url
    except Exception:
        utils.log(traceback.format_exc())
        raise Exception('Failed to upload issue report')
