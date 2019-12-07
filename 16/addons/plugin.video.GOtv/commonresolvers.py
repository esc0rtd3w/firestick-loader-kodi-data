# -*- coding: utf-8 -*-

'''
    This is a mod of Icefilms built-in resolvers.
    Credit goes to Eldorado.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,cookielib,xbmc,xbmcgui

puzzlepath = xbmc.translatePath('special://temp/puzzles')
try: os.makedirs(puzzlepath)
except: pass
cookiepath = xbmc.translatePath('special://temp/cookies')
try: os.makedirs(cookiepath)
except: pass


class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class resolvers:
    def get(self, url):
        try:
            if '/vk.com' in url:                url = self.vk(url)
            elif 'mail.ru' in url:              url = self.mailru(url)
            elif 'videomega.tv' in url:         url = self.videomega(url)
            elif 'docs.google.com' in url:      url = self.googledocs(url)
            elif 'picasaweb.google.com' in url: url = self.picasaweb(url)
            elif 'youtube.com' in url:          url = self.youtube(url)
            elif 'ishared.eu' in url:           url = self.ishared(url)
            elif 'firedrive.com' in url:        url = self.firedrive(url)
            elif 'movreel.com' in url:          url = self.movreel(url)
            elif 'billionuploads.com' in url:   url = self.billionuploads(url)
            elif '180upload.com' in url:        url = self._180upload(url)
            elif 'hugefiles.net' in url:        url = self.hugefiles(url)

            else:
                import urlresolver
                host = urlresolver.HostedMediaFile(url)
                if host: resolver = urlresolver.resolve(url)
                else: return url
                if not resolver.startswith('http://'): return
                if not resolver == url: return resolver

            return url
        except:
            return

    def vk(self, url):
        try:
            links = []
            url = url.replace('http://', 'https://')
            result = getUrl(url).result
            try:
                url = re.compile('url720=(.+?)&').findall(result)[0].replace('https://', 'http://')
                links.append({'quality': 'HD', 'url': url})
            except:
                pass
            try:
                url = re.compile('url540=(.+?)&').findall(result)[0].replace('https://', 'http://')
                links.append({'quality': 'SD', 'url': url})
            except:
                pass
            try:
                url = re.compile('url480=(.+?)&').findall(result)[0].replace('https://', 'http://')
                links.append({'quality': 'SD', 'url': url})
            except:
                pass

            return links
        except:
            return

    def mailru(self, url):
        try:
            url = url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
            result = getUrl(url).result
            url = re.compile('videoSrc = "(.+?)"').findall(result)[0]
            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def videomega(self, url):
        try:
            url = url.replace('/?ref=', '/iframe.php?ref=')
            result = getUrl(url).result
            url = re.compile('document.write.unescape."(.+?)"').findall(result)[0]
            url = urllib.unquote_plus(url)
            url = re.compile('file: "(.+?)"').findall(url)[0]
            return url
        except:
            return

    def googledocs(self, url):
        try:
            try:    import json
            except: import simplejson as json
            url = getUrl(url).result
            url = re.findall('("fmt_stream_map":".+?")', url, re.I)[0]
            url = json.loads('{' + url + '}')['fmt_stream_map']
            url = [i.split('|')[-1] for i in url.split(',')]
            if url == []: return
            try: url = [i for i in url if not any(x in i for x in ['&itag=43&', '&itag=35&', '&itag=34&', '&itag=5&'])][0]
            except: url = url[0]
            return url
        except:
            return

    def picasaweb(self, url):
        try:
            try:    import json
            except: import simplejson as json
            result = getUrl(url).result
            group = re.compile('picasaweb.google.com/.+?/.+?authkey=.+?#(.+)').findall(url)[0]

            result = re.compile('"streamIds":\["shared_group_%s"\],.+?"content":(\[.+?\])' % group).findall(result)[0]
            result = json.loads(result)

            url = [i for i in result if i['type'] == 'application/x-shockwave-flash']
            url += [i for i in result if i['type'] == 'video/mpeg4']
            url = url[-1]['url']
            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def youtube(self, url):
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            result = getUrl('http://gdata.youtube.com/feeds/api/videos/%s?v=2' % id).result

            state, reason = None, None
            try: state = common.parseDOM(result, "yt:state", ret="name")[0]
            except: pass
            try: reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except: pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return

            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

    def ishared(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('path:"(.+?)"').findall(result)[0]
            return url
        except:
            return

    def firedrive(self, url):
        try:
            url = url.replace('/embed/', '/file/')

            result = getUrl(url).result
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)"/>', result)
            for name, value in r: data[name] = value
            post = urllib.urlencode(data)

            result = getUrl(url, post=post).result

            url = None
            try: url = re.compile("file:.+?'(.+?)'").findall(result)[0]
            except: pass
            try: url = re.compile('.*href="(.+?)".+?id=\'external_download\'').findall(result)[0]
            except: pass
            try: url = re.compile('.*href="(.+?)".+?id=\'top_external_download\'').findall(result)[0]
            except: pass
            try: url = re.compile("id='fd_vid_btm_download_front'.+?href='(.+?)'").findall(result)[0]
            except: pass

            url = urllib.unquote_plus(url)
            url = getUrl(url, output='geturl').result

            return url
        except:
            return

    def movreel(self, url):
        try:
            html = getUrl(url).result

            op = re.search('<input type="hidden" name="op" value="(.+?)">', html).group(1)
            id = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)

            post = {'op': op, 'id': id, 'referer': url, 'rand': rand, 'method_premium': ''}
            post = urllib.urlencode(post)

            html = getUrl(url, post=post).result
            url = re.search('<a href="(.+)">Download Link</a>', html).group(1)
            return url
        except:
            return

    def _180upload(self, url):
        try:
            html = getUrl(url).result

            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
            for name, value in r: data[name] = value

            solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
            recaptcha = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
            numeric = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)    

            if solvemedia:
                challenge, solution = captcha().solvemedia(solvemedia.group(1))
                data.update({'adcopy_challenge': challenge, 'adcopy_response': solution})
            elif recaptcha:
                challenge, solution = captcha().google(recaptcha.group(1))
                data.update({'recaptcha_challenge_field': challenge, 'recaptcha_response_field': solution})               
            elif numeric:
                solution = captcha().numeric(numeric)
                data.update({'code':solution})

            data = urllib.urlencode(data)
            html = getUrl(url, post=data).result

            url = re.search('id="lnk_download" href="([^"]+)', html).group(1)
            return url
        except:
            return

    def hugefiles(self, url):
        try:
            html = getUrl(url).result

            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
            for name, value in r: data[name] = value
            data['method_free'] = 'Free Download'

            solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)
            recaptcha = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
            numeric = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)    

            if solvemedia:
                challenge, solution = captcha().solvemedia(solvemedia.group(1))
                data.update({'adcopy_challenge': challenge, 'adcopy_response': solution})
            elif recaptcha:
                challenge, solution = captcha().google(recaptcha.group(1))
                data.update({'recaptcha_challenge_field': challenge, 'recaptcha_response_field': solution})               
            elif numeric:
                solution = captcha().numeric(numeric)
                data.update({'code':solution})

            data = urllib.urlencode(data)

            u = getUrl(url, output='geturl', post=data).result
            if not url == u: return u

            html = getUrl(url, post=data).result

            sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
            r = re.findall(sPattern, html, re.DOTALL|re.I)[0]
            sUnpacked = jsunpack().unpack(r).replace('\\', '')

            url = None
            try: url = re.findall('file,(.+?)\)\;s1',sUnpacked)[0]
            except: url = re.findall('name="src"[0-9]*="(.+?)"/><embed',sUnpacked)[0]
            return url
        except:
            return

    def billionuploads(self, url):
        try:
            cookie_file = os.path.join(cookiepath,'billionuploads.lwp')

            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try: cj.load(cookie_file,True)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)

            normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            headers = [
                ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Language', 'en-US,en;q=0.5'),
                ('Accept-Encoding', ''),
                ('DNT', '1'),
                ('Connection', 'keep-alive'),
                ('Pragma', 'no-cache'),
                ('Cache-Control', 'no-cache')
            ]
            normal.addheaders = headers
            class NoRedirection(urllib2.HTTPErrorProcessor):
                # Stop Urllib2 from bypassing the 503 page.
                def http_response(self, request, response):
                    code, msg, hdrs = response.code, response.msg, response.info()
                    return response
                https_response = http_response
            opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = normal.addheaders
            response = opener.open(url).read()
            decoded = re.search('(?i)var z="";var b="([^"]+?)"', response)
            if decoded:
                decoded = decoded.group(1)
                z = []
                for i in range(len(decoded)/2):
                    z.append(int(decoded[i*2:i*2+2],16))
                decoded = ''.join(map(unichr, z))
                incapurl = re.search('(?i)"GET","(/_Incapsula_Resource[^"]+?)"', decoded)
                if incapurl:
                    incapurl = 'http://billionuploads.com'+incapurl.group(1)
                    opener.open(incapurl)
                    cj.save(cookie_file,True)
                    response = opener.open(url).read()

            captcha = re.search('(?i)<iframe src="(/_Incapsula_Resource[^"]+?)"', response)
            if captcha:
                captcha = 'http://billionuploads.com'+captcha.group(1)
                opener.addheaders.append(('Referer', url))
                response = opener.open(captcha).read()
                formurl = 'http://billionuploads.com'+re.search('(?i)<form action="(/_Incapsula_Resource[^"]+?)"', response).group(1)
                resource = re.search('(?i)src=" (/_Incapsula_Resource[^"]+?)"', response)
                if resource:
                    import random
                    resourceurl = 'http://billionuploads.com'+resource.group(1) + str(random.random())
                    opener.open(resourceurl)
                recaptcha = re.search('(?i)<script type="text/javascript" src="(https://www.google.com/recaptcha/api[^"]+?)"', response)
                if recaptcha:
                    response = opener.open(recaptcha.group(1)).read()
                    challenge = re.search('''(?i)challenge : '([^']+?)',''', response)
                    if challenge:
                        challenge = challenge.group(1)
                        captchaimg = 'https://www.google.com/recaptcha/api/image?c=' + challenge
                        img = xbmcgui.ControlImage(450,15,400,130,captchaimg)
                        wdlg = xbmcgui.WindowDialog()
                        wdlg.addControl(img)
                        wdlg.show()

                        xbmc.sleep(3000)

                        kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                        kb.doModal()
                        capcode = kb.getText()
                        if (kb.isConfirmed()):
                            userInput = kb.getText()
                            if userInput != '': capcode = kb.getText()
                            elif userInput == '':
                                logerror('BillionUploads - Image-Text not entered')
                                xbmc.executebuiltin("XBMC.Notification(Image-Text not entered.,BillionUploads,2000)")              
                                return None
                        else: return None
                        wdlg.close()
                        captchadata = {}
                        captchadata['recaptcha_challenge_field'] = challenge
                        captchadata['recaptcha_response_field'] = capcode
                        opener.addheaders = headers
                        opener.addheaders.append(('Referer', captcha))
                        resultcaptcha = opener.open(formurl,urllib.urlencode(captchadata)).info()
                        opener.addheaders = headers
                        response = opener.open(url).read()

            ga = re.search('(?i)"text/javascript" src="(/ga[^"]+?)"', response)
            if ga:
                jsurl = 'http://billionuploads.com'+ga.group(1)
                p  = "p=%7B%22appName%22%3A%22Netscape%22%2C%22platform%22%3A%22Win32%22%2C%22cookies%22%3A1%2C%22syslang%22%3A%22en-US%22"
                p += "%2C%22userlang%22%3A%22en-US%22%2C%22cpu%22%3A%22WindowsNT6.1%3BWOW64%22%2C%22productSub%22%3A%2220100101%22%7D"
                opener.open(jsurl, p)
                response = opener.open(url).read()
    #         pid = re.search('(?i)PID=([^"]+?)"', response)
    #         if pid:
    #             normal.addheaders += [('Cookie','D_UID='+pid.group(1)+';')]
    #             opener.addheaders = normal.addheaders
            if re.search('(?i)url=/distil_r_drop.html', response) and filename:
                url += '/' + filename
                response = normal.open(url).read()
            jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
            if jschl:
                jschl = jschl[0]    
                maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')
                domain_url = re.compile('(https?://.+?/)').findall(url)[0]
                domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
                final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
                html = normal.open(url).read()
            else: html = response 

            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', html)
            for name, value in r: data[name] = value

            captchaimg = re.search('<img src="((?:http://|www\.)?BillionUploads.com/captchas/.+?)"', html)            
            if captchaimg:

                img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()

                kb = xbmc.Keyboard('', 'Please enter the text in the image', False)
                kb.doModal()
                capcode = kb.getText()
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '': capcode = kb.getText()
                    elif userInput == '':
                        showpopup('BillionUploads','[B]You must enter the text from the image to access video[/B]',5000, elogo)
                        return None
                else: return None
                wdlg.close()

                data.update({'code':capcode})

            data.update({'submit_btn':''})
            enc_input = re.compile('decodeURIComponent\("(.+?)"\)').findall(html)
            if enc_input:
                dec_input = urllib2.unquote(enc_input[0])
                r = re.findall(r'type="hidden" name="(.+?)" value="(.*?)">', dec_input)
                for name, value in r:
                    data[name] = value
            extradata = re.compile("append\(\$\(document.createElement\('input'\)\).attr\('type','hidden'\).attr\('name','(.*?)'\).val\((.*?)\)").findall(html)
            if extradata:
                for attr, val in extradata:
                    if 'source="self"' in val:
                        val = re.compile('<textarea[^>]*?source="self"[^>]*?>([^<]*?)<').findall(html)[0]
                    data[attr] = val.strip("'")
            r = re.findall("""'input\[name="([^"]+?)"\]'\)\.remove\(\)""", html)

            for name in r: del data[name]

            normal.addheaders.append(('Referer', url))
            html = normal.open(url, urllib.urlencode(data)).read()
            cj.save(cookie_file,True)

            def custom_range(start, end, step):
                while start <= end:
                    yield start
                    start += step

            def checkwmv(e):
                s = ""
                i=[]
                u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
                for z in range(0, len(u)):
                    for n in range(u[z][0],u[z][1]):
                        i.append(chr(n))
                t = {}
                for n in range(0, 64): t[i[n]]=n
                for n in custom_range(0, len(e), 72):
                    a=0
                    h=e[n:n+72]
                    c=0
                    for l in range(0, len(h)):            
                        f = t.get(h[l], 'undefined')
                        if f == 'undefined': continue
                        a = (a<<6) + f
                        c = c + 6
                        while c >= 8:
                            c = c - 8
                            s = s + chr( (a >> c) % 256 )
                return s

            dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)
            if dll:
                dl = dll[0].split('GvaZu')[1]
                dl = checkwmv(dl);
                dl = checkwmv(dl);
            else:
                alt = re.compile('<source src="([^"]+?)"').findall(html)
                if alt:
                    dl = alt[0]
                else:
                    raise Exception('Unable to resolve - No Video File Found')  

            return dl

        except Exception, e:
            raise

class captcha:
    def solvemedia(self, captcha):
        try:
            image = os.path.join(puzzlepath, "solve_puzzle.png")

            html = getUrl(captcha).result

            challenge = re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)

            try: puzzle = re.search('<div><iframe src="(/papi/media.+?)"', html).group(1)
            except: puzzle = re.search('<img src="(/papi/media.+?)"', html).group(1)
            puzzle = "http://api.solvemedia.com%s" % puzzle

            file = open(image, 'wb')
            file.write(getUrl(puzzle).result)
            file.close()

            solution = self.solution(image)
            return (challenge, solution)
        except:
            return

    def google(self, captcha):
        try:
            html = getUrl(captcha).result

            challenge = re.search("challenge \: \\'(.+?)\\'", html).group(1)
            image = 'http://www.google.com/recaptcha/api/image?c=' + challenge

            solution = self.solution(image)
            return (challenge, solution)
        except:
            return

    def numeric(self, captcha):
        try:
            result = sorted(captcha, key=lambda ltr: int(ltr[0]))
            solution = ''.join(str(int(num[1])-48) for num in result)
            return solution
        except:
            return

    def solution(self, image):
        try:
            image = xbmcgui.ControlImage(450,15,400,130, image)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(image)
            wdlg.show()

            xbmc.sleep(3000)

            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()

            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    raise Exception ('You must enter text in the image to access video')
            else:
                raise Exception ('Captcha Error')
            wdlg.close()

            return solution
        except:
            return

class jsunpack:
    def unpack(self, sJavascript):
        aSplit = sJavascript.split(";',")
        p = str(aSplit[0])
        aSplit = aSplit[1].split(",")
        a = int(aSplit[0])
        c = int(aSplit[1])
        k = aSplit[2].split(".")[0].replace("'", '').split('|')
        e = ''
        d = ''
        sUnpacked = str(self.__unpack(p, a, c, k, e, d))
        return sUnpacked.replace('\\', '')

    def __unpack(self, p, a, c, k, e, d):
        while (c > 1):
            c = c -1
            if (k[c]):
                p = re.sub('\\b' + str(self.__itoa(c, a)) +'\\b', k[c], p)
        return p

    def __itoa(self, num, radix):
        result = ""
        while num > 0:
            result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
            num /= radix
        return result