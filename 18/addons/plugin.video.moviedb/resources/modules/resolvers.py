#Custom vipplaylist by Blazetamer Ported from Mash
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon,main,math,cookielib,os.path
from resources.modules import main
import urlresolver
from addon.common.addon import Addon
#from addon.common.net import Net as net
from addon.common.net import Net
addon_id = 'plugin.video.moviedb'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.moviedb', sys.argv)
ADDON = xbmcaddon.Addon(id='plugin.video.moviedb')
net = Net(http_debug=True)
#========================Alternate Param Stuff=======================
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
favtype = addon.queries.get('favtype', '')
mainimg = addon.queries.get('mainimg', '')
gomode = addon.queries.get('gomode', '')
iconimage = addon.queries.get('iconimage', '')
artwork = addon.queries.get('artwork', '')
art = addon.queries.get('art', '')
fanart = addon.queries.get('fanart', '')
headers = addon.queries.get('headers', '')
loggedin = addon.queries.get('loggedin', '')
header_dict = addon.queries.get('header_dict', '')
#======================== END Alternate Param Stuff=======================
newagent ='Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'
net.set_user_agent(newagent)
#cookiejar = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookiejar = addon.get_profile()
cookiejar = os.path.join(cookiejar,'cookies.lwp')
settings = xbmcaddon.Addon(id='plugin.video.moviedb')

def LogNotify(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def OPEN_URL(url):
  req=urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
  response=urllib2.urlopen(req)
  link=response.read()
  response.close()
  return link





   

               
#########################Blazetamer's VeeHD  Module########################################




def VHDLOGIN():
    username = settings.getSetting('vhd_user')
    password = settings.getSetting('vhd_pass')    
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-Type'] = 'application/x-www-form-urlencoded'
    header_dict['Host'] = 'veehd.com'
    header_dict['Referer'] = 'http://veehd/'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36'    
    form_data = {'ref':'http://veehd.com/login','uname':username, 'pword':password,'submit':'Login', 'terms':'on','remember_me':'on'}
    net.set_cookies(cookiejar)
    login = net.http_POST('http://veehd/', form_data=form_data, headers=header_dict)
    net.save_cookies(cookiejar)
    link = net.http_GET('http://veehd.com').content
    logincheck=re.compile('<h3><a href="/dashboard">My (.+?)</a></h3>').findall(link)
    for nolog in logincheck:
                    print 'Login Check Return is ' + nolog
                    if 'Dashboard' in nolog :
                        LogNotify('Login Failed at VeeHD', 'Check settings', '5000', '')
                        return True
    else:
                        LogNotify('Welcome Back ' + username, 'Enjoy your stay!', '5000', '')
                        net.save_cookies(cookiejar)
                        return False
  

        
def VHDSTARTUP():
        username = settings.getSetting('vhd_user')
        password = settings.getSetting('vhd_pass')
        cookiejar = addon.get_profile()
        cookiejar = os.path.join(cookiejar,'cookies.lwp')
        if username is '' or password is '':
                dialog = xbmcgui.Dialog()
                ok = dialog.ok('Username or Password Not Set', '            Please Choose VeeHD Account Tab and Set')
                if ok:
                        LogNotify('VeeHD Account Tab ', 'Please set Username & Password!', '5000', '')        
                        print 'YOU HAVE NOT SET THE USERNAME OR PASSWORD!'
                        addon.show_settings()
        


        VHDLOGIN()      
                       
        
#************************End Login**************************************
