"""
 Copyright (c) 2010, 2011, 2012 Popeye

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import locale
import urllib2
import utils

WIN32 = (sys.platform == 'win32')
DARWIN = sys.platform.startswith('darwin')

class Nzbname:
    def __init__(self,nzbname):
        # Modified from SABnzbd /sabnzbd/nzbstuff.py
        self.original = nzbname
        #work_name = platform_encode(nzbname)
        work_name = nzbname
        # If non-future: create safe folder name stripped from ".nzb" and junk
        if work_name and (work_name.lower().endswith('.nzb') or \
                          work_name.lower().endswith('.nzb.gz') or \
                          work_name.lower().endswith('.nzb.zip')):
            dname, ext = os.path.splitext(work_name) # Used for folder name for final unpack
            if ext.lower() == '.gz' or ext.lower() == '.zip':
                work_name = dname
            dname, ext = os.path.splitext(work_name) # Used for folder name for final unpack
            if ext.lower() == '.nzb':
                work_name = dname
        work_name = sanitize_foldername(work_name)
        self.final_name = work_name

# From SABnzbd /sabnzbd/encoding.py
def platform_encode(p):
    """ Return the correct encoding for the platform:
        Latin-1 for Windows/Posix-non-UTF and UTF-8 for OSX/Posix-UTF
    """
    try:
        if DARWIN:
            UTF = True
        else:
            UTF = locale.getdefaultlocale()[1].lower().find('utf') >= 0
    except:
        # Incorrect locale implementation, assume the worst
        UTF = False
    if isinstance(p, unicode):
        if UTF:
            return p.encode('utf-8')
        else:
            return p.encode('latin-1', 'replace')
    elif isinstance(p, basestring):
        if UTF:
            try:
                p.decode('utf-8')
                return p
            except:
                return p.decode('latin-1').encode('utf-8')
        else:
            try:
                return p.decode('utf-8').encode('latin-1', 'replace')
            except:
                return p
    else:
        return p

# Modified from SABnzbd /sabnzbd/misc.py
if WIN32:
    # the colon should be here too, but we'll handle that separately
    CH_ILLEGAL = r'\/<>?*|"'
    CH_LEGAL   = r'++{}!@#`'
else:
    CH_ILLEGAL = r'/'
    CH_LEGAL   = r'+'

def sanitize_filename(name):
    """ Return filename with illegal chars converted to legal ones
        and with the par2 extension always in lowercase
    """
    if not name:
        return name
    illegal = CH_ILLEGAL
    legal   = CH_LEGAL

    if ':' in name:
        if WIN32:
            # Compensate for the odd way par2 on Windows substitutes a colon character
            name = name.replace(':', '3A')
        elif DARWIN:
            # Compensate for the foolish way par2 on OSX handles a colon character
            name = name[name.rfind(':')+1:]
    lst = []
    for ch in name.strip():
        if ch in illegal:
            ch = legal[illegal.find(ch)]
        lst.append(ch)
    name = ''.join(lst)

    if not name:
        name = 'unknown'

    name, ext = os.path.splitext(name)
    lowext = ext.lower()
    if lowext == '.par2' and lowext != ext:
        ext = lowext
    return name + ext

FL_ILLEGAL = CH_ILLEGAL + ':\x92"'
FL_LEGAL   = CH_LEGAL +   "-''"
uFL_ILLEGAL = FL_ILLEGAL.decode('latin-1')
uFL_LEGAL   = FL_LEGAL.decode('latin-1')

def sanitize_foldername(name):
    """ Return foldername with dodgy chars converted to safe ones
        Remove any leading and trailing dot and space characters
    """
    if not name:
        return name
    if isinstance(name, unicode):
        illegal = uFL_ILLEGAL
        legal   = uFL_LEGAL
    else:
        illegal = FL_ILLEGAL
        legal   = FL_LEGAL

    # repl = cfg.replace_illegal()
    repl = True
    lst = []
    for ch in name.strip():
        if ch in illegal:
            if repl:
                ch = legal[illegal.find(ch)]
                lst.append(ch)
        else:
            lst.append(ch)
    name = ''.join(lst)

    name = name.strip('. ')
    if not name:
        name = 'unknown'

    if WIN32:
        maxlen = 128
    else:
        maxlen = 256

    if len(name) > maxlen:
        name = name[:maxlen]

    return name

def save(url, nzb_path):
    file, e = _load_nzb(url)
    if e is None:
        try:
            utils.write(nzb_path, file, 'wb')
        except:
            e = "Pneumatic failed writing %s" % nzb_path
        else:
            e = "Pneumatic saved %s" % nzb_path
    print e
    return

def _load_nzb(url):
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, ex:
        if hasattr(ex, 'reason'):
            print ex.reason
            e = ex.reason
            return None, e
        elif hasattr(ex, 'code'):
            e = ex.code + " " + url
            return None, e
    else:
        doc = response.read()
        response.close()
        return doc, None
    