from metahandler import metahandlers
import teevee2,control,cache
import re
from log_utils import log

enabled = control.setting('tv_metadata')=='true'
metaget=metahandlers.MetaData()       

def get_show_meta(showtitle,url,year='',imdb=''):
    meta = None
    if enabled: 
        
        meta = cache.get(metaget.get_meta,10000,'tvshow', showtitle,imdb,'',year)
        if meta is None:
            imdb,year = cache.get(teevee2.get_info,10000,url)
            meta = cache.get(metaget.get_meta,10000,'tvshow', showtitle,imdb,'',year)

    if meta is None:
        meta={}
        title='%s (%s)'%(showtitle,year)
        meta['title'] = title
        meta['name'] = title
        meta['tvshowtitle'] = showtitle
        meta['cover_url'] = control.icon_path('TV_Shows.png')
        meta['backdrop_url'] = None

    if meta['cover_url']=='':
        meta['cover_url'] = cache.get(teevee2.get_thumbnail,10000,url)
    if meta['backdrop_url']=='':
        meta['backdrop_url'] = control.icon_path('fanart.jpg')
    
    return meta

def get_episode_meta(showtitle,season,episode,url,imdb='',ep_title='',more=False):
    meta = None

    show_url = url.rstrip('/').split('/')
    show_url.pop(-1)
    show_url = '/'.join(show_url)
    if 'iwatch' not in url:
        thumbnail = cache.get(teevee2.get_thumbnail,10000,show_url)
    else:
        thumbnail = control.icon_path('TV_Shows.png')
        
    if enabled:
        meta = cache.get(metaget.get_episode_meta,10000,showtitle, imdb, season.lstrip("0"), episode.lstrip("0"))
        if meta is None and 'iwatch' not in url:
            imdb,year = cache.get(teevee2.get_info,10000,show_url)
            cache.get(metaget.get_episode_meta,10000,showtitle, imdb, season.lstrip("0"), episode.lstrip("0"))
        if meta and more:
            meta['title']='%s %sx%s %s'%(showtitle,season,episode,meta['title'].encode('ascii','ignore'))
        if meta and not more:
            meta['title']='%sx%s %s'%(season,episode,meta['title'].encode('ascii','ignore'))

    if meta is None:


        meta={}
        title='%s: %sx%s'%(showtitle,season,episode)
        if ep_title=='':
            ep_title=title
        else:
            title = title='%sx%s %s'%(season,episode,ep_title)
        meta['title']=title
        meta['name']=ep_title
        meta['tvshowtitle']=showtitle
        meta['season']=season
        meta['episode']=episode
        meta['cover_url']=thumbnail
        meta['backdrop_url']=None

    if meta['cover_url']=='':
        meta['cover_url']=thumbnail

    if meta['backdrop_url']=='':
        meta['backdrop_url'] = control.icon_path('fanart.jpg')
        
    return meta



def get_season_meta(showtitle,season,imdb=''):
    meta = None
    seson = [i for i in range(1,season+1)]
    if enabled:
        meta = metaget.get_seasons(showtitle, imdb, seson)

    else:
        meta = []
        for s in seson:
            meta.append({'Season':s,'cover_url':control.icon_path('TV_Shows.png'),'backdrop_url':control.icon_path('fanart.jpg')})

    return meta