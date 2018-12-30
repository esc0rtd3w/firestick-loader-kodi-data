'''
Created on Dec 22, 2011

@author: ajju
'''
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
import base64
import binascii
import urllib
try:
    import json
except ImportError:
    import simplejson as json


def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.videobb.com/images/logo.jpg')
    video_hosting_info.set_video_hosting_name('Videobb')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://www.videobb.com/player_control/settings.php?v=' + video_id + '&fv=v1.2.72'
        jsonObj = json.load(urllib.urlopen(video_info_link))
                
        key1 = jsonObj["settings"]["config"]["rkts"]
        key2 = jsonObj["settings"]["login_status"]["pepper"]
        key3 = jsonObj["settings"]["banner"]["lightbox2"]["time"]
        
        values = binascii.unhexlify(decrypt(jsonObj["settings"]["login_status"]["spen"], jsonObj["settings"]["login_status"]["salt"], 950569)).split(';')
        spn = HttpUtils.getUrlParams(values[0])
        outk = HttpUtils.getUrlParams(values[1])
        ikey = getikey(int(outk["ik"]))
        
        urlKey = ''
        for spnkey in spn:
            spnval = spn[spnkey]
            if spnval == '1':
                cypher = jsonObj["settings"]["video_details"]["sece2"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey, ln=256) + '&'
            if spnval == '2':
                cypher = jsonObj["settings"]["banner"]["g_ads"]["url"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey) + '&'
            if spnval == '3':
                cypher = jsonObj["settings"]["banner"]["g_ads"]["type"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey, 26, 25431, 56989, 93, 32589, 784152) + '&'
            if spnval == '4':
                cypher = jsonObj["settings"]["banner"]["g_ads"]["time"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key1, ikey, 82, 84669, 48779, 32, 65598, 115498) + '&'
            if spnval == '5':
                cypher = jsonObj["settings"]["login_status"]["euno"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key2, ikey, 10, 12254, 95369, 39, 21544, 545555) + '&'
            if spnval == '6':
                cypher = jsonObj["settings"]["login_status"]["sugar"]
                urlKey = urlKey + spnkey + '=' + decrypt(cypher, key3, ikey, 22, 66595, 17447, 52, 66852, 400595) + '&'
        
        urlKey = urlKey + "start=0"
        
        video_link = ""
        for videoStrm in jsonObj["settings"]["res"]:
            if videoStrm["d"]:
                video_link = str(base64.b64decode(videoStrm["u"]))
        if video_link == "":
            video_info.set_video_stopped(False)
            raise Exception("VIDEO_STOPPED")
        video_link = video_link + '&' + urlKey
        
        video_info.set_video_name(jsonObj["settings"]["video_details"]["video"]["title"])
        video_info.set_video_image(jsonObj["settings"]["config"]["thumbnail"])
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
    except:
        video_info.set_video_stopped(True)
    return video_info

def getikey(i):
    if i == 1:
        return 226593
    elif i == 2:
        return 441252
    elif i == 3:
        return 301517
    elif i == 4:
        return 596338
    elif i == 5:
        return 852084
    else:
        return -1


def hex2bin(hexStr):
    binaryStr = ''
    for c in hexStr:
        binaryStr = binaryStr + bin(int(c, 16))[2:].zfill(4)
    return binaryStr


def bin2hex(binStr):
    hexStr = ''
    for i in range(len(binStr) - 4, -1, -4):
        oneBinStr = binStr[i:i + 4]
        hexStr = hexStr + hex(int(oneBinStr.zfill(4), 2))[2:]
    hexStr = hexStr[::-1]
    return hexStr


def decrypt(cypher, key1, key2, keySetA_1=11, keySetA_2=77213, keySetA_3=81371, keySetB_1=17, keySetB_2=92717, keySetB_3=192811, ln=None):
    
    C = list(hex2bin(cypher))
    if ln is None:
        ln = len(C) * 2
    B = int(ln * 1.5) * [None]
    
    for i in range(0, int(ln * 1.5)):
        key1 = (key1 * keySetA_1 + keySetA_2) % keySetA_3
        key2 = (key2 * keySetB_1 + keySetB_2) % keySetB_3
        B[i] = (key1 + key2) % int(ln * 0.5)

    x = y = z = 0
    
    for i in range(ln, -1 , -1):
        x = B[i]
        y = i % int(ln * 0.5)
        z = C[x]
        C[x] = C[y]
        C[y] = z

    for i in range(0, int(ln * 0.5), 1):
        C[i] = str(int(C[i]) ^ int(B[i + ln]) & 1)

    binStr = ''.join(C)
    return bin2hex(binStr)

