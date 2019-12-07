# -*- coding: utf-8 -*-


import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import re,sys,urllib


#niter Add-on Created By Mucky Duck (12/2015)


addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = Addon(addon_id, sys.argv)
addon_name = addon.get_name()
addon_path = addon.get_path()
md = md(addon_id, sys.argv)

metaset = addon.get_setting('enable_meta')
show_tv = addon.get_setting('enable_shows')
show_mov = addon.get_setting('enable_movies')
show_fav = addon.get_setting('enable_favs')
show_add_set = addon.get_setting('add_set')
show_meta_set = addon.get_setting('enable_meta_set')

art = md.get_art()
icon = addon.get_icon()
fanart = addon.get_fanart()


baseurl = addon.get_setting('base_url')


reload(sys)
sys.setdefaultencoding("utf-8")




def MAIN():
        if show_mov == 'true':
		md.addDir({'mode':'1','name':'[COLOR cyan][B]MOVIES[/B][/COLOR]', 'url':'url', 'content':'movies'})
	#if show_tv == 'true':
		#md.addDir({'mode':'2','name':'[COLOR cyan][B]SERIES[/B][/COLOR]', 'url':'%s/series/' %baseurl, 'content':content})
	if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR cyan][B]MY FAVOURITES[/B][/COLOR]', 'url':'url'})
	if metaset == 'true':
		if show_meta_set == 'true':
			md.addDir({'mode':'meta_settings', 'name':'[COLOR cyan][B]META SETTINGS[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)
	if show_add_set == 'true':
		md.addDir({'mode':'addon_settings', 'name':'[COLOR cyan][B]ADDON SETTINGS[/B][/COLOR]', 'url':'url'}, is_folder=False, is_playable=False)

	setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def MOVIES(content):

        link = open_url(baseurl).content

        md.addDir({'mode':'6','name':'[COLOR cyan][B]HOW DO YOU WANT IT[/B][/COLOR]', 'url':baseurl+'/all/%s' %'movies', 'content':'movies'})
	
        if show_fav == 'true':
		md.addDir({'mode': 'fetch_favs', 'name':'[COLOR cyan][B]MY FAVOURITES[/B][/COLOR]', 'url':'url'})
	md.addDir({'mode':'search', 'name':'[B][COLOR cyan]Movie Search[/COLOR][/B]','url':'url', 'content':content})
        md.addDir({'mode':'search', 'name':'[B][COLOR cyan]Actor Search[/COLOR][/B]','url':'url', 'content':'people'})
        
        match = drop_down(link,'Movies')

        for a in match:
                md.addDir({'mode':'3', 'name':'[B][COLOR cyan]%s[/COLOR][/B]' %a['name'], 'url':a['url'], 'content':content})

        md.addDir({'mode':'5', 'name':'[B][COLOR cyan]Genres[/COLOR][/B]', 'url':'Genres', 'content':content})
        md.addDir({'mode':'5', 'name':'[B][COLOR cyan]Year[/COLOR][/B]', 'url':'Years', 'content':content})
        md.addDir({'mode':'5', 'name':'[B][COLOR cyan]People[/COLOR][/B]', 'url':'People', 'content':'people'})
        
        setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def SERIES(content):

        link = open_url(baseurl)
        md.addDir('[B][COLOR cyan]Movie Search[/COLOR][/B]','url',4,icon,fanart,'')
        md.addDir('[B][COLOR cyan]Actor/Director Search[/COLOR][/B]','url',8,icon,fanart,'')
        match=re.compile('<li><a href="(.*?)">(.*?)</a></li>').findall(link) 
        for url,name in match:
                if 'relevance' in url:
                        md.addDir('[B][COLOR cyan]%s[/COLOR][/B]' %name,url,1,icon,fanart,'')
                if 'actors' in url:
                        md.addDir('[B][COLOR cyan]%s[/COLOR][/B]' %name,url,2,icon,fanart,'')
                if 'directors' in url:
                        md.addDir('[B][COLOR cyan]%s[/COLOR][/B]' %name,url,2,icon,fanart,'')
        md.addDir('[B][COLOR cyan]Rating[/COLOR][/B]',baseurl+'movies?relevance=all&genre=all&yearFrom=1931&yearTo=2015&sortBy=rating&numRows=48&view=0',1,icon,fanart,'')
        md.addDir('[B][COLOR cyan]Genres[/COLOR][/B]',baseurl,5,icon,fanart,'')
        md.addDir('[B][COLOR cyan]Year[/COLOR][/B]',baseurl,7,icon,fanart,'')
        md.addDir('[B][COLOR cyan]A/Z[/COLOR][/B]',baseurl+'movies?relevance=all&genre=all&yearFrom=1931&yearTo=2015&sortBy=A-Z&numRows=48&view=0',1,icon,fanart,'')

        setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def INDEX(url,content):

        link = open_url(url).content
        all_videos = md.regex_get_all(link, '<figure', '</figure>')
        items = len(all_videos)

        for a in all_videos:

                name = md.regex_from_to(a, 'data-name="', '"')
                if not name:
                        name = md.regex_from_to(a, 'title="', '"')
                name = addon.unescape(name)
                year = md.regex_from_to(a, 'data-release="', '"')
                if '<div' in year:
                        year = ''
                url = md.regex_from_to(a, 'href="', '"')
                if baseurl not in url:
                        url = baseurl + url
                thumb = md.regex_from_to(a, 'src="', '"')
                if 'noimage' in thumb:
                        thumb = icon
                if 'http:' not in thumb:
                        thumb = icon
                dis = md.regex_from_to(a, 'Synopsis:</b>', '</')
                dis = addon.unescape(dis)
                fan_art = {'icon':thumb}
                
                if content == 'people':
                        if '/people/' in url or '/director/' in url:
                                md.addDir({'mode':'4', 'name':'[B][COLOR white]%s (%s)[/COLOR][/B]' %(name,year), 'url':url},
                                          fan_art=fan_art, item_count=items)
                else:
                        md.addDir({'mode':'8', 'name':'[B][COLOR white]%s (%s)[/COLOR][/B]' %(name,year),
                                   'url':url, 'content':content}, {'sorttitle':name},
                                  fan_art, is_folder=False, item_count=items)

        try:
                match=re.compile('<li><a href="(.*?)".*?>(.*?)</a></li>').findall(link) 
                for url,name in match:
                    if '&raquo;' in name:
                            md.addDir({'mode':'3', 'name':'[B][COLOR cyan][I]>>Next Page>>>[/I][/COLOR][/B]', 'url':url, 'content':content})
        except: pass

        if content == 'movies':
		setView(addon_id, 'movies', 'movie-view')
	elif content == 'tvshows':
		setView(addon_id, 'tvshows', 'show-view')
	else:
                setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def PINDEX(url):

        link = open_url(url).content
        all_links = md.regex_get_all(link, 'row actor-filmo', '</table>')
        all_videos = md.regex_get_all(str(all_links), '<tr>', '</tr>')

        items = len(all_videos)
        content = 'movies'

        for a in all_videos:

                name = md.regex_from_to(a, 'href=.*?>', '<')
                name = addon.unescape(name)
                url = md.regex_from_to(a, 'href="', '"')
                md.addDir({'mode':'8', 'name':'[B][COLOR white]%s[/COLOR][/B]' %name, 'url':url, 'content':content},
                          {'sorttitle':name}, is_folder=False, item_count=items)

        setView(addon_id, 'movies', 'movie-view')
        addon.end_of_directory()




def DROPDOWN_MENU(url,content):

        link = open_url(baseurl).content
        
        match = drop_down(link,url)

        for a in match:
                md.addDir({'mode':'3', 'name':'[B][COLOR cyan]%s[/COLOR][/B]' %
                           a['name'],'url':a['url'], 'content':content})

        setView(addon_id, 'files', 'menu-view')
	addon.end_of_directory()




def FILTER(url,content):

        link = open_url(url).content

        relevance,relevance_value,relevance_key = filterd(content,link,'Relevance:')
        genre,genre_value,genre_key = filterd(content,link,'Genre:')
        year,year_value,year_key = filterd(content,link,'Year:')
        sort_method,sort_value,sort_key = filterd(content,link,'Sort:')
        items,items_value,items_key = filterd(content,link,'# items:')

        params = {}
        params[relevance_key] = md.sort_choice(link,'Please Choose Relevance',relevance,relevance_value)
        params[genre_key] = md.sort_choice(link,'Please Choose Genre',genre,genre_value)
        params[year_key] = md.sort_choice(link,'Please Choose Year From',year,year_value)
        params['yearTo'] = md.sort_choice(link,'Please Choose Year To',year[::-1],year_value[::-1])
        params[sort_key] = md.sort_choice(link,'Please Choose Sort Method',sort_method,sort_value)
        params[items_key] = md.sort_choice(link,'Please Choose How Many Items Per Page',items,items_value)

        url_args = urllib.urlencode(params)
        filter_url = '%s?%s' %(url,url_args)
        INDEX(filter_url,content)




def SEARCH(content,query):

        try:
		if query:
			search = query.replace(' ','+')
		else:
			search = md.search()
			if search == '':
				md.notification('[COLOR gold][B]EMPTY QUERY[/B][/COLOR],Aborting search',icon)
				return
			else:
				pass

		url = '%s/search?q=%s' %(baseurl,search)
		INDEX(url,content)

	except:
		md.notification('[COLOR gold][B]Sorry No Results',icon)




def RESOLVE(url,name,content,fan_art,infolabels):

        link = open_url(url).content
        referer = url

        try:
                RequestURL = 'http://desmix.org/player/pk/pk/plugins/player_p2.php'

                try:
                        form_data={'url': re.search(r'ic=(.*?)&',link,re.I).group(1)}
                except:
                        form_data={'url': re.search(r'ic=(.*?)<',link,re.I).group(1)}

                headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                           'Origin':baseurl, 'Referer':referer, 'User-Agent':md.User_Agent()}

                r = open_url(RequestURL, 'post', data=form_data, headers=headers).content

                try:
                        data = re.findall(r'"url":"(.*?)"', str(r), re.I|re.DOTALL)[-1]
                except:
                        data = re.findall(r'"url":"(.*?)"', str(r), re.I|re.DOTALL)[0]

                data = data.replace('.pdf','.mp4')
                host = data.split('//')[1].split('/')[0]  
                headers = {'Host':host, 'Referer':referer, 'User-Agent':md.User_Agent()}
                final = data + '|' + urllib.urlencode(headers)
                md.resolved(final, name, fan_art, infolabels)

        except:
                pass
                

        try:
                data = re.findall(r'dir=(.*?)&', str(link), re.I|re.DOTALL)[0]
                headers = {'Referer': referer, 'User-Agent': md.User_Agent()}
                final = data + '|' + urllib.urlencode(headers)
                md.resolved(final, name, fan_art, infolabels)
        except:
                pass

        try:
                try:
                    RequestURL = re.search(r'emb.*?=(.*?)&',link,re.I).group(1)
                except:
                    RequestURL = re.search(r'emb.*?=(.*?)<',link,re.I).group(1)


                if 'videomega' in RequestURL:
                        headers = {'Host': 'videomega.tv', 'Referer': referer, 'User-Agent': md.User_Agent()}
                        link = open_url(RequestURL, headers=headers).content
                        if jsunpack.detect(link):
                                js_data = jsunpack.unpack(link)
                                match = re.search('"src"\s*,\s*"([^"]+)', js_data)
                        headers = {'Origin': 'videomega.tv', 'Referer': link, 'User-Agent': md.User_Agent()}
                        final = match.group(1) + '|' + urllib.urlencode(headers)

                elif 'up2stream' in RequestURL:
                        headers = {'Referer': referer, 'User-Agent': User_Agent}
                        link = open_url(RequestURL, headers=headers).content
                        if jsunpack.detect(link):
                                js_data = jsunpack.unpack(link)
                                match = re.search('"src"\s*,\s*"([^"]+)', js_data)
                        headers = {'Origin': 'http://up2stream.com', 'Referer': RequestURL, 'User-Agent': md.User_Agent()}
                        final = match.group(1) + '|' + urllib.urlencode(headers)
                        md.resolved(final, name, fan_art, infolabels)
        except:
                pass

        addon.end_of_directory()




def drop_down(data,key):
        
        link = md.replace_space(data)

        data = md.regex_get_all(link, 'dropdown">%s<' %key, '</ul>')
        all_links = md.regex_get_all(str(data), '<li>', '</li>')
        r = []

        for a in all_links:
                name = md.regex_from_to(a, 'href=.*?>', '<')
                name = md.space_before_cap(name)
		url = md.regex_from_to(a, 'href="', '"')
		r.append({'name':name, 'url':url})

        return r




def filterd(content,data,key):

        data_name = []
        data_val = []
        all_data = md.regex_get_all(data, '<strong class="">%s</strong>' %key, '</select>')[0]
        data_id = re.search(r'id="(.*?)"',str(all_data),re.I).group(1)
        data = md.regex_get_all(str(all_data), '<option', '</option')

        for a in data:
                name = md.regex_from_to(a, 'value=.*?>', '<')
                val = md.regex_from_to(a, 'value="', '"')
		data_name.append('[COLOR cyan][B][I]%s[/I][/B][/COLOR]' %name)
		data_val.append(val)

        return data_name,data_val,data_id




mode = md.args['mode']
url = md.args.get('url', None)
name = md.args.get('name', None)
query = md.args.get('query', None)
title = md.args.get('title', None)
year = md.args.get('year', None)
season = md.args.get('season', None)
episode = md.args.get('episode' ,None)
infolabels = md.args.get('infolabels', None)
content = md.args.get('content', None)
mode_id = md.args.get('mode_id', None)
iconimage = md.args.get('iconimage', None)
fan_art = md.args.get('fan_art', None)
is_folder = md.args.get('is_folder', True)




if mode is None or url is None or len(url)<1:
        MAIN()

elif mode == '1':
        MOVIES(content)

elif mode == '2':
        SERIES(content)

elif mode == '3':
        INDEX(url,content)

elif mode == '4':
        PINDEX(url)

elif mode == '5':
        DROPDOWN_MENU(url,content)

elif mode == '6':
        FILTER(url,content)

elif mode == '8':
        RESOLVE(url,name,content,
                fan_art,infolabels)

elif mode == 'search':
	SEARCH(content,query)

elif mode == 'addon_search':
	md.addon_search(content,query,fan_art,infolabels)

elif mode == 'add_remove_fav':
	md.add_remove_fav(name,url,infolabels,fan_art,
			  content,mode_id,is_folder)

elif mode == 'fetch_favs':
	md.fetch_favs(baseurl)

elif mode == 'addon_settings':
	addon.show_settings()

elif mode == 'meta_settings':
	import metahandler
	metahandler.display_settings()

md.check_source()
addon.end_of_directory()
