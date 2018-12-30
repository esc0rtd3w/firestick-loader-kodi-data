'''
    Istream
    tvrage by Coolwave
    Copyright (C) 2013 

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.xgoogle.search import GoogleSearch

import re

class tvrage(TVShowIndexer):
    implements = [TVShowIndexer]

    import xbmcaddon
    import os
    addon_id = 'script.icechannel.extn.common'
    addon = xbmcaddon.Addon(addon_id)
    #img = os.path.join( addon.getAddonInfo('path'), 'resources', 'images', 'tvrage.png' )
    	
    #unique name of the source
    name = "tvrage"
    default_indexer_enabled = 'false'
    #source_enabled_by_default = 'false'
    #display name of the source
    display_name = "[COLOR white]TV[/COLOR][COLOR red]Rage[/COLOR]"
    
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/1120740c0028d16de328516e4f0c889aa949b65e/tvrage.png'
    
    #base url of the source website
    base_url_api = 'http://services.tvrage.com/myfeeds/'
    base_url_tv = 'http://www.tvrage.com/'
    api = 'ag6txjP0RH4m0c8sZk2j'
    base_url_watchseries = 'http://www.watchseries.to/'
    base_url_tvseeker = 'http://www.nzbtvseeker.com/'
    base_url_tvrage_48hours = 'http://services.tvrage.com/feeds/last_updates.php?hours=48'
    base_url_tv_com = 'http://www.tv.com/'
    primewire_url = 'http://www.primewire.ag/'
    tv_calender_url = 'http://today.at-my.tv/'
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        if section == 'latest':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = 'http://thewatchseries.to/latest/'+page
                
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            import re
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            total_pages = '9'
            
            self.AddInfo(list, indexer, 'latest', '', type, str(page), total_pages)
            
            match=re.compile('<li><a href="(.+?)">(.+?) Seas. (.+?) Ep. (.+?) .+?<').findall(html)
            for url, name, Sea_num, eps_num in match:
                
                name = self.CleanTextForSearch(name)
                url = self.tv_calender_url
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name +'[COLOR royalblue] ('+sea_eps+')[/COLOR]', item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)

        elif section == 'popular':
            
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = 'http://thewatchseries.to/new/'+page
                
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            import re
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            total_pages = '9'
            
            self.AddInfo(list, indexer, 'popular', '', type, str(page), total_pages)
            
            match=re.compile('<li><a href="(.+?)">(.+?) Seas. (.+?) Ep. (.+?) .+?<').findall(html)
            for url, name, Sea_num, eps_num in match:
                
                name = self.CleanTextForSearch(name)
                url = self.tv_calender_url
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name +'[COLOR royalblue] ('+sea_eps+')[/COLOR]', item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)

        
        elif section == 'web':
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = self.base_url_tv_com + section + '/page'+page+'/'
            #http://www.tv.com/web/page2/
                
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            import re
            url = urllib.unquote_plus(url)
            
            new_url = self.base_url_tv_com + section+'/'
            
            html = net.http_GET(new_url+'page'+str(page)+'/').content

            if total_pages == '':
                #lastlist = url
                r= '>([0-9]*)</a>\s*<a href=".+?" class="next">' #% lastlist
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'web', url, type, str(page), total_pages)
            
            match=re.compile('<div class="mask"><a href=".+?"><img src=".+?" alt="(.+?)"/></a></div>.+?<div class="_clear"></div>\s*<div class="airtime">(.+?)</div>',re.DOTALL).findall(html)
            for name, netw in match:
                name = self.CleanTextForSearch(name)
                url = 'http://services.tvrage.com/myfeeds/search.php?key=ag6txjP0RH4m0c8sZk2j&show='+name
                netw = netw.split('<')[0]
                netw = '[COLOR red]'+netw+'[/COLOR]'
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + netw.replace('(','').replace(')','') +')', '', 'tv_seasons', url=url, name=name)

        elif section == 'decade_title':
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + '/page'+page+'/'
            
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            import re
            url = urllib.unquote_plus(url)
            new_url = url.rpartition('/')[0]
            new_url = new_url+'/'
            html = net.http_GET(new_url+'page'+str(page)+'/').content

            if total_pages == '':
                #lastlist = url
                r= '>([0-9]*)</a>\s*<a href=".+?" class="next">' #% lastlist
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'decade_title', url, type, str(page), total_pages)
            
            match=re.compile('<div class="mask"><a href=".+?"><img src=".+?" alt="(.+?)"/></a></div>.+?<div class="_clear"></div>\s*<div class="airtime">(.+?)</div>',re.DOTALL).findall(html)
            for name, netw in match:
                name = self.CleanTextForSearch(name)
                url = 'http://services.tvrage.com/myfeeds/search.php?key=ag6txjP0RH4m0c8sZk2j&show='+name
                netw = netw.split('<')[0]
                netw = '[COLOR red]'+netw+'[/COLOR]'
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + netw.replace('(','').replace(')','') +')', '', 'tv_seasons', url=url, name=name)

        elif section == 'network_title':
            import re
            #url = url.replace(' ','+')
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + '/page'+page+'/'
            
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            new_url = url.rpartition('/')[0]
            new_url = new_url+'/'
            html = net.http_GET(new_url+'page'+str(page)+'/').content

            if total_pages == '':
                #lastlist = url
                r= '>([0-9]*)</a>\s*<a href=".+?" class="next">' #% lastlist
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'network_title', url, type, str(page), total_pages)
            
            match=re.compile('<div class="mask"><a href=".+?"><img src=".+?" alt="(.+?)"/></a></div>.+?<div class="_clear"></div>\s*<div class="airtime">(.+?)</div>',re.DOTALL).findall(html)
            for name, netw in match:
                name = self.CleanTextForSearch(name)
                url = 'http://services.tvrage.com/myfeeds/search.php?key=ag6txjP0RH4m0c8sZk2j&show='+name
                netw = netw.split('<')[0]
                netw = '[COLOR red]'+netw+'[/COLOR]'
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + netw.replace('(','').replace(')','') +')', '', 'tv_seasons', url=url, name=name)
                  
        elif section == 'genres_title':
            import re
            #url = url.replace(' ','+')
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + '/page'+page+'/'
            
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            new_url = url.rpartition('/')[0]
            new_url = new_url+'/'
            html = net.http_GET(new_url+'page'+str(page)+'/').content

            if total_pages == '':
                #lastlist = url
                r= '>([0-9]*)</a>\s*<a href=".+?" class="next">' #% lastlist
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'genres_title', url, type, str(page), total_pages)
            
            match=re.compile('<div class="mask"><a href=".+?"><img src=".+?" alt="(.+?)"/></a></div>.+?<div class="_clear"></div>\s*<div class="airtime">(.+?)</div>',re.DOTALL).findall(html)
            for name, netw in match:
                name = self.CleanTextForSearch(name)
                url = 'http://services.tvrage.com/myfeeds/search.php?key=ag6txjP0RH4m0c8sZk2j&show='+name
                netw = netw.split('<')[0]
                netw = '[COLOR red]'+netw+'[/COLOR]'
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + netw.replace('(','').replace(')','') +')', '', 'tv_seasons', url=url, name=name)

        elif section == 'news':
            import re
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + '/page'+page+'/'#new_url = new_url + '?p=' + page
            
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            new_url = url.rpartition('/')[0]
            new_url = new_url+'/'
            html = net.http_GET(new_url+'page'+str(page)+'/').content

            if total_pages == '':
                #lastlist = url
                r= '>([0-9]*)</a>\s*<a href=".+?" class="next">' #<a href='?p=.+?'>([0-9]*)</a>  | <a href='?p=.+?'>Next page
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'news', url, type, str(page), total_pages)
            
            
            match=re.compile('<h3 class="title"><a href="(.+?)">(.+?)</a></h3>\s*<p class="body">(.+?)</p>').findall(html)
            for url, title_name, title_name2 in match:#<h3><a href="(.+?)">(.+?)</a></h3>
                url = 'http://www.tv.com'+url#http://www.tvrage.com+url
                #title_name = '[COLOR royalblue]'+title_name+'[/COLOR]'
                title_name = title_name+ ' ' +title_name2
                title_name = title_name.replace('<i>','')
                name = title_name.replace('</i>','')
            
            
                self.AddContent(list, indexer, 'news', name, '', 'news', url=url, name=name)

        elif section == 'listings':
            import re
            #url = url.replace(' ','+')
            new_url = url
                        
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            
            
            r= '<td colspan="3" class="pop"><div align="center"><a href=".+?"><img src=".+?" border="0"></a>&nbsp;&nbsp;<a href="(.+?)">'
            next_pages = re.compile(r).findall(html)[0]
            url = 'http://www.thefutoncritic.com' + next_pages
            #next_pages = next_pages.replace('/listings/','')
            #next_pages = next_pages[:-1]
            #next_pages = next_pages.replace('/','-')
            #self.AddSection(list, indexer,'listings','[COLOR royalblue]<<--'+next_pages+'[/COLOR]',url,indexer)#(list, indexer, 'listings', url, type, '', total_pages)
            
            r2= '<td colspan="3" class="pop"><div align="center"><a href=".+?"><img src=".+?" border="0"></a>&nbsp;&nbsp;<a href=".+?"><img src="/.+?" border="0"></a>&nbsp;&nbsp;.+?&nbsp;&nbsp;<a href="(.+?)"'
            r3= 'border="0"></a>&nbsp;&nbsp;\[.+?, (.+?)\]&'
            todays_date = re.compile(r3).findall(html)[0]
            next_pages2 = re.compile(r2,re.DOTALL).findall(html)[0]
            url = 'http://www.thefutoncritic.com' + next_pages2
            next_pages2 = next_pages2.replace('/listings/','')
            next_pages2 = next_pages2[:-1]
            next_pages2 = next_pages2.replace('/','-')
            todays_date = todays_date.title()
            self.AddSection(list, indexer,'listings','[COLOR white]Today Date: '+'[COLOR red]'+todays_date+' [/COLOR]'+'[COLOR white]Click to go to:[/COLOR] '+'[COLOR royalblue]'+next_pages2+'-->>[/COLOR]',url,indexer)#(list, indexer, 'listings', url, type, '', total_pages)               
            
            match=re.compile('<td width="15%">(.+?)</td>\s*<td width="15%">(.+?)</td>\s*<td width="70%"><a href="(.+?)">(.+?)</a').findall(html)
            date_idem = re.search(r'border="0"></a>&nbsp;&nbsp;[.+?, (.+?)]', html)# february 25, 2014
            for time, netw, url, name in match:
                name = name.split(':')[0]
                name = self.CleanTextForSearch(name)
                url = 'http://www.thefutoncritic.com' + url
                name = re.sub('(.+?), the', 'the \g<1>', name)
                name = name.title()
                name = name.replace('Nhl Special','NHL').replace('$','').replace('Abc Special','ABC Special').replace('Nba Special','NBA').replace('Wwe Main Event','WWE Main Event').replace('Pbs Special','PBS Special').replace('Wwe Raw','WWE Raw').replace('Bet Special','BET Special').replace('Hbo Special','HBO Special').replace('Nbc Sports Special','NBC Sports Special').replace('#','')
                time=time.replace('&nbsp;','')
                netw = '[COLOR red]'+netw+'[/COLOR]'
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + netw + ')'+' '+'[COLOR royalblue]'+time+'[/COLOR]', '', 'tv_seasons', url=url, name=name)

            r= '<td colspan="3" class="pop"><div align="center"><a href=".+?"><img src=".+?" border="0"></a>&nbsp;&nbsp;<a href="(.+?)">'
            next_pages = re.compile(r).findall(html)[0]
            url = 'http://www.thefutoncritic.com' + next_pages
            next_pages = next_pages.replace('/listings/','')
            next_pages = next_pages[:-1]
            next_pages = next_pages.replace('/','-')
            self.AddSection(list, indexer,'listings','[COLOR royalblue]<<--[/COLOR]'+'[COLOR white]Click to go to: [/COLOR]'+'[COLOR royalblue]'+next_pages+'[/COLOR]',url,indexer)
            #self.AddSection(list, indexer,'listings','[COLOR royalblue]<<--'+next_pages+'[/COLOR]',url,indexer)
            

        elif section == 'primewire':
            import re
            import urllib
            url = urllib.unquote_plus(url)
            
            import re
            new_url = url
                    
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + '&page=' + page

            if sort_by == '' and 'sort' not in new_url:
                sort_by = 'date'            
            if 'sort' not in new_url:
                new_url = new_url + '&sort=' + sort_by 

            from entertainment.net import Net
            net = Net(cached=False)
            new_url_for_cache = re.sub('\?key=.+?&', '?', new_url)
            content = net.http_GET(new_url, url_for_cache=new_url_for_cache).content

            if total_pages == '' :
                total_pages = re.search('page=([0-9]*)"> >> <', content)
                if total_pages:
                    total_pages = total_pages.group(1)
                else:
                    if re.search('0 items found', content):
                        page = '0'
                        total_pages = '0'
                    else:
                        page = '1'
                        total_pages = '1'
            
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)

            mode = common.mode_File_Hosts
            if type == 'tv_shows':
                mode = common.mode_Content
                type = 'tv_seasons'
            
            for item in re.finditer(r"<div class=\"index_item.+?\"><a href=\"/(.+?)\" title=\"Watch (.+?)\"", content):
                item_v_id = item.group(1)            
                item_title = common.addon.unescape(item.group(2))
                item_year = re.search("\(([0-9]+)\)", item_title)
                if item_year:
                    item_year = item_year.group(1)
                else:
                    item_year = ''
                item_name = re.sub(" \([0-9]+\)", "", item_title )
            
                item_url = self.primewire_url + item_v_id
            
                if total_pages == '':
                    total_pages = '1'
                
                self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year)

        elif section == 'abc':
            import re
            new_url = url
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
                new_url = new_url + '/page'+page+'/'
            
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            new_url = url.rpartition('/')[0]
            new_url = new_url+'/'
            
            html = net.http_GET(new_url+'page'+str(page)+'/').content

            if total_pages == '':
                r= '>([0-9]*)</a>\s*<a href=".+?" class="next">'
                total_pages = re.compile(r).findall(html)[0]
            self.AddInfo(list, indexer, 'abc', url, type, str(page), total_pages)
            
            match=re.compile('<li class="show">\s*<a href="(.+?)">(.+?)</a>').findall(html)
            for url, name in match:
                name = self.CleanTextForSearch(name)  
                self.AddContent(list, indexer, common.mode_Content, name, '', 'tv_seasons', url=url, name=name)

        elif section == 'tvguide_day':
            import re
            new_url = url
                        
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            
            r2= '<td colspan="7" class="month_name"><div class="prev-month  "><a href=".+?">&lt;&lt; <strong>.+?</strong></a></div><h3>.+?</h3><div class="next-month  "><a href="(.+?)"><strong>.+?</strong>'
            r3= '<td colspan="7" class="month_name"><div class="prev-month  "><a href=".+?">&lt;&lt; <strong>.+?</strong></a></div><h3>(.+?)</h3><div class="next-month'
            todays_date = re.compile(r3).findall(html)[0]
            next_pages2 = re.compile(r2,re.DOTALL).findall(html)[0]
            url = next_pages2
            next_pages2 = next_pages2.replace('http://','').replace('.at-my.tv','')
            next_pages2 = next_pages2.replace('.','-')
            self.AddSection(list, indexer,'tvguide_day','[COLOR white]Today Date: '+'[COLOR red]'+todays_date+' [/COLOR]'+'[COLOR white]Click to go to:[/COLOR] '+'[COLOR royalblue]'+next_pages2+'-->>[/COLOR]',url,indexer)#(list, indexer, 'listings', url, type, '', total_pages)               
            
            match=re.compile('class="openlink">\+ (.+?)</a> </th>.+?<strong>Season  (.+?), Episode (.+?) - "(.+?)"</strong>.+?<strong>Network:</strong> (.+?) .+?<strong>Status:</strong> (.+?) .+?<strong>Rating:</strong> (.+?) ',re.DOTALL).findall(html)
            for name, Sea_num, eps_num, title, netw, info, rate in match:
                name = self.CleanTextForSearch(name)
                url = self.tv_calender_url
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                netw = netw.upper()
                info = info.lower()
                netw = '[COLOR red]'+netw+': '+info+'[/COLOR]'
                
                #self.AddContent(list, indexer, common.mode_File_Hosts, name+ ' (' + netw + ')'+' '+'[COLOR royalblue] '+sea_eps+'[/COLOR] '+'Rating: '+rate, type, url=url, name=name, season=season_pull, episode=episode_pull)

                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name+ ' (' + netw + ')'+' '+'[COLOR royalblue] '+sea_eps+'[/COLOR] '+'Rating: '+rate, 
                    item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)



            r= '<td colspan="7" class="month_name"><div class="prev-month  "><a href="(.+?)">&lt;&lt; <strong>.+?</strong></a></div><h3>.+?</h3><div class="next-month  "><a href=".+?"><strong>.+?</strong>'
            next_pages = re.compile(r).findall(html)[0]
            url = next_pages
            next_pages = next_pages.replace('http://','').replace('.at-my.tv','')
            next_pages = next_pages.replace('.','-')                        
            self.AddSection(list, indexer,'tvguide_day','[COLOR royalblue]<<--[/COLOR]'+'[COLOR white]Click to go to: [/COLOR]'+'[COLOR royalblue]'+next_pages+'[/COLOR]',url,indexer)
            
        elif section == 'tvguide_week':
            import re
            new_url = url
                        
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            
                        
            r3= '</div><h3>(.+?)</h3>'
            todays_date = re.compile(r3).findall(html)[0]

            self.AddSection(list, indexer,'tvguide_week','[COLOR red].:'+todays_date+':. [/COLOR]','',indexer)#(list, indexer, 'listings', url, type, '', total_pages)               
            
            match=re.compile('class="openlink">\+ (.+?)</a> </th>.+?<td class="airdate">(.+?)</td>.+?<strong>Season  (.+?), Episode (.+?) - "(.+?)"</strong>.+?<strong>Network:</strong> (.+?) .+?<strong>Status:</strong> (.+?) .+?<strong>Rating:</strong> (.+?) ',re.DOTALL).findall(html)
            for name, airdate, Sea_num, eps_num, title, netw, info, rate in match:
                name = self.CleanTextForSearch(name)
                url = self.tv_calender_url
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                netw = netw.upper()
                info = info.lower()
                netw = '[COLOR red]'+netw+': '+info+'[/COLOR]'
                
                #self.AddContent(list, indexer, common.mode_Content, name+ ' (' + netw + ')'+' '+'[COLOR royalblue] '+sea_eps+'[/COLOR] '+'Airdate: '+airdate, '', 'tv_seasons', url=url, name=name)
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name+ ' (' + netw + ')'+' '+'[COLOR royalblue] '+sea_eps+'[/COLOR] '+'Airdate: '+airdate, 
                    item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)


        else:
            #section == 'tvguide_month':
            new_url = url
            import re
            from entertainment.net import Net
            net = Net(cached=False)
            import urllib
            url = urllib.unquote_plus(url)
            html = net.http_GET(new_url).content
            
                        
            r3= '</a></div><h3>.+?; (.+?)</h3>'
            todays_month = re.compile(r3).findall(html)[0]
            self.AddSection(list, indexer,'tvguide_week','[COLOR red].:'+todays_month+':. [/COLOR]','',indexer)          
            
            match=re.compile('href="http://(.+?).at-my.tv/#r_.+?" class="eplink ">(.+?)</a><span class="seasep"></span><br /><span class="seasep" >S: (.+?) - Ep: (.+?)</span>').findall(html)

            for url, name, Sea_num, eps_num in match:
                name = self.CleanTextForSearch(name)
                airdate = url.replace('.','-')
                airdate = '[COLOR red]'+airdate+'[/COLOR]'
                season_pull = "0%s"%Sea_num if len(Sea_num)<2 else Sea_num
                episode_pull = "0%s"%eps_num if len(eps_num)<2 else eps_num
                sea_eps = 'S'+season_pull+'E'+episode_pull
                                
                #self.AddContent(list, indexer, common.mode_Content, name+' ('+'[COLOR royalblue]'+sea_eps+'[/COLOR]) '+'Airdate: ('+airdate+')', '', 'tv_seasons', url=url, name=name)
                year= '0'

                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + Sea_num + '_episode_' + eps_num)

                self.AddContent(list, indexer, common.mode_File_Hosts, name+' ('+'[COLOR royalblue]'+sea_eps+'[/COLOR]) '+'Airdate: ('+airdate+')', 
                    item_id, 'tv_episodes', url=url, name=name, year=year, season=Sea_num, episode=eps_num)
              
       
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        from entertainment.net import Net
        net = Net(cached=False)
        import re
        
        show_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid('tvrage.com', name, 'shows', item_count=2, title_extrctr=['(.+?) tv show', '(.+?) \- tvrage'], exact_match=True)
        if show_url == '' :
            tv_url= 'http://www.tvrage.com/search.php?search=%s&searchin=2&button=Go' %(name.lower().replace(' ','+'))
            html = net.http_GET(tv_url).content
            r = re.search(r'<h2><a href="(.+?)">(.+?)</a> <img src=\'.+?\' /> </h2>\s*</dt>\s*<dd class="img"> <a href="/(.+?)">', html)
            show_url = 'http://www.tvrage.com' + r.group(1)
        
        item_url = show_url + '/episode_list'
        
        #year = year
        
        #tv_url= 'http://www.tvrage.com/search.php?search=%s+%s&searchin=2&button=Go' %(name.lower().replace(' ','+'),year)
        #<h2><a href="/Breaking_Bad">Breaking Bad</a>
        #http://www.tvrage.com
        #html = net.http_GET(tv_url).content

        #r = re.search(r'<h2><a href="(.+?)">(.+?)</a> <img src=\'.+?\' /> </h2>\s*</dt>\s*<dd class="img"> <a href="/(.+?)">', html)
        #item_url = 'http://www.tvrage.com' + r.group(1) + '/episode_list'
        #item_name = r.group(2)
        #item_id = r.group(3)
            
        import datetime
        todays_date = datetime.date.today()
        content = net.http_GET(item_url).content
        
        if type == 'tv_seasons':
            match=re.compile('>S-(.+?)<').findall(content)
            for seasonnumber in match:                
                item_url = item_url
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)               
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, season=seasonnumber)

        elif type == 'tv_episodes':
            new_url = url+'/'+season
            content2 = net.http_GET(new_url).content
            match=re.compile("<td width='40' align='center'><a href='(.+?)' title='.+?'>.+?x(.+?)</i></a></td>\s*<td width='80' align='center'>(.+?)</td>\s*<td style='padding-left: 6px;'> <a href='.+?/([0-9]*)'>(.+?)</a> </td>",re.DOTALL).findall(content2)
            for item_url, item_v_id_2, item_date, fixscrape, item_title in match:
                item_v_id_2 = str(int(item_v_id_2))
                
                item_fmtd_air_date = self.get_formated_date( item_date )
                if item_fmtd_air_date.date() > todays_date: break
                
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
            
            
            
    def get_formated_date(self, date_str):
        
        import re
        import datetime

        if '00' in date_str:
            date_str = '01/Aug/2000'
        #date_str = date_str.replace('00/([0-9]{2})/([0-9]{4})','01/Aug/2000')
        date_str = date_str.replace('00/00/0000','01/Aug/2000')
        #date_str = re.sub(pattern, replace, date_str)
        
                
        item_air_date = common.unescape(date_str).replace('      ', '')
        item_fmtd_air_date = ""
        if 'Jan' in item_air_date: item_fmtd_air_date = '01-'
        elif 'Feb' in item_air_date: item_fmtd_air_date = '02-'
        elif 'Mar' in item_air_date: item_fmtd_air_date = '03-'
        elif 'Apr' in item_air_date: item_fmtd_air_date = '04-'
        elif 'May' in item_air_date: item_fmtd_air_date = '05-'
        elif 'Jun' in item_air_date: item_fmtd_air_date = '06-'
        elif 'Jul' in item_air_date: item_fmtd_air_date = '07-'
        elif 'Aug' in item_air_date: item_fmtd_air_date = '08-'
        elif 'Sep' in item_air_date: item_fmtd_air_date = '09-'
        elif 'Oct' in item_air_date: item_fmtd_air_date = '10-'
        elif 'Nov' in item_air_date: item_fmtd_air_date = '11-'
        elif 'Dec' in item_air_date: item_fmtd_air_date = '12-'
        else: item_fmtd_air_date = '12-'
        date = re.search('([0-9]{1,2})', item_air_date)
        if date: 
            date = date.group(1)
            item_fmtd_air_date += "%02d-" % int(date)
        else:
            item_fmtd_air_date += "01-"
        year = re.search('([0-9]{4})', item_air_date)
        if year: 
            year = year.group(1)
            item_fmtd_air_date += year
        else:
            item_fmtd_air_date += "0001"
            
        try:
            item_fmtd_air_date = datetime.datetime.strptime(item_fmtd_air_date, "%m-%d-%Y")
        except TypeError:
            import time
            item_fmtd_air_date = datetime.datetime(*(time.strptime(item_fmtd_air_date, "%m-%d-%Y")[0:6]))
            
        return item_fmtd_air_date
            
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net(cached=False)
        url_type = ''
        content_type = ''

        
        if section == 'main':
            self.AddSection(list, indexer,'latest','Date Added','http://thewatchseries.to/latest',indexer)
            self.AddSection(list, indexer,'popular','Popular Episodes Added This Week','http://thewatchseries.to/new',indexer)
            self.AddSection(list, indexer,'network','By Network',self.base_url_tv_com+'shows/',indexer)
            self.AddSection(list, indexer,'decade','By Decade',self.base_url_tv_com+'shows/',indexer)
            self.AddSection(list, indexer,'web','Web Series',self.base_url_tv_com+'web/',indexer)
            self.AddSection(list, indexer,'genres','Genres',self.base_url_tv_com+'shows/',indexer)
            self.AddSection(list, indexer,'nextaird','Next Aired [COLOR red](New)[/COLOR]',self.tv_calender_url,indexer)
            self.AddSection(list, indexer,'listings','TV Show Schedule','http://www.thefutoncritic.com/listings/',indexer)
            #self.AddSection(list, indexer,'tvguide_day','TV Guide [At-my.tv]',self.tv_calender_url,indexer)
            #self.AddSection(list, indexer,'tvguide','TV Guide [beta2]',self.tv_calender_url,indexer)
            self.AddSection(list, indexer,'az','A-Z',self.base_url_tv_com+'shows/sort/a_z/',indexer)
            self.AddSection(list, indexer,'news','Featured News',self.base_url_tv_com+'news/',indexer)
            
        elif section == 'nextaird':
            import xbmc,os,xbmcplugin,sys
                        
            if os.path.exists(xbmc.translatePath("special://home/addons/") + 'script.tv.show.next.aired'):
                xbmc.executebuiltin('RunScript(script.tv.show.next.aired)')
                xbmcplugin.endOfDirectory(int(sys.argv[1]), False, False)
            else:
                self.AddSection(list, indexer,'main','Please install "TV Show - Next Aired" script in xbmc.org repo.',self.tv_calender_url,indexer)
                    
        elif section == 'tvguide':
            self.AddSection(list, indexer,'tvguide_week','Episodes Aired next Week','http://next.seven.days.at-my.tv/',indexer)
            #self.AddSection(list, indexer,'latest','Episode Aired last Week',self.tv_calender_url,indexer)
            self.AddSection(list, indexer,'tvguide_month','Episode Aired this Month','http://at-my.tv/',indexer)
            self.AddSection(list, indexer,'tvguide_day','Episode Aired by Day',self.tv_calender_url,indexer)

        elif section == 'mostwatched':
            self.AddSection(list, indexer,'Downloads','Most Watched Last Week',self.base_url_tvseeker+'Downloads/',indexer)
            self.AddSection(list, indexer,'Downloads/Month','Most Watched Last Month',self.base_url_tvseeker+'Downloads/Month/',indexer)
            self.AddSection(list, indexer,'Downloads/Year','Most Watched Last Year',self.base_url_tvseeker+'Downloads/Year/',indexer)
            self.AddSection(list, indexer,'Watched','Most Watched of all Time',self.base_url_tvseeker+'Watched/',indexer)           

        elif section == 'decade':
            r = re.findall(r'<a   href="/shows/decade/.+?/">(.+?)</a>', net.http_GET(url).content, re.I)
            for genres in r[0:]:

                self.AddSection(list, indexer, 'decade_title', genres, self.base_url_tv_com+'shows/decade/'+genres+'/', indexer)
        
        elif section == 'network':
            r = re.findall(r'<a   href="/shows/network/(.+?)/">.+?</a>', net.http_GET(url).content, re.I)
            for network in r[0:]:

                network_title = network.replace('-',' ')
                network_title = network_title.replace('and','&')
                network_title = network_title.upper()
                self.AddSection(list, indexer, 'network_title', network_title, self.base_url_tv_com+'shows/network/'+network+'/', indexer)

        elif section == 'genres':
            r = re.findall(r'<a   href="/shows/category/(.+?)/">.+?</a>', net.http_GET(url).content, re.I)
            for genres in r[0:]:
                genres_title = genres.replace('-',' ')
                genres_title = genres_title.replace('and','&')
                genres_title = genres_title.upper()
                self.AddSection(list, indexer, 'genres_title', genres_title, self.base_url_tv_com+'shows/category/'+genres+'/', indexer)

        elif section == 'az':
            r = re.findall(r'<a href="/shows/sort/.+?/">(.+?)</a></li>\s*<li >', net.http_GET(url).content, re.I)
            for abc in r[0:]:
                abc_title = abc.upper()
                abc_title = abc_title.replace('ALL','0-9')
                self.AddSection(list, indexer, 'abc', abc_title, self.base_url_tv_com+'shows/sort/'+abc.replace('All','a_z')+'/', indexer)
            
            
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            

    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        import elementtree.ElementTree as ET
        import urllib
        from entertainment.net import Net
        net = Net(cached=False)
                        
        keywords = self.CleanTextForSearch(keywords) 
        
        import re             
        from entertainment import odict
        search_dict = odict.odict({'search_keywords':keywords})
        name = urllib.urlencode(search_dict)
        id_search = 'http://services.tvrage.com/myfeeds/search.php?key=ag6txjP0RH4m0c8sZk2j&show='+name
        content = net.http_GET(id_search).content
        
        try:
            root = ET.fromstring(content)
        except:
            content = common.CleanText2(content, True, True)
            root = ET.fromstring(content)
            
        shows = root.findall('.//show')
        for show in shows:
            show_id = show.find('showid').text            
            show_url = 'http://services.tvrage.com/myfeeds/episode_list.php?key=ag6txjP0RH4m0c8sZk2j&sid='+str(show_id)            
            show_name = show.find('name').text
            show_year = show.find('started').text
            self.AddContent(list, srcr, common.mode_Content, show_name, '', 'tv_seasons', url=show_url, name=show_name, year=show_year)     
                
    
    
