"""
    urlresolver XBMC Addon
    Copyright (C) 2013 Bstrdsmkr

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

    Adapted for use in xbmc from:
    https://github.com/einars/js-beautify/blob/master/python/jsbeautifier/unpackers/packer.py
    
    usage:

    if detect(some_string):
        unpacked = unpack(some_string)


Unpacker for Dean Edward's p.a.c.k.e.r
"""

import re
import string

def detect(source):
    """Detects whether `source` is P.A.C.K.E.R. coded."""
    source = source.replace(' ','')
    if re.search('eval(function(p,a,c,k,e,(?:r|d)'): return True
    else: return False

def unpack(source):
    """Unpacks P.A.C.K.E.R. packed js code."""
    payload, symtab, radix, count = _filterargs(source)

    if count != len(symtab):
        raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

    try:
        unbase = Unbaser(radix)
    except TypeError:
        raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

    def lookup(match):
        """Look up symbols in the synthetic symtab."""
        word  = match.group(0)
        return symtab[unbase(word)] or word

    source = re.sub(r'\b\w+\b', lookup, payload)
    return _replacestrings(source)

def _filterargs(source):
    """Juice from a source file the four args needed by decoder."""
    argsregex = (r"}\('(.*)', *(\d+), *(\d+), *'(.*?)'\.split\('\|'\)")
    args = re.search(argsregex, source, re.DOTALL).groups()

    try:
        return args[0], args[3].split('|'), int(args[1]), int(args[2])
    except ValueError:
        raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

def _replacestrings(source):
    """Strip string lookup table (list) and replace values in source."""
    match = re.search(r'var *(_\w+)\=\["(.*?)"\];', source, re.DOTALL)

    if match:
        varname, strings = match.groups()
        startpoint = len(match.group(0))
        lookup = strings.split('","')
        variable = '%s[%%d]' % varname
        for index, value in enumerate(lookup):
            source = source.replace(variable % index, '"%s"' % value)
        return source[startpoint:]
    return source


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET  = {
        64 : '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/',
        95 : (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
              '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base

        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for
                    index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                try:
                    self.dictionary = dict((cipher, index) for
                        index, cipher in enumerate(self.ALPHABET[64][:base]))
                except KeyError:
                    raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0
        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret

class UnpackingError(Exception):
    """Badly packed source or general error. Argument is a
    meaningful description."""
    pass


if __name__ == "__main__":
    test='''eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('a(\'c\').q({\'p\':\'0://c.9.1/o.8.n\',\'r\':\'0://m.3-6.1/3/v.u\',\'t\':\'0://d.3-6.1/7/w/j/3/h.g\',\'f\':\'0://i.9.1/7/l/e/5/e.k\',\'s\':\'H\',\'M\':\'0\',\'0.L\':\'x\',\'J\':\'O\',\'Q\':\'R\',\'P\':\'N\',\'I\':{\'B-2\':{}}});A 4=b;a().z(y(){C(4==b)$.D(\'/G.F\',{E:\'0://d.3-6.1\'});4=K});',54,54,'http|com||2gb|played||hosting|files||longtailvideo|jwplayer|false|player|gb3|bekle|skin|flv|af91fdbb64843b3|www|5186ad24|zip|skins|images|swf|player5|flashplayer|setup|image|stretching|file|jpg|4980e8c81d49a6b|20a43863f0fdac56f8fa6733484a0bde|start|function|onPlay|var|timeslidertooltipplugin|if|post|server|php|track|exactfit|plugins|controlbar|true|startparam|provider|350|bottom|height|width|620'.split('|'),0,{}))'''
    print unpack(test)
 
