import os
import re
import posixpath
import xbmc
import xbmcgui
import xbmcaddon
import drmconfig
import platform
import requests
import json
import zipfile
from pipes import quote
from distutils.version import LooseVersion

system_ = platform.system()

# dummy request first for this infolabel, sometimes returns 'Busy'
xbmc.getInfoLabel('System.OSVersionInfo')
xbmc.sleep(100)

version_info = xbmc.getInfoLabel('System.OSVersionInfo')

if xbmc.getCondVisibility('system.platform.android'):
    system_ = 'Android'

try:
    machine = platform.machine()
    if machine[:3] == 'arm':
        machine = machine[:5]
    arch = drmconfig.ARCH_DICT.get(machine, 'NS')
except:
    arch = 'NS'

if system_ == 'Windows':
    try:
        arch = drmconfig.WINDOWS_BITNESS[platform.architecture()[0]]
    except:
        arch = 'Xbox One'

plat = '{0}-{1}'.format(system_, arch)

if plat in drmconfig.SUPPORTED_PLATFORMS:
    supported = True
    if system_ != 'Android':
        ssd_filename = drmconfig.SSD_WV_DICT[system_]
        widevinecdm_filename = drmconfig.WIDEVINECDM_DICT[system_]
else:
    supported = False


def log(message):
    """
    Log message to kodi.log
    """
    ver = xbmcaddon.Addon('script.module.drmhelper').getAddonInfo('version')
    xbmc.log('[DRMHELPER {0}] - {1}'.format(ver, message), xbmc.LOGNOTICE)


def is_libreelec():
    if 'LibreELEC' in version_info:
        return True
    return False


def get_kodi_version():
    """
    Return plain version number as string
    """
    fullver = xbmc.getInfoLabel("System.BuildVersion").split(' ')[0]
    ver = fullver[:fullver.find('-')]
    return ver


def get_kodi_name():
    """
    Returns Kodi codename
    """
    return drmconfig.KODI_NAME[get_kodi_version()[:2]]


def get_kodi_build():
    """
    Return Kodi build date
    """
    try:
        build_string = xbmc.getInfoLabel("System.BuildVersion").split(' ')[1]
    except IndexError:
        return None
    m = re.search('\d{8}', build_string)
    if m:
        return m.group(0)
    else:
        return m


def get_latest_ia_ver():
    """
    Return dict containing info for latest compiled inputstream.adaptive
    addon in the binary repo
    """
    kodi = get_kodi_name()
    return drmconfig.CURRENT_IA_VERSION[kodi]


def is_ia_current(addon, latest=False):
    """
    Check if inputstream.adaptive addon meets the minimum version requirements.
    latest -- checks if addon is equal to the latest available compiled version
    """
    if not addon:
        return False
    ia_ver = addon.getAddonInfo('version')
    if latest:
        ver = get_latest_ia_ver()['ver']
    else:
        ver = drmconfig.MIN_IA_VERSION[get_kodi_name()]
    return LooseVersion(ia_ver) >= LooseVersion(ver)


def get_addon(drm=True):
    """
    Check if inputstream.adaptive is installed, attempt to install if not.
    Enable inpustream.adaptive addon.
    """
    addon = None

    try:
        enabled_json = ('{"jsonrpc":"2.0","id":1,"method":'
                        '"Addons.GetAddonDetails","params":'
                        '{"addonid":"inputstream.adaptive", '
                        '"properties": ["enabled"]}}')
        # is inputstream.adaptive enabled?
        result = json.loads(xbmc.executeJSONRPC(enabled_json))
    except RuntimeError:
        return False

    if 'error' in result:  # not installed
        log('inputstream.adaptive not currently installed')
        try:  # see if there's an installed repo that has it
            xbmc.executebuiltin('InstallAddon(inputstream.adaptive)', True)
            addon = xbmcaddon.Addon('inputstream.adaptive')
            log('inputstream.adaptive installed from repo')
            return addon
        except RuntimeError:
            log('inputstream.adaptive not installed')
            xbmcgui.Dialog().ok('inputstream.adaptive not installed',
                                'inputstream.adaptive not installed. This '
                                'addon now comes supplied with newer builds '
                                'of Kodi 18 for Windows/Mac/LibreELEC/OSMC, '
                                'and can be installed from most Linux package '
                                'managers eg. "sudo apt install kodi-'
                                'inputstream-adaptive"')
        return False

    else:  # installed but not enabled. let's enable it.
        if result['result']['addon'].get('enabled') is False:
            log('inputstream.adaptive not enabled, enabling...')
            json_string = ('{"jsonrpc":"2.0","id":1,"method":'
                           '"Addons.SetAddonEnabled","params":'
                           '{"addonid":"inputstream.adaptive",'
                           '"enabled":true}}')
            try:
                xbmc.executeJSONRPC(json_string)
            except RuntimeError:
                log('Failure in enabling inputstream.adaptive')
                xbmcgui.Dialog().ok('Unable to enable inputstream.adaptive',
                                    'Unable to enable inputstream.adaptive, '
                                    'please try to enable manually '
                                    'and try again')
                return False
        addon = xbmcaddon.Addon('inputstream.adaptive')

    if not is_ia_current(addon):
        xbmcgui.Dialog().ok('inputstream.adaptive version lower than '
                            'required', 'inputstream.adaptive version '
                            'does not meet requirements. Please '
                            'update your Kodi installation to a newer '
                            'v18 build and try again')
        log('inputstream.adaptive version lower than required, aborting..')
        return False

    return addon


def is_supported():
    """
    Reads the value of 'supported' global variable and displays a helpful
    message to the user if on an unsupported platform.
    """
    if not supported:
        xbmcgui.Dialog().ok('Platform not supported',
                            '{0} {1} not supported for DRM playback'.format(
                                system_, arch))
        log('{0} {1} not supported for DRM playback'.format(
            system_, arch))
        return False
    return True


def check_inputstream(drm=True):
    """
    Main function call to check all components required are available for
    DRM playback before setting the resolved URL in Kodi.
    drm -- set to false if you just want to check for inputstream.adaptive
        and not widevine components eg. HLS playback
    """
    try:
        ver = get_kodi_version()
        log('Kodi version: {0}'.format(ver))

        if drm:
            if float(ver) < 18.0:
                xbmcgui.Dialog().ok('Kodi 18+ Required',
                                    ('The minimum version of Kodi required '
                                     'for DRM protected content is 18 - '
                                     'please upgrade in order to use this '
                                     'feature.'))
                return False
        else:
            if float(ver) < 17.0:
                xbmcgui.Dialog().ok('Kodi 17+ Required',
                                    ('The minimum version of Kodi required '
                                     'for inputstream.adaptive is 17.0 - '
                                     'please upgrade in order to use this '
                                     'feature.'))
                return False

    except ValueError:  # custom builds of Kodi may not follow same convention
        pass

    date = get_kodi_build()
    if not date:  # can't find build date, assume meets minimum
        log('Could not determine date of build, assuming date meets minimum. '
            'Build string is {0}'
            ''.format(xbmc.getInfoLabel("System.BuildVersion")))
        date = drmconfig.MIN_LEIA_BUILD[0]

    log('Build date: {0}'.format(date))
    log('System: {0}'.format(system_))
    log('Arch: {0}'.format(arch))

    min_date, min_commit = drmconfig.MIN_LEIA_BUILD
    if int(date) < int(min_date) and float(get_kodi_version()) >= 18.0:
        xbmcgui.Dialog().ok('Kodi 18 build is outdated',
                            ('The minimum Kodi 18 build required for DASH/DRM '
                             'support is dated {0} with commit hash {1}. '
                             'Your installation is dated {2}.'
                             'Please update your Kodi installation '
                             'and try again.'.format(
                                min_date, min_commit, date)))
        return False

    if not is_supported() and drm:
        return False

    addon = get_addon()
    if not addon:
        xbmcgui.Dialog().ok('Missing inputstream.adaptive add-on',
                            ('inputstream.adaptive VideoPlayer InputStream '
                             'add-on not found or not enabled. This add-on '
                             'is required to view DRM protected content. '
                             'Please update your Kodi installation to a '
                             'newer v18 build.'))
        return False

    # widevine built into android - not supported on 17 atm though
    if xbmc.getCondVisibility('system.platform.android'):
        log('Running on Android')
        if get_kodi_version()[:2] == '17' and drm:
            xbmcgui.Dialog().ok('Kodi 17 on Android not supported',
                                ('Kodi 17 is not currently supported for '
                                 'Android with encrypted content. Nightly '
                                 'builds of Kodi 18 are available to download '
                                 'from http://mirrors.kodi.tv/nightlies/androi'
                                 'd/arm/master/'))
            log('Kodi 17 Android DRM - not supported')
            return False
        return True

    # No support for iOS
    if xbmc.getCondVisibility('system.platform.ios'):
        log('Running on iOS')
        if drm:
            xbmcgui.Dialog().ok('DRM not supported on iOS devices',
                                'DRM content cannot be played back on '
                                'iOS devices.')
            return False

    # only checking for installation of inputstream.adaptive (eg HLS playback)
    if not drm:
        log('DRM checking not requested')
        return True

    # only 32bit userspace supported for linux aarch64 - no 64bit widevinecdm
    if plat == 'Linux-aarch64':
        if platform.architecture()[0] == '64bit':
            log('Running on Linux aarch64 64bit userspace - not supported')
            xbmcgui.Dialog().ok('64 bit build for aarch64 not supported',
                                ('A build of your OS that supports 32 bit '
                                 'userspace binaries is required for DRM '
                                 'playback. Try CoreELEC for your device.'))

    cdm_path = xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))
    cdm_path2 = xbmc.translatePath('special://xbmc/addons/'
                                   'inputstream.adaptive')
    cdm_path3 = xbmc.translatePath('special://home/addons/'
                                   'inputstream.adaptive')

    if not os.path.isfile(os.path.join(cdm_path, widevinecdm_filename)):
        log('Widevine CDM missing')
        msg1 = 'Missing widevinecdm module required for DRM content'
        msg2 = '{0} not found in {1}'.format(
            drmconfig.WIDEVINECDM_DICT[system_],
            xbmc.translatePath(addon.getSetting('DECRYPTERPATH')))
        msg3 = ('Do you want to attempt downloading the missing widevinecdm '
                'module for your system?')
        if xbmcgui.Dialog().yesno(msg1, msg2, msg3):
            get_widevinecdm(cdm_path)
        else:
            return False

    if not (os.path.isfile(os.path.join(cdm_path, ssd_filename)) or
            os.path.isfile(os.path.join(cdm_path2, ssd_filename)) or
            os.path.isfile(os.path.join(cdm_path2 + '/lib', ssd_filename)) or
            os.path.isfile(os.path.join(cdm_path3, ssd_filename)) or
            os.path.isfile(os.path.join(cdm_path3 + '/lib/', ssd_filename))):
        log('SSD module not found')
        msg1 = 'Missing ssd_wv module required for DRM content'
        msg2 = '{0} not found in {1}, {2}, or {3}'.format(
            drmconfig.SSD_WV_DICT[system_],
            cdm_path,
            cdm_path2,
            cdm_path3)
        msg3 = ('ssd_wv module is supplied with Windows/Mac/LibreELEC, '
                'and can be installed from most package managers in Linux '
                'eg. "sudo apt install kodi-inputstream-adaptive"')
        xbmcgui.Dialog().ok(msg1, msg2, msg3)
        return False

    return True


def unzip_cdm(zpath, cdm_path):
    """
    extract windows widevinecdm.dll from downloaded zip
    """
    cdm_fn = posixpath.join(cdm_path, widevinecdm_filename)
    log('unzipping widevinecdm.dll from {0} to {1}'.format(zpath, cdm_fn))
    with zipfile.ZipFile(zpath) as zf:
        with open(cdm_fn, 'wb') as f:
            data = zf.read('widevinecdm.dll')
            f.write(data)
    os.remove(zpath)


def get_ssd_wv():
    xbmcgui.Dialog().ok('No longer supported',
                        'This feature is no longer supported. Please upgrade '
                        'your Kodi installation to a newer v18 build, or for '
                        'Linux installations you should be able to obtain '
                        'from your package manager eg. '
                        '"sudo apt update && sudo apt install kodi-inputstream'
                        '-adaptive"')
    return False


def get_widevinecdm(cdm_path=None):
    """
    Win/Mac: download Chrome extension blob ~2MB and extract widevinecdm.dll
    Linux: download Chrome package ~50MB and extract libwidevinecdm.so
    Linux arm: download widevine package ~2MB from 3rd party host
    """
    if not cdm_path:
        addon = get_addon()
        if not addon:
            xbmcgui.Dialog().ok('inputstream.adaptive not found',
                                'inputstream.adaptive add-on must be installed'
                                ' before installing widevide_cdm module')
            return
        cdm_path = xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))

    if xbmc.getCondVisibility('system.platform.android'):
        log('Widevinecdm update - not possible on Android')
        xbmcgui.Dialog().ok('Not required for Android',
                            'This module cannot be updated on Android')
        return

    current_cdm_ver = requests.get(drmconfig.CMD_CURRENT_VERSION_URL).text
    url = drmconfig.WIDEVINECDM_URL[plat].format(current_cdm_ver)
    filename = url.split('/')[-1]

    if not os.path.isdir(cdm_path):
        log('Creating directory: {0}'.format(cdm_path))
        os.makedirs(cdm_path)
    cdm_fn = os.path.join(cdm_path, widevinecdm_filename)
    if os.path.isfile(cdm_fn):
        log('Removing existing widevine_cdm: {0}'.format(cdm_fn))
        os.remove(cdm_fn)
    download_path = os.path.join(cdm_path, filename)
    if not progress_download(url, download_path, widevinecdm_filename):
        return

    dp = xbmcgui.DialogProgress()
    dp.create('Extracting {0}'.format(widevinecdm_filename),
              'Extracting {0} from {1}'.format(widevinecdm_filename, filename))
    dp.update(0)

    if system_ == 'Windows':
        unzip_cdm(download_path, cdm_path)
    else:
        command = drmconfig.UNARCHIVE_COMMAND[plat].format(
            quote(filename),
            quote(cdm_path),
            drmconfig.WIDEVINECDM_DICT[system_])
        log('executing command: {0}'.format(command))
        output = os.popen(command).read()
        log('command output: {0}'.format(output))

    dp.close()
    xbmcgui.Dialog().ok('Success', '{0} successfully installed at {1}'.format(
        widevinecdm_filename, os.path.join(cdm_path, widevinecdm_filename)))


def progress_download(url, download_path, display_filename=None):
    """
    Download file in Kodi with progress bar
    """
    log('Downloading {0}'.format(url))
    try:
        res = requests.get(url, stream=True, verify=False)
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        xbmcgui.Dialog().ok('Download failed',
                            'HTTP ' + str(res.status_code) + ' error')
        log('Error retrieving {0}'.format(url))

        return False

    total_length = float(res.headers.get('content-length'))
    dp = xbmcgui.DialogProgress()
    if not display_filename:
        display_filename = download_path.split()[-1]
    dp.create("Downloading {0}".format(display_filename),
              "Downloading File", url)

    with open(download_path, 'wb') as f:
        chunk_size = 1024
        downloaded = 0
        for chunk in res.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            downloaded += len(chunk)
            percent = int(downloaded*100/total_length)
            if dp.iscanceled():
                dp.close()
                res.close()
            dp.update(percent)
    log('Download {0} bytes complete, saved in {1}'.format(
        int(total_length), download_path))
    dp.close()
    return True


def get_ia_direct(update=False, drm=True):
    """
    Download inputstream.adaptive zip file from remote repository and save in
    Kodi's 'home' folder, unzip to addons folder.
    """
    xbmcgui.Dialog().ok('No longer supported',
                        'This feature is no longer supported. Please upgrade '
                        'your Kodi installation to a newer v18 build, or for '
                        'Linux installations you should be able to obtain '
                        'from your package manager eg. '
                        '"sudo apt update && sudo apt install kodi-inputstream'
                        '-adaptive"')
    return False
