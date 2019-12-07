"""
 Copyright (c) 2013 Popeye

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

import action
import page
from resources.lib import sabutils
from resources.lib.sabnzbd import Sabnzbd
import sys
import xbmc
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.program.sabnzbd')
__language__ = __settings__.getLocalizedString

if (__name__ == "__main__" ):
    sabutils.log('v%s started' % __settings__.getAddonInfo("version"), xbmc.LOGNOTICE)
    HANDLE = int(sys.argv[1])
    if not (__settings__.getSetting("firstrun")):
        __settings__.openSettings()
        if sabutils.pass_setup_test(Sabnzbd().self_test()):
            __settings__.setSetting("firstrun", '1')
    else:
        if (not sys.argv[2]):
            page.Page().page_main()
        else:
            params = sabutils.get_parameters(sys.argv[2])
            get = params.get
            mode = get("mode")
            if mode.startswith("page_"):
                getattr(page.Page(**params), mode)()
            if mode.startswith("dialog_"):
                getattr(page.Dialog(**params), mode)()
            if mode.startswith("nzo_"):
                getattr(action.NzoAction(**params), mode)()
            if mode.startswith("nzf_"):
                getattr(action.NzfAction(**params), mode)()
            if mode.startswith("sab_"):
                getattr(action.SabAction(**params), mode)()
