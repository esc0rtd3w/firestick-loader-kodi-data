# -*- coding: utf-8 -*-
"""
    SALTS XBMC Addon
    Copyright (C) 2017 tknorris
    Derived from pelisalacarta - XBMC Plugin (@robalo & @Cmos)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re

def is_aaencoded(text):
    return text.find('ﾟωﾟﾉ=/｀ｍ´）ﾉ ~┻━┻') > -1 and text.find("(ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');") > -1

def decode(text):
    text = re.sub(r"\s+|/\*.*?\*/", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)", "u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)

        c = ''
        subchar = ''
        for v in char:
            c += v
            try:
                x = c
                subchar += str(eval(x))
                c = ''
            except:
                pass
            
        if subchar:
            txt += subchar + '|'
            
    txt = txt[:-1].replace('+', '')
    txt_result = ''.join([chr(int(n, 8)) for n in txt.split('|')])

    return toStringCases(txt_result)

def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in txt_result:
            m3 = True
            match = re.search(".toString...(\d+).", txt_result)
            sum_base = "+" + match.group(1) if match else ''
            txt_pre_temp = re.findall("..(\d+),(\d+).", txt_result, re.DOTALL)
            txt_temp = [(n, b) for b, n in txt_pre_temp]
        else:
            txt_temp = re.findall('(\d+)\.0.\w+.([^\)]+).', txt_result, re.DOTALL)
            
        for number, base in txt_temp:
            code = to_base(int(number), eval(base + sum_base))
            if m3:
                txt_result = txt_result.replace('(%s,%s)' % (base, number), code)
            else:
                txt_result = txt_result.replace('%s.0.toString(%s)' % (number, base), code)
            txt_result = re.sub(r"'|\+", '', txt_result)
    return txt_result

def to_base(n, base, digits="0123456789abcdefghijklmnopqrstuvwxyz"):
    n, base = int(n), int(base)
    if n < base:
        return digits[n]
    else:
        return to_base(n // base, base, digits).lstrip(digits[0]) + digits[n % base]
