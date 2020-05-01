import os
import cgi
import urllib, urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import re
import logging
logging.basicConfig(level=logging.DEBUG)

from htmlentitydefs import name2codepoint as n2cp

class CTVException(Exception):
    pass

class ParseException(Exception):
    pass


class URLParser(object):
    """
    Unused, incomplete replacement for transform_stream_url
    """

    url_re = re.compile(r"(?P<scheme>\w+)://(?P<netloc>[\w\d\-\.\:]+)/(?P<app>\w+)/(?P<playpath>[^\?]+)(?:\?(?P<querystring>.*))?")

    def __init__(self, swf_url=None, swf_verify=False, \
                 force_rtmp=False, playpath_qs=True, 
                 is_live=False):

        self.swf_url = swf_url
        self.swf_verify = swf_verify
        self.force_rtmp = force_rtmp
        self.playpath_qs=playpath_qs
        self.is_live = is_live

    def __call__(self, url):
        self.input_url = url
        self.parse()
        self.clean()
        self.generate_url()
        return self.output_url

    def parse(self):
        match = self.url_re.match(self.input_url)
        if not match:
            raise ParseException("Couldn't parse input url: %s" % (self.input_url, ))        
        self.data = match.groupdict()    

    def clean_scheme(self, scheme):
        if scheme == 'rtmpe' and self.force_rtmp:
            scheme = 'rtmp'
        return scheme

    def clean_app(self, app):
        if 'live' in app:
            self.is_live = True
        return app

    def clean_playpath(self, playpath):
        basename, extension = os.path.splitext(playpath)

        if extension.lower() in ('.flv',''):
            playpath = basename
        else:
            if ':' in basename:
                playpath = "%s%s" % (basename, extension)
            else:
                playpath = "%s:%s%s" % (extension[1:], basename, extension)

        if self.playpath_qs and self.data['querystring']:
            playpath += "?%(querystring)s" % self.data

        return playpath

    def clean(self):        
        for key in ('querystring', 'playpath', 'scheme', 'netloc', 'app'):
            cleanfunc = getattr(self, 'clean_%s' % (key,), lambda v: v)
            self.data[key] = cleanfunc(self.data[key])            

    def get_base_url(self):
        print self.data
        #url = "%(scheme)s://%(netloc)s/%(app)s?ovpfv=2.1.4" % self.data
        url = "%(scheme)s://%(netloc)s/%(app)s/" % self.data
        if self.data['querystring']:
            url += "&%(querystring)s" % self.data
        return url

    def get_url_params(self):
        params = [('playpath', self.data['playpath']),]

        if self.swf_url:
            params.append(('swfurl', self.swf_url))

        if self.swf_verify:
            params.append(('swfvfy','true'))

        if self.is_live:
            params.append(('live','true'))

        return params


    def generate_url(self):
        base_url = self.get_base_url()

        params = self.get_url_params()
        if params:
            base_url += " %s" % (" ".join(["%s=%s" % item for item in params]))
        self.output_url = base_url


class TestParser(URLParser):
    def clean_netloc(self, netloc):
        if 'edgefcs.net' in netloc:
            return 'r11111.edgefcs.net'
        return netloc

def transform_stream_url(url, swf_url=None, playpath_qs=True):
    logging.debug("ORIGINAL URL: %s"%(url,))
    if swf_url:
        swf_url = 'swfurl=%s swfvfy=true' % (swf_url,)
    else:
        swf_url = ''

    match = re.match(r"rtmp(?P<rtmpe>e?)://(?P<netloc>[\w\d\.]+)/(?P<live_od>(?:\w+))/(?P<path>[^\?]+)(?:\?(?P<querystring>.*))?", url)
    parts = dict(match.groupdict())
    if "." in parts['path']:
        parts['extension'] = parts['path'].rsplit(".",1)[-1].lower()
    else:
        parts['extension'] = ''

    parts['path'] = parts['path'].rsplit(".",1)[0]
    parts['swfurl'] = swf_url
    parts['amp'] = '&'
    parts['q'] = '?'


    if 'querystring' not in parts or not parts['querystring']:
        parts['querystring'] = ''
        parts['amp'] = ''
        parts['q'] = ''

    if parts['extension'] == 'mp4':
        res = "rtmp%(rtmpe)s://%(netloc)s/%(live_od)s/?ovpfv=2.1.4%(amp)s%(querystring)s playpath=%(extension)s:%(path)s.%(extension)s %(swfurl)s" % parts
    else:
        if playpath_qs:
            res = "rtmp%(rtmpe)s://%(netloc)s/%(live_od)s/?ovpfv=2.1.4%(amp)s%(querystring)s playpath=%(path)s%(q)s%(querystring)s %(swfurl)s" % parts
        else:
            res = "rtmp%(rtmpe)s://%(netloc)s/%(live_od)s/?ovpfv=2.1.4%(amp)s%(querystring)s playpath=%(path)s %(swfurl)s" % parts


    if parts['live_od'] == 'live':
        res += " live=true"

    return res


def dequote(s):
    if s[0] in ('"', "'") and s[0] == s[-1]:
        s = s[1:-1].replace('\\' + s[0], s[0])
        return s
    else:
        try:
            return int(s)
        except:
            try:
                return float(s)
            except:
                return s


def parse_javascript_object(objs):
    PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
    pairs = [p.strip().split(":", 1) for p in PATTERN.split(objs) if p.strip() and p.strip() != ',']
    return dict([(k, dequote(v)) for k, v in pairs])


def qasplit(chars, sep=",", quote="'"):
    """ 
    Quote aware split 
    """
    if sep == quote:
        raise Exception("sep and quote cannot be the same character")

    can_split = True
    splitpoints = [-1]
    last_c = None
    for index, c in enumerate(chars):
        if c == quote and last_c != "\\":
            can_split = not can_split

        elif c == sep and can_split:
            splitpoints.append(index)
        last_c = c
    if not can_split:
        raise ValueError("Unterminated quote")

    splitpoints.append(len(chars))

    slices = [chars[splitpoints[i]+1:splitpoints[i+1]] for i in range(len(splitpoints)-1)]
    return slices


def parse_bad_json(json):
    """
    This is currently only used by CTV, it parses Javascript objects
    written in javascript (but not valid json):
    for example: "{IsTrue: true, myName: "Something", otherKey: null}"

    """
    pairs = qasplit(json.lstrip(" {").rstrip("} "))
    data = {}
    for pair in pairs:
        key, value = [t.strip() for t in pair.split(":",1)]
        if value.isdigit():
            value = int(value)
        elif "." in value:
            try:
                value = float(value)
            except (ValueError,TypeError):
                pass

        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        elif value == 'true':
            value = True
        elif value == 'false':
            value = False
        elif value == 'null':
            value = None

        if isinstance(value, basestring):

            value = decode_htmlentities(value).replace(r"\'", r"'")

        data[key] = value

    return data




def substitute_entity(match):
    """
    used by decode_htmlentities.

    """
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()


def decode_htmlentities(string):
    """
    replace &quot; &amp; and all other
    html entity codes.

    """
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]

def unescape(text):
    """Removes HTML or XML character references 
       and entities from a text string.
       keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                print "erreur de valeur"
                pass
        else:
            # named entity
            try:
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    print text[1:-1]
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                print "keyerror"
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
def get_page(url, retry_limit=4):
    """
    fetch a url, damnit.

    """

    retries = 0

    while retries < retry_limit:
        logging.debug("fetching %s" % (url,))
        try:            
            return urllib2.urlopen(url)
        except (urllib2.HTTPError, urllib2.URLError), e:
            retries += 1
    raise CTVException("Failed to retrieve page: %s" %(url,))


def get_soup(url, *args, **kwargs):
    return BeautifulSoup(get_page(url, *args, **kwargs), convertEntities=BeautifulSoup.HTML_ENTITIES)

def get_stone_soup(url):
    return BeautifulStoneSoup(get_page(url))


def urlquoteval(string):
    """ 
    encodes a querystring (or portion) (mostly space to %20)
    """
    return urllib.quote(string)

def urldecode(query):
    """
    parses querystrings

    """
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k,v = map(urllib.unquote_plus, s.split('='))
            if v == 'None':
                v = None
            d[k] = v
    return d

def get_classes(element):
    """
    pull a list of all the css classes on a beautifulsoup element.
    """
    return re.split(r'\s+', element['class'])
