import copy
import urllib
import time
import re
from urlparse import urlparse, parse_qs, urlunparse

# from xml.sax.saxutils import unescape as xml_unescape

ACTION_REGEX = re.compile("(.*?)\((.*)\)")

def page_redux(page):
    pages  = []
    if "|" in page: prepages = page.split("|")
    else: prepages = [page]
    ranges = []
    for p in prepages:
        if "-" in p: ranges = ranges + [i for i in range(int(p.split("-")[0]),int(p.split("-")[1])+1) if i not in pages and i not in ranges]
        else:
            if p not in pages: pages.append(int(p))
    if len(pages) < 1: return None
    else: return pages + ranges

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args: result.update(dictionary)
    return result

def to_utf8(obj):
    if isinstance(obj, unicode):
        obj = obj.encode('utf-8', 'ignore')

    elif isinstance(obj, dict):
        obj = copy.deepcopy(obj)
        for key, val in obj.items():
            obj[key] = to_utf8(val)

    elif obj is not None and hasattr(obj, "__iter__"):
        obj = obj.__class__([to_utf8(x) for x in obj])

    else:
        pass

    return obj


def to_unicode(obj):
    if isinstance(obj, basestring):
        try:
            obj = unicode(obj, 'utf-8')
        except TypeError:
            pass

    elif isinstance(obj, dict):
        obj = copy.deepcopy(obj)
        for key, val in obj.items():
            obj[key] = to_unicode(val)

    elif obj is not None and hasattr(obj, "__iter__"):
        obj = obj.__class__([to_unicode(x) for x in obj])

    else:
        pass

    return obj


def number_to_text(number_text):
    if not number_text.isnumeric():
        return number_text
    if number_text == "" or None:
        return ""
    else:
        number_text = int(number_text)
        numbers = [
            u"zero", u"one", u"two", u"three", u"four", u"five", u"six", u"seven", u"eight",
            u"nine", u"ten", u"eleven", u"twelve", u"thirteen", u"fourteen", u"fifteen",
            u"sixteen", u"seventeen", u"eighteen", u"nineteen"
        ]
        if number_text < 20:
            return numbers[number_text]
        else:
            return ""


def text_to_number(text):
    if text.isnumeric():
        return text
    if text == "" or None:
        return ""
    else:
        numbers = [
            u"zero", u"one", u"two", u"three", u"four", u"five", u"six", u"seven", u"eight",
            u"nine", u"ten", u"eleven", u"twelve", u"thirteen", u"fourteen", u"fifteen",
            u"sixteen", u"seventeen", u"eighteen", u"nineteen"
        ]
        numwords = {}
        for idx, word in enumerate(numbers):
            numwords[word] = idx
        if text.lower() in numwords:
            return numwords[text.lower()]
        else:
            return ""


def equals(a, b):
    return to_unicode(a) == to_unicode(b)

def contains(a, b):
    return to_unicode(a) in to_unicode(b)


def is_ascii(s):
    try:
        if isinstance(s, basestring):
            s.decode()
        return True
    except UnicodeDecodeError:
        pass
    except UnicodeEncodeError:
        pass
    return False


def urlencode_path(path):
    path = to_utf8(path)
    o = urlparse(path)
    query = parse_qs(o.query)
    path = urlunparse([o.scheme, o.netloc, o.path, o.params, urllib.urlencode(query, True), o.fragment])
    return path


def parse_year(text):
    try:
        return text.split("-")[0].strip()
    except:
        return '0'


def date_to_timestamp(date_str, format="%Y-%m-%d"):
    if date_str:
        try:
            tt = time.strptime(date_str, format)
            return int(time.mktime(tt))
        except:
            return 0  # 1970
    return None


def apply_text_actions(text, dictionary):
    def unescape(x):
        # x = xml_unescape(x)
        # x = x.strip()
        x = x.replace('&dot;', '.')
        x = x.replace('&sbo;', '[')
        x = x.replace('&sbc;', ']')
        x = x.replace('&colon;', ':')
        return x

    splitted_text = text.split('|')
    if splitted_text[0] in dictionary:
        value = dictionary.get(splitted_text[0])
        for action in splitted_text[1:]:
            match = ACTION_REGEX.match(action)
            if match:
                action, params = match.groups()
                params = [unescape(x) for x in params.split(',')]

                if action == "ws":
                    value = value.replace(' ', params[0])
                elif action == "replace":
                    value = value.replace(params[0], params[1])
                elif action == "text_to_number":
                    value = text_to_number(value)
                elif action == "number_to_text":
                    value = number_to_text(value)
                else:
                    pass
        return value

    return None


def apply_parameters(text, parameters):
    while True:
        try:
            text = text.format(**parameters)
        except KeyError, e:
            # Auto generate missing parameters if possible
            missing_key = e.args[0]
            new_val = apply_text_actions(missing_key, parameters)
            if new_val is not None:
                parameters = dict(parameters)
                parameters[missing_key] = new_val
            else:
                raise e
        else:
            return text
