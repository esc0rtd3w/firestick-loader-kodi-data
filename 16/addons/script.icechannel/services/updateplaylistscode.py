from entertainment import common
import os

#UPDATE PLAYLISTS CODE
service_py = 'updateplaylistscode.py'
default_sleep_duration = 300
common.addon.log('Playlists Code Update Service - Starting\\Waking...')

from entertainment.filestore import FileStore
filestore = FileStore()
filestore.update_files()

common.addon.log('Playlists Code Update Service - Sleeping... Sleep for %s mins' % str(default_sleep_duration) )
common.SetScriptOnAlarm('iStream-Playlists-Code-Update', os.path.join(common.addon_path, 'services', service_py), duration=default_sleep_duration)
