"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import xbmcgui
import time
import kodi
import random
import json
import log_utils
from utils2 import reset_base_url, i18n

INTERVALS = 5
logger = log_utils.Logger.get_logger()

def perform_auto_conf(responses):
    with kodi.WorkingDialog():
        length = len(responses)
        TOTAL = 13
        if length < TOTAL:
            responses += [True] * (TOTAL - length)
            
        if responses[0]: kodi.set_setting('trakt_timeout', '60')
        if responses[1]: kodi.set_setting('calendar-day', '-1')
        if responses[2]: kodi.set_setting('calendar_time', '2')
        if responses[3]: kodi.set_setting('source_timeout', '20')
        if responses[4]: kodi.set_setting('include_watchlist_next', 'true')
        if responses[5]: kodi.set_setting('filter_direct', 'true')
        if responses[6]: kodi.set_setting('filter_unusable', 'true')
        if responses[7]: kodi.set_setting('show_debrid', 'true')
        if responses[8]: kodi.set_setting('source_results', '0')
        if responses[9]:
            kodi.set_setting('enable_sort', 'true')
            kodi.set_setting('sort1_field', '2')
            kodi.set_setting('sort2_field', '5')
            kodi.set_setting('sort3_field', '6')
            kodi.set_setting('sort4_field', '1')
            kodi.set_setting('sort5_field', '3')
            kodi.set_setting('sort6_field', '4')
    
        if responses[10]:
            tiers = ['Local', 'Premiumize.V2', 'Premiumize.me', 'Furk.net', 'EasyNews', 'DD.tv', 'NoobRoom', 'Sit2Play',
                     ['yify.tv', 'MoviesPlanet', 'goojara', '123Movies', '9Movies', 'DayT.se', 'mvgee', 'niter.tv', 'YesMovies', 'ororo.tv', 'MovieOcean'],
                     ['StreamLord', 'MovieFlix', 'CyberReel', 'm4ufree', 'tunemovie', 'fmovie.co', 'xmovies8', 'xmovies8.v2', 'KiwiHD', 'HDMovieFree', 'Mehliz'],
                     ['OLMovies', 'MovieGo', 'MovieXK', 'PelisPedia', 'PutMV', 'PirateJunkies', 'SeriesWatch', 'VidNow4K', 'VeoCube', 'Quikr', 'MovieBlast', 'Pubfilm.to'],
                     ['IOMovies', 'RealMovies', 'HeyDL', 'HEVCBluRay', 'SezonLukDizi', 'Dizimag', 'Dizilab', 'Dizigold', 'Dizibox', 'Diziay', 'Dizipas', 'OnlineDizi'],
                     ['SeriesOnline', 'MovyTvy', 'Dizist', 'DownloadTube', 'scene-rls', 'DDLValley', '2DDL', 'MyDDL', 'DDLSeries', 'SceneDown', 'CinemaMKV'],
                     ['RMZ', 'BestMoviez', 'SceneHDTV', 'Vumoo', 'TVHD', 'RLSHD', 'rls-movies', 'ReleaseBB', 'MyVideoLinks.eu', 'RLSSource.net', 'SeeHD'],
                     ['TVShow.me', 'vivo.to', 'IceFilms', 'Flixanity', 'Watch5s', 'WatchEpisodes', 'WatchItVideos', 'PrimeWire', 'alluc.com', 'tvonline', 'SantaSeries'],
                     ['WatchOnline', 'StreamDor', 'Vebup', 'WatchSeries', 'Putlocker', 'MovieWatcher', 'VKFlix', 'WatchFree.to', 'pftv', 'Movie4K', 'MovieZone'],
                     ['MovieHubs', 'tvrush', 'afdah', 'MiraDeTodo', 'Filmovizija', 'wso.ch', 'MovieSub', 'MovieHut', 'CouchTunerV1', 'Watch8Now', 'SnagFilms'],
                     ['treasureen', 'MoviePool', 'iWatchOnline', 'vidics.ch', 'pubfilm', 'eMovies.Pro', 'OnlineMoviesPro', 'movie25', 'viooz.ac'],
                     ['SpaceMov', 'LosMovies', 'wmo.ch', 'stream-tv.co', 'MintMovies', 'MovieNight', 'cmz', 'SeriesCoco', 'filmikz.ch', 'clickplay.to'],
                     ['MovieTube']]
        
            sso = []
            random_sso = kodi.get_setting('random_sso') == 'true'
            for tier in tiers:
                if isinstance(tier, basestring):
                    sso.append(tier)
                else:
                    if random_sso:
                        random.shuffle(tier)
                    sso += tier
            kodi.set_setting('source_sort_order', '|'.join(sso))
        
        if responses[11]: reset_base_url()
        if responses[12]: kodi.set_setting('mne_time', '2')
        trigger = [False, True, False, True, False, True, True, False, True, False, False, False]
        if all([t == r for t, r in zip(trigger, responses)]):
            kodi.set_setting('scraper_download', 'true')
        
    kodi.notify(msg=i18n('auto_conf_complete'))

def do_ip_auth(scraper, visit_url, qr_code):
    EXPIRE_DURATION = 60 * 5
    ACTION_PREVIOUS_MENU = 10
    ACTION_BACK = 92
    CANCEL_BUTTON = 200
    INSTR_LABEL = 101
    QR_CODE_CTRL = 102
    PROGRESS_CTRL = 103
    
    class IpAuthDialog(xbmcgui.WindowXMLDialog):
        def onInit(self):
            # logger.log('onInit:', log_utils.LOGDEBUG)
            self.cancel = False
            self.getControl(INSTR_LABEL).setLabel(i18n('ip_auth_line1') + visit_url + i18n('ip_auth_line2'))
            self.progress = self.getControl(PROGRESS_CTRL)
            self.progress.setPercent(100)
            if qr_code:
                img = self.getControl(QR_CODE_CTRL)
                img.setImage(qr_code)
            
        def onAction(self, action):
            # logger.log('Action: %s' % (action.getId()), log_utils.LOGDEBUG)
            if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
                self.cancel = True
                self.close()

        def onControl(self, control):
            # logger.log('onControl: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onFocus(self, control):
            # logger.log('onFocus: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onClick(self, control):
            # logger.log('onClick: %s' % (control), log_utils.LOGDEBUG)
            if control == CANCEL_BUTTON:
                self.cancel = True
                self.close()
        
        def setProgress(self, progress):
            self.progress.setPercent(progress)

    dialog = IpAuthDialog('IpAuthDialog.xml', kodi.get_path())
    dialog.show()
    interval = 5000
    begin = time.time()
    try:
        while True:
            for _ in range(INTERVALS):
                kodi.sleep(interval / INTERVALS)
                elapsed = time.time() - begin
                progress = int((EXPIRE_DURATION - elapsed) * 100 / EXPIRE_DURATION)
                dialog.setProgress(progress)
                if progress <= 0 or dialog.cancel:
                    return False
                
            authorized, result = scraper.check_auth()
            if authorized: return result
    finally:
        del dialog

def do_auto_config():
    ACTION_PREVIOUS_MENU = 10
    ACTION_BACK = 92
    CONTINUE_BUTTON = 200
    CANCEL_BUTTON = 201
    RADIO_BUTTONS = range(302, 316)

    class AutoConfDialog(xbmcgui.WindowXMLDialog):
        def onInit(self):
            logger.log('onInit:', log_utils.LOGDEBUG)
            self.OK = False
            
            try: responses = json.loads(kodi.get_setting('prev_responses'))
            except: responses = [True] * len(RADIO_BUTTONS)
            if len(responses) < len(RADIO_BUTTONS):
                responses += [True] * (len(RADIO_BUTTONS) - len(responses))
                
            for button, response in zip(RADIO_BUTTONS, responses):
                self.getControl(button).setSelected(response)
            
        def onAction(self, action):
            # logger.log('Action: %s' % (action.getId()), log_utils.LOGDEBUG)
            if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
                self.close()

        def onControl(self, control):
            # logger.log('onControl: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onFocus(self, control):
            # logger.log('onFocus: %s' % (control), log_utils.LOGDEBUG)
            pass

        def onClick(self, control):
            # logger.log('onClick: %s' % (control), log_utils.LOGDEBUG)
            focus_button = self.getControl(control)
            if focus_button.getId() == RADIO_BUTTONS[-1]:
                all_status = focus_button.isSelected()
                for button in RADIO_BUTTONS:
                    self.getControl(button).setSelected(all_status)
            
            if control == CONTINUE_BUTTON:
                self.OK = True
                
            if control == CANCEL_BUTTON:
                self.OK = False

            if control == CONTINUE_BUTTON or control == CANCEL_BUTTON:
                self.close()
        
        def get_responses(self):
            return [bool(self.getControl(button).isSelected()) for button in RADIO_BUTTONS]

    dialog = AutoConfDialog('AutoConfDialog.xml', kodi.get_path())
    dialog.doModal()
    if dialog.OK:
        responses = dialog.get_responses()
        kodi.set_setting('prev_responses', json.dumps(responses))
        perform_auto_conf(responses)
    del dialog
