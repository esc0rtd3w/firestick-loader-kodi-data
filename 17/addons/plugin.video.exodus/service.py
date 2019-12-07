# -*- coding: utf-8 -*-

"""
    Exodus Add-on

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
from resources.lib.modules import log_utils
from resources.lib.modules import control
import threading

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

#addon_settings = xbmc.translatePath('special://userdata/addon_data/plugin.video.exodus/settings.xml')
#run2 = control.setting('first.info2')
#if run2 == '': run2 = 'true' #clean install scenerio
#if run2 == 'true':
#    import os
#    if os.path.exists(xbmc.translatePath(addon_settings)):
#        control.deleteFile(addon_settings)
#    control.setSetting(id='first.info2', value='false')

def syncTraktLibrary():
    control.execute(
        'RunPlugin(plugin://%s)' % 'plugin.video.exodus/?action=tvshowsToLibrarySilent&url=traktcollection')
    control.execute(
        'RunPlugin(plugin://%s)' % 'plugin.video.exodus/?action=moviesToLibrarySilent&url=traktcollection')

try:
    ModuleVersion = control.addon('script.module.exodus').getAddonInfo('version')
    AddonVersion = control.addon('plugin.video.exodus').getAddonInfo('version')

    log_utils.log('######################### EXODUS ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT EXODUS VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### EXODUS PLUGIN VERSION: %s ###' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('### EXODUS SCRIPT VERSION: %s ###' % str(ModuleVersion), log_utils.LOGNOTICE)
    #log_utils.log('### EXODUS REPOSITORY VERSION: %s ###' % str(RepoVersion), log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
except:
    log_utils.log('######################### EXODUS ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT EXODUS VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### ERROR GETTING EXODUS VERSIONS - NO HELP WILL BE GIVEN AS THIS IS NOT AN OFFICIAL EXODUS INSTALL. ###', log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)

if control.setting('autoTraktOnStart') == 'true':
    syncTraktLibrary()

if int(control.setting('schedTraktTime')) > 0:
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
    log_utils.log('#################### STARTING TRAKT SCHEDULING ################', log_utils.LOGNOTICE)
    log_utils.log('#################### SCHEDULED TIME FRAME '+ control.setting('schedTraktTime')  + ' HOURS ################', log_utils.LOGNOTICE)
    timeout = 3600 * int(control.setting('schedTraktTime'))
    schedTrakt = threading.Timer(timeout, syncTraktLibrary)
    schedTrakt.start()
