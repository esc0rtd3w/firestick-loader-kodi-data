# -*- coding: latin-1 -*-

import urllib
import urlparse
import re, datetime


import common

from utils import encodingUtils as enc
from utils import datetimeUtils as dt
from utils import regexUtils as reg

from utils.xbmcUtils import select
from utils.webUtils import isOnline
from utils.fileUtils import getFileContent, fileExists



def __parseParams(params):
    seperator = "','"
    arr = params.split(seperator)
    for ndx, member in enumerate(arr):
        arr[ndx] = member.strip("'")
    return arr


def replaceFromDict(dictFilePath, wrd):

    dictionary = enc.smart_unicode(getFileContent(dictFilePath))
    dictionary = dictionary.replace('\r\n','\n')

    p_reg = re.compile('^[^\r\n]+$', re.IGNORECASE + re.DOTALL + re.MULTILINE)
    m_reg = p_reg.findall(dictionary)

    word = enc.smart_unicode(wrd).replace(u'Ãœ','&Uuml;').replace(u'Ã–','&Ouml;').replace(u'Ã„','&Auml;')
    try:
        if m_reg and len(m_reg) > 0:
            index = ''
            words = []
            newword = ''
            for m in m_reg:
                if not m.startswith(' '):
                    index = m
                    del words[:]
                else:
                    replWord = m.strip()
                    words.append(replWord)
                    if word.find(' ') != -1:
                        newword = word.replace(replWord,index)

                if (word in words) or (word == index):
                    return index

            if newword != '' and newword != word:
                return newword
    except:
        common.log('Skipped Replacement: ' + word)

    return word


def select(params,src):
    paramArr = __parseParams(params)
    title = paramArr[0]
    params = paramArr[1]
    menuItems = params.split("|")
    return select(title, menuItems)


def convDate(params, src):
    language = common.language

    if params.find("','") != -1:
        paramArr = __parseParams(params)
        oldfrmt = paramArr[0]
        newfrmt = paramArr[1]
        offsetStr = ''
        if len(paramArr) > 2:
            offsetStr = paramArr[2]
        return dt.convDate(language, src, str(oldfrmt), str(newfrmt), offsetStr)
    else:
        params = params.strip("'")
        return dt.convDate(language, src,params)


def convTimestamp(params, src):
    if params.find("','") != -1:
        paramArr = __parseParams(params)
        newfrmt = paramArr[0]
        offsetStr = paramArr[1]
        return dt.convTimestamp(src, str(newfrmt), offsetStr)
    else:
        newfrmt = params.strip("'")
        return dt.convTimestamp(src, str(newfrmt))


def offset(params, src):
    paramArr = __parseParams(params)
    t = paramArr[0].replace('%s', src)
    o = paramArr[1].replace('%s', src)

    hours = int(t.split(':')[0])
    minutes = int(t.split(':')[1])
    ti = datetime.datetime(2000, 1, 1, hours, minutes)

    offset = dt.datetimeoffset(ti, o)

    return offset.strftime('%H:%M')


def getSource(params, src):
    paramPage = ''
    paramReferer = ''
    if params.find('\',\'') > -1:
        paramPage, paramReferer = __parseParams(params)
    else:
        paramPage = params.strip('\',\'')

    paramPage = paramPage.replace('%s', src)
    return common.getHTML(paramPage, None, paramReferer)


def parseText(item, params, src):
    src = enc.smart_unicode(src)
    paramArr = __parseParams(params)

    text = paramArr[0].replace('%s',src)
    if text.startswith('@') and text.endswith('@'):
        text = item.getInfo(text.strip('@'))

    regex = paramArr[1].replace('%s', src)
    if regex.startswith('@') and regex.endswith('@'):
        regex = item.getInfo(regex.strip('@'))

    variables = []
    if len(paramArr) > 2:
        variables = paramArr[2].split('|')
    return reg.parseText(text, regex, variables)


def getInfo(item, params, src):
    src = enc.smart_unicode(src).encode('utf-8')
    paramArr = __parseParams(params)
    paramPage = paramArr[0].replace('%s', src)

    paramPage = urllib.unquote(paramPage)
    if paramPage.startswith('@') and paramPage.endswith('@'):
        paramPage = item.getInfo(paramPage.strip('@'))

    
    paramRegex = paramArr[1].replace('%s', src)
    if paramRegex.startswith('@') and paramRegex.endswith('@'):
        paramRegex = item.getInfo(paramRegex.strip('@'))
        
    referer = ''
    form_data = ''
    variables=[]
    if len(paramArr) > 2:
        referer = paramArr[2]
        referer = referer.replace('%s', src)
        if referer.startswith('@') and referer.endswith('@'):
            referer = item.getInfo(referer.strip('@'))
    if len(paramArr) > 3:
        variables = paramArr[3].strip("'").split('|')
    common.log('Get Info from: "'+ paramPage + '" from "' + referer + '"')

    try:
        parts = (paramPage.split('|', 1) + [None] * 2)[:2]
        paramPage, form_data = parts
        form_data = urlparse.parse_qsl(form_data)
    except: 
        pass

    data = common.getHTML(paramPage, form_data, referer, referer!='',demystify=True)
    return reg.parseText(data, paramRegex, variables)


def decodeBase64(src):
    src = src.strip('.js').replace('%3D','=')
    try:
        return src.decode('base-64').replace('qo','')
    except:
        return src


def decodeRawUnicode(src):
    try:
        return enc.decodeRawUnicode(src)
    except:
        return src


def replace(params, src):
    src = enc.smart_unicode(src)
    paramArr = __parseParams(enc.smart_unicode(params))
    paramstr = paramArr[0].replace('%s', src)
    paramSrch = paramArr[1]
    paramRepl = paramArr[2]
    return paramstr.replace(paramSrch,paramRepl)


def replaceRegex(params, src):
    src = enc.smart_unicode(src)
    paramArr = __parseParams(params)
    paramStr = paramArr[0].replace('%s', src)
    paramSrch = paramArr[1]
    paramRepl = paramArr[2]

    r = re.compile(paramSrch, re.DOTALL + re.IGNORECASE)
    ms = r.findall(paramStr)
    if ms:
        for m in ms:
            paramStr = paramStr.replace(m, paramRepl,1)
        return paramStr
    return src


def resolveVariable(item, param):
    if param.startswith('@') and param.endswith('@'):
        return item.getInfo(param.strip('@'))
    return param
    

def ifEmpty(item, params, src):
    paramArr = __parseParams(params)

    paramSource = resolveVariable(item, paramArr[0].replace('%s', src))
    paramTrue = resolveVariable(item, paramArr[1].replace('%s', src))
    paramFalse = resolveVariable(item, paramArr[2].replace('%s', src))

    if paramSource == '':
        return paramTrue
    else:
        return paramFalse


def isEqual(item, params, src):
    paramArr = __parseParams(params)
    paramSource = resolveVariable(item, paramArr[0].replace('%s', src))
    paramComp = resolveVariable(item, paramArr[1].replace('%s', src))
    paramTrue = resolveVariable(item, paramArr[2].replace('%s', src))
    paramFalse = resolveVariable(item, paramArr[3].replace('%s', src))

    if (paramSource == paramComp):
        return paramTrue
    else:
        return paramFalse


def ifFileExists(item, params, src):
    paramArr = __parseParams(params)
    paramSource = resolveVariable(item, paramArr[0].replace('%s', src))
    paramTrue = resolveVariable(item, paramArr[1].replace('%s', src))
    paramFalse = resolveVariable(item, paramArr[2].replace('%s', src))

    if fileExists(paramSource):
        return paramTrue
    else:
        return paramFalse    


def ifExists(item, params, src):
    paramArr = __parseParams(params)
    paramSource = resolveVariable(item, paramArr[0].replace('%s', src))
    paramTrue = resolveVariable(item, paramArr[1].replace('%s', src))
    paramFalse = resolveVariable(item, paramArr[2].replace('%s', src))

    if isOnline(paramSource):
        return paramTrue
    else:
        return paramFalse


def urlMerge(params, src):
    paramArr = __parseParams(params)
    paramTrunk = paramArr[0].replace('%s', src).replace("\t","")
    paramFile= paramArr[1].replace('%s', src).replace("\t","")

    if not paramFile.startswith('http'):
        from urlparse import urlparse
        up = urlparse(urllib.unquote(paramTrunk))
        if paramFile.startswith('/'):
            return urllib.basejoin(up[0] + '://' + up[1], paramFile)
        else:
            return urllib.basejoin(up[0] + '://' + up[1] + '/' + up[2],paramFile)
    return src