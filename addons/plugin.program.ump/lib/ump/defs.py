import xbmcaddon
import xbmc
from os import path

loglevel=1
addon = xbmcaddon.Addon('plugin.program.ump')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )
addon_ldir = path.join(addon_dir,"lib")
addon_pdir = path.join(addon_ldir ,'providers')
addon_bdir = path.join(addon_dir,"resources","backup")
addon_setxml = path.join(addon_dir,"resources","settings.xml")
addon_bsetxml = path.join(addon_bdir,"settings.xml")
addon_ddir = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.ump')
addon_stdir = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.ump/stats')
addon_tdir = xbmc.translatePath('special://home/userdata/addon_data/plugin.program.ump/throttle')
addon_preffile= path.join(xbmc.translatePath('special://home/userdata/addon_data/plugin.program.ump'),"prefs.json")
addon_cookfile= path.join(xbmc.translatePath('special://home/userdata/addon_data/plugin.program.ump'),"cookie")
kodi_ddir = xbmc.translatePath('special://home/userdata/')
kodi_sdir=xbmc.translatePath('special://skin/')
kodi_setxml = xbmc.translatePath('special://home/userdata/advancedsettings.xml')
kodi_bsetxml = path.join(addon_bdir,"advancedsettings.xml")
kodi_favxml = xbmc.translatePath('special://home/userdata/favourites.xml')
kodi_bfavxml = path.join(addon_bdir,"favourites.xml")
kodi_guixml = xbmc.translatePath('special://home/userdata/guisettings.xml')
arturi = "https://offshoregit.com/boogiepop/dataserver/ump/images/"
#arturi = "http://boogie.us.to/dataserver/ump/images/"
#arturi="D:/projects/git/dataserver/dataserver/ump/images/"
addonsxmluri="https://offshoregit.com/boogiepop/repository.boogie.dist/addons.xml"
#content types
CT_AUDIO, CT_IMAGE, CT_VIDEO, CT_UMP = "audio", "image","video","ump" ##content types
LI_CTS={CT_AUDIO:"music",CT_IMAGE:"pictures",CT_VIDEO:"video",CT_UMP:"video"}
LI_SIS={CT_AUDIO:"audio",CT_IMAGE:"video",CT_VIDEO:"video",CT_UMP:"video"}
WID={CT_AUDIO:10502,CT_IMAGE:10002,CT_VIDEO:10025}
#media types
MT_MOVIE="movie"
MT_TVSHOW,MT_SEASON,MT_EPISODE="tvshow","season","episode",
MT_ARTIST,MT_ALBUM,MT_SONG,MT_MUSIC="artist","musicalbum","song","music"
MT_MUSICVIDEO="musicvideo"
MT_SET,MT_NONE="set","none"
MT_MANGA,MT_CHAPTER="manga","chapter"
mediapointer={
         MT_MOVIE:["code"],
         MT_TVSHOW:["code"],
         MT_SEASON:["code","season"],
         MT_EPISODE:["code","season","episode"],
         MT_ARTIST:["artist"],
         MT_ALBUM:["artist","album"],
         MT_SONG:["artist","album","title"],
         MT_MUSIC:["code"],
         MT_MUSICVIDEO:["code","title"],
         MT_SET:["code"],
         MT_NONE:["code"],
         MT_MANGA:["code"],
         MT_CHAPTER:["code","episode"],
         }

#media type to kodi content categories
#files, songs, artists, albums, movies, tvshows, episodes, musicvideos
media_to_cc={
         MT_MOVIE:"movies",
         MT_TVSHOW:"tvshows",
         MT_SEASON:"albums",
         MT_EPISODE:"episodes",
         MT_ARTIST:"artists",
         MT_ALBUM:"albums",
         MT_SONG:"songs",
         MT_MUSIC:"songs",
         MT_MUSICVIDEO:"movies",
         MT_SET:"files",
         MT_NONE:"albums",
         MT_MANGA:"tvshows",
         MT_CHAPTER:"episodes",
             }

VIEW_MODES={
	"list":{
        'skin.confluence': 50,
        'skin.aeon.nox': 50,
        'skin.aeon.nox.5': 50,
        'skin.confluence-vertical': 50,
        'skin.jx720': 50,
        'skin.pm3-hd': 50,
        'skin.rapier': 50,
        'skin.simplicity': 50,
        'skin.slik': 50,
        'skin.touched': 50,
        'skin.transparency': 50,
        'skin.xeebo': 50,
        'skin.estuary': 55,
        'skin.estouchy':500,
		},
	"thumb":{
        'skin.confluence': 500,
        'skin.aeon.nox': 551,
        'skin.aeon.nox.5': 500,
        'skin.confluence-vertical': 500,
        'skin.jx720': 52,
        'skin.pm3-hd': 53,
        'skin.rapier': 50,
        'skin.simplicity': 500,
        'skin.slik': 53,
        'skin.touched': 500,
        'skin.transparency': 53,
        'skin.xeebo': 55,
        'skin.estuary': 500,
        'skin.estouchy':50,
		},
	}