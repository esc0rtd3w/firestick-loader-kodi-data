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

import xbmc

from utils import log

class XBMCPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        self.is_active = True
        self.is_playing = False
        self.is_ended = False
        self.is_stopped = False

    def onPlayBackStarted( self ):
        log("XBMCPlayer: onPlayBackStarted")
        self.is_playing = True

    def onPlayBackEnded( self ):
        log("XBMCPlayer: onPlayBackEnded")
        self.is_ended = True

    def onPlayBackStopped( self ):
        log("XBMCPlayer: onPlayBackStopped")
        self.is_stopped = True

    def sleep(self, s):
        xbmc.sleep(s)
