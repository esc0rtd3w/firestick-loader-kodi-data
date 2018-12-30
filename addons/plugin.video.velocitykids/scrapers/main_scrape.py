import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmc
import xbmcvfs
import urllib, urllib2
import urlparse
import sys
import os
import re
import urlresolver
import time
from threading import Thread
from Queue import Queue
import json


import twomovies, merdb,iwatchonline,zmovies,primewire,afdah,nine_movies,ot3_movies,icefilms,santa_tv,putlocker_both
from libs import kodi,trakt_auth
from libs import log_utils
from t0mm0.common.addon import Addon

addon_id=kodi.addon_id
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
fanart = artwork+'fanart.jpg'
ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)

MAX_ERRORS = 10

def wrapper(func, arg, queue):
    queue.put(func(arg))

def find_source(name,thumb,media,movie_title):
    try:
        all_source = []

        q1, q2, q3, q4, q5, q6, q7, q8, q9 = Queue(), Queue(), Queue(),Queue(), Queue(), Queue(), Queue(), Queue(),Queue()

        if thumb is None:
            thumb = ''
        else:
            thumb = thumb
        if media == 'shows':
            find_sourceTV(name,thumb,media,movie_title)
        else:
            # if kodi.get_setting('9movies') == "true":
            #     movie_title = name
            #     Thread(target=wrapper, args=(nine_movies.ninemovies, name, q1)).start()

            if kodi.get_setting('primewire') == "true":
                movie_title = name
                Thread(target=wrapper, args=(primewire.primewire, name, q2)).start()

            # if kodi.get_setting('afdah') =='true':
            #     movie_title = name
            #     Thread(target=wrapper, args=(afdah.afdah, name, q4)).start()

            if kodi.get_setting('merdb') == "true":
                movie_title = name
                Thread(target=wrapper, args=(merdb.merdb, name, q5)).start()

            if kodi.get_setting('zmovies') == "true":
                movie_title = name
                Thread(target=wrapper, args=(zmovies.zmovies, name, q6)).start()

            if kodi.get_setting('123movies') == "true":
                movie_title = name
                Thread(target=wrapper, args=(ot3_movies.ot3_movies, name, q7)).start()

            if kodi.get_setting('ice_films') == "true":
                movie_title = name
                t = Thread(target=wrapper, args=(icefilms.ice_films, name, q8))
                t.daemon = True
                t.start()

            if kodi.get_setting('putlocker') == "true":
                movie_title = name
                t = Thread(target=wrapper, args=(putlocker_both.putlocker_movies, name, q9))
                t.daemon = True
                t.start()

######Grab Results
######TRY TO SORT ALL TOGETHER


            if kodi.get_setting('ice_films') == "true":
                icesources = q8.get()
                all_source.append(icesources)

            if kodi.get_setting('putlocker') == "true":
                putlockersources = q9.get()
                all_source.append(putlockersources)

            # if kodi.get_setting('9movies') == "true":
            #     ninesources = q1.get()
            #     all_source.append(ninesources)

            if kodi.get_setting('123movies') == "true":
                ottsources = q7.get()
                all_source.append(ottsources)

            if kodi.get_setting('primewire') == "true":
                primesources = q2.get()
                all_source.append(primesources)

            # if kodi.get_setting('afdah') =='true':
            #     afdahsources = q4.get()
            #     all_source.append(afdahsources)

            if kodi.get_setting('merdb') == "true":
                mersources = q5.get()
                all_source.append(mersources)

            if kodi.get_setting('zmovies') == "true":
                zmoviesources =q6.get()
                all_source.append(zmoviesources)

            for a in all_source:
                    if a:
                        #b = sorted(a, key=lambda k: (str(k['debrid'])))
                        b = sorted(a, reverse=False)
                        #b.sort(reverse=True)
                        # log_utils.log('TESTING 2 [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                        try:
                            for e in b :
                                # log_utils.log('TESTING 3 [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                                total_items =len(e)
                                if 'debrid' in e:
                                    premium = " [COLOR gold]"+str(e['debrid'])+" [/COLOR]"
                                else:
                                    premium = ''
                                hostname = e['hostname']
                                provider = "[COLOR white]["+hostname+"][/COLOR] - "
                                names = e['host']
                                urls = e['url']
                                if e['views'] == None:
                                    views = ''
                                else:
                                    views = " [COLOR green]Views "+e['views']+"[/COLOR]"
                                if e['quality'] == None:
                                    quals = ''
                                else:quals =" [COLOR red]["+ e['quality']+"][/COLOR]"
                                menu_items=[]
                                menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))
                                #kodi.addDir("[COLORteal]["+hostname+"][/COLOR] - "+names+' ['+quals+']'+' [COLOR gold]'+str(premium)+'[/COLOR]',urls,'get_link',thumb,movie_title,total_items,'','movies',menu_items=menu_items,is_playable='true',fanart=fanart)
                                kodi.addDir(provider+names+quals+views+premium,urls,'get_link',thumb,movie_title,total_items,'','movies',menu_items=menu_items,is_playable='true',fanart=fanart)

                        except:
                            pass




    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "true":
                kodi.notify(header='Movie Scrapers',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
            return



def tv_wrapper(func, arg,arg2, queue):
    queue.put(func(arg,arg2))


def find_sourceTV(name,thumb,media,movie_title):
    q1, q2, q3, q4, q5, q6, q7, q8 = Queue(), Queue(), Queue(),Queue(), Queue(), Queue(), Queue(), Queue()
    try:
        if thumb is None:
            thumb = ''
        else:
            thumb = thumb
        if kodi.get_setting('primewire') == "true":
                Thread(target=tv_wrapper, args=(primewire.primewire_tv, name,movie_title, q2)).start()


        if kodi.get_setting('ice_films') == "true":
                t = Thread(target=tv_wrapper, args=(icefilms.ice_films_tv, name,movie_title, q8))
                t.daemon = True
                t.start()

        if kodi.get_setting('santa_tv') == "true":
                t = Thread(target=tv_wrapper, args=(santa_tv.santa_tv, name,movie_title, q1))
                t.daemon = True
                t.start()


        if kodi.get_setting('putlocker') == "true":
                t = Thread(target=tv_wrapper, args=(putlocker_both.putlocker_tv, name,movie_title, q4))
                t.daemon = True
                t.start()

        # GRAB RETURNS BELOW
        if kodi.get_setting('putlocker') == "true":
                try:
                    putlockersources = q4.get()
                    for e in putlockersources:
                        total_items =len(putlockersources)
                        if 'debrid' in e:
                            premium = e['debrid']#.replace('[','').replace(']','')
                            print str(premium)
                        else:
                            premium = ''
                        names = e['host']
                        urls = e['url']
                        #views = e['views']
                        #label = e['label']
                        if e['quality'] == None:
                            quals = 'unknown'
                        else:quals = e['quality']
                        menu_items=[]
                        menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))
                        kodi.addDir("[COLORteal][Putlocker][/COLOR] - "+names+' ['+quals+']  [COLOR gold]'+str(premium)+'[/COLOR]',urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Putlocker',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)



        if kodi.get_setting('santa_tv') == "true":
                try:
                    santasources = q1.get()
                    for e in santasources:
                        total_items =len(santasources)
                        if 'debrid' in e:
                            premium = e['debrid']#.replace('[','').replace(']','')
                            print str(premium)
                        else:
                            premium = ''
                        names = e['host']
                        urls = e['url']
                        # urls = icefilms.resolve_link(urls)
                        #views = e['views']
                        label = e['label']
                        if e['quality'] == None:
                            quals = 'unknown'
                        else:quals = e['quality']
                        menu_items=[]
                        menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))
                        kodi.addDir("[COLORteal][SantaSeries][/COLOR] - "+names+' ['+quals+'] '+label+' [COLOR gold]'+str(premium)+'[/COLOR]',urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='SantaSeries',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)

        if kodi.get_setting('ice_films') == "true":
                try:
                    icesources = q8.get()
                    for e in icesources:
                        total_items =len(icesources)
                        if 'debrid' in e:
                            premium = e['debrid']#.replace('[','').replace(']','')
                            print str(premium)
                        else:
                            premium = ''
                        names = e['host']
                        urls = e['url']
                        #urls = icefilms.resolve_link(urls)
                        views = e['views']
                        if e['quality'] == None:
                            quals = 'unknown'
                        else:quals = e['quality']
                        menu_items=[]
                        menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))
                        kodi.addDir("[COLORteal][IceFilms][/COLOR] - "+names+' ['+quals+']'+' [COLOR gold]'+str(premium)+'[/COLOR]',urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Ice Films',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


        if kodi.get_setting('primewire') == "true":
                primesources = q2.get()
                for e in primesources:
                        total_items =len(primesources)
                        if 'debrid' in e:
                            premium = e['debrid']
                            print str(premium)
                        else:
                            premium = ''
                        names = e['host']
                        urls = e['url']
                        views = e['view']
                        quals = e['quality']
                        menu_items=[]
                        menu_items.append(('[COLOR gold]Add to Downloads[/COLOR]',      'XBMC.Container.Update(%s)' % addon.build_plugin_url({'mode':'setup_download', 'name':name,'url':urls,'thumb':thumb, 'media':media,'movie_title':movie_title})))
                        kodi.addDir("[COLORteal][Primewire][/COLOR] - "+names+' ['+quals+']'+' Views '+views+' [COLOR gold]'+str(premium)+'[/COLOR]',urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)


        # TODO Add TV
        if kodi.get_setting('afdah') == "true":
            print "AFDAH TV not setup yet"

        # TODO Add Mer TV Scrapers
        if kodi.get_setting('merdb') == "true":
            print "MerDb TV Not Setup Yet"


        # TODO Add ZMovies TV Scrapers
        if kodi.get_setting('zmovies') == "true":
            print "ZMovies TV Not setup yet"

    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "true":
                kodi.notify(header='Scraper',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)



def get_link(url,movie_title,thumb,media):
    hmf = urlresolver.HostedMediaFile(url)
    ##########################################
    if hmf:
        try:
            url = urlresolver.resolve(url)
            params = {'url':url, 'name':movie_title, 'thumb':thumb}
            addon.add_video_item(params, {'title':movie_title}, img=thumb)
            liz=xbmcgui.ListItem(movie_title, iconImage="DefaultFolder.png", thumbnailImage=thumb)
            xbmc.sleep(1000)
            liz.setPath(str(url))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            # #xbmc.Player ().play(url, liz, False)
            # movie_name = movie_title[:-6]
            # movie_name = '"'+movie_name+'"'
            # movie_year_full = movie_title[-6:]
            # movie_year = movie_year_full.replace('(','').replace(')','')
            # if kodi.get_setting('trakt_oauth_token'):
            #     xbmc.sleep(30000)
            #     print "Velocity: Movie Scrobble  Start"
            #     try:
            #         trakt_auth.start_movie_watch(movie_name,movie_year)
            #     except Exception as e:
            #         log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            #         if kodi.get_setting('error_notify') == "true":
            #             kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
            # xbmc.sleep(30000)
            # if kodi.get_setting('trakt_oauth_token'):
            #     check_player(movie_name,movie_year)
        except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)

    if not hmf:
        try:
            params = {'url':url, 'name':movie_title, 'thumb':thumb}
            addon.add_video_item(params, {'title':movie_title}, img=thumb)
            liz=xbmcgui.ListItem(movie_title, iconImage="DefaultFolder.png", thumbnailImage=thumb)
            xbmc.sleep(1000)
            liz.setPath(str(url))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            # #xbmc.Player ().play(url, liz, False)
            # movie_name = movie_title[:-6]
            # movie_name = '"'+movie_name+'"'
            # movie_year_full = movie_title[-6:]
            # movie_year = movie_year_full.replace('(','').replace(')','')
            # if kodi.get_setting('trakt_oauth_token'):
            #     xbmc.sleep(30000)
            #     print "Velocity: Movie Scrobble  Start"
            #     try:
            #         trakt_auth.start_movie_watch(movie_name,movie_year)
            #     except Exception as e:
            #         log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            #         if kodi.get_setting('error_notify') == "true":
            #             kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
            #
            # xbmc.sleep(30000)
            # if kodi.get_setting('trakt_oauth_token'):
            #     check_player(movie_name,movie_year)
        except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)




def get_tv_link(url,movie_title,thumb,media):
    hmf = urlresolver.HostedMediaFile(url)
    ##########################################
    if hmf:
        url = urlresolver.resolve(url)
    if not hmf:
        url = url
    try:
        params = {'url':url, 'name':media, 'thumb':thumb}
        addon.add_video_item(params, {'title':media}, img=thumb)
        liz=xbmcgui.ListItem(media, iconImage="DefaultFolder.png", thumbnailImage=thumb)
        xbmc.sleep(1000)
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        # #xbmc.Player ().play(url, liz, False)
        # movie_name = movie_title[:-6]
        # movie_name = '"'+movie_name+'"'
        # movie_year_full = movie_title[-6:]
        # movie_year = movie_year_full.replace('(','').replace(')','')
        # if kodi.get_setting('trakt_oauth_token'):
        #     xbmc.sleep(30000)
        #     print "Velocity: TV Show Scrobble  Start"
        #     try:
        #         trakt_auth.start_tv_watch(movie_name,media)
        #     except Exception as e:
        #             log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
        #             if kodi.get_setting('error_notify') == "true":
        #                 kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
        # xbmc.sleep(30000)
        # if kodi.get_setting('trakt_oauth_token'):
        #     check_tv_player(movie_name,media)

    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)

class Player(xbmc.Player):
    def __init__(self):
        log_utils.log('Velocity Service: starting...')
        xbmc.Player.__init__(self)
        self.win = xbmcgui.Window(10000)
        #self.reset()

    def onPlayBackStarted(self):
        log_utils.log('Service: Playback Started')


    def onPlayBackStopped(self):
        log_utils.log('Service: Playback Stopped')
        #print" RUN A STOP COMMAND"

    def onPlayBackEnded(self):
        log_utils.log('Service: Playback Ended')

        self.onPlayBackStopped()


def check_player(name,year):

    monitor = Player()

    errors = 0
    while not xbmc.abortRequested:
        try:
            #print"CHECK ONE"
            isPlaying = monitor.isPlaying()
            if  monitor.isPlayingVideo():
                monitor._lastPos = monitor.getTime()
               # print  monitor._lastPos
            else:
                print "Velocity: Scrobble Movie End"
                trakt_auth.stop_movie_watch(name,year)
                break
        except Exception as e:
            errors += 1
            if errors >= MAX_ERRORS:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Ending Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
                break
            else:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Continuing Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
        else:
            errors = 0

        xbmc.sleep(1000)



def check_tv_player(name,media):

    monitor = Player()

    errors = 0
    while not xbmc.abortRequested:
        try:
            isPlaying = monitor.isPlaying()
            if  monitor.isPlayingVideo():
                monitor._lastPos = monitor.getTime()
                #print  monitor._lastPos
            else:
                print "Velocity: Scrobble TV Show End"
                trakt_auth.stop_tv_watch(name,media)
                break
        except Exception as e:
            errors += 1
            if errors >= MAX_ERRORS:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Ending Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
                break
            else:
                log_utils.log('Service: Error (%s) received..(%s/%s)...Continuing Service...' % (e, errors, MAX_ERRORS), log_utils.LOGERROR)
        else:
            errors = 0

        xbmc.sleep(1000)


#######Real Debrid Check
def apply_urlresolver(hosters):
    filter_debrid = kodi.get_setting('filter_debrid') == 'true'
    show_debrid = kodi.get_setting('show_debrid') == 'true'
    if not filter_debrid and not show_debrid:
        print "RETURNING NON FILTERED"
        return hosters

    ## New Resolver
    try:
        import urlresolver.plugnplay
        resolvers = urlresolver.plugnplay.man.implementors(urlresolver.UrlResolver)
        debrid_resolvers = [resolver for resolver in resolvers if resolver.isUniversal() and resolver.get_setting('enabled') == 'true']
    except:
        import urlresolver
        debrid_resolvers = [resolver() for resolver in urlresolver.relevant_resolvers(order_matters=True) if resolver.isUniversal()]
##   End New Resolver

    filtered_hosters = []
    debrid_hosts = {}
    unk_hosts = {}
    known_hosts = {}
    for hoster in hosters:
        #print "HOSTERS ARE: "+str(hoster)
        if 'direct' in hoster and hoster['direct'] == False and hoster['host']:
            host = hoster['host']
            host = (host.lower())
            #
            if kodi.get_setting('filter_debrid')=='true':
                if host in unk_hosts:
                    # log_utils.log('Unknown Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                    unk_hosts[host] += 1
                    continue
                elif host in known_hosts:
                    # log_utils.log('Known Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                    known_hosts[host] += 1
                    filtered_hosters.append(hoster)
                else:
                    hmf = urlresolver.HostedMediaFile(host=host, media_id='dummy')  # use dummy media_id to force host validation
                    if hmf:
                        # log_utils.log('Known Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                        known_hosts[host] = known_hosts.get(host, 0) + 1
                        filtered_hosters.append(hoster)
                    else:
                        # log_utils.log('Unknown Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
                        unk_hosts[host] = unk_hosts.get(host, 0) + 1
                        continue
            else:
                filtered_hosters.append(hoster)

            if host in debrid_hosts:
                log_utils.log('Debrid cache found for %s: %s' % (host, debrid_hosts[host]), log_utils.LOGDEBUG)
                hoster['debrid'] = debrid_hosts[host]
                #print debrid_hosts[host]
            else:
                temp_resolvers = []
                for resolver in debrid_resolvers:
                    if resolver.valid_url('', host):
                        #print resolver.name
                        rname= resolver.name.replace('Real-Debrid','RD').replace('Premiumize.me','PRE')
                        temp_resolvers.append(rname.upper())
                        #temp_resolvers.append(resolver.name.upper())
                        if kodi.get_setting('debug') == "true":
                            print '%s supported by: %s' % (host, temp_resolvers)
                        debrid_hosts[host] = temp_resolvers
                    else:
                         hoster['debrid'] = ''
                if temp_resolvers:
                    hoster['debrid'] = temp_resolvers
                    #print temp_resolvers
        else:
            filtered_hosters.append(hoster)

    #log_utils.log('Discarded Hosts: %s' % (sorted(unk_hosts.items(), key=lambda x: x[1], reverse=True)), xbmc.LOGDEBUG)
    if kodi.get_setting('debug') == "true":
        print "FILTERED HOSTERS ARE =" +str(filtered_hosters)
    return filtered_hosters
