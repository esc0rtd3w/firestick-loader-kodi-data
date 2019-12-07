'''
    USTVnow Plus Add-on

    This version of USTVnow has been built by combining the best of all
    available version of USTVnow found online. This version has been streamlined
    to use the USTVnow API directly to avoid many of the issues in previous versions.

    The following developers have all contributed to this version directly or indirectly.

    mhancoc7, t0mm0, jwdempsey, esxbr, Lunatixz, yrabl, ddurdle

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
'''

import sys, os, re, requests
import urllib, urllib2, socket, cookielib
import json, random
import xbmcgui, xbmc, xbmcvfs
import Addon

import time, datetime

from xml.dom import minidom
from time import time
from datetime import datetime, timedelta


class Ustvnow:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.dlg = xbmcgui.Dialog()
        self.mBASE_URL = 'http://m-api.ustvnow.com'
        self.mcBASE_URL = 'http://mc.ustvnow.com'
        self.mlBASE_URL = 'https://watch.ustvnow.com'

    def build_main(self):
        mode = Addon.plugin_queries['mode']
        Addon.add_directory({'mode': 'live'}, Addon.get_string(30001))
        if Addon.get_setting('show_tv_guide_epg') == 'true':
            Addon.add_directory({'mode': 'tvguide_epg'}, Addon.get_string(40005))
        if Addon.get_setting('show_movies_section') == 'true':
            Addon.add_directory({'mode': 'movies'}, Addon.get_string(40020))
        if Addon.get_setting('show_sports_section') == 'true':
            Addon.add_directory({'mode': 'sports'}, Addon.get_string(40019))
        if Addon.get_setting('rec_live') == 'true':
            Addon.add_directory({'mode': 'dvr'}, Addon.get_string(30101))
        if Addon.get_setting('show_settings_option') == 'true':
            Addon.add_directory({'mode': 'settings'}, Addon.get_string(30002))

        if Addon.get_setting('clear_token') == 'true':
            Addon.set_setting('token', '')
            Addon.set_setting('clear_token', 'false')

    def get_channels(self, quality):
        Addon.log('get_channels,' + str(quality))
        try:
            self._token_check()
            self._account_check()
            self._account_type_check()
            content = self._get_json('gtv/1/live/channelguide', {'token': self.token})
            channels = []
            results = content['results']
            for i in results:
                try:
                    if i['order'] == 1:
                        from datetime import datetime
                        event_date_time = datetime.fromtimestamp(i['ut_start']).strftime('%I:%M %p').lstrip('0')
                        name = Addon.cleanChanName(i['stream_code'])
                        mediatype = i['mediatype']
                        poster_url = self.mcBASE_URL + '/gtv/1/live/viewposter?srsid=' + str(i['srsid']) + '&cs=' + i[
                            'callsign'] + '&tid=' + mediatype
                        mediatype = mediatype.replace('SH', 'tvshow').replace('EP', 'episode').replace('MV',
                                                                                                       'movie').replace(
                            'SP', 'tvshow')
                        rec_url = '/gtv/1/dvr/updatedvr?scheduleid=' + str(
                            i['scheduleid']) + '&token=' + self.token + '&action=add'
                        set_url = '/gtv/1/dvr/updatedvrtimer?connectorid=' + str(i['connectorid']) + '&prgsvcid=' + str(
                            i['prgsvcid']) + '&eventtime=' + str(
                            i['event_time']) + '&token=' + self.token + '&action=add'
                        if Addon.get_setting('free_package') == 'true':
                            if name in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                                channels.append({
                                    'name': name,
                                    'episode_title': i['episode_title'],
                                    'title': i['title'],
                                    'plot': i['description'],
                                    'mediatype': mediatype,
                                    'playable': True,
                                    'poster_url': poster_url,
                                    'rec_url': rec_url,
                                    'set_url': set_url,
                                    'event_date_time': event_date_time
                                })
                        else:
                            channels.append({
                                'name': name,
                                'episode_title': i['episode_title'],
                                'title': i['title'],
                                'plot': i['description'],
                                'mediatype': mediatype,
                                'playable': True,
                                'poster_url': poster_url,
                                'rec_url': rec_url,
                                'set_url': set_url,
                                'event_date_time': event_date_time
                            })
                except:
                    pass
            return channels
        except:
            if Addon.get_setting('activation') == 'true' and Addon.get_setting('renew') == 'true':
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
            exit()

    def get_link(self, get_name, quality):
        Addon.log('get_link,' + str(quality))
        try:
            self._token_check()
            self._account_check()
            content = self._get_json('gtv/1/live/channelguide', {'token': self.token})
            channels = []
            results = content['results'];
            quality = (quality + 1)
            for i in results:
                try:
                    if i['order'] == 1:
                        name = Addon.cleanChanName(i['stream_code'])
                        if name == get_name:
                            json = self._get_json('stream/1/live/view',
                                                  {'token': self.token, 'key': self.passkey, 'scode': i['scode']})
                            stream = json['stream']
                            if quality == 4:
                                url = stream
                            else:
                                url = stream.replace('smil:', 'mp4:').replace('USTVNOW1', 'USTVNOW').replace('USTVNOW',
                                                                                                             'USTVNOW' + str(
                                                                                                                 quality))
                            if Addon.get_setting('free_package') == 'true':
                                if name in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                                    channels.append({
                                        'name': name,
                                        'url': url
                                    })
                            else:
                                channels.append({
                                    'name': name,
                                    'url': url
                                })
                except:
                    pass
            return channels
        except:
            if Addon.get_setting('activation') == 'true' and Addon.get_setting('renew') == 'true':
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
            exit()

    def get_dvr_link(self, get_scheduleid, quality_type, recordings_quality):
        Addon.log('get_dvr_link,' + str(recordings_quality))
        try:
            self._token_check()
            self._account_check()
            content = self._get_json('gtv/1/live/viewdvrlist', {'token': self.token})
            channels = []
            results = content['results'];
            for i in results:
                try:
                    name = Addon.cleanChanName(i['stream_code'])
                    scheduleid = str(i['scheduleid'])
                    if scheduleid == get_scheduleid:
                        json = self._get_json('stream/1/dvr/play',
                                              {'token': self.token, 'key': self.passkey, 'scheduleid': i['scheduleid']})
                        stream = json['stream']
                        if recordings_quality == '950':
                            url = stream
                        else:
                            url = stream.replace('smil:', 'mp4:').replace('.smil',
                                                                          '_' + str(recordings_quality) + '.mp4')
                        if Addon.get_setting('free_package') == 'true':
                            if name in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                                channels.append({
                                    'scheduleid': scheduleid,
                                    'url': url
                                })
                        else:
                            channels.append({
                                'scheduleid': scheduleid,
                                'url': url
                            })
                except:
                    pass
            return channels
        except:
            if Addon.get_setting('activation') == 'true' and Addon.get_setting('renew') == 'true':
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
            exit()

    def get_recordings(self, type='recordings'):
        from datetime import datetime
        Addon.log('get_recordings')
        try:
            self._token_check()
            self._account_check()
            self._account_type_check()
            content = self._get_json('gtv/1/live/viewdvrlist', {'token': self.token})
            recordings = []
            scheduled = []
            recurring = []
            achannels = []
            results = content['results'];
            for i in results:
                chan = Addon.cleanChanName(i['callsign'])
                mediatype = i['connectorid'][:2]
                icon = self.mcBASE_URL + '/gtv/1/live/viewposter?srsid=' + str(i['srsid']) + '&cs=' + i[
                    'callsign'] + '&tid=' + mediatype
                title = i['title']
                plot = i['description']
                plot = plot.replace("&amp;", "&").replace('&quot;', '"')
                orig_air_date = i['orig_air_date']
                event_time = datetime.fromtimestamp(i['ut_start']).strftime('%I:%M %p').lstrip('0')
                event_date_month = datetime.fromtimestamp(i['ut_start']).strftime('%m').lstrip('0')
                event_date_day = datetime.fromtimestamp(i['ut_start']).strftime('%d').lstrip('0')
                event_date_year = datetime.fromtimestamp(i['ut_start']).strftime('%y')
                event_date_name = datetime.fromtimestamp(i['ut_start']).strftime('%A - ')
                event_date_time = event_date_name + event_date_month + '/' + event_date_day + '/' + event_date_year + ' at ' + event_time
                dvrtimertype = i['dvrtimertype']
                event_inprogress = i['event_inprogress']
                if event_inprogress == 0:
                    expire_time = datetime.fromtimestamp(i['ut_expires']).strftime('%I:%M %p').lstrip('0')
                    expire_date_month = datetime.fromtimestamp(i['ut_expires']).strftime('%m').lstrip('0')
                    expire_date_day = datetime.fromtimestamp(i['ut_expires']).strftime('%d').lstrip('0')
                    expire_date_year = datetime.fromtimestamp(i['ut_expires']).strftime('%y')
                    expire_date_name = datetime.fromtimestamp(i['ut_expires']).strftime('%A - ')
                    expire_date_time = expire_date_name + expire_date_month + '/' + expire_date_day + '/' + expire_date_year + ' at ' + expire_time
                rec_date = i['recordedonmmddyyyy']
                synopsis = i['synopsis']
                duration = i['runtime']
                episode_title = i['episode_title']
                app_name = 'dvrrokuplay'
                del_url = '/gtv/1/dvr/updatedvr?scheduleid=' + str(
                    i['scheduleid']) + '&token=' + self.token + '&action=remove'
                remove_url = '/gtv/1/dvr/updatedvrtimer?connectorid=' + str(i['connectorid']) + '&prgsvcid=' + str(
                    i['prgsvcid']) + '&eventtime=' + str(i['event_time']) + '&token=' + self.token + '&action=remove'
                set_url = '/gtv/1/dvr/updatedvrtimer?connectorid=' + str(i['connectorid']) + '&prgsvcid=' + str(
                    i['prgsvcid']) + '&eventtime=' + str(i['event_time']) + '&token=' + self.token + '&action=add'
                datetimestart = datetime.fromtimestamp(i['ut_start']).strftime('%Y-%m-%d %H:%M')

                if (type == 'recordings' and event_inprogress == 0):
                    recordings.append({'channel': chan,
                                       'title': title,
                                       'datetimestart': datetimestart,
                                       'episode_title': episode_title,
                                       'tvshowtitle': title,
                                       'plot': plot,
                                       'rec_date': rec_date,
                                       'icon': icon,
                                       'duration': duration,
                                       'orig_air_date': orig_air_date,
                                       'event_date_time': event_date_time,
                                       'expire_date_time': expire_date_time,
                                       'synopsis': synopsis,
                                       'playable': (event_inprogress == 0),
                                       'del_url': del_url,
                                       'set_url': set_url,
                                       'remove_url': remove_url,
                                       'dvrtimertype': dvrtimertype,
                                       'mediatype': mediatype,
                                       'scheduleid': i['scheduleid']
                                       })
                elif (type == 'scheduled' and event_inprogress != 0):
                    scheduled.append({'channel': chan,
                                      'title': title,
                                      'datetimestart': datetimestart,
                                      'episode_title': episode_title,
                                      'tvshowtitle': title,
                                      'plot': plot,
                                      'rec_date': rec_date,
                                      'icon': icon,
                                      'duration': duration,
                                      'orig_air_date': orig_air_date,
                                      'event_date_time': event_date_time,
                                      'synopsis': synopsis,
                                      'playable': False,
                                      'del_url': del_url,
                                      'set_url': set_url,
                                      'remove_url': remove_url,
                                      'dvrtimertype': dvrtimertype,
                                      'mediatype': mediatype,
                                      })
                elif (type == 'recurring' and dvrtimertype != 0):
                    aChannelname = {'title': title}
                    aChannel = {'title': title}
                    if aChannelname not in achannels:
                        achannels.append(aChannelname)
                        recurring.append({'channel': chan,
                                          'title': title,
                                          'episode_title': episode_title,
                                          'tvshowtitle': title,
                                          'plot': plot,
                                          'rec_date': rec_date,
                                          'icon': icon,
                                          'duration': duration,
                                          'orig_air_date': orig_air_date,
                                          'event_date_time': event_date_time,
                                          'synopsis': synopsis,
                                          'playable': False,
                                          'remove_url': remove_url
                                          })
            if (type == 'recordings'):
                return recordings
            elif (type == 'scheduled'):
                return scheduled
            elif (type == 'recurring'):
                return recurring
            else:
                return []
            return recordings
        except:
            if Addon.get_setting('activation') == 'true' and Addon.get_setting('renew') == 'true':
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
            exit()

    def get_movies(self, quality, type='now'):
        from datetime import datetime
        Addon.log('get_movies' + str(quality))
        try:
            self._token_check()
            self._account_check()
            self._account_type_check()
            content = self._get_json('gtv/1/live/upcoming', {'token': self.token})
            now = []
            today = []
            later = []
            results = content;
            for i in results:
                chan = Addon.cleanChanName(i['callsign'])
                mediatype = i['connectorid'][:2]
                icon = self.mcBASE_URL + '/gtv/1/live/viewposter?srsid=' + str(i['srsid']) + '&cs=' + i[
                    'callsign'] + '&tid=' + mediatype
                title = i['title']
                plot = i['description']
                plot = plot.replace("&amp;", "&").replace('&quot;', '"')
                orig_air_date = i['orig_air_date']
                event_time = datetime.fromtimestamp(i['ut_start']).strftime('%I:%M %p').lstrip('0')
                event_date_month = datetime.fromtimestamp(i['ut_start']).strftime('%m').lstrip('0')
                event_date_day = datetime.fromtimestamp(i['ut_start']).strftime('%d').lstrip('0')
                event_date_year = datetime.fromtimestamp(i['ut_start']).strftime('%y')
                event_date_name = datetime.fromtimestamp(i['ut_start']).strftime('%A - ')
                event_date_time = event_date_name + event_date_month + '/' + event_date_day + '/' + event_date_year + ' at ' + event_time
                event_date_time_now = datetime.fromtimestamp(i['ut_start']).strftime('%I:%M %p').lstrip('0')
                dvrtimertype = i['dvrtimertype']
                event_inprogress = i['event_inprogress']
                timecat = i['timecat']
                synopsis = i['synopsis']
                duration = i['runtime']
                episode_title = i['episode_title']
                app_name = 'dvrrokuplay'
                rec_url = '/gtv/1/dvr/updatedvr?scheduleid=' + str(
                    i['scheduleid']) + '&token=' + self.token + '&action=add'

                if (type == 'now' and event_inprogress == 1):
                    if Addon.get_setting('free_package') == 'true':
                        if chan in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                            now.append({'channel': chan,
                                        'title': title,
                                        'episode_title': episode_title,
                                        'tvshowtitle': title,
                                        'plot': plot,
                                        'icon': icon,
                                        'duration': duration,
                                        'orig_air_date': orig_air_date,
                                        'event_date_time_now': event_date_time_now,
                                        'synopsis': synopsis,
                                        'playable': (event_inprogress == 1),
                                        'dvrtimertype': dvrtimertype,
                                        'mediatype': mediatype,
                                        'rec_url': rec_url
                                        })
                    else:
                        now.append({'channel': chan,
                                    'title': title,
                                    'episode_title': episode_title,
                                    'tvshowtitle': title,
                                    'plot': plot,
                                    'icon': icon,
                                    'duration': duration,
                                    'orig_air_date': orig_air_date,
                                    'event_date_time_now': event_date_time_now,
                                    'synopsis': synopsis,
                                    'playable': (event_inprogress == 1),
                                    'dvrtimertype': dvrtimertype,
                                    'mediatype': mediatype,
                                    'rec_url': rec_url
                                    })
                elif (type == 'today' and event_inprogress != 1 and timecat == 'Today'):
                    if Addon.get_setting('free_package') == 'true':
                        if chan in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                            today.append({'channel': chan,
                                          'title': title,
                                          'episode_title': episode_title,
                                          'tvshowtitle': title,
                                          'plot': plot,
                                          'icon': icon,
                                          'duration': duration,
                                          'orig_air_date': orig_air_date,
                                          'event_date_time': event_date_time,
                                          'synopsis': synopsis,
                                          'playable': (event_inprogress == 1),
                                          'dvrtimertype': dvrtimertype,
                                          'mediatype': mediatype,
                                          'rec_url': rec_url
                                          })
                    else:
                        today.append({'channel': chan,
                                      'title': title,
                                      'episode_title': episode_title,
                                      'tvshowtitle': title,
                                      'plot': plot,
                                      'icon': icon,
                                      'duration': duration,
                                      'orig_air_date': orig_air_date,
                                      'event_date_time': event_date_time,
                                      'synopsis': synopsis,
                                      'playable': (event_inprogress == 1),
                                      'dvrtimertype': dvrtimertype,
                                      'mediatype': mediatype,
                                      'rec_url': rec_url
                                      })
                elif (type == 'later' and event_inprogress != 0 and timecat == 'Tomorrow'):
                    if Addon.get_setting('free_package') == 'true':
                        if chan in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                            later.append({'channel': chan,
                                          'title': title,
                                          'episode_title': episode_title,
                                          'tvshowtitle': title,
                                          'plot': plot,
                                          'icon': icon,
                                          'duration': duration,
                                          'orig_air_date': orig_air_date,
                                          'event_date_time': event_date_time,
                                          'synopsis': synopsis,
                                          'playable': (event_inprogress == 1),
                                          'dvrtimertype': dvrtimertype,
                                          'mediatype': mediatype,
                                          'rec_url': rec_url
                                          })
                    else:
                        later.append({'channel': chan,
                                      'title': title,
                                      'episode_title': episode_title,
                                      'tvshowtitle': title,
                                      'plot': plot,
                                      'icon': icon,
                                      'duration': duration,
                                      'orig_air_date': orig_air_date,
                                      'event_date_time': event_date_time,
                                      'synopsis': synopsis,
                                      'playable': (event_inprogress == 1),
                                      'dvrtimertype': dvrtimertype,
                                      'mediatype': mediatype,
                                      'rec_url': rec_url
                                      })
            if (type == 'now'):
                return now
            elif (type == 'today'):
                return today
            elif (type == 'later'):
                return later
            else:
                return []
            return now
        except:
            if Addon.get_setting('activation') == 'true' and Addon.get_setting('renew') == 'true':
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
            exit()

    def get_sports(self, quality, type='now'):
        Addon.log('get_sports,' + str(quality))
        try:
            self._token_check()
            self._account_check()
            self._account_type_check()
            content = self._get_json('gtv/1/live/channelguide', {'token': self.token})
            now = []
            today = []
            later = []
            results = content['results'];
            import time, datetime
            date_today = datetime.date.today()
            sports = ['Basketball', 'Football', 'Baseball', 'Soccer', 'Tennis', 'Golf', 'Skating', 'Skateboarding',
                      'Skiing', 'Snowboarding', 'Rugby', 'Nascar', 'Bowling', 'Olympics', 'Paralympics']
            for i in results:
                from datetime import datetime
                event_time = datetime.fromtimestamp(i['ut_start']).strftime('%I:%M %p').lstrip('0')
                event_date_month = datetime.fromtimestamp(i['ut_start']).strftime('%m').lstrip('0')
                event_date_day = datetime.fromtimestamp(i['ut_start']).strftime('%d').lstrip('0')
                event_date_year = datetime.fromtimestamp(i['ut_start']).strftime('%y')
                event_date_name = datetime.fromtimestamp(i['ut_start']).strftime('%A - ')
                event_date_time = event_date_name + event_date_month + '/' + event_date_day + '/' + event_date_year + ' at ' + event_time
                event_date_time_now = datetime.fromtimestamp(i['ut_start']).strftime('%I:%M %p').lstrip('0')
                try:
                    if type == 'now' and i['order'] == 1:
                        name = Addon.cleanChanName(i['stream_code'])
                        mediatype = i['mediatype']
                        poster_url = self.mcBASE_URL + '/gtv/1/live/viewposter?srsid=' + str(i['srsid']) + '&cs=' + i[
                            'callsign'] + '&tid=' + mediatype
                        mediatype = mediatype.replace('SH', 'tvshow').replace('EP', 'episode').replace('MV',
                                                                                                       'movie').replace(
                            'SP', 'tvshow')
                        rec_url = '/gtv/1/dvr/updatedvr?scheduleid=' + str(
                            i['scheduleid']) + '&token=' + self.token + '&action=add'
                        set_url = '/gtv/1/dvr/updatedvrtimer?connectorid=' + str(i['connectorid']) + '&prgsvcid=' + str(
                            i['prgsvcid']) + '&eventtime=' + str(
                            i['event_time']) + '&token=' + self.token + '&action=add'
                        if any(i['title'].find(s) >= 0 for s in
                               sports) or name == 'ESPN' or name == 'ESPN2' or name == 'NBCSNHD':
                            if Addon.get_setting('free_package') == 'true':
                                if name in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                                    now.append({
                                        'name': name,
                                        'episode_title': i['episode_title'],
                                        'title': i['title'],
                                        'plot': i['description'],
                                        'mediatype': mediatype,
                                        'playable': True,
                                        'poster_url': poster_url,
                                        'rec_url': rec_url,
                                        'set_url': set_url,
                                        'event_date_time_now': event_date_time_now
                                    })
                            else:
                                now.append({
                                    'name': name,
                                    'episode_title': i['episode_title'],
                                    'title': i['title'],
                                    'plot': i['description'],
                                    'mediatype': mediatype,
                                    'playable': True,
                                    'poster_url': poster_url,
                                    'rec_url': rec_url,
                                    'set_url': set_url,
                                    'event_date_time_now': event_date_time_now
                                })

                    elif type == 'today' and i['order'] != 1 and str(date_today) == str(i['event_date']):
                        name = Addon.cleanChanName(i['stream_code'])
                        mediatype = i['mediatype']
                        poster_url = self.mcBASE_URL + '/gtv/1/live/viewposter?srsid=' + str(i['srsid']) + '&cs=' + i[
                            'callsign'] + '&tid=' + mediatype
                        mediatype = mediatype.replace('SH', 'tvshow').replace('EP', 'episode').replace('MV',
                                                                                                       'movie').replace(
                            'SP', 'tvshow')
                        rec_url = '/gtv/1/dvr/updatedvr?scheduleid=' + str(
                            i['scheduleid']) + '&token=' + self.token + '&action=add'
                        set_url = '/gtv/1/dvr/updatedvrtimer?connectorid=' + str(i['connectorid']) + '&prgsvcid=' + str(
                            i['prgsvcid']) + '&eventtime=' + str(
                            i['event_time']) + '&token=' + self.token + '&action=add'
                        if any(i['title'].find(s) >= 0 for s in
                               sports) or name == 'ESPN' or name == 'ESPN2' or name == 'NBCSNHD':
                            if Addon.get_setting('free_package') == 'true':
                                if name in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                                    today.append({
                                        'name': name,
                                        'episode_title': i['episode_title'],
                                        'title': i['title'],
                                        'plot': i['description'],
                                        'mediatype': mediatype,
                                        'playable': True,
                                        'poster_url': poster_url,
                                        'rec_url': rec_url,
                                        'set_url': set_url,
                                        'event_date_time': event_date_time
                                    })
                            else:
                                today.append({
                                    'name': name,
                                    'episode_title': i['episode_title'],
                                    'title': i['title'],
                                    'plot': i['description'],
                                    'mediatype': mediatype,
                                    'playable': True,
                                    'poster_url': poster_url,
                                    'rec_url': rec_url,
                                    'set_url': set_url,
                                    'event_date_time': event_date_time
                                })

                    elif type == 'later' and i['order'] != 1 and str(date_today) != str(i['event_date']):
                        name = Addon.cleanChanName(i['stream_code'])
                        mediatype = i['mediatype']
                        poster_url = self.mcBASE_URL + '/gtv/1/live/viewposter?srsid=' + str(i['srsid']) + '&cs=' + i[
                            'callsign'] + '&tid=' + mediatype
                        mediatype = mediatype.replace('SH', 'tvshow').replace('EP', 'episode').replace('MV',
                                                                                                       'movie').replace(
                            'SP', 'tvshow')
                        rec_url = '/gtv/1/dvr/updatedvr?scheduleid=' + str(
                            i['scheduleid']) + '&token=' + self.token + '&action=add'
                        set_url = '/gtv/1/dvr/updatedvrtimer?connectorid=' + str(i['connectorid']) + '&prgsvcid=' + str(
                            i['prgsvcid']) + '&eventtime=' + str(
                            i['event_time']) + '&token=' + self.token + '&action=add'
                        if any(i['title'].find(s) >= 0 for s in
                               sports) or name == 'ESPN' or name == 'ESPN2' or name == 'NBCSNHD':
                            if Addon.get_setting('free_package') == 'true':
                                if name in ['CW', 'ABC', 'PBS', 'CBS', 'MY9']:
                                    later.append({
                                        'name': name,
                                        'episode_title': i['episode_title'],
                                        'title': i['title'],
                                        'plot': i['description'],
                                        'mediatype': mediatype,
                                        'playable': True,
                                        'poster_url': poster_url,
                                        'rec_url': rec_url,
                                        'set_url': set_url,
                                        'event_date_time': event_date_time
                                    })
                            else:
                                later.append({
                                    'name': name,
                                    'episode_title': i['episode_title'],
                                    'title': i['title'],
                                    'plot': i['description'],
                                    'mediatype': mediatype,
                                    'playable': True,
                                    'poster_url': poster_url,
                                    'rec_url': rec_url,
                                    'set_url': set_url,
                                    'event_date_time': event_date_time
                                })
                except:
                    pass
            if (type == 'now'):
                return now
            elif (type == 'today'):
                return today
            elif (type == 'later'):
                return later
            else:
                return []
            return now
        except:
            if Addon.get_setting('activation') == 'true' and Addon.get_setting('renew') == 'true':
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
            exit()

    def delete_recording(self, del_url):
        Addon.log('delete_recording')
        html = self._get_html(del_url)
        if 'success' in html:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30017))
        else:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30018))

    def remove_recurring(self, remove_url):
        Addon.log('remove_recurring')
        html = self._get_html(remove_url)
        if 'success' in html:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30020))
        else:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30021))

    def set_recurring(self, set_url):
        Addon.log('set_recurring')
        html = self._get_html(set_url)
        if 'success' in html:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30024))
        else:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30025))

    def record_show(self, rec_url):
        Addon.log('record_show')
        html = self._get_html(rec_url)
        if 'success' in html:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30013))
        else:
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30016))

    def _build_url(self, path, queries={}):
        Addon.log('_build_url')
        if queries:
            query = Addon.build_query(queries)
            return '%s/%s?%s' % (self.mBASE_URL, path, query)
        else:
            return '%s/%s' % (self.mBASE_URL, path)

    def _build_json(self, path, queries={}):
        Addon.log('_build_json')
        if queries:
            query = urllib.urlencode(queries)
            return '%s/%s?%s' % (self.mBASE_URL, path, query)
        else:
            return '%s/%s' % (self.mBASE_URL, path)

    def _fetch(self, url, form_data=False):
        Addon.log('_fetch')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        if form_data:
            req = urllib2.Request(url, form_data)
        else:
            req = url
        try:
            response = opener.open(req)
            return response
        except urllib2.URLError, e:
            return False

    def _get_json(self, path, queries={}):
        Addon.log('_get_json')
        content = False
        url = self._build_json(path, queries)
        response = self._fetch(url)
        if response:
            content = json.loads(response.read())
        else:
            content = False
        return content

    def _get_html(self, path, queries={}):
        Addon.log('_get_html')
        html = False
        url = self._build_url(path, queries)

        response = self._fetch(url)
        if response:
            html = response.read()
        else:
            html = False
        return html

    def randomagent(self):
        BR_VERS = [
            ['%s.0' % i for i in xrange(18, 43)],
            ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111',
             '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
             '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124',
             '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
             '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
            ['11.0']]
        WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1',
                    'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
        FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
        RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                    'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                    'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
        index = random.randrange(len(RAND_UAS))
        return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES),
                                      br_ver=random.choice(BR_VERS[index]))

    def _token_check(self):
        token_check = self._get_json('gtv/1/live/getcustomerkey', {'token': Addon.get_setting('token')})['username']
        if token_check != Addon.get_setting('email'):
            self.token = self._login()
        else:
            try:
                self.token = Addon.get_setting('token')
                self.passkey = self._get_passkey()
            except:
                self.token = self._login()

    def _account_check(self):
        activation_check = self._get_json('gtv/1/live/getuserbytoken', {'token': self.token})['data'][
            'need_account_activation']
        if activation_check == True:
            Addon.set_setting('activation', 'false')
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30031))
            exit()
        else:
            Addon.set_setting('activation', 'true')
        renew_check = self._get_json('gtv/1/live/getuserbytoken', {'token': self.token})['data']['need_account_renew']
        if renew_check == True:
            Addon.set_setting('renew', 'false')
            self.dlg.ok(Addon.get_string(30000), Addon.get_string(30032))
            exit()
        else:
            Addon.set_setting('renew', 'true')

    def _get_passkey(self):
        passkey = self._get_json('gtv/1/live/viewdvrlist', {'token': self.token})['globalparams']['passkey']
        return passkey

    def _account_type_check(self):
        dvr_check = self._get_json('gtv/1/live/getuserbytoken', {'token': self.token})['data']['plan_name']
        if 'DVR' in dvr_check or dvr_check == 'Nittany Plan' or dvr_check == 'Monitoring' or dvr_check == 'Comped All Channel':
            Addon.set_setting('dvr', 'true')
        else:
            Addon.set_setting('dvr', 'false')
        account_type = self._get_json('gtv/1/live/getuserbytoken', {'token': self.token})['data']['plan_free']
        if account_type == 0 or dvr_check == 'Nittany Plan' or dvr_check == 'Monitoring' or dvr_check == 'Comped All Channel':
            Addon.set_setting('free_package', 'false')
        else:
            Addon.set_setting('free_package', 'true')

    def _login(self):
        with requests.Session() as s:

            url = self.mlBASE_URL + "/account/signin"
            r = s.get(url)
            html = r.text
            html = ' '.join(html.split())
            ultimate_regexp = "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>"
            for match in re.finditer(ultimate_regexp, html):
                i = repr(match.group())
                if '<input type="hidden" name="csrf_ustvnow" value="' in i:
                    csrf = i.replace('<input type="hidden" name="csrf_ustvnow" value="', '').replace('">', '')
                    csrf = str(csrf).replace("u'", "").replace("'", "")

            url = self.mlBASE_URL + "/account/login"
            payload = {'csrf_ustvnow': csrf, 'signin_email': self.user, 'signin_password': self.password,
                       'signin_remember': '1'}
            r = s.post(url, data=payload)
            html = r.text
            html = ' '.join(html.split())
            html = html[html.find('var token = "') + len('var token = "'):]
            html = html[:html.find(';') - 1]
            token = str(html)
            if "USTVnow" not in token:
                Addon.set_setting('token', token)
                email = self._get_json('gtv/1/live/getcustomerkey', {'token': Addon.get_setting('token')})['username']
                Addon.set_setting('email', email)
                return token
            else:
                self.dlg.ok(Addon.get_string(30000), Addon.get_string(30011))
