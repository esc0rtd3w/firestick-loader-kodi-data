# -*- coding: utf-8 -*-
import xbmc , xbmcaddon , xbmcgui , xbmcplugin , urllib , urllib2 , os , re , sys , datetime , urlresolver , random , liveresolver , base64 , pyxbmct , glob , net
from resources . lib . common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources . lib import mamahd
from resources . lib import crickfree
from resources . lib import bigsports
from resources . lib import hergundizi
from resources . lib import tv
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.ukturk'
Oo0Ooo = Addon ( OO0o , sys . argv )
O0O0OO0O0O0 = xbmcaddon . Addon ( id = OO0o )
iiiii = xbmc . translatePath ( O0O0OO0O0O0 . getAddonInfo ( 'profile' ) )
ooo0OO = xbmc . translatePath ( 'special://home/addons/' ) + '/*.*'
II1 = xbmc . translatePath ( 'special://home/addons/' )
O00ooooo00 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'fanart.jpg' ) )
IIi1IiiiI1Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'icon.png' ) )
I11i11Ii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o , 'next.png' ) )
oO00oOo = O0O0OO0O0O0 . getSetting ( 'adult' )
OOOo0 = O0O0OO0O0O0 . getSetting ( 'password' )
Oooo000o = int ( O0O0OO0O0O0 . getSetting ( 'count' ) )
IiIi11iIIi1Ii = O0O0OO0O0O0 . getSetting ( 'enable_meta' )
Oo0O = xbmc . translatePath ( 'special://home/userdata/addon_data/' + OO0o )
IiI = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'UKTurk.db' ) )
ooOo = 'http://ukturk.offshorepastebin.com/ukturk2.jpg'
Oo = 'https://www.googleapis.com/youtube/v3/search?q='
o0O = '&regionCode=US&part=snippet&hl=en_US&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&type=video&maxResults=50'
IiiIII111iI = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId='
IiII = '&maxResults=50&key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA'
iI1Ii11111iIi = open ( IiI , 'a' )
iI1Ii11111iIi . close ( )
net = net . Net ( )
if 41 - 41: I1II1
def Ooo0OO0oOO ( ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 if not os . path . exists ( Oo0O ) :
  os . mkdir ( Oo0O )
 oooO0oo0oOOOO = O0oO ( ooOo )
 o0oO0 = re . compile ( '<index>(.+?)</index>' ) . findall ( oooO0oo0oOOOO ) [ 0 ]
 oooO0oo0oOOOO = O0oO ( o0oO0 )
 oo00 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 for o00 , Oo0oO0ooo , o0oOoO00o in oo00 :
  if not 'XXX' in o00 :
   i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
  if 'XXX' in o00 :
   if oO00oOo == 'true' :
    if OOOo0 == '' :
     oOOoo00O0O = xbmcgui . Dialog ( )
     i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'Lets Go' )
     if i1111 == 1 :
      i11 = xbmc . Keyboard ( '' , 'Set Password' )
      i11 . doModal ( )
      if ( i11 . isConfirmed ( ) ) :
       I11 = i11 . getText ( )
       O0O0OO0O0O0 . setSetting ( 'password' , I11 )
      i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
   if oO00oOo == 'true' :
    if OOOo0 <> '' :
     i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
 i1 ( 'Favourites' , IiI , 15 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20favourites.jpg' , O00ooooo00 )
 i1 ( 'Search' , 'url' , 5 , 'http://ukturk.offshorepastebin.com/UKTurk/thumbs/new/Uk%20turk%20thumbnails%20search.jpg' , O00ooooo00 )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 98 - 98: I1111 * o0o0Oo0oooo0 / I1I1i1 * oO0 / IIIi1i1I
def OOoOoo00oo ( url ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'yes' )
 iiI11 = None
 file = open ( IiI , 'r' )
 iiI11 = file . read ( )
 oo00 = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( iiI11 )
 for OOooO in oo00 :
  OOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( OOooO )
  for o00 , url , o0oOoO00o in OOoO00o :
   if '.txt' in url :
    i1 ( o00 , url , 1 , o0oOoO00o , O00ooooo00 )
   else :
    II111iiii ( o00 , url , 2 , o0oOoO00o , O00ooooo00 )
    if 48 - 48: I1Ii . IiIi1Iii1I1 - O0O0O0O00OooO % Ooooo % i1iIIIiI1I - OOoO000O0OO
def iiI1IiI ( name , url , iconimage ) :
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 II = '<FAV><item>\n<title>' + name + '</title>\n<link>' + url + '</link>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n</item></FAV>\n'
 iI1Ii11111iIi = open ( IiI , 'a' )
 iI1Ii11111iIi . write ( II )
 iI1Ii11111iIi . close ( )
 if 57 - 57: ooOoo0O
def OooO0 ( name , url , iconimage ) :
 iiI11 = None
 file = open ( IiI , 'r' )
 iiI11 = file . read ( )
 II11iiii1Ii = ''
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( iiI11 )
 for OOoO00o in oo00 :
  II = '\n<FAV><item>\n' + OOoO00o + '</item>\n'
  if name in OOoO00o :
   II = II . replace ( 'item' , ' ' )
  II11iiii1Ii = II11iiii1Ii + II
 file = open ( IiI , 'w' )
 file . truncate ( )
 file . write ( II11iiii1Ii )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 70 - 70: O00 / i1I1i1Ii11 . IIIIII11i1I - o0o0OOO0o0 % ooOOOo0oo0O0
def o0 ( name , url , iconimage , fanart ) :
 I11II1i = IIIII ( name )
 O0O0OO0O0O0 . setSetting ( 'tv' , I11II1i )
 oooO0oo0oOOOO = O0oO ( url )
 ooooooO0oo ( oooO0oo0oOOOO )
 if '/UKTurk/TurkishTV.txt' in url : IIiiiiiiIi1I1 ( )
 if '/UKTurk/tv shows/Index.txt' in url : I1IIIii ( )
 if 'Index' in url :
  oOoOooOo0o0 ( url )
 if 'XXX' in name : OOOO ( oooO0oo0oOOOO )
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 Oooo000o = str ( len ( oo00 ) )
 O0O0OO0O0O0 . setSetting ( 'count' , Oooo000o )
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 for OOooO in oo00 :
  try :
   if '<sportsdevil>' in OOooO : OOO00 ( OOooO , url , iconimage )
   elif '<iptv>' in OOooO : iiiiiIIii ( OOooO )
   elif '<Image>' in OOooO : O000OO0 ( OOooO )
   elif '<text>' in OOooO : I11iii1Ii ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
   elif '<redirect>' in OOooO : REDIRECT ( OOooO )
   elif '<oktitle>' in OOooO : O000oo0O ( OOooO )
   elif '<dl>' in OOooO : OOOOi11i1 ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
   else : IIIii1II1II ( OOooO , url , iconimage )
  except : pass
  if 42 - 42: OoO0O0o0Ooo + i1iIIIiI1I
def I1IIIii ( ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 Oo0oO0ooo = 'https://watchseries-online.pl/last-350-episodes'
 i1 ( 'New Episodes of TV Shows' , Oo0oO0ooo , 23 , 'http://ukturk.offshorepastebin.com/UKTurk/tv%20shows/Uk turk thumbnails new episodes tv shows1.jpg' , O00ooooo00 , description = '' )
 if 56 - 56: OoO0O0o0Ooo
def o0OO00oO ( url ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 I11i1I1I = tv . TVShows ( url )
 oo00 = re . compile ( '<start>(.+?)<sep>(.+?)<end>' ) . findall ( str ( I11i1I1I ) )
 for o00 , url in oo00 :
  II111iiii ( o00 , url , 24 , o0oOoO00o , O00ooooo00 , description = '' )
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 83 - 83: i1iIIIiI1I / OoO0O0o0Ooo
def iIIIIii1 ( name , url , iconimage ) :
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 oo000OO00Oo = [ 'vidto.me' , 'gorillavid.in' , 'vidzi.tv' , 'rapidvideo.ws' ]
 Oooo000o = [ ]
 O0OOO0OOoO0O = [ ]
 O00Oo000ooO0 = tv . Stream ( url )
 OoO0O00 = 1
 for oooO0oo0oOOOO in O00Oo000ooO0 :
  if urlresolver . HostedMediaFile ( oooO0oo0oOOOO ) . valid_url ( ) :
   for IIiII in oo000OO00Oo :
    if IIiII in oooO0oo0oOOOO :
     Oooo000o . append ( 'Link ' + str ( OoO0O00 ) )
     O0OOO0OOoO0O . append ( oooO0oo0oOOOO )
     OoO0O00 = OoO0O00 + 1
 oOOoo00O0O = xbmcgui . Dialog ( )
 o0ooOooo000oOO = oOOoo00O0O . select ( 'Choose a link..' , Oooo000o )
 if o0ooOooo000oOO < 0 : quit ( )
 url = O0OOO0OOoO0O [ o0ooOooo000oOO ]
 Oo0oOOo ( name , url , iconimage )
 if 58 - 58: oO0 * ooOoo0O * i1iIIIiI1I / ooOoo0O
def IIiiiiiiIi1I1 ( ) :
 Oo0oO0ooo = 'http://www.hergundizi.net'
 i1 ( '[COLOR gold]**** Yerli Yeni Eklenenler Diziler ****[/COLOR]' , Oo0oO0ooo , 21 , o0oOoO00o , O00ooooo00 , description = '' )
 if 75 - 75: OOoO000O0OO
def I1III ( url ) :
 I11i1I1I = hergundizi . TVShows ( url )
 oo00 = re . compile ( '<start>(.+?)<sep>(.+?)<sep>(.+?)<end>' ) . findall ( str ( I11i1I1I ) )
 for o00 , url , o0oOoO00o in oo00 :
  if not 'dızlar' in o00 :
   II111iiii ( o00 , url , 22 , o0oOoO00o , O00ooooo00 , description = '' )
 try :
  OO0O0OoOO0 = re . compile ( '<np>(.+?)<np>' ) . findall ( str ( I11i1I1I ) ) [ 0 ]
  i1 ( 'Next Page>>' , OO0O0OoOO0 , 21 , I11i11Ii , O00ooooo00 , description = '' )
 except : pass
 xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 if 10 - 10: o0o0Oo0oooo0 % I1111
def O00o0O00 ( name , url , iconimage ) :
 ii111111I1iII = hergundizi . Parts ( url )
 O00ooo0O0 = len ( ii111111I1iII )
 if O00ooo0O0 > 1 :
  Oooo000o = [ ]
  OoO0O00 = 1
  for i1iIi1iIi1i in ii111111I1iII :
   Oooo000o . append ( 'Part ' + str ( OoO0O00 ) )
   OoO0O00 = OoO0O00 + 1
   oOOoo00O0O = xbmcgui . Dialog ( )
  o0ooOooo000oOO = oOOoo00O0O . select ( 'Choose a Part..' , Oooo000o )
  if o0ooOooo000oOO < 0 : quit ( )
  url = ii111111I1iII [ o0ooOooo000oOO ]
 I1I1iIiII1 = hergundizi . Stream ( url )
 Oo0oOOo ( name , I1I1iIiII1 , iconimage )
 if 4 - 4: OoO0O0o0Ooo + I1II1 * ooOoo0O
def I1IIiiIiii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<scraper>(.+?)</scraper>' ) . findall ( item ) [ 0 ]
 i1 ( o00 , Oo0oO0ooo , 20 , o0oOoO00o , O00ooooo00 )
 if 55 - 55: I1Ii + I1111 / O0O0O0O00OooO * OOoO000O0OO - i11iIiiIii - i1I1i1Ii11
def ii1ii1ii ( url , iconimage ) :
 II = url + '.scrape()'
 oooO0oo0oOOOO = eval ( II )
 oo00 = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 Oooo000o = str ( len ( oo00 ) )
 O0O0OO0O0O0 . setSetting ( 'count' , Oooo000o )
 O0O0OO0O0O0 . setSetting ( 'fav' , 'no' )
 for OOooO in oo00 :
  try :
   if '<sportsdevil>' in OOooO : OOO00 ( OOooO , url , iconimage )
   elif '<iptv>' in OOooO : iiiiiIIii ( OOooO )
   elif '<Image>' in OOooO : O000OO0 ( OOooO )
   elif '<text>' in OOooO : I11iii1Ii ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
   elif '<redirect>' in OOooO : REDIRECT ( OOooO )
   elif '<oktitle>' in OOooO : O000oo0O ( OOooO )
   elif '<dl>' in OOooO : OOOOi11i1 ( OOooO )
   elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO , iconimage )
   else : IIIii1II1II ( OOooO , url , iconimage )
  except : pass
  if 91 - 91: o0o0OOO0o0
def OOOOi11i1 ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<dl>(.+?)</dl>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiIii ( o00 , Oo0oO0ooo , 19 , o0oOoO00o , O00ooooo00 )
 if 79 - 79: o0o0Oo0oooo0 / I1II1
def OO0OoO0o00 ( name , url ) :
 ooOO0O0ooOooO = url . split ( '/' ) [ - 1 ]
 if ooOO0O0ooOooO == 'latest' : ooOO0O0ooOooO = 'AceStreamEngine.apk'
 import downloader
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOOo00O00oOo = xbmcgui . DialogProgress ( )
 iiIIIi = oOOoo00O0O . browse ( 0 , 'Select folder to download to' , 'myprograms' )
 ooo00OOOooO = os . path . join ( iiIIIi , ooOO0O0ooOooO )
 oOOOo00O00oOo . create ( 'Downloading' , '' , '' , 'Please Wait' )
 downloader . download ( url , ooo00OOOooO , oOOOo00O00oOo )
 oOOOo00O00oOo . close ( )
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOoo00O0O . ok ( 'Download complete' , 'Please install from..' , iiIIIi )
 if 67 - 67: O00 * OOoO000O0OO * i1iIIIiI1I + ooOoo0O / I1I1i1
def O000oo0O ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 I1I111 = re . compile ( '<oktitle>(.+?)</oktitle>' ) . findall ( item ) [ 0 ]
 Oo00oo0oO = re . compile ( '<line1>(.+?)</line1>' ) . findall ( item ) [ 0 ]
 IIiIi1iI = re . compile ( '<line2>(.+?)</line2>' ) . findall ( item ) [ 0 ]
 i1IiiiI1iI = re . compile ( '<line3>(.+?)</line3>' ) . findall ( item ) [ 0 ]
 i1iIi = '##' + I1I111 + '#' + Oo00oo0oO + '#' + IIiIi1iI + '#' + i1IiiiI1iI + '##'
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiIii ( o00 , i1iIi , 17 , o0oOoO00o , O00ooooo00 )
 if 68 - 68: i11iIiiIii % i1iIIIiI1I + i11iIiiIii
def iii ( name , url ) :
 II1I = re . compile ( '##(.+?)##' ) . findall ( url ) [ 0 ] . split ( '#' )
 oOOoo00O0O = xbmcgui . Dialog ( )
 oOOoo00O0O . ok ( II1I [ 0 ] , II1I [ 1 ] , II1I [ 2 ] , II1I [ 3 ] )
 if 84 - 84: o0o0OOO0o0 . i11iIiiIii . o0o0OOO0o0 * i1iIIIiI1I - O00
def I11iii1Ii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 i1iIi = re . compile ( '<text>(.+?)</text>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 iiIii ( o00 , i1iIi , 9 , o0oOoO00o , O00ooooo00 )
 if 42 - 42: i11iIiiIii
def I11i1iIII ( name , url ) :
 iiIiI = O0oO ( url )
 o00oooO0Oo ( name , iiIiI )
 if 78 - 78: i1I1i1Ii11 % ooOOOo0oo0O0 + i1iIIIiI1I
def O000OO0 ( item ) :
 OOooOoooOoOo = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item )
 if len ( OOooOoooOoOo ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  o0OOOO00O0Oo = re . compile ( '<Image>(.+?)</Image>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  o0OOOO00O0Oo = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
  iiIii ( o00 , o0OOOO00O0Oo , 7 , o0oOoO00o , O00ooooo00 )
 elif len ( OOooOoooOoOo ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  ii = ''
  for o0OOOO00O0Oo in OOooOoooOoOo :
   o0oOoO00o = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   o0OOOO00O0Oo = o0OOOO00O0Oo . replace ( 'http://imgur.com/' , 'http://i.imgur.com/' ) + '.jpg'
   ii = ii + '<Image>' + o0OOOO00O0Oo + '</Image>'
  oOooOOOoOo = Oo0O
  o00 = IIIII ( o00 )
  i1Iii1i1I = os . path . join ( os . path . join ( oOooOOOoOo , '' ) , o00 + '.txt' )
  if not os . path . exists ( i1Iii1i1I ) : file ( i1Iii1i1I , 'w' ) . close ( )
  OOoO00 = open ( i1Iii1i1I , "w" )
  OOoO00 . write ( ii )
  OOoO00 . close ( )
  iiIii ( o00 , 'image' , 8 , o0oOoO00o , O00ooooo00 )
  if 40 - 40: IIIi1i1I * i1I1i1Ii11 + ooOoo0O % IIIIII11i1I
def iiiiiIIii ( item ) :
 o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
 o0oOoO00o = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
 Oo0oO0ooo = re . compile ( '<iptv>(.+?)</iptv>' ) . findall ( item ) [ 0 ]
 i1 ( o00 , Oo0oO0ooo , 6 , o0oOoO00o , O00ooooo00 )
 if 74 - 74: OOoO000O0OO - I1Ii + o0o0Oo0oooo0 + ooOOOo0oo0O0 / O0O0O0O00OooO
def i1I1iI1iIi111i ( url , iconimage ) :
 oooO0oo0oOOOO = O0oO ( url )
 iiIi1IIi1I = re . compile ( '^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)$' , re . I + re . M + re . U + re . S ) . findall ( oooO0oo0oOOOO )
 o0OoOO000ooO0 = [ ]
 for o0o0o0oO0oOO , o00 , url in iiIi1IIi1I :
  ii1Ii11I = { "params" : o0o0o0oO0oOO , "name" : o00 , "url" : url }
  o0OoOO000ooO0 . append ( ii1Ii11I )
 list = [ ]
 for o00o0 in o0OoOO000ooO0 :
  ii1Ii11I = { "name" : o00o0 [ "name" ] , "url" : o00o0 [ "url" ] }
  iiIi1IIi1I = re . compile ( ' (.+?)="(.+?)"' , re . I + re . M + re . U + re . S ) . findall ( o00o0 [ "params" ] )
  for iiOOooooO0Oo , OO in iiIi1IIi1I :
   ii1Ii11I [ iiOOooooO0Oo . strip ( ) . lower ( ) . replace ( '-' , '_' ) ] = OO . strip ( )
  list . append ( ii1Ii11I )
 for o00o0 in list :
  if '.ts' in o00o0 [ "url" ] : iiIii ( o00o0 [ "name" ] , o00o0 [ "url" ] , 2 , iconimage , O00ooooo00 )
  else : II111iiii ( o00o0 [ "name" ] , o00o0 [ "url" ] , 2 , iconimage , O00ooooo00 )
  if 25 - 25: IiIi1Iii1I1
def IIIii1II1II ( item , url , iconimage ) :
 oOo0oO = iconimage
 OOOO0oo0 = url
 O0OOO0OOoO0O = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 OOoO00o = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>' , re . DOTALL ) . findall ( item )
 for o00 , I11iiI1i1 , iconimage in OOoO00o :
  if 'youtube.com/playlist?' in I11iiI1i1 :
   I1i1Iiiii = I11iiI1i1 . split ( 'list=' ) [ 1 ]
   i1 ( o00 , I11iiI1i1 , OOo0oO00ooO00 , iconimage , O00ooooo00 , description = I1i1Iiiii )
 if len ( O0OOO0OOoO0O ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<link>(.+?)</link>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  if '.ts' in url : iiIii ( o00 , url , 16 , iconimage , O00ooooo00 , description = '' )
  elif 'movies' in OOOO0oo0 :
   oOO0O00oO0Ooo ( o00 , url , 2 , iconimage , int ( Oooo000o ) , isFolder = False )
  else : II111iiii ( o00 , url , 2 , iconimage , O00ooooo00 )
 elif len ( O0OOO0OOoO0O ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  if '.ts' in url : iiIii ( o00 , url , 16 , iconimage , O00ooooo00 , description = '' )
  elif 'movies' in OOOO0oo0 :
   oOO0O00oO0Ooo ( o00 , url , 3 , iconimage , int ( Oooo000o ) , isFolder = False )
  else : II111iiii ( o00 , url , 3 , iconimage , O00ooooo00 )
  if 67 - 67: IiIi1Iii1I1 - ooOoo0O
def oOoOooOo0o0 ( url ) :
 oooO0oo0oOOOO = O0oO ( url )
 iI1i11iII111 = False
 oo00 = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
 if 'tv%20shows' in url or 'cartoons' in url :
  oo00 = sorted ( oo00 )
  iI1i11iII111 = True
 for o00 , url , IIi1IiiiI1Ii in oo00 :
  if o00 [ 0 ] == '0' :
   if iI1i11iII111 == True :
    o00 = o00 [ 1 : ] + '[COLOR gold]   (New)[/COLOR]'
  if 'youtube.com/playlist?list=' in url :
   i1 ( o00 , url , 18 , IIi1IiiiI1Ii , O00ooooo00 )
  elif 'youtube.com/results?search_query=' in url :
   i1 ( o00 , url , 18 , IIi1IiiiI1Ii , O00ooooo00 )
  else :
   i1 ( o00 , url , 1 , IIi1IiiiI1Ii , O00ooooo00 )
   if 15 - 15: i11iIiiIii % i1I1i1Ii11 . I1Ii + i1iIIIiI1I
def OO0OOOOoo0OOO ( name , url , iconimage ) :
 if 'youtube.com/results?search_query=' in url :
  I1i1Iiiii = url . split ( 'search_query=' ) [ 1 ]
  i1i1Ii1 = Oo + I1i1Iiiii + o0O
  Ii11iIi = urllib2 . Request ( i1i1Ii1 )
  Ii11iIi . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  O00O0Oooo0oO = urllib2 . urlopen ( Ii11iIi )
  oooO0oo0oOOOO = O00O0Oooo0oO . read ( )
  O00O0Oooo0oO . close ( )
  oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oo00 = re . compile ( '"videoId": "(.+?)".+?"title": "(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
  for IIii11I1 , name in oo00 :
   url = 'https://www.youtube.com/watch?v=' + IIii11I1
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % IIii11I1
   II111iiii ( name , url , 2 , iconimage , O00ooooo00 )
 elif 'youtube.com/playlist?list=' in url :
  I1i1Iiiii = url . split ( 'playlist?list=' ) [ 1 ]
  i1i1Ii1 = IiiIII111iI + I1i1Iiiii + IiII
  Ii11iIi = urllib2 . Request ( i1i1Ii1 )
  Ii11iIi . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
  O00O0Oooo0oO = urllib2 . urlopen ( Ii11iIi )
  oooO0oo0oOOOO = O00O0Oooo0oO . read ( )
  O00O0Oooo0oO . close ( )
  oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '\r' , '' ) . replace ( '\n' , '' ) . replace ( '  ' , '' )
  oo00 = re . compile ( '"title": "(.+?)".+?"videoId": "(.+?)"' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
  for name , IIii11I1 in oo00 :
   url = 'https://www.youtube.com/watch?v=' + IIii11I1
   iconimage = 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % IIii11I1
   II111iiii ( name , url , 2 , iconimage , O00ooooo00 )
   if 83 - 83: OoO0O0o0Ooo
def oO00Oo0O0o ( item ) :
 item = item . replace ( '\r' , '' ) . replace ( '\t' , '' ) . replace ( '&nbsp;' , '' ) . replace ( '\'' , '' ) . replace ( '\n' , '' )
 OOoO00o = re . compile ( 'name="(.+?)".+?rl="(.+?)".+?mg="(.+?)"' , re . DOTALL ) . findall ( item )
 for o00 , Oo0oO0ooo , o0oOoO00o in OOoO00o :
  if 'youtube.com/channel/' in Oo0oO0ooo :
   I1i1Iiiii = Oo0oO0ooo . split ( 'channel/' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 , description = I1i1Iiiii )
  elif 'youtube.com/user/' in Oo0oO0ooo :
   I1i1Iiiii = Oo0oO0ooo . split ( 'user/' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 , description = I1i1Iiiii )
  elif 'youtube.com/playlist?' in Oo0oO0ooo :
   I1i1Iiiii = Oo0oO0ooo . split ( 'list=' ) [ 1 ]
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 , description = I1i1Iiiii )
  elif 'plugin://' in Oo0oO0ooo :
   ii1 = HTMLParser ( )
   Oo0oO0ooo = ii1 . unescape ( Oo0oO0ooo )
   i1 ( o00 , Oo0oO0ooo , OOo0oO00ooO00 , o0oOoO00o , O00ooooo00 )
  else :
   i1 ( o00 , Oo0oO0ooo , 1 , o0oOoO00o , O00ooooo00 )
   if 35 - 35: IIIIII11i1I * OOoO000O0OO / I1111 - Ooooo / o0o0Oo0oooo0 - ooOOOo0oo0O0
def OOO00 ( item , url , iconimage ) :
 oOo0oO = iconimage
 O0OOO0OOoO0O = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item )
 II1I1iiIII = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 if len ( O0OOO0OOoO0O ) + len ( II1I1iiIII ) == 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  url = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( item ) [ 0 ]
  url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + url
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  iiIii ( o00 , url , 16 , iconimage , O00ooooo00 )
 elif len ( O0OOO0OOoO0O ) + len ( II1I1iiIII ) > 1 :
  o00 = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  if iconimage == 'ImageHere' : iconimage = oOo0oO
  iiIii ( o00 , url , 3 , iconimage , O00ooooo00 )
  if 77 - 77: O0O0O0O00OooO - oO0 - OoO0O0o0Ooo
def OOOO ( link ) :
 if OOOo0 == '' :
  oOOoo00O0O = xbmcgui . Dialog ( )
  i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'You have opted to show adult content' , '' , 'Please set a password to prevent accidental access' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Set Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
    O0O0OO0O0O0 . setSetting ( 'password' , I11 )
  else : quit ( )
 elif OOOo0 <> '' :
  oOOoo00O0O = xbmcgui . Dialog ( )
  i1111 = oOOoo00O0O . yesno ( 'Adult Content' , 'Please enter the password you set' , 'to continue' , '' , 'Cancel' , 'OK' )
  if i1111 == 1 :
   i11 = xbmc . Keyboard ( '' , 'Enter Password' )
   i11 . doModal ( )
   if ( i11 . isConfirmed ( ) ) :
    I11 = i11 . getText ( )
   if I11 <> OOOo0 :
    quit ( )
  else : quit ( )
  if 49 - 49: oO0 % I1II1 . O0O0O0O00OooO + OOoO000O0OO / IIIi1i1I
def O0oOOoOooooO ( ) :
 i11 = xbmc . Keyboard ( '' , 'Search' )
 i11 . doModal ( )
 if ( i11 . isConfirmed ( ) ) :
  I1i1Iiiii = i11 . getText ( )
  I1i1Iiiii = I1i1Iiiii . upper ( )
 else : quit ( )
 oooO0oo0oOOOO = O0oO ( ooOo )
 oooOo0OOOoo0 = re . compile ( '<link>(.+?)</link>' ) . findall ( oooO0oo0oOOOO )
 for Oo0oO0ooo in oooOo0OOOoo0 :
  try :
   oooO0oo0oOOOO = O0oO ( Oo0oO0ooo )
   OOoO = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO )
   for OOooO in OOoO :
    oo00 = re . compile ( '<title>(.+?)</title>' ) . findall ( OOooO )
    for OO0O000 in oo00 :
     OO0O000 = OO0O000 . upper ( )
     if I1i1Iiiii in OO0O000 :
      try :
       if '<sportsdevil>' in OOooO : OOO00 ( OOooO , Oo0oO0ooo , o0oOoO00o )
       elif '<iptv>' in OOooO : iiiiiIIii ( OOooO )
       elif '<Image>' in OOooO : O000OO0 ( OOooO )
       elif '<text>' in OOooO : I11iii1Ii ( OOooO )
       elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO )
       elif '<redirect>' in OOooO : REDIRECT ( OOooO )
       elif '<oktitle>' in OOooO : O000oo0O ( OOooO )
       elif '<dl>' in OOooO : OOOOi11i1 ( OOooO )
       elif '<scraper>' in OOooO : I1IIiiIiii ( OOooO , o0oOoO00o )
       else : IIIii1II1II ( OOooO , Oo0oO0ooo , o0oOoO00o )
      except : pass
  except : pass
  if 37 - 37: o0o0Oo0oooo0 - I1II1 - Ooooo
def o0o0O0O00oOOo ( name , url , iconimage ) :
 oOo0oO = iconimage
 iIIIiIi = [ ]
 OO0O0 = [ ]
 I11I11 = [ ]
 oooO0oo0oOOOO = O0oO ( url )
 o000O0O = re . compile ( '<title>' + re . escape ( name ) + '</title>(.+?)</item>' , re . DOTALL ) . findall ( oooO0oo0oOOOO ) [ 0 ]
 O0OOO0OOoO0O = [ ]
 if '<link>' in o000O0O :
  I1i1i1iii = re . compile ( '<link>(.+?)</link>' ) . findall ( o000O0O )
  for I1111i in I1i1i1iii :
   O0OOO0OOoO0O . append ( I1111i )
 if '<sportsdevil>' in o000O0O :
  iIIii = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( o000O0O )
  for o00O0O in iIIii :
   o00O0O = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + o00O0O
   O0OOO0OOoO0O . append ( o00O0O )
 OoO0O00 = 1
 for ii1iii1i in O0OOO0OOoO0O :
  Iii1I1111ii = ii1iii1i
  if 'acestream://' in ii1iii1i or '.acelive' in ii1iii1i or 'sop://' in ii1iii1i : ooOoO00 = ' (Acestreams)'
  else : ooOoO00 = ''
  if '(' in ii1iii1i :
   ii1iii1i = ii1iii1i . split ( '(' ) [ 0 ]
   Ii1IIiI1i = str ( Iii1I1111ii . split ( '(' ) [ 1 ] . replace ( ')' , '' ) + ooOoO00 )
   iIIIiIi . append ( ii1iii1i )
   OO0O0 . append ( Ii1IIiI1i )
  else :
   o0O00Oo0 = ii1iii1i . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
   iIIIiIi . append ( ii1iii1i )
   OO0O0 . append ( 'Link ' + str ( OoO0O00 ) + ooOoO00 )
  OoO0O00 = OoO0O00 + 1
 oOOoo00O0O = xbmcgui . Dialog ( )
 o0ooOooo000oOO = oOOoo00O0O . select ( 'Choose a link..' , OO0O0 )
 if o0ooOooo000oOO < 0 : quit ( )
 else :
  url = iIIIiIi [ o0ooOooo000oOO ]
  Oo0oOOo ( name , url , iconimage )
  if 33 - 33: I1II1 * Ooooo - ooOOOo0oo0O0 % ooOOOo0oo0O0
def I11I ( url ) :
 II = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( II )
 if 50 - 50: ooOOOo0oo0O0 * i11iIiiIii * I1111 - oO0 * Ooooo * O0O0O0O00OooO
def Oo0oOOo ( name , url , iconimage ) :
 try :
  if 'sop://' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=2&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   OoooOoo ( name , url , iconimage )
  elif 'acestream://' in url or '.acelive' in url :
   url = urllib . quote ( url )
   url = 'plugin://program.plexus/?mode=1&url=%s&name=%s' % ( url , name . replace ( ' ' , '+' ) )
   OoooOoo ( name , url , iconimage )
  elif 'plugin://plugin.video.SportsDevil/' in url :
   OoooOoo ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   OoooOoo ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   O0o000Oo ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   O0o000Oo ( name , url , iconimage )
  else : OoooOoo ( name , url , iconimage )
 except :
  ooo ( 'UKTurk' , 'Stream Unavailable' , '3000' , IIi1IiiiI1Ii )
  if 27 - 27: OoO0O0o0Ooo % IIIi1i1I
def o0oooOO00 ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 32 - 32: ooOOOo0oo0O0
def O0o000Oo ( name , url , iconimage ) :
 Iii1 = True
 oOOOoo00 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; oOOOoo00 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = oOOOoo00 )
 oOOOoo00 . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , oOOOoo00 )
 if 9 - 9: I1II1 % I1II1 - Ooooo
def OoooOoo ( name , url , iconimage ) :
 Iii1 = True
 oOOOoo00 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; oOOOoo00 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = oOOOoo00 )
 oOOoo00O0O = xbmcgui . Dialog ( )
 xbmc . Player ( ) . play ( url , oOOOoo00 , False )
 if 51 - 51: IIIi1i1I . I1111 - i1iIIIiI1I / I1II1
def OOOoO00 ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 40 - 40: i1iIIIiI1I % IIIi1i1I . OoO0O0o0Ooo . I1II1 * ooOOOo0oo0O0
def i11II1I11I1 ( url ) :
 OOoOO0ooo = O0O0OO0O0O0 . getSetting ( 'layout' )
 if OOoOO0ooo == 'Listers' : O0O0OO0O0O0 . setSetting ( 'layout' , 'Category' )
 else : O0O0OO0O0O0 . setSetting ( 'layout' , 'Listers' )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 30 - 30: Ooooo - I1I1i1 % oO0 + O00 * I1111
def O0oO ( url ) :
 Ii11iIi = urllib2 . Request ( url )
 Ii11iIi . add_header ( 'User-Agent' , 'mat' )
 O00O0Oooo0oO = urllib2 . urlopen ( Ii11iIi )
 oooO0oo0oOOOO = O00O0Oooo0oO . read ( )
 O00O0Oooo0oO . close ( )
 oooO0oo0oOOOO = oooO0oo0oOOOO . replace ( '</fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in oooO0oo0oOOOO : oooO0oo0oOOOO = o0ooooO0o0O ( oooO0oo0oOOOO )
 return oooO0oo0oOOOO
 if 24 - 24: I1II1 * Ooooo
def IiI1iiiIii ( ) :
 I1III1111iIi = [ ]
 I1i111I = sys . argv [ 2 ]
 if len ( I1i111I ) >= 2 :
  o0o0o0oO0oOO = sys . argv [ 2 ]
  Ooo = o0o0o0oO0oOO . replace ( '?' , '' )
  if ( o0o0o0oO0oOO [ len ( o0o0o0oO0oOO ) - 1 ] == '/' ) :
   o0o0o0oO0oOO = o0o0o0oO0oOO [ 0 : len ( o0o0o0oO0oOO ) - 2 ]
  Oo0oo0O0o00O = Ooo . split ( '&' )
  I1III1111iIi = { }
  for OoO0O00 in range ( len ( Oo0oo0O0o00O ) ) :
   I1i11 = { }
   I1i11 = Oo0oo0O0o00O [ OoO0O00 ] . split ( '=' )
   if ( len ( I1i11 ) ) == 2 :
    I1III1111iIi [ I1i11 [ 0 ] ] = I1i11 [ 1 ]
 return I1III1111iIi
 if 12 - 12: I1I1i1 + I1I1i1 - i1iIIIiI1I * I1Ii % I1Ii - oO0
def ooo ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 52 - 52: OoO0O0o0Ooo . IIIIII11i1I + ooOOOo0oo0O0
def IIIII ( string ) :
 iiii1IIi = re . compile ( '\[(.+?)\]' ) . findall ( string )
 for iII1i11IIi1i in iiii1IIi : string = string . replace ( iII1i11IIi1i , '' ) . replace ( '[/]' , '' ) . replace ( '[]' , '' )
 return string
 if 73 - 73: Ooooo * I1II1 - i11iIiiIii
def O0O0o0oOOO ( string ) :
 string = string . split ( ' ' )
 OOoOoOo = ''
 for o000ooooO0o in string :
  iI1i11 = '[B][COLOR red]' + o000ooooO0o [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + o000ooooO0o [ 1 : ] + '[/COLOR][/B] '
  OOoOoOo = OOoOoOo + iI1i11
 return OOoOoOo
 if 66 - 66: I1II1 % i1iIIIiI1I + i11iIiiIii . O0O0O0O00OooO / i1I1i1Ii11 + i1iIIIiI1I
def oOO0O00oO0Ooo ( name , url , mode , iconimage , itemcount , isFolder = False ) :
 if IiIi11iIIi1Ii == 'true' :
  if not 'COLOR' in name :
   ooo00Ooo = name . partition ( '(' )
   Oo0o0O00 = ""
   ii1I1i11 = ""
   if len ( ooo00Ooo ) > 0 :
    Oo0o0O00 = ooo00Ooo [ 0 ]
    ii1I1i11 = ooo00Ooo [ 2 ] . partition ( ')' )
   if len ( ii1I1i11 ) > 0 :
    ii1I1i11 = ii1I1i11 [ 0 ]
   OOo0O0oo0OO0O = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
   OO0 = OOo0O0oo0OO0O . get_meta ( 'movie' , name = Oo0o0O00 , year = ii1I1i11 )
   o0Oooo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( iiI ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
   Iii1 = True
   oOOOoo00 = xbmcgui . ListItem ( name , iconImage = OO0 [ 'cover_url' ] , thumbnailImage = OO0 [ 'cover_url' ] )
   oOOOoo00 . setInfo ( type = "Video" , infoLabels = OO0 )
   oOOOoo00 . setProperty ( "IsPlayable" , "true" )
   oO = [ ]
   if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : oO . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : oO . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
   oOOOoo00 . addContextMenuItems ( oO , replaceItems = False )
   if not OO0 [ 'backdrop_url' ] == '' : oOOOoo00 . setProperty ( 'fanart_image' , OO0 [ 'backdrop_url' ] )
   else : oOOOoo00 . setProperty ( 'fanart_image' , O00ooooo00 )
   Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o0Oooo , listitem = oOOOoo00 , isFolder = isFolder , totalItems = itemcount )
   return Iii1
 else :
  o0Oooo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&site=" + str ( iiI ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
  Iii1 = True
  oOOOoo00 = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage )
  oOOOoo00 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
  oOOOoo00 . setProperty ( 'fanart_image' , O00ooooo00 )
  oOOOoo00 . setProperty ( "IsPlayable" , "true" )
  oO = [ ]
  if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : oO . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : oO . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  oOOOoo00 . addContextMenuItems ( oO , replaceItems = False )
  Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o0Oooo , listitem = oOOOoo00 , isFolder = isFolder )
  return Iii1
  if 10 - 10: I1Ii / I1Ii / ooOOOo0oo0O0 . ooOOOo0oo0O0
def i1 ( name , url , mode , iconimage , fanart , description = '' ) :
 o0Oooo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 Iii1 = True
 oOOOoo00 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 oOOOoo00 . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 oOOOoo00 . setProperty ( 'fanart_image' , fanart )
 oO = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : oO . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : oO . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 oOOOoo00 . addContextMenuItems ( oO , replaceItems = False )
 if 'plugin://' in url :
  o0Oooo = url
 Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o0Oooo , listitem = oOOOoo00 , isFolder = True )
 return Iii1
 if 98 - 98: I1Ii / IIIi1i1I . I1II1 + IiIi1Iii1I1
def iiIii ( name , url , mode , iconimage , fanart , description = '' ) :
 o0Oooo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 Iii1 = True
 oOOOoo00 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 oOOOoo00 . setProperty ( 'fanart_image' , fanart )
 oO = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : oO . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : oO . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 oOOOoo00 . addContextMenuItems ( oO , replaceItems = False )
 Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o0Oooo , listitem = oOOOoo00 , isFolder = False )
 return Iii1
 if 43 - 43: oO0 . OOoO000O0OO / i1iIIIiI1I
def II111iiii ( name , url , mode , iconimage , fanart , description = '' ) :
 o0Oooo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 Iii1 = True
 oOOOoo00 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 oOOOoo00 . setProperty ( 'fanart_image' , fanart )
 oOOOoo00 . setProperty ( "IsPlayable" , "true" )
 oO = [ ]
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'yes' : oO . append ( ( '[COLOR red]Remove from UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 if O0O0OO0O0O0 . getSetting ( 'fav' ) == 'no' : oO . append ( ( '[COLOR white]Add to UK Turk Favourites[/COLOR]' , 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 oOOOoo00 . addContextMenuItems ( oO , replaceItems = False )
 Iii1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o0Oooo , listitem = oOOOoo00 , isFolder = False )
 return Iii1
 if 20 - 20: IIIi1i1I
def o0oO000oo ( url , name ) :
 o00o0II1I = O0oO ( url )
 if len ( o00o0II1I ) > 1 :
  oOooOOOoOo = Oo0O
  i1Iii1i1I = os . path . join ( os . path . join ( oOooOOOoOo , '' ) , name + '.txt' )
  if not os . path . exists ( i1Iii1i1I ) :
   file ( i1Iii1i1I , 'w' ) . close ( )
  II1I1I1Ii = open ( i1Iii1i1I )
  OOOOoO00o0O = II1I1I1Ii . read ( )
  if OOOOoO00o0O == o00o0II1I : pass
  else :
   o00oooO0Oo ( 'UKTurk' , o00o0II1I )
   OOoO00 = open ( i1Iii1i1I , "w" )
   OOoO00 . write ( o00o0II1I )
   OOoO00 . close ( )
   if 41 - 41: ooOoo0O * i1I1i1Ii11 - o0o0OOO0o0 + Ooooo
def o00oooO0Oo ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 oOOOo00O00O = xbmcgui . Window ( id )
 iIIIII1I = 50
 while ( iIIIII1I > 0 ) :
  try :
   xbmc . sleep ( 10 )
   iIIIII1I -= 1
   oOOOo00O00O . getControl ( 1 ) . setLabel ( heading )
   oOOOo00O00O . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 51 - 51: I1111 . OoO0O0o0Ooo + I1111
def oOoOO ( name ) :
 global Icon
 global Next
 global Previous
 global window
 global Quit
 global images
 i1Iii1i1I = os . path . join ( os . path . join ( Oo0O , '' ) , name + '.txt' )
 II1I1I1Ii = open ( i1Iii1i1I )
 OOOOoO00o0O = II1I1I1Ii . read ( )
 images = re . compile ( '<image>(.+?)</image>' ) . findall ( OOOOoO00o0O )
 O0O0OO0O0O0 . setSetting ( 'pos' , '0' )
 window = pyxbmct . AddonDialogWindow ( '' )
 Ii1i1 = '/resources/art'
 O0o = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'next_focus.png' ) )
 i1iIiIIi = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'next1.png' ) )
 oO0o00oo0 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'previous_focus.png' ) )
 ii1IIII = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'previous.png' ) )
 oO00oOooooo0 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'close_focus.png' ) )
 oOo = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'close.png' ) )
 O0OOooOoO = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + OO0o + Ii1i1 , 'main-bg1.png' ) )
 window . setGeometry ( 1300 , 720 , 100 , 50 )
 i1II1I1Iii1 = pyxbmct . Image ( O0OOooOoO )
 window . placeControl ( i1II1I1Iii1 , - 10 , - 10 , 130 , 70 )
 i1iIi = '0xFF000000'
 Previous = pyxbmct . Button ( '' , focusTexture = oO0o00oo0 , noFocusTexture = ii1IIII , textColor = i1iIi , focusedColor = i1iIi )
 Next = pyxbmct . Button ( '' , focusTexture = O0o , noFocusTexture = i1iIiIIi , textColor = i1iIi , focusedColor = i1iIi )
 Quit = pyxbmct . Button ( '' , focusTexture = oO00oOooooo0 , noFocusTexture = oOo , textColor = i1iIi , focusedColor = i1iIi )
 Icon = pyxbmct . Image ( images [ 0 ] , aspectRatio = 1 )
 window . placeControl ( Previous , 102 , 1 , 10 , 10 )
 window . placeControl ( Next , 102 , 40 , 10 , 10 )
 window . placeControl ( Quit , 102 , 21 , 10 , 10 )
 window . placeControl ( Icon , 0 , 0 , 100 , 50 )
 Previous . controlRight ( Next )
 Previous . controlUp ( Quit )
 window . connect ( Previous , iiI11Iii )
 window . connect ( Next , O0o0O0 )
 Previous . setVisible ( False )
 window . setFocus ( Quit )
 Previous . controlRight ( Quit )
 Quit . controlLeft ( Previous )
 Quit . controlRight ( Next )
 Next . controlLeft ( Quit )
 window . connect ( Quit , window . close )
 window . doModal ( )
 del window
 if 11 - 11: oO0 % IiIi1Iii1I1 * IIIIII11i1I + OoO0O0o0Ooo + i1I1i1Ii11
def O0o0O0 ( ) :
 II1Iiiiii = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 ii1ii111 = int ( II1Iiiiii ) + 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( ii1ii111 ) )
 I111i1i1111 = len ( images )
 Icon . setImage ( images [ int ( ii1ii111 ) ] )
 Previous . setVisible ( True )
 if int ( ii1ii111 ) == int ( I111i1i1111 ) - 1 :
  Next . setVisible ( False )
  if 49 - 49: IiIi1Iii1I1 / OOoO000O0OO + I1II1 * Ooooo
def iiI11Iii ( ) :
 II1Iiiiii = int ( O0O0OO0O0O0 . getSetting ( 'pos' ) )
 I1ii11 = int ( II1Iiiiii ) - 1
 O0O0OO0O0O0 . setSetting ( 'pos' , str ( I1ii11 ) )
 Icon . setImage ( images [ int ( I1ii11 ) ] )
 Next . setVisible ( True )
 if int ( I1ii11 ) == 0 :
  Previous . setVisible ( False )
  if 74 - 74: I1Ii - Ooooo . I1I1i1
def o0ooooO0o0O ( gobble ) :
 gobble = gobble . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
 gobble = gobble + '=='
 gobble = gobble . decode ( 'base64' )
 return gobble
 if 43 - 43: IIIIII11i1I / IIIi1i1I
def OO0oo0O ( text ) :
 def Ii1i1iI ( m ) :
  i1iIi = m . group ( 0 )
  if i1iIi [ : 3 ] == "&#x" : return unichr ( int ( i1iIi [ 3 : - 1 ] , 16 ) ) . encode ( 'utf-8' )
  else : return unichr ( int ( i1iIi [ 2 : - 1 ] ) ) . encode ( 'utf-8' )
 try : return re . sub ( "(?i)&#\w+;" , Ii1i1iI , text . decode ( 'ISO-8859-1' ) . encode ( 'utf-8' ) )
 except : return re . sub ( "(?i)&#\w+;" , Ii1i1iI , text . encode ( "ascii" , "ignore" ) . encode ( 'utf-8' ) )
 if 16 - 16: ooOoo0O / I1Ii / o0o0Oo0oooo0 * IIIi1i1I + I1I1i1 % ooOoo0O
def ooooooO0oo ( link ) :
 try :
  ooo0o00 = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if ooo0o00 == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 99 - 99: I1II1 . O00 + I1111
o0o0o0oO0oOO = IiI1iiiIii ( ) ; Oo0oO0ooo = None ; o00 = None ; OOo0oO00ooO00 = None ; iiI = None ; o0oOoO00o = None
try : iiI = urllib . unquote_plus ( o0o0o0oO0oOO [ "site" ] )
except : pass
try : Oo0oO0ooo = urllib . unquote_plus ( o0o0o0oO0oOO [ "url" ] )
except : pass
try : o00 = urllib . unquote_plus ( o0o0o0oO0oOO [ "name" ] )
except : pass
try : OOo0oO00ooO00 = int ( o0o0o0oO0oOO [ "mode" ] )
except : pass
try : o0oOoO00o = urllib . unquote_plus ( o0o0o0oO0oOO [ "iconimage" ] )
except : pass
try : O00ooooo00 = urllib . unquote_plus ( o0o0o0oO0oOO [ "fanart" ] )
except : pass
try : I11IIi = urllib . unquote_plus ( [ "description" ] )
except : pass
if 66 - 66: OOoO000O0OO % IiIi1Iii1I1 . ooOoo0O
if OOo0oO00ooO00 == None or Oo0oO0ooo == None or len ( Oo0oO0ooo ) < 1 : Ooo0OO0oOO ( )
elif OOo0oO00ooO00 == 1 : o0 ( o00 , Oo0oO0ooo , o0oOoO00o , O00ooooo00 )
elif OOo0oO00ooO00 == 2 : Oo0oOOo ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 3 : o0o0O0O00oOOo ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 4 : O0o000Oo ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 5 : O0oOOoOooooO ( )
elif OOo0oO00ooO00 == 6 : i1I1iI1iIi111i ( Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 7 : I11I ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 8 : oOoOO ( o00 )
elif OOo0oO00ooO00 == 9 : I11i1iIII ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 10 : DOSCRAPER ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 11 : OOOoO00 ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 12 : iiI1IiI ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 13 : i11II1I11I1 ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 14 : OooO0 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 15 : OOoOoo00oo ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 16 : OoooOoo ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 17 : iii ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 18 : OO0OOOOoo0OOO ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 19 : OO0OoO0o00 ( o00 , Oo0oO0ooo )
elif OOo0oO00ooO00 == 20 : ii1ii1ii ( Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 21 : I1III ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 22 : O00o0O00 ( o00 , Oo0oO0ooo , o0oOoO00o )
elif OOo0oO00ooO00 == 23 : o0OO00oO ( Oo0oO0ooo )
elif OOo0oO00ooO00 == 24 : iIIIIii1 ( o00 , Oo0oO0ooo , o0oOoO00o )
if 86 - 86: I1111
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
