import xbmc,xbmcaddon,os      
import kodi
import client
import cache
import log_utils
 
def check(scraper):
    return
    # try:
        # disable_check = xbmcaddon.Addon('plugin.video.xxx-o-dus').getSetting('dev_scrapers')

        # if ( not disable_check == 'true' ): 
            # scraperFile = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.scrapers', 'lib/scrapers/%s.py' % scraper.lower()))
            # scraperLink = 'https://raw.githubusercontent.com/echocoderxbmc/script.xxxodus.scrapers/master/lib/scrapers/%s.py' % scraper.lower()
            # r = cache.get(client.request, 4, scraperLink)

            # if len(r)>1:
                # with open(scraperFile,'r') as f: compfile = f.read()
                # if 'import' in r:
                    # if compfile == r: 
                        # log_utils.log('%s checked and up to date!' % scraper.title(), log_utils.LOGNOTICE)
                        # pass
                    # else:
                        # with open(scraperFile,'w') as f: f.write(r)
                        # icon = xbmc.translatePath(os.path.join('special://home/addons/script.xxxodus.artwork', 'resources/art/%s/icon.png' % scraper.lower()))
                        # log_utils.log('%s updated!' % scraper.title(), log_utils.LOGNOTICE)
                        # kodi.notify(msg='%s Updated.' % scraper.title(), duration=1250, sound=True, icon_path=icon)
    # except Exception as e:
        # log_utils.log('Error checking for scraper update %s :: Error: %s' % (scraper.title(),str(e)), log_utils.LOGERROR)