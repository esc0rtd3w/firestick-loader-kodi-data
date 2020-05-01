# -*- coding: latin-1 -*-


import regexUtils as re
import urllib
import urlparse


def findJS(data):
    idName = 'f*id'
    jsName = '(.*?\.js)'
    regex = "(?:java)?script[^<]+" + idName + "\s*=\s*[\"']([^\"']+)[\"'][^<]*</script\s*>[^<]*<script[^<]*src=[\"']" + jsName + "[\"']"
    
    jscript = re.findall(data, regex)
    if jscript:
        jscript = filter(lambda x: x[1].find('twitter') == -1, jscript)
        return jscript
    
    return None


def findPHP(data, streamId):
    regex = "document.write\('.*?src=['\"]*(.*?.php\?.*?=).*?['\" ]*.*?\)"
    php = re.findall(data, regex)
    if php:
        return php[0] + streamId
    return None

def findRTMP(url, data):
    #if data.lower().find('rtmp') == -1:
    #    return None
    try:
        text = str(data)
    except:
        text = data
    
    #method 1
    #["'=](http://[^'" ]*.swf[^'" ]*file=([^&"']+)[^'" ]*&streamer=([^"'&]+))
    #streamer=([^&"]+).*?file=([^&"]+).*?src="([^"]+.swf)"
    
    # method 2
    #"([^"]+.swf\?.*?file=(rtmp[^&]+)&.*?id=([^&"]+)[^"]*)"

    sep1 = '[\'"&\? ]'
    sep2 = '(?:[\'"]\s*(?:,|\:)\s*[\'"]|=)'
    value = '([^\'"&]+)'


    method1 = True
    method2 = False
    radius = 400

    playpath = ''
    swfUrl = ''

    rtmp = re.findall(text, sep1 + 'streamer' + sep2 + value)
    if not rtmp:
        tryMethod2 = re.findall(text, sep1 + 'file' + sep2 + value)
        if tryMethod2 and tryMethod2[0].startswith('rtmp'):
            method1 = False
            method2 = True
            rtmp = tryMethod2
            
    if rtmp:
        for r in rtmp:
            
            tmpRtmp = r.replace('/&','').replace('&','')
                        
            idx = text.find(tmpRtmp)
            
            min_idx = 0
            max_idx = len(text) - 1
            
            start = idx-radius
            if start < min_idx:
                start = min_idx
                
            end = idx+radius
            if end > max_idx:
                end = max_idx
            
            area = text[start:end]
            
            clipStart = idx+len(tmpRtmp)
            if clipStart < max_idx:
                text = text[clipStart:]
            if method1:
                playpath = re.findall(area, sep1 + 'file' + sep2 + value)
            if method2:
                playpath = re.findall(area, sep1 + 'id' + sep2 + value)
                if playpath:
                    tmpRtmp = tmpRtmp + '/' + playpath[0]
            
            if playpath:
                swfUrl = re.findall(area, 'SWFObject\([\'"]([^\'"]+)[\'"]')
                if not swfUrl:
                    swfUrl = re.findall(area, sep1 + '([^\'"& ]+\.swf)')
                    if not swfUrl:
                        swfUrl = re.findall(data, sep1 + '([^\'"& ]+\.swf)')

                if swfUrl:
                    finalSwfUrl = swfUrl[0]
                    if not finalSwfUrl.startswith('http'):
                        finalSwfUrl = urlparse.urljoin(url, finalSwfUrl)
                    
                    regex = '://(.*?)/'
                    server = re.findall(tmpRtmp, regex)
                    if server:
                        if server[0].find(':') == -1:
                            tmpRtmp = tmpRtmp.replace(server[0], server[0] + ':1935')
                    
                    return [tmpRtmp, playpath[0], finalSwfUrl]
    
    return None


def getHostName(url):
    scheme = urlparse.urlparse(url)
    if scheme:
        return scheme.netloc.replace('www.','')
    return None


def findFrames(data):
    if data.lower().find('frame') == -1:
        return None
    return re.findall(data, "(frame[^>]*)>")


def findContentRefreshLink(data):
    
    maxLength = 100
    if len(data.replace(' ','')) > maxLength:
        return None 
    
    regex = '0;url=([^\'" ]+)'
    links = re.findall(data, regex)
    if links:
        return links[0]
    else:
        regex = 'window.location\s*=\s*[\'"]([^\'"]+)[\'"]'
        links = re.findall(data, regex)
        if links:
            return links[0]
        
    return None


def findEmbedPHPLink(data):
    regex = '<script type="text/javascript" src="([^"]+\.php\?[^"]+)"\s*>\s*</script>'

    links = re.findall(data, regex)
    if links:
        return links[0]
    
    return None


def findVCods(data):
    regex = "function getURL03.*?sUrl.*?'([^']+)'.*?cod1.*?'([^']+)'.*?cod2.*?'([^']+)'.*?SWFObject\('([^']+)'"
    vcods = re.findall(data, regex)
    if vcods:
        return vcods[0]
    
    return None
        

def findVideoFrameLink(page, data):
    
    minheight=300
    minwidth=300
    
    frames = findFrames(data)
    if not frames:
        return None
    
    iframes = re.findall(data, "(frame[^>]* height=[\"']*(\d+)[\"']*[^>]*>)")

    if iframes:
        for iframe in iframes:

            height = int(iframe[1])
            if height > minheight:
                m = re.findall(iframe[0], "[\"' ]width=[\"']*(\d+[%]*)[\"']*")
                if m:
                    if m[0] == '100%':
                        width = minwidth+1
                    else:
                        width = int(m[0])
                    if width > minwidth:
                        m = re.findall(iframe[0], '[\'"\s]src=["\']*\s*([^"\' ]+)\s*["\']*')
                        if m:
                            link = m[0]
                            if not link.startswith('http://'):
                                up = urlparse.urlparse(urllib.unquote(page))
                                if link.startswith('/'):
                                    link = urllib.basejoin(up[0] + '://' + up[1],link)
                                else:
                                    link = urllib.basejoin(up[0] + '://' + up[1] + '/' + up[2],link)
                            return link.strip()

    # Alternative 1
    iframes = re.findall(data, "(frame[^>]*[\"; ]height:\s*(\d+)[^>]*>)")
    if iframes:
        for iframe in iframes:
            height = int(iframe[1])
            if height > minheight:
                m = re.findall(iframe[0], "[\"; ]width:\s*(\d+)")
                if m:
                    width = int(m[0])
                    if width > minwidth:
                        m = re.findall(iframe[0], '[ ]src=["\']*\s*([^"\' ]+)\s*["\']*')
                        if m:
                            link = m[0]
                            if not link.startswith('http://'):
                                link = urllib.basejoin(page,link)
                            return link.strip()

    # Alternative 2 (Frameset)
    iframes = re.findall(data, '<FRAMESET[^>]+100%[^>]+>\s*<FRAME[^>]+src="([^"]+)"')
    if iframes:
        link = iframes[0]
        if not link.startswith('http://'):
            link = urllib.basejoin(page,link)
        return link.strip()
        
    return None
