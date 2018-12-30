"""
    Velocity XBMC Addon
    Copyright (C) 2016 blazetamer

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
import xbmcgui,xbmc,sys
import time
import os
import kodi
import random
import json
from libs import log_utils
from t0mm0.common.addon import Addon
from libs import trakt
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)

ICON_PATH = os.path.join(kodi.get_path(), 'icon.png')
#use_https = kodi.get_setting('use_https') == 'true'
#trakt_timeout = int(kodi.get_setting('trakt_timeout'))

def get_pin():
    AUTH_BUTTON = 200
    LATER_BUTTON = 201
    NEVER_BUTTON = 202
    ACTION_PREVIOUS_MENU = 10
    ACTION_BACK = 92
    CENTER_Y = 6
    CENTER_X = 2
    
    class PinAuthDialog(xbmcgui.WindowXMLDialog):
        auth = False
        
        def onInit(self):
            self.pin_edit_control = self.__add_editcontrol(30, 240, 40, 550)
            self.setFocus(self.pin_edit_control)
            auth = self.getControl(AUTH_BUTTON)
            never = self.getControl(NEVER_BUTTON)
            self.pin_edit_control.controlUp(never)
            self.pin_edit_control.controlLeft(never)
            self.pin_edit_control.controlDown(auth)
            self.pin_edit_control.controlRight(auth)
            auth.controlUp(self.pin_edit_control)
            auth.controlLeft(self.pin_edit_control)
            never.controlDown(self.pin_edit_control)
            never.controlRight(self.pin_edit_control)
            
        def onAction(self, action):
            # print 'Action: %s' % (action.getId())
            if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
                self.close()

        def onControl(self, control):
            # print 'onControl: %s' % (control)
            pass

        def onFocus(self, control):
            # print 'onFocus: %s' % (control)
            pass

        def onClick(self, control):
            # print 'onClick: %s' % (control)
            if control == AUTH_BUTTON:
                print "PIN INPUT"
                if not self.__get_token():
                    kodi.notify(header='Not Authorized',msg='Using Standard Menus',duration=5000,sound=None)
                #self.auth = True

            if control == NEVER_BUTTON:

                #xbmc.executebuiltin('RunPlugin(%s)' % addon.build_plugin_url({'mode':None}))
                kodi.notify(header='Not Authorized',msg='Using Standard Menus',duration=5000,sound=None)

                # kodi.notify(msg=i18n('use_addon_settings'), duration=5000)
                # kodi.set_setting('last_reminder', '-1')

            if control in [AUTH_BUTTON, LATER_BUTTON, NEVER_BUTTON]:
                self.close()
        
        def __get_token(self):
            pin = self.pin_edit_control.getText().strip()
            if pin:
                try:
                    trakt_api=trakt.TraktAPI()
                    trakt_api.authorize(pin=pin)
                    # trakt_api = Trakt_API(use_https=use_https, timeout=trakt_timeout)
                    # result = trakt_api.get_token(pin=pin)
                    # kodi.set_setting('trakt_oauth_token', result['access_token'])
                    # kodi.set_setting('trakt_refresh_token', result['refresh_token'])
                    # profile = trakt_api.get_user_profile(cached=False)
                    # kodi.set_setting('trakt_user', '%s (%s)' % (profile['username'], profile['name']))
                    return True
                except Exception as e:
                    log_utils.log('Trakt Authorization Failed: %s' % (e), log_utils.LOGDEBUG)
                    return False
            return False
        
        # have to add edit controls programatically because getControl() (hard) crashes XBMC on them
        def __add_editcontrol(self, x, y, height, width):
            media_path = os.path.join(kodi.get_path(), 'resources', 'skins', 'Default', 'media')
            temp = xbmcgui.ControlEdit(5, 5, 5, 5, '', font='font12', textColor='0xFFFFFFFF', focusTexture=os.path.join(media_path, 'button-focus2.png'),
                                       noFocusTexture=os.path.join(media_path, 'button-nofocus.png'), _alignment=CENTER_Y | CENTER_X)
            temp.setPosition(x, y)
            temp.setHeight(height)
            temp.setWidth(width)
            self.addControl(temp)
            return temp
        
    dialog = PinAuthDialog('TraktPinAuthDialog.xml', kodi.get_path())
    dialog.doModal()
    # if dialog.auth:
    #     kodi.notify(msg=i18n('trakt_auth_complete'), duration=3000)
    del dialog






class ProgressDialog(object):
    def __init__(self, heading, line1='', line2='', line3='', active=True):
        if active:
            self.pd = xbmcgui.DialogProgress()
            self.pd.create(heading, line1, line2, line3)
            self.pd.update(0)
        else:
            self.pd = None

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd
    
    def is_canceled(self):
        if self.pd is not None:
            return self.pd.iscanceled()
        else:
            return False
        
    def update(self, percent, line1='', line2='', line3=''):
        if self.pd is not None:
            self.pd.update(percent, line1, line2, line3)










# def perform_auto_conf(responses):
#     length = len(responses)
#     TOTAL = 12
#     if length < TOTAL:
#         responses += [True] * (TOTAL - length)
#
#     if responses[0]: kodi.set_setting('trakt_timeout', '60')
#     if responses[1]: kodi.set_setting('calendar-day', '-1')
#     if responses[2]: kodi.set_setting('calendar_time', '2')
#     if responses[3]: kodi.set_setting('source_timeout', '20')
#     if responses[4]: kodi.set_setting('include_watchlist_next', 'true')
#     if responses[5]: kodi.set_setting('filter_direct', 'true')
#     if responses[6]: kodi.set_setting('filter_unusable', 'true')
#     if responses[7]: kodi.set_setting('show_debrid', 'true')
#     if responses[8]: kodi.set_setting('source_results', '0')
#     if responses[9]:
#         kodi.set_setting('enable_sort', 'true')
#         kodi.set_setting('sort1_field', '2')
#         kodi.set_setting('sort2_field', '5')
#         kodi.set_setting('sort3_field', '6')
#         kodi.set_setting('sort4_field', '1')
#         kodi.set_setting('sort5_field', '3')
#         kodi.set_setting('sort6_field', '4')
#
#     if responses[10]:
#         tiers = ['Local', 'Furk.net', 'Premiumize.me', 'EasyNews', 'DD.tv', 'NoobRoom',
#                  ['WatchHD', 'IFlix', 'MoviesPlanet', 'TVWTVS', '9Movies', '123Movies', 'niter.tv', 'HDMovie14', 'ororo.tv'],
#                  ['movietv.to', 'StreamLord', 'tunemovie', 'afdah.org', 'xmovies8', 'xmovies8.v2', 'IzlemeyeDeger', 'alluc.com'],
#                  ['torba.se', 'Rainierland', 'FardaDownload', 'zumvo.com', 'PutMV', 'MiraDeTodo', 'beinmovie', 'FireMoviesHD'],
#                  ['SezonLukDizi', 'Dizimag', 'Dizilab', 'Dizigold', 'Dizibox', 'Diziay', 'Dizipas', 'OneClickTVShows'],
#                  ['DayT.se', 'DDLValley', 'ReleaseBB', 'MyVideoLinks.eu', 'OCW', 'RLSSource.net', 'TVRelease.Net'],
#                  ['IceFilms', 'PrimeWire', 'Flixanity', 'wso.ch', 'WatchSeries', 'UFlix.org', 'Putlocker', 'MovieHut'],
#                  ['funtastic-vids', 'WatchFree.to', 'pftv', 'streamallthis.is', 'Movie4K', 'afdah', 'SolarMovie', 'yify-streaming'],
#                  ['CouchTunerV2', 'CouchTunerV1', 'Watch8Now', 'yshows', 'TwoMovies.us', 'iWatchOnline', 'vidics.ch', 'pubfilm'],
#                  ['OnlineMoviesIs', 'OnlineMoviesPro', 'ViewMovies', 'movie25', 'viooz.ac', 'view47', 'MoviesHD', 'wmo.ch'],
#                  ['ayyex', 'stream-tv.co', 'clickplay.to', 'MintMovies', 'MovieNight', 'cmz', 'ch131', 'filmikz.ch'],
#                  ['MovieTube', 'LosMovies', 'FilmStreaming.in', 'moviestorm.eu', 'MerDB']]
#
#         sso = []
#         random_sso = kodi.get_setting('random_sso') == 'true'
#         for tier in tiers:
#             if isinstance(tier, basestring):
#                 sso.append(tier)
#             else:
#                 if random_sso:
#                     random.shuffle(tier)
#                 sso += tier
#         kodi.set_setting('source_sort_order', '|'.join(sso))
#
#     if responses[11]: reset_base_url()
#     kodi.notify(msg=i18n('auto_conf_complete'))
#
# def do_auto_config():
#     ACTION_PREVIOUS_MENU = 10
#     ACTION_BACK = 92
#     CONTINUE_BUTTON = 200
#     CANCEL_BUTTON = 201
#
#     starty = 60
#     posx = 30
#     gap = 35
#     RADIO_BUTTONS = [
#         i18n('set_trakt_timeout'),
#         i18n('set_cal_start'),
#         i18n('set_cal_airtime'),
#         i18n('set_scraper_timeout'),
#         i18n('set_wl_mne'),
#         i18n('set_test_direct'),
#         i18n('set_filter_unusable'),
#         i18n('set_show_debrid'),
#         i18n('set_no_limit'),
#         i18n('set_source_sort'),
#         i18n('set_sso'),
#         i18n('set_reset_url'),
#         i18n('select_all_none')]
#
#     class AutoConfDialog(xbmcgui.WindowXMLDialog):
#         def onInit(self):
#             log_utils.log('onInit:', log_utils.LOGDEBUG)
#             self.OK = False
#             self.radio_buttons = []
#             posy = starty
#             for label in RADIO_BUTTONS:
#                 self.radio_buttons.append(self.__get_radio_button(posx, posy, label))
#                 posy += gap
#
#             try: responses = json.loads(kodi.get_setting('prev_responses'))
#             except: responses = [True] * len(self.radio_buttons)
#             if len(responses) < len(self.radio_buttons):
#                 responses += [True] * (len(self.radio_buttons) - len(responses))
#
#             self.addControls(self.radio_buttons)
#             last_button = None
#             for response, radio_button in zip(responses, self.radio_buttons):
#                 radio_button.setSelected(response)
#                 if last_button is not None:
#                     radio_button.controlUp(last_button)
#                     radio_button.controlLeft(last_button)
#                     last_button.controlDown(radio_button)
#                     last_button.controlRight(radio_button)
#                 last_button = radio_button
#
#             continue_ctrl = self.getControl(CONTINUE_BUTTON)
#             cancel_ctrl = self.getControl(CANCEL_BUTTON)
#             self.radio_buttons[0].controlUp(cancel_ctrl)
#             self.radio_buttons[0].controlLeft(cancel_ctrl)
#             self.radio_buttons[-1].controlDown(continue_ctrl)
#             self.radio_buttons[-1].controlRight(continue_ctrl)
#             continue_ctrl.controlUp(self.radio_buttons[-1])
#             continue_ctrl.controlLeft(self.radio_buttons[-1])
#             cancel_ctrl.controlDown(self.radio_buttons[0])
#             cancel_ctrl.controlRight(self.radio_buttons[0])
#
#         def __get_radio_button(self, x, y, label):
#             kwargs = {'font': 'font12', 'focusTexture': 'button-focus2.png', 'noFocusTexture': 'button-nofocus.png', 'focusOnTexture': 'radiobutton-focus.png',
#                       'noFocusOnTexture': 'radiobutton-focus.png', 'focusOffTexture': 'radiobutton-nofocus.png', 'noFocusOffTexture': 'radiobutton-nofocus.png'}
#             temp = xbmcgui.ControlRadioButton(x, y, 450, 30, label, **kwargs)
#             return temp
#
#         def onAction(self, action):
#             # log_utils.log('Action: %s' % (action.getId()), log_utils.LOGDEBUG)
#             if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
#                 self.close()
#
#         def onControl(self, control):
#             # log_utils.log('onControl: %s' % (control), log_utils.LOGDEBUG)
#             pass
#
#         def onFocus(self, control):
#             # log_utils.log('onFocus: %s' % (control), log_utils.LOGDEBUG)
#             pass
#
#         def onClick(self, control):
#             # log_utils.log('onClick: %s' % (control), log_utils.LOGDEBUG)
#             focus_button = self.getControl(control)
#             if focus_button == self.radio_buttons[-1]:
#                 all_status = focus_button.isSelected()
#                 for button in self.radio_buttons:
#                     button.setSelected(all_status)
#
#             if control == CONTINUE_BUTTON:
#                 self.OK = True
#
#             if control == CANCEL_BUTTON:
#                 self.OK = False
#
#             if control == CONTINUE_BUTTON or control == CANCEL_BUTTON:
#                 self.close()
#
#         def get_responses(self):
#             return [bool(button.isSelected()) for button in self.radio_buttons]
#
#     dialog = AutoConfDialog('AutoConfDialog.xml', kodi.get_path())
#     dialog.doModal()
#     if dialog.OK:
#         responses = dialog.get_responses()
#         kodi.set_setting('prev_responses', json.dumps(responses))
#         perform_auto_conf(responses)
#     del dialog
