import cookielib
import urllib2
import json
import urllib
import client

def resolve(link,ref):
        out=[]
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
            out+=[{x['key']:url}]
        return out