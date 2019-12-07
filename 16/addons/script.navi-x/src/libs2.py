#############################################################################
#
#   Copyright (C) 2013 Navi-X
#
#   This file is part of Navi-X.
#
#   Navi-X is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   Navi-X is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Navi-X.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import zipfile
import socket
from settings import *
from compiler import parse
from compiler.ast import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

######################################################################
# Description: Playlist item class. 
######################################################################
#class CMediaItem:
#    def __init__(self, id='0', type='unknown', version=plxVersion, name='', thumb='default', URL=''):
#        self.id = id        #identifier
#        self.type = type    #type (playlist, image, video, audio, text)
#        self.version = version #playlist version
#        self.name = name    #name as displayed in list view
#        self.thumb = thumb  #URL to thumb image or 'default'
#        self.URL = URL      #URL to playlist entry
######################################################################
class CMediaItem:
    def __init__(
        self,
        type='unknown',
        version=plxVersion,
        name='',
        description='',
        date='',
        thumb='default',
        icon='default',
        URL='',
        DLloc='',
        player='default',
        processor='',
        playpath='',
        swfplayer='',
        pageurl='',
        referer='',
        agent='',
        background='default',
        rating='',
        infotag='',
        view='default',
        processed=False,
        data={}
    ):
        self.type = type    #(required) type (playlist, image, video, audio, text)
        self.version = version #(optional) playlist version
        self.name = name    #(required) name as displayed in list view
        self.description = description    #(optional) description of this item
        self.date = date    #(optional) release date of this item (yyyy-mm-dd)
        self.thumb = thumb  #(optional) URL to thumb image or 'default'
        self.icon = icon  #(optional) URL to icon image or 'default'
        self.URL = URL      #(required) URL to playlist entry
        self.DLloc = DLloc  #(optional) Download location
        self.player = player #(optional) player core to use for playback
        self.processor = processor #(optional) URL to mediaitem processing server 
        self.playpath = playpath #(optional) 
        self.swfplayer = swfplayer #(optional)
        self.pageurl = pageurl #(optional)
        self.background = background #(optional) background image
        self.rating = rating #(optional) rating value
        self.infotag = infotag
        self.referer = referer #(optional)
        self.agent = agent #(optional)
        self.view = view #(optional) List view option (list, panel)
        self.processed = processed
        self.data = data #(optional) multi-purpose slot for Python dictionaries
               
    ######################################################################
    # Description: Get mediaitem type.
    # Parameters : field: field to retrieve (type or attributes)
    # Return     : -
    ######################################################################
    def GetType(self, field=0):
        index = self.type.find(':')
        if index != -1:
            if field == 0:
                value = self.type[:index]
            elif field == 1:
                value = self.type[index+1:]
            else: #invalid field
                value == ''
        else:
            if field == 0:
                value = self.type
            elif field == 1:
                value = ''
            else: #invalid field
                value == ''

        return value
        
######################################################################
# Description: Playlist item class. 
######################################################################
class CHistorytem:
    def __init__(self, index=0, mediaitem=CMediaItem()):
        self.index = index
        self.mediaitem = mediaitem


######################################################################
# Description: parse FTP URL.
# Parameters : URL, retrieval parameters
# Return     : username, password, host, port, path, file
######################################################################  
class CURLParseFTP:
    def __init__(self, URL):
        #Parse URL according RFC 1738: ftp://user:password@host:port/path 
        #There is no standard Python 2.4 funcion to split these URL's.
        self.username=''
        self.password=''        
        self.port=21
                
        #check for username, password
        index = URL.find('@')
        if index != -1:
            index2 = URL.find(':',6,index)
            if index2 != -1:
                self.username = URL[6:index2]
                print 'user: ' + self.username
                self.password = URL[index2+1:index]
                print 'password: ' + self.password            
            URL = URL[index+1:]
        else:
            URL = URL[6:]
                
        #check for host
        index = URL.find('/')
        if index != -1:
            self.host = URL[:index]
            self.path = URL[index:]
        else:
            self.host = URL
            self.path = ''
                
        #retrieve the port
        index = self.host.find(':')
        if index != -1:
            self.port = int(self.host[index+1:])
            self.host = self.host[:index]
            
        print 'host: ' + self.host    
        print 'port: ' + str(self.port)        
    
        #split path and file
        index = self.path.rfind('/')
        if index != -1:
            self.file = self.path[index+1:]
            self.path = self.path[:index]
        else:
            self.file = ''        
        
        print 'path: ' + self.path
        print 'file: ' + self.file

######################################################################
# Description: Get the file extension of a URL
# Parameters : filename=local path + file name
# Return     : the file extension Excluding the dot
######################################################################
def getFileExtension(filename):
    ext_pos = filename.rfind('.') #find last '.' in the string
    if ext_pos != -1:
        ext_pos2 = filename.rfind('?', ext_pos) #find last '.' in the string
        if ext_pos2 != -1:
            return filename[ext_pos+1:ext_pos2]
        else:
            return filename[ext_pos+1:]
    else:
        return ''

######################################################################
# Description: Get the socket timeout time
# Parameters : -
# Return     : -
######################################################################
def socket_getdefaulttimeout():
    return socket.getdefaulttimeout()

######################################################################
# Description: Set the socket timeout time
# Parameters : time in seconds
# Return     : -
######################################################################
def socket_setdefaulttimeout(url_open_timeout):
#    if platform == "xbox":
    socket.setdefaulttimeout(url_open_timeout)
        
######################################################################
# Description: Trace function for debugging
# Parameters : string: text string to trace
# Return     : -
######################################################################
def Trace(string):
    f = open(RootDir + "trace.txt", "w")
    f.write(string + '\n')
    f.close()


######################################################################
# Description: Display popup error message
# Parameters : string: text string to trace
# Return     : -
######################################################################
def Message(string):
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", string)  
    
######################################################################
# Description: Retrieve the platform Navi-X is running on.
# Parameters : -
# Return     : string containing the platform.
######################################################################  
def get_system_platform():
    platform = "unknown"
    if xbmc.getCondVisibility( "system.platform.linux" ):
        platform = "linux"
    elif xbmc.getCondVisibility( "system.platform.xbox" ):
        platform = "xbox"
    elif xbmc.getCondVisibility( "system.platform.windows" ):
        platform = "windows"
    elif xbmc.getCondVisibility( "system.platform.osx" ):
        platform = "osx"
#    Trace("Platform: %s"%platform)
    return platform

######################################################################
# Description: Retrieve remote information.
# Parameters : URL, retrieval parameters
# Return     : string containing the page contents.
######################################################################  
def getRemote(url,args={}):
    rdefaults={
        'agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
        'referer': '',
        'cookie': '',
        'method': 'get',
        'action': 'read',
        'postdata': '',
        'headers': {}
    }

    for ke in rdefaults:
        try:
            args[ke]
        except KeyError:
            args[ke]=rdefaults[ke]

    if url.find(nxserver_URL) != -1:
        from CServer import nxserver
        if args['cookie']>'':
            args['cookie']=args['cookie']+'; '
        args['cookie']=args['cookie']+'; nxid='+str(nxserver.user_id).strip()
        #if len(str(args['cookie']).strip()) > 0:
        #    args['cookie']=args['cookie']+'; '
        #args['cookie']=args['cookie']+'nxid='+str(nxserver.user_id).strip()
        #print {'cookies':args['cookie']}

    try:
        hdr={'User-Agent':args['agent'], 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Referer':args['referer'], 'Cookie':args['cookie']}
    except:
        print "Unexpected error:", sys.exc_info()[0]

    for ke in args['headers']:
        try:
            hdr[ke]=args['headers'][ke]
        except:
            print "Unexpected error:", sys.exc_info()[0]

    #if len(rdefaults['agent']) > 0:
    try:
        if args['method'] == 'get':
            req=urllib2.Request(url=url, headers=hdr)
        else:
            req=urllib2.Request(url, args['postdata'], hdr)

        cookieprocessor=urllib2.HTTPCookieProcessor()
        opener=urllib2.build_opener(cookieprocessor)
        urllib2.install_opener(opener)
        response=urllib2.urlopen(req)

        cookies={}
        for c in cookieprocessor.cookiejar:
            cookies[c.name]=c.value

        oret={
      	    'headers':response.info(),
      	    'geturl':response.geturl(),
      	    'cookies':cookies
        }
        if args['action'] == 'read':
            oret['content']=response.read()
        
        rkeys=['content','geturl']
        for rkey in rkeys:
            try:
                oret[rkey]
            except KeyError:
                oret[rkey]=''
        rkeys=['cookies','headers']
        for rkey in rkeys:
            try:
                oret[rkey]
            except KeyError:
                oret[rkey]={}

        response.close()
    except IOError:         
        print "*** IOError *** "+str(sys.exc_info()[0])
        oret = {
            'content': str(sys.exc_info()[0]),
      	    'headers':'',
      	    'geturl':'',
      	    'cookies':''
        }
    except ValueError:
        print "*** Value Error *** "+str(sys.exc_info()[0])
        oret = {
            'content': str(sys.exc_info()[0]),
      	    'headers':'',
      	    'geturl':'',
      	    'cookies':''
        }
    
    return oret

######################################################################
# Description: Retrieve NIPL cookies, or "nookies" for specific
#              processor URL. Also handles expiration
# Parameters : URL
# Return     : dictionary containing values of non-expired nookies
######################################################################  
def NookiesRead(url):
    pfilename=ProcessorLocalFilename(url)
    if pfilename=='':
        return {}
    nookiefile=nookieCacheDir+pfilename
    if not os.path.exists(nookiefile):
        return {}
    try:
        f=open(nookiefile, 'r')
    except IOError:
        return {}

    re_parse=re.compile('^(\d+):([^=]+)=(.*)$');
    now=time.time()
    oret={};
    for line in f:
        if line=='':
            continue
        match=re_parse.search(line)
        exp=match.group(1)
        #key='nookie.'+match.group(2)
        key=match.group(2)
        val=match.group(3)
        f_exp=float(exp)
        if f_exp>0 and f_exp<now:
            continue
        oret[key]={'value':val,'expires':exp}
    f.close()
    return oret

######################################################################
# Description: Store nookie for specific processor URL
# Parameters : URL, name, value, expires
# Notes      : expiration format: 0, [n](m|h|d)
#                 0: never, 5m: 5 minutes, 1h: 1 hour, 2d: 2 days
# Return     : -
######################################################################  
def NookieSet(url, name, value, expires):
    pfilename=ProcessorLocalFilename(url)
    if pfilename=='':
        return
    nookiefile=nookieCacheDir+pfilename

    nookies=NookiesRead(url)

    # set expiration timestamp
    if expires=='0':
        int_expires=0
    else:
        now=int(time.time())
        re_exp=re.compile('^(\d+)([mhd])$');
        match=re_exp.search(expires)
        mult={'m':60, 'h':3600, 'd':86400}
        int_expires=now + int(match.group(1)) * mult[match.group(2)]

    # set specified nookie
    nookies[name]={'value':value,'expires':str(int_expires)}

    # compile all non-empty nookies into output string
    str_out=''
    for ke in nookies:
        if nookies[ke]['value']=='':
            continue
        str_out=str_out+nookies[ke]['expires']+':'+ke+'='+nookies[ke]['value']+"\n"
    if str_out>'':
        f=open(nookiefile, 'w')
        f.write(str_out)    
        f.close()
    else:
        os.remove(nookiefile)
    
######################################################################
# Description: Generate unique filename based on processor URL
# Parameters : URL
# Return     : string containing local filename
######################################################################  
def ProcessorLocalFilename(url):
    re_procname=re.compile('([^/]+)$')
    match=re_procname.search(url)
    if match is None:
        return ''

    fn_raw="%X"%(reduce(lambda x,y:x+y, map(ord, url))) + "~" + match.group(1)
    return fn_raw[:42]

######################################################################
# Description: Creates an addon.xml file (needed for Dharma)
# Parameters : name: shortcut name
#            : path: short pathname in the scripts folder
# Return     : -
######################################################################
def CreateAddonXML(name, path):
    sum = 0
    #calculate hash of name
    for i in range(len(name)):
        sum = sum + (ord(name[i]) * i)
    sum_str = str(sum)

    try:
        f=open(initDir + 'addon.xml', 'r')
        data = f.read()
        data = data.splitlines()
        f.close()
        
        f=open(path + 'addon.xml', 'w')
        for m in data:
            line = m
            if m.find("name=") != -1:
                line = line + '"' + name + '"'
            elif m.find("id=") != -1:
                line = line + '"scrip.navi-x' + sum_str + '"' 
            f.write(line + '\n')
        f.close()     
    except IOError:
        pass

 
######################################################################
# Description: Controls the info text label on the left bottom side
#              of the screen.
# Parameters : folder=path to local folder
# Return     : -
######################################################################
def SetInfoText(text='', window=0, setlock=False):
    global win
    global locked
    
    if window != 0:
        win=window
        locked = False
        
    if text == '':
        locked = False
     
    if text != '':
        if locked == False:
            win.setLabel(text)
            win.setVisible(1)
    else:
        win.setVisible(0)
        
    if setlock == True:
        locked = True

        
#retrieve the platform.
platform = get_system_platform()

######################################################################
# Description: Presents a countdown timer
# Parameters : delay_time = int: countdown time in seconds
#              title      = string: dialog label
#              caption    = string: caption
# Return     : True if countdown complete, False if cancelled
######################################################################
def countdown_timer(delay_time,title,caption):
    if delay_time==0:
        print '0-second delay time specified; returning'
        return True

    print 'Waiting '+str(delay_time)+' seconds'    
    if title=='':
        title='Please wait'
    dialog=xbmcgui.DialogProgress()
    dialog.create(title)
    secs=0
    while secs<delay_time:
        secs=secs+1
        dialog.update(int(100*secs/delay_time), caption, str(delay_time-secs)+" seconds remaining")
        xbmc.sleep(1000)
        if(dialog.iscanceled()):
            print 'Wait cancelled'
            return False

    dialog.close()
    print 'Wait finished'
    return True

######################################################################
# Description: Parse Python exception into an error-message string
# Parameters : ex = exception object
# Return     : string [exception type]: [exception message]
######################################################################
def exception_parse(ex):
    print "exc_info:"
    print str(sys.exc_info()[0])
    msg=ex.args[0]
    traw=str(type(ex))
    m=re.match(r"<type 'exceptions\.([^']+)", traw) # Python 2.6+
    if m is None:
        m=re.match(r"exceptions.(\w+)", str(sys.exc_info()[0]) ) # pre Python 2.6
        if m is None:
            intro=traw
        else:
            intro=m.group(1)
    else:
        intro=m.group(1)
    return intro+': '+msg

######################################################################
# Description: Parse string into python dictionary
# Parameters : node or string
# Return     : dictionary
######################################################################
def literal_eval(node_or_string):
    _safe_names = {'None': None, 'True': True, 'False': False}
    if isinstance(node_or_string, basestring):
        try:
            node_or_string = parse(node_or_string, mode='eval')
        except SyntaxError:
            print "!!! literal_eval  syntax error\nCould not parse: "+node_or_string
            return {}
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.node
    def _convert(node):
        if isinstance(node, Const) and isinstance(node.value, (basestring, int, float, long, complex)):
            return node.value
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.nodes))
        elif isinstance(node, List):
            return list(map(_convert, node.nodes))
        elif isinstance(node, Dict):
            return dict((_convert(k), _convert(v)) for k, v in node.items)
        elif isinstance(node, Name):
            if node.name in _safe_names:
                return _safe_names[node.name]
        elif isinstance(node, UnarySub):
            return -_convert(node.expr)
        raise ValueError('malformed string')
    return _convert(node_or_string)

######################################################################
# Description: Transforms XBMC-style URLs with headers incuded into
#              a standard URL + a dictionary of headers
# Parameters : string
# Return     : URL string, headers dictionary
######################################################################
def parse_headers(URL, entry=CMediaItem()):
    headers = { 'User-Agent' : user_agent_default }
    try:
        index = URL.find('|')
    except: index = -1
    if index != -1:
        dtmp = parse_qs(URL[index+1:])
        URL=URL[:index]
        for ke in dtmp:
            headers[ke]=dtmp[ke]

    if entry.agent>'':
        headers['User-Agent']=entry.agent
    
    if entry.referer>'':
        headers['Referer']=entry.referer

    return URL, headers
