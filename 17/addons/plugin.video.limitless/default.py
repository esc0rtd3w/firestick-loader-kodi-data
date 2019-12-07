# -*- coding: utf-8 -*-
"""
    default.py --- Jen Addon entry point
    Copyright (C) 2017, Jen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import __builtin__
import xbmcaddon

# CONFIGURATION VARIABLES
# -----------------------
addon_id = xbmcaddon.Addon().getAddonInfo('id')
ownAddon = xbmcaddon.Addon(id=addon_id)
enable_installa = ownAddon.getSetting('dlimage')
enable_newswin = ownAddon.getSetting('news_win')
root_xml_url = ownAddon.getSetting('root_xml')
if not 'file:' in root_xml_url and not 'http' in root_xml_url:
    root_xml_url = root_xml_url.decode('base64')
__builtin__.tvdb_api_key = ownAddon.getSetting('tvdb_api_key')
__builtin__.tmdb_api_key = ownAddon.getSetting('tmdb_api_key')
__builtin__.trakt_client_id = ownAddon.getSetting('trakt_api_client_id')
__builtin__.trakt_client_secret = ownAddon.getSetting('trakt_api_client_secret')
__builtin__.search_db_location = ownAddon.getSetting('search_db_location')

__builtin__.login_url = ownAddon.getSetting('login_url')
__builtin__.login_verified = ownAddon.getSetting('login_verified')
__builtin__.user_var = ownAddon.getSetting('user_var')
__builtin__.pwd_var = ownAddon.getSetting('pwd_var')
__builtin__.session_length = ownAddon.getSetting('session_length')

import os
import sys

import koding
import koding.router as router
import weblogin,time,traceback
from resources.lib.installa import Dialog_specific
from resources.lib.news_window import Dialog_Example
import resources.lib.search
import resources.lib.sources
import resources.lib.testings
import resources.lib.util.info
import xbmc,xbmcgui,xbmcplugin
from koding import route
from resources.lib.util.xml import JenList, display_list
import resources.lib.util.views
from resources.lib.plugins import *
from language import get_string as _
from resources.lib.plugin import run_hook


addon_name = xbmcaddon.Addon().getAddonInfo('name')
home_folder = xbmc.translatePath('special://home/')
addon_folder = os.path.join(home_folder, 'addons')
art_path = os.path.join(addon_folder, addon_id)
content_type = "files"

@route("main")
def root():
    try:
        """ check if user has enabled user-login setting """
        use_account = ownAddon.getSetting('use-account')
        display_menu = False 

        if use_account == 'true':
            display_menu = handle_login()

            if display_menu == None:
                return
        else:
            display_menu = True
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Login Exception - Report this to the developer',str(failure))
        pass

    """root menu of the addon"""
    try:
        if display_menu == True:
            if enable_newswin == 'true':
                koding.Add_Dir(name='Latest News And Updates', url='{"my_text":"Latest News[CR]!!!","my_desc":""}', mode='dialog_example', folder=False, icon=os.path.join(art_path,'icon.png'), fanart=os.path.join(art_path,'fanart.jpg'))
            if not get_list(root_xml_url):
                koding.Add_Dir(
                    name=_("Message"),
                    url=_("Sorry, server is down"),
                    mode="message",
                    folder=True,
                    icon=xbmcaddon.Addon().getAddonInfo("icon"),
                    fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
                    content_type="")
                koding.Add_Dir(
                    name=_("Search"),
                    url="",
                    mode="Search",
                    folder=True,
                    icon=xbmcaddon.Addon().getAddonInfo("icon"),
                    fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
                    content_type="")
                koding.Add_Dir(
                    name=_("Testings"),
                    url='{"file_name":"testings.xml"}',
                    mode="Testings",
                    folder=True,
                    icon=xbmcaddon.Addon().getAddonInfo("icon"),
                    fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
                    content_type="")
            if enable_installa =='true':
                koding.Add_Dir(name='Download Backgrounds', url='{"my_text":"INSTALLA[CR]!!!","my_desc":""}', mode='dialog_specific', folder=False, icon=os.path.join(art_path,'icon.png'), fanart=os.path.join(art_path,'fanart.jpg'))
        else:
            koding.Add_Dir(
                name=_("You must be logged in"),
                url=_("You are not logged in"),
                mode="message",
                folder=False,
                icon=xbmcaddon.Addon().getAddonInfo("icon"),
                fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
                content_type="")
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Main Menu Exception - Report this to the developer',str(failure))
        pass


def handle_login():
    try:
        """ get username and password and do login with them """
        """ also get whether to hide successful login notification """
        username = ownAddon.getSetting('username')
        password = ownAddon.getSetting('password')

        login_message_style = ownAddon.getSetting('login_message_style')
        login_welcome_msg = ownAddon.getSetting('login_welcome_msg')
        login_failed_msg = ownAddon.getSetting('login_failed_msg')
        login_required_msg = ownAddon.getSetting('login_required_msg')

        if username == '' or password == '':
            koding.Add_Dir(
                name=_(login_required_msg),
                url=_(login_required_msg),
                mode="message",
                folder=False,
                icon=xbmcaddon.Addon().getAddonInfo("icon"),
                fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
                content_type="") 
            return None

        true_path = koding.Physical_Path(('special://home/addons/%s/' % (addon_id)))
        expiration = ownAddon.getSetting('WEBLOGIN_EXPIRES_AT')
        if time.time() > expiration or expiration == '':
            logged_in = weblogin.verify_login(true_path,username,password)
            if logged_in == True:
                login_message = login_welcome_msg
                expires_at = time.time() + 60 * 60 * int(session_length)
                expiration = expires_at
                ownAddon.setSetting("WEBLOGIN_EXPIRES_AT", str(expires_at))
                display_menu = True
            else:
                login_message = login_failed_msg
                display_menu = False

            if '%s' in login_message:
                login_message = login_message % (username)

            if 'notification' in login_message_style:
                xbmcgui.Dialog().notification('Login Update', login_message,xbmcaddon.Addon().getAddonInfo("icon"), 4000)
            elif 'popup' in login_message_style:
                xbmcgui.Dialog().ok('Login Update', login_message)
        else:
            display_menu = True
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Handle Login Exception - Report this to the developer',str(failure))
        display_menu = False
    return display_menu


@route(mode='get_list_uncached', args=["url"])
def get_list_uncached(url):
    """display jen list uncached"""
    global content_type
    jen_list = JenList(url, cached=False)
    if not jen_list:
        koding.dolog(_("returned empty for ") + url)
    items = jen_list.get_list()
    content = jen_list.get_content_type()
    if items == []:
        return False
    if content:
        content_type = content
    display_list(items, content_type)
    return True


@route(mode="get_list", args=["url"])
def get_list(url):
    """display jen list"""
    global content_type
    jen_list = JenList(url)
    if not jen_list:
        koding.dolog(_("returned empty for ") + url)
    items = jen_list.get_list()
    content = jen_list.get_content_type()
    if items == []:
        return False
    if content:
        content_type = content
    display_list(items, content_type)
    return True


@route(mode="all_episodes", args=["url"])
def all_episodes(url):
    global content_type
    import pickle
    import xbmcgui
    season_urls = pickle.loads(url)
    result_items = []
    dialog = xbmcgui.DialogProgress()
    dialog.create(addon_name, _("Loading items"))
    num_urls = len(season_urls)
    for index, season_url in enumerate(season_urls):
        if dialog.iscanceled():
            break
        percent = ((index + 1) * 100) / num_urls
        dialog.update(percent, _("processing lists"), _("%s of %s") % (
            index + 1,
            num_urls))

        jen_list = JenList(season_url)
        result_items.extend(jen_list.get_list(skip_dialog=True))
    content_type = "episodes"
    display_list(result_items, "episodes")


@route(mode="Settings")
def settings():
    xbmcaddon.Addon().openSettings()


@route(mode="ScraperSettings")
def scraper_settings():
    xbmcaddon.Addon('script.module.universalscrapers').openSettings()


@route(mode="ResolverSettings")
def resolver_settings():
    try:
        import resolveurl
        xbmcaddon.Addon('script.module.resolveurl').openSettings()
    except:
        import urlresolver
        xbmcaddon.Addon('script.module.urlresolver').openSettings()

@route(mode="ClearTraktAccount")
def clear_trakt_account():
    import xbmcgui
    if xbmcgui.Dialog().yesno(addon_name, "{0} Trakt {1}. {2}".format(_("Delete"), _("Settings").lower(), _("Are you sure?"))):
        xbmcaddon.Addon().setSetting("TRAKT_EXPIRES_AT", "")
        xbmcaddon.Addon().setSetting("TRAKT_ACCESS_TOKEN", "")
        xbmcaddon.Addon().setSetting("TRAKT_REFRESH_TOKEN", "")


@route(mode="message", args=["url"])
def show_message(message):
    import xbmcgui
    if len(message) > 80:
        koding.Text_Box(addon_name, message)
    else:
        xbmcgui.Dialog().ok(addon_name, message)


@route('clearCache')
def clear_cache():
    import xbmcgui
    skip_prompt = xbmcaddon.Addon().getSetting("quiet_cache")
    dialog = xbmcgui.Dialog()
    if skip_prompt == 'false':
        if dialog.yesno(addon_name, _("Clear Metadata?")):
            koding.Remove_Table("meta")
            koding.Remove_Table("episode_meta")
        if dialog.yesno(addon_name, _("Clear Scraper Cache?")):
            import universalscrapers
            universalscrapers.clear_cache()
        if dialog.yesno(addon_name, _("Clear GIF Cache?")):
            dest_folder = os.path.join(
                xbmc.translatePath(xbmcaddon.Addon().getSetting("cache_folder")),
                "artcache")
            koding.Delete_Folders(dest_folder)
    else:
        koding.Remove_Table("meta")
        koding.Remove_Table("episode_meta")
        import universalscrapers
        universalscrapers.clear_cache()
        dest_folder = os.path.join(
            xbmc.translatePath(xbmcaddon.Addon().getSetting("cache_folder")),
            "artcache")
        koding.Delete_Folders(dest_folder)

    xbmc.log("running hook: clear cache", xbmc.LOGNOTICE)
    run_hook("clear_cache")
    xbmcgui.Dialog().notification('Clear Cache', 'Cache has been cleared',xbmcaddon.Addon().getAddonInfo("icon"), 4000)


def get_addon_url(mode, url=""):
    import urllib
    result = sys.argv[0] + "?mode=%s" % mode

    if url:
        result += "&url=%s" % urllib.quote_plus(url)
    return result


def first_run_wizard():
    result = run_hook("first_run_wizard")
    if result:
        return


# koding.User_Info()
if xbmcaddon.Addon().getSetting("first_run") == "true":
    first_run_wizard()

foldername = xbmc.getInfoLabel("Container.FolderName")
if foldername in ["", "plugin.program.super.favourites"]:
    __builtin__.JEN_WIDGET = True
else:
    __builtin__.JEN_WIDGET = False

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

router.Run()

xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
try:
    content_type = __builtin__.content_type
except:
    pass
if not xbmcaddon.Addon().getSetting("first_run") == "true":
    if content_type == "files":
        content_type = "other"
    resources.lib.util.views.set_list_view_mode(content_type)
