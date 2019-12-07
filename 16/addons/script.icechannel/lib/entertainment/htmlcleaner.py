#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 HTMLCLEANER
 A bastardised version of html2text, only retaining the entity cleaner.

 What does it do?
 Replaces annoying characters like &#x27;

 USAGE:
 import htmlcleaner
 cleanedhtml = htmlcleaner.clean(my-html-string, strip=False)
 print cleanedhtml

 if strip = True, é will be replaced with e and so on.
"""

__version__ = "1.0"
__author__ = "Anarchintosh  (@xbmcforums)"
__copyright__ = "Copyleft 2011 onwards  GNU GPL 3."
__contributors__ = ["Aaron Swartz", "Martin 'Joey' Schulze", "Ricardo Reyes", "Kevin Jay North"]

try:
    True
except NameError:
    setattr(__builtins__, 'True', 1)
    setattr(__builtins__, 'False', 0)

def has_key(x, y):
    if hasattr(x, 'has_key'): return x.has_key(y)
    else: return y in x

try:
    import htmlentitydefs
except ImportError: #Python3
    import html.entities as htmlentitydefs

import re, codecs, unicodedata

try: from textwrap import wrap
except: pass

# Use Unicode characters instead of their ascii psuedo-replacements
UNICODE_SNOB = 1

### Entity Nonsense ###

def name2cp(k):
    if k == 'apos': return ord("'")
    if hasattr(htmlentitydefs, "name2codepoint"): # requires Python 2.3
        return htmlentitydefs.name2codepoint[k]
    else:
        k = htmlentitydefs.entitydefs[k]
        if k.startswith("&#") and k.endswith(";"): return int(k[2:-1]) # not in latin-1
        return ord(codecs.latin_1_decode(k)[0])

unifiable = {'rsquo':"'", 'lsquo':"'", 'rdquo':'"', 'ldquo':'"', 
'copy':'(C)', 'mdash':'--', 'nbsp':' ', 'rarr':'->', 'larr':'<-', 'middot':'*',
'ndash':'-', 'oelig':'oe', 'aelig':'ae',
'agrave':'a', 'aacute':'a', 'acirc':'a', 'atilde':'a', 'auml':'a', 'aring':'a', 
'egrave':'e', 'eacute':'e', 'ecirc':'e', 'euml':'e', 
'igrave':'i', 'iacute':'i', 'icirc':'i', 'iuml':'i',
'ograve':'o', 'oacute':'o', 'ocirc':'o', 'otilde':'o', 'ouml':'o', 
'ugrave':'u', 'uacute':'u', 'ucirc':'u', 'uuml':'u'}

unifiable_n = {}

for k in unifiable.keys():
    unifiable_n[name2cp(k)] = unifiable[k]

def charref(name):
    if name[0] in ['x','X']:
        c = int(name[1:], 16)
    else:
        c = int(name)
    
    if not UNICODE_SNOB and c in unifiable_n.keys():
        return unifiable_n[c]
    else:
        try:
            return unichr(c)
        except NameError: #Python3
            return chr(c)

def entityref(c):
    if not UNICODE_SNOB and c in unifiable.keys():
        return unifiable[c]
    else:
        try: name2cp(c)
        except KeyError: return "&" + c + ';'
        else:
            try:
                return unichr(name2cp(c))
            except NameError: #Python3
                return chr(name2cp(c))

def replaceEntities(s):
    s = s.group(1)
    if s[0] == "#":
        return charref(s[1:])
    elif s.startswith('u') or s.startswith('U'):
        return charref('x' + s[1:])
    else: return entityref(s)

r_unescape = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")
r_unescape_unicode = re.compile(r"\\([uU]{1}[0-9a-fA-F]{4})")
def unescape(s):
    
    html_has_unicode = False
    if '\\u' in s or '\\U' in s: html_has_unicode = True
    
    s = r_unescape.sub(replaceEntities, s)
    
    if html_has_unicode:
        s = r_unescape_unicode.sub(replaceEntities, s)

    return s
### End Entity Nonsense ###

def cleanUnicode(string):   
    try:
        try:
            #string = str(string)
            if isinstance(string, unicode):
                unicode_replaced_str = string.decode('utf-8')
            elif isinstance(string, str):
                unicode_replaced_str = string.decode('utf-8')
            import unidecode
            unicode_replaced_str = unidecode.unidecode(unicode_replaced_str)
            string = unicode_replaced_str
            
        except:
            pass
        
        fixed_string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore' )    
        return fixed_string
    except:
        return string
        
#interface:

def clean(html,strip=False,remove_non_ascii=False):
    cleaned = unescape(html)
    if remove_non_ascii:
        cleaned = re.sub(r'[^\x00-\x7F]+',' ', cleaned)
    if strip == True:
        return cleanUnicode(cleaned)
    else:
        return cleaned

def clean2(html,strip=False,remove_non_ascii=False):
    cleaned = unescape(html)    
    if strip == True:
        cleaned = cleanUnicode(cleaned)
    if remove_non_ascii:
        return re.sub(r'[^\x00-\x7F]+',' ', cleaned)
    else:
        return cleaned
