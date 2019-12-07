# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: MuadDib

from resources.lib.modules import log_utils
from resources.lib.modules import control

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    ModuleVersion = control.addon('script.module.placenta').getAddonInfo('version')
    AddonVersion = control.addon('plugin.video.placenta').getAddonInfo('version')
    RepoVersion = control.addon('repository.blamo').getAddonInfo('version')

    log_utils.log('######################### PLACENTA ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT PLACENTA VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### PLACENTA PLUGIN VERSION: %s ###' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('### PLACENTA SCRIPT VERSION: %s ###' % str(ModuleVersion), log_utils.LOGNOTICE)
    log_utils.log('### TEAM REBIRTH REPOSITORY VERSION: %s ###' % str(RepoVersion), log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
except:
    log_utils.log('######################### PLACENTA ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT PLACENTA VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### ERROR GETTING PLACENTA VERSIONS - NO HELP WILL BE GIVEN AS YOU ARE EATING OUR AFTERBIRTH BITCHES. ###', log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)