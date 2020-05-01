'''
    Ice Channel
    Easy News
'''
import os
import xbmc, xbmcaddon, xbmcgui, xbmcplugin

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import re

class EasyNews(MovieSource, TVShowSource, CustomSettings):
    implements = [MovieSource, TVShowSource, CustomSettings]
    
    name = "EasyNews"
    display_name = "Easy News"
    
    source_enabled_by_default = 'false'
    
    auto_play_supported = False
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="ssl" type="bool" label="Use SSL" default="false" />\n'
        xml += '<setting id="easy_user" type="text" label="Username" default="" />\n'
        xml += '<setting id="easy_pass" type="text" option="hidden" label="Password" default="" />\n'
        xml += '</category>\n' 
        xml += '<category label="Movies">\n'
        xml += '<setting id="mfileext" type="enum" values="Any|AVI|MKV|MP4|ISO|DIVX|MPG|FLV|WMV|MOV|ASF|RM" label="File Extension:" default="2" />\n'
        xml += '<setting id="mfilesize" type="enum" values="Any|1MB|5Mb|15MB|25Mb|30Mb|40Mb|50Mb|75Mb|100Mb|200Mb|300Mb|400Mb|500Mb|750M|1Gb|1.5Gb|2Gb|2.5Gb|3Gb|3.5Gb|4Gb|5GB|6Gb|7GB|8Gb" label="Minimum File Size" default="0" />\n'
        xml += '<setting id="mmaxfilesize" type="enum" values="Any|1MB|5Mb|15MB|25Mb|30Mb|40Mb|50Mb|75Mb|100Mb|200Mb|300Mb|400Mb|500Mb|750M|1Gb|1.5Gb|2Gb|2.5Gb|3Gb|3.5Gb|4Gb|5GB|6Gb|7GB|8Gb" label="Max File Size:" default="0" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="mresults" type="number" label="Maximum Results:" default="1000" enable="!eq(-1,false)"/>\n'
        xml += '<setting id="mlangex" type="text" label="Language Exclusions:" default="" enable="!eq(-3,false)"/>\n'
        xml += '<setting id="mreso" type="enum" values="Any|Up To 720p|720p Exactly|1080p Exactly|" label="Choose Resolution:" default="0" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="mspam" type="bool" label="Enable Spam Filter:" default="true"/>\n'
        xml += '<setting id="mrem" type="bool" label="Remove Duplicates:" default="true"/>\n'
        xml += '<setting id="mgrex" type="bool" label="Enable Group Exclusion:" default="true"/>\n'
        xml += '<setting id="msubject" type="text" label="Subject:" default="" enable="!eq(-2,false)"/>\n'
        xml += '<setting id="mposter" type="text" label="Poster:" default="" enable="!eq(-3,false)"/>\n'
        xml += '<setting id="mnewsgroup" type="text" label="Newsgroup:" default="" enable="!eq(-4,false)"/>\n'
        xml += '<setting id="mfilename" type="text" label="Filename:" default="" enable="!eq(-5,false)"/>\n'
        xml += '<setting id="mvcodec" type="text" label="Video Codec:" default="" enable="!eq(-6,false)"/>\n'
        xml += '<setting id="macodec" type="text" label="Audio Codec:" default="" enable="!eq(-7,false)"/>\n'
        xml += '</category>\n'
        xml += '<category label="Tv-Shows">\n'
        xml += '<setting id="tvfileext" type="enum" values="Any|AVI|MKV|MP4|ISO|DIVX|MPG|FLV|WMV|MOV|ASF|RM" label="File Extension:" default="1" />\n'
        xml += '<setting id="tvfilesize" type="enum" values="Any|1MB|5Mb|15MB|25Mb|30Mb|40Mb|50Mb|75Mb|100Mb|200Mb|300Mb|400Mb|500Mb|750M|1Gb|1.5Gb|2Gb|2.5Gb|3Gb|3.5Gb|4Gb|5GB|6Gb|7GB|8Gb" label="Minimum File Size" default="0" />\n'
        xml += '<setting id="tvmaxfilesize" type="enum" values="Any|1MB|5Mb|15MB|25Mb|30Mb|40Mb|50Mb|75Mb|100Mb|200Mb|300Mb|400Mb|500Mb|750M|1Gb|1.5Gb|2Gb|2.5Gb|3Gb|3.5Gb|4Gb|5GB|6Gb|7GB|8Gb" label="Max File Size:" default="0" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="tvresults" type="number" label="Maximum Results:" default="1000" enable="!eq(-1,false)"/>\n'
        xml += '<setting id="tvlangex" type="text" label="Language Exclusions:" default="" enable="!eq(-3,false)"/>\n'
        xml += '<setting id="tvreso" type="enum" values="Any|Up To 720p|720p Exactly|1080p Exactly|" label="Choose Resolution:" default="0" />\n'
        xml += '<setting type="sep" />\n'
        xml += '<setting id="tvspam" type="bool" label="Enable Spam Filter:" default="true"/>\n'
        xml += '<setting id="tvrem" type="bool" label="Remove Duplicates:" default="true"/>\n'
        xml += '<setting id="tvgrex" type="bool" label="Enable Group Exclusion:" default="true"/>\n'
        xml += '<setting id="tvsubject" type="text" label="Subject:" default="" enable="!eq(-2,false)"/>\n'
        xml += '<setting id="tvposter" type="text" label="Poster:" default="" enable="!eq(-3,false)"/>\n'
        xml += '<setting id="tvnewsgroup" type="text" label="Newsgroup:" default="" enable="!eq(-4,false)"/>\n'
        xml += '<setting id="tvfilename" type="text" label="Filename:" default="" enable="!eq(-5,false)"/>\n'
        xml += '<setting id="tvvcodec" type="text" label="Video Codec:" default="" enable="!eq(-6,false)"/>\n'
        xml += '<setting id="tvacodec" type="text" label="Audio Codec:" default="" enable="!eq(-7,false)"/>\n'
        xml += '</category>\n'
        xml += '</settings>\n'
        
        self.CreateSettings(self.name, self.display_name, xml)
        
    def mlang_ex(self):
        return self.Settings().get_setting('mlangex').replace(' ','+')
          
        
    def m_filesize(self):
        quality = self.Settings().get_setting('mfilesize')
        if quality == '0':
            return ''
        elif quality == '1':
            return '8'
        elif quality == '2':
            return '9'
        elif quality == '3':
            return '10'
        elif quality == '4':
            return '11'
        elif quality == '5':
            return '12'
        elif quality == '6':
            return '13'
        elif quality == '7':
            return '14'
        elif quality == '8':
            return '15'
        elif quality == '9':
            return '16'
        elif quality == '10':
            return '17'
        elif quality == '11':
            return '18'
        elif quality == '12':
            return '19'
        elif quality == '13':
            return '20'
        elif quality == '14':
            return '21'
        elif quality == '15':
            return '22'
        elif quality == '16':
            return '23'
        elif quality == '17':
            return '24'
        elif quality == '18':
            return '25'
        elif quality == '19':
            return '26'
        elif quality == '20':
            return '27'
        elif quality == '21':
            return '28'
        elif quality == '22':
            return '29'
        elif quality == '23':
            return '30'
        elif quality == '24':
            return '31'
        elif quality == '25':
            return '32'
            
            
    def m_maxfilesize(self):
        quality = self.Settings().get_setting('mmaxfilesize')
        if quality == '0':
            return ''
        elif quality == '1':
            return '8'
        elif quality == '2':
            return '9'
        elif quality == '3':
            return '10'
        elif quality == '4':
            return '11'
        elif quality == '5':
            return '12'
        elif quality == '6':
            return '13'
        elif quality == '7':
            return '14'
        elif quality == '8':
            return '15'
        elif quality == '9':
            return '16'
        elif quality == '10':
            return '17'
        elif quality == '11':
            return '18'
        elif quality == '12':
            return '19'
        elif quality == '13':
            return '20'
        elif quality == '14':
            return '21'
        elif quality == '15':
            return '22'
        elif quality == '16':
            return '23'
        elif quality == '17':
            return '24'
        elif quality == '18':
            return '25'
        elif quality == '19':
            return '26'
        elif quality == '20':
            return '27'
        elif quality == '21':
            return '28'
        elif quality == '22':
            return '29'
        elif quality == '23':
            return '30'
        elif quality == '24':
            return '31'
        elif quality == '25':
            return '32'
            
    def tv_filesize(self):
        quality = self.Settings().get_setting('tvfilesize')
        if quality == '0':
            return ''
        elif quality == '1':
            return '8'
        elif quality == '2':
            return '9'
        elif quality == '3':
            return '10'
        elif quality == '4':
            return '11'
        elif quality == '5':
            return '12'
        elif quality == '6':
            return '13'
        elif quality == '7':
            return '14'
        elif quality == '8':
            return '15'
        elif quality == '9':
            return '16'
        elif quality == '10':
            return '17'
        elif quality == '11':
            return '18'
        elif quality == '12':
            return '19'
        elif quality == '13':
            return '20'
        elif quality == '14':
            return '21'
        elif quality == '15':
            return '22'
        elif quality == '16':
            return '23'
        elif quality == '17':
            return '24'
        elif quality == '18':
            return '25'
        elif quality == '19':
            return '26'
        elif quality == '20':
            return '27'
        elif quality == '21':
            return '28'
        elif quality == '22':
            return '29'
        elif quality == '23':
            return '30'
        elif quality == '24':
            return '31'
        elif quality == '25':
            return '32'
            
            
    def tv_maxfilesize(self):
        quality = self.Settings().get_setting('tvmaxfilesize')
        if quality == '0':
            return ''
        elif quality == '1':
            return '8'
        elif quality == '2':
            return '9'
        elif quality == '3':
            return '10'
        elif quality == '4':
            return '11'
        elif quality == '5':
            return '12'
        elif quality == '6':
            return '13'
        elif quality == '7':
            return '14'
        elif quality == '8':
            return '15'
        elif quality == '9':
            return '16'
        elif quality == '10':
            return '17'
        elif quality == '11':
            return '18'
        elif quality == '12':
            return '19'
        elif quality == '13':
            return '20'
        elif quality == '14':
            return '21'
        elif quality == '15':
            return '22'
        elif quality == '16':
            return '23'
        elif quality == '17':
            return '24'
        elif quality == '18':
            return '25'
        elif quality == '19':
            return '26'
        elif quality == '20':
            return '27'
        elif quality == '21':
            return '28'
        elif quality == '22':
            return '29'
        elif quality == '23':
            return '30'
        elif quality == '24':
            return '31'
        elif quality == '25':
            return '32'
            

    def m_fileext(self):
        quality = self.Settings().get_setting('mfileext')
        if quality == '0':
            return ''
        elif quality == '1':   
            return 'AVI'
        elif quality == '2':
            return 'MKV'
        elif quality == '3':
            return 'MP4'
        elif quality == '4':
            return 'ISO'
        elif quality == '5':
            return 'DIVX'
        elif quality == '6':
            return 'MPG'
        elif quality == '7':
            return 'FLV'
        elif quality == '8':
            return 'WMV'
        elif quality == '9':
            return 'MOV'
        elif quality == '10':
            return 'ASF'
        elif quality == '11':
            return 'RM'
            
    def tv_fileext(self):
        quality = self.Settings().get_setting('tvfileext')
        if quality == '0':
            return ''
        elif quality == '1':   
            return 'AVI'
        elif quality == '2':
            return 'MKV'
        elif quality == '3':
            return 'MP4'
        elif quality == '4':
            return 'ISO'
        elif quality == '5':
            return 'DIVX'
        elif quality == '6':
            return 'MPG'
        elif quality == '7':
            return 'FLV'
        elif quality == '8':
            return 'WMV'
        elif quality == '9':
            return 'MOV'
        elif quality == '10':
            return 'ASF'
        elif quality == '11':
            return 'RM'


    def easy_url(self):
        return 'http://members-beta.easynews.com/global5/search.html?&gps='
        
    def end_url(self):
        return '&st=adv&safe=1&boost=1&sb=1'
        
    def m_subject(self):
        return  self.Settings().get_setting('msubject')
        
        
    def m_poster(self):
        return self.Settings().get_setting('mposter')
        
    def m_newsgroup(self):
        return self.Settings().get_setting('mnewsgroup').replace(',','%2c')
        
    def m_filename(self):
        return self.Settings().get_setting('mfilename')
        
    def m_vcodec(self):
        return self.Settings().get_setting('mvcodec')
        
    def m_acodec(self):
        return self.Settings().get_setting('macodec')
        
    def m_filename(self):
        return self.Settings().get_setting('mfilename')
        
    def m_results(self):
        return self.Settings().get_setting('mresults')
        
       
        
    def tv_subject(self):
        return self.Settings().get_setting('tvsubject')
        
    def tv_poster(self):
        return self.Settings().get_setting('tvposter')
        
    def tv_newsgroup(self):
        return self.Settings().get_setting('tvnewsgroup')
        
    def tv_vcodec(self):
        return self.Settings().get_setting('tvvcodec')
        
    def tv_acodec(self):
        return self.Settings().get_setting('tvacodec')
        
    def tv_filename(self):
        return self.Settings().get_setting('tvfilename')
        
    def tv_results(self):
        return self.Settings().get_setting('tvresults')
        
    def m_spam(self):
        if self.Settings().get_setting('mspam') == "true":
            return '&spamf=1'
        if self.Settings().get_setting('mspam') == "false":
            return ''
            
    def tv_spam(self):
        if self.Settings().get_setting('tvspam') == "true":
            return '&spamf=1'
        if self.Settings().get_setting('tvspam') == "false":
            return ''
                 
    def m_rem(self):
        if self.Settings().get_setting('mrem') == "true":
            return '&u=1'
        if self.Settings().get_setting('mrem') == "false":
            return ''
            
    def tv_rem(self):
        if self.Settings().get_setting('tvrem') == "true":
            return '&u=1'
        if self.Settings().get_setting('tvrem') == "false":
            return ''
                    
    def m_grex(self):
        if self.Settings().get_setting('mgrex') == "true":
            return '&gx=1'
        if self.Settings().get_setting('mgrex') == "false":
            return ''
            
    def tv_grex(self):
        if self.Settings().get_setting('tvgrex') == "true":
            return '&gx=1'
        if self.Settings().get_setting('tvgrex') == "false":
            return ''
            
    def tvlang_ex(self):
        return self.Settings().get_setting('tvlangex').replace(' ','+')
        
    def tv_reso(self):
        quality = self.Settings().get_setting('tvreso')
        if quality == '0':
            return '&px1=&px1t=&px=&px2t='
        if quality == '1':
            return '&px1=&px1t=&px2=&px2t=9'
        elif quality == '2':
            return '&px1=&px1t=5&px2=&px2t=9'
        elif quality == '3':
            return '&px1=&px1t=8&px2=&px2t=10'
            
    def m_reso(self):
        quality = self.Settings().get_setting('mreso')
        if quality == '0':
            return '&px1=&px1t=&px=&px2t='
        if quality == '1':
            return '&px1=&px1t=&px2=&px2t=9'
        elif quality == '2':
            return '&px1=&px1t=5&px2=&px2t=9'
        elif quality == '3':
            return '&px1=&px1t=8&px2=&px2t=10'
        
    def passman(self, theurl):
            import urllib2
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, theurl, self.Settings().get_setting('easy_user'), self.Settings().get_setting('easy_pass'))
            
            class HTTPBasicAuthHandlerWithLimitedRetries(urllib2.HTTPBasicAuthHandler):
                max_retries = 1
                cur_retries = 0
                def http_error_401(self, req, fp, code, msg, headers):
                    if self.cur_retries == self.max_retries:
                        return None
                        
                    self.cur_retries += 1
                    url = req.get_full_url()
                    return self.http_error_auth_reqed('www-authenticate',
                                                      url, req, headers)
            
            authhandler = HTTPBasicAuthHandlerWithLimitedRetries(passman)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
            pagehandle = urllib2.urlopen(theurl)
            link= pagehandle.read()    
            return link  
    
    def GetFileHosts(self, url, list, lock, message_queue,codec,name): 
        
        if self.Settings().get_setting('easy_user') == '':
            return
            
        self.AddFileHost(list, codec.upper(), url,name)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
    
        if self.Settings().get_setting('easy_user') == '':
            return
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        match_name = name
        
        if type == 'movies':
            search_term = name+ ' '+year
            theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_term.replace(' ','+')+'+%21+'+self.mlang_ex()+'&sbj='+self.m_subject()+'&from='+self.m_poster()+'&ns='+self.m_newsgroup()+'&fil='+self.m_filename()+'&fex=&vc='+self.m_vcodec()+'&ac='+self.m_acodec()+'&pby='+self.m_results()+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+self.m_filesize()+'&b2t='+self.m_maxfilesize()+self.m_reso()+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+self.m_spam()+self.m_rem()+self.m_grex()+'&st=adv&safeO=0&sb=1'
        elif type == 'tv_episodes':
            season = 's'+season
            season = season.replace('s1','s01').replace('s2','s02').replace('s3','s03').replace('s4','s04').replace('s5','s05').replace('s6','s06').replace('s7','s07').replace('s8','s08').replace('s9','s09')
            if len(season)> 3:
                season = season.replace('s0','s')
            episode = 'e'+episode
            episode = episode.replace('e1','e01').replace('e2','e02').replace('e3','e03').replace('e4','e04').replace('e5','e05').replace('e6','e06').replace('e7','e07').replace('e8','e08').replace('e9','e09')
            if len(episode)> 3:
                episode = episode.replace('e0','e')
            search_term = name+ ' '+season+ ' '+episode
            theurl = 'http://members.easynews.com/2.0/search/solr-search/advanced?gps='+search_term.replace(' ','+')+'+%21+'+self.tvlang_ex()+'&sbj='+self.tv_subject()+'&from='+self.tv_poster()+'&ns='+self.tv_newsgroup()+'&fil='+self.tv_filename()+'&fex=&vc='+self.tv_vcodec()+'&ac='+self.tv_acodec()+'&pby='+self.tv_results()+'&pno=1&s1=nsubject&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t='+self.tv_filesize()+'&b2t='+self.tv_maxfilesize()+self.tv_reso()+'&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&fty[]=VIDEO'+self.tv_spam()+self.tv_rem()+self.tv_grex()+'&st=adv&safeO=0&sb=1'
            
        link= self.passman(theurl)    
        import json
        link = json.loads(link, encoding='utf8')
        results=link['results']
        data=link['data']
        for field in data:
            num= field['0']
            size= field['4']
            codec=field['11']
            
            _name=field['10']
            if self.Match(match_name, _name) == False:
                continue
            
            lang=field['alangs']
            lang='[COLOR yellow]%s[/COLOR]'%(lang)
            url='http://members.easynews.com/dl/'+num+codec+'/'+_name+codec
            name_ = '[COLOR orange][FMT: %s, FSZ: %s][/COLOR] %s' %(codec.replace('.','').upper(),size,lang)+' '+_name
            name = name_.replace('None','').replace("u'",'').replace("'",'')
            
            if self.Settings().get_setting('ssl') == 'true':
                    url = str(url).replace('http://','https://').replace(' ','%20')

            
            res = 'NA'
            file_name_lower = _name.lower()
            for key, value in common.quality_dict.iteritems():
                if re.search('[^a-zA-Z0-9]' + key + '[^a-zA-Z0-9]', file_name_lower) or file_name_lower.endswith(key):
                    res = value
                    break
                
            if '3d' in file_name_lower:
                res ='3D'
                
            if res == 'NA':
                if 'GB' in size:
                    file_sz_flt = float( re.search( '([0-9\.]+)', size ).group(1) )
                    if file_sz_flt >= 2.0:
                        res = 'HD'
                    else:
                        res = 'SD'
                else:
                    res = 'LOW'
            
            self.GetFileHosts(url, list, lock, message_queue,res,name)
                
            
    def Resolve(self, url):
        import base64
        url = url+'|Authorization=Basic%20' + base64.b64encode(self.Settings().get_setting('easy_user')+':'+self.Settings().get_setting('easy_pass'))
        return url
