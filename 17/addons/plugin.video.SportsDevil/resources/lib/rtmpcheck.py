import xbmc
import xbmcgui
import xbmcaddon
import json

##############################################################
#                                                            #
#                                                            #
#			from script.module.drmhelper                     #
#				ausieaddons                                  #
# 					by glennguy                              #
#                                                            #
##############################################################



def get_addon(wtyk="inputstream.rtmp"):
    """
    Check if inputstream is installed, attempt to install if not.
    Enable inpustream addon.
    """
    addon = None

    try:
        enabled_json = ('{"jsonrpc":"2.0","id":1,"method":'
                        '"Addons.GetAddonDetails","params":'
                        '{"addonid":"%s", '
                        '"properties": ["enabled"]}}'%wtyk)
        result = json.loads(xbmc.executeJSONRPC(enabled_json))
    except RuntimeError:
        return False

    if 'error' in result:  # not installed
        try:  # see if there's an installed repo that has it
            xbmc.executebuiltin('InstallAddon(%s)'%wtyk, True)
            addon = xbmcaddon.Addon('%s'%wtyk)
            return addon
        except RuntimeError:
            xbmcgui.Dialog().ok('%s not installed'%wtyk,
                                '%s not installed. This '
                                'addon now comes supplied with newer builds '
                                'of Kodi 18 for Windows/Mac/LibreELEC/OSMC, '%wtyk)
        return False

    else:  # installed but not enabled. let's enable it.
        if result['result']['addon'].get('enabled') is False:
            json_string = ('{"jsonrpc":"2.0","id":1,"method":'
                           '"Addons.SetAddonEnabled","params":'
                           '{"addonid":"%s",'
                           '"enabled":true}}'%wtyk)
            try:
                xbmc.executeJSONRPC(json_string)
            except RuntimeError:
                xbmcgui.Dialog().ok('Unable to enable %s'%wtyk,
                                    'Unable to enable %s, '
                                    'please try to enable manually '
                                    'and try again'%wtyk)
                return False
        addon = xbmcaddon.Addon('%s'%wtyk)

    return addon

def disable_addon(wtyk="inputstream.rtmp"):
	addon=None
	json_string = ('{"jsonrpc":"2.0","id":1,"method":'
				'"Addons.SetAddonEnabled","params":'
				'{"addonid":"%s",'
				'"enabled":false}}'%wtyk)
	try:
		xbmc.executeJSONRPC(json_string)
		#xbmcgui.Dialog().ok('Disabled','%s is disabled'%wtyk)
	except RuntimeError:
		xbmcgui.Dialog().ok('Unable to disable %s'%wtyk,
							'Unable to disable %s, '
							'please try to disable manually '
							'and try again'%wtyk)
		return False

	return addon
