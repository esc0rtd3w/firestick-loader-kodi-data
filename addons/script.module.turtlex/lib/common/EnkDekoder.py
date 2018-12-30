'''
Created on May 17, 2013

@author: ajju
'''
import re

def _enk_dec_num(kode, enc):
    if re.search('fromCharCode', enc):
        x = ''
        for nbr in kode.split():
            x += chr(int(nbr) - 3)
        return x
    else:
        return None
    
def _enk_dec_swap(kode, enc):
    if re.search('charAt', enc) and not re.search('@', enc):
        x = ''
        i = 0
        while i < (len(kode) - 1):
            x += (kode[i + 1] + kode[i])
            i += 2
        return (x + (kode[len(kode) - 1] if i < len(kode) else ''))
    else:
        return None

def _enk_dec_skip(kode, enc):
    if re.search('charAt', enc) and re.search('@', enc):
        x = ''
        i = 0
        while i < len(kode):
            if(kode[i] == '|' and kode[i + 1] == '|'):
                x += '@'
            else:
                x += kode[i]
            i += 2
        return x
    else:
        return None
    
def _enk_dec_reverse(kode, enc):
    if re.search('reverse', enc):
        return kode[::-1]
    else:
        return None
    
ENK_DEC_FUNC = [_enk_dec_num, _enk_dec_skip, _enk_dec_swap, _enk_dec_reverse]


def dekode(html):
    kodeParts = re.compile('var kode\="kode\=\\\\"(.+?)\\\\";(.+?);"').findall(html)
    if len(kodeParts) == 0:
        return None
    kode = None
    while len(kodeParts) == 1:
        kode = kodeParts[0][0].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        enc = kodeParts[0][1].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        for dec_func in ENK_DEC_FUNC:
            x = dec_func(kode, enc)
            if x is not None:
                kode = x
        kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))
    dekoded = kode.replace('\\"', '"').replace('\\\'', '\'').replace('\\\\', '\\')
    return dekoded
