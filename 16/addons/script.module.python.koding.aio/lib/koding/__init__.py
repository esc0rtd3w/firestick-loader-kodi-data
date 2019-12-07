# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by TOTALREVOLUTION LTD (support@trmc.freshdesk.com)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. If you're found to be in breach of this license
# then any affected add-ons will be blacklisted and will not be able to work on the same system
# as any other add-ons which use this code. Thank you for your cooperation.

import os
import re
import shutil
import sys
import time
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import inspect
try:
    import simplejson as json
except:
    import json

from addons         import *
from android        import *
from database       import *
from directory      import *
from filetools      import *
from guitools       import *
from router         import *
from systemtools    import *
from tutorials      import *
from video          import *
from vartools       import *
from web            import *

def converthex(url):
    """ internal command ~"""
    import binascii
    return binascii.unhexlify(url)

try:
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
except:
    ADDON_ID = Caller()

AddonVersion = xbmcaddon.Addon(id=ADDON_ID).getAddonInfo('version')
ORIG_ID      = ADDON_ID

TestID           =  ADDON_ID
if not ADDON_ID.endswith(converthex('2e74657374')):
    TestID       =  ADDON_ID+converthex('2e74657374')

MODULE_ID        =  'script.module.python.koding.aio'
ADDON            =  xbmcaddon.Addon(id=ADDON_ID)
THIS_MODULE      =  xbmcaddon.Addon(id=MODULE_ID)
USERDATA         =  'special://profile'
ADDON_DATA       =  os.path.join(USERDATA,'addon_data')
ADDONS           =  'special://home/addons'
PACKAGES         =  os.path.join(ADDONS,'packages')
UPDATE_ICON      =  os.path.join(ADDONS,MODULE_ID,'resources','update.png')
DEBUG            =  Addon_Setting(addon_id=ORIG_ID,setting=converthex('6465627567'))
KODI_VER         =  int(float(xbmc.getInfoLabel("System.BuildVersion")[:2]))

dialog           =  xbmcgui.Dialog()
dp               =  xbmcgui.DialogProgress()

if not xbmcvfs.exists(os.path.join(ADDON_DATA,ORIG_ID,'cookies')):
    xbmcvfs.mkdirs(os.path.join(ADDON_DATA,ORIG_ID,'cookies'))
#----------------------------------------------------------------
# TUTORIAL #
def dolog(string, my_debug=False, line_info=False):
    """
Print to the Kodi log but only if debugging is enabled in settings.xml

CODE: koding.dolog(string, [my_debug])

AVAILABLE PARAMS:

    (*) string  -  This is your text you want printed to log.

    my_debug  -  This is optional, if you set this to True you will print
    to the log regardless of what the debug setting is set at in add-on settings.

    line_info - By default this is set to True and will show the line number where
    the dolog command was called from along with the filepath it was called from.

EXAMPLE CODE:
koding.dolog(string='Quick test to see if this gets printed to the log', my_debug=True, line_info=True)
dialog.ok('[COLOR gold]CHECK LOGFILE 1[/COLOR]','If you check your log file you should be able to see a new test line we printed \
and immediately below that should be details of where it was called from.')
koding.dolog(string='This one should print without the line and file info', my_debug=True, line_info=False)
dialog.ok('[COLOR gold]CHECK LOGFILE 2[/COLOR]','If you check your log file again you should now be able to see a new line printed \
but without the file/line details.')
~"""
    import xbmc
    if DEBUG == 'true' or my_debug:
        try:
            xbmc.log('### %s (%s) : %s'%(ADDON_ID,AddonVersion,string), level=xbmc.LOGNOTICE)
        except:
            xbmc.log(Last_Error(),level=xbmc.LOGNOTICE)
    if line_info:
        try:
            from inspect import getframeinfo, stack
            caller = getframeinfo(stack()[1][0])
            xbmc.log('^ Line No. %s  |  File: %s'%(caller.lineno,caller.filename),level=xbmc.LOGNOTICE)
        except:
            xbmc.log(Last_Error(),level=xbmc.LOGNOTICE)