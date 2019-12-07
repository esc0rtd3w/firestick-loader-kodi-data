#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

    service.py for Jen Template
    Copyright (C) 2018

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

    -------------------------------------------------------------

    Version:
        2018-11-15:
            Minor fixes for some cases seen.

        2018-05-21:
            Updated to be self updating via settings.xml - NO Need To Change This File Anymore
            Takes into account if end-user API keys are stored in settings, and doesn't update it
                if they are.

        2018-05-19:
            Updated documentation in Header
            Added ability to disable service after updating API Keys (reduces load on Kodi startup)
            Removed old stuff

    Variables To Change:
        Nothing. Nada. Zilch. Woot!


    Usage:
        Set this in your Jen v1.6 or higher and it should keep your end user's API Keys and Root XML
            in order automatically. Takes into account when user's have entered their own API keys



"""

import os
import re
import traceback
import xbmc
import xbmcaddon
import xbmcgui


addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_name = xbmcaddon.Addon().getAddonInfo('name')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
ownAddon = xbmcaddon.Addon(id=addon_id)

addon_path = xbmc.translatePath(('special://home/addons/%s' % (addon_id))).decode('utf-8')


#######################################################################
# Do Not Change Any Settings Or Code In This File.
#######################################################################


my_settings = {'root_xml': 'file://jen_main.xml'}


def main():
    try:
        get_my_settings()

        current_version = my_settings['current_version']
        if current_version == '':
            current_version = '0'
        enable_notification = ownAddon.getSetting('enable_notification')
        if enable_notification == '' or enable_notification == 'false':
            enable_notification = False
        else:
            enable_notification = True
        disable_after_update = ownAddon.getSetting('disable_service')
        if disable_after_update == '' or disable_after_update == 'false':
            disable_after_update = False
        else:
            disable_after_update = True

        update_version = ownAddon.getSetting('update_ver')
        if update_version == '':
            update_version = '0'

        debug = ownAddon.getSetting('debug')
        if debug == '' or debug == 'false':
            debug = False
        else:
            debug = True

        if int(current_version) > int(update_version):
            if debug:
                pass
            else:
                try:
                    ownAddon.setSetting('root_xml', my_settings['root_xml'])
                except Exception:
                    failure = traceback.format_exc()
                    print('Service Setting Exception - Root XML \n %s' % (str(failure)))
                    pass
            try:
                ownAddon.setSetting('message_xml_url', my_settings['message_xml_url'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Message XML \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('tvdb_api_key', my_settings['tvdb_api_key'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - TVDB API \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('tmdb_api_key', my_settings['tmdb_api_key'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - TMDB API \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('trakt_api_client_id', my_settings['trakt_api_client_id'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Trakt API \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('trakt_api_client_secret', my_settings['trakt_api_client_secret'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Trakt API Secret \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('TRAKT_ACCESS_TOKEN', my_settings['TRAKT_ACCESS_TOKEN'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Trakt API Token \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('TRAKT_EXPIRES_AT', my_settings['TRAKT_EXPIRES_AT'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Trakt API Expires \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('TRAKT_REFRESH_TOKEN', my_settings['TRAKT_REFRESH_TOKEN'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Trakt API Refresh \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('lastfm_api_key', my_settings['lastfm_api_key'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Last.fm API \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('lastfm_secret', my_settings['lastfm_secret'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Last.fm Secret \n %s' % (str(failure)))
                pass
            try:
                ownAddon.setSetting('search_db_location', my_settings['search_db_location'])
            except Exception:
                failure = traceback.format_exc()
                print('Service Setting Exception - Search DB \n %s' % (str(failure)))
                pass

            ownAddon.setSetting('update_ver', current_version)
            ownAddon.setSetting('current_version', current_version)
            if enable_notification:
                xbmcgui.Dialog().notification(addon_name, 'Updated API keys', addon_icon)
    except Exception:
        failure = traceback.format_exc()
        print('Service Main Exception: \n %s' % (str(failure)))
        pass
    if disable_after_update:
        disable_this()


def get_my_settings():
    try:
        settings_xml_path = os.path.join(addon_path, 'resources/settings.xml')
        xml_content = openfile(settings_xml_path)

        try:
            current_version = re.search('id="current_version".+?/>', xml_content)
            if current_version is not None:
                current_version = re.findall('default="(.+?)"', current_version.group())[0]
                my_settings['current_version'] = (current_version if 'visible' not in current_version else '0')
            else:
                my_settings['current_version'] = '0'
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Current Version \n %s' % (str(failure)))
            pass

        try:
            xml_root = re.search('id="root_xml".+?/>', xml_content)
            if xml_root is not None:
                xml_root = re.findall('default="(.+?)"', xml_root.group())[0]
                my_settings['root_xml'] = (xml_root if 'visible' not in xml_root else 'file://main.xml')
            else:
                my_settings['root_xml'] = 'file://main.xml'
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Root XML \n %s' % (str(failure)))
            pass

        try:
            message_xml_url = re.search('id="message_xml_url".+?/>', xml_content)
            if message_xml_url is not None:
                message_xml_url = re.findall('default="(.+?)"', message_xml_url.group())[0]
                my_settings['message_xml_url'] = (
                    message_xml_url if 'visible' not in message_xml_url else 'http://www.example.com/news.xml')
            else:
                my_settings['message_xml_url'] = 'http://www.example.com/news.xml'
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Message XML \n %s' % (str(failure)))
            pass

        try:
            tvdb_api_key = re.search('id="tvdb_api_key".+?/>', xml_content)
            if tvdb_api_key is not None:
                tvdb_api_key = re.findall('default="(.+?)"', tvdb_api_key.group())[0]
                my_settings['tvdb_api_key'] = (tvdb_api_key if 'visible' not in tvdb_api_key else '')
            else:
                my_settings['tvdb_api_key'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - TVDB API \n %s' % (str(failure)))
            pass

        try:
            tmdb_api_key = re.search('id="tmdb_api_key".+?/>', xml_content)
            if tmdb_api_key is not None:
                tmdb_api_key = re.findall('default="(.+?)"', tmdb_api_key.group())[0]
                my_settings['tmdb_api_key'] = (tmdb_api_key if 'visible' not in tmdb_api_key else '')
            else:
                my_settings['tmdb_api_key'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - TMDB API \n %s' % (str(failure)))
            pass

        try:
            trakt_api_client_id = re.search('id="trakt_api_client_id".+?/>', xml_content)
            if trakt_api_client_id is not None:
                trakt_api_client_id = re.findall('default="(.+?)"', trakt_api_client_id.group())[0]
                my_settings['trakt_api_client_id'] = (trakt_api_client_id
                                                      if 'visible' not in trakt_api_client_id else '')
            else:
                my_settings['trakt_api_client_id'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Trakt API \n %s' % (str(failure)))
            pass

        try:
            trakt_api_client_secret = re.search('id="trakt_api_client_secret".+?/>', xml_content)
            if trakt_api_client_secret is not None:
                trakt_api_client_secret = re.findall('default="(.+?)"', trakt_api_client_secret.group())[0]
                my_settings['trakt_api_client_secret'] = (
                    trakt_api_client_secret if 'visible' not in trakt_api_client_secret else '')
            else:
                my_settings['trakt_api_client_secret'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Trakt API Client \n %s' % (str(failure)))
            pass

        try:
            lastfm_api_key = re.search('id="lastfm_api_key".+?/>', xml_content)
            if lastfm_api_key is not None:
                lastfm_api_key = re.findall('default="(.+?)"', lastfm_api_key.group())[0]
                my_settings['lastfm_api_key'] = (lastfm_api_key if 'visible' not in lastfm_api_key else '')
            else:
                my_settings['lastfm_api_key'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Last.fm API \n %s' % (str(failure)))
            pass

        try:
            lastfm_secret = re.search('id="lastfm_secret".+?/>', xml_content)
            if lastfm_secret is not None:
                lastfm_secret = re.findall('default="(.+?)"', lastfm_secret.group())[0]
                my_settings['lastfm_secret'] = (lastfm_secret if 'visible' not in lastfm_secret else '')
            else:
                my_settings['lastfm_secret'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Last.fm API Secret \n %s' % (str(failure)))
            pass

        try:
            search_db_location = re.search('id="search_db_location".+?/>', xml_content)
            if search_db_location is not None:
                search_db_location = re.findall('default="(.+?)"', search_db_location.group())[0]
                my_settings['search_db_location'] = (search_db_location if 'visible' not in search_db_location else '')
            else:
                my_settings['search_db_location'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Search DB \n %s' % (str(failure)))
            pass

        try:
            TRAKT_ACCESS_TOKEN = re.search('id="TRAKT_ACCESS_TOKEN".+?/>', xml_content)
            if TRAKT_ACCESS_TOKEN is not None:
                TRAKT_ACCESS_TOKEN = re.findall('default="(.+?)"', TRAKT_ACCESS_TOKEN.group())[0]
                my_settings['TRAKT_ACCESS_TOKEN'] = (TRAKT_ACCESS_TOKEN if 'visible' not in TRAKT_ACCESS_TOKEN else '')
            else:
                my_settings['TRAKT_ACCESS_TOKEN'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Trakt API Token \n %s' % (str(failure)))
            pass

        try:
            TRAKT_EXPIRES_AT = re.search('id="TRAKT_EXPIRES_AT".+?/>', xml_content)
            if TRAKT_EXPIRES_AT is not None:
                TRAKT_EXPIRES_AT = re.findall('default="(.+?)"', TRAKT_EXPIRES_AT.group())[0]
                my_settings['TRAKT_EXPIRES_AT'] = (TRAKT_EXPIRES_AT if 'visible' not in TRAKT_EXPIRES_AT else '')
            else:
                my_settings['TRAKT_EXPIRES_AT'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Trakt API Expires \n %s' % (str(failure)))
            pass

        try:
            TRAKT_REFRESH_TOKEN = re.search('id="TRAKT_REFRESH_TOKEN".+?/>', xml_content)
            if TRAKT_REFRESH_TOKEN is not None:
                TRAKT_REFRESH_TOKEN = re.findall('default="(.+?)"', TRAKT_REFRESH_TOKEN.group())[0]
                my_settings['TRAKT_REFRESH_TOKEN'] = (TRAKT_REFRESH_TOKEN
                                                      if 'visible' not in TRAKT_REFRESH_TOKEN else '')
            else:
                my_settings['TRAKT_REFRESH_TOKEN'] = ''
        except Exception:
            failure = traceback.format_exc()
            print('Service XML Parse Exception - Trakt API Refresh \n %s' % (str(failure)))
            pass
    except Exception:
        failure = traceback.format_exc()
        print('Service Get My Settings Exception \n %s' % (str(failure)))
        pass


def disable_this():
    addonxml_path = os.path.join(addon_path, 'addon.xml')
    xml_content = openfile(addonxml_path)
    if re.search('xbmc.service', xml_content):
        xml_content = xml_content.replace('xbmc.service', 'xbmc.arrakis')
        savefile(addonxml_path, xml_content)
    else:
        pass


def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'rb')
        contents = fh.read()
        fh.close()
        return contents
    except Exception:
        failure = traceback.format_exc()
        print('Service Open File Exception - %s \n %s' % (path_to_the_file, str(failure)))
        return None


def savefile(path_to_the_file, content):
    try:
        fh = open(path_to_the_file, 'wb')
        fh.write(content)
        fh.close()
    except Exception:
        failure = traceback.format_exc()
        print('Service Save File Exception - %s \n %s' % (path_to_the_file, str(failure)))


if __name__ == '__main__':
    main()
