"""
    Copyright (C) 2016 ECHO Wizard

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
import xbmcgui
import urllib
import time
from urllib import FancyURLopener
import sys

class MyOpener(FancyURLopener):
	version = 'python-requests/2.9.1'

myopener = MyOpener()
urlretrieve = MyOpener().retrieve
urlopen = MyOpener().open
AddonTitle     = "[COLOR red]XXX-O-DUS[/COLOR]"

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle,"Download In Progress",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(dest,nb, bs, fs, dp, start_time))

def auto(url, dest, dp = None):
	dp = xbmcgui.DialogProgress()
	start_time=time.time()
	urlretrieve(url, dest, lambda nb, bs, fs: _pbhookauto(nb, bs, fs, dp, start_time))

def _pbhookauto(numblocks, blocksize, filesize, url, dp):
	none = 0

def _pbhook(dest,numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR pink]%.02f MB[/COLOR] of [B]%.02f MB[/B]' % (currently_downloaded, total)
            e = '[COLOR white][B]Speed: [/B][/COLOR][COLOR pink]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            e += '[COLOR white][B]ETA: [/B][/COLOR][COLOR pink]%02d:%02d' % divmod(eta, 60)  + '[/COLOR]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dp.close()
            quit()