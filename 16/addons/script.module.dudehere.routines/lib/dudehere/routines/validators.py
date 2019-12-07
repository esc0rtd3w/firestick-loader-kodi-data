from dudehere.routines import plugin


'''*  	Validation functions 
		
		These functions are passed to some of the menu or context menu entries
		where needed. Trakt authorization dependent functions are passed validate_trakt
		for example, which simply checks to see if trakt as been authorized.
		A dependent menu would then be visible or hidden based on the result.
		This could be more complicated in the future. 

*'''

def validate_advanced():
	return plugin.get_setting('advanced_mode') == 'true'

def validate_walter():
	installed = plugin.get_condition_visiblity('System.HasAddon(service.walter.sobchak)') == 1
	if validate_advanced() and installed:
		return True
	else:
		return False

def validate_trakt():
	return plugin.get_setting('trakt_authorized') == "true"

def validate_default_views():
	return ( plugin.get_setting('enable_default_views') == "true" and validate_advanced() )

def validate_transmogrifier():
	installed = plugin.get_condition_visiblity('System.HasAddon(service.transmogrifier)') == 1
	if installed:
		return plugin.get_setting('enable_transmogrifier') == "true" and validate_advanced()
	else:
		return False

def validate_transmogrifier_streaming():
	if validate_transmogrifier() and plugin.get_setting('enable_transmogrifier_streaming') == "true":
		return True
	else:
		return False

def validate_watched():
	if plugin.get_setting('trakt_authorized') == "false" or plugin.get_setting('advanced_mode') == "false":
		return False
	return plugin.get_setting('hide_watched_episodes') == "true"

def validate_calendar_browser():
	if validate_advanced() is False or validate_trakt() is False: return False
	return plugin.get_setting('enable_calendar_browser') == "true"

def validate_ondeck():
	if validate_advanced() is False or validate_trakt() is False: return False
	return plugin.get_setting('enable_episodes_ondeck') == "true"	

def validate_transmogrifier_streaming():
	if validate_transmogrifier() and plugin.get_setting('enable_transmogrifier_streaming') == "true":
		return True
	else:
		return False

def validate_source_filter():
	return validate_advanced() and plugin.get_setting('enable_result_filters') == 'true'

def validate_default_views():
	return plugin.get_setting('enable_default_views') == "true"

def validate_show_settings():
	return plugin.get_setting('enable_full_context') != "true"

def validate_fanart():
	return plugin.get_setting('enable_fanart') == "true"

def validate_show_fanart():
	return validate_fanart() and plugin.get_setting('enable_series_fanart') == "true"

def validate_movie_fanart():
	return validate_fanart() and plugin.get_setting('enable_movie_fanart') == "true"




