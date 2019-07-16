# flake8: noqa

DRM_INFO = 'http://aussieaddons.com/drm'

REPO_BASE = 'https://github.com/aussieaddons/repo-binary/raw/master/'

CMD_CURRENT_VERSION_URL = 'https://dl.google.com/widevine-cdm/current.txt'

WIDEVINE_CDM_URL = {
    ('Linux', 'x86_64'): 'https://dl.google.com/widevine-cdm/{0}-linux-x64.zip',
    ('Linux', 'arm'): 'https://k.mjh.nz/.decryptmodules/widevine/1.4.9.1088-linux-armv7.so',
    ('Linux', 'aarch64'): 'https://k.mjh.nz/.decryptmodules/widevine/1.4.9.1088-linux-armv7.so',
    ('Windows', 'x86_64'): 'https://dl.google.com/widevine-cdm/{0}-win-x64.zip',
    ('Windows', 'x86'): 'https://dl.google.com/widevine-cdm/{0}-win-ia32.zip',
    ('Darwin', 'x86_64'): 'https://dl.google.com/widevine-cdm/{0}-mac-x64.zip'
}

UNARCHIVE_COMMAND = {
    ('Linux', 'x86_64'): '(cd {download_folder} && unzip {filename} {wvcdm_filename} -d {cdm_path} && chmod 755 {cdm_path}/{wvcdm_filename} && rm -f {filename})',
    ('Linux','arm'): '(cd {download_folder} && mv {filename} {cdm_path}/{wvcdm_filename} && chmod 755 {cdm_path}/{wvcdm_filename})',
    ('Linux', 'aarch64'): '(cd {download_folder} && mv {filename} {cdm_path}/{wvcdm_filename} && chmod 755 {cdm_path}/{wvcdm_filename})',
    ('Darwin', 'x86_64'): '(cd {download_folder} && unzip {filename} {wvcdm_filename} -d {cdm_path} && chmod 755 {cdm_path}/{wvcdm_filename} && rm -f {filename})',
}

CDM_PATHS = [
    "xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))",
    "xbmc.translatePath('special://xbmcbinaddons/inputstream.adaptive')"
]

DEFAULT_CDM_PATH = 'special://home/cdm'

SSD_WV_DICT = {
    'Android': None,
    'Windows': 'ssd_wv.dll',
    'Linux': 'libssd_wv.so',
    'Darwin': 'libssd_wv.dylib'
}

WIDEVINE_CDM_DICT = {
    'Android': None,
    'Windows': 'widevinecdm.dll',
    'Linux': 'libwidevinecdm.so',
    'Darwin': 'libwidevinecdm.dylib'
}

### Not used??
ARCH_DICT = {
    'aarch64': 'aarch64',
    'aarch64_be': 'aarch64',
    'arm64': 'aarch64',
    'arm': 'arm',
    'armv7': 'arm',
    'armv8': 'aarch64',
    'AMD64': 'x86_64',
    'x86_64': 'x86_64',
    'x86': 'x86',
    'i386': 'x86',
    'i686': 'x86'
}

SUPPORTED_WV_DRM_PLATFORMS = [
    ('Windows', 'x86_64'),
    ('Windows', 'x86'),
    ('Darwin', 'x86_64'),
    ('Linux', 'x86_64'),
    ('Linux', 'arm'),
    ('Linux', 'aarch64'),
    ('Android', 'x86'),
    ('Android', 'arm'),
    ('Android', 'aarch64')
]

WINDOWS_BITNESS = {
    '32bit': 'x86',
    '64bit': 'x86_64'
}

KODI_NAME = {
    12: 'Frodo',
    13: 'Gotham',
    14: 'Helix',
    15: 'Isengard',
    16: 'Jarvis',
    17: 'Krypton',
    18: 'Leia',
    19: 'Matrix'
}