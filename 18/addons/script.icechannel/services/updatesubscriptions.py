from entertainment import istream as entertainment
from entertainment import common
import os

entertainment.loadiStreamPlugins(load_settings=True)

#SUBSCRIPTIONS AUTO UPDATE
service_py = 'updatesubscriptions.py'
default_subs_auto_update_sleep_duration = 30
common.addon.log('Subscription Auto Update Service - Starting\\Waking...')
auto_update_subs = entertainment.GetiStreamSettings(common.settings_XBMC_Integration, 'auto_update_subscriptions')
if auto_update_subs == 'true':
    import datetime
    common.addon.log('Subscription Auto Update Service - Auto Update Enabled')
    subs_last_update = entertainment.GetiStreamSettings(common.settings_XBMC_Integration, 'update_suscription_timestamp')
    if subs_last_update == '' or not subs_last_update:        
        subs_last_update = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        entertainment.SetiStreamSettings(common.settings_XBMC_Integration, 'update_suscription_timestamp', subs_last_update)
        
    try:
        subs_last_update_dt = datetime.datetime.strptime(subs_last_update, "%Y-%m-%d %H:%M:%S")
    except:
        import time
        subs_last_update_dt = datetime.datetime(*(time.strptime(subs_last_update, "%Y-%m-%d %H:%M:%S")[0:6]))

    curr_dt = datetime.datetime.today()

    time_diff = curr_dt - subs_last_update_dt

    auto_update_interval = datetime.timedelta ( hours = int(entertainment.GetiStreamSettings(common.settings_XBMC_Integration, 'auto_update_interval')))

    if time_diff >= auto_update_interval:
        common.addon.log('Subscription Auto Update Service - Interval Reached')
        import xbmc
        import os
        if not xbmc.Player().isPlaying() and not xbmc.getCondVisibility('Library.IsScanningVideo') and not common.GetGlobalProperty(common.gb_Lib_Subs_Op_Running):
            common.addon.log('Subscription Auto Update Service - Working...')
            cmd = 'RunPlugin(plugin://script.icechannel/?mode=%s&indexer=%s&type=tv_seasons&video_type=%s&service=true)' % ( common.mode_Update_Subs, common.indxr_TV_Shows,  common.VideoType_TV)
            xbmc.executebuiltin(cmd)        
            total_mins = common.GetTotalMinutesFromTimeDelta(auto_update_interval)
            common.SetScriptOnAlarm('iStream-Auto-Update-Subscriptions', os.path.join(common.addon_path, 'services', service_py), duration=total_mins)
            common.addon.log('Subscription Auto Update Service - Sleeping... Sleep for %s mins after update is complete' % str(total_mins) )
        else:
            common.addon.log('Subscription Auto Update Service - Sleeping... XBMC is Busy, Sleep for %s mins' % str(default_subs_auto_update_sleep_duration) )
            common.SetScriptOnAlarm('iStream-Auto-Update-Subscriptions',
                os.path.join(common.addon_path, 'services', service_py), duration=default_subs_auto_update_sleep_duration)
    else:        
        diff_diff = auto_update_interval - time_diff
        total_mins = common.GetTotalMinutesFromTimeDelta(diff_diff)
        common.addon.log('Subscription Auto Update Service - Sleeping... Interval not Reached, Sleep for %s mins' % str(total_mins) )
        common.SetScriptOnAlarm('iStream-Auto-Update-Subscriptions', os.path.join(common.addon_path, 'services', service_py), duration=total_mins)
else:
    common.addon.log('Subscription Auto Update Service - Auto Update Disabled, Sleep for %s mins' %  str(default_subs_auto_update_sleep_duration))
    common.SetScriptOnAlarm('iStream-Auto-Update-Subscriptions', os.path.join(common.addon_path, 'services', service_py), duration=default_subs_auto_update_sleep_duration)