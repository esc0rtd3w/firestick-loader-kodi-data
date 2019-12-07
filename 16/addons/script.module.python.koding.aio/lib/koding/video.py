# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by TOTALREVOLUTION LTD (support@trmc.freshdesk.com)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. If you're found to be in breach of this license
# then any affected add-ons will be blacklisted and will not be able to work on the same system
# as any other add-ons which use this code. Thank you for your cooperation.

import os
import requests
import shutil
import xbmc
import xbmcgui

from guitools    import Show_Busy
from systemtools import Last_Error

dp            = xbmcgui.DialogProgress()
check_started = xbmc.translatePath('special://profile/addon_data/script.module.python.koding.aio/temp/playback_in_progress')
#----------------------------------------------------------------
# TUTORIAL #
def Check_Playback(ignore_dp=False,timeout=10):
    """
This function will return true or false based on video playback. Simply start a stream
(whether via an add-on, direct link to URL or local storage doesn't matter), the code will
then work out if playback is successful. This uses a number of checks and should take into
account all potential glitches which can occur during playback. The return should happen
within a second or two of playback being successful (or not).

CODE: Check_Playback()

AVAILABLE PARAMS:

    ignore_dp  -  By default this is set to True but if set to False
    this will ignore the DialogProgress window. If you use a DP while
    waiting for the stream to start then you'll want to set this True.
    Please bare in mind the reason this check is in place and enabled
    by default is because some streams do bring up a DialogProgress
    when initiated (such as f4m proxy links) and disabling this check
    in those circumstances can cause false positives.

    timeout  -  This is the amount of time you want to allow for playback
    to start before sending back a response of False. Please note if
    ignore_dp is set to True then it will also add a potential 10s extra
    to this amount if a DialogProgress window is open. The default setting
    for this is 10s.

EXAMPLE CODE:
xbmc.Player().play('http://totalrevolution.tv/videos/python_koding/Browse_To_Folder.mov')
isplaying = koding.Check_Playback()
if isplaying:
    dialog.ok('PLAYBACK SUCCESSFUL','Congratulations, playback was successful')
    xbmc.Player().stop()
else:
    dialog.ok('PLAYBACK FAILED','Sorry, playback failed :(')
~"""
    if not ignore_dp:
        isdialog = True
        counter = 1

# Check if the progress window is active and wait for playback
        while isdialog and counter < 60:
            if xbmc.getCondVisibility('Window.IsActive(progressdialog)'):
                try:
                    if dp.iscanceled():
                        dp.close()
                        break
                except:
                    pass
            xbmc.log('### Current Window: %s' % xbmc.getInfoLabel('System.CurrentWindow'))
            xbmc.log('### Current XML: %s' % xbmc.getInfoLabel('Window.Property(xmlfile)'))
            xbmc.log('### Progress Dialog active, sleeping for %s seconds' % counter)
            xbmc.sleep(1000)
            if xbmc.getCondVisibility('Window.IsActive(progressdialog)') or (xbmc.getInfoLabel('Window.Property(xmlfile)') == 'DialogProgress.xml'):
                isdialog = True
            else:
                isdialog = False
            counter += 1
            xbmc.log('counter: %s' % counter)

# Given the DialogProgress 10 seconds to finish and it's still up - time to close it
            if counter >= 10:
                try:
                    xbmc.log('attempting to send click to close dp')
                    xbmc.executebuiltin('SendClick()')
                    if dp.iscanceled():
                        dp.close()
                    try:
                        dp.close()
                    except:
                        pass
                except:
                    xbmc.log('### FAILED TO CLOSE DP')
    try:
        dp.close()
    except:
        pass

    isplaying = xbmc.Player().isPlaying()
    counter   = 1
    if xbmc.Player().isPlayingAudio():
        return True
# If xbmc player is not yet active give it some time to initialise
    while not isplaying and counter < timeout:
        xbmc.sleep(1000)
        isplaying = xbmc.Player().isPlaying()
        xbmc.log('### XBMC Player not yet active, sleeping for %s seconds' % counter)
        counter += 1

    success = 0
    counter = 0

# If it's playing give it time to physically start streaming then attempt to pull some info
    if isplaying:
        xbmc.sleep(1000)
        while not success and counter < 5:
            try:
                if xbmc.Player().isPlayingVideo():
                    infotag = xbmc.Player().getVideoInfoTag()
                vidtime = xbmc.Player().getTime()
                if vidtime > 0:
                    success = 1

# If playback doesn't start automatically (buffering) we force it to play
                else:
                    xbmc.log('### Playback active but time at zero, trying to unpause')
                    xbmc.executebuiltin('PlayerControl(Play)')
                    xbmc.sleep(2000)
                    vidtime = xbmc.Player().getTime()
                    if vidtime > 0:
                        success = 1

# If no infotag or time could be pulled then we assume playback failed, try and stop the xbmc.player
            except:
                counter += 1
                xbmc.sleep(1000)

# Check if the busy dialog is still active from previous locked up playback attempt
    isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
    counter   = 1
    while isbusy:
        xbmc.log('### Busy dialog active, sleeping for %ss' % counter)
        xbmc.sleep(1000)
        isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
        counter += 1
        if counter >= 5:
            xbmc.executebuiltin('Dialog.Close(busydialog)')

    if not success:
        xbmc.executebuiltin('PlayerControl(Stop)')
        xbmc.log('### Failed playback, stopped stream')
        return False
    else:
        return True
#----------------------------------------------------------------
# TUTORIAL #
def Last_Played():
    """
Return the link of the last played (or currently playing) video.
This differs to the built in getPlayingFile command as that only shows details
of the current playing file, these details can differ to the url which was
originally sent through to initiate the stream. This Last_Played function
directly accesses the database to get the REAL link which was initiated and
will even return the plugin path if it's been played through an external add-on.

CODE: Last_Played()

EXAMPLE CODE:
if koding.Play_Video('http://totalrevolution.tv/videos/python_koding/Browse_To_Folder.mov'):
    xbmc.sleep(3000)
    xbmc.Player().stop()
    last_vid = Last_Played()
    dialog.ok('VIDEO LINK','The link we just played is:\n\n%s'%last_vid)
else:
    dialog.ok('PLAYBACK FAILED','Sorry this video is no longer available, please try using a different video link.')
~"""
    from database  import DB_Query
    from filetools import DB_Path_Check
    from vartools  import Decode_String
    db_path = DB_Path_Check('MyVideos')
    sql     = "SELECT files.strFilename as mystring, path.strPath as mybase FROM files JOIN path ON files.idPath=path.idPath ORDER BY files.lastPlayed DESC LIMIT 1"
    results = DB_Query(db_path, sql)
    try:
        if Decode_String(results[0]['mybase']).startswith('plugin://'):
            return Decode_String(results[0]['mystring'])
        else:
            return Decode_String(results[0]['mybase']+results[0]['mystring'])
    except:
        return False
#----------------------------------------------------------------
# TUTORIAL #
def Link_Tester(video='', local_check=True, proxy_list=None, proxy_url='https://free-proxy-list.net/', ip_col=0, port_col=1, table=0):
    """
Send through a link and test whether or not it's playable on other devices.
Many links include items in the query string which lock the content down to your
IP only so what may open fine for you may not open for anyone else!

This function will attempt to load the page using a proxy. If when trying to access
the link via a proxy the header size and content-type match then we assume the
link will play on any device. This is not fool proof and could potentially return
false positives depending on the security used on the website being accessed.

The return you'll get is a dictionary of the following items:

    'plugin_path' - This will have the path for a plugin, it means the stream was
    originally passed through an add-on to get the final link. If this is not set
    to None then it "should" work on any device so long as that add-on is installed
    (e.g. YouTube).

    'url' - This is the final resolved url which Kodi was playing, you need to check
    the status though to find out whether or not that link is locked to your IP only.

    'status' - This will return one of the following status codes:
        good - The link should work on all IPs.

        bad_link - The link was not valid, won't even play on your current Kodi setup.

        proxy_fail - None of the proxies sent through worked.

        locked - The url only works on this device, if this is the case consider using
        the plugin_path which should generally work on all devices (although this does
        depend on how the developer of that add-on coded up their add-on).

CODE: Link_Tester([proxy_list, url, ip_col, port_col, table])

AVAILABLE PARAMS:

    video  -  This is the url of the video you want to check

    local_check - By default this is set to True and this function will first of
    all attempt to play the video locally with no proxy just to make sure the
    link is valid in the first place. If you want to skip this step then set
    this to False.

    proxy_list  -  If you already have a list of proxies you want to test with
    send them through in the form of a list of dictionaries. Use the following
    format: [{"ip":"0.0.0.0","port":"80"},{"ip":"127.0.0.1","port":"8080"}]

    proxy_url  -  If you want to scrape for online proxies and loop through until a
    working one has been found you can set the url here. If using this then
    proxy_list can be left as the default (None). If you open this Link_Tester
    function with no params the defaults are setup to grab from:
    free-proxy-list.net but there is no guarantee this will always
    work, the website may well change it's layout/security over time.

    ip_col  -  If you've sent through a proxy_url then you'll need to set a column number
    for where in the table the IP address is stored. The default is 0

    port_col  -  If you've sent through a proxy_url then you'll need to set a column number
    for where in the table the port details are stored. The default is 1

    table  -  If you've sent through a proxy_url then you'll need to set a table number.
    The default is 0 - this presumes we need to use the first html table found on the
    page, if you require a different table then alter accordingly - remember zero is the
    first instance so if you want the 3rd table on the page you would set to 2.

EXAMPLE CODE:
vid_test = Link_Tester(video='http://totalrevolution.tv/videos/python_koding/Browse_To_Folder.mov')
if vid_test['status'] == 'bad_link':
    dialog.ok('BAD LINK','The link you sent through cannot even be played on this device let alone another one!')
elif vid_test['status'] == 'proxy_fail':
    dialog.ok('PROXIES EXHAUSTED','It was not possible to get any working proxies as a result it\'s not possible to fully test whether this link will work on other devices.')
elif vid_test['status'] == 'locked':
    dialog.ok('NOT PLAYABLE','Although you can play this link locally the tester was unable to play it when using a proxy so this is no good.')
    if vid_test['plugin_path']:
        dialog.ok('THERE IS SOME GOOD NEWS!','Although the direct link for this video won\'t work on other IPs it "should" be possible to open this using the following path:\n[COLOR dodgerblue]%s[/COLOR]'%vid_test['plugin_path'])
else:
    dialog.ok('WORKING!!!','Congratulations this link can be resolved and added to your playlist.')
~"""
    import random
    import urllib
    from guitools    import Notify
    from vartools    import Table_Convert
    from systemtools import System
    # xbmc.executebuiltin('RunScript(special://home/addons/script.module.python.koding.aio/lib/koding/localproxy.py)')
    Notify('PLEASE WAIT','Checking Link - Step 1','5000','Video.png')
    isplaying = xbmc.Player().isPlaying()

# If video not yet playing try playing it
    if not isplaying:
        xbmc.Player().play(video)

    if Check_Playback(True):
        xbmclink        = xbmc.Player().getPlayingFile()
        active_plugin   = System(command='addonid')
        plugin_path     = System(command='currentpath')
        vid_title       = ''
        title_count     = 0

        while vid_title == '' and title_count < 10:
            vid_title  = xbmc.getInfoLabel('Player.Title')
            xbmc.sleep(100)
            title_count += 1

        xbmc.Player().stop()
        video_orig = Last_Played()
        xbmc.log('VIDEO: %s'%video_orig,2)
        if video_orig.startswith('plugin://'):
            video = xbmclink
            xbmc.log('NEW VIDEO: %s'%video,2)
        else:
            video = video_orig
        r = requests.head(url=video, timeout=5)
        orig_header  = r.headers
        try:
            orig_size = orig_header['Content-Length']
        except:
            orig_size = 0
        try:
            orig_type = orig_header['Content-Type']
        except:
            orig_type = ''
        proxies      = Table_Convert(url=proxy_url, contents={"ip":ip_col,"port":port_col}, table=table)
        myproxies    = []
        used_proxies = []
        for item in proxies:
            myproxies.append({'http':'http://%s:%s'%(item['ip'],item['port']),'https':'https://%s:%s'%(item['ip'],item['port'])})
        success = False
        if video_orig.startswith('plugin://'):
            dp.create('[COLOR gold]CHECKING PROXIES[/COLOR]','This video is being parsed through another add-on so using the plugin path should work. Now checking the final resolved link...','')
        else:
            dp.create('[COLOR gold]CHECKING PROXIES[/COLOR]','Please wait...','')

        counter = 1
        while (not success) and (len(myproxies) > 0):
            dp.update(counter/len(myproxies),'Checking proxy %s'%counter)
            counter += 1
            proxychoice  = random.choice( range(0,len(myproxies)) )
            currentproxy = myproxies[proxychoice]

        # Find a working proxy and play the video through it
            try:
                xbmc.log(repr(currentproxy),2)
                r = requests.head(url=video, proxies=currentproxy, timeout=5)
                headers  = r.headers
                try:
                    new_size = headers['Content-Length']
                except:
                    new_size = 0
                try:
                    new_type = headers['Content-Type']
                except:
                    new_type = ''
                xbmc.log('orig size: %s'%orig_size,2)
                xbmc.log('new size: %s'%new_size,2)
                xbmc.log('orig type: %s'%orig_type,2)
                xbmc.log('new type: %s'%new_type,2)
                xbmc.log('VIDEO: %s'%video,2)
                if orig_size != 0 and (orig_size==new_size) and (orig_type==new_type):
                    dp.close()
                    success  = True
            except:
                xbmc.log('failed with proxy: %s'%currentproxy,2)

            myproxies.pop(proxychoice)
            if dp.iscanceled():
                dp.close()
                break
        plugin_path = None
        if video_orig.startswith('plugin://'):
            plugin_path = video_orig
        if len(myproxies)==0 and not success:
            return {"plugin_path":plugin_path, "url":video, "status":"proxy_fail"}
        elif not success:
            return {"plugin_path":plugin_path, "url":video, "status":"locked"}
        else:
            return {"plugin_path":plugin_path, "url":video, "status":"good"}
    else:
        return {"plugin_path":None, "url":video, "status":"bad_link"}
#----------------------------------------------------------------
# TUTORIAL #
def M3U_Selector(url,post_type='get',header='Stream Selection'):
    """
Send through an m3u/m3u8 playlist and have the contents displayed via a dialog select.
The return will be a dictionary of 'name' and 'url'. You can send through either
a locally stored filepath or an online URL.

This function will try it's best to pull out the relevant playlist details even if the
web page isn't a correctly formatted m3u playlist (e.g. an m3u playlist embedded into
a blog page).

CODE: M3U_Selector(url, [post_type, header])

AVAILABLE PARAMS:
    (*) url  -  The location of your m3u file, this can be local or online

    post_type  -  If you need to use POST rather than a standard query string
    in your url set this to 'post', by default it's set to 'get'.

    header  -  This is the header you want to appear at the top of your dialog
    selection window, by default it's set to "Stream Selection"

EXAMPLE CODE:
dialog.ok('M3U SELECTOR','We will now call this function using the following url:','','[COLOR dodgerblue]http://totalrevolution.tv/videos/playlists/youtube.m3u[/COLOR]')

# This example uses YouTube plugin paths but any playable paths will work
vid = koding.M3U_Selector(url='http://totalrevolution.tv/videos/playlists/youtube.m3u')


# Make sure there is a valid link returned
if vid:
    playback = koding.Play_Video(video=vid['url'], showbusy=False)
    if playback:
        dialog.ok('SUCCESS!','Congratulations the playback was successful!')
        xbmc.Player().stop()
    else:
        dialog.ok('OOPS!','Looks like something went wrong there, the playback failed. Check the links are still valid.')
~"""
    from web import Open_URL
    from vartools import Cleanup_String, Find_In_Text
    from filetools import Text_File
    success = False
    if url.startswith('http'):
        content = Open_URL(url=url, post_type=post_type, timeout=10)
    else:
        try:
            url = xbmc.translatePath(url)
        except:
            pass
        content = Text_File(url,'r')
    if content:
        newcontent = content.splitlines()
        name_array = []
        url_array  = []
        name = ''
        for line in newcontent:
            line = line.strip()
        # Grab the name of the stream
            if line.startswith('#EXT'):
                name = line.split(',')
                name.pop(0)
                name = ''.join(name)
        # Grab the url(s) of the stream
            if name != '' and line != '' and not line.startswith('#EXT'):
                name_array.append(Cleanup_String(name))
                line = line.replace('<br>','').replace('<br />','').replace('<br/>','')
                line = line.replace('</p>','').replace('</div>','').replace('</class>','')
                xbmc.log('line: %s'%line)
                if 'm3u' in line or 'm3u8' in line:
                    line = 'LIST~'+line
                if 'src="' in line:
                    line = Find_In_Text(content=line, start='src="', end='"')[0]
                url_array.append(line)
                name = ''
                line = ''
        # If there is only one entry with no names/comments just return as unknown with the link
            if not '#EXT' in content:
                return {'name' : 'Unknown', 'url' : line}

    # If there's a list we show a dialog select of the available links
        if len(name_array) > 0:
            choice = xbmcgui.Dialog().select(header, name_array)
            if choice >= 0:

            # If the selection is a final url and not a list of multiple links
                if not url_array[choice].startswith('LIST~'):
                    success = True
                    return {'name' : name_array[choice], 'url' : url_array[choice]}

            # List of multiple links detected, give option of which link to play
                else:
                    clean_link = url_array[choice].replace('LIST~','')
                    content = Open_URL(url=clean_link, timeout=10)
                    if content:
                        newcontent = content.splitlines()
                        name_array = []
                        url_array  = []
                        name = ''
                        counter = 1
                        for line in newcontent:
                        # Show name as link 1,2,3,4 etc.
                            if line.startswith('#EXT'):
                                name = 'LINK '+str(counter)
                        # Grab the link(s) to the video
                            if name != '' and line != '' and not line.startswith('#EXT'):
                                name_array.append(name)
                                line = line.replace('<br>','').replace('<br />','').replace('<br/>','')
                                line = line.replace('</p>','').replace('</div>','').replace('</class>','')
                                url_array.append(line)
                                name = ''
                                line = ''
                                counter += 1
                        # If there is only one entry with no names/comments just return as unknown with the link
                            if not '#EXT' in content:
                                return {'name' : 'Unknown', 'url' : line}

                    # Give option of which link to play in case of multiple links available
                        if len(name_array) > 0:
                            choice = xbmcgui.Dialog().select(header, name_array)
                            if choice >= 0:
                                success = True
                                return {'name' : name_array[choice], 'url' : url_array[choice]}
    if not success:
        xbmcgui.Dialog().ok('NO LINKS FOUND','Sorry no valid links could be found for this stream.')
        return False
#----------------------------------------------------------------
# TUTORIAL #
def Play_Video(video,showbusy=True,content='video',ignore_dp=False,timeout=10, item=None, player=xbmc.Player(), resolver=None):
    """
This will attempt to play a video and return True or False on
whether or not playback was successful. This function is similar
to Check_Playback but this actually tries a number of methods to
play the video whereas Check_Playback does not actually try to
play a video - it will just return True/False on whether or not
a video is currently playing.

If you have m3u or m3u8 playlist links please use the M3U_Selector
function to get the final resolved url.

CODE: Play_Video(video, [showbusy, content, ignore_dp, timeout, item])

AVAILABLE PARAMS:

    (*) video  -  This is the path to the video, this can be a local
    path, online path or a channel number from the PVR.

    showbusy  -  By default this is set to True which means while the
    function is attempting to playback the video the user will see the
    busy dialog. Set to False if you prefer this not to appear but do
    bare in mind a user may navigate to another section and try playing
    something else if they think this isn't doing anything.

    content  -  By default this is set to 'video', however if you're
    passing through audio you may want to set this to 'music' so the
    system can correctly set the tags for artist, song etc.

    ignore_dp  -  By default this is set to True but if set to False
    this will ignore the DialogProgress window. If you use a DP while
    waiting for the stream to start then you'll want to set this True.
    Please bare in mind the reason this check is in place and enabled
    by default is because some streams do bring up a DialogProgress
    when initiated (such as f4m proxy links) and disabling this check
    in those circumstances can cause false positives.

    timeout  -  This is the amount of time you want to allow for playback
    to start before sending back a response of False. Please note if
    ignore_dp is set to True then it will also add a potential 10s extra
    to this amount if a DialogProgress window is open. The default setting
    for this is 10s.

    item  -  By default this is set to None and in this case the metadata
    will be auto-populated from the previous Add_Dir so you'll just get the
    basics like title, thumb and description. If you want to send through your
    own metadata in the form of a dictionary you can do so and it will override
    the auto-generation. If anything else sent through no metadata will be set,
    you would use this option if you've already set metadata in a previous function.

    player  -  By default this is set to xbmc.Player() but you can send through
    a different class/function if required.

    resolver  -  By default this is set to urlresolver but if you prefer to use
    your own custom resolver then just send through that class when calling this
    function and the link sent through will be resolved by your custom resolver.
    
EXAMPLE CODE:
isplaying = koding.Play_Video('http://totalrevolution.tv/videos/python_koding/Browse_To_Folder.mov')
if isplaying:
    dialog.ok('PLAYBACK SUCCESSFUL','Congratulations, playback was successful')
    xbmc.Player().stop()
else:
    dialog.ok('PLAYBACK FAILED','Sorry, playback failed :(')
~"""

    xbmc.log('### ORIGINAL VIDEO: %s'%video)
    if not resolver:
        import urlresolver
        resolver = urlresolver
    try:    import simplejson as json
    except: import json

    if not item:
        meta = {}
        for i in ['title', 'originaltitle', 'tvshowtitle', 'year', 'season', 'episode', 'genre', 'rating', 'votes',
                  'director', 'writer', 'plot', 'tagline']:
            try:
                meta[i] = xbmc.getInfoLabel('listitem.%s' % i)
            except:
                pass
        meta = dict((k, v) for k, v in meta.iteritems() if not v == '')
        if 'title' not in meta:
            meta['title'] = xbmc.getInfoLabel('listitem.label')
        icon = xbmc.getInfoLabel('listitem.icon')
        item = xbmcgui.ListItem(path=video, iconImage =icon, thumbnailImage=icon)
        if content == "music":
            try:
                meta['artist'] = xbmc.getInfoLabel('listitem.artist')
                item.setInfo(type='Music', infoLabels={'title': meta['title'], 'artist': meta['artist']})
            except:
                item.setInfo(type='Video', infoLabels=meta)
        else:
            item.setInfo(type='Video', infoLabels=meta)

    elif type(item).__name__ == 'dict':
        item.setInfo(type='Video', infoLabels=meta)

    else:
        pass

    playback = False
    if showbusy:
        Show_Busy()


# if a plugin path is sent we try activate window
    if video.startswith('plugin://'):
        try:
            xbmc.log('Attempting to play via xbmc.Player().play() method')
            player.play(video)
            playback = Check_Playback(ignore_dp,timeout)
        except:
            xbmc.log(Last_Error())

# If an XBMC action has been sent through we do an executebuiltin command
    elif video.startswith('ActivateWindow') or video.startswith('RunAddon') or video.startswith('RunScript') or video.startswith('PlayMedia'):
        try:
            xbmc.log('Attempting to play via xbmc.executebuiltin method')
            xbmc.executebuiltin('%s'%video)
            playback = Check_Playback(ignore_dp,timeout)
        except:
            xbmc.log(Last_Error())

    elif ',' in video:
# Standard xbmc.player method (a comma in url seems to throw urlresolver off)
        try:
            xbmc.log('Attempting to play via xbmc.Player.play() method')
            player.play('%s'%video, item)
            playback = Check_Playback(ignore_dp,timeout)

# Attempt to resolve via urlresolver
        except:
            try:
                xbmc.log('Attempting to resolve via urlresolver module')
                xbmc.log('video = %s'%video)
                hmf = resolver.HostedMediaFile(url=video, include_disabled=False, include_universal=True)
                if hmf.valid_url() == True:
                    video = hmf.resolve()
                    xbmc.log('### VALID URL, RESOLVED: %s'%video)
                player.play('%s' % video, item)
                playback = Check_Playback(ignore_dp,timeout)
            except:
                xbmc.log(Last_Error())

# Play from a db entry - untested
    elif video.isdigit():
        xbmc.log('### Video is digit, presuming it\'s a db item')
        command = ('{"jsonrpc": "2.0", "id":"1", "method": "Player.Open","params":{"item":{"channelid":%s}}}' % url)
        xbmc.executeJSONRPC(command)
        playback = Check_Playback(ignore_dp,timeout)

    else:
# Attempt to resolve via urlresolver
        try:
            xbmc.log('Attempting to resolve via urlresolver module')
            xbmc.log('video = %s'%video)
            hmf = resolver.HostedMediaFile(url=video, include_disabled=False, include_universal=True)
            if hmf.valid_url() == True:
                video = hmf.resolve()
                xbmc.log('### VALID URL, RESOLVED: %s'%video)
            player.play('%s' % video, item)
            playback = Check_Playback(ignore_dp,timeout)

# Standard xbmc.player method
        except:
            try:
                xbmc.log('Attempting to play via xbmc.Player.play() method')
                player.play('%s' % video, item)
                playback = Check_Playback(ignore_dp,timeout)
            except:
                xbmc.log(Last_Error())

    xbmc.log('Playback status: %s' % playback)
    Show_Busy(False)
    counter = 1
    dialogprogress = xbmc.getCondVisibility('Window.IsActive(progressdialog)')
    if not ignore_dp:
        while dialogprogress:
            dp.create('Playback Good','Closing dialog...')
            xbmc.log('Attempting to close dp #%s'%counter)
            dp.close()
            xbmc.sleep(1000)
            counter += 1
            dialogprogress = xbmc.getCondVisibility('Window.IsActive(progressdialog)')

    return playback
#----------------------------------------------------------------
# TUTORIAL #
def Sleep_If_Playback_Active():
    """
This will allow you to pause code while kodi is playing audio or video

CODE: Sleep_If_Playback_Active()

EXAMPLE CODE:
dialog.ok('PLAY A VIDEO','We will now attempt to play a video, once you stop this video you should see a dialog.ok message.')
xbmc.Player().play('http://download.blender.org/peach/bigbuckbunny_movies/big_buck_bunny_720p_stereo.avi')
xbmc.sleep(3000) # Give kodi enough time to load up the video
koding.Sleep_If_Playback_Active()
dialog.ok('PLAYBACK FINISHED','The playback has now been finished so this dialog code has now been initiated')
~"""
    isplaying = xbmc.Player().isPlaying()
    while isplaying:
        xbmc.sleep(500)
        isplaying = xbmc.Player().isPlaying()
