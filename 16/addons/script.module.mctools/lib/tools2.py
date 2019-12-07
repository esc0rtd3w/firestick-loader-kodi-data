# coding: utf-8
import os
import re
import urllib2
from ast import literal_eval
from cookielib import LWPCookieJar
from json import loads
from os import path
from time import sleep
from urllib import quote_plus
from urllib import urlencode

import bs4
import requests
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


# library to access URL, translation title and filtering
# using the great jobs of ElDorado for scrobbling
__author__ = 'mancuniancol'


################################
#### SCRAPER TITLES ############
################################
def normalize(name, onlyDecode=False):
    from unicodedata import normalize
    import types
    if type(name) == types.StringType:
        unicode_name = name.decode('unicode-escape')
    else:
        try:
            unicode_name = name.encode('latin-1').decode('utf-8')  # to latin-1
        except:
            unicode_name = name
    normalize_name = unicode_name if onlyDecode else normalize('NFKD', unicode_name)
    return normalize_name.encode('ascii', 'ignore')


def uncodeName(name):  # Convert all the &# codes to char, remove extra-space and normalize
    from HTMLParser import HTMLParser
    name = name.replace('<![CDATA[', '').replace(']]', '')
    name = HTMLParser().unescape(name)
    return name


def unquoteName(name):  # Convert all %symbols to char
    from urllib import unquote
    return unquote(name).decode("utf-8")


def safeName(value):  # Make the name directory and filename safe
    value = normalize(value)  # First normalization
    value = unquoteName(value)
    value = uncodeName(value)
    value = normalize(value)  # Last normalization, because some unicode char could appear from the previous steps
    value = value.lower().title().replace('_', ' ')
    # erase keyword
    value = re.sub('^\[.*?\]', '', value)  # erase [HorribleSub] for ex.
    # check for anime
    value = re.sub('- ([0-9][0-9][0-9][0-9]) ', ' \g<1>', value + " ")
    value = re.sub('- ([0-9]+) ', '- EP\g<1>', value + " ")
    if 'season' not in value.lower():
        value = value.lower().replace(" episode ", " - EP")
    # check for qualities
    value = value.replace("1920x1080", "1080p")
    value = value.replace("1280x720", "720p")
    value = value.replace("853x480", "480p")
    value = value.replace("848x480", "480p")
    value = value.replace("704x480", "480p")
    value = value.replace("640x480", "480p")
    value = value.replace("microhd", " microhd")  # sometimes comes with the year
    value = value.replace("dvdrip", " dvdrip")  # sometimes comes with the year
    keys = {'"': ' ', '*': ' ', '/': ' ', ':': ' ', '<': ' ', '>': ' ', '?': ' ', '|': ' ', '~': ' ',
            "'": '', 'Of': 'of', 'De': 'de', '.': ' ', ')': ' ', '(': ' ', '[': ' ', ']': ' ', '-': ' '}
    for key in keys.keys():
        value = value.replace(key, keys[key])
    value = ' '.join(value.split())
    return value.replace('s h i e l d', 'SHIELD').replace('c s i', 'CSI')


def checkQuality(text=""):
    # quality
    keyWords = {"Cam": ["camrip", "cam"],
                "Telesync": ["ts", "telesync", "pdvd"],
                "Workprint": ["wp", "workprint"],
                "Telecine": ["tc", "telecine"],
                "Pay-Per-View Rip": ["ppv", "ppvrip"],
                "Screener": ["scr", "screener", "screeener", "dvdscr", "dvdscreener", "bdscr"],
                "DDC": ["ddc"],
                "R5": ["r5", "r5.line", "r5 ac3 5 1 hq"],
                "DVD-Rip": ["dvdrip", "dvd-rip"],
                "DVD-R": ["dvdr", "dvd-full", "full-rip", "iso rip", "lossless rip", "untouched rip", "dvd-5 dvd-9"],
                "HDTV": ["dsr", "dsrip", "dthrip", "dvbrip", "hdtv", "pdtv", "tvrip", "hdtvrip", "hdrip", "hdit",
                         "high definition"],
                "VODRip": ["vodrip", "vodr"],
                "WEB-DL": ["webdl", "web dl", "web-dl"],
                "WEBRip": ["web-rip", "webrip", "web rip"],
                "WEBCap": ["web-cap", "webcap", "web cap"],
                "BD/BRRip": ["bdrip", "brrip", "blu-ray", "bluray", "bdr", "bd5", "bd", "blurip"],
                "MicroHD": ["microhd"],
                "FullHD": ["fullhd"],
                "BR-Line": ["br line"],
                # video formats
                "x264": ["x264", "x 264"],
                "x265 HEVC": ["x265 hevc", "x265", "x 265", "hevc"],
                # audio
                "DD5.1": ["dd5 1", "dd51", "dual audio 5"],
                "AC3 5.1": ["ac3"],
                "ACC": ["acc"],
                "DUAL AUDIO": ["dual", "dual audio"],
                }
    color = {"Cam": "FFF4AE00",
             "Telesync": "FFF4AE00",
             "Workprint": "FFF4AE00",
             "Telecine": "FFF4AE00",
             "Pay-Per-View Rip": "FFD35400",
             "Screener": "FFD35400",
             "DDC": "FFD35400",
             "R5": "FFD35400",
             "DVD-Rip": "FFD35400",
             "DVD-R": "FFD35400",
             "HDTV": "FFD35400",
             "VODRip": "FFD35400",
             "WEB-DL": "FFD35400",
             "WEBRip": "FFD35400",
             "WEBCap": "FFD35400",
             "BD/BRRip": "FFD35400",
             "MicroHD": "FFD35400",
             "FullHD": "FFD35400",
             "BR-Line": "FFD35400",
             # video formats
             "x264": "FFFB0C06",
             "x265 HEVC": "FFFB0C06",
             # audio
             "DD5.1": "FF089DE3",
             "AC3 5.1": "FF089DE3",
             "ACC": "FF089DE3",
             "DUAL AUDIO": "FF089DE3",
             }
    quality = "480p"
    textQuality = ""
    for key in keyWords:
        for keyWord in keyWords[key]:
            if ' ' + keyWord + ' ' in ' ' + text + ' ':
                quality = "480p"
                textQuality += " [COLOR %s][%s][/COLOR]" % (color[key], key)

    if "480p" in text:
        quality = "480p"
        textQuality += " [COLOR FF2980B9][480p][/COLOR]"
    if "720p" in text:
        quality = "720p"
        textQuality += " [COLOR FF5CD102][720p][/COLOR]"
    if "1080p" in text:
        quality = "1080p"
        textQuality += " [COLOR FFF4AE00][1080p][/COLOR]"
    if "3d" in text:
        quality = "1080p"
        textQuality += " [COLOR FFD61515][3D][/COLOR]"
    if "4k" in text:
        quality = "2160p"
        textQuality += " [COLOR FF16A085][4K][/COLOR]"
    return quality, textQuality


def width(quality="480p"):
    result = 720
    if '480p' in quality:
        result = 720
    elif '720p' in quality:
        result = 1280
    elif '1080p' in quality:
        result = 1920
    elif '2160p' in quality:
        result = 2160
    return result


def height(quality="480p"):
    result = 480
    if '480p' in quality:
        result = 480
    elif '720p' in quality:
        result = 720
    elif '1080p' in quality:
        result = 1080
    elif '2160p' in quality:
        result = 3840
    return result


def findLanguage(value=""):
    language = ""  # It is english or unknown
    if "spa" in value or "spanish" in value or "espanol" in value:
        language = "[Español]"
    if "hindi" in value:
        language = "[Hindi]"
    if "castellano" in value:
        language = "[Castellano]"
    if "french" in value or 'francais' in value:
        language = "[French]"
    if "german" in value:
        language = "[German]"
    return language


def exceptionsTitle(title=""):
    value = title + " "
    if "csi " in value and "ny" not in value and "miami" not in value and "cyber" not in value:
        title = title.replace("csi", "CSI Crime Scene Investigation")
    if "juego de tronos" in value:
        title = title.replace("juego de tronos", "Game of Thrones")
    if "mentes criminales" in value:
        title = title.replace("mentes criminales", "criminal minds")
    if "les revenants" in value:
        title = title.replace("les revenants", "The returned")
    return title


def _cleanTitle(value=''):
    keywordsCleanTitle = ['version', 'extendida', 'extended', 'edition', 'hd', 'unrated', 'version', 'vose',
                          'special', 'edtion', 'uncensored', 'fixed', 'censurada', 'episode', 'ova', 'complete',
                          'swesub'
                          ]
    for keyword in keywordsCleanTitle:  # checking keywords
        value = (value + ' ').replace(' ' + keyword.title() + ' ', ' ')
    return value.strip()


def formatTitle(value='', fileName='', typeVideo="MOVIE"):
    if fileName.startswith('magnet'):
        fileName = ''
    if fileName == '':
        fileName = value
    pos = value.rfind("/")
    value = value if pos < 0 else value[pos:]
    temp_info = re.search("<(.*?)>", value)
    information = ""
    if temp_info:
        information = "[%s] " % temp_info.group(1)
    value = safeName(value).lower() + ' '
    fileName = safeName(fileName).lower() + ' '
    quality, textQuality = checkQuality(value + ' ' + fileName)  # find quality
    language = findLanguage(value)  # find language
    formats = [' ep[0-9]+', ' s[0-9]+e[0-9]+', ' s[0-9]+ e[0-9]+', ' [0-9]+x[0-9]+',
               ' [0-9][0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]',
               ' [0-9][0-9] [0-9][0-9] [0-9][0-9]', ' season [0-9]+ episode [0-9]+',
               ' season [0-9]+', ' season[0-9]+', ' s[0-9][0-9]',
               ' temporada [0-9]+ capitulo [0-9]+', ' temporada[0-9]+', ' temporada [0-9]+',
               ' seizoen [0-9]+ afl [0-9]+', ' saison[0-9]+', ' saison [0-9]+',
               ' temp [0-9]+ cap [0-9]+', ' temp[0-9]+ cap[0-9]+',
               ]
    keywords = ['en 1080p', 'en 720p', 'en dvd', 'en dvdrip', 'en hdtv', 'en bluray', 'en blurayrip',
                'en web', 'en rip', 'en ts screener', 'en screener', 'en cam', 'en camrip', 'pcdvd', 'bdremux',
                'en ts-screener', 'en hdrip', 'en microhd', '1080p', '720p', 'dvd', 'dvdrip', 'hdtv', 'bluray',
                'blurayrip', 'web', 'rip', 'ts screener', 'screener', 'cam', 'camrip', 'ts-screener', 'hdrip',
                'brrip', 'blu', 'webrip', 'hdrip', 'bdrip', 'microhd', 'ita', 'eng', 'esp', "spanish espanol",
                'castellano', '480p', 'bd', 'bdrip', 'hi10p', 'sub', 'x264', 'sbs', '3d', 'br', 'hdts', 'dts',
                'dual audio', 'hevc', 'aac', 'batch', 'h264', 'gratis', 'descargar', 'hd', 'html', 'hdit',
                'blurip', 'high definition', 'german', 'french', 'truefrench', 'vostfr', 'dvdscr', 'swesub',
                '4k', 'uhd',
                ]
    sshow = None
    for format in formats:  # search if it is a show
        sshow = re.search(format, value)  # format shows
        if sshow is not None:
            break
    if sshow is None and typeVideo != "MOVIE":
        if typeVideo == 'SHOW':
            value += ' s00e00'
        if typeVideo == 'ANIME':
            value += ' ep00'
        for format in formats:  # search if it is a show
            sshow = re.search(format, value)  # format shows
            if sshow is not None:
                break
    if sshow is None:
        # it is a movie
        value += ' 0000 '  # checking year
        syear = re.search(' [0-9][0-9][0-9][0-9] ', value)
        year = syear.group(0).strip()
        pos = value.find(year)
        if pos > 0:
            title = value[:pos].strip()
            rest = value[pos + 5:].strip().replace('0000', '')
        else:
            title = value.replace('0000', '')
            rest = ''

        while pos != -1:  # loop until doesn't have any keyword in the title
            value = title + ' '
            for keyword in keywords:  # checking keywords
                pos = value.find(' ' + keyword + ' ')
                if pos > 0:
                    title = value[:pos]
                    rest = value[pos:].strip() + ' ' + rest
                    break

        title = title.title().strip().replace('Of ', 'of ').replace('De ', 'de ')
        cleanTitle = _cleanTitle(title)
        # finishing cleanTitle
        if '0000' not in year:
            title += ' (' + year.strip() + ')'
        year = year.replace('0000', '')
        folder = title
        result = {'title': title, 'folder': folder, 'rest': rest.strip(), 'type': 'MOVIE', 'cleanTitle': cleanTitle,
                  'year': year, 'quality': quality, 'textQuality': textQuality, 'height': height(quality),
                  "width": width(quality), 'language': language, 'folderPath': settings.movieFolder,
                  'information': information
                  }
        return result
    else:
        # it is a show
        rest = value.strip()  # original name
        seasonEpisode = sshow.group(0)
        # clean title
        for keyword in keywords:  # checking keywords
            value = value.replace(' ' + keyword + ' ', ' ')
        title = value[:value.find(seasonEpisode)].strip()
        title = title.strip()
        seasonEpisode = seasonEpisode.replace('temporada ', 's').replace(' capitulo ', 'e')
        seasonEpisode = seasonEpisode.replace('season ', 's').replace(' episode ', 'e')
        seasonEpisode = seasonEpisode.replace('temp ', 's').replace(' cap ', 'e')
        seasonEpisode = seasonEpisode.replace('seizoen ', 's').replace(' afl ', 'e')

        if 'x' in seasonEpisode:
            seasonEpisode = 's' + seasonEpisode.replace('x', 'e')

        if 's' in seasonEpisode and 'e' in seasonEpisode and 'season' not in seasonEpisode:  # force S00E00 instead S0E0
            temp_episode = seasonEpisode.replace('s', '').split('e')
            seasonEpisode = 's%02de%02d' % (int(temp_episode[0]), int(temp_episode[1]))

        if 's' not in seasonEpisode and 'e' not in seasonEpisode:  # date format
            date = seasonEpisode.split()
            if len(date[0]) == 4:  # yyyy-mm-dd format
                seasonEpisode = seasonEpisode.replace(' ', '-')  # date style episode talk shows
            else:  # dd mm yy format
                if int(date[2]) > 50:
                    date[2] = '19' + date[2]
                else:
                    date[2] = '20' + date[2]
                seasonEpisode = date[2] + '-' + date[1] + '-' + date[0]

        seasonEpisode = seasonEpisode.replace(' ', '')  # remove spaces in the episode format
        title = exceptionsTitle(title)
        # finding year
        value = title + ' 0000 '
        syear = re.search(' [0-9][0-9][0-9][0-9] ', value)
        year = syear.group(0).strip()
        pos = value.find(year)
        if pos > 0:
            title = value[:pos].strip()
        title = value.replace('0000', '')
        year = year.replace('0000', '')
        # the rest
        title = title.title().strip().replace('Of ', 'of ').replace('De ', 'de ')
        folder = title  # with year
        cleanTitle = _cleanTitle(title.replace(year, '').strip())  # without year
        title = folder + ' ' + seasonEpisode.upper()
        title = title.replace('S00E00', '').replace('EP00', '')
        ttype = "SHOW"
        result = {'title': title, 'folder': folder, 'rest': rest, 'type': ttype, 'cleanTitle': cleanTitle,
                  'year': year, 'quality': quality, 'textQuality': textQuality, 'height': height(quality),
                  "width": width(quality), "language": language, 'folderPath': settings.showFolder,
                  'information': information
                  }
        if bool(re.search("EP[0-9]+", title)):
            result['type'] = "ANIME"
            result['folderPath'] = settings.animeFolder
            result['season'] = 1
            result['episode'] = int(seasonEpisode.replace('ep', ''))
        else:
            temp = (seasonEpisode.replace('s', '')).split('e')
            result['season'] = 0
            result['episode'] = 0
            try:
                result['season'] = int(temp[0])
                result['episode'] = int(temp[1])
            except:
                pass
        return result


class UnTaggle():
    infoTitle = {}
    infoLabels = {}
    infoStream = {}
    title = ""
    fileName = ""
    typeVideo = ""
    label = ""
    id = ""
    info = {}
    cover = ""
    fanart = ""
    season = ""
    episode = ""
    imdb_id = ""
    titleEpisode = ""

    def __init__(self, value='', fileName='', typeVideo="MOVIE", useUrl=True):
        self.title = normalize(value)
        self.fileName = fileName
        if useUrl:
            self.infoTitle = formatTitle(value, fileName, typeVideo)  # organize the title information
        else:
            self.infoTitle = formatTitle(value, '', typeVideo)  # organize the title information
        self.typeVideo = self.infoTitle["type"]
        if settings.value["infoLabels"] == "true":
            self.infoLabels = getInfoLabels(self.infoTitle)  # using script.module.metahandlers to the the infoLabels
            self.infoStream = getInfoStream(self.infoTitle, self.infoLabels)
        settings.debug(self.infoTitle)
        settings.debug(self.infoLabels)
        settings.debug(self.infoStream)
        self.info = self.infoLabels
        self.label = self.infoTitle["title"] + " " + self.infoTitle.get("textQuality", "") + self.infoTitle[
            "language"] + self.infoTitle.get("information", "")
        self.id = self.infoLabels.get("imdb_id", "")
        self.imdb_id = self.id
        if self.infoTitle["type"] == 'SHOW' and settings.value[
            "infoLabels"] == "true":  # difference with show and anime
            self.info = getInfoEpisode(self.infoLabels)
            self.id = self.infoLabels.get("tvdb_id", "")
            self.titleEpisode = ' - ' + normalize(self.info.get('title', "")) if self.info.get('title',
                                                                                               "") != "" else ""
            self.label += self.titleEpisode
            self.season = self.infoTitle.get("season", "")
            self.episode = self.infoTitle.get("episode", "")
        self.cover = self.info.get('cover_url', settings.icon)
        self.fanart = self.info.get("backdrop_url", settings.fanart)


################################
#### CLASS #####################
################################
class Storage:
    def __init__(self, fileName="", type="list", eval=False):
        from ast import literal_eval
        self.path = os.path.join(xbmc.translatePath('special://temp'), fileName)
        self.type = type
        if type == "list":
            # get the list
            self.database = []
            try:
                with open(self.path, 'r') as fp:
                    for line in fp:
                        self.database.append(line.strip())
            except:
                pass
        elif type == "dict":
            # get the Dictionary
            self.database = {}
            try:
                with open(self.path, 'r') as fp:
                    for line in fp:
                        listedline = line.strip().split('::')  # split around the :: sign
                        if len(listedline) > 1:  # we have the : sign in there
                            settings.debug(listedline[0] + ' : ' + listedline[1])
                            self.database[listedline[0]] = listedline[1] if not eval else literal_eval(listedline[1])
            except:
                pass

    def destroy(self):  # Erase the database from the HD
        try:
            os.remove(self.path)
        except OSError:
            pass

    def add(self, key="", info="", safe=True):  # add element
        if self.type == "list" and key not in self.database:
            self.database.append(key)
        elif self.type == "dict":
            if safe:
                keySafe = formatTitle(key)
                self.database[keySafe['folder']] = info
            else:
                self.database[key] = info

    def remove(self, key="", safe=True):  # remove element
        if self.type == "list":
            self.database.remove(key)
        elif self.type == "dict":
            if safe:
                keySafe = formatTitle(key)
                del self.database[keySafe['folder']]
            else:
                del self.database[key]

    def save(self):  # save the database
        if self.type == "list":
            # save the list
            with open(self.path, 'w') as fp:
                for p in self.database:
                    fp.write("%s\n" % p)
        elif self.type == "dict":
            # save the dictionary
            with open(self.path, 'w') as fp:
                for p in self.database.items():
                    fp.write("%s::%s\n" % p)


class Settings:  # Read Configuration's Addon
    def __init__(self, anime=False):
        # Objects
        self.dialog = xbmcgui.Dialog()
        self.pDialog = xbmcgui.DialogProgress()
        self.settings = xbmcaddon.Addon()

        # General information
        self.idAddon = self.settings.getAddonInfo('ID')  # gets name
        self.icon = self.settings.getAddonInfo('icon')
        self.fanart = self.settings.getAddonInfo('fanart')
        self.path = self.settings.getAddonInfo('path')
        self.name = self.settings.getAddonInfo('name')  # gets name
        self.cleanName = re.sub('.COLOR (.*?)]', '', self.name.replace('[/COLOR]', ''))
        self.storageName = self.cleanName + ".txt"  # Name Database

        # Everything else
        self.value = {}  # it contains all the settings from xml file
        self.value["movieFolder"] = ""
        self.value["showFolder"] = ""
        self.value["animeFolder"] = ""

        with open(path.join(self.path, "resources", "settings.xml"), 'r') as fp:
            data = fp.read()
        soup = bs4.BeautifulSoup(data)
        settings = soup.select("setting")
        for setting in settings:
            id = setting.attrs.get("id")
            if id is not None:
                self.value[id] = self.settings.getSetting(id)

        # Set-up Output folder
        self.movieFolder = self.__folder__(self.value["movieFolder"], "movies")
        self.showFolder = self.__folder__(self.value["showFolder"], "shows")
        self.animeFolder = self.__folder__(self.value["animeFolder"], "animes")

        # subscription
        if "subscription" in self.cleanName.lower(): self.__subscription__()

    def __folder__(self, folder, default=""):  # Change to OS friendly names
        if folder == '':  # define default folder
            folder = 'special://temp/%s/' % default
        folder = folder.replace('special://temp/', xbmc.translatePath('special://temp'))
        return folder.replace('smb:', '')  # network compatibility

    def __subscription__(self):  # Additional Code for Subscription List Scripts
        # remove .strm
        self.debug("removeStrm= " + self.value["removeStrm"])
        if self.value["removeStrm"] == 'true':
            self.notification('Removing .strm files...')
            if self.value["typeLibrary"] == "Global":
                self.storageName = "quasar global subscription.txt"
            storage = Storage(self.storageName, type="dict")
            from shutil import rmtree
            for item in storage.database:
                data = literal_eval(storage.database[item])
                rmtree(data['path'])
                settings.log('path: ' + data['path'] + ' removed!!')
            self.log('All .strm files removed!')
            self.notification('All .strm files removed!', force=True)
            self.settings.setSetting('removeStrm', 'false')
        # clear the database
        self.debug("clearDatabase= " + self.value["clearDatabase"])
        if self.value["clearDatabase"] == 'true':
            self.notification('Erasing Database...', force=True)
            storage = Storage(self.storageName, type="dict")
            storage.destroy()
            self.settings.setSetting('clearDatabase', 'false')

    def log(self, message="", level=xbmc.LOGNOTICE):  # to write in the Kodi's log
        try:
            if message is not str:
                message = str(message)
            try:
                xbmc.log('[' + self.cleanName + '] ' + message, level=level)
            except:
                xbmc.log('[' + self.cleanName + '] ' + safeName(message), level=level)
        except:
            xbmc.log("Error with the message", level=xbmc.LOGERROR)

    def debug(self, message=""):  # to write in the Kodi's log
        self.log(message, xbmc.LOGDEBUG)

    def notification(self, message="", force=False, time=1000):  # to display a message in Kodi
        if float(self.value["timeNotification"]) > 0 or force:
            xbmcgui.Dialog().notification(self.name, "%s" % message, self.icon,
                                          time if force else int(float(self.value["timeNotification"]) * 1000))

    def string(self, id):
        return self.settings.getLocalizedString(id)


#############################################
##############Browser HTTPS support##########
#############################################

class Response:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = int(status_code)


# provider web browser with cookies management
class Browser:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36" \
                 " (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36"
    _cookies = None
    cookies = LWPCookieJar()
    content = None
    status = None
    headers = ""

    def __init__(self):
        pass

    @classmethod
    def create_cookies(cls, payload):

        cls._cookies = urlencode(payload)

    # to open any web page
    @classmethod
    def open(cls, url='', language='en', post_data=None, get_data=None):
        if post_data is None:
            post_data = {}
        if get_data is not None:
            url += '?' + urlencode(get_data)
        print(url)
        result = True
        if len(post_data) > 0:
            cls.create_cookies(post_data)
        if cls._cookies is not None:
            req = urllib2.Request(url, cls._cookies)
            cls._cookies = None
        else:
            req = urllib2.Request(url)
        req.add_header('User-Agent', cls.USER_AGENT)
        req.add_header('Content-Language', language)
        req.add_header("Accept-Encoding", "gzip")
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cls.cookies))  # open cookie jar
        try:
            response = opener.open(req)  # send cookies and open url
            cls.headers = response.headers
            # borrow from provider.py Steeve
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib
                cls.content = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(response.read())
            else:
                cls.content = response.read()
            response.close()
            cls.status = 200
        except urllib2.HTTPError as e:
            cls.status = e.code
            result = False
            if e.code == 503:
                # trying to open with antibots tool
                import cfscrape
                scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
                cls.content = scraper.get(url).content
                cls.status = 200
                result = True
        except urllib2.URLError as e:
            cls.status = e.reason
            result = False
        xbmc.log("Status: %s" % cls.status)
        xbmc.log(cls.content, level=xbmc.LOGDEBUG)
        return result

    # alternative when it is problem with https
    @classmethod
    def open2(cls, url=''):
        import httplib

        word = url.split("://")
        pos = word[1].find("/")
        conn = httplib.HTTPConnection(re.search[:pos])
        conn.request("GET", re.search[pos:])
        r1 = conn.getresponse()
        cls.status = str(r1.status) + " " + r1.reason
        cls.content = r1.read()
        if r1.status == 200:
            return True
        else:
            return False

    # used for sites with login
    @classmethod
    def login(cls, url, payload, word):
        result = False
        cls.create_cookies(payload)
        if cls.open(url):
            result = True
            data = cls.content
            if word in data:
                cls.status = 'Wrong Username or Password'
                result = False
        return result

    def json(self):
        return loads(self.content)


# Create settings object and browser to be used in the other tool's functions
settings = Settings()
browser = requests.Session()
browser2 = Browser()
browser.headers[
    'User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
browser.headers['Accept-Language'] = 'en'


class TextViewer_Dialog(xbmcgui.WindowXMLDialog):  # taking from script.toolbox
    ACTION_PREVIOUS_MENU = [9, 92, 10]

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)

        self.text = kwargs.get('text')
        self.header = kwargs.get('header')

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.text)

    def onAction(self, action):
        if action in self.ACTION_PREVIOUS_MENU:
            self.close()

    def onClick(self, controlID):
        pass

    def onFocus(self, controlID):
        pass


class Filtering:
    def __init__(self):
        self.reason = ''
        self.title = ''
        self.quality_allow = ['*']
        self.quality_deny = []
        self.title = ''
        self.maxSize = 10.00  # 10 it is not limit
        self.minSize = 0.00

        # size
        if settings.value.has_key('movieMinSize'):  # there is size restrictions
            settings.value['movieMinSize'] = float(settings.value['movieMinSize'])
        else:
            settings.value['movieMinSize'] = 0.0
        self.movieMinSize = settings.value['movieMinSize']

        if settings.value.has_key('movieMaxSize'):  # there is size restrictions
            settings.value['movieMaxSize'] = float(settings.value['movieMaxSize'])
        else:
            settings.value['movieMaxSize'] = 10.0
        self.movieMaxSize = settings.value['movieMaxSize']

        if settings.value.has_key('tvMinSize'):  # there is size restrictions
            settings.value['tvMinSize'] = float(settings.value['movieMinSize'])
        else:
            settings.value['tvMinSize'] = 0.0
        self.tvMinSize = settings.value['tvMinSize']

        if settings.value.has_key('tvMaxSize'):  # there is size restrictions
            settings.value['tvMaxSize'] = float(settings.value['movieMaxSize'])
        else:
            settings.value['tvMaxSize'] = 10.0
        self.tvMaxSize = settings.value['tvMaxSize']

        # movie
        movieAllow = []
        if settings.value.has_key('movieKeyAllow') and settings.value['movieKeyAllow'] <> "":
            movieAllow = re.split(',', settings.value['movieKeyAllow'].replace(', ', ',').replace(' ,', ','))
        if settings.value.has_key('movieQua1') and settings.value['movieQua1'] == 'Accept File':
            movieAllow.append('480p')  # 480p
        if settings.value.has_key('movieQua2') and settings.value['movieQua2'] == 'Accept File':
            movieAllow.append('HDTV')  # HDTV
        if settings.value.has_key('movieQua3') and settings.value['movieQua3'] == 'Accept File':
            movieAllow.append('720p')  # 720p
        if settings.value.has_key('movieQua4') and settings.value['movieQua4'] == 'Accept File':
            movieAllow.append('1080p')  # 1080p
        if settings.value.has_key('movieQua5') and settings.value['movieQua5'] == 'Accept File':
            movieAllow.append('3D')  # 3D
        if settings.value.has_key('movieQua6') and settings.value['movieQua6'] == 'Accept File':
            movieAllow.append('CAM')  # CAM
        if settings.value.has_key('movieQua7') and settings.value['movieQua7'] == 'Accept File':
            movieAllow.extend(['TeleSync', ' TS '])  # TeleSync
        if settings.value.has_key('movieQua8') and settings.value['movieQua8'] == 'Accept File':
            movieAllow.append('Trailer')  # Trailer

        # Block File
        movieDeny = []
        if settings.value.has_key('movieKeyDenied') and settings.value['movieKeyDenied'] <> "":
            movieDeny = re.split(',', settings.value['movieKeyDenied'].replace(', ', ',').replace(' ,', ','))
        if settings.value.has_key('movieQua1') and settings.value['movieQua1'] == 'Block File':
            movieDeny.append('480p')  # 480p
        if settings.value.has_key('movieQua2') and settings.value['movieQua2'] == 'Block File':
            movieDeny.append('HDTV')  # HDTV
        if settings.value.has_key('movieQua3') and settings.value['movieQua3'] == 'Block File':
            movieDeny.append('720p')  # 720p
        if settings.value.has_key('movieQua4') and settings.value['movieQua4'] == 'Block File':
            movieDeny.append('1080p')  # 1080p
        if settings.value.has_key('movieQua5') and settings.value['movieQua5'] == 'Block File':
            movieDeny.append('3D')  # 3D
        if settings.value.has_key('movieQua6') and settings.value['movieQua6'] == 'Block File':
            movieDeny.append('CAM')  # CAM
        if settings.value.has_key('movieQua7') and settings.value['movieQua7'] == 'Block File':
            movieDeny.extend(['TeleSync', ' TS '])  # TeleSync
        if settings.value.has_key('movieQua8') and settings.value['movieQua8'] == 'Block File':
            movieDeny.append('Trailer')  # Trailer

        if '' in movieAllow: movieAllow.remove('')
        if '' in movieDeny: movieDeny.remove('')
        if len(movieAllow) == 0: movieAllow = ['*']
        self.movieAllow = movieAllow
        self.movieDeny = movieDeny

        # TV
        tvAllow = []
        if settings.value.has_key('tvKeyAllow'):
            tvAllow.append(re.split(',', settings.value['tvKeyAllow'].replace(', ', ',').replace(' ,', ',')))
        if settings.value.has_key('tvQua1') and settings.value['tvQua1'] == 'Accept File':
            tvAllow.append('480p')  # 480p
        if settings.value.has_key('tvQua2') and settings.value['tvQua2'] == 'Accept File':
            tvAllow.append('HDTV')  # HDTV
        if settings.value.has_key('tvQua3') and settings.value['tvQua3'] == 'Accept File':
            tvAllow.append('720p')  # 720p
        if settings.value.has_key('tvQua4') and settings.value['tvQua4'] == 'Accept File':
            tvAllow.append('1080p')  # 1080p

        # Block File
        tvDeny = []
        if settings.value.has_key('tvKeyDeny'):
            tvDeny.append(re.split(',', settings.value['tvKeyDeny'].replace(', ', ',').replace(' ,', ',')))
        if settings.value.has_key('tvQua1') and settings.value['tvQua1'] == 'Block File':
            tvDeny.append('480p')  # 480p
        if settings.value.has_key('tvQua2') and settings.value['tvQua2'] == 'Block File':
            tvDeny.append('HDTV')  # HDTV
        if settings.value.has_key('tvQua3') and settings.value['tvQua3'] == 'Block File':
            tvDeny.append('720p')  # 720p
        if settings.value.has_key('tvQua4') and settings.value['tvQua4'] == 'Block File':
            tvDeny.append('1080p')  # 1080p

        if '' in tvAllow: tvAllow.remove('')
        if '' in tvDeny: tvDeny.remove('')
        if len(tvAllow) == 0: tvAllow = ['*']
        self.tvAllow = tvAllow
        self.tvDeny = tvDeny

    def useMovie(self):
        self.qualityAllow = self.movieAllow
        self.qualityDeny = self.movieDeny
        self.minSize = self.movieMinSize
        self.maxSize = self.movieMaxSize

    def useTv(self):
        self.qualityAllow = self.tvAllow
        self.qualityDeny = self.tvDeny
        self.minSize = self.tvMinSize
        self.maxSize = self.tvMaxSize

    def information(self):
        settings.log('Accepted Keywords: %s' % str(self.qualityAllow))
        settings.log('Blocked Keywords: %s' % str(self.qualityDeny))
        settings.log('min Size: %s' % str(self.minSize) + ' GB')
        settings.log('max Size: %s' % str(self.maxSize) + ' GB') if self.maxSize != 10 else 'MAX'

    # validate keywords
    def included(self, value, keys, strict=False):
        value = ' ' + normalize(value) + ' '
        res = False
        if '*' in keys:
            res = True
        else:
            res1 = []
            for key in keys:
                res2 = []
                for item in re.split('\s', key):
                    item = normalize(item)
                    item = item.replace('?', ' ')
                    if strict: item = ' ' + item + ' '  # it makes that strict the comparation
                    if item.upper() in value.upper():
                        res2.append(True)
                    else:
                        res2.append(False)
                res1.append(all(res2))
            res = any(res1)
        return res

    # validate size
    def size_clearance(self, size):
        max_size1 = 100 if self.maxSize == 10 else self.maxSize
        res = False
        value = float(re.split('\s', size.replace(',', ''))[0])
        value *= 0.001 if 'M' in size else 1
        if self.minSize <= value <= max_size1:
            res = True
        return res

    # verify
    def verify(self, name, size):  # modify to just check quality and size, not name
        self.reason = name.replace(' - ' + settings.cleanName, '') + ' ***Blocked File by'
        result = True
        if name != None:
            if not self.included(name, self.qualityAllow) or self.included(name, self.qualityDeny):
                self.reason += ", Keyword"
                result = False
        if size != None:
            if not self.size_clearance(size):
                result = False
                self.reason += ", Size"
        self.reason = self.reason.replace('by,', 'by') + '***'
        return result


#######################################
######## CLASS FOR SUBSCRIPTION #######
#######################################
class TvShow():
    def __init__(self, name):
        import urllib

        browser.get('http://localhost:65251/shows/search?q=%s' % urllib.quote(name))
        sleep(1.5)
        response = browser.get('http://localhost:65251/shows/search?q=%s' % urllib.quote(name))
        if response.status_code == requests.codes.ok:
            data = response.json()
            dataShow = None
            if len(data['items']) > 0:  # To find the right Tv Show
                dataShow = data['items'][0]
                for item in data['items']:
                    if item['label'].lower() == name.lower():
                        dataShow = item
                        break
            if dataShow is not None:
                self.code = dataShow['path'].replace('plugin://plugin.video.quasar/show/', '').replace(
                    '/seasons', '')
                sleep(0.5)
                response = browser.get('http://localhost:65251/show/%s/seasons' % self.code)
                data = {}
                try:
                    data = response.json()
                except:
                    data['items'] = []
                seasons = []
                for item in data['items']:
                    seasons.append(int(item['label'].replace('Season ', '').replace('Specials', '0')))
                seasons.sort()
                episodes = {}
                for season in seasons:
                    sleep(0.5)
                    response = browser.get('http://localhost:65251/show/%s/season/%s/episodes' % (self.code, season))
                    data = response.json()
                    episodes[season] = len(data['items'])
                if len(seasons) > 0:
                    self.firstSeason = seasons[0]
                    self.lastSeason = seasons[-1]
                else:
                    self.firstSeason = 0
                    self.lastSeason = 0
                self.lastEpisode = episodes
            else:
                self.code = None
        else:
            self.code = None


class TvShowCode():
    def __init__(self, code, episodes={}, lastSeason=0):
        self.code = code
        response = browser.get('http://localhost:65251/show/%s/seasons' % self.code)
        data = {}
        try:
            data = response.json()
        except:
            data['items'] = []
        seasons = []
        for item in data['items']:
            seasons.append(int(item['label'].replace('Season ', '').replace('Specials', '0')))
        seasons.sort()
        if episodes.has_key(0):
            del episodes[0]
        if lastSeason is not 0:
            del episodes[lastSeason]
        for season in seasons:
            if not episodes.has_key(season):
                sleep(0.5)
                response = browser.get('http://localhost:65251/show/%s/season/%s/episodes' % (self.code, season))
                data = response.json()
                episodes[season] = len(data['items'])
        if len(seasons) > 0:
            self.firstSeason = seasons[0]
            self.lastSeason = seasons[-1]
        else:
            self.firstSeason = 0
            self.lastSeason = 0
        self.lastEpisode = episodes


class Movie():
    def __init__(self, name):
        import urllib

        if ')' in name and '(' in name:
            try:
                yearMovie = int(name[name.find("(") + 1:name.find(")")])
                name = name.replace('(%s)' % yearMovie, '').rstrip()
            except:
                yearMovie = None
        else:
            yearMovie = None
        browser.get('http://localhost:65251/movies/search?q=%s' % urllib.quote(name))  # avoid not info
        sleep(1.5)
        response = browser.get('http://localhost:65251/movies/search?q=%s' % urllib.quote(name))
        if response.status_code == requests.codes.ok:
            data = response.json()
            if len(data['items']) > 0:
                if yearMovie is not None:
                    for movie in data['items']:
                        label = movie['label']
                        path = movie['path']
                        if movie['info'].has_key('year'):
                            year = movie['info']['year']
                        else:
                            year = 0000
                        if year == yearMovie:
                            break
                else:
                    label = data['items'][0]['label']
                    path = data['items'][0]['path']
                    year = data['items'][0]['info']['year']
                self.code = path.replace('plugin://plugin.video.quasar/movie/', '').replace('/play', '')
                self.label = label
                self.year = year
            else:
                self.code = None
                self.label = name
        else:
            self.code = None
            self.label = name


class Magnet():
    def __init__(self, magnet):
        self.magnet = magnet + '&'
        # hash
        hash = re.search('urn:btih:(.*?)&', self.magnet)
        result = ''
        if hash is not None:
            result = hash.group(1)
        self.hash = result
        # name
        name = re.search('dn=(.*?)&', self.magnet)
        result = ''
        if name is not None:
            result = name.group(1).replace('+', ' ')
        self.name = safeName(result)
        # trackers
        self.trackers = re.findall('tr=(.*?)&', self.magnet)


################################
#### FUNCTIONS #################
################################
def printer(message=""):
    print '****************************'
    print message
    print '*-**************************'


def find_nth(string="", substring="", nth=1, start=0):
    start = string.find(substring, start)
    if nth == 1 or start == -1:
        return start
    else:
        return find_nth(string, substring, nth - 1, start + len(substring))


def textViewer(text="", once=False):
    if not once or (once and settings.settings.getSetting("firstOpen") != "NO"):
        settings.settings.setSetting("firstOpen", "NO")
        w = TextViewer_Dialog('DialogTextViewer.xml', settings.path, header=settings.name, text=text)
        w.doModal()


def getMagnet(text=""):
    pos = text.rfind('/')
    magnet = text[pos + 1:]
    return unquoteName(magnet)


def goodSpider():
    from time import sleep
    import random
    sleep(random.randrange(100, 1000, 1) / 1000)


def dirImages(value):
    imageFile = os.path.join(settings.path, 'resources', 'images', value)
    if not os.path.isfile(imageFile):
        imageFile = settings.icon
    return imageFile


def removeDirectory(folder):
    from os import listdir
    from xbmc import translatePath

    folder = folder.replace('special://temp/', translatePath('special://temp'))
    folder = folder.replace('smb:', '')  # network compatibility
    listFolders = listdir(folder)
    rep = settings.dialog.select('Select the Folder to erase:', listFolders + ['-CANCEL'])
    if rep < len(listFolders):
        if settings.dialog.yesno("Attention!", "Are you sure to erase?", nolabel="No", yeslabel="Yes"):
            __removeDirectory__(folder=folder, title=listFolders[rep])


def __removeDirectory__(folder="", title=""):
    info = formatTitle(title)
    directory = os.path.join(folder, info['folder'])
    if os.path.exists(directory):
        import shutil
        shutil.rmtree(directory, ignore_errors=True)
    if not xbmc.getCondVisibility('Library.IsScanningVideo'):
        xbmc.executebuiltin('XBMC.CleanLibrary(video)')  # clean the library


def getPlayableLink(page):
    exceptionsList = Storage(settings.storageName.replace(".txt", "-exceptions.txt"))
    result = page
    settings.debug(result)
    if 'divxatope' in page:
        page = page.replace('/descargar/', '/torrent/')
        result = page
    isLink = True
    settings.debug(exceptionsList.database)
    for exception in exceptionsList.database:
        if exception in page:
            isLink = False
            break
    if page.startswith("http") and isLink:
        # exceptions
        settings.debug(result)
        # download page
        try:
            response = browser.get(page, verify=False)
            data = normalize(response.text)
            settings.debug(response.headers)
            if 'text/html' in response.headers.get("content-type", ""):
                content = re.findall('magnet:\?[^\'"\s<>\[\]]+', data)
                if content != None and len(content) > 0:
                    result = content[0]
                else:
                    content = re.findall('/download\?token=[A-Za-z0-9%]+', data)
                    if content != None and len(content) > 0:
                        result = settings.value["urlAddress"] + content[0]
                    else:
                        content = re.findall('/telechargement/[a-z0-9-_.]+', data)  # cpasbien
                        if content != None and len(content) > 0:
                            result = settings.value["urlAddress"] + content[0]
                        else:
                            content = re.findall('https?:[^\'"\s<>\[\]]+torrent', data)
                            if content != None and len(content) > 0:
                                result = content[0]
            else:
                exceptionsList.add(re.search("^https?:\/\/(.*?)/", page).group(1))
                exceptionsList.save()
        except:
            pass
    settings.log(result)
    return result


def getInfoLabels(infoTitle):
    from metahandler import metahandlers
    metaget = metahandlers.MetaData()
    infoLabels = {}
    try:
        if infoTitle is str:  # if it is a string get the FormatTitle dict structure
            infoTitle = formatTitle(infoTitle)
        settings.debug(infoTitle)
        cleanTitle = infoTitle["cleanTitle"]
        year = infoTitle["year"]
        if infoTitle["type"] == "MOVIE":
            infoLabels = metaget.get_meta('movie', cleanTitle, year=year)
        else:  # it is a TV Show or Anime
            infoLabels = metaget.get_meta('tvshow', cleanTitle, year=year)
        # cast and castandrole
        castList = []
        castAndRoleList = []
        for item in infoLabels.get("cast", []):
            if item is not None and item is str:
                castList.append(item)
                castAndRoleList.append((item, ""))
            else:
                castList.append(item[0])
                castAndRoleList.append(item)
        infoLabels["cast"] = castList
        infoLabels["castandrole"] = castAndRoleList
        # add episode and season
        infoLabels['season'] = infoTitle['season']
        infoLabels['episode'] = infoTitle['episode']
    except:
        pass
    duration = 0
    if infoLabels.has_key("duration") and infoLabels["duration"] != '' and infoLabels["duration"] != 'None':
        duration = int(infoLabels["duration"])
    infoLabels['duration'] = duration
    # force creation
    infoLabels['imdb_id'] = infoLabels.get('imdb_id', "")
    infoLabels['cover_url'] = infoLabels.get("cover_url", settings.icon)
    infoLabels['backdrop_url'] = infoLabels.get("backdrop_url", settings.fanart)
    # add label
    infoLabels['label'] = infoTitle["title"] + infoTitle.get("textQuality", "") + " " + infoTitle["language"]
    settings.debug(infoLabels)
    return infoLabels


def getInfoStream(infoTitle={}, infoLabels={}):
    infoStream = {'width': infoTitle["width"],
                  'height': infoTitle["height"],
                  'aspect': infoTitle["width"] / infoTitle["height"],
                  'duration': infoLabels["duration"],
                  }
    return infoStream


def getInfoSeason(infoLabels, seasons=[]):
    from metahandler import metahandlers
    metaget = metahandlers.MetaData()
    images = metaget.get_seasons(tvshowtitle=infoLabels["title"], imdb_id=infoLabels["imdb_id"],
                                 seasons=seasons, overlay=6)
    seasons = []
    for image in images:
        if image["cover_url"] == "":
            image["cover_url"] = infoLabels["cover_url"]
        if image["backdrop_url"] == "":
            image["backdrop_url"] = infoLabels["backdrop_url"]
        seasons.append(image)
    return seasons


def getInfoEpisode(infoLabels):
    from metahandler import metahandlers
    metaget = metahandlers.MetaData()
    result = infoLabels
    try:
        if infoLabels["episode"] != 0:
            result = metaget.get_episode_meta(tvshowtitle=infoLabels["title"], imdb_id=infoLabels["imdb_id"],
                                              season=infoLabels["season"], episode=infoLabels["episode"])
    except:
        pass
    return result


#  Search if a video is already in Kodi Database
def existInKodiLibrary(id, season="1", episode="1"):
    import json

    result = False
    if 'tt' in id:
        # Movies
        query = {
            'jsonrpc': '2.0',
            'id': 0,
            'method': 'VideoLibrary.GetMovies',
            'params': {
                'properties': ['imdbnumber', 'file']
            }
        }
        response = json.loads(xbmc.executeJSONRPC(json.dumps(query)))
        movieDict = dict(
            (movie['imdbnumber'], movie['file'])
            for movie in response.get('result', {}).get('movies', [])
        )
        if movieDict.has_key(id):
            result = True
    else:
        # TV Shows
        query = {
            'jsonrpc': '2.0',
            'id': 0,
            'method': 'VideoLibrary.GetTVShows',
            'params': {
                'properties': ['imdbnumber', 'file', 'season', 'episode']
            }
        }
        response = json.loads(xbmc.executeJSONRPC(json.dumps(query)))
        showDict = dict(
            (show['imdbnumber'] + "-" + str(show['season']) + "-" + str(show['episode']), show['file'])
            for show in response.get('result', {}).get('tvshows', [])
        )
        if showDict.has_key(id + "-" + str(season) + "-" + str(episode)):
            result = True
    return result


############  INTEGRATION   ###########################
def integration(titles=[], id=[], magnets=[], typeList='', folder='', typeVideo=[],
                silence=False, message='', channel=""):
    messageType = {'MOVIE': settings.string(32031), 'SHOW': settings.string(32032), 'ANIME': settings.string(32043),
                   '': 'Videos'}
    filters = Filtering()  # start filtering

    total = len(titles)
    answer = True
    if not silence:
        answer = settings.dialog.yesno(settings.string(32033) %
                                       (normalize(settings.name), total), '%s' % titles)
    if answer:  # it will integrate the filename list to the local library
        if not silence:
            settings.pDialog.create(settings.name, settings.string(32034) % (messageType[typeList], message))
        else:
            settings.notification(settings.string(32034) % (messageType[typeList], message))

        cont = 0
        for cm, title in enumerate(titles):
            # typeVideo or typeList
            if typeList == "":
                typeListItem = typeVideo[cm]
            else:
                typeListItem = typeList
            # folder
            if folder == '':
                if typeListItem == 'MOVIE':
                    folder = settings.movieFolder
                if typeListItem == 'SHOW':
                    folder = settings.showFolder
                if typeListItem == 'ANIME':
                    folder = settings.animeFolder
            # filters
            if typeListItem == 'MOVIE':
                filters.useMovie()
            else:
                filters.useTv()  # TV SHOWS and Anime
            filters.information()
            # formatTitle
            info = formatTitle(title, typeVideo=typeListItem)
            info['folder'] = info['folder'][:100].strip()  # to limit the length of directory name
            check = True
            detailsTitle = ''

            if len(info['rest']) > 0:  # check for quality filtering
                filters.title = info['title'] + ' ' + info['rest']
                if filters.verify(filters.title, None):  # just check the quality no more
                    check = True
                    if settings.value.get("duplicated", "false") == "true":
                        detailsTitle = ' ' + info['rest']
                else:
                    check = False
            if check:  # the file has passed the filtering
                name = info['title'] + detailsTitle
                name = name[:99].strip()  # to limit the length of name

                # Try to create the directory if it doesn't exist
                directory = path.join(folder, info['folder'])
                try:
                    os.makedirs(directory)
                except:
                    pass
                # Set-up the plugin
                goodSpider()  # to be a smart spider
                if channel == "":
                    uri_string = quote_plus(getPlayableLink(uncodeName(normalize(magnets[cm]))))
                    if settings.value["plugin"] == 'Quasar':
                        link = 'plugin://plugin.video.quasar/play?uri=%s' % uri_string
                    elif settings.value["plugin"] == 'Pulsar':
                        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string
                    elif settings.value["plugin"] == 'KmediaTorrent':
                        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string
                    elif settings.value["plugin"] == "Torrenter":
                        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string + \
                               '&not_download_only=True'
                    elif settings.value["plugin"] == "YATP":
                        link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
                    else:
                        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
                else:
                    link = "plugin://plugin.video.pelisalacarta/?channel=%s&action=play_from_library&url=%s" % (
                        channel, quote_plus(magnets[cm]))
                settings.debug(link)
                # start to create the strm file
                filename = path.join(directory, name + ".strm")
                # Find the code for the video
                codeMovie = ""
                codeShow = ""
                infoLabels = getInfoLabels(info)
                if len(id) > 0 and id[cm] != "":
                    codeMovie = codeShow = id[cm]
                else:
                    codeMovie = infoLabels.get("imdb_id", "")  # it tries to retrieve the IMDB number from title
                    codeShow = infoLabels.get("tvdb_id", "")  # it tries to retrieve the TVDB number from title
                # Write the strm file
                isAlreadyAdded = False
                if typeListItem == "MOVIE":
                    isAlreadyAdded = existInKodiLibrary(codeMovie)
                else:
                    isAlreadyAdded = existInKodiLibrary(codeShow, infoLabels['season'], infoLabels['episode'])
                if (not os.path.isfile(filename) and not isAlreadyAdded) or settings.value["overwrite"] == 'true':
                    cont += 1  # add new file's count
                    with open(filename, "w") as text_file:  # create .strm
                        text_file.write(link)
                    if os.path.isfile("*.nfo"):
                        settings.debug(".nfo existe!!!")
                    if codeMovie != "" and codeShow != "":  # Only it creates the nfo file if it is a IMDB number
                        if typeListItem == "MOVIE":
                            with open(filename.replace(".strm", ".nfo"), "w") as text_file:  # create .nfo MOVIE
                                text_file.write("http://www.imdb.com/title/%s/" % codeMovie)
                            settings.debug("imdb= " + codeMovie)
                        else:
                            with open(path.join(directory, "tvshow.nfo"), "w") as text_file:  # create .nfo SHOW
                                text_file.write("http://thetvdb.com/?tab=series&id=%s" % codeShow)
                            settings.debug("tvdb= " + codeShow)

                    if not silence: settings.pDialog.update(int(float(cm) / total * 100), settings.string(32036)
                                                            % (directory, name))
                    if not silence and settings.pDialog.iscanceled(): break
                    if cont % 100 == 0: settings.notification(
                        settings.string(32037) % (cont, messageType[typeListItem], message))
                    settings.log(settings.string(32038) % filename)
                elif isAlreadyAdded:
                    settings.log("%s is already in the library" % name)
                if not silence and settings.pDialog.iscanceled(): break
        if not silence: settings.pDialog.close()

        if cont > 0:  # There are files added
            if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
            settings.log(settings.string(32040) % (cont, messageType[typeListItem], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32040) % (cont, messageType[typeListItem], message))
            else:
                settings.notification(settings.string(32040) % (cont, messageType[typeListItem], message))
        else:
            settings.log(settings.string(32041) % (messageType[typeListItem], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32042) % (messageType[typeListItem], message))
            else:
                settings.notification(settings.string(32042) % (messageType[typeListItem], message))
                # del filters


############  SUBSCRIPTION   ###########################
def subscription(titles=[], id=[], typeList='', folder='', silence=False, message=''):
    from types import StringType
    messageType = {'MOVIE': settings.string(32031), 'SHOW': settings.string(32032)}
    total = len(titles)
    answer = True
    if not silence:
        answer = settings.dialog.yesno(settings.string(32033) %
                                       (settings.name, total), '%s' % titles)

    if answer:  # it will integrate the filename list to the local library
        if not silence:
            settings.pDialog.create(settings.name, settings.string(32034) % (messageType[typeList], message))
        else:
            settings.notification(settings.string(32034) % (messageType[typeList], message))
        # Open Database
        storage = Storage(settings.storageName, type="dict")
        cont = 0
        for cm, itemList in enumerate(titles):
            info = formatTitle(itemList if typeList == 'MOVIE' else itemList + ' S00E00')
            item = info['title'] if typeList == 'MOVIE' else info['cleanTitle']
            if storage.database.has_key(item):
                data = storage.database[item]
                data = literal_eval(data) if type(data) == StringType else data
                settings.debug('item(' + str(cm) + '): ' + str(data))
                settings.debug('type item(' + str(cm) + '): ' + str(type(data)))
                if typeList == 'SHOW':  # update the database to find new episodes
                    tvShow = TvShowCode(data['ID'], data['lastEpisode'], data['lastSeason'])
                    data['firstSeason'] = tvShow.firstSeason
                    data['lastSeason'] = tvShow.lastSeason
                    data['lastEpisode'] = tvShow.lastEpisode
            else:
                # create the item
                data = {}
                if len(id) > 0:
                    data['ID'] = id[cm]
                    if typeList == 'SHOW':
                        tvShow = TvShowCode(id[cm])
                        data['firstSeason'] = tvShow.firstSeason
                        data['lastSeason'] = tvShow.lastSeason
                        data['lastEpisode'] = tvShow.lastEpisode
                else:
                    if typeList == 'MOVIE':
                        movie = Movie(item)  # name of the movie with (year) format: Frozen (2013)
                        data['ID'] = movie.code  # search the IMDB id
                    elif typeList == 'SHOW':
                        tvShow = TvShow(info['cleanTitle'])  # search the name without year
                        data['ID'] = tvShow.code
                        if data['ID'] is not None:
                            data['firstSeason'] = tvShow.firstSeason
                            data['lastSeason'] = tvShow.lastSeason
                            data['lastEpisode'] = tvShow.lastEpisode
                data['type'] = typeList
                data['season'] = 0
                data['episode'] = 0

            # start to create strm files
            if typeList == 'MOVIE' and data['type'] == 'MOVIE' and data['episode'] == 0 and data[
                'ID'] is not None and not existInKodiLibrary(data['ID']):
                cont += 1
                # Try to create the directory if it doesn't exist
                directory = path.join(folder, info['folder'])
                try:
                    os.makedirs(directory)
                except:
                    pass
                data['path'] = directory  # To be able to erase the folder

                if settings.value["detailedLog"] == 'true':
                    settings.log('Code %s=%s' % (typeList, data['ID']))

                link = "plugin://plugin.video.quasar/library/play/movie/" + str(data['ID'])

                # start to create the strm file
                filename = path.join(directory, item + ".strm")
                with open(filename, "w") as text_file:  # create .strm MOVIE
                    text_file.write(link)
                with open(filename.replace(".strm", ".nfo"), "w") as text_file:  # create .nfo MOVIE
                    text_file.write("http://www.imdb.com/title/%s/" % data['ID'])
                data['episode'] = 1
                if not silence: settings.pDialog.update(int(float(cm) / total * 100), settings.string(32036)
                                                        % (directory, item))
                if cont % 100 == 0: settings.notification(settings.string(32037)
                                                          % (cont, messageType[typeList], message))
                settings.log(settings.string(32038) % filename)
            elif typeList == 'SHOW' and data['type'] == 'SHOW' and data['ID'] is not None:  # add shows
                if settings.value["specials"] == 'false' and data['firstSeason'] == 0:
                    data['firstSeason'] = 1
                directory = folder + item + folder[-1]
                # Try to create the directory if it doesn't exist
                directory = path.join(folder, info['folder'])
                try:
                    os.makedirs(directory)
                except:
                    pass
                data['path'] = directory  # To be able to erase the folder
                if settings.value["detailedLog"] == 'true':
                    settings.log(settings.string(32035) % (typeList, data['ID']))
                    settings.log(
                        '%s %s-%s: %s' % (item, data['firstSeason'], data['lastSeason'], data['lastEpisode']))
                with open(path.join(directory, "tvshow.nfo"), "w") as text_file:  # create .nfo SHOW
                    text_file.write("http://thetvdb.com/?tab=series&id=%s" % data['ID'])
                for season in range(max(data['season'], data['firstSeason']), data['lastSeason'] + 1):
                    if data['lastEpisode'].has_key(season):
                        for episode in range(data['episode'] + 1, data['lastEpisode'][season] + 1):
                            if not existInKodiLibrary(data['ID'], str(season), str(episode)):
                                cont += 1
                                link = 'plugin://plugin.video.quasar/show/%s/season/%s/episode/%s/%s' % (
                                    data['ID'], season, episode, settings.value["action"])
                                if not silence: settings.pDialog.update(int(float(cm) / total * 100),
                                                                        "%s%s S%02dE%02d.strm" % (
                                                                            directory, item, season, episode))
                                if cont % 100 == 0: settings.notification(
                                    settings.string(32037) % (cont, messageType[typeList], message))
                                filename = path.join(directory, item + " S%02dE%02d.strm" % (season, episode))
                                with open(filename, "w") as text_file:  # create .strm
                                    text_file.write(link)
                                    settings.log(settings.string(32038) % filename)
                                if not silence and settings.pDialog.iscanceled(): break
                        data['episode'] = 0  # change to new season and reset the episode to 1
                if not silence and settings.pDialog.iscanceled(): break
                data['season'] = data['lastSeason']
                if data['lastEpisode'].has_key(data['lastSeason']):
                    data['episode'] = data['lastEpisode'][data['lastSeason']]
                if not silence: settings.pDialog.update(int(float(cm) / total * 100),
                                                        settings.string(32036) % (directory, item))
                settings.log(settings.string(32039) % (directory, item))
            # update database
            if data['ID'] is not None:
                storage.database[item] = data
            if not silence and settings.pDialog.iscanceled(): break
        # confirmation and close database
        storage.save()
        if cont > 0:
            if not xbmc.getCondVisibility('Library.IsScanningVideo'):
                xbmc.executebuiltin('XBMC.UpdateLibrary(video)')  # update the library with the new information
            settings.log(settings.string(32040) % (cont, messageType[typeList], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32040) % (cont, messageType[typeList], message))
            else:
                settings.notification(settings.string(32040) % (cont, messageType[typeList], message))

        else:
            settings.log(settings.string(32041) % (messageType[typeList], message))
            if not silence:
                settings.dialog.ok(settings.name, settings.string(32042) % (messageType[typeList], message))
            else:
                settings.notification(settings.string(32042) % (messageType[typeList], message))
        del storage
