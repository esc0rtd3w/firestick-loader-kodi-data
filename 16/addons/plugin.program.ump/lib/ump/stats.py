import xbmcvfs
import os
import time
import defs
import identifier
import shutil
import datetime
import xbmcgui
import calendar

ttol=12*60*60

def mkdir(*paths):
    paths=list(paths)
    paths.append("")
    path=os.path.join(*paths)
    if not xbmcvfs.exists(path):xbmcvfs.mkdirs(path)
    
def rmdir(path):
    return shutil.rmtree(path)

class stats():
    def __init__(self):
        self.seenids=[] #cache wacthed ids in ram on each run to make it faster
        mkdir(defs.addon_stdir)
        self.identifier=identifier.identifier()
        
    def gettime(self,info):
        timestamp=None
        timestamp=info.get("aired",None)
        if timestamp is None:
            timestamp=info.get("date","")
        formats=["%Y-%m-%d"]
        for format in formats:
            try:
                timestamp=calendar.timegm(time.strptime(timestamp,format))
            except:
                timestamp=None
                continue
            break
        return timestamp
        
    def _checkid(self,id,ts=None):
        path=os.path.join(defs.addon_stdir,id,"")
        prechk=id in self.seenids or xbmcvfs.exists(path)
        if ts is None:
            return prechk
        elif prechk:
            tfile=os.path.join(path,"timestamp.ascii")
            f = xbmcvfs.File(tfile,'r')
            timestamp=float(f.read())
            f.close()
            if timestamp>ts+ttol:
                #put half a day time tolerance for different timezones in world :/
                return True
            else:
                return False
        else:
            return False
            
    def markseen(self,info,mediapointer=None):
        ts=self.gettime(info)
        if ts and ts>time.time():
            d=xbmcgui.Dialog()
            d.ok("UMP","You can not mark a media which is not yet released!\nIs your system time correct?\nYour system time: %s, \nMedia release time:\n%s"%(
                                       datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                                       datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                       )
                 )
            return
        id=self.identifier.createhash(info,mediapointer)
        mkdir(defs.addon_stdir,id)
        f = xbmcvfs.File(os.path.join(defs.addon_stdir,id,"timestamp.ascii"),'w')
        f.write(str(time.time()))
        f.close()
        self.seenids.append(id)
        
    def markunseen(self,info,mediapointer=None):
        id=self.identifier.createhash(info,mediapointer)
        path=os.path.join(defs.addon_stdir,id,"")
        if xbmcvfs.exists(path):
            rmdir(path)
        
    def isseen(self,info,mediapointer=None):
        if mediapointer:
            id=self.identifier.createhash(info,mediapointer)
            if self._checkid(id):
                    self.seenids.append(id)
                    return 1
        else:
            ts=self.gettime(info)
            mediapointer=self.identifier.getpointer(info)
            for i in range(len(mediapointer)):
                nestedid=self.identifier.createhash(info,mediapointer=mediapointer[:i+1])
                if self._checkid(nestedid,ts):
                    self.seenids.append(nestedid)
                    return 1
        return 0