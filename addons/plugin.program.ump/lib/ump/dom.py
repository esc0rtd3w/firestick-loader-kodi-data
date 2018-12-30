from xml.dom import minidom
import xbmcvfs
import xbmcgui
from os.path import split

def read(xname):
    try:
        f=open(xname,"r")
        data=f.read()
        f.close()
        #ignore wihtespace befaor '<' character. some android versions suspected to put chars in front of xmls 
        c=0
        for c in range(len(data)):
            if data[c]=="<":
                break     
        return minidom.parseString(data[c:])
    except:
        return

def write(xname,res):
    try:
        data=res.toxml("UTF-8")
        with open(xname, 'w') as f:
            f.write(data)
        res.unlink()
        return True
    except:
        return False
    
def check(xname,backup):
    if not read(xname):
        xbmcvfs.copy(backup, xname)
        dialog=xbmcgui.Dialog()
        (head,tail)=split(xname)
        dialog.ok("UMP Recovery","Ump has succesfully recoverd broken xml file",head,tail)
        del(dialog)
        return False
    else:
        return True