# -*- coding: utf-8 -*-
from re import sub, search
from browser import Browser
from json import loads
import storage
from utils import get_int


#  ###############################
#  ### SCRAPER TITLES ############
#  ###############################


# noinspection PyBroadException
def read_json(value=""):
    try:
        response = loads(value)
    except:
        response = {}
    return response


def read_dict(dictionary=None, key="", default=""):
    value = default
    if dictionary is not None:
        value = dictionary.get(key, default)
        if value is None:
            value = ""
    return value


def normalize(name):
    if isinstance(name, unicode):
        return name.encode('utf-8', 'ignore')
    return name


# noinspection PyBroadException
def normalize2(name, only_decode=False):
    from unicodedata import normalize
    if isinstance(name, str):
        unicode_name = name.decode('unicode-escape')
    else:
        try:
            unicode_name = name.encode('latin-1').decode('utf-8')  # to latin-1
        except:
            unicode_name = name
    normalize_name = unicode_name if only_decode else normalize('NFKD', unicode_name)
    return normalize_name.encode('ascii', 'ignore')


# Convert all the &# codes to char, remove extra-space and normalize
def uncode_name(name):
    from HTMLParser import HTMLParser
    name = name.replace('<![CDATA[', '').replace(']]', '')
    name = HTMLParser().unescape(name)
    return name


def unquote_name(name):  # Convert all %symbols to char
    from urllib import unquote
    return unquote(name).decode("utf-8")


def safe_name(value):  # Make the name directory and filename safe
    value = normalize(value)  # First normalization
    value = unquote_name(value)
    value = uncode_name(value)
    value = normalize2(value)  # Last normalization, because some unicode char could appear from the previous steps
    value = value.lower().title().replace('_', ' ')
    # erase keyword
    value = sub('^\[.*?\]', '', value)  # erase [HorribleSub] for ex.
    # check for anime
    value = sub('- ([0-9][0-9][0-9][0-9]) ', ' \g<1>', value + " ")
    value = sub('- ([0-9]+) ', '- EP\g<1>', value + " ")
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


def check_quality(text=""):
    # quality
    key_words = {"Cam": ["camrip", "cam"],
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
    text_quality = ""
    for key in key_words:
        for keyWord in key_words[key]:
            if ' ' + keyWord + ' ' in ' ' + text + ' ':
                quality = "480p"
                text_quality += " [COLOR %s][%s][/COLOR]" % (color[key], key)

    if "480p" in text:
        quality = "480p"
        text_quality += " [COLOR FF2980B9][480p][/COLOR]"
    if "720p" in text:
        quality = "720p"
        text_quality += " [COLOR FF5CD102][720p][/COLOR]"
    if "1080p" in text:
        quality = "1080p"
        text_quality += " [COLOR FFF4AE00][1080p][/COLOR]"
    if "3d" in text:
        quality = "1080p"
        text_quality += " [COLOR FFD61515][3D][/COLOR]"
    if "4k" in text:
        quality = "2160p"
        text_quality += " [COLOR FF16A085][4K][/COLOR]"
    return quality, text_quality


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


def find_language(value=""):
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


def exceptions_title(title=""):
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


def _clean_title(value=''):
    keywords_clean_title = ['version', 'extendida', 'extended', 'edition', 'hd', 'unrated', 'version', 'vose',
                            'special', 'edtion', 'uncensored', 'fixed', 'censurada', 'episode', 'ova', 'complete',
                            'swesub'
                            ]
    for keyword in keywords_clean_title:  # checking keywords
        value = (value + ' ').replace(' ' + keyword.title() + ' ', ' ')
    return value.strip()


# noinspection PyBroadException
def format_title(value='', file_name='', type_video="MOVIE"):
    if file_name.startswith('magnet'):
        file_name = ''
    if file_name == '':
        file_name = value
    pos = value.rfind("/")
    value = value if pos < 0 else value[pos:]
    value = safe_name(value).lower() + ' '
    file_name = safe_name(file_name).lower() + ' '
    quality, text_quality = check_quality(value + ' ' + file_name)  # find quality
    language = find_language(value)  # find language
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
                '4k', 'uhd', 'subbed', 'mp4'
                ]
    s_show = None
    for f_format in formats:  # search if it is a show
        s_show = search(f_format, value)  # format shows
        if s_show is not None:
            break
    if s_show is None and type_video != "MOVIE":
        if type_video == 'SHOW':
            value += ' s00e00'
        if type_video == 'ANIME':
            value += ' ep00'
        for f_format in formats:  # search if it is a show
            s_show = search(f_format, value)  # format shows
            if s_show is not None:
                break
    if s_show is None:
        # it is a movie
        value += ' 0000 '  # checking year
        s_year = search(' [0-9][0-9][0-9][0-9] ', value)
        year = s_year.group(0).strip()
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
        clean_title = _clean_title(title)
        # finishing clean_title
        if '0000' not in year:
            title += ' (' + year.strip() + ')'
        year = year.replace('0000', '')
        folder = title
        result = {'title': title, 'folder': folder, 'rest': rest.strip(), 'type': 'MOVIE', 'clean_title': clean_title,
                  'year': year, 'quality': quality, 'text_quality': text_quality, 'height': height(quality),
                  "width": width(quality), 'language': language
                  }
        return result
    else:
        # it is a show
        rest = value.strip()  # original name
        season_episode = s_show.group(0)
        # clean title
        for keyword in keywords:  # checking keywords
            value = value.replace(' ' + keyword + ' ', ' ')
        title = value[:value.find(season_episode)].strip()
        title = title.strip()
        season_episode = season_episode.replace('temporada ', 's').replace(' capitulo ', 'e')
        season_episode = season_episode.replace('season ', 's').replace(' episode ', 'e')
        season_episode = season_episode.replace('temp ', 's').replace(' cap ', 'e')
        season_episode = season_episode.replace('seizoen ', 's').replace(' afl ', 'e')

        if 'x' in season_episode:
            season_episode = 's' + season_episode.replace('x', 'e')

        # force S00E00 instead S0E0
        if 's' in season_episode and 'e' in season_episode and 'season' not in season_episode:
            temp_episode = season_episode.replace('s', '').split('e')
            season_episode = 's%02de%02d' % (int(temp_episode[0]), int(temp_episode[1]))

        if 's' not in season_episode and 'e' not in season_episode:  # date format
            date = season_episode.split()
            if len(date[0]) == 4:  # yyyy-mm-dd format
                season_episode = season_episode.replace(' ', '-')  # date style episode talk shows
            else:  # dd mm yy format
                if int(date[2]) > 50:
                    date[2] = '19' + date[2]
                else:
                    date[2] = '20' + date[2]
                season_episode = date[2] + '-' + date[1] + '-' + date[0]

        season_episode = season_episode.replace(' ', '')  # remove spaces in the episode format
        title = exceptions_title(title)
        # finding year
        value = title + ' 0000 '
        s_year = search(' [0-9][0-9][0-9][0-9] ', value)
        year = s_year.group(0).strip()
        pos = value.find(year)
        if pos > 0:
            title = value[:pos].strip()
        else:
            title = value.replace('0000', '')
        year = year.replace('0000', '')
        # the rest
        title = title.title().strip().replace('Of ', 'of ').replace('De ', 'de ')
        folder = title  # with year
        clean_title = _clean_title(title.replace(year, '').strip())  # without year
        title = folder + ' ' + season_episode.upper()
        title = title.replace('S00E00', '').replace('EP00', '')
        t_type = "SHOW"
        result = {'title': title, 'folder': folder, 'rest': rest, 'type': t_type, 'clean_title': clean_title,
                  'year': year, 'quality': quality, 'text_quality': text_quality, 'height': height(quality),
                  "width": width(quality), "language": language
                  }
        if bool(search("EP[0-9]+", title)):
            result['type'] = "ANIME"
            result['season'] = 1
            result['episode'] = int(season_episode.replace('ep', ''))
        else:
            temp = (season_episode.replace('s', '')).split('e')
            result['season'] = 0
            result['episode'] = 0
            try:
                result['season'] = int(temp[0])
                result['episode'] = int(temp[1])
            except:
                pass
        return result


def find_imdb(title=None):
    imdb = storage.Storage.open("imdb", ttl=None)
    if title is None:
        imdb.clear()
        result = ''
    else:
        title = title.lower()
        result = imdb.get(title, '')
        if result == '':
            Browser.open('https://www.google.ca/search?q=%s+imdb' % title.replace(' ', '+'))
            data = Browser.content
            # noinspection PyBroadException
            try:
                s_imdb = search('(tt[0-9]+)', data)
            except:
                s_imdb = None
            if s_imdb:
                result = s_imdb.group(1)
                imdb[title] = result
                imdb.sync()
    return result


class Untangle:
    base_url = 'http://image.tmdb.org/t/p/w500'
    info_title = dict()
    info_labels = dict()
    info_stream = dict()
    title = ""
    proper_title = ""
    clean_title = ""
    year = ""
    file_name = ""
    type_video = ""
    label = ""
    id = ""
    info = dict()
    cover = ""
    fanart = ""
    season = ""
    episode = ""
    imdb_id = ""
    title_episode = ""
    tmdb_api = ""
    tmdb_id = ""
    info_labels_init = {
        'tmdb_id': '',
        'cover_url': '',
        'fanart': '',
        'genre': '',  # string(Comedy)
        'year': 0,  # integer(2009)
        'episode': 0,  # integer(4)
        'season': 0,  # integer(1)
        'top250': 0,  # integer(192)
        'tracknumber': 0,  # integer(3)
        'rating': 0.0,  # float(6.4) - range is 0..10
        'playcount': 0,  # integer(2) - number of times this item has been played (watched)
        'overlay': 0,  # integer(2) - range is 0..8.See GUIListItem.h for values
        'cast': [],  # list(["Michal C. Hall", "Jennifer Carpenter"])
        'castandrole': [],  # list of tuples([("Michael C. Hall", "Dexter"), ("Jennifer Carpenter", "Debra")])
        'director': '',  # string(Dagur Kari)
        'mpaa': '',  # string(PG - 13)
        'plot': '',  # string(Long Description)
        'plotoutline': '',  # string(Short Description)
        'title': '',  # string(Big Fan)
        'originaltitle': '',  # string(Big Fan)
        'sorttitle': '',  # string(BigFan)
        'duration': 0,  # integer(245) - duration in seconds
        'studio': '',  # string(Warner Bros.)
        'tagline': '',  # string(An awesome movie) - short description
        'writer': '',  # string(Robert D.Siegel)
        'tvshowtitle': '',  # string(Heroes)
        'premiered': '',  # string(2005 - 03 - 04)
        'status': '',  # string(Continuing) - status of a TVshow
        'code': '',  # string(tt0110293) - IMDb code
        'aired': '',  # string(2008 - 12 - 07)
        'credits': '',  # string(Andy Kaufman) - writing  credits
        'lastplayed': '',  # string(Y - m - d  h:m:s = 2009 - 04 - 05 23:16:04)
        'album': '',  # string(The Joshua Tree)
        'artist': [''],  # list(['U2'])
        'votes': '',  # string(12345 votes)
        'trailer': '',  # string( / home / user / trailer.avi)
        'dateadded': '',  # string(Y - m - d h:m:s = 2009 - 04 - 05 23:16:04)"""
    }
    info_stream_init = {'width': 0,
                        'height': 0,
                        'aspect': 1,
                        'duration': 0,
                        }
    use_meta_info = True

    def __init__(self, value='', file_name='', type_video="MOVIE", use_url=True, use_meta_info=True, imdb_id='',
                 icon='', fanart='', tmdb_api=''):
        self.title = normalize(value)
        self.file_name = file_name
        self.tmdb_api = tmdb_api
        self.imdb_id = imdb_id
        self.use_meta_info = use_meta_info

        # Formatting the title
        if use_url:
            self.info_title = format_title(value, file_name, type_video)  # organize the title information
        else:
            self.info_title = format_title(value, '', type_video)  # organize the title information

        # Reading form format title information
        self.proper_title = self.info_title["title"] if self.info_title == 'MOVIE' else self.info_title["clean_title"]
        self.clean_title = self.info_title["clean_title"]
        self.year = self.info_title["year"]
        self.type_video = self.info_title["type"]

        # getting IMDB code
        if self.imdb_id is '':
            self.id = find_imdb(self.proper_title)
            self.imdb_id = self.id

        # Reading infoLabels
        self.info_labels = self.get_info_labels()
        self.info_stream = self.get_info_stream()
        self.cover = self.info_labels["cover_url"]
        self.fanart = self.info_labels["fanart"]

        # reading last info
        self.info = self.info_labels.copy()
        self.label = self.info_title["title"] + self.info_title.get("text_quality") + " " + self.info_title[
            "language"]
        if self.info_title["type"] == 'SHOW':  # difference with show and anime
            self.info = self.get_info_episode(self.info_labels)
            self.title_episode = ' - ' + normalize(self.info.get('title'))
        if self.cover == "":
            self.cover = icon
        if self.fanart == "":
            self.fanart = fanart

    def get_info_labels(self):
        info_labels = self.info_labels_init.copy()
        info_labels['code'] = self.imdb_id
        if self.imdb_id is not '' and self.use_meta_info:
            info_labels_storage = storage.Storage.open('info_labels')
            info_labels = info_labels_storage.get(self.imdb_id, '')
            if info_labels == '':
                info_labels = self.get_meta()
                if info_labels is not self.info_labels_init:
                    info_labels_storage[self.imdb_id] = info_labels
                    info_labels_storage.sync()
        self.episode = self.info_title.get("episode", 0)
        self.season = self.info_title.get("season", 0)
        self.tmdb_id = info_labels["tmdb_id"]
        return info_labels

    def get_info_stream(self):
        info_stream = self.info_stream_init.copy()
        if self.info_title is not None and self.info_labels is not None:
            s_width = self.info_title.get("width", 640)
            s_height = self.info_title.get("height", 800)
            info_stream = {'width': s_width,
                           'height': s_height,
                           'aspect': s_width / s_height,
                           'duration': self.info_labels.get("duration", 0),
                           }
        return info_stream

    def get_info_episode(self, info_labels_init):
        info_labels = info_labels_init.copy()
        if self.imdb_id is not '' and self.use_meta_info:
            info_labels_storage = storage.Storage.open('info_labels')
            info_labels = info_labels_storage.get("%s-%s-%s" % (self.imdb_id, self.season, self.episode), '')
            if info_labels == '':
                info_labels = self.get_meta_episode(info_labels_init)
                if info_labels is not self.info_labels_init:
                    info_labels_storage["%s-%s-%s" % (self.imdb_id, self.season, self.episode)] = info_labels
                    info_labels_storage.sync()
        return info_labels

    # noinspection PyTypeChecker
    def get_meta(self):
        info_labels = self.info_labels_init.copy()

        if self.tmdb_api != '':
            url = 'https://api.themoviedb.org/3/find/%s?external_source=imdb_id&api_key=%s' % (
                self.imdb_id, self.tmdb_api)
            Browser.open(url)
            response = read_json(Browser.content)
            if read_dict(response, 'movie_results', False) and self.type_video == 'MOVIE':
                for item in response['movie_results']:
                    info_labels["tmdb_id"] = self.tmdb_id = read_dict(item, 'id')
                    info_labels["code"] = self.imdb_id
                    info_labels["type"] = "movie"
                    info_labels["fanart"] = self.base_url + read_dict(item, "backdrop_path")
                    info_labels['cover_url'] = self.base_url + read_dict(item, "poster_path")
                    info_labels["originaltitle"] = read_dict(item, "original_title")
                    info_labels["premiered"] = read_dict(item, "release_date")
                    info_labels["aired"] = read_dict(item, "release_date")
                    info_labels["year"] = read_dict(item, "release_date")[:4]
                    info_labels["title"] = read_dict(item, "title")
                    info_labels["sorttitle"] = read_dict(item, "title").replace(" ", "")
                    info_labels["plot"] = read_dict(item, "overview")
                    info_labels["votes"] = read_dict(item, "vote_count")

                    # Read Details
                    url = 'http://api.themoviedb.org/3/movie/%s?api_key=%s' % (self.tmdb_id, self.tmdb_api)
                    Browser.open(url)
                    details = read_json(Browser.content)
                    info_labels["status"] = read_dict(details, "status")
                    info_labels["duration"] = read_dict(details, "runtime", 0) * 60
                    info_labels["rating"] = read_dict(details, "popularity")
                    info_labels["tagline"] = read_dict(details, "tagline")

                    # Read genres
                    genres = read_dict(details, "genres", [])
                    for genre in genres:
                        info_labels["genre"] += genre["name"] + ", "

                    # Read studios
                    studios = read_dict(details, "production_companies", [])
                    for studio in studios:
                        info_labels["studio"] += studio["name"] + ", "

                    # Read cast
                    url = 'http://api.themoviedb.org/3/movie/%s/credits?api_key=%s' % (self.tmdb_id, self.tmdb_api)
                    Browser.open(url)
                    details = read_json(Browser.content)
                    cast_list = []
                    cast_and_role_list = []
                    for cast in read_dict(details, 'cast', []):
                        cast_list.append(cast["name"])
                        cast_and_role_list.append((cast["name"], cast["character"]))
                    info_labels["cast"] = cast_list
                    info_labels["castandrole"] = cast_and_role_list

                    # read crew
                    info_labels["director"] = ''
                    info_labels["credits"] = ''
                    for crew in read_dict(details, 'crew', []):
                        info_labels["credits"] += " %s - %s," % (crew["name"], crew["job"])
                        if crew["job"].lower() == "director":
                            info_labels["director"] = crew["name"]
                        if crew["job"].lower() == "writer":
                            info_labels["writer"] = crew["name"]

                    # read trailer
                    url = 'http://api.themoviedb.org/3/movie/%s/videos?api_key=%s' % (self.tmdb_id, self.tmdb_api)
                    Browser.open(url)
                    trailers = read_json(Browser.content)
                    for trailer in trailers.get("results", []):
                        info_labels["trailer"] = 'http://www.youtube.com/watch?v=%s' % trailer["key"]
                        break

                    # other information
                    info_labels["top250"] = 0
                    info_labels["tracknumber"] = 0
                    info_labels["playcount"] = 0
                    info_labels["overlay"] = 0
                    info_labels["mpaa"] = ''
                    info_labels["tvshowtitle"] = ''
                    info_labels["lastplayed"] = ''
                    info_labels["album"] = ''
                    info_labels["artist"] = ['']
                    info_labels["dateadded"] = ''

            elif read_dict(response, 'tv_results', False):
                for item in response['tv_results']:
                    info_labels["tmdb_id"] = self.tmdb_id = read_dict(item, 'id')
                    info_labels["code"] = self.imdb_id
                    info_labels["type"] = "series"
                    info_labels["fanart"] = self.base_url + read_dict(item, "backdrop_path")
                    info_labels['cover_url'] = self.base_url + read_dict(item, "poster_path")
                    info_labels["originaltitle"] = read_dict(item, "original_name")
                    info_labels["premiered"] = read_dict(item, "first_air_date")
                    info_labels["aired"] = read_dict(item, "first_air_date")
                    info_labels["year"] = read_dict(item, "first_air_date")[:4]
                    info_labels["title"] = read_dict(item, "name")
                    info_labels["sorttitle"] = read_dict(item, "name").replace(" ", "")
                    info_labels["plot"] = read_dict(item, "overview")
                    info_labels["votes"] = read_dict(item, "vote_count")

                    # Read Details
                    url = 'http://api.themoviedb.org/3/tv/%s?api_key=%s' % (self.tmdb_id, self.tmdb_api)
                    Browser.open(url)
                    details = read_json(Browser.content)
                    info_labels["status"] = read_dict(details, "status")
                    info_labels["duration"] = read_dict(details, "episode_run_time", [0]) * 60
                    info_labels["rating"] = read_dict(details, "popularity")
                    info_labels["tagline"] = ""

                    # Read genres
                    genres = read_dict(details, "genres", [])
                    for genre in genres:
                        info_labels["genre"] += genre["name"] + ", "

                    # Read studios
                    studios = read_dict(details, "production_companies", [])
                    for studio in studios:
                        info_labels["studio"] += studio["name"] + ", "

                    # Read cast
                    url = 'http://api.themoviedb.org/3/movie/%s/credits?api_key=%s' % (self.tmdb_id, self.tmdb_api)
                    Browser.open(url)
                    details = read_json(Browser.content)
                    cast_list = []
                    cast_and_role_list = []
                    for cast in read_dict(details, 'cast', []):
                        cast_list.append(cast["name"])
                        cast_and_role_list.append((cast["name"], cast["character"]))
                    info_labels["cast"] = cast_list
                    info_labels["castandrole"] = cast_and_role_list

                    # read crew
                    info_labels["director"] = ''
                    info_labels["credits"] = ''
                    for crew in read_dict(details, 'crew', []):
                        info_labels["credits"] += " %s - %s," % (crew["name"], crew["job"])
                        if crew["job"].lower() == "director":
                            info_labels["director"] = crew["name"]
                        if crew["job"].lower() == "writer":
                            info_labels["writer"] = crew["name"]

                    # read trailer
                    url = 'http://api.themoviedb.org/3/tv/%s/videos?api_key=%s' % (self.tmdb_id, self.tmdb_api)
                    Browser.open(url)
                    trailers = read_json(Browser.content)
                    for trailer in trailers.get("results", []):
                        info_labels["trailer"] = 'http://www.youtube.com/watch?v=%s' % trailer["key"]
                        break

                    # other information
                    info_labels["top250"] = 0
                    info_labels["tracknumber"] = 0
                    info_labels["playcount"] = 0
                    info_labels["overlay"] = 0
                    info_labels["mpaa"] = ''
                    info_labels["tvshowtitle"] = info_labels["title"]
                    info_labels["lastplayed"] = ''
                    info_labels["album"] = ''
                    info_labels["artist"] = ['']
                    info_labels["dateadded"] = ''
        else:
            # Search in http://www.omdbapi.com/
            # Please visit the page and donate
            url = 'http://www.omdbapi.com/?i=%s&plot=full&r=json' % self.imdb_id
            Browser.open(url)
            response = read_json(Browser.content)
            info_labels["tmdb_id"] = ""
            info_labels["code"] = read_dict(response, "imdbID")
            info_labels["type"] = read_dict(response, "Type")
            info_labels['fanart'] = read_dict(response, "Poster")
            info_labels['cover_url'] = read_dict(response, "Poster")
            info_labels["originaltitle"] = read_dict(response, "Title")
            info_labels["premiered"] = read_dict(response, "Released")
            info_labels["aired"] = read_dict(response, "Released")
            info_labels["year"] = read_dict(response, "Year")
            info_labels["title"] = read_dict(response, "Title")
            if info_labels["type"] == "series":
                info_labels["tvshowtitle"] = read_dict(response, "Title")
            info_labels["sorttitle"] = read_dict(response, "Title").replace(" ", "")
            info_labels["plot"] = read_dict(response, "Plot")
            info_labels["votes"] = read_dict(response, "imdbVotes")
            info_labels["status"] = "Released"
            info_labels["duration"] = get_int(read_dict(response, "Runtime", "0")) * 60
            info_labels["rating"] = read_dict(response, "imdbRating")
            info_labels["tagline"] = read_dict(response, "Awards")
            info_labels["genre"] = read_dict(response, "Genre")
            info_labels["studios"] = ""
            info_labels["cast"] = read_dict(response, "Actors")
            info_labels["castandrole"] = ""
            info_labels["director"] = read_dict(response, "Director")
            info_labels["writer"] = read_dict(response, "Writer")
            info_labels["credits"] = read_dict(response, "Writer")
            info_labels["trailer"] = ""

            # other information
            info_labels["episode"] = 0
            info_labels["season"] = 0
            info_labels["top250"] = 0
            info_labels["tracknumber"] = 0
            info_labels["playcount"] = 0
            info_labels["overlay"] = 0
            info_labels["mpaa"] = read_dict(response, "Rated")
            info_labels["tvshowtitle"] = ''
            info_labels["lastplayed"] = ''
            info_labels["album"] = ''
            info_labels["artist"] = ['']
            info_labels["dateadded"] = ''
        # Common information
        info_labels["episode"] = self.info_title.get("episode", 0)
        info_labels["season"] = self.info_title.get("season", 0)
        return info_labels

    # noinspection PyTypeChecker
    def get_meta_episode(self, info_labels_init):
        info_labels = info_labels_init.copy()
        # Read Details Episode
        url = 'http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=%s' % (
            self.tmdb_id, self.season, self.episode, self.tmdb_api)
        Browser.open(url)
        details = read_json(Browser.content)
        info_labels["aired"] = read_dict(details, "air_date")
        info_labels["title"] = read_dict(details, "name")
        info_labels["status"] = read_dict(details, "status", "Aired")
        info_labels["rating"] = read_dict(details, "vote_average")
        info_labels["plot"] = read_dict(details, "overview")
        info_labels['cover_url'] = self.base_url + read_dict(details, "still_path")
        # Read genres
        cast_list = []
        cast_and_role_list = []
        for cast in read_dict(details, 'guest_stars', []):
            cast_list.append(cast["name"])
            cast_and_role_list.append((cast["name"], cast["character"]))
        info_labels["cast"] = cast_list
        info_labels["castandrole"] = cast_and_role_list
        return info_labels
