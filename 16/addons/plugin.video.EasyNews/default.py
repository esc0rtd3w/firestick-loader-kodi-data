import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,base64,datetime,os
import settings
from urlparse import urlparse
import time
import threading
from functools import wraps
import json
from addon.common.addon import Addon

PLUGIN='plugin.video.EasyNews'

#Global Constants
addon_id='plugin.video.EasyNews'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')

VERSION = ADDON.getAddonInfo('version')
art = ADDON_PATH + "/resources/icons/"
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

username = ADDON.getSetting('easy_user')
password = ADDON.getSetting('easy_pass')
#lovefilm='http://www.lovefilm.com/browse/film/films/dvd/'
downloads=ADDON.getSetting('download_path')
if ADDON.getSetting('visitor_ga')=='':
    from random import randint
    ADDON.setSetting('visitor_ga',str(randint(0, 0x7fffffff)))
    
base='http://dl.dropbox.com/u/129714017/hubmaintenance/'
VERSION = "5.0.0"
PATH = "EasyNews"            
UATRACK="UA-35537758-1"

        
mlangex = settings.mlang_ex()
mreso = settings.m_reso()
mfilesize=settings.m_filesize()
mmaxfilesize= settings.m_maxfilesize()
mfileext= settings.m_fileext()
msubject= settings.m_subject()
mposter= settings.m_poster()
mnewsgroup= settings.m_newsgroup()
mfilename= settings.m_filename()
mvcodec= settings.m_vcodec()
macodec= settings.m_acodec()
mfilename =settings.m_filename()
mresults =settings.m_results()
mspam = settings.m_spam()
mrem = settings.m_rem()
mgrex = settings.m_grex()
tvresults = settings.tv_results()
tvfileext= settings.tv_fileext()
tvfilesize=settings.tv_filesize()
tvmaxfilesize= settings.tv_maxfilesize()
tvgrex = settings.tv_grex()
tvlangex = settings.tvlang_ex()
tvreso = settings.tv_reso()
tvsubject = settings.tv_subject()
tvposter =settings.tv_poster()
tvnewsgroup =settings.tv_newsgroup()
tvvcodec= settings.tv_vcodec()
tvacodec = settings.tv_acodec()
tvfilename = settings.tv_filename()
tvspam = settings.tv_spam()
tvrem = settings.tv_rem()
glresults = settings.gl_results()
glfileext= settings.gl_fileext()
glfilesize=settings.gl_filesize()
glmaxfilesize= settings.gl_maxfilesize()
glgrex = settings.gl_grex()
gllangex = settings.gllang_ex()
glreso = settings.gl_reso()
glsubject = settings.gl_subject()
glposter =settings.gl_poster()
glnewsgroup =settings.gl_newsgroup()
glvcodec= settings.gl_vcodec()
glacodec = settings.gl_acodec()
glfilename = settings.gl_filename()
glspam = settings.gl_spam()
glrem = settings.gl_rem()
IMDBTV_WATCHLIST = settings.imdbtv_watchlist_url()
IMDB_LIST = settings.imdb_list_url()
# iconimg='https://dl.dropbox.com/u/35759481/Mikey1234/KaraokeArt/'


           
def MOVIE_CATEGORIES():
        addDir('[B][COLOR blue]Search EasyNews[/COLOR][/B]','url',1,art+'s_en.jpg',FANART,'','','')
        addDir('[B][COLOR white]Most Popular Movies[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=moviemeter&title_type=feature',32,art+'pop.jpg',FANART,'','','')
        addDir('[B][COLOR white]IMDb US Box Office[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=boxoffice_gross_us&title_type=feature',32,art+'box.jpg',FANART,'','','')
        addDir('[B][COLOR white]IMDb US Release Date[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=release_date_us,desc&title_type=feature',32,art+'release.jpg',FANART,'','','')
        addDir('[B][COLOR white]IMDb All Time Top Movies[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&title_type=feature',32,art+'all.jpg',FANART,'','','')
        addDir('[B][COLOR white]IMDb Genres[/COLOR][/B]','http://akas.imdb.com/genre',33,art+'genre.jpg',FANART,'','','')
        if ADDON.getSetting('imdb') == 'true':
                addDir('[B][COLOR white]IMDb List[/COLOR][/B]','url',25,art+'list.jpg',FANART,'','','')
        addDir('[B][COLOR blue]Search for a Movie[/COLOR][/B]','url',6,art+'mov_search.jpg',FANART,'','','')
        addDir('[B][COLOR white]TV Shows Popular[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=moviemeter&title_type=tv_series',9,art+'pop_tv.jpg',FANART,'','','')
        addDir('[B][COLOR white]All Time Shows[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=user_rating&title_type=tv_series',9,art+'all_tv.jpg',FANART,'','','')
        addDir('[B][COLOR white]TV Release Date[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=release_date_us,desc&title_type=tv_series',9,art+'tv_rel.jpg',FANART,'','','')
        addDir('[B][COLOR white]A to Z Shows[/COLOR][/B]','http://akas.imdb.com/search/title?num_votes=5000,&sort=alpha,asc&start=&title_type=tv_series',9,art+'a_z_tv.jpg',FANART,'','','')  
        addDir('[B][COLOR blue]Search for a Show[/COLOR][/B]','url',12,art+'tv_search.jpg',FANART,'','','')
        xbmc.executebuiltin('Container.SetViewMode(50)')
            
# def TOP_CATEGORIES():
        # addDir('Action',lovefilm+'action/p1/?rows=50',14,art+'action.png','','','','')
        # addDir('Animated',lovefilm+'animated/p1/?rows=50',14,art+'animated.png','','','','')
        # addDir('BollyWood',lovefilm+'bollywood/p1/?rows=50',14,art+'bollywood.png','','','','')
        # addDir('Children',lovefilm+'childrens/p1/?rows=50',14,art+'childrens.png','','','','')
        # addDir('Comedy',lovefilm+'comedy/p1/?rows=50',14,art+'comedy.png','','','','')
        # addDir('Crime',lovefilm+'action/crime/p1/?rows=50',14,art+'crime.png','','','','')
        # addDir('Drama',lovefilm+'drama/p1/?rows=50',14,art+'drama.png','','','','')
        # addDir('Family',lovefilm+'family/p1/?rows=50',14,art+'family.png','','','','')
        # addDir('Historical',lovefilm+'action/historical/p1/?rows=50',14,art+'historical.png','','','','')
        # addDir('Horror',lovefilm+'horror/p1/?rows=50',14,art+'horror.png','','','','')
        # addDir('Musical',lovefilm+'music/p1/?rows=50',14,art+'musical.png','','','','')
        # addDir('Romance',lovefilm+'romance/p1/?rows=50',14,art+'romance.png','','','','')
        # addDir('Sci-Fi',lovefilm+'sci-fi/p1/?rows=50',14,art+'sci-fi.png','','','','')
        # addDir('Super Heroes',lovefilm+'action/superheroes/p1/?rows=50',14,art+'superheros.png','','','','')
        # addDir('Thriller',lovefilm+'thriller/p1/?rows=50',14,art+'thriller.png','','','','')
        # addDir('War',lovefilm+'action/war/p1/?rows=50',14,art+'war.png','','','','')
        # addDir('[COLOR red][B]<< Return Movie Menu[/B][/COLOR]','url',4,art+'back.png','','','','')    
        # setView('movies', 'default-view')    
        
# def TV_CATEGORIES():
        # addDir('Search Tv Shows','url',12,art+'searchtv.png','','','','')
        # addDir('Current Popular','http://akas.imdb.com/search/title?num_votes=5000,&sort=moviemeter&title_type=tv_series',9,art+'currentpopular.png','','','','')
        # addDir('All Time Popular','http://akas.imdb.com/search/title?num_votes=5000,&sort=user_rating&title_type=tv_series',9,art+'alltimepopular.png','','','','')
        # addDir('Release Date','http://akas.imdb.com/search/title?num_votes=5000,&sort=release_date_us,desc&title_type=tv_series',9,art+'newreleases.png','','','','')
        # addDir('A to Z','http://akas.imdb.com/search/title?num_votes=5000,&sort=alpha,asc&start=&title_type=tv_series',9,art+'atoz.png','','','','')
        # addDir('[COLOR red][B]<< Return Main Menu[/B][/COLOR]','','',art+'back.png','','','','')    
        # setView('movies', 'default-view')
        
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
           
def passman(theurl):
        import cookielib
        cookies = cookielib.LWPCookieJar()
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, theurl, username, password)
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies),
            urllib2.HTTPBasicAuthHandler(passman)
            ]
        opener = urllib2.build_opener(*handlers)
        urllib2.install_opener(opener)
        pagehandle = urllib2.urlopen(theurl)
        link= pagehandle.read()
        for cookie in cookies:
            COOKIE= cookie.name+'='+cookie.value
           
        return link ,COOKIE
        
def Fileextension(name):
            mkv=''
            avi=''
            vob=''
            mov=''
            mp4=''
            iso=''
            m4v=''
            wmv=''
            flv=''
            if re.search('.mkv', name, re.IGNORECASE):
                    mkv= 'MKV'    
            if not re.search('.mkv', name, re.IGNORECASE):
                    mkv= ''          
            if re.search('.avi', name, re.IGNORECASE):
                    avi= 'AVI' 
            if not re.search('.avi', name, re.IGNORECASE):
                    avi= ''          
            if re.search('.vob', name, re.IGNORECASE):
                    vob= 'VOB'
            if not re.search('.vob', name, re.IGNORECASE):
                    vob= ''     
            if re.search('.mov', name, re.IGNORECASE):
                    mov= 'MOV'
            if not re.search('.mov', name, re.IGNORECASE):
                    mov= '' 
            if re.search('.mp4', name, re.IGNORECASE):
                    mp4= 'MP4'
            if not re.search('.mp4', name, re.IGNORECASE):
                    mp4= '' 
            if re.search('.iso', name, re.IGNORECASE):
                    iso= 'ISO'
            if not re.search('.iso', name, re.IGNORECASE):
                    iso= ''
            if re.search('.m4v', name, re.IGNORECASE):
                    m4v='M4V'
            if not re.search('.m4v', name, re.IGNORECASE):
                    m4v= '' 
            if re.search('.flv', name, re.IGNORECASE):
                    flv='FLV'
            if not re.search('.flv', name, re.IGNORECASE):
                    flv= '' 
            if re.search('.wmv', name, re.IGNORECASE):
                    wmv='WMV'
            if not re.search('.wmv', name, re.IGNORECASE):
                    wmv= ''  
            allofthem=str(mkv)+str(avi)+str(vob)+str(mov)+str(mp4)+str(iso)+str(m4v)+str(flv)+str(wmv)
            return allofthem
            
# def SEARCH_CATEGORIES():
        # addDir('Search Movies','url',6,art+'searchmovies.png','','','','')
        # addDir('Actor Search','url',16,art+'newreleases.png','','','','')
        # addDir('Actress Search','url',17,art+'newreleases.png','','','','')
        # xbmc.executebuiltin('Container.SetViewMode(50)')
    
def SEARCH(url):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search EasyNews')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            if search_entered == None:
                return False          
        dialog = xbmcgui.Dialog()
        if ADDON.getSetting('searchnoclick')=='false':
            if dialog.yesno("Search Options", "Choose your required quality?", "Custom: Use your custom settings", "Any: Returns any available quality", glfileext, "Any"):
                    theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+gllangex+'&sbj='+glsubject+'&from='+glposter+'&ns='+glnewsgroup+'&fil='+glfilename+'&fex=&vc='+glvcodec+'&ac='+glacodec+'&pby='+glresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+glfilesize+'&b2t='+glmaxfilesize+glreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+glspam+glrem+glgrex+'&st=adv&safeO'
            else:
                    theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+gllangex+'&sbj='+glsubject+'&from='+glposter+'&ns='+glnewsgroup+'&fil='+glfilename+'&fex='+glfileext+'&vc='+glvcodec+'&ac='+glacodec+'&pby='+glresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+glfilesize+'&b2t='+glmaxfilesize+glreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+glspam+glrem+glgrex+'&st=adv&safeO'
        else:
            theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+gllangex+'&sbj='+glsubject+'&from='+glposter+'&ns='+glnewsgroup+'&fil='+glfilename+'&fex='+glfileext+'&vc='+glvcodec+'&ac='+glacodec+'&pby='+glresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+glfilesize+'&b2t='+glmaxfilesize+glreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+glspam+glrem+glgrex+'&st=adv&safeO'
        if ADDON.getSetting('ssl') == 'true':
            theurl = str(theurl).replace('http:','https:')
            SSL='https://'
        else:
            theurl = str(theurl)
            SSL='http://'
        link,COOKIE=passman(theurl)   
        link = json.loads(link, encoding='utf8')
        results=link['results']
        data=link['data']

        for field in data:
            num= field['0']
            size= field['4']
            codec=field['11']
            name=field['10']
            lang=field['alangs']
            lang='[COLOR yellow]%s[/COLOR]'%(lang)
            url=SSL+'members.easynews.com/dl/'+num+codec+'/'+name+codec+'|Authorization=Basic%20' + base64.b64encode('%s:%s' % (username, password))
            name = '[B][%s %s] %s[/B]' %(size,codec.replace('.','').upper(),lang)+' '+name
            name = name.replace('None','').replace("u'",'').replace("'",'')

            downloadname=str(search_entered).replace('+',' ')+codec
            
            iconimage='http://th.easynews.com/thumbnails-'+num[0]+num[1]+num[2]+'/pr-'+num+'.jpg'
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            addLink(name,url,iconimage,FANART,'','',downloadname)
        addDir('[COLOR yellow][B]PLEASE SEARCH ARCHIVE INSTEAD[/B][/COLOR]',theurl,15,art+'searchmovies.png','','','','')  
        setView('movies', 'movie-view')  
        
# def actorsearch():
        # search_entered = ''
        # keyboard = xbmc.Keyboard(search_entered, 'Search EasyNews...XUNITYTALK.COM')
        # keyboard.doModal()
        # if keyboard.isConfirmed():
            # search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            # if search_entered == None:
                # return False  
        # link=OPEN_URL('http://www.imdb.com/search/name?name='+search_entered)
        # match=re.compile('<a href="(.+?)" title=".+?"><img src=".+?"').findall(link)
        # url='http://www.imdb.com'+match[0]+'filmotype/actor'
        # link=OPEN_URL(url).replace('\n','').replace('<img src="http://i.media-imdb.com/images/SF9340d31a91d54b19f05ac3c0e596ea5c/mobile/logo_55x29.png','')
        # match=re.compile('<span class="retina-capable"><img src="(.+?)".+?onClick="_gaq.push.+?">(.+?)</a> (.+?)    </div').findall(link)
        # for iconimage,name,year in match:
            # year=year.replace('TV series ','') 
            # regex=re.compile('(.+?)_V1.+?.jpg')
            # regex1=re.compile('(.+?).gif')
            # try:
                    # match = regex.search(iconimage)
                    # iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
            # except:
                    # pass
            # try:    
                    # match= regex1.search(iconimage)
                    # iconimage= '%s.gif'%(match.group(1))
            # except:
                    # pass
            # addDir(name+' '+year,'url',3,iconimage,'','','','')
            
# def actresssearch():
        # search_entered = ''
        # keyboard = xbmc.Keyboard(search_entered, 'Search EasyNews...XUNITYTALK.COM')
        # keyboard.doModal()
        # if keyboard.isConfirmed():
            # search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20
            # if search_entered == None:
                # return False  
        # link=OPEN_URL('http://m.imdb.com/search/name?name='+search_entered)
        # match=re.compile('<a href="(.+?)" title=".+?"><img src=".+?"').findall(link)
        # url='http://m.imdb.com'+match[0]+'filmotype/actress'
        # link=OPEN_URL(url).replace('\n','').replace('<img src="http://i.media-imdb.com/images/SF9340d31a91d54b19f05ac3c0e596ea5c/mobile/logo_55x29.png','')
        # match=re.compile('<span class="retina-capable"><img src="(.+?)".+?onClick="_gaq.push.+?">(.+?)</a> (.+?)    </div').findall(link)
        # for iconimage,name,year in match:
            # year=year.replace('TV series ','') 
            # regex=re.compile('(.+?)_V1.+?.jpg')
            # regex1=re.compile('(.+?).gif')
            # try:
                    # match = regex.search(iconimage)
                    # iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
            # except:
                    # pass
            # try:    
                    # match= regex1.search(iconimage)
                    # iconimage= '%s.gif'%(match.group(1))
            # except:
                    # pass
            # addDir(name+' '+year,'url',3,iconimage,'','','','')
        
def IMDB_SEARCH(name,iconimage):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search EasyNews')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20#
            if search_entered == None:
                return False   
        url= 'http://akas.imdb.com/search/title?title=%s&title_type=feature'% (search_entered) 
        ALLTIMEIMDB(url)        
        # req = urllib2.Request(url)
        # req.add_header('User-Agent', USER_AGENT)
        # response = urllib2.urlopen(req)
        # link=response.read()
        # response.close()
        # LINK=link.split('class="loadlate"')
        # match=[]
        
        # for p in LINK:
            # try:
                # iconimage = re.compile('loadlate="(.+?)"').findall(p)[0]
                # title = re.compile('v_li_tt"\n>(.+?)<').findall(p)[0]
                # year = re.compile('class="lister-item-year text-muted unbold">(.+?)</span>').findall(p)[0]
                # name = title + ' ' + year
                # description = re.compile('<p class="text-muted">\n(.+?)<').findall(p)[0]
                # match.append([name, iconimage])                          
            # except:pass  
        # #match=re.compile('title="(.+?)"><img src="(.+?)"').findall(link)
        # for name,iconimage in match:
            # regex=re.compile('(.+?)_V1.+?.jpg')
            # regex1=re.compile('(.+?).gif')
            # try:
                    # match = regex.search(iconimage)
                    # iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                    # fanart= '%s_V1.jpg'%(match.group(1))
            # except:
                    # pass
            # try:    
                    # match= regex1.search(iconimage)
                    # iconimage= '%s.gif'%(match.group(1))
                    # fanart= '%s_V1.jpg'%(match.group(1))
            # except:
                    # pass
            # addDir(name,url,3,iconimage,FANART,description,'','')
        # setView('movies', 'movie-view')
                                                                
def TMDB(url):
        link=OPEN_URL(url)
        match = re.compile('<div class="item poster card".+?title="(.+?)".+?data-src="(.+?)"',re.DOTALL).findall(link)
        nextp=re.compile('class="right pagination"><a href="(.+?)"').findall(link)
        try:
                nextp1=nextp[0]
        except:
                pass
        for name,iconimage in match:
            name = str(name).replace('&hellip;','')
            iconimage = str(iconimage).replace('w92','original')
            fanart = str(iconimage)
            addDir(name,'url',3,iconimage,fanart,'','','')
            setView('movies', 'default-view') 
        try:
                url=str(nextp1)
                name= '[COLOR blue][B]Next Page >>[/B][/COLOR]'
                addDir(name,'https://www.themoviedb.org%s'%url,2,art+'next.png','','','','')    
                setView('movies', 'movies-view') 
        except:
                pass
        #addDir('[COLOR red][B]<< Return To Movie Menu[/B][/COLOR]','url',4,art+'back.png','','','','')    
        setView('movies', 'movies-view') 
             
def ONDVD(url):
        link=OPEN_URL(url)
        link1=str(link).replace('\n','').replace('\t','')
        match=re.compile(' <img src="(.+?)" alt="(.+?)"').findall(link1)
        nextp=re.compile('<a href="(.+?)"  >Next &gt;</a>').findall(link)
        try:
                nextp1=nextp[0]
        except:
                pass
        for iconimage, name in match:
            name = str(name).replace('&#39;','').replace('-','').replace('&amp;','And').replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e')
            iconimage = str(iconimage).replace('UX140_CR0,0,140,200','UX420_CR0,0,420,600')
            addDir(name,'url',3,iconimage,'','','','')
            setView('movies', 'movies-view')
        try:
                url=str(nextp1).replace('/?','/?sort_by=release_date&r=50&')
                name= '[COLOR blue][B]Next Page >>[/B][/COLOR]'
                addDir(name,url,14,art+'next.png','','','','')    
                setView('movies', 'movies-view') 
        except:
                pass
        #addDir('[COLOR red][B]<< Return To Movie Menu[/B][/COLOR]','url',4,art+'back.png','','','','')    
        setView('movies', 'movies-view') 
        

            
                                              
def EasySearch(name,iconimage, fanart):
        try:
            search_entered = str(name).split(' (')[0].replace("The ",'').replace("the ",'').replace('.','').replace(', ','+').replace(' ','+') .replace(':','').replace('[','').replace(']',' ').replace('(The)','').replace('(','') .replace(')','') .replace('-','+').replace("'",'') .replace("&",'').replace("!",'').replace("Assemble",'2012')           
        except:
            search_entered = str(url).replace("The ",'').replace("the ",'').replace('.','').replace(', ','+').replace(' ','+') .replace(':','').replace('[','').replace(']',' ').replace('(The)','').replace('(','') .replace(')','') .replace('-','+').replace("'",'') .replace("&",'').replace("!",'').replace("Assemble",'2012')           
        dialog = xbmcgui.Dialog()
        if ADDON.getSetting('movienoclick')=='false':
            if dialog.yesno("Search Options", "Choose your required quality?", "Custom: Use your custom settings", "Any: Returns any available quality", mfileext, "Any"):
                    theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+mlangex+'&sbj='+msubject+'&from='+mposter+'&ns='+mnewsgroup+'&fil='+mfilename+'&fex=&vc='+mvcodec+'&ac='+macodec+'&pby='+mresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+mfilesize+'&b2t='+mmaxfilesize+mreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+mspam+mrem+mgrex+'&st=adv&safeO=0&sb=1'
            else:
                    theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+mlangex+'&sbj='+msubject+'&from='+mposter+'&ns='+mnewsgroup+'&fil='+mfilename+'&fex='+mfileext+'&vc='+mvcodec+'&ac='+macodec+'&pby='+mresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+mfilesize+'&b2t='+mmaxfilesize+mreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+mspam+mrem+mgrex+'&st=adv&safeO=0&sb=1'
        else:
            theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+mlangex+'&sbj='+msubject+'&from='+mposter+'&ns='+mnewsgroup+'&fil='+mfilename+'&fex='+mfileext+'&vc='+mvcodec+'&ac='+macodec+'&pby='+mresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+mfilesize+'&b2t='+mmaxfilesize+mreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+mspam+mrem+mgrex+'&st=adv&safeO=0&sb=1'
        if ADDON.getSetting('ssl') == 'true':
            theurl = str(theurl).replace('http:','https:')
            SSL='https://'
        else:
            theurl = str(theurl)
            SSL='http://'
        link,COOKIE=passman(theurl) 
        link = json.loads(link, encoding='utf8')
        results=link['results']
        data=link['data']
        #print data
        for field in data:
            num= field['0']
            size= field['4']
            codec=field['11']
            name=field['10']
            lang=field['alangs']
            lang='[COLOR yellow]%s[/COLOR]'%(lang)
            url=SSL+'members.easynews.com/dl/'+num+codec+'/'+name+codec+'|Authorization=Basic%20' + base64.b64encode('%s:%s' % (username, password))
            name = '[B][%s %s] %s[/B]' %(size,codec.replace('.','').upper(),lang)+' '+name
            name = name.replace('None','').replace("u'",'').replace("'",'')

            downloadname=name.split('[/B] ')[1]+codec
            iconimage='http://th.easynews.com/thumbnails-'+num[0]+num[1]+num[2]+'/pr-'+num+'.jpg'
            #print iconimage
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            addLink(name,url,iconimage,fanart,'','',downloadname)
        try:
            _name = str(name).split(' (')[0]
        except:
            search_entered = str(url)
        addDir('[COLOR yellow][B]PLEASE SEARCH ARCHIVE INSTEAD[/B][/COLOR]',theurl,15,art+'searchmovies.png','','',_name,'')  
        setView('movies', 'movie-view')
            
def EasySearch_tryagain(url,iconimage, description):
        theurl=url.replace('members.easynews.com/2.0/search/solr-search/advanced?','members.easynews.com/global4/search.html?').replace('https://','http://')
        #print theurl
        link,COOKIE= passman(theurl)      
        match=re.compile('url="http://(.+?)" length="(.+?)" type="application/octet-stream" />\n<link>http.+?com/dl/.+?/.+?/.+?/(.+?)</link>').findall(link)
        iconimage=str(iconimage)
        for url ,filesize, name in match:
            match=url.split('80/')[1]
            match=match.split('.')[0]
            iconimage='http://th.easynews.com/thumbnails-%s%s%s/pr-%s.jpg'%(match[0],match[1],match[2],match[0:41])
            all=Fileextension(name)
            name = '[[B]%s %s[/B]]' % (filesize,all)+'  '+str(name).replace('%20',' ').replace('%28','(').replace('%29',')').replace('.mkv','').replace('.avi','').replace('.iso','').replace('.mov','').replace('.mp4','').replace('.m4v','').replace('.vob','').replace('.flv','').replace('.wmv','').replace('%5B','').replace('%5C','').replace('%5A','')
            url =SSL+str(url)+'|Cookie='+COOKIE
            downloadname=str(description).replace('+',' ')+'.'+str(all).lower()
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            addLink(name,url,iconimage,'','','',downloadname)
        setView('movies', 'movie-view') 
            
                
def TV_POPULAR(url):
        link=OPEN_URL(url)
        LINK=link.split('class="loadlate"')
        match=[]
        
        for p in LINK:
            try:
                iconimage = re.compile('loadlate="(.+?)"').findall(p)[0]
                url = re.compile('href="(.+?)"').findall(p)[0]
                try:url=url.split('?')[0]
                except:pass
                name = re.compile('v_li_tt"\n>(.+?)<').findall(p)[0]
                description = re.compile('<p class="text-muted">\n(.+?)<').findall(p)[0]
                match.append([iconimage, name,url, description])                          
            except:pass  
        nextp=re.compile('<a href="(.+?)\&ref_=adv_nxt"').findall(link)
        try:      
                nextp1=nextp[0]
        except:
                pass       
        for iconimage, name, url, description in match:
            name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#x26;','And')
            iconimage1 = iconimage
            url = 'http://akas.imdb.com'+str(url)
            series = str(name).replace('&#xB7','').replace('&#x27;','').replace('&#x26;','And').replace('&#x26;','And')
            regex=re.compile('(.+?)_V1.+?.jpg')
            regex1=re.compile('(.+?).gif')
            try:
                    match = regex.search(iconimage1)
                    iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
            try:    
                    match= regex1.search(iconimage1)
                    iconimage= '%s.gif'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
            addDir(name,url,10,iconimage,fanart,series,description,'')   
 
        try:
                url='http://akas.imdb.com/search/title'+str(nextp1)
                name= '[COLOR blue][B]Next Page >>[/B][/COLOR]'
                addDir(name,url,9,art+'next.png','','','','')  
        except:
                pass
        setView('movies', 'movie-view')

def TV_SEASON(url,iconimage,series,fanart):
        #print url
        link=OPEN_URL(url)

        #match = re.compile('<a href=".+?episode.+?season=(.+?)&ref').findall(link)
        match = re.compile('<a href=".+?episodes\?season=(.+?)&').findall(link)
        
        url2= str(url)
        try:url2=url2.split('?')[0]
        except:pass
        for season in match:
            url = str(url2)+'episodes?season='+str(season)
            #print url
            name = 'Season '+str(season)
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            addDir(name,url,11,iconimage,fanart,series,'','') 
        setView('movies', 'movie-view')
            
def TV_EPISODE(url,iconimage,series,fanart):
        links=OPEN_URL(url)
        p=links.split('itemprop="url">')
        series1=series
        replacementicon=series
        icon=iconimage
        for link in p:
                #print p
	        if 'itemprop="episodes"' in link:
                        try:
                            icons=link.split('src="')[1]
                            iconimage=icons.split('"')[0]
                        except:iconimage=''    
		        ep=link.split('<div>')[1]
		        _name=link.split('itemprop="name">')[1]
		        des=link.split('<div class="item_description" itemprop="description">')[1]
		        description=des.split('</div>')[0]
		        name=_name.split('</a>')[0]
		        episode=ep.split('</div>')[0]
		        if iconimage.endswith(".png"):
		                iconimage = str(icon)
		        description= str(description).replace('&#700;','').replace('">','')
		        iconimage1= iconimage
		        episode='['+str(episode).replace('26,','26').replace('25,','25').replace('24,','24').replace('23,','23').replace('22,','22').replace('21,','21').replace('20,','20').replace('19,','19').replace('18,','18').replace('17,','17').replace('16,','16').replace('15,','15').replace('14,','14').replace('13,','13').replace('12,','12').replace('11,','11').replace('10,','10').replace('9,','09').replace('8,','08').replace('7,','07').replace('6,','06').replace('5,','05').replace('4,','04').replace('3,','03').replace('2,','02').replace('1,','01').replace('p26','26').replace('p25','25').replace('p24','24').replace('p23','23').replace('p22','22').replace('p21','p21').replace('p20','20').replace('p19','19').replace('p18','18').replace('p17','17').replace('p16','16').replace('p15','15').replace('p14','14').replace('p13','13').replace('p12','12').replace('p11','11').replace('p10','10').replace('p9','09').replace('p8','08').replace('p7','07').replace('p6','06').replace('p5','05').replace('p4','04').replace('p3','03').replace('p2','02').replace('p1','01')+']'
		        name= str(episode)+' '+str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And')
		        series = str(episode)+' '+str(series1)
		        regex=re.compile('(.+?)_V1.+?.jpg')
		        regex1=re.compile('(.+?).gif')
		        try:
		                match = regex.search(iconimage1)
		                iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
		        except:
		                pass
		        try:    
		                match= regex1.search(iconimage1)
		                iconimage= '%s.gif'%(match.group(1))
		        except:
		                pass
		        addDir(name,url,13,iconimage,fanart,series,description,'')                
        setView('movies', 'movie-view') 
            
                             
def TV_SEARCH(name,iconimage):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search EasyNews for a TV Show')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText() .replace(' ','+')  # sometimes you need to replace spaces with + or %20#
            if search_entered == None:
                return False   
        url= 'http://akas.imdb.com/search/title?title=%s&title_type=tv_series'% (search_entered)           
        link=OPEN_URL(url)
        LINK=link.split('class="loadlate"')
        match=[]
        
        for p in LINK:
            try:
                iconimage = re.compile('loadlate="(.+?)"').findall(p)[0]
                url = re.compile('href="(.+?)"').findall(p)[0]
                try:url=url.split('?')[0]
                except:pass
                name = re.compile('v_li_tt"\n>(.+?)<').findall(p)[0]
                description = re.compile('<p class="text-muted">\n(.+?)<').findall(p)[0]
                match.append([url,name, iconimage, description])                          
            except:pass  
        for url, name, iconimage, description in match:
            iconimage1 = iconimage
            url = 'http://akas.imdb.com'+str(url).replace("'",'')
            name= str(name).replace('-',' ').replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And')
            series = name
            regex=re.compile('(.+?)_V1.+?.jpg')
            match = regex.search(iconimage1)
            try:
                fanart= '%s_V1.jpg'%(match.group(1))
                iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
            except:
                pass
            addDir(name,url,10,iconimage,fanart,series,description,'')   
        setView('movies', 'movie-view')
                  
def TV_EASY_SEARCH(name,series,iconimage):
        search_entered = str(series).replace("The ",'').replace("the ",'').replace('.','').replace(' ','+') .replace(':','') .replace(',','').replace('[','').replace(']','')  
        dialog = xbmcgui.Dialog()
        if ADDON.getSetting('tvnoclick')=='false':
            if dialog.yesno("Search Options", "Choose your required quality?", "Custom: Use your custom settings", "Any: Returns any available quality", tvfileext, "Any"):
                    theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+tvlangex+'&sbj='+tvsubject+'&from='+tvposter+'&ns='+tvnewsgroup+'&fil='+tvfilename+'&fex=&vc='+tvvcodec+'&ac='+tvacodec+'&pby='+tvresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+tvfilesize+'&b2t='+tvmaxfilesize+tvreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+tvspam+tvrem+tvgrex+'&st=adv&safeO=0&sb=1'
            else:
                    theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+tvlangex+'&sbj='+tvsubject+'&from='+tvposter+'&ns='+tvnewsgroup+'&fil='+tvfilename+'&fex='+tvfileext+'&vc='+tvvcodec+'&ac='+tvacodec+'&pby='+tvresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+tvfilesize+'&b2t='+tvmaxfilesize+tvreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+tvspam+tvrem+tvgrex+'&st=adv&safeO=0&sb=1'
        else:
            theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_entered+'+%21+'+tvlangex+'&sbj='+tvsubject+'&from='+tvposter+'&ns='+tvnewsgroup+'&fil='+tvfilename+'&fex='+tvfileext+'&vc='+tvvcodec+'&ac='+tvacodec+'&pby='+tvresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+tvfilesize+'&b2t='+tvmaxfilesize+tvreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+tvspam+tvrem+tvgrex+'&st=adv&safeO=0&sb=1'
        if ADDON.getSetting('ssl') == 'true':
            theurl = str(theurl).replace('http:','https:')
            SSL='https://'
        else:
            theurl = str(theurl)
            SSL='http://'
        link,COOKIE=passman(theurl)     
        link = json.loads(link, encoding='utf8')
        results=link['results']
        if results <1:
            #print '========= TRYING AGAIN =========='
            theurl=theurl.replace('members.easynews.com/2.0/search/solr-search/advanced?','members.easynews.com/global4/search.html?').replace('https:','http') 
            link= passman(theurl) 
            #print theurl
            match=re.compile('url="http://(.+?)" length="(.+?)" type="application/octet-stream" />\n<link>http.+?com/dl/.+?/.+?/.+?/(.+?)</link>').findall(link)
            iconimage=str(iconimage)
            for url ,filesize, name in match:
	        match=url.split('80/')[1]
	        match=match.split('.')[0]
	        iconimage='http://th.easynews.com/thumbnails-%s%s%s/pr-%s.jpg'%(match[0],match[1],match[2],match[0:41])
                all=Fileextension(name)
                DOWNLOAD=str(name).replace('%20',' ').replace('%28','(').replace('%29',')').replace('.mkv','').replace('.avi','').replace('.iso','').replace('.mov','').replace('.mp4','').replace('.m4v','').replace('.vob','').replace('.flv','').replace('.wmv','').replace('%5B','').replace('%5C','').replace('%5A','')
                name = '[[B]%s %s[/B]]' % (filesize,all)+'  '+str(name).replace('%20',' ').replace('%28','(').replace('%29',')').replace('.mkv','').replace('.avi','').replace('.iso','').replace('.mov','').replace('.mp4','').replace('.m4v','').replace('.vob','').replace('.flv','').replace('.wmv','').replace('%5B','').replace('%5C','').replace('%5A','')
                url=SSL+str(url)+'|Cookie='+COOKIE
                downloadname=DOWNLOAD+'.'+str(all).lower()
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                addLink(name,url,iconimage,'',series,'',downloadname)
            theurl=theurl.replace('http://members.easynews.com/global4/search.html?','http://members.easynews.com/2.0/search/solr-search/advanced?') 
            addDir('[COLOR yellow][B]PLEASE SEARCH ARCHIVE INSTEAD[/B][/COLOR]',theurl,27,art+'searchtv.png','',series,'','')    
            #addDir('[COLOR red][B]<< Exit EasyNews[/B][/COLOR]','url',26,art+'back.png','','','','')    
            setView('movies', 'movie-view') 
        else:
            #print theurl
            data=link['data']
            #print data
            for field in data:
                num= field['0']
                size= field['4']
                codec=field['11']
                name=field['10']
                lang=field['alangs']
                lang='[COLOR yellow]%s[/COLOR]'%(lang)
                url=SSL+'members.easynews.com/dl/'+num+codec+'/'+name+codec+'|Authorization=Basic%20' + base64.b64encode('%s:%s' % (username, password))
                name = '[B][%s %s] %s[/B]' %(size,codec.replace('.','').upper(),lang)+' '+name
                name = name.replace('None','').replace("u'",'').replace("'",'')

                downloadname=name.split('[/B] ')[1]+codec
                iconimage='http://th.easynews.com/thumbnails-'+num[0]+num[1]+num[2]+'/pr-'+num+'.jpg'
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                addLink(name,url,iconimage,'',series,'',downloadname)
            addDir('[COLOR yellow][B]PLEASE SEARCH ARCHIVE INSTEAD[/B][/COLOR]',theurl,27,art+'searchtv.png','',series,'','')    
            addDir('[COLOR red][B]<< Exit EasyNews[/B][/COLOR]','url',26,art+'back.png','','','','')    
            setView('movies', 'movie-view')
        
def TV_EASY_SEARCH2(name,url,iconimage,series):
        theurl = str(url).replace('01','1').replace('02','2').replace('03','3').replace('04','4').replace('05','5').replace('06','6').replace('07','7').replace('08','8') .replace('09','9')
        if ADDON.getSetting('ssl') == 'true':
            theurl = str(theurl).replace('http:','https:')
            SSL='https://'
        else:
            theurl = str(theurl)
            SSL='http://'
        link ,COOKIE= passman(theurl)     
        link = json.loads(link, encoding='utf8')
        results=link['results']
        if results <1:
            #print '========= TRYING AGAIN =========='
            theurl= theurl.replace('members.easynews.com/2.0/search/solr-search/advanced?','members.easynews.com/global4/search.html?').replace('https:','http:')
            link= passman(theurl.replace('members.easynews.com/2.0/search/solr-search/advanced?','members.easynews.com/global4/search.html?')) 
            #print theurl
            match=re.compile('url="http://(.+?)" length="(.+?)" type="application/octet-stream" />\n<link>http.+?com/dl/.+?/.+?/.+?/(.+?)</link>').findall(str(link))
            iconimage=str(iconimage)
            for url ,filesize, name in match:
	        match=url.split('80/')[1]
	        match=match.split('.')[0]
	        iconimage='http://th.easynews.com/thumbnails-%s%s%s/pr-%s.jpg'%(match[0],match[1],match[2],match[0:41])
                all=Fileextension(name)
                DOWNLOAD=str(name).replace('%20',' ').replace('%28','(').replace('%29',')').replace('.mkv','').replace('.avi','').replace('.iso','').replace('.mov','').replace('.mp4','').replace('.m4v','').replace('.vob','').replace('.flv','').replace('.wmv','').replace('%5B','').replace('%5C','').replace('%5A','')
                
                name = '[[B]%s %s[/B]]' % (filesize,all)+'  '+str(name).replace('%20',' ').replace('%28','(').replace('%29',')').replace('.mkv','').replace('.avi','').replace('.iso','').replace('.mov','').replace('.mp4','').replace('.m4v','').replace('.vob','').replace('.flv','').replace('.wmv','').replace('%5B','').replace('%5C','').replace('%5A','')
                url = SSL+str(url).replace(' ','%20')+'|Cookie='+COOKIE
                downloadname=DOWNLOAD+'.'+str(all).lower()
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                addLink(name,url,iconimage,'',series,'',downloadname)
            setView('movies', 'movie-view') 
        else:
            #print theurl
            data=link['data']
            #print data
            for field in data:
                num= field['0']
                size= field['4']
                codec=field['11']
                name=field['10']
                lang=field['alangs']
                lang='[COLOR yellow]%s[/COLOR]'%(lang)
                url=SSL+'members.easynews.com/dl/'+num+codec+'/'+name+codec+'|Authorization=Basic%20' + base64.b64encode('%s:%s' % (username, password))
                name = '[B][%s %s] %s[/B]' %(size,codec.replace('.','').upper(),lang)+' '+name
                name = name.replace('None','').replace("u'",'').replace("'",'')

                downloadname=name.split('[/B] ')[1]+codec
                iconimage='http://th.easynews.com/thumbnails-'+num[0]+num[1]+num[2]+'/pr-'+num+'.jpg'
                xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                addLink(name,url,iconimage,'',series,'',downloadname)
            setView('movies', 'movie-view')
            
        
def IMDB_LISTS(url): 
        addDir('[B][COLOR white]Watch List[/COLOR][/B]',IMDBTV_WATCHLIST,40,art+'watchlist.jpg',FANART,'','','')
        if ADDON.getSetting('imdb_user') == 'ur********':
                xbmcgui.Dialog().ok('EasyNews Information','You Need To Input Your IMDb Number Into ','Addon Settings')
        if ADDON.getSetting('message') == 'false':
                xbmcgui.Dialog().ok('EasyNews Information','            For Full Support For This Plugin Please Visit','                    [COLOR yellow][B]WWW.XUNITYTALK.COM[/B][/COLOR]','Please Turn Off Message in Addon Settings')
        url=IMDB_LIST
    
        link=OPEN_URL(url)
        match = re.compile('<a class="list-name" href="(.+?)">(.+?)<').findall(link)
        for url, name in match:
            url='http://akas.imdb.com'+str(url)+'?start=1&view=grid&sort=listorian:asc&defaults=1'   
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,8,art+'list.jpg',FANART,'','','')    
        setView('files', 'menu-view')  


def WATCHLIST(url):   #new GW
        link=OPEN_URL(url)
        Regex = re.compile('class="ab_react">(.+?)</span>',re.DOTALL).findall(link)
        match=re.compile('"href":"(.+?)".+?title":"(.+?)".+?"plot":"(.+?)".+?"url":"(.+?)"',re.DOTALL).findall(str(Regex))
        for url,name,description,iconimage in match:
            if re.search('V1', iconimage, re.IGNORECASE):
                regex=re.compile('(.+?)_V1.+?.jpg')
                match = regex.search(iconimage)
                iconimage='%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                fanart=str(iconimage).replace('_.SX593_SY799_','')
            else:
                fanart='None'
            url = 'http://akas.imdb.com'+str(url)
            name=str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace(':','')
            series=str(name)
            addDir(name,url,24,iconimage,fanart,series,description,'')   
        setView('movies', 'movie-view') 
        
def WATCH_TV_LIST(url):
        link=OPEN_URL(url)
        link=str(link).replace('\n','').replace('src="http://i.media-imdb.com/images/SFaa265aa19162c9e4f3781fbae59f856d/nopicture/medium/film.png" ','')
        link=link.split('<div class="list grid">')[1]
        link=link.split('<div class="see-more">')[0]
        match=re.compile('''src="(.+?)".+?<a href="(.+?)">(.+?)</a>''').findall(link)
        for iconimage, url, name in match:
            if re.search('V1', iconimage, re.IGNORECASE):
                regex=re.compile('(.+?)_V1.+?.jpg')
                match = regex.search(iconimage)
                iconimage='%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                fanart=str(iconimage).replace('_.SX593_SY799_','')
            else:
                fanart='None'
            url = 'http://akas.imdb.com'+str(url)
            name=str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace(':','')
            series=str(name)
            description=''
            addDir(name,url,24,iconimage,fanart,series,description,'')   
        setView('files', 'menu-view') 
                        
def WATCH_LIST_SEARCH(name,url,iconimage,fanart,description):
        series = str(name)
        dialog = xbmcgui.Dialog()
        if dialog.yesno("Please Select Correct Type", "", "[B]    Please Select If Item Is A Movie Or Tv Series[/B]", '', "MOVIE", "TV"): 
                        TV_SEASON(url,iconimage,series,fanart)
        else:
                        EasySearch(name,iconimage, fanart)
                        
# def TRAKT_LISTS(url): 
        # addDir('Watch List','url',31,art+'trakt.png','','','','')
        # if ADDON.getSetting('trakt_user') == '':
                # xbmcgui.Dialog().ok('EasyNews Information','You Need To Input Your Trakt UserName Into ','Addon Settings')
        # if ADDON.getSetting('message') == 'false':
                # xbmcgui.Dialog().ok('EasyNews Information','            For Full Support For This Plugin Please Visit','                    [COLOR yellow][B]WWW.XUNITYTALK.COM[/B][/COLOR]','Please Turn Off Message in Addon Settings')
        # url='http://trakt.tv/user/%s/lists'% ADDON.getSetting('trakt_user')
        # link=OPEN_URL(url)
        # match = re.compile('<a href="(.+?)">(.+?)</a>\n\t\t\t\t\t\t\t</h3>').findall(link)
        # for url, name in match:
            # url='http://trakt.tv'+str(url)   
            # addDir(name,url,29,art+'trakt.png','','','','')    
        # setView('movies', 'default-view')  


# def TRAKT_WATCHLISTS_RESULTS(url): 
        # url = 'http://trakt.tv/user/%s/watchlist' % ADDON.getSetting('trakt_user')
        # link=OPEN_URL(url)
        # link1=str(link).replace('\n','').replace('\t','')
        # match = re.compile('<img alt="" src="(.+?)" /></a></div><div class="rating-pod"><div class="percent love"><span class="number">.+?</span><span class="percent-sign">.+?/span></div><div class="votes">.+?</div></div><h4><div class="title-overflow"></div><a class="title" href="(.+?)">(.+?)</a>').findall(link1)
        # for iconimage, url, name, in match:
            # series=str(name).replace('(','').replace(')','')    
            # url='http://trakt.tv'+str(url)   
            # addDir(name,url,30,iconimage,'',series,'','')    
            # setView('movies', 'default-view')
        # url = 'http://trakt.tv/user/%s/watchlist/movies/added' % ADDON.getSetting('trakt_user')
        # link=OPEN_URL(url)
        # link1=str(link).replace('\n','').replace('\t','')
        # match = re.compile('<img alt="" src="(.+?)" /></a></div><div class="rating-pod"><div class="percent love"><span class="number">.+?</span><span class="percent-sign">.+?/span></div><div class="votes">.+?</div></div><h4><div class="title-overflow"></div><a class="title" href="(.+?)">(.+?)</a>').findall(link1)
        # for iconimage, url, name, in match:
            # series=str(name).replace('(','').replace(')','')    
            # url='http://trakt.tv'+str(url)   
            # addDir(name,url,30,iconimage,'',series,'','')    
        # setView('movies', 'default-view')  
            
            
# def TRAKT_LISTS_RESULTS(url): 
        # link=OPEN_URL(url)
        # match = re.compile('<a href="(.+?)">\n\t\t\t\t\t\t\t\t\t\t\t\t<img class="poster-art" alt="(.+?)" src="(.+?)" />').findall(link)
        # for url, name, iconimage, in match:
            # series=str(name).replace('(','').replace(')','')    
            # url='http://trakt.tv'+str(url)   
            # addDir(name,url,30,iconimage,'',series,'','')    
        # setView('movies', 'default-view')  
            
# def TRAKTTV_SEASON(url,iconimage,series,fanart):
        # link=OPEN_URL(url)
        # match1 = re.compile('href="(.+?)" rel="external" class="button external">IMDb</a>').findall(link)
        # url1 = match1
        # link1=OPEN_URL(url1)
        # match = re.compile('.+?/rg/tt-episodes/season.+?/images/.+?season.+?     href="(.+?)"    >(.+?)</a>').findall(link1)
        # url2= str(url)
        # for url1, name in match:
            # url = str(url2)+str(url1)
            # name = 'Season '+str(name)
            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
            # addDir(name,url,11,iconimage,fanart,series,'','') 
        # setView('movies', 'seasons-view') 
 
# def TRAKT_LIST_SEARCH(name,url,iconimage,fanart,description):
        # series = str(name)
        # dialog = xbmcgui.Dialog()
        # if dialog.yesno("Please Select Correct Type", "", "[B]    Please Select If Item Is A Movie Or Tv Series[/B]", '', "MOVIE", "TV"): 
                                        # link=OPEN_URL(url)
                                        # match1 = re.compile('href="(.+?)" rel="external" class="button external">IMDb</a>').findall(link)
                                        # url2= match1[0]
                                        # for url1 in match1:
                                                # link1=OPEN_URL(url)
                                                # match = re.compile('.+?/rg/tt-episodes/season.+?/images/.+?season.+?     href="(.+?)"    >(.+?)</a>').findall(link1)
                                                # for url3, name in match:
                                                    # url = str(url2)+'/'+str(url3)
                                                    # name = 'Season '+str(name)
                                                    # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                                                    # addDir(name,url,11,iconimage,fanart,series,description,'') 
                                                # setView('movies', 'seasons-view') 
        # else:
                        # search_entered = str(name).replace("The ",'').replace("the ",'').replace('.','').replace(', ','+').replace(' ','+') .replace(':','').replace('[','').replace(']',' ').replace('(The)','').replace('(','') .replace(')','') .replace('-','+').replace("'",'') .replace("&",'').replace("!",'')     
                        # dialog = xbmcgui.Dialog()
                        # if dialog.yesno("Search Options", "Choose your required quality?", "Custom: Use your custom settings", "Any: Returns any available quality", mfileext, "Any"):
                                # theurl = 'http://members.easynews.com/global4/search.html?&gps='+search_entered+'+%21+'+mlangex+'&sbj='+msubject+'&from='+mposter+'&ns='+mnewsgroup+'&fil='+mfilename+'&fex=&vc='+mvcodec+'&ac='+macodec+'&pby='+mresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+mfilesize+'&b2t='+mmaxfilesize+mreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+mspam+mrem+mgrex+'&st=adv&safeO=0&sb=1'
                        # else:
                                # theurl = 'http://members.easynews.com/global4/search.html?&gps='+search_entered+'+%21+'+mlangex+'&sbj='+msubject+'&from='+mposter+'&ns='+mnewsgroup+'&fil='+mfilename+'&fex='+mfileext+'&vc='+mvcodec+'&ac='+macodec+'&pby='+mresults+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+mfilesize+'&b2t='+mmaxfilesize+mreso+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+mspam+mrem+mgrex+'&st=adv&safeO=0&sb=1'
                        # #print theurl
                        # link,COOKIE= passman(theurl)        
                        # match=re.compile('url="http://(.+?)" length="(.+?)" type="application/octet-stream" />\n<link>http.+?com/dl/.+?/.+?/.+?/(.+?)</link>').findall(link)
                        # fanart=str(fanart)
                        # iconimage=str(iconimage)
                        # for url ,filesize, name in match:
                            # all=Fileextension(name)
                            # name = '[[B]%s %s[/B]]' % (filesize,all)+'  '+str(name).replace('%20',' ').replace('%28','(').replace('%29',')').replace('.mkv','').replace('.avi','').replace('.iso','').replace('.mov','').replace('.mp4','').replace('.m4v','').replace('.vob','').replace('.flv','').replace('.wmv','').replace('%5B','').replace('%5C','').replace('%5A','')
                            # url = 'http://'+str(url)+'|Cookie'+COOKIE
                            # downloadname=str(search_entered).replace('+',' ')+'.'+str(all).lower()
                            # xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
                            # addLink(name,url,iconimage,fanart,series,description,downloadname) 
                        # addDir('[COLOR red][B]<< Exit EasyNews[/B][/COLOR]','url',26,art+'back.png','','','','')    
                        # setView('movies', 'easy-view') 
            
            
def ALLTIMEIMDB(url):
        link=OPEN_URL(url)
        LINK=link.split('class="loadlate"')
        match=[]
        
        for p in LINK:
            try:
                iconimage = re.compile('loadlate="(.+?)"').findall(p)[0]
                url = re.compile('href="(.+?)"').findall(p)[0]
                try:url=url.split('?')[0]
                except:pass
                title = re.compile('v_li_tt"\n>(.+?)<').findall(p)[0]
                year = re.compile('class="lister-item-year text-muted unbold">(.+?)</span>').findall(p)[0]
                if ') (' in year:
                    year = year.split(' ')[1]
                name = title + ' ' + year
                description = re.compile('<p class="text-muted">\n(.+?)<').findall(p)[0]
                match.append([iconimage, name,url, description])                          
            except:pass  
        nextp=re.compile('<a href="(.+?)\&ref_=adv_nxt"').findall(link)
        try:      
                nextp1=nextp[0]
        except:
                pass       
        for iconimage, name,url, description in match:
            name = str(name).replace('&#xB7;','').replace('&#x27;','').replace('&#x26;','And').replace('&#xE9;','e').replace('&amp;','And')
            iconimage1 = iconimage
            url = 'http://akas.imdb.com/title'+str(url)
            regex=re.compile('(.+?)_V1.+?.jpg')
            regex1=re.compile('(.+?).gif')
            try:
                    match = regex.search(iconimage1)
                    iconimage= '%s_V1_.SX593_SY799_.jpg'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
            try:    
                    match= regex1.search(iconimage1)
                    iconimage= '%s.gif'%(match.group(1))
                    fanart= '%s_V1.jpg'%(match.group(1))
            except:
                    pass
                    addDir(name,url,3,iconimage,fanart,'',description,'')   
                     
        try:
                url='http://akas.imdb.com/search/title'+str(nextp1)
                name= '[COLOR blue][B]Next Page >>[/B][/COLOR]'
                addDir(name,url,32,art+'next.png','','','','')
        except:
                pass
        #addDir('[COLOR red][B]<< Return To TV Menu[/B][/COLOR]','url',5,art+'back.png','','','','')    
        setView('movies', 'movie-view')
        
def IMDBGENRE(url): 
        link=OPEN_URL(url)
        match = re.compile('<a href="/genre/(.+?)">(.+?)</a>').findall(link)
        for url1, name, in match:
            url='http://akas.imdb.com/search/title?genres=%s&title_type=feature&sort=moviemeter,asc'% (url1) 
            iconimage=art+url1+'.png' 
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,32,art+'genre.jpg',FANART,'','','')     
        setView('files', 'menu-view')  
        
        
def EXIT_EASYNEWS():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
        
def DownloaderClass(url):
    
    downloadname=url.rsplit('/', 1)[1]
    url =url.split('|')[0]
    url =url.split('//')[1]
    url='http://'+username+':'+password+'@'+url
    if downloads == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("EasyNews", "You Need To Set Your Download Path", "A Window Will Now Open For You To Set")
        ADDON.openSettings()
   
    path = os.path.join(xbmc.translatePath(downloads))
    dest=os.path.join(path, downloadname)
    dp = xbmcgui.DialogProgress()
    dp.create("XUNITYTALK...Maintenance","Downloading & Copying File",downloadname)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
    
    
def DOWNLOADS(url):
     import glob
     path = os.path.join(xbmc.translatePath(ADDON.getSetting('download_path')), '')
     for infile in glob.glob(os.path.join(path, '*.*')):
         url=str(infile)
         name=str(infile).replace(path,'')
         if '.' in name:
             addLink1(name.split('.')[-2],url,ICON)
             xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE) 
     setView('movies', 'movies-view')  

        
def deletefile(url):
    file=str(url)
    os.remove(file)
    d = xbmcgui.Dialog()
    d.ok('EasyNews', 'Thank You File Deleted')         
         
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        #print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        #print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()
        
        
def track(group, name):
    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            t = threading.Thread(target = GA, args=(group, name))
            t.start()
            return func(*args, **kwargs)
        return decorator
    return factory
    
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

        
def addDir(name,url,mode,iconimage,fanart,series,description,downloadname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&series="+urllib.quote_plus(series)+"&description="+urllib.quote_plus(description)+"&downloadname="+urllib.quote_plus(downloadname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        menu = []
        if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.whatthefurk'):
            if mode==13:
                name_wtf=str(name)+'"'
                regex=re.compile('\[(.+?) (.+?)\] (.+?)"').findall(name_wtf)
                for season,episode,name in regex:
                    name1='%s%s - %s'%(season,episode,name)
                    season=str(season).replace('S0','').replace('S','')
                    episode=str(episode).replace('E0','').replace('E','')
                    series_regex_wtf=str(series)+'"'
                    match=re.compile('\[.+?\] (.+?)"').findall(series_regex_wtf)
                    series_wtf=match[0]
                    data='%s$%s$%s$%s' %(series_wtf,name,season,episode)
                    data=str(data)
                    menu.append(('@Search Episode WTF', 'XBMC.Container.Update(%s?mode=episode dialog menu&name=%s&imdb_id=None&data=%s)' %('plugin://plugin.video.whatthefurk/',name1,data)))
                    liz.addContextMenuItems(items=menu, replaceItems=True)
            if mode==3:
                menu.append(('@Search Movie WTF', 'XBMC.Container.Update(%s?data=%s&imdb_id=None&mode=movie dialog menu&name=%s)' %('plugin://plugin.video.whatthefurk/',name,name)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
            if mode==24:
                menu.append(('@Search Movie WTF', 'XBMC.Container.Update(%s?data=%s&imdb_id=None&mode=movie dialog menu&name=%s)' %('plugin://plugin.video.whatthefurk/',name,name)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
        if os.path.exists(xbmc.translatePath("special://home/addons/")+'plugin.video.1channel'):
            if mode==13:
                series_regex_1channel=str(series)+'"'
                match=re.compile('.+?\] (.+?)"').findall(series_regex_1channel)
                series_1channel=match[0]
                menu.append(('@Search Tv 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=tv&query=%s)' %('plugin://plugin.video.1channel/',series_1channel)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
            if mode==3:
                menu.append(('@Search Movie 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
            if mode==24:
                menu.append(('@Search Movie 1Channel', 'XBMC.Container.Update(%s?mode=7000&section=&query=%s)' %('plugin://plugin.video.1channel/',name)))
                liz.addContextMenuItems(items=menu, replaceItems=True)
        if (mode == 2000):
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        else:
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=True)
        return ok
                
def addLink(name,url,iconimage,fanart,series,description,downloadname):
        ok=True
    
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        menu = []
        if ADDON.getSetting('downloads') == 'true':
            menu.append(('Download', 'XBMC.RunPlugin(%s?mode=103&url=%s)'% (sys.argv[0], url)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        
        
def addLink1(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        menu = []
        if ADDON.getSetting('downloads') == 'true':
            menu.append(('Delete Download', 'XBMC.RunPlugin(%s?mode=101&url=%s)'% (sys.argv[0], url)))
        liz.addContextMenuItems(items=menu, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)        
        
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
series=None
description=None
downloadname=None



try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:
        series=urllib.unquote_plus(params["series"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass   
        
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass 
        
try:        
        downloadname=params["downloadname"]
except:
        pass                      

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "IconImage: "+str(iconimage)
#print "Series: "+str(series)
#print "Fanart: "+str(fanart)

def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':

        print addon.get_setting(viewType)
        if addon.get_setting(viewType) == 'Info':
            VT = '504'
        elif addon.get_setting(viewType) == 'Info2':
            VT = '503'
        elif addon.get_setting(viewType) == 'Info3':
            VT = '515'
        elif addon.get_setting(viewType) == 'Fanart':
            VT = '508'
        elif addon.get_setting(viewType) == 'Poster Wrap':
            VT = '501'
        elif addon.get_setting(viewType) == 'Big List':
            VT = '51'
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
        elif addon.get_setting(viewType) == 'List':
            VT = '50'
        elif addon.get_setting(viewType) == 'Default Menu View':
            VT = addon.get_setting('default-view1')
        elif addon.get_setting(viewType) == 'Default TV Shows View':
            VT = addon.get_setting('default-view2')
        elif addon.get_setting(viewType) == 'Default Episodes View':
            VT = addon.get_setting('default-view3')
        elif addon.get_setting(viewType) == 'Default Movies View':
            VT = addon.get_setting('default-view4')
        elif addon.get_setting(viewType) == 'Default Docs View':
            VT = addon.get_setting('default-view5')
        elif addon.get_setting(viewType) == 'Default Cartoons View':
            VT = addon.get_setting('default-view6')
        elif addon.get_setting(viewType) == 'Default Anime View':
            VT = addon.get_setting('default-view7')

        print viewType
        print VT
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )


if mode==None or url==None or len(url)<1:
        #print ""
        MOVIE_CATEGORIES()
       
elif mode==1:
        SEARCH(url)
        
elif mode==2:
        TMDB(url)      
elif mode==3:
        EasySearch(name,iconimage, fanart)   
        
elif mode==4:
        MOVIE_CATEGORIES()  
        
elif mode==5:
        TV_CATEGORIES()  
        
elif mode==6:
        IMDB_SEARCH(name,iconimage)   
                  
elif mode==8:
        #print ""+url
        WATCH_TV_LIST(url)  
        
elif mode==9:
        TV_POPULAR(url) 
        
elif mode==10:
        TV_SEASON(url,iconimage,series,fanart) 
        
elif mode==11:
        TV_EPISODE(url,iconimage, series, fanart)

elif mode==12:
        TV_SEARCH(url,iconimage)     
        
elif mode==13:
        #print ""+series
        TV_EASY_SEARCH(name,series,iconimage) 
        
elif mode==14:
        ONDVD(url)
        
elif mode==15:
        EasySearch_tryagain(url,iconimage, description)
        
elif mode==16:
        actorsearch()
elif mode==17:
        actresssearch()
        
elif mode==18:
        SEARCH_CATEGORIES()
               
elif mode==21:
        TOP_CATEGORIES()
               
elif mode==24:
        WATCH_LIST_SEARCH(name,url,iconimage,fanart,description)
        
elif mode==25:
        IMDB_LISTS(url)
        
elif mode==26:
        EXIT_EASYNEWS()
        
elif mode==27:
        TV_EASY_SEARCH2(name,url,iconimage,series) 
        
elif mode==28:
        TRAKT_LISTS(url) 
        
elif mode==29:
        TRAKT_LISTS_RESULTS(url) 
        
elif mode==30:
        TRAKT_LIST_SEARCH(name,url,iconimage,fanart,description) 
        
elif mode==31:
        TRAKT_WATCHLISTS_RESULTS(url) 
        
elif mode==32:
        ALLTIMEIMDB(url) 

elif mode==33:
        IMDBGENRE(url) 

elif mode==40:
        #print ""+url
        WATCHLIST(url) 
        
elif mode==101:
        #print ""+url
        deletefile(url)  
               
elif mode==102:
        DOWNLOADS(url)
elif mode==103:
        DownloaderClass(url)      
elif mode==2000:
        pop()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
