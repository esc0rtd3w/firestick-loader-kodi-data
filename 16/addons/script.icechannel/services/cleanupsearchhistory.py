from entertainment import common
import os
from entertainment import searchhistory

common._update_settings_xml()

#CLEANUP SEARCH HISTORY
service_py = 'cleanupsearchhistory.py'
default_sleep_duration = 300
common.addon.log('Search History Cleanup Service - Starting\\Waking...')

SH = searchhistory.SearchHistory()
SH.cleanup_search_history()

common.addon.log('Search History Cleanup Service - Sleeping... Sleep for %s mins' % str(default_sleep_duration) )
common.SetScriptOnAlarm('iStream-Cleanup-Search-History', os.path.join(common.addon_path, 'services', service_py), duration=default_sleep_duration)
