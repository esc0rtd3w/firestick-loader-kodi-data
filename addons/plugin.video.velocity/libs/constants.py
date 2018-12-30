"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris
    Alterd by : Blazetamer for Velocity

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
def __enum(**enums):
    return type('Enum', (), enums)

SECTIONS = __enum(TV='TV', MOVIES='Movies')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')
CONTENT_TYPES = __enum(TVSHOWS='tvshows', MOVIES='movies', SEASONS='seasons', EPISODES='episodes', FILES='files', ADDONS='addons')
TRAKT_SECTIONS = {SECTIONS.TV: 'shows', SECTIONS.MOVIES: 'movies'}
TRAKT_SORT = __enum(TITLE='title', RECENT_ACTIVITY='recent-activity', MOST_COMPLETED='most-completed', LEAST_COMPLETED='least-completed', RECENTLY_AIRED='recently-aired',
                    PREVIOUSLY_AIRED='previously-aired', PAST_ACTIVITY='past-activity')
TRAKT_LIST_SORT = __enum(RANK='rank', RECENTLY_ADDED='added', TITLE='title', RELEASE_DATE='released', RUNTIME='runtime', POPULARITY='popularity',
                         PERCENTAGE='percentage', VOTES='votes')
TRAKT_SORT_DIR = __enum(ASCENDING='asc', DESCENDING='desc')
SORT_MAP = [TRAKT_SORT.RECENT_ACTIVITY, TRAKT_SORT.TITLE, TRAKT_SORT.MOST_COMPLETED, TRAKT_SORT.LEAST_COMPLETED, TRAKT_SORT.RECENTLY_AIRED,
            TRAKT_SORT.PREVIOUSLY_AIRED, TRAKT_SORT.PAST_ACTIVITY]
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
DIRS = __enum(UP='up', DOWN='down')
REWATCH_METHODS = __enum(LAST_WATCHED='last_watched', LEAST_WATCHED='min_watched', MOST_WATCHED='max_watched')
GENRE_LIST = __enum(TRENDING=0, POPULAR=1, ANTICIPATED=2, MOST_WATCHED_WEEK=3, MOST_WATCHED_MONTH=4, MOST_WATCHED_ALL=5,
                    MOST_PLAYED_WEEK=6, MOST_PLAYED_MONTH=7, MOST_PLAYED_ALL=8,
                    MOST_COLLECTED_WEEK=9, MOST_COLLECTED_MONTH=10, MOST_COLLECTED_ALL=11)
WATCHLIST_SLUG = 'watchlist_slug'
COLLECTION_SLUG = 'collection_slug'
SEARCH_HISTORY = 10
DEFAULT_EXT = '.mpg'
CHUNK_SIZE = 512 * 1024
PROGRESS = __enum(OFF=0, WINDOW=1, BACKGROUND=2)
FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
SHORT_MONS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ACTIONS = __enum(ADD='add', REMOVE='remove')
TRIG_DB_UPG = False

# sort keys need to be defined such that "best" have highest values
# unknown (i.e. None) is always worst
SORT_KEYS = {}
SORT_KEYS['quality'] = {None: 0, QUALITIES.LOW: 1, QUALITIES.MEDIUM: 2, QUALITIES.HIGH: 3, QUALITIES.HD720: 4, QUALITIES.HD1080: 5}
SORT_LIST = ['none', 'source', 'quality', 'views', 'rating', 'direct', 'debrid']
SORT_SIGNS = {'0': -1, '1': 1}  # 0 = Best to Worst; 1 = Worst to Best


LONG_AGO = '1970-01-01 23:59:00.000000'
TEMP_ERRORS = [500, 502, 503, 504, 520, 521, 522, 524]
SRT_SOURCE = 'addic7ed'
DISABLE_SETTINGS = __enum(OFF='0', PROMPT='1', ON='2')

BLOG_Q_MAP = {}
BLOG_Q_MAP[QUALITIES.LOW] = [' CAM ', ' TS ', ' R6 ', 'CAMRIP']
BLOG_Q_MAP[QUALITIES.MEDIUM] = ['-XVID', '-MP4', 'MEDIUM']
BLOG_Q_MAP[QUALITIES.HIGH] = ['HDRIP', 'DVDRIP', 'BRRIP', 'BDRIP', '480P', 'HDTV']
BLOG_Q_MAP[QUALITIES.HD720] = ['720', 'HDTS', ' HD ']
BLOG_Q_MAP[QUALITIES.HD1080] = ['1080']

HOST_Q = {}
HOST_Q[QUALITIES.LOW] = ['youwatch', 'allmyvideos', 'played.to', 'gorillavid']
HOST_Q[QUALITIES.MEDIUM] = ['primeshare', 'exashare', 'bestreams', 'flashx', 'vidto', 'vodlocker', 'vidzi', 'vidbull', 'realvid', 'nosvideo',
                            'daclips', 'sharerepo', 'zalaa', 'filehoot', 'vshare.io']
HOST_Q[QUALITIES.HIGH] = ['vidspot', 'mrfile', 'divxstage', 'streamcloud', 'mooshare', 'novamov', 'mail.ru', 'vid.ag', 'thevideo']
HOST_Q[QUALITIES.HD720] = ['thefile', 'sharesix', 'filenuke', 'vidxden', 'movshare', 'nowvideo', 'vidbux', 'streamin.to', 'allvid.ch', 'weshare']
HOST_Q[QUALITIES.HD1080] = ['hugefiles', '180upload', 'mightyupload', 'videomega', 'allmyvideos']

Q_ORDER = {QUALITIES.LOW: 1, QUALITIES.MEDIUM: 2, QUALITIES.HIGH: 3, QUALITIES.HD720: 4, QUALITIES.HD1080: 5}

IMG_SIZES = ['full', 'medium', 'thumb']

XHR = {'X-Requested-With': 'XMLHttpRequest'}
USER_AGENT = "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"
BR_VERS = [
    ['%s.0' % i for i in xrange(18, 50)],
    ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
     '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
     '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80', '48.0.2564.116', '49.0.2623.112', '50.0.2661.86', '51.0.2704.103', '52.0.2743.116', '53.0.2785.143', '54.0.2840.71'],
    ['11.0'],
    ['8.0', '9.0', '10.0', '10.6']]
WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
            'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
            'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko',
            'Mozilla/5.0 (compatible; MSIE {br_ver}; {win_ver}{feature}; Trident/6.0)']
