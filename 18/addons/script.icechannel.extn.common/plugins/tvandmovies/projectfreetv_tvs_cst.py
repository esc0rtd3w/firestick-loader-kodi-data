'''
    Istream
    Project Free TV
    Copyright (C) 2013 Coolwave

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
import re

class projectfreetv(TVShowSource,CustomSettings):
    implements = [TVShowSource,CustomSettings]
	
    #unique name of the source
    name = "projectfreetv"
    source_enabled_by_default = 'true'
    #display name of the source
    display_name = "Project Free TV"

    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/1120740c0028d16de328516e4f0c889aa949b65e/pojectfreetv.png'
    
    #base url of the source website 
    base_url_tv = 'http://project-free-tv.li/'

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_url" type="labelenum" label="URL" default="http://projectfreetv.at/" values="Custom|http://projectfreetv.at/" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom" default="" enable="eq(-1,0)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

    def get_url(self):
        custom_url = self.Settings().get_setting('custom_url')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')
        if not custom_url.startswith('http://'):
            custom_url = ('http://' + custom_url)
        if not custom_url.endswith('/'):
            custom_url += '/'
        return custom_url


  
        
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        custom_url = self.get_url()
        #custom_url = self.get_url()
        name = (name).lower()
        
        import re
        tv_url= custom_url+'%s/index.html' %(name.lower().replace(' ','-'))
     
        new_url = url
               
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET(tv_url).content
        
        if type == 'tv_seasons':
            match=re.compile('<td width="99%" class="mnlcategorylist"><a href="(.+?)"><b>Season (.+?)</b></a>').findall(content)
            for url, seasonnumber in match:                
                item_url = custom_url+'%s/' %(name.lower().replace(' ','_'))
                item_url1 = item_url+url
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url1, name=name, season=seasonnumber)
               
        elif type == 'tv_episodes':
            tv_url2=custom_url+'%s/season_%s.html' %(name.lower().replace(' ','_'),season)
            from entertainment.net import Net
            net = Net(cached=False)
            content2 = net.http_GET(tv_url2).content
            match=re.compile('<td class="episode"><a name=".+?"></a><b>.+?. (.+?)</b></td>\s*<td class="mnllinklist" align="right"><div class="right">S.+?E(.+?)&').findall(content2)
            for item_title, item_v_id_2  in match:
                item_v_id_2 = str(int(item_v_id_2))
                item_url = tv_url2 + '?episode=' + item_v_id_2
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
            
    

    
    def GetFileHosts(self, url, list, lock, message_queue):
        import re

        from entertainment.net import Net
        net = Net(cached=False)

        
        content = net.http_GET(url).content#<a onclick='visited(1980258)' href="http://www.free-tv-video-online.me/player/novamov.php?id=uauyj7jxjsw83" target="_blank">
        r = '<a href="(.+?)" target="_blank" rel="nofollow"><img src=".+?domain=(.+?)"'
        match  = re.compile(r).findall(content)
        
        
        for url,host in match:

            
            self.AddFileHost(list, 'SD', url, host=host.upper())


    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        custom_url = self.get_url()
        
        import urllib2
        import re
        from entertainment.net import Net
        net = Net(cached=False)

        search_term = self.CleanTextForSearch(name)
        category = ''
        if type == 'tv_episodes':
            category = 'category=4'
        elif type == 'movies':
            category = 'category=5'
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        #Movies = http://oneclickwatch.org/?s=Escape+Plan+2013
        #TV Shows = http://www.free-tv-video-online.me/search/?q=2%20broke%20Girls&md=all
        #tv shows = http://www.free-tv-video-online.me/internet/%s/season_%s.html
        
        if type == 'tv_episodes':
            season_pull = "%s"%season if len(season)<2 else season
            episode_pull = "%s"%episode if len(episode)<2 else episode

            tv_url=custom_url+'episode/%s-season-%s-episode-%s' %(name.lower().replace(' ','-'),season_pull,episode_pull)
            
            self.GetFileHosts(tv_url, list, lock, message_queue)



