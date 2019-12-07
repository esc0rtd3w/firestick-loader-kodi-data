import urlparse
import re
import decryptionUtils


def remove_referer(url):
    return re.sub("referer=.+?(?:&|$)","",url).rstrip('?').rstrip('&')


def prepare(netloc):
    netloc = netloc.replace('www.','').replace('config.','')
    netloc = re.sub(r'www\d+.','',netloc)
    return netloc

def manual_url_fix(url):

    try:    url = url.replace('wizhdsports.com','wizhdsports.sx')
    except: pass
    try:
        url = url.replace('navixsport.com/sport.php','navixsport.com/m/sport.php')
        if 'prmobiles' in url: return
        url = remove_referer(url)
    except:
        pass
    try:
        import HTMLParser
        h = HTMLParser.HTMLParser()
        url = h.unescape(url)
    except:
        pass
    return url

def manual_html_fix(url,html, headers):
    
    
    if 'livetv.sx' in url or 'shadow' in url or 'futandres' in url and 'goto/' not in url:
        import requests
        s = requests.Session()
        s.headers.update(headers)
        html = s.get(url).text
        try:
            if 'zonasports' not in url:
                html = decryptionUtils.doDemystify(html)

        except: pass


    
    return html

def manual_fix(url,ref):
    netlock = urlparse.urlparse(url).netloc
    url = url.replace('../','')
    if url.startswith('//'):    url = 'http:' + url
    if netlock == 'ibrod.tv':
        url=url.replace('ibrod.tv','www.ibrod.tv')

    if 'http' not in url:
        if url !='ifi.html':
            uri = 'http://' + urlparse.urlparse(ref).netloc + '/' + url
        else:
            uri = 'http://' + urlparse.urlparse(ref).netloc + '/' + urlparse.urlparse(ref).path + '/' + url
    else:
        uri = url

    if 'referer=' not in url:
        uri = add_args(uri,{'referer':ref})
    return uri



def add_args(url, arg_dict):
    import urllib, urlparse

    try:
        from urlparse import parse_qs
    except ImportError:
        from cgi import parse_qs

    url_parts = urlparse.urlparse(url)

    qs_args = parse_qs(url_parts[4])
    qs_args.update(arg_dict)

    new_qs = urllib.urlencode(qs_args, True)

    return urlparse.urlunparse(list(url_parts[0:4]) + [new_qs] + list(url_parts[5:]))




def replace_vars(text):
    vars = re.findall('\s*(\w+)\s*=\s*[\'\"](.+?)[\'\"]',text)

    #remove var from string
    for v in vars:
        text = re.sub('var\s*%s=\s*[\"\']%s[\"\']'%(v[0],v[1]),'',text)


    var_dict = {}
    for v in vars:
        var_dict[v[0]] = v[1]
    #replace var with values
    for v in vars:
        text = text.replace(v[0],'"%s"'%v[1])

    for v in vars:
        if '+' in v[1]:
            ss = v[1].rstrip('+').replace('"+','').split('+')
            sg = v[1].rstrip('+').replace('"+','')
            for s in ss:
                try:
                    sg = sg.replace(s, var_dict[s])
                except:
                    pass
            
                var_dict[v[0]]=sg.replace('+','')
        

    for i in range(100):
        for v in vars: text = text.replace(" %s " % v[0], ' %s '%var_dict[v[0]])
    
    for i in range(100):
        for v in var_dict.keys(): text = text.replace("'%s'" % v, var_dict[v])
        for v in var_dict.keys(): text = text.replace("(%s)" % v, "(%s)" % var_dict[v])


    return text