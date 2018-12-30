# flake8: noqa

CMD_CURRENT_VERSION_URL = 'https://dl.google.com/widevine-cdm/current.txt'

WIDEVINECDM_URL = {'Linux-x86_64': 'https://dl.google.com/widevine-cdm/{0}-linux-x64.zip',
                   'Linux-arm': 'https://github.com/matthuisman/decryptmodules/raw/master/widevine/4.10.1146.0-linux-armv7.so',
                   'Linux-aarch64': 'https://github.com/matthuisman/decryptmodules/raw/master/widevine/4.10.1146.0-linux-armv7.so',
                   'Windows-x86_64': 'https://dl.google.com/widevine-cdm/{0}-win-x64.zip',
                   'Windows-x86': 'https://dl.google.com/widevine-cdm/{0}-win-ia32.zip',
                   'Darwin-x86_64': 'https://dl.google.com/widevine-cdm/{0}-mac-x64.zip'}

UNARCHIVE_COMMAND = {'Linux-x86_64': '(cd {1} && unzip {0} {2} -d {1} && chmod 755 {1}/{2} && rm -f {0})',
                     'Linux-arm': '(cd {1} && mv {0} {2} && chmod 755 {2})',
                     'Linux-aarch64': '(cd {1} && mv {0} {2} && chmod 755 {2})',
                     'Darwin-x86_64': '(cd {1} && unzip {0} {2} -d {1} && chmod 755 {1}/{2} && rm -f {0})'}

SSD_WV_DICT = {'Windows': 'ssd_wv.dll',
               'Linux': 'libssd_wv.so',
               'Darwin': 'libssd_wv.dylib'}

WIDEVINECDM_DICT = {'Windows': 'widevinecdm.dll',
                    'Linux': 'libwidevinecdm.so',
                    'Darwin': 'libwidevinecdm.dylib'}

ARCH_DICT = {'aarch64': 'aarch64',
             'aarch64_be': 'aarch64',
             'arm64': 'aarch64',
             'arm': 'arm',
             'armv7': 'arm',
             'armv8': 'aarch64',
             'AMD64': 'x86_64',
             'x86_64': 'x86_64',
             'x86': 'x86',
             'i386': 'x86',
             'i686': 'x86'}

SUPPORTED_PLATFORMS = ['Windows-x86_64',
                       'Windows-x86',
                       'Darwin-x86_64',
                       'Darwin-arm',
                       'Darwin-aarch64',
                       'Linux-x86_64',
                       'Linux-arm',
                       'Linux-aarch64',
                       'Android-x86',
                       'Android-arm',
                       'Android-aarch64']
                       
WINDOWS_BITNESS = {'32bit': 'x86',
                   '64bit': 'x86_64'}

REPO_BASE = 'https://github.com/aussieaddons/repo-binary/raw/master/'

KODI_NAME = {'17': 'Krypton', '18': 'Leia'}

MIN_IA_VERSION = {'Krypton': '2.0.7', 'Leia': '2.0.10'}

CURRENT_IA_VERSION = {'Krypton': {'ver': '2.0.19', 'commit': '9af2121'},
                      'Leia': {'ver': '2.0.10', 'commit': '0c7e975'}}

MIN_LEIA_BUILD = ('20170818', 'e6b0c83')
