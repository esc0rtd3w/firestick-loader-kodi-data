# load lib directory
# begin
import xbmc,os,shutil
import re
xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
if xbmc_version:
    xbmc_version = int(xbmc_version.group(1))
else:
    xbmc_version = 1


main_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.mdrepo'))
repo_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.istream'))
repoxml = xbmc.translatePath(os.path.join('special://home/addons', 'repository.istream','addon.xml'))
addonxml=xbmc.translatePath(os.path.join('special://home/addons', 'repository.mdrepo','addon.xml'))




WRITEREPO = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <addon id="repository.istream" name="iSTREAM Repository" version="10.3" provider-name="iSTREAM">
            <extension point="xbmc.addon.repository" name="iSTREAM">
		<info compressed="false">https://raw.githubusercontent.com/mucky-duck/istream/master/repo/addons.xml</info>
		<checksum>https://raw.githubusercontent.com/mucky-duck/istream/master/repo/addons.xml.md5</checksum>
		<datadir zip="true">https://raw.githubusercontent.com/mucky-duck/istream/master/repo/zips/</datadir>
            </extension>
            <extension point="xbmc.addon.metadata">
		<summary>iSTREAM XBMC Addons and Extensions</summary>
		<description>iSTREAM XBMC Addons and Extensions</description>
		<platform>all</platform>
            </extension>
        </addon>'''


WRITEME = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.mdrepo" name="Mucky Ducks Repo" version="1.0.1" provider-name="Mucky Duck">
	<extension point="xbmc.addon.repository" name="Mucky Ducks Repo">
		<info compressed="false">https://raw.githubusercontent.com/mucky-duck/mdrepo/master/addons.xml</info>
		<checksum>https://raw.githubusercontent.com/mucky-duck/mdrepo/master/addons.xml.md5</checksum>
		<datadir zip="true">https://raw.githubusercontent.com/mucky-duck/mdrepo/master/</datadir>
	</extension>
	<extension point="xbmc.addon.metadata">
		<summary>Mucky Ducks Repo</summary>
		<description>Download And Install Addons Developed By Mucky Duck And Various Other Developers </description>
		<disclaimer>The owners and submitters to this repository do not host or distribute any of the content displayed by these addons nor do they have any affiliation with the content providers.</disclaimer>
		<platform>all</platform>
	</extension>
</addon>'''


old = xbmc.translatePath('special://home/addons/script.icechannel.extn.xunitytalk')


if os.path.exists(old):
    shutil.rmtree(old, ignore_errors=True)
    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")


if not os.path.exists(repoxml):

    if not os.path.exists(repo_path):
        try:
            os.makedirs(repo_path)
        except:pass


        f = open(repoxml, mode='w')
        f.write(WRITEREPO)
        f.close()

        xbmc.executebuiltin('UpdateLocalAddons')
        xbmc.executebuiltin("UpdateAddonRepos")

        
        

if os.path.exists(addonxml) == False:

    if os.path.exists(main_path) == False:
        try:
            os.makedirs(main_path)
        except:pass


        f = open(addonxml, mode='w')
        f.write(WRITEME)
        f.close()

        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")

        

if xbmc_version >= 16.9:
        dependencies = ['repository.istream', 'script.module.muckys.common', 'script.module.elementtree',
                        'script.common.plugin.cache','script.istream.dialogs', 'script.module.addon.common',
                        'script.module.dnspython', 'script.module.f4mproxy', 'script.module.feedparser',
                        'script.module.metahandler','script.module.myconnpy', 'script.module.parsedom',
                        'script.module.pyamf', 'script.module.simple.downloader', 'script.module.socksipy',
                        'script.module.t0mm0.common', 'script.module.unidecode', 'script.module.universal',
                        'script.module.urlresolver', 'repository.mdrepo', 'script.module.beautifulsoup']
        
        import glob


        folder = xbmc.translatePath('special://home/addons/')

        for DEPEND in glob.glob(folder+'script.icechannel*'):
            try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
            except:dependencies.append(DEPEND.rsplit('/', 1)[1])


        for THEPLUGIN in dependencies:
            xbmc.log(str(THEPLUGIN))
            query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
         
            xbmc.executeJSONRPC(query)
    
        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")

                
if xbmc_version >= 14:
    addon_id = 'script.icechannel'
    lib_addon_dir_name = "lib"
    import xbmcaddon
    import os
    from os.path import join, basename
    import sys
    addon = xbmcaddon.Addon(id=addon_id)
    addon_path = addon.getAddonInfo('path')
    sys.path.append(addon_path)
    lib_addon_dir_path = os.path.join( addon_path, lib_addon_dir_name)
    sys.path.append(lib_addon_dir_path)
    for dirpath, dirnames, files in os.walk(lib_addon_dir_path):
        sys.path.append(dirpath)
# end

from entertainment import common
import os

common._update_settings_xml()

services_path = os.path.join(common.addon_path, 'services')

sti=1

for dirpath, dirnames, files in os.walk(services_path):
    for f in files:
        if f.endswith('.py'):
            service_py = os.path.join(dirpath, f)
            #cmd = 'RunScript(%s,%s)' % (service_py, '1')
            #xbmc.executebuiltin(cmd)
            common.SetScriptOnAlarm(f[:-3], service_py, duration=sti)
            sti = sti + 1

import xbmcaddon


PLUGIN='script.icechannel'
ADDON = xbmcaddon.Addon(id=PLUGIN)
if 'googlecode' in ADDON.getSetting('Default_themeurl'):
    ADDON.setSetting('Default_themeurl','https://raw.githubusercontent.com/mucky-duck/istream/master/images/default/')

try:
    if 'googlecode' in ADDON.getSetting('Xunity_themeurl'):
        ADDON.setSetting('Xunity_themeurl','https://raw.githubusercontent.com/mucky-duck/istream/master/images/default/')
except:pass
