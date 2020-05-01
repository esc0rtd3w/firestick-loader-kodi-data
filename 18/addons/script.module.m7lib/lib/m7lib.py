"""
    m7lib

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

    Checkout the Free Live TV addon for an example of how to use m7lib
    https://github.com/mhancoc7/kodi-addons/tree/master/_repo/plugin.video.freelivetv.tva
"""

import os
import json
import base64
import re
import xbmc
import xbmcplugin
import xbmcgui
import sys
import string
import random

try:
    # Python 3
    from urllib.request import urlopen, Request
except ImportError:
    # Python 2
    from urllib2 import urlopen, Request

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser

convert_special_characters = HTMLParser()
dlg = xbmcgui.Dialog()

stream_failed = "Unable to get stream. Please try again later."
stream_plug = "aHR0cHM6Ly9tN2xpYi5kZXYvYXBpL2xpdmVfc3RyZWFtcy92MS9nZXRfc3RyZWFtLnBocD9pZD0="
stirr_base = "aHR0cHM6Ly9vdHQtZ2F0ZXdheS1zdGlyci5zaW5jbGFpcnN0b3J5bGluZS5jb20vYXBpL3Jlc3QvdjMvc3RhdHVzLw=="
pluto_base = "aHR0cDovL2FwaS5wbHV0by50di92Mi9jaGFubmVscz9hcHBOYW1lPXdlYiZkZXZpY2VNYWtlPUNocm9tZSZkZXZpY2VUeXBlPXdlYiY="
explore_org_base = "aHR0cHM6Ly9vbWVnYS5leHBsb3JlLm9yZy9hcGkvZ2V0X2NhbV9ncm91cF9pbmZvLmpzb24/aWQ9Nzk="
tubi_tv_base = "aHR0cHM6Ly90dWJpdHYuY29tL296"


class Common:

    @staticmethod
    def dlg_failed(mode):
        dlg.ok(mode, stream_failed)
        exit()

    @staticmethod
    def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
        # Added '# nosec' to suppress bandit warning since this is not used for security/cryptographic purposes.
        return ''.join(random.choice(chars) for x in range(size))  # nosec

    @staticmethod
    # Parse string and extracts first match as a string
    # The default is to find the first match. Pass a 'number' if you want to match a specific match. So 1 would match
    # the second and so forth
    def find_single_match(text, pattern, number=0):
        try:
            matches = re.findall(pattern, text, flags=re.DOTALL)
            result = matches[number]
        except AttributeError:
            result = ""
        return result

    @staticmethod
    # Parse string and extracts multiple matches using regular expressions
    def find_multiple_matches(text, pattern):
        matches = re.findall(pattern, text, re.DOTALL)
        return matches

    @staticmethod
    # Open URL
    def open_url(url, user_agent=True):
        if url.lower().startswith('http'):
            # Added '# nosec' to suppress bandit warnings since the code is not accepting non-http schemes
            req = Request(url)  # nosec
        else:
            raise ValueError
        if user_agent is not False:
            req.add_header('User-Agent',
                           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11'
                           '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        # Added '# nosec' to suppress bandit warnings since the code is not accepting non-http schemes
        response = urlopen(req)  # nosec
        link = response.read()
        response.close()
        return link

    @staticmethod
    # Section, Genre, or Channel logos
    def get_logo(channel, logo_type=None):
        if logo_type is None:
            return xbmc.translatePath(
                os.path.join('special://home/addons/script.module.m7lib', 'lib', 'resources', 'images',
                             channel + ".png"))
        elif logo_type == "section":
            return xbmc.translatePath(
                os.path.join('special://home/addons/script.module.m7lib', 'lib', 'resources', 'images', 'sections',
                             channel + ".png"))
        elif logo_type == "genre":
            return xbmc.translatePath(
                os.path.join('special://home/addons/script.module.m7lib', 'lib', 'resources', 'images', 'genres',
                             channel + ".png"))

    @staticmethod
    # Available channels
    def get_channels():
        channel_list = [
                            {"name": "24-7 Retro", "type": "Retro"},
                            {"name": "Adventure TV", "type": "Lifestyle"},
                            {"name": "Aljazeera", "type": "News"},
                            {"name": "American Classics", "type": "Retro"},
                            {"name": "Antenna TV", "type": "Retro"},
                            {"name": "Big Life TV", "type": "Lifestyle"},
                            {"name": "Black Cinema", "type": "Movies"},
                            {"name": "Bloomberg", "type": "News"},
                            {"name": "Buzzr", "type": "Retro"},
                            {"name": "CBN", "type": "Faith"},
                            {"name": "Charge!", "type": "Action"},
                            {"name": "Cheddar", "type": "News"},
                            {"name": "Classic Arts Showcase", "type": "Music"},
                            {"name": "Classic Movies Channel", "type": "Movies, Retro"},
                            {"name": "Classic Toons TV", "type": "Retro, Kids"},
                            {"name": "Classic TV", "type": "Retro"},
                            {"name": "CMT Westerns", "type": "Movies, Western"},
                            {"name": "Cold Case Files", "type": "Crime, 24-7"},
                            {"name": "CombatGo", "type": "Sports"},
                            {"name": "Comedy Dynamics", "type": "Comedy"},
                            {"name": "Comet", "type": "Sci-Fi"},
                            {"name": "CONtv", "type": "Special Interest"},
                            {"name": "Court TV", "type": "Crime"},
                            {"name": "Crime Network", "type": "Crime"},
                            {"name": "Docurama", "type": "Curiosity, Documentary"},
                            {"name": "Dog the Bounty Hunter", "type": "Crime, 24-7"},
                            {"name": "Dust", "type": "Sci-Fi"},
                            {"name": "Evine", "type": "Shopping"},
                            {"name": "Fail Army", "type": "Special Interest"},
                            {"name": "Fight", "type": "Sports"},
                            {"name": "FilmRise Classic TV", "type": "Retro"},
                            {"name": "FilmRise Free Movies", "type": "Movies"},
                            {"name": "Flicks of Fury", "type": "Movies, Action"},
                            {"name": "Food TV", "type": "Lifestyle"},
                            {"name": "Forensic Files", "type": "Crime, 24-7"},
                            {"name": "FOX Sports", "type": "Sports"},
                            {"name": "France 24", "type": "News"},
                            {"name": "FrontDoor", "type": "Lifestyle"},
                            {"name": "Futurism", "type": "Curiosity, Special Interest"},
                            {"name": "Glewed TV", "type": "Lifestyle"},
                            {"name": "GLORY Kickboxing", "type": "Sports"},
                            {"name": "Gravitas Movies", "type": "Movies"},
                            {"name": "Gusto", "type": "Lifestyle"},
                            {"name": "Hallypop", "type": "Music"},
                            {"name": "Hell's Kitchen", "type": "24-7"},
                            {"name": "HSN", "type": "Shopping"},
                            {"name": "IMPACT Wrestling", "type": "Sports"},
                            {"name": "Jewelry TV", "type": "Shopping"},
                            {"name": "Kitchen Nightmares", "type": "24-7"},
                            {"name": "Live Music Replay", "type": "Music"},
                            {"name": "Made in Hollywood", "type": "Celebrity"},
                            {"name": "Mobcrush", "type": "Special Interest"},
                            {"name": "Movie Mix", "type": "Movies"},
                            {"name": "MST3K", "type": "Comedy, 24-7"},
                            {"name": "Music Baeble", "type": "Music"},
                            {"name": "NASA TV", "type": "Curiosity"},
                            {"name": "NBC News", "type": "News"},
                            {"name": "Newsmax", "type": "News"},
                            {"name": "News Net", "type": "News"},
                            {"name": "Newsy", "type": "News"},
                            {"name": "Outdoor America", "type": "Lifestyle"},
                            {"name": "Outside TV", "type": "Lifestyle"},
                            {"name": "PBS Kids", "type": "Kids"},
                            {"name": "PeopleTV", "type": "Celebrity"},
                            {"name": "Pluto TV Animals", "type": "Curiosity"},
                            {"name": "Pluto TV Biography", "type": "Biography, Curiosity"},
                            {"name": "Pluto TV Comedy", "type": "Movies, Comedy"},
                            {"name": "Pluto TV Conspiracy", "type": "Curiosity"},
                            {"name": "Pluto TV Documentaries", "type": "Documentary, Curiosity"},
                            {"name": "Pluto TV Drama", "type": "Movies"},
                            {"name": "Pluto TV Family", "type": "Movies, Family"},
                            {"name": "Pluto TV History", "type": "Curiosity"},
                            {"name": "Pluto TV Indies", "type": "Movies"},
                            {"name": "Pluto TV Movies", "type": "Movies"},
                            {"name": "Pluto TV Movies 2", "type": "Movies"},
                            {"name": "Pluto TV Romance", "type": "Movies, Romance"},
                            {"name": "Pluto TV Travel", "type": "Lifestyle"},
                            {"name": "Pluto TV Thrillers", "type": "Movies, Thriller"},
                            {"name": "QVC", "type": "Shopping"},
                            {"name": "Retro TV", "type": "Retro"},
                            {"name": "RiffTrax", "type": "Comedy, 24-7"},
                            {"name": "RT News", "type": "News"},
                            {"name": "Shout TV", "type": "Retro"},
                            {"name": "Sky News", "type": "News"},
                            {"name": "Stadium", "type": "Sports"},
                            {"name": "Stand-Up TV", "type": "Comedy"},
                            {"name": "Stirr Action", "type": "Movies, Action"},
                            {"name": "Stirr Biographies", "type": "Biography"},
                            {"name": "Stirr Black Cinema", "type": "Movies"},
                            {"name": "Stirr Comedy", "type": "Movies, Comedy"},
                            {"name": "Stirr Lifestyle", "type": "Lifestyle"},
                            {"name": "Stirr Movies", "type": "Movies"},
                            {"name": "Stirr Music", "type": "Music"},
                            {"name": "Stirr Sports", "type": "Sports"},
                            {"name": "Stirr Travel", "type": "Lifestyle"},
                            {"name": "Stirr Westerns", "type": "Movies, Western"},
                            {"name": "TBD", "type": "Special Interest"},
                            {"name": "Tennis Channel", "type": "Sports"},
                            {"name": "The Asylum", "type": "Movies, Sci-Fi"},
                            {"name": "The Film Detective", "type": "Movies, Retro"},
                            {"name": "The New Detectives", "type": "Crime, 24-7"},
                            {"name": "The Pet Collective", "type": "Special Interest"},
                            {"name": "This TV", "type": "Retro"},
                            {"name": "Unsolved Mysteries", "type": "Crime, 24-7"},
                            {"name": "Voyager Documentaries", "type": "Curiosity, Documentary"},
                            {"name": "World Poker Tour", "type": "Special Interest"}
                        ]

        return channel_list

    @staticmethod
    # Available sections
    def get_sections():
        section_list = ["All Channels", "Genres"]
        return section_list

    @staticmethod
    # Available genres
    def get_genres():
        genre_list = ["24-7", "Action", "Biography", "Celebrity", "Comedy", "Crime", "Curiosity", "Documentary",
                      "Faith", "Family", "Kids", "Lifestyle", "News", "Movies", "Music", "Retro", "Romance", "Sci-Fi",
                      "Shopping", "Special Interest", "Sports", "Thriller", "Western"]
        return genre_list

    @staticmethod
    def add_channel(mode, icon, fanart, title=None, live=True):
        if live is True:
            u = sys.argv[0] + "?mode=" + str(mode) + "&pvr=.pvr"
        else:
            u = sys.argv[0] + "?mode=" + str(mode)
        if title is not None:
            item = title
        else:
            item = mode
        liz = xbmcgui.ListItem(str(item), iconImage=icon, thumbnailImage=icon)
        liz.setArt({'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': fanart})
        liz.setProperty("IsPlayable", "true")
        liz.setInfo('video', {'Title': item})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
        return ok

    @staticmethod
    def add_section(mode, icon, fanart, title=None):
        u = sys.argv[0] + "?mode=" + str(mode) + "&rand=" + Common.random_generator()
        if title is not None:
            item = title
        else:
            item = mode
        liz = xbmcgui.ListItem(str(item), iconImage=icon, thumbnailImage=icon)
        liz.setArt({'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': fanart})
        liz.setProperty("IsPlayable", "true")
        liz.setInfo('video', {'Title': item})
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
        return ok

    @staticmethod
    # Return the Channel ID from YouTube URL
    def get_youtube_channel_id(url):
        return url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]

    @staticmethod
    # Return the full YouTube plugin url
    def get_playable_youtube_url(channel_id):
        return 'plugin://plugin.video.youtube/play/?video_id=%s' % channel_id

    @staticmethod
    # Play stream
    # Optional: set xbmc_player to True to use xbmc.Player() instead of xbmcplugin.setResolvedUrl()
    def play(stream, channel=None, xbmc_player=False):
        if xbmc_player:
            li = xbmcgui.ListItem(channel)
            xbmc.Player().play(stream, li, False)
        else:
            item = xbmcgui.ListItem(channel, path=stream)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

    @staticmethod
    # Get and Play stream
    def get_stream_and_play(mode):
        stream = None
        if mode == "24-7 Retro":
            stream = Stream.twenty_four_seven_retro()

        elif mode == "Adventure TV":
            stream = Stream.adventure_tv()

        elif mode == "Aljazeera":
            stream = Stream.aljazeera()

        elif mode == "American Classics":
            stream = Stream.american_classics()

        elif mode == "Antenna TV":
            stream = Stream.antenna_tv()

        elif mode == "Big Life TV":
            stream = Stream.big_life_tv()

        elif mode == "Black Cinema":
            stream = Stream.black_cinema()

        elif mode == "Bloomberg":
            stream = Stream.bloomberg()

        elif mode == "Buzzr":
            stream = Stream.buzzr()

        elif mode == "CBN":
            stream = Stream.cbn()

        elif mode == "Charge!":
            stream = Stream.charge()

        elif mode == "Cheddar":
            stream = Stream.cheddar()

        elif mode == "Classic Arts Showcase":
            stream = Stream.classic_arts_showcase()

        elif mode == "Classic Movies Channel":
            stream = Stream.classic_movies_channel()

        elif mode == "Classic Toons TV":
            stream = Stream.classic_toons_tv()

        elif mode == "Classic TV":
            stream = Stream.classic_tv()

        elif mode == "Cold Case Files":
            stream = Stream.cold_case_files()

        elif mode == "CombatGo":
            stream = Stream.combatgo()

        elif mode == "Comedy Dynamics":
            stream = Stream.comedy_dynamics()

        elif mode == "Comet":
            stream = Stream.comet()

        elif mode == "CONtv":
            stream = Stream.contv()

        elif mode == "Court TV":
            stream = Stream.courttv()

        elif mode == "Crime Network":
            stream = Stream.crime_network()

        elif mode == "Docurama":
            stream = Stream.docurama()

        elif mode == "Dog the Bounty Hunter":
            stream = Stream.dog_the_bounty_hunter()

        elif mode == "Dust":
            stream = Stream.dust()

        elif mode == "Evine":
            stream = Stream.evine()

        elif mode == "Fail Army":
            stream = Stream.fail_army()

        elif mode == "Fight":
            stream = Stream.fight()

        elif mode == "FilmRise Classic TV":
            stream = Stream.filmrise_tv()

        elif mode == "FilmRise Free Movies":
            stream = Stream.filmrise()

        elif mode == "Flicks of Fury":
            stream = Stream.flicks_of_fury()

        elif mode == "Food TV":
            stream = Stream.food_tv()

        elif mode == "Forensic Files":
            stream = Stream.forensic_files()

        elif mode == "FOX Sports":
            stream = Stream.fox_sports()

        elif mode == "France 24":
            stream = Stream.france_24()

        elif mode == "FrontDoor":
            stream = Stream.frontdoor()

        elif mode == "Futurism":
            stream = Stream.futurism()

        elif mode == "Glewed TV":
            stream = Stream.glewed_tv()

        elif mode == "GLORY Kickboxing":
            stream = Stream.glory_kickboxing()

        elif mode == "Gravitas Movies":
            stream = Stream.gravitas_movies()

        elif mode == "Gusto":
            stream = Stream.gusto()

        elif mode == "Hallypop":
            stream = Stream.hallypop()

        elif mode == "Hell's Kitchen":
            stream = Stream.hells_kitchen()

        elif mode == "HSN":
            stream = Stream.hsn()

        elif mode == "IMPACT Wrestling":
            stream = Stream.impact_wrestling()
            if stream is not None:
                Common.play(stream)
            else:
                Common.dlg_failed(mode)

        elif mode == "Jewelry TV":
            stream = Stream.jewelry_tv()

        elif mode == "Kitchen Nightmares":
            stream = Stream.kitchen_nightmares()

        elif mode == "Live Music Replay":
            stream = Stream.live_music_replay()

        elif mode == "Made in Hollywood":
            stream = Stream.made_in_hollywood()

        elif mode == "Mobcrush":
            stream = Stream.mobcrush()

        elif mode == "Movie Mix":
            stream = Stream.movie_mix()

        elif mode == "MST3K":
            stream = Stream.mst3k()

        elif mode == "Music Baeble":
            stream = Stream.music_baeble()

        elif mode == "NASA TV":
            stream = Stream.nasa_tv()

        elif mode == "NBC News":
            stream = Stream.nbc_news()

        elif mode == "Newsmax":
            stream = Stream.newsmax_tv()

        elif mode == "News Net":
            stream = Stream.news_net()

        elif mode == "Newsy":
            stream = Stream.newsy()

        elif mode == "Outdoor America":
            stream = Stream.outdoor_america()

        elif mode == "Outside TV":
            stream = Stream.outside_tv()

        elif mode == "PBS Kids":
            stream = Stream.pbs_kids()

        elif mode == "PeopleTV":
            stream = Stream.peopletv()

        elif mode == "Pluto TV Animals":
            stream = Stream.pluto_tv_animals()

        elif mode == "Pluto TV Biography":
            stream = Stream.pluto_tv_biography()

        elif mode == "Pluto TV Comedy":
            stream = Stream.pluto_tv_comedy()

        elif mode == "Pluto TV Conspiracy":
            stream = Stream.pluto_tv_conspiracy()

        elif mode == "Pluto TV Documentaries":
            stream = Stream.pluto_tv_documentaries()

        elif mode == "Pluto TV Drama":
            stream = Stream.pluto_tv_drama()

        elif mode == "Pluto TV Family":
            stream = Stream.pluto_tv_family()

        elif mode == "Pluto TV History":
            stream = Stream.pluto_tv_history()

        elif mode == "Pluto TV Indies":
            stream = Stream.pluto_tv_indies()

        elif mode == "Pluto TV Movies":
            stream = Stream.pluto_tv_movies()

        elif mode == "Pluto TV Movies 2":
            stream = Stream.pluto_tv_movies_2()

        elif mode == "Pluto TV Romance":
            stream = Stream.pluto_tv_romance()

        elif mode == "Pluto TV Thrillers":
            stream = Stream.pluto_tv_thrillers()

        elif mode == "Pluto TV Travel":
            stream = Stream.pluto_tv_travel()

        elif mode == "CMT Westerns":
            stream = Stream.pluto_tv_westerns()

        elif mode == "QVC":
            stream = Stream.qvc()

        elif mode == "Retro TV":
            stream = Stream.retro_tv()

        elif mode == "RiffTrax":
            stream = Stream.rifftrax()

        elif mode == "RT News":
            stream = Stream.rt()

        elif mode == "Shout TV":
            stream = Stream.shout_tv()

        elif mode == "Sky News":
            stream = Stream.sky_news()

        elif mode == "Stadium":
            stream = Stream.stadium()

        elif mode == "Stand-Up TV":
            stream = Stream.standup_tv()

        elif mode == "Stirr Action":
            stream = Stream.stirr_action()

        elif mode == "Stirr Biographies":
            stream = Stream.stirr_biographies()

        elif mode == "Stirr Black Cinema":
            stream = Stream.stirr_black_cinema()

        elif mode == "Stirr Comedy":
            stream = Stream.stirr_comedy()

        elif mode == "Stirr Lifestyle":
            stream = Stream.stirr_life()

        elif mode == "Stirr Movies":
            stream = Stream.stirr_movies()

        elif mode == "Stirr Music":
            stream = Stream.stirr_music()

        elif mode == "Stirr Sports":
            stream = Stream.stirr_sports()

        elif mode == "Stirr Travel":
            stream = Stream.stirr_travel()

        elif mode == "Stirr Westerns":
            stream = Stream.stirr_westerns()

        elif mode == "TBD":
            stream = Stream.tbd()

        elif mode == "Tennis Channel":
            stream = Stream.tennis_channel()

        elif mode == "This TV":
            stream = Stream.this_tv()

        elif mode == "The Asylum":
            stream = Stream.the_asylum()

        elif mode == "The Film Detective":
            stream = Stream.the_film_detective()

        elif mode == "The New Detectives":
            stream = Stream.the_new_detectives()

        elif mode == "Unsolved Mysteries":
            stream = Stream.unsolved_mysteries()

        elif mode == "The Pet Collective":
            stream = Stream.the_pet_collective()

        elif mode == "Voyager Documentaries":
            stream = Stream.voyager_documentaries()

        elif mode == "World Poker Tour":
            stream = Stream.world_poker_tour()

        if stream is not None:
            Common.play(stream)
        else:
            Common.dlg_failed(mode)


class Stream:

    @staticmethod
    def twenty_four_seven_retro():
        try:
            site_url = "http://www.247retro.com/"
            match_string = 'src:  "(.+?)"'
            req = Common.open_url(site_url).decode("UTF-8")
            stream = Common.find_single_match(req, match_string)
            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def adventure_tv():
        return Stream.pluto("Adventure TV")

    @staticmethod
    def aljazeera():
        try:
            site_url = "https://www.aljazeera.com/live/"
            channel_match_string = '<iframe width="100%" src="(.+?)\&'
            video_match_string = '\'VIDEO_ID\': "(.+?)"'

            # Get AlJazerra YouTube Channel
            req = Common.open_url(site_url).decode("UTF-8")
            channel_url = Common.find_single_match(req, channel_match_string)

            # Get Stream
            req = Common.open_url(channel_url).decode("UTF-8")
            channel_id = Common.find_single_match(req, video_match_string)
            if channel_id is not "":
                return Common.get_playable_youtube_url(channel_id)
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def american_classics():
        return Stream.stirr("american-classics-07-18-2019-202011476")

    @staticmethod
    def antenna_tv():
        return Stream.m7lib("antenna_tv")

    @staticmethod
    def big_life_tv():
        return Stream.stirr("externallinearfeed-03-06-2019-235515534-03-06-2019")

    @staticmethod
    def black_cinema():
        return Stream.pluto("Black Cinema")

    @staticmethod
    def bloomberg():
        return Stream.m7lib("bloomberg")

    @staticmethod
    def buzzr():
        return Stream.stirr("buzzr-wurl-external-08-27-2018")

    @staticmethod
    def cbn():
        return Stream.m7lib("cbn")

    @staticmethod
    def charge():
        return Stream.stirr("externallinearfeed-01-15-2020-201540715-01-15-2020")

    @staticmethod
    def cheddar():
        return Stream.stirr("cheddar-wurl-external")

    @staticmethod
    def classic_arts_showcase():
        try:
            site_url = "http://www.classicartsshowcase.org/watch-classic-arts-showcase/"
            match_string = "hls.loadSource\('(.+?)'"
            req = Common.open_url(site_url).decode("UTF-8")
            stream = Common.find_single_match(req, match_string)
            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def classic_movies_channel():
        return Stream.pluto("Classic Movies Channel")

    @staticmethod
    def classic_toons_tv():
        return Stream.pluto("Classic Toons TV")

    @staticmethod
    def classic_tv():
        return Stream.pluto("Classic TV")

    @staticmethod
    def cold_case_files():
        return Stream.pluto("Cold Case Files")

    @staticmethod
    def combatgo():
        return Stream.stirr("externallinearfeed-07-10-2019-07-10-2019")

    @staticmethod
    def comedy_dynamics():
        return Stream.stirr("externallinearfeed-08-01-2019-08-01-2019")

    @staticmethod
    def comet():
        return Stream.stirr("externallinearfeed-05-21-2019-05-21-2019")

    @staticmethod
    def contv():
        return Stream.stirr("contv-wurl-external-12-03-2018")

    @staticmethod
    def courttv():
        try:
            site_url = "https://www.courttv.com/title/court-tv-live-stream-web/"
            match_string = 'm3u8=(.+?)&'

            # Get stream url
            req = Common.open_url(site_url).decode("UTF-8")
            stream = Common.find_single_match(req, match_string).replace("%3A", ":").replace("%2F","/")

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def crime_network():
        return Stream.pluto("Crime Network")

    @staticmethod
    def docurama():
        return Stream.stirr("externallinearfeed-05-20-2019-05-20-2019")

    @staticmethod
    def dog_the_bounty_hunter():
        return Stream.pluto("Dog the Bounty Hunter")

    @staticmethod
    def dust():
        return Stream.stirr("dust-wurl-external")

    @staticmethod
    def evine():
        try:
            site_url = "https://www.evine.com/onair/watchuslive/"
            stream_match_string = "hlsStream: '(.+?)'"

            # Get stream url
            req = Common.open_url(site_url).decode("UTF-8")
            stream = Common.find_single_match(req, stream_match_string)

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def fail_army():
        return Stream.stirr("fail-army-wurl-external")

    @staticmethod
    def fight():
        return Stream.pluto("Fight")

    @staticmethod
    def filmrise_tv():
        return Stream.stirr("filmrise-classic-tv-09-27-2019")

    @staticmethod
    def filmrise():
        return Stream.stirr("filmrise-free-movies-09-27-2019")

    @staticmethod
    def flicks_of_fury():
        return Stream.pluto("Flicks of Fury")

    @staticmethod
    def food_tv():
        return Stream.pluto("Food TV")

    @staticmethod
    def forensic_files():
        return Stream.pluto("Forensic Files")

    @staticmethod
    def fox_sports():
        return Stream.pluto("FOX Sports")

    @staticmethod
    def france_24():
        try:
            fr24_fr_url = "http://www.france24.com/fr/tv-en-direct-chaine-live"
            fr24_en_url = "http://www.france24.com/en/livefeed"
            fr24_esp_url = "http://www.france24.com/es/tv-en-vivo-live"
            fr24_ar_url = "http://www.france24.com/ar/livefeed"
            channel_id_match_string = 'src="https://www.youtube.com(.+?)&'
            video_match_string = '\'VIDEO_ID\': "(.+?)"'

            # Channel Selection
            source = dlg.select("Choose Channel", [
                "[COLOR lightskyblue]French[/COLOR]",
                "[COLOR lightskyblue]English[/COLOR]",
                "[COLOR lightskyblue]Spanish[/COLOR]",
                "[COLOR lightskyblue]Arabic[/COLOR]"])
            if source == 0:
                channel_url = fr24_fr_url
            if source == 1:
                channel_url = fr24_en_url
            if source == 2:
                channel_url = fr24_esp_url
            if source == 3:
                channel_url = fr24_ar_url
            if source < 0:
                exit()

            # Get France 24 YouTube Channel
            req = Common.open_url(channel_url).decode("UTF-8")
            channel = "https://www.youtube.com" + Common.find_single_match(req, channel_id_match_string)

            # Get Stream
            req = Common.open_url(channel).decode("UTF-8")
            channel_id = Common.find_single_match(req, video_match_string)

            if channel_id is not "":
                return Common.get_playable_youtube_url(channel_id)
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def frontdoor():
        return Stream.pluto("FrontDoor")

    @staticmethod
    def futurism():
        return Stream.stirr("futurism-wurl-external")

    @staticmethod
    def glewed_tv():
        return Stream.stirr("externallinearfeed-09-12-2019-09-12-2019")

    @staticmethod
    def glory_kickboxing():
        return Stream.pluto("GLORY Kickboxing")

    @staticmethod
    def gravitas_movies():
        return Stream.stirr("gravitas-wurl-external")

    @staticmethod
    def gusto():
        return Stream.stirr("externallinearfeed-03-08-2019-021739216-03-08-2019")

    @staticmethod
    def hallypop():
        return Stream.stirr("externallinearfeed-07-11-2019-07-11-2019")

    @staticmethod
    def hells_kitchen():
        return Stream.stirr("hells-kitchen")

    @staticmethod
    def hsn():
        channel_url = ""
        try:
            hsn1_url = "https://www.hsn.com/watch/live"
            hsn2_url = "https://www.hsn.com/watch/live?network=4"
            stream_id_match_string = "watchTemplate.PlayLiveYoutubeVideo\('(.+?)'"
            program_match_string = '<span class="show-title" id="show-title" tabindex="0">(.+?)</span>'

            # Get HSN TV current program info
            req = Common.open_url(hsn1_url).decode("UTF-8")
            hsn1_program = Common.find_single_match(req, program_match_string).replace("&amp;", "&")

            # Get HSN2 TV current program info
            req = Common.open_url(hsn2_url).decode("UTF-8")
            hsn2_program = Common.find_single_match(req, program_match_string).replace("&amp;", "&")

            # Channel Selection
            source = xbmcgui.Dialog().select("Choose Channel", [
                "[COLOR lightskyblue]HSN TV:[/COLOR] " + convert_special_characters.unescape(hsn1_program),
                "[COLOR lightskyblue]HSN2 TV:[/COLOR] " + convert_special_characters.unescape(hsn2_program)
            ])
            if source == 0:
                channel_url = hsn1_url
            elif source == 1:
                channel_url = hsn2_url
            else:
                exit()

            # Get HSN TV or HSN2 TV stream depending on Channel Selection
            req = Common.open_url(channel_url).decode("UTF-8")
            channel_id = Common.find_single_match(req, stream_id_match_string)
            if channel_id is not "":
                return Common.get_playable_youtube_url(channel_id)
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def impact_wrestling():
        return Stream.pluto("IMPACT Wrestling")

    @staticmethod
    def jewelry_tv():
        try:
            embed_url = "https://content.jwplatform.com/players/id2Frx0C-VaWDbo4e.js"
            playlist_match_string = '"playlist": "(.+?)"'

            # Get playlist
            req = Common.open_url(embed_url).decode("UTF-8")
            playlist_url = "https:" + Common.find_single_match(req, playlist_match_string)

            # Get stream url
            req = Common.open_url(playlist_url).decode("UTF-8")
            jewelry_tv_json = json.loads(req)
            stream = jewelry_tv_json["playlist"][0]["sources"][0]["file"]

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def kitchen_nightmares():
        return Stream.stirr("kitchen-nightmares-07-19-2019")

    @staticmethod
    def live_music_replay():
        return Stream.pluto("Live Music Replay")

    @staticmethod
    def made_in_hollywood():
        return Stream.stirr("externallinearfeed-09-16-2019-09-16-2019")

    @staticmethod
    def mobcrush():
        return Stream.stirr("mobcrush-wurl-external")

    @staticmethod
    def movie_mix():
        return Stream.stirr("movie-mix-wurl-external")

    @staticmethod
    def mst3k():
        return Stream.pluto("MST3K")

    @staticmethod
    def music_baeble():
        return Stream.stirr("externallinearfeed-09-27-2019-204104392-09-27-2019")

    @staticmethod
    def nasa_tv():
        try:
            stream = ""
            # Channel Selection
            source = xbmcgui.Dialog().select("Choose Channel", [
                "[COLOR lightskyblue]NASA TV's Media Channel[/COLOR]",
                "[COLOR lightskyblue]Earth Views from the Space Station[/COLOR]",
                "[COLOR lightskyblue]NASA X[/COLOR]",
            ])

            if source == 0:
                # Get NASA TV Media Channel Stream
                req = Common.open_url(
                    base64.b64decode(stream_plug).decode("UTF-8") + 'nasa_tv')
                nasa_tv_json = json.loads(req)
                stream = nasa_tv_json["results"][0]["stream"]

            elif source == 1:
                # Get NASA TV Space Station Channel Stream
                req = Common.open_url(
                    base64.b64decode(stream_plug).decode("UTF-8") + 'nasa_tv_2')
                nasa_tv_2_json = json.loads(req)
                stream = nasa_tv_2_json["results"][0]["stream"]

            elif source == 2:
                # Get NASA X Stream
                stream = Stream.stirr("nasatv-gracenote-external")
            else:
                exit()

            # Play NASA TV stream depending on Channel Selection
            if "m3u8" in stream:
                return stream
            elif "youtube" in stream:
                channel_id = Common.get_youtube_channel_id(stream)
                return Common.get_playable_youtube_url(channel_id)
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def nbc_news():
        return Stream.pluto("NBC News")

    @staticmethod
    def newsmax_tv():
        try:
            site_url = "https://www.newsmaxtv.com/"
            embed_match_string = '"embedUrl": "(.+?)"'
            stream_match_string = 'hlsStreamUrl(.+?)",'

            # Get embed url
            req = Common.open_url(site_url).decode("UTF-8")
            embed_url = Common.find_single_match(req, embed_match_string)

            # Get stream url
            req = Common.open_url(embed_url).decode("UTF-8")
            stream = Common.find_single_match(req, stream_match_string)\
                .replace('\\":\\"', '')\
                .replace('\\\\\\', '')\
                .replace('\\', '')

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def newsy():
        return Stream.stirr("externallinearfeed-09-27-2019-204550290-09-27-2019")

    @staticmethod
    def news_net():
        return Stream.m7lib("news_net")

    @staticmethod
    def outdoor_america():
        return Stream.stirr("outdoor-america-wurl-external")

    @staticmethod
    def outside_tv():
        return Stream.stirr("externallinearfeed-05-30-2019-05-30-2019")

    @staticmethod
    def pbs_kids():
        try:
            json_url = "http://pbskids.org/api/video/v1/livestream"

            # Get stream url
            req = Common.open_url(json_url).decode("UTF-8")
            pbs_kids_json = json.loads(req)
            stream = pbs_kids_json["livestream"]

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def peopletv():
        return Stream.stirr("externallinearfeed-09-26-2019-09-26-2019")

    @staticmethod
    def pluto_tv_animals():
        return Stream.pluto("Pluto TV Animals")

    @staticmethod
    def pluto_tv_biography():
        return Stream.pluto("Pluto TV Biography")

    @staticmethod
    def pluto_tv_comedy():
        return Stream.pluto("Pluto TV Comedy")

    @staticmethod
    def pluto_tv_conspiracy():
        return Stream.pluto("Pluto TV Conspiracy")

    @staticmethod
    def pluto_tv_documentaries():
        return Stream.pluto("Pluto TV Documentaries")

    @staticmethod
    def pluto_tv_drama():
        return Stream.pluto("Pluto TV Drama")

    @staticmethod
    def pluto_tv_family():
        return Stream.pluto("Pluto TV Family")

    @staticmethod
    def pluto_tv_history():
        return Stream.pluto("Pluto TV History")

    @staticmethod
    def pluto_tv_indies():
        return Stream.pluto("Pluto TV Indies")

    @staticmethod
    def pluto_tv_movies():
        return Stream.pluto("Pluto TV Movies")

    @staticmethod
    def pluto_tv_movies_2():
        return Stream.pluto("Pluto TV Movies 2")

    @staticmethod
    def pluto_tv_romance():
        return Stream.pluto("Pluto TV Romance")

    @staticmethod
    def pluto_tv_thrillers():
        return Stream.pluto("Pluto TV Thrillers")

    @staticmethod
    def pluto_tv_travel():
        return Stream.pluto("Pluto TV Travel")

    @staticmethod
    def pluto_tv_westerns():
        return Stream.pluto("CMT Westerns")

    @staticmethod
    def qvc():
        channel_url = ""
        try:
            site_url = "https://www.qvc.com/content/shop-live-tv.html"
            json_match_string = "var oLiveStreams=(.+?),liveDefaultChannel"

            # Get QVC json
            # For some reason setting User Agent breaks things for QVC
            # Send False for user_agent
            req = Common.open_url(site_url, False).decode("UTF-8")
            qvc_json = json.loads(Common.find_single_match(req, json_match_string))

            qvc_url = qvc_json["QVC"]["url"]
            qvc2_url = qvc_json["2CH"]["url"]
            qvc3_url = qvc_json["ONQ"]["url"]
            iq_url = qvc_json["STA"]["url"]

            # Channel Selection
            source = xbmcgui.Dialog().select("Choose Channel", [
                "[COLOR lightskyblue]QVC[/COLOR]",
                "[COLOR lightskyblue]QVC2[/COLOR]",
                "[COLOR lightskyblue]QVC3[/COLOR]",
                "[COLOR lightskyblue]Beauty IQ[/COLOR]"
            ])
            if source == 0:
                channel_url = qvc_url
            elif source == 1:
                channel_url = qvc2_url
            elif source == 2:
                channel_url = qvc3_url
            elif source == 3:
                channel_url = iq_url
            else:
                exit()

            # Play QVC stream depending on Channel Selection
            stream = channel_url
            if "m3u8" in channel_url:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def retro_tv():
        return Stream.m7lib("retro_tv")

    @staticmethod
    def rifftrax():
        return Stream.pluto("RiffTrax")

    @staticmethod
    def rt():
        channel_url = ""
        match_string = ""
        try:
            rt_url = "https://www.rt.com/on-air/"
            rtus_url = "https://www.rt.com/on-air/rt-america-air/"
            rtuk_url = "https://www.rt.com/on-air/rt-uk-air/"
            rtfr_url = "https://francais.rt.com/en-direct"
            rtar_url = "https://arabic.rt.com/live/"
            rtesp_url = "https://actualidad.rt.com/en_vivo"
            rtdoc_url = "https://rtd.rt.com/on-air/"
            stream_id_match_string = "embed/(.+?)\""
            stream_uk_match_string = "embed/(.+?)\""
            stream_france_id_match_string = 'file: "(.+?)"'
            stream_doc_id_match_string = 'url: "(.+?)"'

            # Channel Selection
            source = xbmcgui.Dialog().select("Choose Channel", [
                "[COLOR lightskyblue]RT Global[/COLOR]",
                "[COLOR lightskyblue]RT America[/COLOR]",
                "[COLOR lightskyblue]RT UK[/COLOR]",
                "[COLOR lightskyblue]RT France[/COLOR]",
                "[COLOR lightskyblue]RT Arabic[/COLOR]",
                "[COLOR lightskyblue]RT Spanish[/COLOR]",
                "[COLOR lightskyblue]RT Documentary[/COLOR]"
            ])
            if source == 0:
                channel_url = rt_url
                match_string = stream_id_match_string
            elif source == 1:
                channel_url = rtus_url
                match_string = stream_id_match_string
            elif source == 2:
                channel_url = rtuk_url
                match_string = stream_uk_match_string
            elif source == 3:
                channel_url = rtfr_url
                match_string = stream_france_id_match_string
            elif source == 4:
                channel_url = rtar_url
                match_string = stream_id_match_string
            elif source == 5:
                channel_url = rtesp_url
                match_string = stream_id_match_string
            elif source == 6:
                channel_url = rtdoc_url
                match_string = stream_doc_id_match_string
            else:
                exit()

            # Get RT stream depending on Channel Selection
            req = Common.open_url(channel_url).decode("UTF-8")

            # Use YouTube for RT Spanish Streams
            if source == 0 or source == 1 or source == 2 or source == 4 or source == 5:
                channel_id = Common.find_single_match(req, match_string)
                if channel_id is not "":
                    return Common.get_playable_youtube_url(channel_id)
                else:
                    return None

            # Stream direct for streams other than RT Spanish
            else:
                stream = Common.find_single_match(req, match_string)
                if "m3u8" in stream:
                    return stream
                else:
                    return None
        except StandardError:
            return None

    @staticmethod
    def shout_tv():
        return Stream.stirr("externallinearfeed-03-08-2019-03-08-2019")

    @staticmethod
    def sky_news():
        try:
            site_url = "https://news.sky.com/watch-live"
            match_string = 'embed/(.+?)\?'

            req = Common.open_url(site_url).decode("UTF-8")
            channel_id = Common.find_single_match(req, match_string)
            if channel_id is not "":
                return Common.get_playable_youtube_url(channel_id)
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def stadium():
        try:
            site_url = "http://reachtv.com/live/WATCHSTADIUM"
            stream_match_string = 'var getPlayFile = "(.+?)"'

            # Get Stadium Stream
            req = Common.open_url(site_url).decode("UTF-8")
            stream = Common.find_single_match(req, stream_match_string)

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def standup_tv():
        return Stream.pluto("Stand-Up TV")

    @staticmethod
    def stirr_action():
        return Stream.stirr("stirr-action-movies-09-27-2019")

    @staticmethod
    def stirr_biographies():
        return Stream.stirr("stirr-biographies-10-10-2019")

    @staticmethod
    def stirr_black_cinema():
        return Stream.stirr("stirr-black-cinema-09-30-2019")

    @staticmethod
    def stirr_comedy():
        return Stream.stirr("stirr-comedy")

    @staticmethod
    def stirr_life():
        return Stream.stirr("stirr-life-09-10-2018")

    @staticmethod
    def stirr_movies():
        return Stream.stirr("stirr-movies-internal")

    @staticmethod
    def stirr_music():
        return Stream.stirr("stirr-travel-10-10-2019")

    @staticmethod
    def stirr_sports():
        return Stream.stirr("stirr-sports-09-10-2018")

    @staticmethod
    def stirr_travel():
        return Stream.stirr("stirr-travel-10-10-2019")

    @staticmethod
    def stirr_westerns():
        return Stream.stirr("stirr-westerns")

    @staticmethod
    def tbd():
        return Stream.stirr("externallinearfeed-05-22-2019-05-22-2019")

    @staticmethod
    def tennis_channel():
        return Stream.stirr("free")

    @staticmethod
    def this_tv():
        return Stream.m7lib("this_tv")

    @staticmethod
    def the_asylum():
        return Stream.pluto("The Asylum")

    @staticmethod
    def the_film_detective():
        return Stream.stirr("externallinearfeed-07-18-2019-07-18-2019")

    @staticmethod
    def the_new_detectives():
        return Stream.pluto("The New Detectives")

    @staticmethod
    def unsolved_mysteries():
        return Stream.pluto("Unsolved Mysteries")

    @staticmethod
    def the_pet_collective():
        return Stream.stirr("the-pet-collective-wurl-external")

    @staticmethod
    def voyager_documentaries():
        return Stream.pluto("Voyager Documentaries")

    @staticmethod
    def world_poker_tour():
        return Stream.stirr("world-poker-tour-wurl-external")

    @staticmethod
    def stirr(url_slug):
        try:
            json_url = base64.b64decode(stirr_base).decode('UTF-8') + url_slug

            # Get stream url
            req = Common.open_url(json_url).decode("UTF-8")
            stirr_json = json.loads(req)
            stream = stirr_json["rss"]["channel"]["item"]["media:content"]["url"].strip().replace('\\', '')

            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def pluto(channel):
        try:
            stream = ""
            json_url = base64.b64decode(pluto_base).decode('UTF-8')\
                       + "sid=" + Common.random_generator(18, string.ascii_letters + string.digits) \
                       + "&deviceId=" + Common.random_generator(18, string.ascii_letters + string.digits)

            # Get stream url
            req = Common.open_url(json_url).decode("UTF-8")
            pluto_json = json.loads(req)
            for i in pluto_json:
                if i["name"] == channel:
                    stream = i["stitched"]["urls"][0]["url"]
            if "m3u8" in stream:
                return stream
            else:
                return None
        except StandardError:
            return None

    @staticmethod
    def m7lib(channel):
        try:
            req = Common.open_url(
                base64.b64decode(stream_plug).decode('UTF-8') + channel)
            channel_json = json.loads(req)
            stream = channel_json["results"][0]["stream"]

            if "m3u8" in stream:
                return stream
            elif "youtube" in stream:
                channel_id = Common.get_youtube_channel_id(stream)
                return Common.get_playable_youtube_url(channel_id)
            else:
                return None
        except StandardError:
            return None

    # Begin Explore.org #
    @staticmethod
    def get_explore_org_streams():
        stream_list = []
        url = base64.b64decode(explore_org_base).decode('UTF-8')
        open_url = Common.open_url(url).decode("UTF-8")
        json_results = json.loads(open_url)['data']['feeds']
        for stream in sorted(json_results, key=lambda k: k['title']):
            if stream["is_inactive"] is False and stream["is_offline"] is False and stream["video_id"] is not None:
                if stream["thumb"] == "":
                    icon = "https://i.ytimg.com/vi/" + stream["video_id"] + "/hqdefault.jpg"
                else:
                    icon = stream["thumb"]
                if stream["thumbnail_large_url"] == "":
                    fanart = "https://i.ytimg.com/vi/" + stream["video_id"] + "/hqdefault.jpg"
                else:
                    fanart = stream["thumbnail_large_url"]
                stream_list.append({"id": stream["video_id"], "icon": icon, "fanart": fanart,
                                    "title": stream["title"].encode(encoding='UTF-8', errors='strict')})
        return stream_list
    # End Explore.org #

    # Begin Tubi TV #
    @staticmethod
    def get_tubi_tv_categories():
        cat_list = []
        url = base64.b64decode(tubi_tv_base) + '/containers/'
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)
        for category in range(0, len(json_results['list'])):
            try:
                icon = json_results['hash'][json_results['list'][category]]['thumbnail']
            except StandardError:
                icon = "none"
            cat_list.append({"id": json_results['list'][category],
                             "icon": icon,
                             "title": json_results['hash'][json_results['list'][category]]['title'].encode('UTF-8', 'ignore')})
        return cat_list

    @staticmethod
    def get_tubi_tv_content(category):
        content_list = []
        url = base64.b64decode(tubi_tv_base) + '/containers/' + category + '/content?cursor=1&limit=200'
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)

        for movie in json_results['contents'].keys():
            try:
                content_list.append({"id": json_results['contents'][movie]['id'],
                                     "icon": json_results['contents'][movie]['posterarts'][0],
                                     "title": json_results['contents'][movie]['title'].decode('UTF-8'),
                                     "type": json_results['contents'][movie]['type']})
            except StandardError:
                pass
        return content_list

    @staticmethod
    def get_tubi_tv_episodes(show):
        episode_list = []
        url = base64.b64decode(tubi_tv_base) + '/videos/0' + show + '/content'
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)

        for season in range(0, len(json_results['children'])):
            try:
                for episode in range(0, len(json_results['children'][season]['children'])):
                    episode_list.append({"id": json_results['children'][season]['children'][episode]['id'],
                                         "icon":
                                             json_results['children'][season]['children'][episode]['thumbnails'][0],
                                         "title": json_results['children'][season]['children'][episode]['title'].decode('UTF-8')})
            except StandardError:
                pass
        return episode_list

    @staticmethod
    def get_tubi_tv_search(text):
        search_list = []
        url = base64.b64decode(tubi_tv_base) + '/search/' + text
        req = Common.open_url(url).decode('UTF-8')
        json_results = json.loads(req)

        for result in json_results:
            try:
                search_list.append({"id": result['id'],
                                     "icon": result['posterarts'][0],
                                     "title": result['title'].decode('UTF-8'),
                                     "type": result['type']})
            except StandardError:
                pass
        return search_list

    @staticmethod
    def get_tubi_tv_stream(stream_id):
        req = Common.open_url(base64.b64decode(tubi_tv_base) + '/videos/' + stream_id + '/content')
        return json.loads(req)['url']
    # End Tubi TV #
