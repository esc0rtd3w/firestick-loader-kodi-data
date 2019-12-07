import common
import os

custom_live_tv_id = 'script.icechannel.extn.livetv.custom'

custom_live_tv_path = common.addon_path.replace(common.addon_id, custom_live_tv_id)
resources_path = os.path.join(custom_live_tv_path, 'resources')
images_path = os.path.join(resources_path, 'images')
plugins_path = os.path.join(custom_live_tv_path, 'plugins')
livetv_path = os.path.join(plugins_path, 'livetv')

custom_icon_src = os.path.join(common.addon_path, 'themes', common.theme_dir, 'custom_live_tv.png')
custom_icon_dst = os.path.join(custom_live_tv_path, 'icon.png')


if not os.path.exists(custom_live_tv_path):
    try:
        os.makedirs(custom_live_tv_path)
        
        # create addon.xml
        addon_xml_path = os.path.join(custom_live_tv_path, 'addon.xml')
        f = open(addon_xml_path, 'w')                
        try:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<addon id="%s" version="0.0.1" name="iStream - Live TV - Custom" provider-name="iStream">\n' % custom_live_tv_id )
            f.write('<extension point="xbmc.python.pluginsource" library="default.py" />\n')
            f.write('<extension point="xbmc.addon.metadata">\n')
            f.write('<summary lang="en">%s</summary>\n' % ('iStream - Live TV - Custom ') )
            f.write('<description lang="en">%s</description>\n' % ('iStream - Live TV - Custom ') )
            f.write('<platform></platform>\n')
            f.write('<language></language>\n')
            f.write('<license></license>\n')
            f.write('<forum></forum>\n')
            f.write('<website></website>\n')
            f.write('<source></source>\n')
            f.write('<email></email>\n')
            f.write('</extension>\n')
            f.write('</addon>\n')
        finally:
            f.close
        
        # create directories
        os.makedirs(resources_path)
        os.makedirs(images_path)
        os.makedirs(plugins_path)
        os.makedirs(livetv_path)
        
        # create default.py
        default_py_path = os.path.join(custom_live_tv_path, 'default.py')
        f = open(default_py_path, 'w')                
        try:
            f.write('addon_id="%s"\n' % custom_live_tv_id)
            f.write('addon_name="iStream - Live TV - Custom"\n')            
        finally:
            f.close
            
        import shutil
        shutil.copyfile(custom_icon_src, custom_icon_dst)
            
        xbmc.executebuiltin('UpdateLocalAddons ')
            
    except:
        pass
        
custom_channel_code = """

from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class <custom_channel_class>(LiveTVIndexer):
    implements = [LiveTVIndexer]
    
    display_name = "<custom_channel_name>"
    
    name = '<custom_channel_id>'
    
    other_names = '<other_names>'
    
    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.livetv.custom'
    addon = xbmcaddon.Addon(addon_id)
    img = <img>
    
    regions = [ 
            {
                'name':'Custom', 
                'img':addon.getAddonInfo('icon'), 
                'fanart':addon.getAddonInfo('fanart')
                }, 
        ]
        
    languages = [ 
        {'name':'Custom', 'img':'', 'fanart':''}, 
        ]
        
    genres = [ 
        {'name':'Custom', 'img':'', 'fanart':''} 
        ]

    addon = None
    
    
"""
        
def add(csv_names, img=None):   

    import xbmcaddon
    success = False
    import time
    while not success:
        try:
            a = xbmcaddon.Addon(custom_live_tv_id)
            success = True
        except:
            print 'waiting'
            time.sleep(0.25)
    
    names = csv_names.split(',')
    name = names[0]
    for x in range(0, len(names)): names[x] = common.CreateIdFromString(names[x])
    c = names[0]
    i = c + '__custom'
    on = ",".join(names)
    
    if not img:
        import shutil
        shutil.copyfile(custom_icon_src, os.path.join(images_path, i + '.png'))
        img = "os.path.join( addon.getAddonInfo('path'), 'resources', 'images', name + '.png' )"
    else:
        img = "'%s'" % img
    
    temp_custom_channel_code = custom_channel_code.replace('<custom_channel_class>', c)
    temp_custom_channel_code = temp_custom_channel_code.replace('<custom_channel_name>', name)
    temp_custom_channel_code = temp_custom_channel_code.replace('<other_names>', on)
    temp_custom_channel_code = temp_custom_channel_code.replace('<custom_channel_id>', i)
    temp_custom_channel_code = temp_custom_channel_code.replace('<img>', img)
    
    # create file
    py_path = os.path.join(livetv_path, i + '.py')
    f = open(py_path, 'w')                
    try:
        f.write(temp_custom_channel_code)
    finally:
        f.close