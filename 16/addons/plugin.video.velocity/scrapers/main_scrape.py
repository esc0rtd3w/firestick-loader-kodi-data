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
from libs import viewsetter

import iwatchonline,primewire,afdah_scraper,icefilms,putlocker_both,real_scraper,swatch_scraper,watchepisodes,twoddl
from libs import kodi,trakt_auth
from libs import log_utils
from libs.modules.addon import Addon
from scrapers import ScraperVideo
import threading
import Queue



addon_id=kodi.addon_id
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
fanart = artwork+'fanart.jpg'
ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon = Addon(addon_id, sys.argv) # use 1

MAX_ERRORS = 10

ssource=[]
timeout = 30




progressDialog = kodi.progressDialog

q = Queue.Queue()

percen = 0
start_time = time.time()
timetaken = time.time() - start_time


movie_scraper_timeout = int(kodi.get_setting('scraper2_timeout'))
tv_scraper_timeout = int(kodi.get_setting('scraper3_timeout'))



def find_source(name,thumb,media,movie_title):

    if media == 'shows':
        find_sourceTV(name, thumb, media, movie_title)
    else:
        try:
            if thumb is None:
                thumb = ''
            else:
                thumb = thumb
            q = Queue.Queue()

            progressDialog.create(name, '')
            progressDialog.update(0, line1='Gathering Movie Scrapers ', line2='Please wait', line3='')


            title = name[:-7]
            movie_year = name[-6:]
            year = movie_year.replace('(', '').replace(')', '')
            video_type = 'movies'
            total_items = 0
            #<<<<<<<<<Build Threads>>>>>>>>>#
            thread_results = []
            threads = []
            RunAll =Run_Scrapers()
            if kodi.get_setting('ice_films') == 'true':
                thesearch = icefilms.Scraper()
                t1 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "IceFilms", video_type, title, year, q),name = "IceFilms")
                threads.insert(len(threads), t1)

            if kodi.get_setting('primewire') == 'true':
                thesearch = primewire.Scraper()
                t2 = threading.Thread(target=RunAll.go_scraper, args=(thesearch,"PrimeWire", video_type, title, year, q),name = "Primewire")
                threads.insert(len(threads), t2)

            if kodi.get_setting('iwatchon') == 'true':
                thesearch = iwatchonline.Scraper()
                t3 = threading.Thread(target=RunAll.go_scraper, args=(thesearch,"IwatchOnline", video_type, title, year, q),name = "iWatchOnline")
                threads.insert(len(threads), t3)

            if kodi.get_setting('afdah') == 'true':
                thesearch = afdah_scraper.Scraper()
                t4 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "AFDAH", video_type, title, year, q),name = "Afdah")
                threads.insert(len(threads), t4)

            if kodi.get_setting('putlocker') == 'true':
                thesearch = putlocker_both.Scraper()
                t5 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "PutLocker", video_type, title, year, q),name = "Putlocker")
                threads.insert(len(threads), t5)

            if kodi.get_setting('real_movies') == 'true':
                thesearch = real_scraper.Scraper()
                t6 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "RealMovies", video_type, title, year, q),name = "RealMovies")
                threads.insert(len(threads), t6)

            if kodi.get_setting('swatch') == 'true':
                thesearch = swatch_scraper.Scraper()
                t7 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "SeriesWatch", video_type, title, year, q),name = "SeriesWatch")
                threads.insert(len(threads), t7)

            if kodi.get_setting('2ddl') == 'true':
                thesearch = twoddl.Scraper()
                t8 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "2DDL", video_type, title, year, q),name = "2DDL")
                threads.insert(len(threads), t8)
# TODO Finish Scene Release
#             if kodi.get_setting('scener') == 'true':
#                 thesearch = scener_scraper.Scraper()
#                 t8 = threading.Thread(target=RunAll.go_scraper,args=(thesearch, "SceneRelease", video_type, title, year, q),name = "SceneRelease")
#                 threads.insert(len(threads), t8)

            [t.start() for t in threads]
            string1 = "Time elapsed: %s seconds"
            string3 = "Remaining providers: %s"
            for t in range(0, (movie_scraper_timeout * 2) + 60):
                try:
                    if xbmc.abortRequested == True: return sys.exit()

                    try:
                        info = [[x.getName()] for x in threads if x.is_alive() == True]
                    except:
                        info = []

                    timerange = int(t * 0.5)

                    try:
                        if progressDialog.iscanceled(): break
                    except:
                        pass
                    try:
                        string4 = string1 % str(timerange)
                        if len(info) > 5:
                            string5 = string3 % str(len(info))
                        else:
                            string5 = string3 % str(info).translate(None, "[]'")
                        progressDialog.update(
                            int((100 / float(len(threads))) * len([x for x in threads if x.is_alive() == False])),
                            str(string4), str(string5))
                    except:
                        pass

                    is_alive = [x.is_alive() for x in threads]
                    if all(x == False for x in is_alive): break

                    if timerange >= movie_scraper_timeout:
                        is_alive = [x for x in threads if x.is_alive() == True]
                        if not is_alive: break

                    #time.sleep(0.5)
                    response = q.get()
                    thread_results.extend(response[2])
                    all_results = len(thread_results)
                except:
                    pass
            kodi.progressDialog.update(100, line1='[COLOR gold]COMPLETE[/COLOR]',line2='Sorting ' + str(all_results) + ' Results',line3='[COLOR green]Please Wait[/COLOR]')
            xbmc.sleep(2000)
            progressDialog.close()

########SORTING

            sorter = 'hostname'
            if kodi.get_setting('enable_sort') =='true':
                if kodi.get_setting('sort_field') == "0":
                    sorter =  'quality'
                elif kodi.get_setting('sort_field') == "1":
                    sorter = 'debrid'
                elif kodi.get_setting('sort_field') == "2":
                    sorter = 'host'
########SORTING
            my_list = sorted(thread_results, key=lambda k: k[sorter])
            for a in my_list:
                    if a:
                        try:
                                e=a
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
                                kodi.addDir(provider + names + quals + views + premium, urls, 'get_link', thumb,movie_title + movie_year, total_items, '', 'movies',menu_items=menu_items, is_folder=False, is_playable='true',fanart=fanart)
                                viewsetter.set_view('files')
                        except:
                            pass

        except Exception as e:
                log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                if kodi.get_setting('error_notify') == "true":
                    kodi.notify(header='Movie Scrapers',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
                return



def find_sourceTV(name,thumb,media,movie_title):

    try:
        if thumb is None:
            thumb = ''
        else:
            thumb = thumb

        q = Queue.Queue()

        progressDialog.create(movie_title+': '+name, '')
        progressDialog.update(0, line1='Gathering TV Scrapers ', line2='Please wait', line3='')

        #############Constants########################
        title = movie_title[:-7]
        movie_year = movie_title[-6:]
        year = movie_year.replace('(', '').replace(')', '')
        video_type = 'shows'
        total_items = 0

        thread_results = []
        threads = []
        RunAll = Run_Scrapers()
        if kodi.get_setting('ice_films') == 'true':
            thesearch = icefilms.Scraper()
            t1 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "IceFilms", video_type, title, year,name,q),name = "IceFilms")
            threads.insert(len(threads), t1)

        if kodi.get_setting('primewire') == 'true':
            thesearch = primewire.Scraper()
            t2 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "PrimeWire", video_type, title, year,name,q),name = "Primewire")
            threads.insert(len(threads), t2)

        if kodi.get_setting('iwatchon') == 'true':
            thesearch = iwatchonline.Scraper()
            t3 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "IwatchOnline", video_type, title, year,name,q),name = "iWatchOnline")
            threads.insert(len(threads), t3)

        if kodi.get_setting('putlocker') == 'true':
            thesearch = putlocker_both.Scraper()
            t4 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "PutLocker", video_type, title, year,name,q),name = "Putlocker")
            threads.insert(len(threads), t4)

        if kodi.get_setting('watchepi') == 'true':
            thesearch = watchepisodes.Scraper()
            t5 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "WatchEpisodes", video_type, title, year,name,q),name = "WatchEpisodes")
            threads.insert(len(threads), t5)

        if kodi.get_setting('swatch') == 'true':
            thesearch = swatch_scraper.Scraper()
            t6 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "SeriesWatch",video_type, title, year,name,q),name = "SeriesWatch")
            threads.insert(len(threads), t6)

        if kodi.get_setting('2ddl') == 'true':
            thesearch = twoddl.Scraper()
            t8 = threading.Thread(target=RunAll.go_scraper_tv, args=(thesearch, "2DDL", video_type, title, year,name, q),name="2DDL")
            threads.insert(len(threads), t8)
#TODO Finish Scene Release
        # if kodi.get_setting('scener') == 'true':
        #     thesearch = scener_scraper.Scraper()
        #     t7 = threading.Thread(target=RunAll.go_scraper_tv,args=(thesearch, "SceneRelease",video_type, title, year,name,q),name = "SceneRelease")
        #     threads.insert(len(threads), t7)

        [t.start() for t in threads]
        string1 = "Time elapsed: %s seconds"
        string3 = "Remaining providers: %s"
        for t in range(0, (tv_scraper_timeout * 2) + 60):
            try:
                if xbmc.abortRequested == True: return sys.exit()

                try:
                    info = [[x.getName()] for x in threads if x.is_alive() == True]
                except:
                    info = []

                timerange = int(t * 0.5)

                try:
                    if progressDialog.iscanceled(): break
                except:
                    pass
                try:
                    string4 = string1 % str(timerange)
                    if len(info) > 5:
                        string5 = string3 % str(len(info))
                    else:
                        string5 = string3 % str(info).translate(None, "[]'")
                    progressDialog.update(
                        int((100 / float(len(threads))) * len([x for x in threads if x.is_alive() == False])),
                        str(string4), str(string5))
                except:
                    pass

                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break

                if timerange >= tv_scraper_timeout:
                    is_alive = [x for x in threads if x.is_alive() == True]
                    if not is_alive: break

                # time.sleep(0.5)
                response = q.get()
                thread_results.extend(response[2])
                all_results = len(thread_results)
            except:
                pass
        kodi.progressDialog.update(100,line1='[COLOR gold]COMPLETE[/COLOR]',line2='Sorting '+str(all_results)+' Results',line3='[COLOR green]Please Wait[/COLOR]')
        xbmc.sleep(2000)
        progressDialog.close()

#####SORTING
        sorter = 'hostname'
        if kodi.get_setting('enable_sort') == 'true':
            if kodi.get_setting('sort_field') == "0":
                sorter = 'quality'
            elif kodi.get_setting('sort_field') == "1":
                sorter = 'debrid'
            elif kodi.get_setting('sort_field') == "2":
                sorter = 'host'
########SORTING
        my_list = sorted(thread_results, key=lambda k: k[sorter])
        for a in my_list:
            if a:
                try:
                        e = a
                        if 'debrid' in e:
                            premium = " [COLOR gold]" + str(e['debrid']) + " [/COLOR]"
                        else:
                            premium = ''
                        hostname = e['hostname']
                        provider = "[COLOR white][" + hostname + "][/COLOR] - "
                        names = e['host']
                        urls = e['url']
                        if e['views'] == None:
                            views = ''
                        else:
                            views = " [COLOR green]Views " + e['views'] + "[/COLOR]"
                        if e['quality'] == None:
                            quals = ''
                        else:
                            quals = " [COLOR red][" + e['quality'] + "][/COLOR]"
                        menu_items=[]
                        kodi.addDir(provider + names + quals + views + premium,urls,'get_tv_link',thumb,movie_title,total_items,'',name,menu_items=menu_items,is_playable='true',fanart=fanart)
                        viewsetter.set_view('files')
                except:
                    pass

    except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            if kodi.get_setting('error_notify') == "tru# e":
                kodi.notify(header='Scraper',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)

class Run_Scrapers():
    def __init__(self):
        self.sources = []

    def go_scraper(self,thesearch, path, video_type, title, year, q):
        try:
            kodi.slog(path + ": Gathering Movie Sources")
            thesource = thesearch.search(video_type, title, year)
            if thesource == []:
                blank_source = []
                q.put(("done", path, blank_source, 0))
                kodi.slog(path + " GOT NONE")
            else:
                for e in thesource:
                    thesources = thesearch.get_sources(e, video_type)
                    total_sources = len(thesources)
                    q.put(("done", path, thesources, total_sources))

        except Exception as e:
            blank_source = []
            q.put(("done", path, blank_source, 0))
            kodi.slog(path + ' Failed Due to Error : ' + str(e))

    def go_scraper_tv(self,thesearch,path,video_type, title, year, name, q):
        try:
            kodi.slog(path + ": Gathering TV Sources")
            thesource = thesearch.search(video_type, title, year)
            if thesource == []:
                blank_source = []
                q.put(("done", path, blank_source,0))
                kodi.slog(path + " GOT NONE")
            else:
                for e in thesource:
                    url = e['url']
                    # TV MAIN URL RETURNED HERE
                    newseas = re.compile('S(.+?)E(.+?)  (?P<name>[A-Za-z\t .]+)').findall(name)
                    for sea, epi, epi_title in newseas:
                        video = ScraperVideo(video_type, title, year, '', sea, epi, epi_title, '')
                        theepi = thesearch._get_episode_url(url, video)
                        thehosters = thesearch.get_sources(theepi, video_type)
                        total_sources = len(thehosters)
                        q.put(("done", path, thehosters, total_sources))

        except Exception as e:
            blank_source = []
            q.put(("done", path, blank_source, 0))
            kodi.slog(path + ' Failed Due to Error : ' +str(e))




def get_link(url,movie_title,thumb,media):
    hmf = urlresolver.HostedMediaFile(url)
    ##########################################
    if hmf:
        try:
            url = urlresolver.resolve(url)
            params = {'url':url, 'title':movie_title, 'thumb':thumb}
            listitem = xbmcgui.ListItem(path=url, iconImage=thumb, thumbnailImage=thumb)
            listitem.setProperty('fanart_image', fanart)

            listitem.setPath(url)
            listitem.setInfo('video', params)

            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            movie_name = movie_title[:-6]
            movie_name = '"'+movie_name+'"'
            movie_year_full = movie_title[-6:]
            movie_year = movie_year_full.replace('(','').replace(')','')
            if kodi.get_setting('trakt_oauth_token'):
                xbmc.sleep(30000)
                kodi.log( "Velocity: Movie Scrobble  Start")
                try:
                    trakt_auth.start_movie_watch(movie_name,movie_year)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
            xbmc.sleep(30000)
            if kodi.get_setting('trakt_oauth_token'):
                check_player(movie_name,movie_year)
        except Exception as e:
            log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
            kodi.notify(header='Try Another Source', msg='Link Removed or Failed', duration=4000, sound=None)

    if not hmf:
        try:
            params = {'url':url, 'title':movie_title, 'thumb':thumb}
            addon.add_video_item(params, {'title':movie_title}, img=thumb)
            liz=xbmcgui.ListItem(movie_title, iconImage="DefaultFolder.png", thumbnailImage=thumb)
            xbmc.sleep(1000)
            liz.setPath(str(url))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
            #xbmc.Player ().play(url, liz, False)
            movie_name = movie_title[:-6]
            movie_name = '"'+movie_name+'"'
            movie_year_full = movie_title[-6:]
            movie_year = movie_year_full.replace('(','').replace(')','')
            if kodi.get_setting('trakt_oauth_token'):
                xbmc.sleep(30000)
                print "Velocity: Movie Scrobble  Start"
                try:
                    trakt_auth.start_movie_watch(movie_name,movie_year)
                except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)

            xbmc.sleep(30000)
            if kodi.get_setting('trakt_oauth_token'):
                check_player(movie_name,movie_year)
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

        params = {'url': url, 'title': media, 'thumb': thumb}
        listitem = xbmcgui.ListItem(path=url, iconImage=thumb, thumbnailImage=thumb)
        listitem.setProperty('fanart_image', fanart)
        listitem.setPath(url)
        listitem.setInfo('video', params)

        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        movie_name = movie_title[:-6]
        movie_name = '"'+movie_name+'"'
        movie_year_full = movie_title[-6:]
        movie_year = movie_year_full.replace('(','').replace(')','')
        if kodi.get_setting('trakt_oauth_token'):
            xbmc.sleep(30000)
            log_utils.log("Velocity: TV Show Scrobble  Start")
            try:
                trakt_auth.start_tv_watch(movie_name,media)
            except Exception as e:
                    log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
                    if kodi.get_setting('error_notify') == "true":
                        kodi.notify(header='Scrobble not loggged', msg='%s  %s' % (str(e), ''), duration=5000, sound=None)
        xbmc.sleep(30000)
        if kodi.get_setting('trakt_oauth_token'):
            check_tv_player(movie_name,media)

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

# def apply_urlresolverHIS(hosters):
#     filter_debrid = kodi.get_setting('filter_debrid') == 'true'
#     show_debrid = kodi.get_setting('show_debrid') == 'true'
#     if not filter_debrid and not show_debrid:
#         print "RETURNING NON FILTERED"
#         return hosters
#
#     debrid_resolvers = [resolver() for resolver in urlresolver.relevant_resolvers(order_matters=True) if
#                         resolver.isUniversal()]
#     filtered_hosters = []
#     debrid_hosts = {}
#     unk_hosts = {}
#     known_hosts = {}
#     for hoster in hosters:
#         if 'direct' in hoster and hoster['direct'] == False and hoster['host']:
#             host = hoster['host']
#             if filter_debrid:
#                 if host in unk_hosts:
#                     # log_utils.log('Unknown Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
#                     unk_hosts[host] += 1
#                     continue
#                 elif host in known_hosts:
#                     # log_utils.log('Known Hit: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
#                     known_hosts[host] += 1
#                     filtered_hosters.append(hoster)
#                 else:
#                     hmf = urlresolver.HostedMediaFile(host=host,
#                                                       media_id='dummy')  # use dummy media_id to force host validation
#                     if hmf:
#                         # log_utils.log('Known Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
#                         known_hosts[host] = known_hosts.get(host, 0) + 1
#                         filtered_hosters.append(hoster)
#                     else:
#                         # log_utils.log('Unknown Miss: %s from %s' % (host, hoster['class'].get_name()), log_utils.LOGDEBUG)
#                         unk_hosts[host] = unk_hosts.get(host, 0) + 1
#                         continue
#             else:
#                 filtered_hosters.append(hoster)
#
#             if host in debrid_hosts:
#                 # log_utils.log('Debrid cache found for %s: %s' % (host, debrid_hosts[host]), log_utils.LOGDEBUG)
#                 hoster['debrid'] = debrid_hosts[host]
#             else:
#                 temp_resolvers = [resolver.name[:3].upper() for resolver in debrid_resolvers if
#                                   resolver.valid_url('', host)]
#                 # log_utils.log('%s supported by: %s' % (host, temp_resolvers), log_utils.LOGDEBUG)
#                 debrid_hosts[host] = temp_resolvers
#                 if temp_resolvers:
#                     hoster['debrid'] = temp_resolvers
#         else:
#             filtered_hosters.append(hoster)
#
#     log_utils.log('Discarded Hosts: %s' % (sorted(unk_hosts.items(), key=lambda x: x[1], reverse=True)),
#                   log_utils.LOGDEBUG, 'get_sources')
#     return filtered_hosters


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
        if 'direct' in hoster and hoster['direct'] == False and hoster['host']:
            host = hoster['host']
            host = (host.lower())
            #
            if kodi.get_setting('filter_debrid')=='true':
                if host in unk_hosts:
                    unk_hosts[host] += 1
                    continue
                elif host in known_hosts:
                    known_hosts[host] += 1
                    filtered_hosters.append(hoster)
                else:
                    hmf = urlresolver.HostedMediaFile(host=host, media_id='dummy')  # use dummy media_id to force host validation
                    if hmf:
                        known_hosts[host] = known_hosts.get(host, 0) + 1
                        filtered_hosters.append(hoster)
                    else:
                        unk_hosts[host] = unk_hosts.get(host, 0) + 1
                        continue
            else:
                filtered_hosters.append(hoster)

            if host in debrid_hosts:
                log_utils.log('Debrid cache found for %s: %s' % (host, debrid_hosts[host]), log_utils.LOGDEBUG)
                hoster['debrid'] = debrid_hosts[host]
            else:
                temp_resolvers = []
                for resolver in debrid_resolvers:
                    if resolver.valid_url('', host):
                        rname= resolver.name.replace('Real-Debrid','RD').replace('Premiumize.me','PRE')
                        temp_resolvers.append(rname.upper())
                        if kodi.get_setting('debug') == "true":
                            print '%s supported by: %s' % (host, temp_resolvers)
                        debrid_hosts[host] = temp_resolvers
                    else:
                         hoster['debrid'] = ''
                if temp_resolvers:
                    hoster['debrid'] = temp_resolvers
        else:
            filtered_hosters.append(hoster)

    if kodi.get_setting('debug') == "true":
        kodi.log( "FILTERED HOSTERS ARE =" +str(filtered_hosters))
    return filtered_hosters


