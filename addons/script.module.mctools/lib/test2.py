# coding: utf-8
__author__ = 'Mancuniancol'
import re


class Settings():
    animeFolder = ''
    movieFolder = ''
    showFolder = ''

settings = Settings()


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
        language = " Español "
    if "hindi" in value:
        language = "Hindi"
    if "castellano" in value:
        language = "Castellano"
    if "french" in value or 'francais' in value:
        language = "French"
    if "german" in value:
        language = "German"
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
                  "width": width(quality), 'language': language, 'folderPath': settings.movieFolder
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
                  "width": width(quality), "language": language, 'folderPath': settings.showFolder
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


print formatTitle('[4k ultra hd] San Andreas 4K SBS 6 Channel AAC  ENG 3D [SEEDERS (0) LEECHERS (0)]')
