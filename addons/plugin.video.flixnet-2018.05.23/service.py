# -*- coding: utf-8 -*-

"""
    flixnet Addon

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

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    ModuleVersion = control.addon('script.module.flixnet').getAddonInfo('version')
    AddonVersion = control.addon('plugin.video.flixnet').getAddonInfo('version')
    # RepoVersion = control.addon('repository.jesusboxtv').getAddonInfo('version')

    log_utils.log('######################### flixnet ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT flixnet VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### flixnet PLUGIN VERSION: %s ###' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('### flixnet SCRIPT VERSION: %s ###' % str(ModuleVersion), log_utils.LOGNOTICE)
    # log_utils.log('### jesus Box TV REPOSITORY VERSION: %s ###' % str(RepoVersion), log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
except:
    log_utils.log('######################### flixnet ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT flixnet VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### ERROR GETTING flixnet VERSIONS - NO HELP WILL BE GIVEN AS THIS IS NOT AN OFFICIAL flixnet INSTALL. ###', log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
