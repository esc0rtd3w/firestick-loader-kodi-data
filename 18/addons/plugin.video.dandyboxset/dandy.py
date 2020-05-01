import os,xbmc

addon_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.dandymedia'))
addonxml=xbmc.translatePath(os.path.join('special://home/addons', 'repository.dandymedia','addon.xml'))




WRITEME='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.dandymedia" name="Dandymedia Repository" version="1.0.0" provider-name="Dandymedia">
    <extension point="xbmc.addon.repository" name="Dandymedia Repository">
        <info compressed="true">https://github.com/dandy0850/dandymedia/raw/master/addons.xml</info>
        <checksum>https://github.com/dandy0850/dandymedia/raw/master/addons.xml.md5</checksum>
        <datadir zip="true">https://github.com/dandy0850/dandymedia/raw/master/repo</datadir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary>Dandymedia Repository</summary>
        <description>Dandymedia collection all addons</description>
        <platform>all</platform>
    </extension>
</addon>
'''





if os.path.exists(addon_path) == False:
        os.makedirs(addon_path)


     
if os.path.exists(addonxml) == False:

    f = open(addonxml, mode='w')
    f.write(WRITEME)
    f.close()

    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")
