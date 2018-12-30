# -*- coding: utf-8 -*-

import re,urllib,urlparse,base64
from resources.lib.modules import client
from resources.lib.modules import jsunpack

def TEST():
    return

def resolve(url):
        #url = 'http://www3.sawlive.tv/embed/lag3pc'
        try:        
                page = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(url)[0]
                page = 'http://%s/embed/%s' % (page[0], page[1])
                
                try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
                except: referer = page
                
                result = client.request(page, referer=referer)
                unpacked = ''
                packed = result.split('\n')
                print packed
                for i in packed: 
                    try: unpacked += jsunpack.unpack(i)
                    except: pass
                result += unpacked
                
                result = urllib.unquote_plus(result)
                print result
                vars = re.compile("var (.+?='.+?');").findall(str(result))
                print vars
                for item in vars:
                        var = item.split('=')
                rep = re.findall('(.+?)=.+?\.replace\((.+?),(.+?)\)',str(result))
                result = re.sub('\s\s+', ' ', result)
                url = client.parseDOM(result, 'iframe', ret='src')[-1]
                url = url.replace(' ', '').split("'")[0]
                var = re.compile('var zdywbs="([^"]+)"').findall(str(result))[0]
                value = re.compile('value="([^"]+)"').findall(str(result))[0]
                url='http://www.sawlive.tv/embed/watch/'+var+'/'+value
                result = client.request(url)                
                file = re.compile("\('file',(.+?)\)").findall(result)[0]
                
                file = urllib.unquote_plus(file)
                
                var2= re.compile("var (.+?) =.+?'(.+?)'").findall(result)
                strm = re.compile("\('streamer',(.+?)\)").findall(result)[0]
                #replaceVar=re.search("= (.+?).replace\('(.+?)',('.+?)\);",result,re.I)
                testLink=re.compile("\{ return '(.+?)'; \}").findall(result)[0]
                strm =strm.replace("'",'').replace('"','')
                for name, parts in var2:
                        if 'bmakz' in name:
                                parts=' '+parts
                        name = name.replace("'",'').replace('"','')
                        parts = parts.replace("'",'').replace('"','')
                        if (name) in file: file = file.replace(name,parts)
                        if (name) in strm: strm = strm.replace(name,testLink)
                file = file.replace(' ','').replace('"','').replace("'","").replace("33333","").replace("1?","?")
                #file=file.split('?')[0]

                try:
                    if not file.startswith('http'): raise Exception()
                    url = client.request(file, output='geturl')
                    if not '.m3u8' in url: raise Exception()
                    url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': file})
                    return url
                    
                except:
                    pass

                #strm = re.compile("'streamer'.+?'(.+?)'").findall(result)[0]
                swf = re.compile("SWFObject\('(.+?)'").findall(result)[0]
                
                url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=30' % (strm.replace(' ',''), file, swf, url)
                finalUrl = urllib.unquote_plus(url.replace('unescape(','').replace('+',''))
                return finalUrl
                    
            
          
        except:
                return

