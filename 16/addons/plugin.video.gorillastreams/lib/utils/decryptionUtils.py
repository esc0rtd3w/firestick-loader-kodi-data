# -*- coding: latin-1 -*-

import pyDes
import urllib
import re

from regexUtils import parseTextToGroups
from webUtils import get_redirected_url

from javascriptUtils import JsFunctions, JsUnpacker,JsUnpackerV2, JsUnwiser, JsUnIonCube


def encryptDES_ECB(data, key):
    data = data.encode()
    k = pyDes.des(key, pyDes.ECB, IV=None, pad=None, padmode=pyDes.PAD_PKCS5)
    d = k.encrypt(data)
    assert k.decrypt(d, padmode=pyDes.PAD_PKCS5) == data
    return d

def encryptJimey(data):
    result = encryptDES_ECB(data,"PASSWORD").encode('base64').replace('/','').strip()
    return result

# used by 24cast
def destreamer(s):
    #remove all but[0-9A-Z]
    string = re.sub("[^0-9A-Z]", "", s.upper())
    result = ""
    nextchar = ""
    for i in range(0,len(string)-1):
        nextchar += string[i]
        if len(nextchar) == 2:
            result += ntos(int(nextchar,16))
            nextchar = ""
    return result

def ntos(n):
    n = hex(n)[2:]
    if len(n) == 1:
        n = "0" + n
    n = "%" + n
    return urllib.unquote(n)

def doDemystify(data):

    #init jsFunctions and jsUnpacker
    jsF = JsFunctions()
    jsU = JsUnpacker()
    jsUV2 =JsUnpackerV2()
    jsUW = JsUnwiser()
    jsUI = JsUnIonCube()

    # replace NUL
    data = data.replace('\0','')

    # unescape
    r = re.compile('unescape\(\s*["\']([^\'"]+)["\']')
    gs = r.findall(data)
    if gs:
        for g in gs:
            quoted=g
            data = data.replace(quoted, urllib.unquote_plus(quoted))

    # n98c4d2c
    if 'function n98c4d2c(' in data:
        gs = parseTextToGroups(data, ".*n98c4d2c\(''\).*?'(%[^']+)'.*")
        if gs != None and gs != []:
            data = data.replace(gs[0], jsF.n98c4d2c(gs[0]))

    # o61a2a8f
    if 'function o61a2a8f(' in data:
        gs = parseTextToGroups(data, ".*o61a2a8f\(''\).*?'(%[^']+)'.*")
        if gs != None and gs != []:
            data = data.replace(gs[0], jsF.o61a2a8f(gs[0]))

    # RrRrRrRr
    if 'function RrRrRrRr(' in data:
        r = re.compile("(RrRrRrRr\(\"(.*?)\"\);)</SCRIPT>", re.IGNORECASE + re.DOTALL)
        gs = r.findall(data)
        if gs != None and gs != []:
            for g in gs:
                data = data.replace(g[0], jsF.RrRrRrRr(g[1].replace('\\','')))

    # hp_d01
    if 'function hp_d01(' in data:
        r = re.compile("hp_d01\(unescape\(\"(.+?)\"\)\);//-->")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, jsF.hp_d01(g))

    # ew_dc
    if 'function ew_dc(' in data:
        r = re.compile("ew_dc\(unescape\(\"(.+?)\"\)\);</SCRIPT>")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, jsF.ew_dc(g))

    # pbbfa0
    if 'function pbbfa0(' in data:
        r = re.compile("pbbfa0\(''\).*?'(.+?)'.\+.unescape")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, jsF.pbbfa0(g))


    # util.de
    if 'Util.de' in data:
        r = re.compile("Util.de\(unescape\(['\"](.+?)['\"]\)\)")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g,g.decode('base64'))

    # 24cast
    if 'destreamer(' in data:
        r = re.compile("destreamer\(\"(.+?)\"\)")
        gs = r.findall(data)
        if gs:
            for g in gs:
                data = data.replace(g, destreamer(g))


    # Tiny url
    r = re.compile('[\'"](http://(?:www.)?tinyurl.com/[^\'"]+)[\'"]',re.IGNORECASE + re.DOTALL)
    m = r.findall(data)
    if m:
        for tiny in m:
            data = data.replace(tiny, get_redirected_url(tiny))


    # JS P,A,C,K,E,D
    if jsU.containsPacked(data):
        data = jsU.unpackAll(data)
        
    escape_again=False
    #if still exists then apply v2
    if jsUV2.containsPacked(data):
        data = jsUV2.unpackAll(data)
        escape_again=True

    # JS W,I,S,E
    if jsUW.containsWise(data):
        data = jsUW.unwiseAll(data)
        escape_again=True

    # JS IonCube
    if jsUI.containsIon(data):
        data = jsUI.unIonALL(data)
        escape_again=True

    # unescape again
    if escape_again:
        r = re.compile('unescape\(\s*["\']([^\'"]+)["\']')
        gs = r.findall(data)
        if gs:
            for g in gs:
                quoted=g
                data = data.replace(quoted, urllib.unquote_plus(quoted))            
    return data

    
