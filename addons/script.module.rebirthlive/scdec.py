from __future__ import division
import urllib2, base64
import urllib2,urllib,cgi, re,traceback,sys,os,json
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        print url
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Accept-Encoding','gzip')

    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;
def Colored(text = '', colorid = '', isBold = False):
    if colorid == 'ZM':
        color = 'FF11b500'
    elif colorid == 'EB':
        color = 'FFe37101'
    elif colorid == 'bold':
        return '[B]' + text + '[/B]'
    else:
        color = colorid
        
    if isBold == True:
        text = '[B]' + text + '[/B]'
    return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def gettext(htmltxt):
    import re
    jsurl=re.findall('(http.*?smartcric.*?\.js)',htmltxt)[-1]
    print jsurl
    jsdata=getUrl(jsurl)
    if jsdata.strip().startswith('var _'):
        return gettext2(jsdata)
    import re
    try:
        anchorreg='parseInt\((.*?)\)'
        ancdata=re.findall(anchorreg,jsdata)[0]
        parsedata=re.findall('\[([0-9,\,]*)\];var %s=(.*?);.+?[^(parse)]parseInt\((.*?)\)'%ancdata,jsdata)[0]

        maincode=parsedata[0]
        mathdata=parsedata[1]
        s= '[%s]'%maincode;
        s=eval(s)
        #s=[47, 42]
        ss=[]
        MathData = eval(mathdata)
        for a in s:
            try:
                ss+=chr(a-int(MathData))
            except: 
                print 'error'
        print repr(  ''.join(ss))
    except: 
        ss=[jsdata]
    return 'v1',''.join(ss)

def gettext2(jstext):
    import re
    regs="var _.*?(\[.*?\])"
    vals=re.findall(regs,jstext)[0]
    d1= '\n'.join(eval(vals))
    varname=re.findall(";var (.*?)=",jstext)[0]
    d2=re.findall(";%s=(.*?);"%varname,jstext)[0]
    return 'v2',d1,d2
    
def getlinks():    
    ret=[]
    import random,math
    rnd1=str(int(math.floor(random.random()*5) ))
    rnd2=str(int(math.floor(random.random()*1000000) ))
    rnd3=str(int(math.floor(random.random()*1000000) ))
    headers=[('Cookie', '_ga=GA1.%s.%s.%s'%(rnd1,rnd2,rnd3)),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('User-Agent','Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')]
    link = getUrl(base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuaXMv'),headers=headers)

    jsdata=gettext(link)
#    print link
    if jsdata[0]=='v1':
        patt='performGet\(\'(.+)\''
        match_url =re.findall(patt,jsdata[1])[0]
    else:
        patt='(http.*?live/)'
        match_url =re.findall(patt,jsdata[1])[0]        
    #match_url='http://webaddress:8087/mobile/channels/live/'
    channeladded=False
    patt_sn='sn = "(.*?)"'
    patt_pk='showChannels.?\([\'"](.*?)[\'"]'
    try:
        match_sn =re.findall(patt_sn,link)[0]
        match_pk =re.findall(patt_pk,link)[0]
        print match_pk
        match_pk=smpk(match_pk,jsdata)
        print 'match_pk',match_pk
        ref=[('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A452 Safari/601.1'),
            ('Referer','http://smartcric.is/')]
        #lburl=re.findall('(http.*?loadbalancer)',link)[0]
        #fms=getUrl(lburl,headers=ref).split('=')[1]
        #sourcelb=lburl.split('/')[2].split(':')[0]
        #match_url=match_url.replace('webaddress',sourcelb)
        final_url=  match_url+   match_sn
        headers=[('Referer', base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuaXMvJw==')),('Origin', base64.b64decode('aHR0cDovL3d3dy5zbWFydGNyaWMuaXM=')),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),('User-Agent','Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3')]

        link = getUrl(final_url,headers=headers)

        sources = json.loads(link)
        #addDir('Refresh' ,'Live' ,144,'')
        for source in sources["channelsList"]:
            if 1==1:#ctype=='liveWMV' or ctype=='manual':
#                print source
                curl=''
                cname=source["caption"]
                fms=source["fmsUrl"]
#                print curl
                #if ctype<>'': cname+= '[' + ctype+']'
                #ret.append( (cname ,curl ,-1,'', False, True,isItFolder=False)		#name,url,mode,icon


                
                if 'streamsList' in source and source["streamsList"] and len(source["streamsList"])>0:
                    for s in source["streamsList"]:
                        qname=s["caption"]
                        curl=s["streamName"]
                        streamid=str(s["streamId"])
                        
                        curl1="http://"+fms+":8088/mobile/"+curl+"/playlist.m3u8?id="+streamid+"&pk="+match_pk+'|Referer=http://www.smartcric.is/&User-Agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3';
                        ret.append((cname+' '+Colored(qname ,'red',True) ,curl1 ,15))		#name,url,mode,icon
                        #curl1="rtsp://"+"206.190.140.164"+":1935/mobile/"+curl+"?key="+match_sn+match_pk;
                        #curl1="rtsp://"+fms+":1935/mobile/"+curl+"?id="+streamid+"&key="+match_sn+match_pk;
                        #addDir('    -'+cname +" (rtsp)",curl1 ,15,'', False, True,isItFolder=False)		#name,url,mode,icon

                        channeladded=True
                else:
                    
                    curl=''
                    ret.append((cname+Colored(' NOT AVAILABLE YET','red',True),curl ,-1))
    except: traceback.print_exc(file=sys.stdout)
    return ret
    
    
def smpk(frompk, jsdata):
    if jsdata[0]=='v2':
        return smpk2(frompk,jsdata);
    varname='oh'
    try:
        
        refind='hash.*?(oh.*)'
        jsline=re.findall(refind, jsdata)[0].split(' ')
    except : 
        varname=re.findall('showChannels.?.?\((.*?)\)',jsdata[1])[0]
        refind='\=.?(%s.*)'%varname
        print jsdata[1]
        jsline=re.findall(refind, jsdata[1])[0].split(' ')
    oh=''
    oh=frompk
    fv=[]
    
    for ln in jsline:
        if 'substring' in ln:
            ln=ln.replace('%s.substring('%varname,'oh[')
            ln=ln.replace(',',':')
            ln=ln.replace(')',']')
        if '%s.length'%varname in ln:
            ln=ln.replace('%s.length'%varname,'len(oh)')
        fv.append(ln.strip().replace(';',''))
    print fv
    s=' '.join(fv)
    print s
    return eval(s)
    
def smpk2(frompk, jsdata):
    #refind='hash.*?(oh.*)'
    jsline=jsdata[2].split('+');#re.findall(refind, jsdata)[0].split(' ')
    
    oh=''
    oh=frompk
    fv=[]
    print jsline
    for ln in jsline:
        if len(re.findall('(\([0-9]+?,[0-9]+?\))',ln))>0:
            ln='oh['+ln.split('(')[1].split(')')[0]+']'
            ln=ln.replace(',',':')
        if len(re.findall('(\([0-9]+?,_.*?\])',ln))>0:
            ln='oh['+ln.split('(')[1].split(',')[0]+':]'
        fv.append(ln.strip().replace(';',''))
    print fv
    s='+'.join(fv)
    print s
    return eval(s)     