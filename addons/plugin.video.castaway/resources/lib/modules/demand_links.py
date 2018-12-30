import re
import convert
import client
import control
from log_utils import log

def links(url,base,img,icon):
    if base not in url:
        url = base + url
    ref = url
    out = []
    html = client.request(url)

    html = convert.unescape(html.decode('utf-8'))
    dailys = re.findall('src=[\"\'](//(?:www.)?dailymotion.com/embed/video/[^\"\']+)[\"\']',html)
    vks = re.findall('src=[\"\'](//(?:www.)?vk.com/video_ext.php[^\"\']+)[\"\']',html)
    gvid720 = re.findall('src=[\"\'](https?://.+?google.+?/[^\"\']+)" type=[\"\']video/mp4[\"\'] data-res=[\"\']720p[\"\']',html)
    gvid360 = re.findall('src=[\"\'](https?://.+?google.+?[^\"\']+)" type=[\"\']video/mp4[\"\'] data-res=[\"\']360p[\"\']',html)
    mailru = re.findall('(https?://(?:www.)?videoapi.my.mail.ru/videos/[^\"\']+)[\"\']',html)
    opnld = re.findall('(https?://(?:www.)?openload.co/[^\"\']+)[\"\']',html)
    uptstrm = re.findall('(https?://(?:www(?:[\d+])?.)?uptostream.com[^\"\']+)[\"\']',html)
    veevr = re.findall('(https?://(?:www.)?veevr.com[^\"\']+)[\"\']',html)
    plywr = re.findall('(//config.playwire.com/[^\"\']+)[\"\']',html)
    speedvideo = re.findall('(https?://(?:www.)?speedvideo.net/[^\"\']+)[\"\']',html)
    videowood = re.findall('(https?://(?:www.)?videowood.tv/video/[^\"\']+)[\"\']',html)
    vshare = re.findall('(https?://(?:www.)?vshare.io/[^\"\']+)[\"\']',html)
    youtube = re.findall('(https?://(?:www.)?youtu(?:be)?.(?:be|com)/embed/[^\"\']+)[\"\']',html)
    filehoot = re.findall('(https?://(?:www.)?filehoot.com[^\"\']+)[\"\']',html)
    torrent = re.findall('(https?://(?:www.)?userscloud.com[^\"\']+)[\"\']',html)
    urls = []

    i = 0
    for v in plywr:
        i+=1
        title = 'Playwire video %s'%i
        url = v 
        if url not in urls:
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in veevr:
        i+=1
        url = v
        from resources.lib.resolvers import veevr
        urlx = veevr.resolve(url)
        
        for url in urlx:
            if url[0] not in urls:
                title = 'Veevr video %s'%url[1].replace('<sup>HD</sup>','')
                out.append((title,url[0],control.icon_path(icon)))
                urls.append(url[0])

    i = 0
    for v in uptstrm:
        from resources.lib.resolvers import uptostream
        urlx =  uptostream.resolve(v)
        i+=1
        for u in urlx:
            q = u[1]
            title = 'Uptostream video n.%s %s'%(i,q)
            url = u[0] 
            if url not in urls:
                out.append((title,url,control.icon_path(icon)))
                urls.append(url)

    i = 1
    for v in dailys:
        
        title = 'Dailymotion video %s'%i
        url = v
        if url not in urls:
            i+=1
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in vks:
        i+=1
        title = 'VK.com video %s'%i
        url = v
        if url not in urls:
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in gvid720:
        i+=1
        title = 'GVIDEO video %s 720p'%i
        url = v
        if url not in urls:
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in gvid360:
        i+=1
        title = 'GVIDEO video 360p'%i
        url = v
        if url not in urls:
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 1
    for v in opnld:
        
        title = 'Openload video %s'%i
        url = v.replace('/embed/','/f/').rstrip('/')
        if url not in urls:
            i+=1
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in speedvideo:
        i+=1
        title = 'Speedvideo video %s'%i
        url = v
        if url not in urls:
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)
    i = 0
    for v in videowood:
        i+=1
        title = 'Videowood video %s'%i
        url = v
        if url not in urls:
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)
    

    i = 0
    for v in vshare:
        i+=1
        url = v
        title = 'vshare.io video %s'%i
        if url not in urls:

            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in youtube:
        i+=1
        url = v
        title = 'YouTube video %s'%i
        if url not in urls:

            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in filehoot:
        i+=1
        url = v
        title = 'Filehoot video %s'%i
        if url not in urls:

            out.append((title,url,control.icon_path(icon)))
            urls.append(url)

    i = 0
    for v in torrent:
        i+=1
        url = v
        title = 'Torrent video %s'%i
        if url not in urls:
            url = url + '?referer=%s'%ref
            out.append((title,url,control.icon_path(icon)))
            urls.append(url)


    i = 0
    for v in mailru:
        link = v
        i+=1
        title = 'Mail.ru video %s'%i
        link = link.replace('https://videoapi.my.mail.ru/videos/embed/mail/','http://videoapi.my.mail.ru/videos/mail/')
        link = link.replace('html','json')
        cookieJar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar), urllib2.HTTPHandler())
        conn = urllib2.Request(link)
        connection = opener.open(conn)
        f = connection.read()
        connection.close()
        js = json.loads(f)
        for cookie in cookieJar:
            token = cookie.value
        js = js['videos']
        for x in js:
            url = x['url'] + '|%s'%(urllib.urlencode({'Cookie':'video_key=%s'%token, 'User-Agent':client.agent(), 'Referer':ref} ))
            title = 'Mail.ru video ' + x['key']
            if url not in urls:
                out.append((title,url,control.icon_path(icon)))
                urls.append(url)
    log(out)
    return out

def resolve(url):
    if 'uptostream' in url:
        return url
    if 'veevr'in url:
        return url
    if 'playwire' in url:
        from resources.lib.resolvers import playwire
        return playwire.resolve(url)
    if 'userscloud' in url:
        from resources.lib.resolvers import userscloud
        return userscloud.resolve(url)


    import urlresolver
    return urlresolver.resolve(url)