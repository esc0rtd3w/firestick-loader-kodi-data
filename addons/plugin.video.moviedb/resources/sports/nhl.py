import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,time
from resources.modules import main


from addon.common.addon import Addon
addon_id = 'plugin.video.moviedb'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.moviedb', sys.argv)
art = main.art
artwork = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/', ''))
fanart = xbmc.translatePath(os.path.join('http://cliqaddon.com/support/commoncore/tvaddons/moviedb/showgunart/images/fanart/fanart.jpg', ''))


def MAINNHL():
    source_media = {}
    from datetime import datetime
    datex=datetime.now().strftime('%Y%m%d')
    xml='http://live.nhl.com/GameData/SeasonSchedule-20142015.json'
    link=main.OPEN_URL(xml)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    main.addDir('[COLOR red]Archived Games[/COLOR]','Archived',394,art+'/nhl.png','','')
    if 'Archived' not in murl:
        main.addLink("[COLOR red]Live Games Windows Only, Requires some modifications to get working visit forum.[/COLOR]",'','')
    match=re.compile('{"id":(.+?),"est":"(.+?)","a":"(.+?)","h":"(.+?)"}',re.DOTALL).findall(link)
    for id,timed,ateam,hteam in match:
        split= re.search('(.+?)\s(\d+:\d+):\d+',timed)
        split1=str(split.group(1))
        split2=str(split.group(2))
        if 'Archived' in murl:
            if int(split1)<=int(datex):
                dates= re.search('(\d{4})(\d{2})(\d{2})',split1)
                date=str(dates.group(2))+"/"+str(dates.group(3))+"/"+str(dates.group(1))
                timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
                main.addDir(ateam+' at '+hteam+' [COLOR red]('+timed+')[/COLOR] [COLOR blue]('+date+')[/COLOR]',id,395,art+'/nhl.png','','')
        else:
            if datex == split1:
                
                dates= re.search('(\d{4})(\d{2})(\d{2})',split1)
                date=str(dates.group(2))+"/"+str(dates.group(3))+"/"+str(dates.group(1))
                timed = time.strftime("%I:%M %p", time.strptime(split2, "%H:%M"))
                main.addDir(ateam+' at '+hteam+' [COLOR red]('+timed+')[/COLOR] [COLOR blue]('+date+')[/COLOR]',id,395,art+'/nhl.png','','')
                

def LISTSTREAMS(mname,murl):
    mname=main.removeColoredText(mname)
    id= re.search('(\d{4})(\d{2})(\d{4})',murl)
    xml='http://smb.cdnak.neulion.com/fs/nhl/mobile/feed_new/data/streams/'+str(id.group(1))+'/ipad/'+str(id.group(2))+'_'+str(id.group(3))+'.json'
    link=main.OPEN_URL(xml)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('"vod-condensed":{"bitrate0":"([^"]+)"},"vod-continuous":{"bitrate0":"([^"]+)","image":"([^"]+)"},"vod-whole":{"bitrate0":"([^"]+)"}',re.DOTALL).findall(link)
    for cond,cont,thumb,whole in match:
        if '_h_condensed' in cond:
            main.addPlayc(mname+' [COLOR blue]Home Condensed[/COLOR]',cond,396,thumb,'','','','','')
        else:
            main.addPlayc(mname+' [COLOR blue]Away Condensed[/COLOR]',cond,396,thumb,'','','','','')
        if '_h_continuous' in cont:
            main.addPlayc(mname+' [COLOR blue]Home Continuous[/COLOR]',cont,396,thumb,'','','','','')
        else:
            main.addPlayc(mname+' [COLOR blue]Away Continuous[/COLOR]',cont,396,thumb,'','','','','')
        if '_h_whole' in whole:
            main.addPlayc(mname+' [COLOR blue]Home Whole[/COLOR]',whole,396,thumb,'','','','','')
        else:
            main.addPlayc(mname+' [COLOR blue]Away Whole[/COLOR]',whole,396,thumb,'','','','','')
    match2=re.compile('"away".+?"live":{"bitrate0":"([^"]+)"},.+?"image":"([^"]+)"',re.DOTALL).findall(link)
    for live,thumb in match2:
        main.addPlayc(mname+' [COLOR blue]Away Live[/COLOR]',live+'x0xe'+str(murl),396,thumb,'','','','','')
    match3=re.compile('"home".+?"live":{"bitrate0":"([^"]+)"},.+?"image":"([^"]+)"',re.DOTALL).findall(link)
    for live,thumb in match3:
        main.addPlayc(mname+' [COLOR blue]Home LIVE[/COLOR]',live+'x0xe'+str(murl),396,thumb,'','','','','')
def LINK(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        namelist=[]
        urllist=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        if '_whole' in murl:
            link=main.OPEN_URL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
            part= re.findall('/([^/]+)ipad.mp4.m3u8',murl)[0]
            match=re.compile('BANDWIDTH=.+?'+part+'(.+?)_ipad.mp4.m3u8',re.DOTALL).findall(link)
            for band in sorted(match):
                namelist.append(band)
            dialog = xbmcgui.Dialog()
            answer =dialog.select("Pick A Bandwidth", namelist)
            if answer != -1:
                nurl=murl.split('ipad.mp4.m3u8')[0]
                stream_url=nurl+namelist[int(answer)]+'_ipad.mp4.m3u8'+'|User-Agent=PS4 libhttp/1.76 (PlayStation 4)'
            else:
                return
        elif '/live/' in murl:
            import subprocess
            jarfile = xbmc.translatePath('special://home/addons/plugin.video.moviedb/resources/libs/live/FuckNeulionV2.jar')
            if 'Home' in mname:
                Side='home'
            if 'Away' in mname:
                Side='away'
            SelectGame=murl.split('x0xe')[1]
            murl=murl.split('x0xe')[0]
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            command=['java','-jar',jarfile,SelectGame,Side]
            proxy_hack_process = subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          startupinfo=startupinfo)
            xbmc.sleep(1000)
            link=main.OPEN_URL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
            part= re.findall('/([^/]+)ipad.m3u8',murl)[0]
            match=re.compile('BANDWIDTH=.+?'+part+'(.+?)_ipad.m3u8',re.DOTALL).findall(link)
            for band in sorted(match):
                namelist.append(band)
            dialog = xbmcgui.Dialog()
            answer =dialog.select("Pick A Bandwidth", namelist)
            if answer != -1:
                nurl=murl.split('ipad.m3u8')[0]
                stream_url=nurl+namelist[int(answer)]+'_ipad.m3u8'+'|User-Agent=PS4 libhttp/1.76 (PlayStation 4)'
            
            else:
                return
        else:
            stream_url = murl+'|User-Agent=PS4 libhttp/1.76 (PlayStation 4)'
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        infoL={'Title': mname, 'Genre': 'Live'} 
        from resources.universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='movie', title=mname,season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams='',imdb_id='')

        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from resources.universal import watchhistory
            wh = watchhistory.WatchHistory('plugin.video.movie25')
            wh.add_item(mname+' '+'[COLOR green]NHL[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok

