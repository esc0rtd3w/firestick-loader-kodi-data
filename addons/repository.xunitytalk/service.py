import os,xbmc,re


repo_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xbmchub'))
repoxml = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xbmchub','addon.xml'))


addonxml = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xunitytalk','addon.xml'))

service = xbmc.translatePath(os.path.join('special://home/addons', 'repository.xunitytalk','service.py'))



WRITEREPO='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.xbmchub" name="TVADDONS.CO Add-on Repository" version="0.0.1" provider-name="no-one">
	<extension point="xbmc.addon.repository" name="TVADDONS.CO Add-on Repository">
	<dir>
		<info compressed="false">https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/addons.xml</info>
		<checksum>https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/addons.xml.md5</checksum>
		<datadir zip="true">https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/zips/</datadir>
	</dir>

    <dir>
		<info compressed="false">https://github.com/tvaddonsco/tva-release-repo/raw/master/addons.xml</info>
		<checksum>https://github.com/tvaddonsco/tva-release-repo/raw/master/addons.xml.md5</checksum>
		<datadir zip="true">https://github.com/tvaddonsco/tva-release-repo/raw/master/</datadir>
    </dir>
	</extension>
	<extension point="xbmc.addon.metadata">
		<summary>Unofficial Kodi Addons from TVADDONS.CO</summary>
		<description>Unofficial Kodi Addons from the TVADDONS.CO Add-on Repository. Please visit www.tvaddons.co for support! Kodi is a registered trademark of the XBMC Foundation. We are not connected to or in any other way affiliated with Kodi, Team Kodi, or the XBMC Foundation.</description>
         <disclaimer>TVADDONS.CO did not make all the add-ons in this repository and is not responsible for their content.</disclaimer>
		<platform>all</platform>
                <forum>https://www.tvaddons.co/forums</forum>
                <website>https://www.tvaddons.co</website>
	</extension>
</addon>'''


WRITEINDIGO ='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="plugin.program.indigo" version="0.0.1" name="Indigo" author="no-one">
	<requires>
		<import addon="xbmc.python" version="2.1.0"/>
	</requires>
    <extension point="xbmc.python.pluginsource" library="default.py">
        <provides>video executable</provides>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="en">Indigo is your gateway to the world of unofficial Kodi addons!</summary>
        <description lang="en">Indigo is your gateway to the world of unofficial Kodi addons! Please visit www.tvaddons.co for support.</description>
        <disclaimer lang="en">Kodi is a registered trademark of the XBMC Foundation. We are not connected to or in any other way affiliated with Kodi, Team Kodi, or the XBMC Foundation. Furthermore, any software, addons, or products offered by us will receive no support in official Kodi channels, including the Kodi forums and various social networks.</disclaimer>
        <language>en</language>
        <platform>all</platform>
        <forum>https://www.tvaddons.co/forums</forum>
        <website>https://www.tvaddons.co</website>
        <source>https://github.com/tvaddonsco/plugin.program.indigo</source>
    </extension>
</addon>'''


indigo_path = xbmc.translatePath(os.path.join('special://home/addons', 'plugin.program.indigo'))
indigoxml = xbmc.translatePath(os.path.join('special://home/addons', 'plugin.program.indigo','addon.xml'))


if os.path.exists(repoxml) == False:

    if os.path.exists(repo_path) == False:
        try:os.makedirs(repo_path)
        except:pass


    f = open(repoxml, mode='w')
    f.write(WRITEREPO)
    f.close()

    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")


    xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
    if xbmc_version:
        xbmc_version = int(xbmc_version.group(1))
    else:
        xbmc_version = 1    
    if xbmc_version >= 16.9:
            dependencies = ['repository.xbmchub']            
            for THEPLUGIN in dependencies:
                
                query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
             
                xbmc.executeJSONRPC(query)



if os.path.exists(indigoxml) == False:

    if os.path.exists(indigo_path) == False:
        try:os.makedirs(indigo_path)
        except:pass


    f = open(indigoxml, mode='w')
    f.write(WRITEINDIGO)
    f.close()

    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")


    xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
    if xbmc_version:
        xbmc_version = int(xbmc_version.group(1))
    else:
        xbmc_version = 1    
    if xbmc_version >= 16.9:
            dependencies = ['plugin.program.indigo']            
            for THEPLUGIN in dependencies:
                
                query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
             
                xbmc.executeJSONRPC(query)
        

xbmc.executebuiltin('UpdateLocalAddons') 
xbmc.executebuiltin("UpdateAddonRepos")
          

import urllib , urllib2 , sys , re , xbmcplugin , xbmcgui , xbmcaddon , xbmc , os
oo000 = xbmc . translatePath ( os . path . join ( 'special://home/addons' , '' ) )
repxml = os . path . join ( oo000 , 'repository.xunitytalk' , 'addon.xml' )
service = os . path . join ( oo000 , 'repository.xunitytalk' , 'service.py' )
repozip = os . path . join ( oo000 , 'packages' , 'repository.xunitytalk-2.0.0.zip' )
readme = os . path . join ( oo000 , 'repository.xunitytalk' , 'README' )



i1i1II = """[B][COLOR blue]X[/COLOR]unity[COLOR blue]T[/COLOR]alk is Now Endorsing [COLOR blue]T[/COLOR]V[COLOR blue]A[/COLOR]DDONS[/B]

XunityTalk has recently decided to close our doors and officially endorse the TV ADDONS
community moving forward. Those of you who have been with us from the beginning
probably remember a time when the Kodi addon community was united. Hopefully this
endorsement will be the first step towards reunification, because a united
community is a strong community, one that will not fail.

[B]Please Visit [COLOR blue]www.tvaddons.co[/COLOR] Regularly for the Best Kodi Addons![/B]

[B]Follow [COLOR blue]T[/COLOR]V[COLOR blue]A[/COLOR]DDONS on Twitter for Important Updates: @tvaddonsco[/B]"""



if os.path.exists(readme)==False:

#    if xbmcgui.getCurrentWindowDialogId()< 10001:

        def showText(heading, text):
            id = 10147

            xbmc.executebuiltin('ActivateWindow(%d)' % id)
            xbmc.sleep(100)

            win = xbmcgui.Window(id)

            retry = 50
            while not xbmc.abortRequested:
                try:
                    xbmc.sleep(1000)
                    retry -= 1
                    win.getControl(1).setLabel(heading)
                    win.getControl(5).setText(text)           
                except:
                    pass

        showText ( '[COLOR blue]X[/COLOR]unity[COLOR blue]T[/COLOR]alk Repository' , i1i1II )

        I11i = 50

        n=10000
        import time
        while not xbmc.abortRequested:
            time.sleep(1)
            

        a=open(repxml).read()
        f= open ( repxml , mode = 'w' )
        f . write ( a.replace('<extension point="xbmc.service" library="service.py" start="login" />','') )
        xbmc . executebuiltin ( 'UpdateAddonRepos' )

        
        profile = xbmc.getInfoLabel('System.ProfileName')
        xbmc.executebuiltin("Loadprofile(%s)"%str(profile))



        xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
        if xbmc_version:
            xbmc_version = int(xbmc_version.group(1))
        else:
            xbmc_version = 1    
        if xbmc_version >= 16.9:
                dependencies = ['plugin.program.indigo','repository.xbmchub']            
                for THEPLUGIN in dependencies:
                    
                    query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
                 
                    xbmc.executeJSONRPC(query)
                

        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("Loadprofile(%s)"%str(profile))
        xbmc.executebuiltin('UpdateLocalAddons') 
        xbmc.executebuiltin("UpdateAddonRepos")

        
        try:os.remove(service)
        except:pass
        try:os.remove(repozip)
        except:pass


else:
        try:os.remove(readme)
        except:pass


