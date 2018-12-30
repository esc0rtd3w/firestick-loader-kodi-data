# -*- coding: latin-1 -*-

import re
from encodingUtils import smart_unicode

def findall(data,regex):
    p_reg = re.compile(regex, re.IGNORECASE + re.DOTALL + re.MULTILINE)
    result = p_reg.findall(data)
    return result

def parseTextToGroups(txt, regex):
    p = re.compile(regex, re.IGNORECASE + re.DOTALL + re.MULTILINE)
    m = p.match(smart_unicode(txt))
    if m:
        return m.groups()
    else:
        return None
    
def parseText(txt, regex, variables=[]):
    groups = parseTextToGroups(txt, regex)
    if variables == []:
        if groups:
            return groups[0]
        else:
            return ''
    else:
        resultArr = {}
        i = 0
        for v in variables:
            if groups:
                resultArr[v] = groups[i]
            else:
                resultArr[v] = ''
            i += 1
        return resultArr