'''
kinkin
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import settings
import time,datetime
import glob
import shutil
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom


ADDON = settings.addon()
VIEW = settings.viewtype()
FILE_DIR = settings.xml_files()
addon_path = os.path.join(xbmc.translatePath('special://home/addons'), '')
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.advancedsettings', 'fanart.jpg'))
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.advancedsettings', 'icon.png'))
SETTINGS_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.program.advancedsettings'), 'settings.xml')
USERDATA_PATH = os.path.join(xbmc.translatePath('special://profile'), '')
ACTIVESETTINGSFILE = os.path.join(xbmc.translatePath('special://profile'), 'advancedsettings.xml')
editfile = settings.xml_file()

def MENU(name):
    addDir("Edit Settings", 'url',499, iconart,'blank','Build your advanced settings file')
    addDirPlayable("Write XML File", 'url',500, iconart,'Feeling brave? Write your advanced settings directly to your userdata directory. You may need to reboot for settings to take effect',ACTIVESETTINGSFILE,'')
    if os.path.exists(ACTIVESETTINGSFILE):
        addDirPlayable("View active advancedsettings.xml", 'url',495, '','View your active advanced settings file','','')
        addDirPlayable("Remove advancedsettings.xml", 'url',490, '','Delete all advanced settings (settings are saved in this addon to be written later). Reboot may be required to take effect','','')
    addDirPlayable("Write XML File to temporary location", 'url',500, '','Play it safe. Write your advanced settings to userdata/plugin.program.advancedsettings/XML_FILES/ directory',editfile,'')
    addDirPlayable("Reset all settings", 'url',489, '','Resets all settings saved in this addon only. You will still need to run "Remove advancedsettings.xml" and reboot to remove completely','','')
    addDir("List enabled settings", 'url',498, '','blank','Check which settings are enabled before writing your xml file')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def buildmenu(name):
    addDir("Troubleshooting settings ", 'url',10, '','blank','Define your video settings')
    addDir("Audio/video playback settings", 'url',11, '','blank','Define your audio settings')
    addDir("Video library settings", 'url',12, '','blank','Define your video library settings')
    addDir("Library artwork", 'url',13, '','blank','Define your library artwork settings')
    addDir("Video and music library settings", 'url',14, '','blank','Define your video and music library settings')
    addDir("Music settings", 'url',15, '','blank','Define your music settings')
    addDir("Photos settings", 'url',16, '','blank','Define your photo settings')
    addDir("Network settings", 'url',17, '','blank','Define your network settings')
    addDir("File system settings", 'url',18, '','blank','Define your file system settings')
    addDir("Remote control settings", 'url',19, '','blank','Define your remote control settings')
    addDir("Other interface settings", 'url',20, '','blank','Define other interface settings')#Unsorted 
    addDir("Unsorted", 'url',21, '','blank','Unsorted network settings')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def removexmlfile(name):
    if os.path.exists(ACTIVESETTINGSFILE):
        os.remove(ACTIVESETTINGSFILE)
        notification('Easy Advanced Settings', 'advancedsettings.xml removed', '4000', iconart)
        xbmc.executebuiltin("Container.Refresh")
		
def resetsettings(name):
    allsettings = read_from_file(SETTINGS_PATH)
    all_ids = regex_get_all(allsettings, 'setting id="', '"')
    for id in all_ids:
        if id != 'viewtype':
            ADDON.setSetting(id, value="DISABLED")
    notification('Easy Advanced Settings', 'All settings reset', '4000', iconart)
		
def checksettings(name):
    allsettings = read_from_file(SETTINGS_PATH)
    match = re.compile('setting id="(.+?)" value="(.+?)"').findall(allsettings)
    for id, value in match:
        if value != 'DISABLED' and id != 'viewtype':
            value = value.replace('&#x0A;', '\n').replace('&lt;', '<').replace('&gt;', '>')
            text = "[COLOR lime]%s[/COLOR]" % (value)
            addDirPlayable(text, 'url','url', '','','','')
	
def troubleshooting(name):
    addDir("jsonrpc", 'url',101, '','blank','To make it easier for developers using the JSON RPC API in their (third party) applications to debug during development the json output of XBMC can be prettified by setting compactoutput to false. Default json output mode is a compact print which does not contain any unnecessary whitespaces and therefore is difficult to read for humans. Furthermore using the tcpport setting it is possible to change the default TCP port used by XBMC for JSON RPC (which is 9090) to any other valid port')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def audiovideo(name):
    addDir("Video", 'url',102, '','blank','Define your video settings')
    addDir("Audio", 'url',103, '','blank','Define your audio settings')
    addDir("EDL", 'url',104, '','blank','Commercial break detection not as good you think it could be? Are some commercial breaks in a series of adverts not being skipped? Are some parts being skipped that are clearly not commercials? Does the end of the previous recording still show? The following advanced settings can be used to better identify full commercial break sequences, remove incorrectly flagged commercial breaks, and have playback start at the actual beginning of the recording.')
    addDir("PVR", 'url',105, '','blank','Define your PVR settings')
    addDir("EPG", 'url',106, '','blank','Define your EPG settings')
    name = name.lower()
    dirlist =  ['skiploopfilter<>dialog<>The amount of the loop filter to skip on h264 decoding. This can help the performance of slower machines when decoding h264 content. Values, in decreasing CPU usage (and decreasing quality)<>["-16","0","8","16","32","48","DISABLED"]<>root', 
	'measurerefreshrate<>bool<>When using "Sync playback to display" on Windows, the detected refreshrate might be wrong. When enabling measurerefreshrate, the refreshrate is measured instead, which makes it more accurate<><>root',
	'forcedswaptime<>num<>Use to force a backbuffer->frontbuffer swap while vsync is enabled. Set to the time (in ms) to allow for the swap (e.g. <forcedswaptime>1</forcedswaptime> is typical)<><>root']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        try:
            name = splitd[4]
        except:
            name = name
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def videolibrary(name):
    name = name.lower()
    addDir("Video Library", 'url',115, '','blank','Options specific to the Video Library')
    dirlist =  ['videoextensions$add<>text<>Allow (add) file extensions in the My Video windows (.m4v .3gp). Separate with a space<>', 
	'videoextensions$remove<>text<>Exclude (remove) file extensions in the My Video windows (.m4v .3gp). Separate with a space<>',
	'discstubextensions$add<>text<>Additional file-extensions that will be treated as disc stubs (.dvd .blu). Separate with a space<>', 
	'discstubextensions$remove<>text<>Additional file-extensions that will NOT be treated as disc stubs (.dvd .blu). Separate with a space<>',
	'sorttokens$token<>text<>Allows you to specify additional tokens that will be ignored at the start of lines during sorting (ie. the)<>',
	'moviestacking$regexp<>moviestcking<>This is used by the File Stacking algorithm to combine multi-part files and contains a list of "Regular Expressions". As of XBMC v9.11, video stacking regular expressions must contain exactly four (4) capture expressions<>',
	'video$cleandatetime<>text<>Matches a year number in a string using a Regular Expression. The string found before will be used as basis string getting cleaned by the cleanstrings expressions.By default date formats like MM:YY are ignored.<>',
	'video$cleanstrings$regexp<>text<>Clean unwanted characters from filenames or folders by using a list of Regular Expressions. Please note that everything right of the match (at the end of the file name) is removed, so if you would have a file named Super movie.mp4 and would add <regexp> </regexp> (only a space), the only thing that would be left is Super, which is probably not what you want.<>'
	'tvshowmatching$regexp<>text<>Matches the season and episode numbers in file paths by using a list of Regular Expressions. Arguments action="append" or action="prepend" will insert user specified expressions after, or before, the defaults. For multi-episode matching to work, there needs to be a third set of parentheses at the end, this part is fed back into the regexp engine. <>',
	'tvmultipartmatching<>text<>Matches a multipart episode number based on a previously identified episode file, using a list of Regular Expressions<>',
	'video$excludetvshowsfromscan$regexp<>text<>Matches filenames or folders which should be excluded from a tvshow library scan using a list of Regular Expressions<>',
	'trailermatching$regexp<>text<>Contains "Regular Expression" syntax (commonly referred to as "RegEx" or "RegExp") to match the locally stored trailers to movies in the library<>',
	'videoscanner$ignoreerrors<>bool<>Set to true to silently ignore errors while scanning videos. This prevents the error dialogue box, so you do not have to keep hitting "yes" to keep scanning<>'
	'myth$movielength<>num<>Not seeing all the recordings you expected in the Movies folder? If so, it is very likely that the electronic program guide (EPG) used by MythTV does not accurately distinguish between TV Shows and Movies all the time. The following setting allows the length of the recording to also be used to determine if a recording is a Movie<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def video_library(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['allitemsonbottom<>bool<>Sorts the "*All" items at the bottom of the list when in Ascending order<>', 
	'backgroundupdate<>bool<>Set to hide the video scanner dialog from the gui. NOTE: To get this working properly, you have to do a "Clean Library" in settings the first time after you enable the setting<>',
	'cleanonupdate<>bool<>Sefault set to false to prevent xbmc from removing items from the database while updating<>', 
	'hideallitems<>bool<>Removes the "*All" items from the video library<>',
	'hideemptyseries<>bool<>Hide empty series in the video library<>',
	'hiderecentlyaddeditems<>bool<>Removes the "Recently added ..." items from the video library<>',
	'recentlyaddeditems<>num<>Number of recently added items. Defaults to 25<>',
	'itemseparator<>text<>Separator used for multiple artists/genres in tags.<>'
	'exportautothumbs<>bool<>Export auto-generated thumbs. Defaults to false <>',
	'importwatchedstate<>bool<>Import previously exported playdate and playcount from .nfo files. Defaults to false<>',
	'importresumepoint<>bool<>Import previously exported resume point from .nfo files. Defaults to false<>',
	'mymovies$categoriestogenres<>bool<>Add MyMovies Custom Categories to XBMC Genres (boolean, default is false)<>',
	'dateadded<>dialog<>0 results in using the current datetime when adding a video. 1 (default) results in prefering to use the files mtime (if it is valid) and only using the files ctime if the mtime is not valid. 2 results in using the newer datetime of the files mtime and ctime<>["0","1","2","DISABLED"]']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        options = splitd[3]
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def libraryartwork(name):
    name = 'root'
    dirlist =  ['imageres<>num<>Specify the maximal resolution that art should be resized to in pixels. The width is automatically calculated as being 16/9*height. The image will be resized to fit within this size. e.g. an image that is 2000x500 will be cached at size 1280x320. An image that is 500x800 will be cached at size 450x720 using the default value of 720<>', 
	'fanartres<>num<>Specify the resolution that cached fanart should be resized to in pixels. The width is automatically calculated as being 16/9*height. Only images that are exactly 16x9 and equal to or greater than this resolution will be cached at this size - all other images will be cached using <imageres>. The default value is 1080<>',
	'fanart$add<>text<>A list of additional files to try when searching for fanart images. (The defaults are fanart.jpg and fanart.png which can be removed.)<>', 
	'fanart$remove<>text<>A list of additional files to try when searching for fanart images. (The defaults are fanart.jpg and fanart.png which can be removed.)<>',
	'musicthumbs$add<>text<>A list of additional files to try when searching for music thumbnail images. (The default is folder.jpg which can be removed.) <>', 
	'musicthumbs$remove<>text<>A list of additional files to try when searching for music thumbnail images. (The default is folder.jpg which can be removed.) <>',
	'useddsfanart<>bool<>This settings allows XBMC to use your GPU rendering fanart and some other images. This will make loading images considerably faster, especially on systems with slower processors (e.g. atom based systems). Do not use this option on ARM based systems (Apple TV2/iOS/RPi/many Android systems) as it is likely to degrade performance because DDS images are not supported<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def videomusiclibrary(name):
    name = 'root'
    addDir("Video Database", 'url',470, '','blank','Allows advanced customization of the default database settings for video\nNote: It is HIGHLY recommended that you not attempt to place an sqlite3 database outside of XBMCs path. sqlite3 contains no filesystem abstraction, so this will plain break on any non-local (as far as XBMC is concerned) paths. Use this for mysql only.')
    addDir("Music Database", 'url',471, '','blank','Allows advanced customization of the default database settings for music\nNote: It is HIGHLY recommended that you not attempt to place an sqlite3 database outside of XBMCs path. sqlite3 contains no filesystem abstraction, so this will plain break on any non-local (as far as XBMC is concerned) paths. Use this for mysql only.\nNote: If you use MySQL for the music database, but are finding that it slows down your music library significantly, execute the following query to create an index on the song table. This will significantly speed up queries using the songview views looking up by artist')
    dirlist =  ['playlistretries<>num<>The number of retries attempted if a source is offline. With this control you can alter the number of consecutive failed items before a playlist fails<>', 
	'playlisttimeout<>num<>The timeout, in seconds, before item failure.<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)

def videodatabase(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['type<>dialog<>Can be either "sqlite3" or "mysql" (default: sqlite3)<>["sqlite3","mysql","DISABLED"]', 
	'host<>text<>sqlite3: defines the relative path to the database file (eg. /usr/local/xbmc/databases)\nmysql: defines the host of the mysql socket (eg. localhost, 192.168.0.1, etc)<>',
	'port<>num<>sqlite3: silently ignored\nmysql: defines the port of the mysql socket (default: 3306)<>', 
	'name<>text<>Not needed by default, and some users report issues when defining the this tag. When not used "MyVideos"+DB number will be used\nsqlite3: defines the name of the database file to read from, excluding the ".db" extensionznmysql: defines the name of the database to use<>',
	'user<>text<>sqlite3: silently ignored\nmysql: defines the user with privileged access to the database <>', 
	'pass<>text<>sqlite3: silently ignored\nmysql: defines the password for the user with privileged access to the database<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def musicdatabase(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['_type<>dialog<>Can be either "sqlite3" or "mysql" (default: sqlite3)<>["sqlite3","mysql","DISABLED"]', 
	'_host<>text<>sqlite3: defines the relative path to the database file (eg. /usr/local/xbmc/databases)\nmysql: defines the host of the mysql socket (eg. localhost, 192.168.0.1, etc)<>',
	'_port<>num<>sqlite3: silently ignored\nmysql: defines the port of the mysql socket (default: 3306)<>', 
	'_name<>text<>Not needed by default, and some users report issues when defining the this tag. When not used "MyVideos"+DB number will be used\nsqlite3: defines the name of the database file to read from, excluding the ".db" extensionznmysql: defines the name of the database to use<>',
	'_user<>text<>sqlite3: silently ignored\nmysql: defines the user with privileged access to the database <>', 
	'_pass<>text<>sqlite3: silently ignored\nmysql: defines the password for the user with privileged access to the database<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def music(name):
    name = 'root'
    addDir("Music Library", 'url',472, '','blank','Allows advanced customization of the default database settings for video\nNote: It is HIGHLY recommended that you not attempt to place an sqlite3 database outside of XBMCs path. sqlite3 contains no filesystem abstraction, so this will plain break on any non-local (as far as XBMC is concerned) paths. Use this for mysql only.')
    addDir("Karaoke", 'url',473, '','blank','Allows advanced customization of the default database setting')
    dirlist =  ['musicextensions$add<>text<>A list of additional file-extensions to allow (add) in the My Music window. Separate with a space<>', 
	'musicextensions$remove<>text<>A list of additional file-extensions to remove from the My Music window. Separate with a space<>',
	'cddbaddress<>text<>The address of the online CDDb database. You may set this to another freedb mirror if there is a more suitable one<>', 
	'songinfoduration<>num<>This controls how long the song information will remain onscreen when the song changes during visualisations. The valid range is "1" to "Indefinite (0)", in seconds. This does not include the duration of any transition effects<>',
	'musicfilenamefilters<>text<>Contains filters to match music information (artist, title etc.) from a tag-less music filename. The first <filter> to match completely is used. Matched items include\n%A - Artist\n%T - Title\n%B - Album\n%N - Track number\n%S - Part of set (disk number)\n%D - Duration\n%G - Genre\n%Y - Year\n%R - Rating\n\nExample: %A - %T<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def musiclibrary(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['_hideallitems<>bool<>Removes the "*All" items from the music library<>', 
	'_allitemsonbottom<>bool<>Sorts the "*All" items at the bottom of the list when in Ascending order<>',
	'_backgroundupdate<>bool<>Set to hide the music scanner dialog from the gui<>', 
	'_recentlyaddeditems<>num<>Number of recently added items. Defaults to 25<>',
	'albumssortbyartistthenyear<>bool<>At an albums listing, when you sort by artist, secondary sort will be year<>', 
	'albumformat<>text<>Album label template, default is "%B"<>'
	'_prioritiseapetags<>bool<>Prioritise APEv2 tags over ID3v1/2 tags, default is false<>'
	'_itemseparator<>text<>Separator used for multiple artists/genres in tags<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def karaoke(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['syncdelaycdg<>text<>Music-lyrics delay for CDG format lyrics in SECONDS. Floating number, may be negative<>', 
	'syncdelaylrc<>text<>Music-lyrics delay for LRC format lyrics in 1/10 seconds. Floating number, may be negative<>',
	'alwaysreplacegenre<>bool<>If set to true, when the songs are added to the library, XBMC will automatically replace the song genre by "Karaoke" if the song has associated lyrics. Default is false.<>', 
	'storedelay<>bool<>If set to true, when the music-lyrics delay was modified while playing using subtitle delay buttons, the delay value for this song will be stored, and restored when the song is played next time. Default is true.<>',
	'autoassignstartfrom<>num<>When karaoke songs are added to the library during scans, an autoincrement number is automatically assigned to each song, starting from the value specified below. Default starts from 1<>', 
	'nocdgbackground<>bool<>If set to true (default), the background for CDG songs is always empty (plain color) no matter what setting is set in defaultbackground below. When setting this to false, then one can see through the background and see the video or visualization<>'
	'defaultbackground:none<>text<>Sets default background mode. For image/video types the path should specify the image or video file to play<>',
	'defaultbackground:vis<>text<>Sets default background mode. For image/video types the path should specify the image or video file to play<>',
	'defaultbackground:image<>text<>Sets default background mode. For image/video types the path should specify the image or video file to play<>',
	'defaultbackground:video<>text<>Sets default background mode. For image/video types the path should specify the image or video file to play<>',
	'nextsongpopuptime<>text<>If non-zero, specifies the time in seconds left before the end of the current song when a window will pop up informing you about the next played song. The window does not pop up if there is no next song, or it is not a karaoke song<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def photos(name):
    name = 'root'
    dirlist =  ['pictureextensions$add<>text<>A list of additional file-extensions to allow (add) in the My Pictures window. Separate with a space<>', 
	'pictureextensions$remove<>text<>A list of additional file-extensions to remove from the My Pictures window. Separate with a space<>',
	'pictureexcludes$regexp<>text<>Regular expressions that if evaluated to true will not be displayed in My Pictures<>', 
	'slideshow$panamount<>text<>Amount to pan images as a percentage of the screen<>',
	'slideshow$zoomamount<>text<>Amount to zoom images as a percentage of the screen<>'
    'slideshow$blackbarcompensation<>num<>Amount to compensate (zoom) images to attempt to reduce black bars.\nResults in cropping of the longer length of the image in order to reduce the black bars on the shorter length of the image. Defaults to 20<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def networkmenu(name):
    addDir("Samba", 'url',301, '','blank','Samba settings')
    addDir("Network", 'url',302, '','blank','Network client settings')
    addDir("Tuxbox", 'url',303, '','blank','Tuxboc settings')
    name = "root"
    dirlist =  ['ftpshowcache<>bool<>default is false, if set to true, shows cache (X Y Z) partitions in the root directory listing <>', 
	'enableairtunesdebuglog<>bool<>This enables the debug output of libshairport which is used for the AirTunes feature. Defaults to off - because its spamming badly.<>',
	'airtunesport<>num<>This overwrites the defalt listening port of the AirTunes server (announced via zeroconf)<>',
	'airplayport<>num<>This overwrites the default listening port of the AirPlay server (announced via zeroconf)<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def filesystem(name):
    addDir("Path Substitution", 'url',430, '','blank','Path substitutions are for use for redirecting file paths. These are processed in order, and are useful for substituting an absolute path on a PC with a path suitable for XBMC to handle.')
    name = "root"
    dirlist =  ['packagefoldersize<>num<>The amount (in megabytes) of add-on zip packages saved from previous add-on installs. These packages are mainly used for the add-on rollback feature. Increasing the size should increase the amount of past versions saved.<>', 
	'detectasudf<>bool<>Set to true if you wish to detect joint ISO9660/UDF disks as UDF. Default is False<>',
	'virtualshares<>bool<>Set to false to disable virtual shares like plugin, last.fm or shoutcast sources. Default is True<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def pathsubstitution(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['substitute$from<>text<>Substitute from this path. you must set the "To" path below<>', 
	'substitute$to<>text<>Substitute to this path.<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def remotecontrol(name):
    name = "root"
    dirlist =  ['remotedelay<>num<>The repeat delay for a LIRC remote control. A delay value between 1 and 20 before a remote button starts repeating on a long keypress (i.e. continuously sending button pushes while it is held down)  Default: 3<>', 
	'remoterepeat<>num<>This used to adjust the amount of time in milliseconds between repeated keystrokes. Used to prevent key-bounce, in other words prevents xbmc (lirc?) seeing one key press as multiple key presses with certain remotes<>',
	'controllerdeadzone<>text<>The controller deadzone is the region of movement around the center which is not recognized by the device. Because joysticks can have noise (report motion when still) and bias (report an offset when centered), spurious events can be reported even though the controller is not being touched. If you notice these kinds of events, you most likely need to increase your controllers deadzone (both axes recommended). The values range from 0.0 (no deadzone, XBMC will see all input your controller is capable of registering) to 1.0 (XBMC will ignore all input inside of the devices physical limits)<>',
	'enablemultimediakeys<>bool<>This setting only has any effect on Windows versions of XBMC, and only applies to builds from 28th May 2011 onwards. In Windows the multimedia keys generate a WM_APPCOMMAND message in addition the keypress. XBMC processes both keypresses and the WM_APPCOMMAND messages, and the end result would be that the command is executed twice. To avoid this, by default multimedia keypresses are disabled. Although it should rarely be necessary, the enablemultimediakeys setting allows you to enable the multimedia keys<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def interface(name):
    name = "root"
    dirlist =  ['allowd3d9ex<>bool<>Applies only to Windows Vista and up. Values: true/false. Allows xbmc to use Direct3D 9Ex, which is a bit more stable and robust than Direct3D 9<>', 
	'restrictcapsmask<>dialog<>Windows only. A bitmask to prevent xbmc from using detected texture capabilities of the GPU. This helps work around buggy hardware/drivers\n1: prevent the use of compressed textures (DXT1, DXT3, DXT5) 2: prevent the use of non-power-of-two dimensions for textures 4: prevent the use of compressed textures with non-power-of-two dimensions.<>["1","2","4","DISABLED"]',
	'forced3d9ex<>bool<>Windows only: XBMC attempts to detect drivers released for a version earlier than Vista, to avoid using advanced features which are often not emulated correctly. The detection may be incorrect and this setting allows forcing the using of D3D9Ex<>',
	'gui$algorithmdirtyregions<>dialog<>Enable dirty-region processing. Dirty regions are any parts of the screen that have changed since the last frame. By not re-rendering what has not changed, big speed gains can be seen. Because all GPUs work differently, only Mode 3, combined with nofliptimeout=0, is guaranteed to be safe for everyone, but current timing issues with nofliptimeout keep this from being the default\n0: Off-The entire viewport is always rendered\n1:	Union-All dirty regions are grouped into the smallest possible rectangle. This is typically the fastest mode for slower GPUs due to only making one pass.\n2: Cost reduction-Each dirty region is presented separately, in as many passes as there are regions\n3: Whole Screen-The entire screen is rendered if there are any dirty regions. This, combined with nofliptimeout is a safe default for drivers that clear buffer contents (manifests as blinking or vibrating images).<>["0","1","2","3","DISABLED"]',
	'gui$visualizedirtyregions<>bool<>Enable dirty-region visualization. Paints a rectangle over marked controls<>',
	'gui$nofliptimeout<>text<>Specifies the timeout in milliseconds after which XBMC will not flip the graphics buffers anymore when nothing has been rendered, this lowers both CPU and GPU usage\n-1: disabled\n0 or higher: timeout in milliseconds (0 is default)<>',
	'showexitbutton<>bool<>Setting to hide the exit button, useful for people running appliance based setups where exit would only confuse/complicate the user. Modifiable via the advancedsettings.xml by setting showexitbutton to false, default is true (show)<>',
	'screensaver$dimlevel<>num<>To avoid potential worries of plasma screen burn-in, you can set the Dim screensaver fade level to 0% here or in the Settings\n0 will remove the Fade Level control from the settings screen altogether<>',
	'fullscreen<>bool<>Starts XBMC in full screen (check resolutions!)<>',
	'cputempcommand<>text<>Provide a shell command XBMC will use to get CPU temperature. It should print out only "[temp as integer] [scale as one of "CcFf"]"<>',
	'gputempcommand<>text<>Provide a shell command XBMC will use to get GPU temperature. It should print out only "[temp as integer] [scale as one of "CcFf"]"<>',
	'glrectanglehack<>dialog<>Problems with ghosting or videos which are only played back in the left upper quarter? The following ATI hack may solve it<>["yes","DISABLED"]',
	'alwaysontop<>dialog<>Added in XBMC v9.11 (Windows OS only). Keeps XBMC always on top when windowed<>["yes","DISABLED"]']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def unsorted(name):
    name = "masterlock"
    dirlist =  ['startuplock<>bool<>true prompts user for code upon startup\nIf you enable, setting will be removed from UI<>', 
	'automastermode<>bool<>automatically enters master mode if the master code is given\nIf you enable, setting will be removed from UI<>',
	'loginlock<>bool<>whether to use locks on login screen or not\nIf you enable, setting will be removed from UI<>',
	'maxretries<>num<>enter the max number of retries to input code, 3 is default.<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def edl(name):
    name = "edl"
    dirlist =  ['mergeshortcommbreaks<>bool<>If true, commercial breaks will be merged according to the remaining options.<>', 
	'maxcommbreaklength<>num<>Commercial breaks will not be merged if the total length of the commercial break would be greater than this (seconds)<>',
	'mincommbreaklength<>num<>After merging, commercial breaks shorter than this will be removed (seconds)<>',
	'maxcommbreakgap<>num<>Commercial breaks that are further apart than this will not be merged (seconds)<>',
	'commbreakautowait<>num<>How long to wait before automatically skipping when the start of a commercial break reached (seconds)<>',
	'commbreakautowind<>num<>How long to rewind after automatically skipping to the end of the commercial break (seconds)<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def pvr(name):
    name = "pvr"
    dirlist =  ['timecorrection<>num<>Correct all times (epg tags, timer tags, recording tags) by this amount of minutes<>', 
	'infotoggleinterval<>num<>If there is more than one pvr gui info item available (e.g. multiple recordings active at the same time), use this toggle delay in milliseconds<>',
	'minvideocachelevel<>num<>Cache up to this level in the video buffer buffer before resuming playback if the buffers run dry<>',
	'maxvideocachelevel<>num<>Cache up to this level in the audio buffer before resuming playback if the buffers run dry<>',
	'cacheindvdplayer<>bool<>Cache PVR stream in DVDPlayer<>',
	'channeliconsautoscan<>bool<>Automatically scan user defined folder for channel icons when loading internal channel groups<>',
	'autoscaniconsuserset<>bool<>Mark channel icons populated by auto scan as "user set"<>',
	'numericchannelswitchtimeout<>num<>Time in ms before the numeric dialog auto closes when confirmchannelswitch is disabled<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],'')
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def epg(name):
    name = "epg"
    dirlist =  ['lingertime<>num<>keep X minutes of past epg data (default: 24h)<>', 
	'updatecheckinterval<>num<>Check if tables need to be updated every X minutes<>',
	'lingercleanupintervaltime<>num<>Remove old entries from the EPG every X minutes<>',
	'activetagcheckinterval<>num<>Check for updated active tags every X minute<>',
	'retryinterruptedupdateinterval<>num<>Retry an interrupted epg update after X seconds<>',
	'updateemptytagsinterval<>num<>Override user selectable EPG update interval (minutes) for empty EPG tags<>',
	'displayupdatepopup<>bool<>Display a progress popup while updating EPG data from clients<>',
	'displayincrementalupdatepopup<>bool<>also display a progress popup while doing incremental EPG updates<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)

def samba(name):
    name = name.lower()
    dirlist =  ['doscodepage<>text<>code page to use for filenames<>', 
	'clienttimeout<>num<>timeout (in seconds)<>',
	'statfiles<>bool<>Set to false to disable smb stat() on files to speed up listings of large directories (over slow links)<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def tuxbox(name):
    name = name.lower()
    dirlist =  ['audiochannelselection<>bool<>"audiochannelselection"; default is "false", "true" will popup the audio channel selection if there is more then one audio stream<>', 
	'submenuselection<>bool<>"submenuselection"; default is "false", "true" will popup the Submenu selection<>',
	'defaultrootmenu<>dialog<>"defaultrootmenu"; MODE: 0 = TV (Default), 1 = Radio, 2 = Data, 3 = Movies, 4 = Root<>["0","1","2","3","4","DISABLED"]',
	'defaultsubmenu<>dialog<>"defaultsubmenu"; 1=Services  2=Satellites 3=Providers 4=Bouquets (default)<>["1","2","3","4","DISABLED"]',
	'pictureicon<>bool<>"pictureicon"; default is "true", will use the Picture Icons from folder /UserData/PictureIcon/<>',
	'epgrequesttime<>num<>"epgrequesttime"; default is "10", 0-3600, defines the time in seconds between epg queries, some tuxbox devices need longer to response (Minimum: 1, Maximum: 3600)<>',
	'zapwaittime<>num<>"zapwaittime"; default is "0" (0 = OFF), defines the time in seconds to wait for a valid PMT after the zaping was send (Minimum: 0, Maximum: 120)<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)

def network(name):
    name = name.lower()
    dirlist =  ['curlclienttimeout<>num<>Timeout in seconds for libcurl (http/ftp) connections<>', 
	'curllowspeedtime<>num<>Time in seconds for libcurl to consider a connection lowspeed<>',
	'httpproxyusername<>text<>username for Basic Proxy Authentication<>',
	'httpproxypassword<>text<>password for Basic Proxy Authentication<>',
	'cachemembuffersize<>text<>Number of bytes used for buffering streams ahead in memory XBMC will not buffer ahead more than this. WARNING: for the bytes set here, XBMC will consume 3x the amount of RAM. When set to 0 the cache will be written to disk instead of RAM, as of v12 Frodo \nRemember, 1MB = 1,048,576 bytes<>',
	'buffermode<>dialog<>Choose what to buffer: 0) Buffer all internet filesystems (like "2" but additionally also ftp, webdav, etc.) (default) 1) Buffer all filesystems (including local) 2) Only buffer true internet filesystems (streams) (http, etc.) 3) No buffer<>["0","1","2","3","DISABLED"]',
	'readbufferfactor<>text<>This factor determines the max readrate in terms of readbufferfactor * avg bitrate of a video file.This can help on bad connections to keep the cache filled. It will also greatly speed up buffering. Default value 1.0<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def jsonrpc(name):
    dirlist =  ['compactoutput<>bool<>Prettify json output<>', 
	'tcpport<>num<>Change the default TCP port used by XBMC for JSON RPC (which is 9090) to any other valid port<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def video(name):
    name = name.lower()
    addDir("Adjust Refresh Rate", 'url',202, '','blank','Settings for when "Adjust refreshrate to match video fps" is enabled. "Adjust refreshrate to match video fps" will try to select the best refreshrate for the video fps but it does not always get it right, for example it might switch to an unsupported refreshrate. You can add overrides here to switch to a certain refreshrate based on video fps. It is possible to add as many overrides as you need. Overrides are processed in order, if the first one does not match the fps or no refreshrates match that override, it will try the next one until no overrides are left')
    addDir("Latency", 'url',205, '','blank','Compensate display latency (video lag). Latency is given in msecs.. Requires XBMC 11.0 (Eden) or later.')
    addDir("Stagefright", 'url',206, '','blank','Enable and disable codecs')
    dirlist =  ['subsdelayrange<>num<>Delay range for subtitles, in seconds.<>', 
	'audiodelayrange<>num<>Delay range for audio/video sync, in seconds.<>',
	'smallstepbackseconds<>num<>Length of the small skip back when playing a video<>',
	'usetimeseeking<>bool<>Whether to use time based or percentage based seeking.<>',
	'timeseekforward<>num<>Time to seek forward in seconds when doing a short seek.  Defaults to 30.<>',
	'timeseekbackward<>num_minus<>Time to seek backward in seconds when doing a short seek.  Defaults to -30.<>',
	'timeseekforwardbig<>num<>Time to seek forward in seconds when doing a long seek.  Defaults to 600 (10 minutes).<>',
	'timeseekbackwardbig<>num_minus<>Time to seek forward in seconds when doing a long seek.  Defaults to -600 (10 minutes).<>',
	'percentseekforward<>num<>Amount to seek forward as a percentage, when doing a short seek.  Defaults to 2.<>',
	'percentseekbackward<>num_minus<>Amount to seek backward as a percentage, when doing a short seek.  Defaults to -2.<>',
	'percentseekforwardbig<>num<>Amount to seek forward as a percentage, when doing a long seek.  Defaults to 10.<>',
	'percentseekbackwardbig<>num_minus<>Amount to seek forward as a percentage, when doing a long seek.  Defaults to -10.<>',
	'blackbarcolour<>num<>colour of the black bars (0->255), (black->white) on videos.<>',
	'fullscreenonmoviestart<>bool<>Whether to go to fullscreen or not when starting a movie. Defaults to true.<>',
	'defaultplayer<>text<>Set the default video player: dvdplayer or extplayer.<>',
	'excludefromscan<>text<>Regular expressions that if evaluated to true will not be added to library. Separate each word with a space (" "), string will be converted to correct format<>text',
	'excludefromlisting<>text<>Regular expressions that if evaluated to true will not be displayed in Files View. Separate each word with a space (" "), string will be converted to correct format<>text',
	'playcountminimumpercent<>num<>Minimum percentage that has to be played before it is marked as watched. Set to 101 to never auto-mark items as watched<>',
	'ignoresecondsatstart<>num<>Number of seconds to ignore at video start after which a resume point is created<>',
	'ignorepercentatend<>num<>percentage of video to ignore at the end. If you stop watching the video here no resume point is created. Set to 101 to never save a resume point. The video is already marked as watched at 90%, see above "ignoresecondsatstart" setting<>',
	'vdpauscaling<>bool<>scales with vdpau instead of opengl and turns on its HQ scaler when available, enabling this might slow down rendering and cause framedrops especially on ION systems. This setting requires a vdpau feature set C gpu<>',
	'enablehighqualityhwscalers<>bool<>allow turning on the spline36 and lanczos3 shader (for GL builds)<>',
	'ppffmpegdeinterlacing<>text<>override the deinterlacing options passed to libpostproc (i.e. linblenddeint)<>',
	'ppffmpegpostprocessing<>text<>override the post processing options passed to libpostproc when "Video post-processing" is activated in GUI Videos-Settings-Playback (i.e. ha:128:7,va,dr)<>'
	'allowmpeg4vdpau<>bool<>allows mpeg4 decoding with vdpau, currently broken<>',
	'allowmpeg4vaapi<>bool<>allows mpeg4 decoding with vaapi, currently broken on Nvidia cards, not implemented on Intel<>',
	'autoscalemaxfps<>num<>when scaling method is set to auto, bilinear is chosen when the fps is higher than this limit, the default is 30<>',
	'checkdxvacompatibility<>bool<>Advanced setting not present: let xbmc autodetect cards that support H264 profile > L4.1. Set value to false to enable DXVA no matter what. Set value to true if xbmc does not autodetect that the graphics card does not support > L4.1<>',
	'useocclusionquery<>dialog<>Use an occlusion query when capturing videoframes, -1 means auto detect, 0 means disabled, 1 means enabled, the default is -1.<>["-1","0","1","DISABLED"]',
	'fpsdetect<>dialog<>fps detection for video playback, 0 = trust codec fps, 1 = recalculate from video timestamps with uniform spacing, 2 = recalculate from video timestamps always<>["0","1","2","DISABLED"]',
	'stereoscopicregex3d<>textreg<>Filename triggers for 3D (stereoscopic) mode.<>',
	'stereoscopicregexsbs<>textreg<>Filename triggers for 3D (stereoscopic) mode.<>',
	'stereoscopicregextab<>textreg<>Filename triggers for 3D (stereoscopic) mode.<>',
	'disablehi10pmultithreading<>bool<>If you want hi10p decoded only on one CPU, set this to true. It will be renamed to disableswmultithreading in v14 Helix<>']
	
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1], options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def adjustrefreshrates(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['override-av<>override<>Overrides are processed in order, if the first one does not match the fps or no refreshrates match that override, it will try the next one until no overrides are left<>',
	'override-bv<>override<>Overrides are processed in order, if the first one does not match the fps or no refreshrates match that override, it will try the next one until no overrides are left<>',
    'override-range-av<>override_range<>You can also specify the fps range yourself<>',
    'override-range-bv<>override_range<>You can also specify the fps range yourself<>',	
	'fallback-av<>fallback<>Switch to the first found refreshrate<>'
	'fallback-bv<>fallback<>Switch to the first found refreshrate<>'
	'fallback-range-av<>fallback_range<>You can also specify the range for the fallback yourself<>'
	'fallback-range-bv<>fallback_range<>You can also specify the range for the fallback yourself<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2].replace('\n', '').replace('&lt;', '<').replace('&gt;', '>').replace(' ', '')
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1], options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def stagefright(name):
    name = name.lower().replace(' ', '')
    dirlist =  ['useavccodec<>dialog<>-1 is default, 0 is never used this codec, 1 is always use this codec, bypassing blacklist<>["-1","0","1","DISABLED"]',
	'usevc1codec<>dialog<>-1 is default, 0 is never used this codec, 1 is always use this codec, bypassing blacklist<>["-1","0","1","DISABLED"]',
    'usevpxcodec<>dialog<>-1 is default, 0 is never used this codec, 1 is always use this codec, bypassing blacklist<>["-1","0","1","DISABLED"]',
    'usemp4codec<>dialog<>-1 is default, 0 is never used this codec, 1 is always use this codec, bypassing blacklist<>["-1","0","1","DISABLED"]',
	'usempeg2codec<>dialog<>-1 is default, 0 is never used this codec, 1 is always use this codec, bypassing blacklist<>["-1","0","1","DISABLED"]',
	'useswrenderer<>bool<>True or False<>']	
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2].replace('\n', '').replace('&lt;', '<').replace('&gt;', '>').replace(' ', '')
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1], options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def latency(name):
    name = name.lower()
    dirlist =  ['delay-av<>num1<>Global default display latency<>',
    'refresh-rate-av<>num2<>Override latency for given display (not video) refresh rates. When XBMC is in windowed mode, override is ignored. Multiple overrides are allowed<>',	
	'refresh-range-bv<>num3<>Override latency for given range of display (not video) refresh rates. When XBMC is in windowed mode, override is ignored. Multiple overrides are allowed<>']
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2].replace('\n', '').replace('&lt;', '<').replace('&gt;', '>').replace(' ', '')
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1], options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)
	
def audio(name):
    name = name.lower()
    dirlist =  ['headroom<>dialog<>Amount of headroom XBMC should use above the maximum volume level, in decibels.  Defaults to 0, valid values 0, 6, 12.<>["0","6","12","DISABLED"]', 
	'_defaultplayer<>dialog<>Default audio player: paplayer or dvdplayer<>["paplayer","dvdplayer","DISABLED"]',
	'ac3downmixgain<>dialog<>Amount of gain (dB) to be applied to AC3 streams that have been mixed-down to 2 channels. Default is 12.0. Valid values are: -96.0 to 96.0<>["-96","-84","-72","-60","-48","-36","-24","-12","0","12","24","36","48","60","72","84","96","DISABLED"]',
	'_playcountminimumpercent<>num<>Minimum percentage that has to be played before it is considered for incrementing in the Top 100 database view, or for last.fm submittal<>',
	'resample<>num<>Force a specific samplerate to be produced by paplayer to send to the audio hardware, i.e HDMI Audio is usually only capable of 48000<>',
	'applydrc<>bool<>Whether to use DRC on AC3 and DTS streams<>',
	'dvdplayerignoredtsinwav<>bool<>set to true to skip decoding of DTS in wav files when using dvdplayer (10.10 only)<>',
	'limiterhold<>num<>default values for limiter/compressor<>',
	'limiterrelease<>num<>default values for limiter/compressor<>',
	'_excludefromscan<>text<>Regular expressions that if evaluated to true will not be added to library. Separate each word with a space (" "), string will be converted to correct format<>',
	'_excludefromlisting<>text<>Regular expressions that if evaluated to true will not be displayed in Files View. Separate each word with a space (" "), string will be converted to correct format<>',
	'forceDirectSound<>dialog<>Windows-specific - will not use Wasapi API 0 = false, 1 = true<>["0","1","DISABLE"]',
	'audiophile<>dialog<>forces playback of original format, will not down/upmix next song to match current, not compatible with cross-fading 0 = false, 1 = true<>["0","1","DISABLED"]',
	'audiosinkbufferdurationmsec<>num<>Windows-specific, buffer time in msec, hard minimum of 50msec<>',
	'allowtranscode44100<>dialog<>allows 44100hz when trancoding for SPDIF devices 0=false, 1=true<>["0","1","DISABLED"]',
	'streamsilence<>dialog<>Forces original AE behaviour where an audio signal is constantly streamed to the audio device, even if silent. If 1 or true, this prevents some receivers from losing the signal/source, and prevents sinks re-opening and possible receiver switching with each new stream after any silence. If 0 or false, enables Eden-style releasing of the audio device so external players, programs and the system can access the audio device, i.e. prevents XBMC from hogging the audio device.<>["0","1","DISABLED"]']
	
    for d in dirlist:
        splitd=d.split('<>')
        description = splitd[2]
        options = splitd[3]
        currentsetting = ADDON.getSetting(str(splitd[0]))
        if '<>' in currentsetting:
            currentsetting = currentsetting.split('<>')[2]
        if currentsetting == 'DISABLED':
           d = "[COLOR red]%s[/COLOR] (%s)" % (splitd[0], currentsetting)
        else:
            d = "[COLOR lime]%s[/COLOR] (%s)" % (splitd[0], currentsetting) 
        addDirPlayable(d,name,200,currentsetting,description,splitd[1],options)
    setView('movies', 'movies-view')
    xbmc.executebuiltin("Container.SetViewMode(%s)" % VIEW)

def edit_setting(name,url,iconimage,list,options):
    if 'COLOR' in name:
        name = regex_from_to(name, 'COLOR', '/COLOR').replace(' red','').replace(' lime','').replace('[','').replace(']','')
    if list == 'num':
        data = keypad(name,iconimage)
    elif list == 'num1':
        data = keypad_root(name,iconimage)
    elif list == 'num2':
        data = keypad_root2(name,iconimage)
    elif list == 'num3':
        data = keypad_root3(name,iconimage)
    elif list == 'num_minus':
        data = keypad_minus(name,iconimage)
    elif list == 'text':
        data = keyboard(name,iconimage)
    elif list == 'bool':
        data = bool(name)
    elif list == 'dialog':
        data = dialog(name,options)
    elif list == 'override':
        data = override(name,options)
    elif list == 'override_range':
        data = override_range(name,options)
    elif list == 'fallback':
        data = fallback(name,options)
    elif list == 'fallback_range':
        data = fallback_range(name,options)
    if len(data)>0:
        if data != 'DISABLED':
            data = "%s<>%s<>%s" % (url, name, str(data))
        ADDON.setSetting(name, value=str(data))
        xbmc.executebuiltin("Container.Refresh")
	
def write_xml(name,dir_path):
    count = 0
    readsettings = read_from_file(SETTINGS_PATH)
    settings = regex_get_all(readsettings, '<setting', '/>')
    for s in settings:
        try:
            value = regex_from_to(s, 'value="', '"')
            if value != 'DISABLED' and 'id="viewtype"' not in s:
                count = count + 1
        except:
            pass
    if count > 0:
        write_to_file(dir_path, '<!-- Created using Easy Advanced Settings addon -->\n<advancedsettings>\n', False)
        settinglist = ['video&lt;&gt;','audio&lt;&gt;','network&lt;&gt;','edl&lt;&gt;','pvr&lt;&gt;','epg&lt;&gt;','samba&lt;&gt;','videolibrary&lt;&gt;','videodatabase&lt;&gt;','musicdatabase&lt;&gt;','musiclibrary&lt;&gt;','karaoke&lt;&gt;','tuxbox&lt;&gt;','pathsubstitution&lt;&gt;','masterlock&lt;&gt;']
        for s in settinglist:
            buildsection(s, dir_path)
        for s in settings:
            try:
                value = regex_from_to(s, 'value="', '"')
            except:
                pass
            if value != 'DISABLED' and 'id="viewtype"' not in s:
                rootid = value.split('&lt;&gt;')[0]
                id = value.split('&lt;&gt;')[1]
                id1 = id.replace('_','')
                if '$' in id:
                    multi = "two"
                    splitid = id.split('$')
                    id1 = splitid[0]
                    id2 = splitid[1]
                    try:
                        id3 = splitid[2]
                        if len(id3)>0:
                            multi = 'three'
                    except:
                        pass
                else:
                    multi = "one"
                setting = value.split('&lt;&gt;')[2]
                
                if multi == 'two':
                    settingstring = "    <%s>\n        <%s>%s</%s>\n    </%s>\n" % (id1, id2, setting.replace(' ', '|'),id2, id1)
                elif multi == 'three':
                    settingstring = "    <%s>\n        <%s>\n            <%s>%s</%s>\n        </%s>\n    </%s>\n" % (id1, id2, id3,setting.replace(' ', '|'), id3, id2, id1)
                elif rootid == 'root':
                    settingstring = "    <%s>%s</%s>\n" % (id1, setting, id1)
                elif '-av' in id or '-bv' in id or rootid == 'stagefright':
                    id = id.replace('-av','').replace('-bv','').replace('-range','').replace('-rate','')
                    setting = setting.replace('&#x0A;', '\n').replace('&lt;', '<').replace('&gt;', '>')
                    settingstring = "    <%s>\n        <%s>\n            <%s>%s\n            </%s>\n        </%s>\n    </%s>\n" % ('video', rootid,id, setting,id, rootid,'video')
                    if id == 'delay':
                        settingstring = "    <%s>\n        <%s>%s\n        </%s>\n    </%s>\n" % ('video', rootid, setting, rootid,'video')
                    if rootid == 'stagefright':
                        settingstring = "    <%s>\n        <%s>\n            <%s>%s</%s>\n        </%s>\n    </%s>\n" % ('video', rootid, id,setting,id, rootid,'video')
                else:
                    settingstring = "    <%s>\n        <%s>%s</%s>\n    </%s>\n" % (rootid, id1, setting, id1, rootid)
                if rootid not in str(settinglist):#!= 'video' and rootid != 'audio' and rootid != 'network' and rootid != 'edl' and rootid != 'pvr' and rootid != 'samba' and rootid != 'epg'
                    write_to_file(dir_path, settingstring, True)
        write_to_file(dir_path, '</advancedsettings>', True)
    else:
        write_to_file(dir_path, '', False)
    notification('Easy Advanced Settings', 'File created', '4000', iconart)
    xbmc.executebuiltin("Container.Refresh")

def buildsection(settingid, dir_path):
    countsettingid = 0
    setid = settingid.replace('&lt;&gt;','')
    readsettings = read_from_file(SETTINGS_PATH)
    settings = regex_get_all(readsettings, '<setting', '/>')
    for s in settings:
        try:
            value = regex_from_to(s, 'value="', '"')
            if str(settingid) in value:
                countsettingid = countsettingid + 1
        except:
            pass
    if countsettingid > 0:
        write_to_file(dir_path, '    <%s>\n' % setid, True)
        for s in settings:
            try:
                value = regex_from_to(s, 'value="', '"')
            except:
                pass
            if value != 'DISABLED' and 'id="viewtype"' not in s:
                rootid = value.split('&lt;&gt;')[0]
                id = value.split('&lt;&gt;')[1]
                id = id.replace('_','')
                if '$' in id:
                    multi = "two"
                    splitid = id.split('$')
                    id1 = splitid[0]
                    id2 = splitid[1]
                    try:
                        id3 = splitid[2]
                        if len(id3)>0:
                            multi = 'three'
                    except:
                        pass
                else:
                    multi = "one"
                setting = value.split('&lt;&gt;')[2]
                if rootid == setid:
                    if (id == 'excludefromscan' or id == 'excludefromlisting'):
                        settingstring = "        <%s>\n            <regexp>[-\._ ](%s)[-\._ ]</regexp>\n        </%s>\n" % (id, setting.replace(' ', '|'), id)
                    elif multi == 'two':
                        settingstring = "        <%s>\n            <%s>%s</%s>\n        </%s>\n" % (id1, id2, setting.replace(' ', '|'),id2, id1)
                    elif multi == 'three':
                        settingstring = "        <%s>\n            <%s>\n                <%s>%s</%s>\n            </%s>\n        </%s>\n" % (id1, id2, id3,setting.replace(' ', '|'), id3, id2, id1)
                    else:
                        if ":" in id:
                            idsplit = id.split(':')
                            settingstring = '        <%s type="%s" path="%s/>\n' % (idsplit[0], idsplit[1], setting)
                        else:
                            settingstring = "        <%s>%s</%s>\n" % (id, setting, id)
                    write_to_file(dir_path, settingstring, True)
        write_to_file(dir_path, '    </%s>\n' % setid, True)

	
def keypad(name,csetting):
    data = xbmcgui.Dialog().numeric(0,'Enter ' + name + ' value')
    data=int(data)
    if data>0:
        return str(data)
    else:
        return 'DISABLED'
		
def keypad_root(name,csetting):
    data = xbmcgui.Dialog().numeric(0,'Enter latency value')
    data=int(data)
    if data>0:
        data = "\n            <delay>%s</delay>" % data
        return str(data)
    else:
        return 'DISABLED'
		
def keypad_root3(name,csetting):
    data = xbmcgui.Dialog().numeric(0,'Enter MIN rate (Hz) value')
    minrate=int(data)
    if data>0:
        data = xbmcgui.Dialog().numeric(0,'Enter MAX rate (Hz) value')
        maxrate=int(data)
        if data>0:
            data = xbmcgui.Dialog().numeric(0,'Enter delay value')
            delay=int(data)
            if data>0:
                data = "\n                <min>%s</min>\n                <max>%s</max>\n                <delay>%s</delay>" % (minrate,maxrate,delay)
                return str(data)
            else:
                return 'DISABLED'
        else:
            return 'DISABLED'
    else:
        return 'DISABLED'
		
def keypad_root2(name,csetting):
    data = xbmcgui.Dialog().numeric(0,'Enter rate (Hz) value')
    rate=int(data)
    if data>0:
        data = xbmcgui.Dialog().numeric(0,'Enter delay value')
        delay=int(data)
        if data>0:
            data = "\n                <rate>%s</rate>\n                <delay>%s</delay>" % (rate,delay)
            return str(data)
        else:
            return 'DISABLED'
    else:
        return 'DISABLED'
			
def keypad_minus(name,csetting):
    data = xbmcgui.Dialog().numeric(0,'Enter ' + name + ' value')
    data=int(data)
    if data>0:
        return "%s%s" % ('-', str(data))
    else:
        return 'DISABLED'
		
def keyboard(name,csetting):
    keyboard = xbmc.Keyboard(csetting, 'Enter ' + name + ' value', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        data = keyboard.getText()
        if len(data) > 0:
            return data
        else:
            return 'DISABLED'
			
def bool(name):
    dialog = xbmcgui.Dialog()
    action_list = ["True","False", "Disable"]
    action_list_return = ["true","false", "DISABLED"]
    action_id = dialog.select('Select ' + name + ' option', action_list)
    action = action_list_return[action_id]
    if(action_id < 0):
        return "DISABLED"
    else:
        return action
		
def override(name,csetting):
    keyboard = xbmc.Keyboard(csetting, 'Enter fps value', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        fps = keyboard.getText()
        if len(fps) > 0:
            keyboard = xbmc.Keyboard(csetting, 'Enter refresh value', False)
            keyboard.doModal()
            if keyboard.isConfirmed():
                refresh = keyboard.getText()
                if len(refresh) > 0:
                    data = "\n                <fps>%s</fps>\n                <refresh>%s</refresh>" % (fps,refresh)
                    return data
                else:
                    return 'DISABLED'
        else:
            return 'DISABLED'
			
def override_range(name,csetting):
    keyboard = xbmc.Keyboard(csetting, 'Enter MIN fps value', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        fpsmin = keyboard.getText()
        if len(fpsmin) > 0:
            keyboard = xbmc.Keyboard(csetting, 'Enter MAX fps value', False)
            keyboard.doModal()
            if keyboard.isConfirmed():
                fpsmax = keyboard.getText()
                if len(fpsmax) > 0:
                    keyboard = xbmc.Keyboard(csetting, 'Enter MIN refresh value', False)
                    keyboard.doModal()
                    if keyboard.isConfirmed():
                        refreshmin = keyboard.getText()
                        if len(refreshmin) > 0:
                            keyboard = xbmc.Keyboard(csetting, 'Enter MAX refresh value', False)
                            keyboard.doModal()
                            if keyboard.isConfirmed():
                                refreshmax = keyboard.getText()
                                if len(refreshmax) > 0:
                                    data = "\n                <fpsmin>%s</fpsmin>\n                <fpsmax>%s</fpsmax>\n                <refreshmin>%s</refreshmin>\n                <refreshmax>%s</refreshmax>" % (fpsmin,fpsmax,refreshmin,refreshmax)
                                    return data
                                else:
                                    return 'DISABLED'
                        else:
                            return 'DISABLED'                
                else:
                    return 'DISABLED'
        else:
            return 'DISABLED'
			
def fallback(name,csetting):
    keyboard = xbmc.Keyboard(csetting, 'Enter fallback refresh value', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        refresh = keyboard.getText()
        if len(refresh) > 0:
            data = "\n                <refresh>%s</refresh>" % (refresh)
            return data
        else:
            return 'DISABLED'
    else:
        return 'DISABLED'
		
def fallback_range(name,csetting):
    keyboard = xbmc.Keyboard(csetting, 'Enter MIN fallback refresh value', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        refreshmin = keyboard.getText()
        if len(refreshmin) > 0:
            keyboard = xbmc.Keyboard(csetting, 'Enter MAX fallback refresh value', False)
            keyboard.doModal()
            if keyboard.isConfirmed():
                refreshmax = keyboard.getText()
                if len(refreshmax) > 0:
                    data = "\n                <refreshmin>%s</refreshmin>\n                <refreshmax>%s</refreshmax>" % (refreshmin,refreshmax)
                    return data
                else:
                    return 'DISABLED'
        else:
            return 'DISABLED'
		
def dialog(name, options):
    dialog = xbmcgui.Dialog()
    list = regex_get_all(options, '"', '"')
    action_list = list
    action_id = dialog.select('Select ' + name + ' option', action_list)
    action = action_list[action_id]
    if(action_id < 0):
        return "DISABLED"
    else:
        return action
		
def viewxml(name):
    msg = ACTIVESETTINGSFILE
    TextBoxes("[B][COLOR lime]Your advancedsettings.xml file[/B][/COLOR]",msg)

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)" + start_with + "([\S\s]+?)" + end_with, text)
    return r

def strip_text(r, f, t, excluding=True):
    r = re.search("(?i)" + f + "([\S\s]+?)" + t, r).group(1)
    return r


def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)
    xbmc.executebuiltin("Container.Refresh")
    
def remove_from_list(list, file):
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        xbmc.executebuiltin("Container.Refresh")
		
def write_to_file(path, content, append, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None

		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
	
def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
        xbmc.executebuiltin("Container.SetViewMode(504)")
        #xbmc.executebuiltin("Container.SetViewMode(504)")
   

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addDir(name,url,mode,iconimage,list,description):
        suffix = ""
        suffix2 = ""
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+str(iconimage)+"&list="+str(list)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name + suffix + suffix2, iconImage=iconart, thumbnailImage=iconart)
        liz.setProperty('fanart_image', fanart )
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description, 'year': '2014', 'genre': 'Advanced Setings' } )
        setView('movies', 'movies-view')
        #xbmc.executebuiltin("Container.SetViewMode(52)")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirPlayable(name,url,mode,iconimage, description,list,options):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+str(description)+"&list="+str(list)+"&options="+str(options)
        ok=True
        liz=xbmcgui.ListItem(name, iconart, thumbnailImage=iconart)
        liz.setProperty('fanart_image', fanart )
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description, 'year': '2014', 'genre': 'Advanced Setings' } )
        setView('movies', 'movies-view')
        #xbmc.executebuiltin("Container.SetViewMode(502)")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
options=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        start=urllib.unquote_plus(params["start"])
except:
        pass
try:
        list=urllib.unquote_plus(params["list"])
except:
        pass
try:
        options=str(params["options"])
except:
        pass
try:
        description=str(params["description"])
except:
        pass

if mode==None or url==None or len(url)<1:
        #ADDON.setSetting('element', value='advancedsettings')
        MENU(name)
		
elif mode == 499:
        buildmenu(name)
		
elif mode == 498:
        checksettings(name)
		
elif mode == 490:
        removexmlfile(name)
		
elif mode == 489:
        resetsettings(name)
		
elif mode == 10:
        troubleshooting(name)
		
elif mode == 11:
        audiovideo(name)
		
elif mode == 12:
        videolibrary(name)
		
elif mode == 13:
        libraryartwork(name)
		
elif mode == 14:
        videomusiclibrary(name)
		
elif mode == 15:
        music(name)
		
elif mode == 16:
        photos(name)
		
elif mode == 17:
        networkmenu(name)
		
elif mode == 18:
        filesystem(name)
		
elif mode == 19:
        remotecontrol(name)
		
elif mode == 20:
        interface(name)
		
elif mode == 21:
        unsorted(name)
        
elif mode==101:
        jsonrpc(name)
		
elif mode==102:
        video(name)
		
elif mode==103:
        audio(name)
		
elif mode==104:
        edl(name)
		
elif mode==105:
        pvr(name)
		
elif mode==106:
        epg(name)
		
elif mode==115:
        video_library(name)
		
elif mode == 202:
        adjustrefreshrates(name)
		
elif mode == 205:
        latency(name)
		
elif mode == 206:
        stagefright(name)

elif mode==300:
        networksettings(name)
		
elif mode==301:
        samba(name)
		
elif mode==302:
        network(name)
		
elif mode==303:
        tuxbox(name)

elif mode == 200:
    edit_setting(name,url,iconimage,list,options)
	
elif mode==470:
        videodatabase(name)
		
elif mode==471:
       musicdatabase(name)
	   
elif mode==472:
        musiclibrary(name)
		
elif mode==473:
       karaoke(name)

elif mode == 495:
    viewxml(name)
	
elif mode == 430:
    pathsubstitution(name)
	
elif mode == 500:
    write_xml(name,list)
	

		
xbmcplugin.endOfDirectory(int(sys.argv[1]))


