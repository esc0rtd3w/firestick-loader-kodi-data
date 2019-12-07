import sys,traceback,urllib2,re, urllib,xbmc,requests
def createCookie(url,cj=None,agent='Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'):
    urlData=''
    try:
        import urlparse,cookielib,urllib2
        class NoRedirection(urllib2.HTTPErrorProcessor):    
            def http_response(self, request, response):
                return response
        def parseJSString(s):
            try:
                offset=1 if s[0]=='+' else 0
                val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
                return val
            except:
                pass
        if cj==None:
            cj = cookielib.CookieJar()
        headers={'User-Agent' : agent,'Referer' : url}       
        result = requests.get(url,headers=headers).content
        jschl = re.compile('name="jschl_vc" value="(.+?)"/>').findall(result)[0]
        init = re.compile('setTimeout\(function\(\){\s*.*?.*:(.*?)};').findall(result)[0]
        builder = re.compile(r"challenge-form\'\);\s*(.*)a.v").findall(result)[0]
        decryptVal = parseJSString(init)
        lines = builder.split(';')
        for line in lines:
            if len(line)>0 and '=' in line:
                sections=line.split('=')
                line_val = parseJSString(sections[1])
                decryptVal = int(eval(str(decryptVal)+sections[0][-1]+str(line_val)))
        answer = decryptVal + len(urlparse.urlparse(url).netloc)
        http=url.split('//')[0]
        domain1=url.split('//')[1]
        domain=domain1.split('/')[0]
        u=http+'//'+domain
        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (u, jschl, answer)

        if 'type="hidden" name="pass"' in result:
            passval=re.compile('name="pass" value="(.*?)"').findall(result)[0]
            query = '%s/cdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % (u,urllib.quote_plus(passval), jschl, answer)
            xbmc.sleep(4*1000) ##sleep so that the call work
        import net
        net = net.Net()
        final = net.http_POST(query,'',headers=headers)
        if not cj == '':
            net.save_cookies(cj)   
        return final.content
    except:
        traceback.print_exc(file=sys.stdout)
        return urldata

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
