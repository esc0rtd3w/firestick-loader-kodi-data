import os
import xbmcvfs
import urllib
import json
import md5
import zlib
import time

class throttle():
    def __init__(self,path):
        self.path=path
        if not xbmcvfs.exists(path):
            xbmcvfs.mkdir(path)
    
    def check(self,tid,lag=2):
        fname=os.path.join(self.path,tid,"data.bin")
        tsname=os.path.join(self.path,tid,"timestamp.ascii")
        if lag==0:
            return xbmcvfs.exists(fname)
        elif isinstance(lag,(float,int)) and xbmcvfs.exists(tsname):
            f=xbmcvfs.File(tsname,"r")
            timestamp=float(f.read())
            f.close()
            if time.time()-timestamp<lag*60*60:
                return True
            else:
                return False
        else:
            return False
    
    def get(self,tid):
        fname=os.path.join(self.path,tid,"data.bin")
        f=xbmcvfs.File(fname,"rb")
        data=zlib.decompress(f.read())
        f.close()
        return data
    
    def do(self,tid,data):
        fname=os.path.join(self.path,tid,"")
        xbmcvfs.mkdir(fname)
        fname=os.path.join(self.path,tid,"data.bin")
        f=xbmcvfs.File(fname,"wb")
        f.write(zlib.compress(data,9))
        f.close()
        fname=os.path.join(self.path,tid,"timestamp.ascii")
        f=xbmcvfs.File(fname,"w")
        f.write(str(time.time()))
        f.close()
        return True
    
    def id(self,*args,**kwargs):
        return md5.new(json.dumps({"args":args,"kwargs":kwargs})).hexdigest()