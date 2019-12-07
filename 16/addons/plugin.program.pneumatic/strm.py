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

import urllib

from utils import log
import utils
import nzb as m_nzb

class StrmFile:
    def __init__(self, folder, nzbname, nzb):
        self.folder = folder
        self.nzbname = nzbname
        self.nzb = nzb

    def save(self):
        strm_path = utils.join(self.folder, ('%s.strm' % self.nzbname))
        nzb_path = utils.join(self.folder, ('%s.nzb' % self.nzbname))
        nzb = urllib.quote_plus(self.nzb)
        nzbname = urllib.quote_plus(self.nzbname)
        if utils.exists(strm_path):
            log("StrmFile: save: replacing .strm file: %s" % strm_path.encode("utf_8"))
        line = "plugin://plugin.program.pneumatic/?mode=strm&nzb=" + nzb +\
                       "&nzbname=" + nzbname
        try: 
            utils.write(strm_path, line, 'wb')
        except:
            log("StrmFile: save: failed to create .strm file: %s" % strm_path.encode("utf_8"))
        if utils.exists(nzb_path):
            log("StrmFile: save: replacing .nzb file: %s" % nzb_path.encode("utf_8"))
        m_nzb.save(self.nzb, nzb_path)
