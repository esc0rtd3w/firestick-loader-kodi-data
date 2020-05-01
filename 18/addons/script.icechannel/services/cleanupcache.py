from entertainment import common
import os

common._update_settings_xml()

#CLEANUP CACHE
service_py = 'cleanupcache.py'
default_sleep_duration = 300
common.addon.log('Cache Cleanup Service - Starting\\Waking...')

from entertainment.net import Net
net = Net()
net.cleanup_cache()

common.addon.log('Cache Cleanup Service - Sleeping... Sleep for %s mins' % str(default_sleep_duration) )
common.SetScriptOnAlarm('iStream-Cleanup-Cache', os.path.join(common.addon_path, 'services', service_py), duration=default_sleep_duration)
