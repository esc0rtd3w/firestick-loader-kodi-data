
#
#      Copyright (C) 2015 Mikey1234
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
#  This code is a derivative of the YouTube plugin for XBMC and associated works
#  released under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3


import re
import requests
from types import *



def getNested(s, delim=("(", ")")):
        level = 0
        pos = 0
        for c in s:
                pos+=1
                if c == delim[0]:
                        level +=1
                elif c == delim[1]:
                        level -=1
                if level == -1: 
                        return pos-1
        print "Couldn't find matching - level ", level
        return s
indent = -1
def solveEquation(q):
        global indent
        indent +=1
        pos = 0
        res = 0
        stringify = False
        if q[0] == "!":
                stringify = True
        while pos < len(q):
                if q[pos] == "(":
                        nested = getNested(q[pos+1:len(q)])
                        nres = solveEquation(q[pos+1:pos+1+nested])
                        if type(nres) is StringType and type(res) is not StringType :
                                res = str(res)+nres
                        elif type(res) == StringType and type(nres) is IntType:
                                res = res + str(nres)
                        else:
                                res +=nres
                        pos+=nested+1
                elif q[pos] == ")":
                        pass
                        pos+=1
                elif q[pos:pos+4] == "!+[]":
                        res+=1
                        pos+=4
                elif q[pos:pos+5] == "+!![]":
                        res+=1
                        pos+=5
                elif q[pos:pos+3] == "+[]":
                        pos+=3
                elif q[pos:pos+2] == "+(":
                        pos+=1
                # we dont care about whitespaces
                elif q[pos] == " ": 
                        pos+=1
                elif q[pos] == "\t":
                        pos+=1
                else: 
                        print '\t'*indent, "Unknown", q[pos:pos+6]
                        break
        
        indent -=1
        if stringify:
                return str(res)
        return res

def solve(url,cookie_file='',UA='',timed='',wait=True):
        if UA=='':
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        solverregex = re.compile('var s,t,o,p,b,r,e,a,k,i,n,g,f, (.+?)={"(.+?)":(.+?)};.+challenge-form\'\);.*?\n.*?;(.*?);a\.value',  re.DOTALL)
        vcregex = re.compile('<input type="hidden" name="jschl_vc" value="([^"]+)"/>')
        headers={'User-Agent' : UA,'Referer':url}       
        
        request = requests.get(url,headers=headers).content
        passv = re.compile('<input type="hidden" name="pass" value="([^"]+)"/>').findall(request)[0]
        res = solverregex.findall(request)

        res=res[0]
        vc = vcregex.findall(request)

        vc = vc[0]

        varname = (res[0], res[1])
        solved = int(solveEquation(res[2].rstrip()))

        for extra in res[3].split(";"):
                extra = extra.rstrip()
                if extra[:len('.'.join(varname))] != '.'.join(varname):
                        print "fuck all"
                else:
                        extra = extra[len('.'.join(varname)):]
                if extra[:2] == "+=":
                        solved += int(solveEquation(extra[2:]))
                elif extra[:2] == "-=":
                        solved -= int(solveEquation(extra[2:]))
                elif extra[:2] == "*=":
                        solved *= int(solveEquation(extra[2:]))
                elif extra[:2] == "/=":
                        solved /= int(solveEquation(extra[2:]))
                else:
                        print "Unknown modifier"
       

        http=url.split('//')[0]
        domain1=url.split('//')[1]
        domain=domain1.split('/')[0]
        solved += len(domain)
   
        
        from entertainment.net import Net
        net = Net(cached=False)
        
        if wait ==True:
                
                import time
                if not timed == '':
                    print 'Sleepin for '+ str(timed) +' Seconds'
                    time.sleep(int(timed))
                    
                else:
                    print 'Sleepin for 6 Seconds'    
                    time.sleep(6)
        
        final = net.http_POST(http+"//"+domain+"/cdn-cgi/l/chk_jschl?jschl_vc={0}&pass={1}&jschl_answer={2}".format(vc,passv, solved),'',headers=headers)

        if not cookie_file == '':
            net.save_cookies(cookie_file)
            

                

             
        return final.content

        
