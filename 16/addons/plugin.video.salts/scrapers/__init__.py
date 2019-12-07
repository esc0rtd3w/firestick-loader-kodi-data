import os
import re
import time

import kodi
import log_utils  # @UnusedImport
from salts_lib import utils2
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES

__all__ = ['scraper', 'proxy', 'local_scraper', 'pw_scraper', 'watchseries_scraper', 'movie25_scraper', 'nitertv_scraper',
           'filmovizjia_scraper', 'icefilms_scraper', 'viooz_scraper', 'mvl_proxy', 'streamdor_scraper', 'goojara_proxy',
           'filmikz_scraper', 'vidnow4k_proxy', 'downloadtube_scraper', 'iwatch_scraper', 'ororotv_scraper', 'vidics_scraper',
           'losmovies_scraper', 'movie4k_scraper', 'easynews_scraper', 'noobroom_scraper', 'seriesonline_scraper',
           'directdl_scraper', 'afdah_scraper', 'dizibox_scraper', 'yesmovies_scraper', 'iomovies_scraper',
           'streamtv_scraper', 'wmo_scraper', 'wso_scraper', 'watchfree_scraper', 'streamlord_scraper', 'yify_proxy',
           'pftv_scraper', 'flixanity_scraper', 'cmz_scraper', 'movienight_scraper', 'alluc_scraper', 'watchonline_scraper',
           'xmovies8_scraper', 'moviexk_scraper', 'mintmovies_scraper', 'pubfilm_scraper', 'rlssource_scraper', 'mehliz_scraper',
           'couchtunerv1_scraper', 'ddlvalley_scraper', 'pelispedia_scraper', 'spacemov_scraper', 'putmv_scraper',
           'watch8now_scraper', 'dizilab_scraper', 'dizimag_scraper', 'moviehut_scraper', 'serieswatch_scraper', 'dizist_scraper',
           'dizigold_scraper', 'onlinemoviespro_scraper', 'emoviespro_scraper', 'one23movies_proxy', 'rlsbb_scraper',
           'sezonlukdizi_scraper', 'movietube_scraper', 'putlocker_scraper', 'diziay_scraper', 'scenehdtv_scraper', 'pubfilmto_scraper',
           'furk_scraper', 'hevcbluray_scraper', 'ninemovies_proxy', 'miradetodo_scraper', 'dizipas_scraper', 'xmovies8v2_scraper',
           'moviesplanet_scraper', 'premiumize_scraper', 'tvonline_scraper', 'watchitvideos_scraper', 'movieblast_scraper',
           'ddlseries_scraper', 'fmovie_scraper', 'seriescoco_scraper', 'veocube_scraper', 'piratejunkies_scraper', 'sit2play_scraper',
           'watch5s_scraper', 'moviesub_scraper', 'watchepisodes_scraper', 'heydl_scraper', 'vkflix_scraper', 'bestmoviez_scraper',
           'm4ufree_scraper', 'moviewatcher_scraper', 'vivoto_scraper', '2ddl_scraper', 'onlinedizi_scraper', 'moviehubs_scraper',
           'premiumizev2_scraper', 'cinemamkv_scraper', 'dayt_scraper', 'moviego_scraper', 'treasureen_scraper', 'movieocean_proxy',
           'rlsmovies_scraper', 'hdmoviefree_scraper', 'tvrush_scraper', 'snagfilms_scraper', 'scenedown_scraper', 'scenerls_scraper',
           'tvshow_scraper', 'quikr_scraper', 'rlshd_scraper', 'tvhd_scraper', 'seehd_scraper', 'myddl_scraper', 'rmz_scraper',
           'ol_scraper', 'real_scraper', 'movytvy_scraper', 'vumoo_scraper', 'vebup_scraper', 'mvgee_proxy']

from . import *

logger = log_utils.Logger.get_logger()
  
class ScraperVideo:
    def __init__(self, video_type, title, year, trakt_id, season='', episode='', ep_title='', ep_airdate=''):
        assert(video_type in (VIDEO_TYPES.__dict__[k] for k in VIDEO_TYPES.__dict__ if not k.startswith('__')))
        self.video_type = video_type
        if isinstance(title, unicode): self.title = title.encode('utf-8')
        else: self.title = title
        self.year = str(year)
        self.season = season
        self.episode = episode
        if isinstance(ep_title, unicode): self.ep_title = ep_title.encode('utf-8')
        else: self.ep_title = ep_title
        self.trakt_id = trakt_id
        self.ep_airdate = utils2.to_datetime(ep_airdate, "%Y-%m-%d").date() if ep_airdate else None

    def __str__(self):
        return '|%s|%s|%s|%s|%s|%s|%s|' % (self.video_type, self.title, self.year, self.season, self.episode, self.ep_title, self.ep_airdate)

def update_xml(xml, new_settings, cat_count):
    new_settings.insert(0, '<category label="Scrapers %s">' % (cat_count))
    new_settings.append('    </category>')
    new_settings = '\n'.join(new_settings)
    match = re.search('(<category label="Scrapers %s">.*?</category>)' % (cat_count), xml, re.DOTALL | re.I)
    if match:
        old_settings = match.group(1)
        if old_settings != new_settings:
            xml = xml.replace(old_settings, new_settings)
    else:
        logger.log('Unable to match category: %s' % (cat_count), log_utils.LOGWARNING)
    return xml

def update_settings():
    full_path = os.path.join(kodi.get_path(), 'resources', 'settings.xml')
    
    try:
        # open for append; skip update if it fails
        with open(full_path, 'a') as f:
            pass
    except Exception as e:
        logger.log('Dynamic settings update skipped: %s' % (e), log_utils.LOGWARNING)
    else:
        with open(full_path, 'r') as f:
            xml = f.read()

        new_settings = []
        cat_count = 1
        old_xml = xml
        classes = scraper.Scraper.__class__.__subclasses__(scraper.Scraper)  # @UndefinedVariable
        classes += proxy.Proxy.__class__.__subclasses__(proxy.Proxy)  # @UndefinedVariable
        for cls in sorted(classes, key=lambda x: x.get_name().upper()):
            if not cls.get_name() or cls.has_proxy(): continue
            new_settings += cls.get_settings()
            if len(new_settings) > 90:
                xml = update_xml(xml, new_settings, cat_count)
                new_settings = []
                cat_count += 1
    
        if new_settings:
            xml = update_xml(xml, new_settings, cat_count)
    
        if xml != old_xml:
            with open(full_path, 'w') as f:
                f.write(xml)
        else:
            logger.log('No Settings Update Needed', log_utils.LOGDEBUG)


def update_all_scrapers():
        try: last_check = int(kodi.get_setting('last_list_check'))
        except: last_check = 0
        now = int(time.time())
        list_url = kodi.get_setting('scraper_url')
        scraper_password = kodi.get_setting('scraper_password')
        list_path = os.path.join(kodi.translate_path(kodi.get_profile()), 'scraper_list.txt')
        exists = os.path.exists(list_path)
        if list_url and scraper_password and (not exists or (now - last_check) > 15 * 60):
            _etag, scraper_list = utils2.get_and_decrypt(list_url, scraper_password)
            if scraper_list:
                try:
                    with open(list_path, 'w') as f:
                        f.write(scraper_list)
    
                    kodi.set_setting('last_list_check', str(now))
                    kodi.set_setting('scraper_last_update', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))
                    for line in scraper_list.split('\n'):
                        line = line.replace(' ', '')
                        if line:
                            scraper_url, filename = line.split(',')
                            if scraper_url.startswith('http'):
                                update_scraper(filename, scraper_url)
                except Exception as e:
                    logger.log('Exception during scraper update: %s' % (e), log_utils.LOGWARNING)
    
def update_scraper(filename, scraper_url):
    try:
        if not filename: return
        py_path = os.path.join(kodi.get_path(), 'scrapers', filename)
        exists = os.path.exists(py_path)
        scraper_password = kodi.get_setting('scraper_password')
        if scraper_url and scraper_password:
            old_lm = None
            old_py = ''
            if exists:
                with open(py_path, 'r') as f:
                    old_py = f.read()
                    match = re.search('^#\s+Last-Modified:\s*(.*)', old_py)
                    if match:
                        old_lm = match.group(1).strip()

            new_lm, new_py = utils2.get_and_decrypt(scraper_url, scraper_password, old_lm)
            if new_py:
                logger.log('%s path: %s, new_py: %s, match: %s' % (filename, py_path, bool(new_py), new_py == old_py), log_utils.LOGDEBUG)
                if old_py != new_py:
                    with open(py_path, 'w') as f:
                        f.write('# Last-Modified: %s\n' % (new_lm))
                        f.write(new_py)
                    kodi.notify(msg=utils2.i18n('scraper_updated') + filename)
                        
    except Exception as e:
        logger.log('Failure during %s scraper update: %s' % (filename, e), log_utils.LOGWARNING)

update_settings()
update_all_scrapers()
