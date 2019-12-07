#############################################################################
#
#   Copyright (C) 2013 Navi-X
#
#   This file is part of Navi-X.
#
#   Navi-X is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   Navi-X is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Navi-X.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

#############################################################################
#
# CURLLoader:
# This class Retrieves the URL to a media item which the XBMC player
# understands.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import zipfile
from libs2 import *
from settings import *
from CFileLoader import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

class CURLLoader:
    def __init__(self, parent=0):
        self.parent=parent
        self.processed=False

######################################################################
# Description: This class is used to retrieve the direct URL of given
#              URL which the XBMC player understands.
#              
# Parameters : URL=source URL, mediaitem = mediaitem to open
# Return     : 0=successful, -1=fail
######################################################################
    def urlopen(self, URL, mediaitem=0):
        result = {"code":0} #successful
        try: import urlresolver; 
        except: pass
        try:
        	#import urlresolver; 
        	if urlresolver.HostedMediaFile(mediaitem.URL).valid_url()==True:
        		print "CURLL line64 valid url for local UrlResolver"; 
        		self.loc_url=urlresolver.HostedMediaFile(mediaitem.URL).resolve(); print "CURLL searchline65 loc_url: "+ str(self.loc_url); 
        		if '://' in self.loc_url: self.processed=True; return {"code":0}; 
        except urllib2.URLError, e: print e; pass
        except Exception, e: print e; pass
        except: pass
        
        if mediaitem.processor != '':
          #if tfalse(SettingG("use-LocalUrlResolver"))==True:
          #  try:
          #    #import urlresolver; 
          #    print "using urlresolver method"; print "mediaitem.URL"; 
          #    if urlresolver.HostedMediaFile(mediaitem.URL).valid_url()==True:
          #      print "valid url"; 
          #      self.loc_url=urlresolver.HostedMediaFile(mediaitem.URL).resolve(); print "loc_url:"; print self.loc_url; 
          #      self.processed=True; return {"code":0}; 
          #  except: ## Fall back to site processors
          #    result=self.geturl_processor(mediaitem)
          #else: 
          result=self.geturl_processor(mediaitem)
          #print "======================================="; print mediaitem.processor; print mediaitem.URL; print result; print "======================================="; 
        elif URL.find('http://www.youtube.com') != -1:
          #if tfalse(SettingG("use-LocalUrlResolver"))==True:
          #  try:
          #    import urlresolver; print "using urlresolver method"; print "mediaitem.URL"; 
          #    if urlresolver.HostedMediaFile(mediaitem.URL).valid_url():
          #      print "valid url"; 
          #      self.loc_url=urlresolver.HostedMediaFile(mediaitem.URL).resolve(); print "loc_url:"; print self.loc_url; 
          #      self.processed=True; return {"code":0}; 
          #  except: ## Fall back to site processors
          #    mediaitem.processor="http://www.navixtreme.com/proc/youtube"; 
          #    result=self.geturl_processor(mediaitem); 
          #else:
          mediaitem.processor="http://www.navixtreme.com/proc/youtube"; 
          result=self.geturl_processor(mediaitem); 
          #print "======================================="; print URL; print mediaitem.processor; print mediaitem.URL; print result; print "======================================="; 
        elif URL[:4] == 'http':
            if mediaitem.processed==True:
                self.loc_url=mediaitem.URL
            else:
                result=self.geturl_redirect(URL,mediaitem) 
        else:
            self.loc_url=URL
        print "======================================="; print URL; print mediaitem.processor; print mediaitem.URL; print result; print "======================================="; 
        try:
          if (not result["code"] == 0) and ('http' in mediaitem.URL): ## Thus far result['code'] seems to be 0 even if online processor fails.
              #import urlresolver; 
              #if (URL.find('http://www.youtube.com') != -1) or (mediaitem.processor=="http://www.navixtreme.com/proc/youtube"): return result
              print "using urlresolver method as final fallback attempt"; print "mediaitem.URL"; 
              if urlresolver.HostedMediaFile(mediaitem.URL).valid_url()==True:
                print "valid url"; 
                self.loc_url=urlresolver.HostedMediaFile(mediaitem.URL).resolve(); print "loc_url:"; print self.loc_url; 
                self.processed=True; result={"code":0}; 
        except: pass
        return result

######################################################################
# Description: This class is used to retrieve the real URL of 
#              a media item. The XBMC player sometimes fails to handle
#              HTTP redirection. Therefore we do it here.
# Parameters : URL=source URL
# Return     : 0=successful, -1=fail
######################################################################
    def geturl_redirect(self, URL, entry):

        try:
            URL=self.loc_url
        except AttributeError:
            try:
                URL=entry.URL
            except AttributeError:
                print "geturl_redirect from vanilla URL"

        URL, headers=parse_headers(URL, entry)

        try:
            req = urllib2.Request(URL, None, headers)
            f = urllib2.urlopen(req)
            self.loc_url=f.geturl()
            f.close()            
        except IOError:
            return {"code": 1} # failed

        #always return true    
        return {"code":0}

######################################################################
# Description: Retrieve playback parameters using a remote processor
#
# Parameters : mediaitem = mediaitem to open
# Return     : 0=successful, -1=fail
######################################################################
    def geturl_processor(self, mediaitem):
        cache_filename=procCacheDir + ProcessorLocalFilename(mediaitem.processor)
        is_cached=False
        proc_ori=""
        htmRaw=""
        if cache_filename>"" and os.path.exists(cache_filename):
            # use cached processor if no older than 24 hours
            if os.path.getmtime(cache_filename) + 60*60*24 > time.mktime(time.gmtime()):
                try:
                    htmRaw=open(cache_filename, 'r').read()
                    is_cached=True
                    print "Processor: phase 1 - query\n URL: "+mediaitem.URL+"\n Processor (cached): "+mediaitem.processor
                except IOError:
                    pass

        if htmRaw=="":
            print "Processor: phase 1 - query\n URL: "+mediaitem.URL+"\n Processor: "+mediaitem.processor
            SetInfoText("Processor: getting filter...")
            #print 'mediaitem.processor'; print mediaitem.processor; 
            #mediaitem.processor=mediaitem.processor.replace('navi','n_a_v_i'); print mediaitem.processor; 
            htmRaw=getRemote(mediaitem.processor+'?url='+urllib.quote_plus(mediaitem.URL),{'cookie':'version='+Version+'.'+SubVersion+'; platform='+platform})['content']
            #print "testing for htmRaw"; 
            #print htmRaw; 
            #if ("urllib2.URLError" in htmRaw) or ("urllib2.URLError" in htmRaw):
            proc_ori=htmRaw

        if htmRaw <= '':
            return self.proc_error("nothing returned from learning phase")

        if htmRaw[:2]=='v2':
            htmRaw=htmRaw[3:]
            inst=htmRaw
            htmRaw=''
            phase=0
            exflag=False
            phase1complete=False
            verbose=0
            proc_args=''
            inst_prev=''
            headers={}

            v=NIPLVars()

            ## no-argument command detection
            noarg_parse=re.compile('^(scrape|play|report|else|endif|endwhile)$')

            ## flow control statements
            fcparse=re.compile('^(if|endif|while|endwhile)$')

            ## command parser
            lparse=re.compile('^([^ =]+)([ =])(.+)$')

            ## dot property parser
            dotvarparse=re.compile('^(nookies|s_headers)\.(.+)$')

            self.multiIfTest=re.compile('^\(')
            self.conditionExtract=re.compile('\(\s*([^\(\)]+)\s*\)')
            self.ifparse=re.compile('^([^<>=!]+)\s*([!<>=]+)\s*(.+)$')


            nookies=NookiesRead(mediaitem.processor)
            for ke in nookies:
                hkey='nookies.'+ke
                v[hkey]=nookies[ke]['value']

            while exflag==False:
                scrape=1
                phase=phase+1
                rep={}

                control_stack=[]
                control_stacklen=0

                src_printed=False

                ## load defaults into v, leave undefined keys alone
                v.reset()

                ## get instructions if args present
                if proc_args>'':
                    SetInfoText("Processor: phase "+str(phase)+" learn")
                    print "Processor: phase "+str(phase)+" learn"
                    inst=getRemote(mediaitem.processor+'?'+proc_args)['content']
                    proc_args=''
                elif phase1complete:
                    SetInfoText("")
                    print "Processor error: nothing to do"
                    exflag=True
                else:
                    v['s_url']=mediaitem.URL

                if inst==inst_prev:
                    return self.proc_error("endless loop detected")

                inst_prev=inst
                v['NIPL']=inst
                lines=inst.splitlines()
                eof=len(lines)
                if eof < 1:
                    return self.proc_error("nothing returned from phase "+str(phase))

                linenum=-1
                while linenum<eof:
                    # Note: while loop will need to set linenum to linenum-1 since it is incremented at start of block
                    linenum=linenum+1
                    self.linenum_display=linenum+2
                    line=re.sub('^\s*', '', lines[linenum])
                    self.line_display=line

                    if verbose>0 and src_printed==False:
                        print "Processor NIPL source:\n"+inst
                        src_printed=True

                    if line>'' and verbose>1:
                        str_report="NIPL line "+str(linenum)+": "+line

                    # skip comments and blanks
                    if line[:1]=='#' or line[:2]=='//' or line=='':
                        continue

                    # parse subj & args
                    subj='';
                    arg='';
                    is_assignment=False

                    match=noarg_parse.search(line)
                    if match:
                        subj=match.group(1)
                        #print "noarg_parse match"
                    else:
                        match=lparse.search(line)
                        #print "MG ["+match.group(1)+"], ["+match.group(2)+"], ["+match.group(3)+"]"
                        if match is None:
                            return self.proc_error("syntax error: "+line)
                        subj=match.group(1)
                        arg=match.group(3)
                        if match.group(2)=='=':
                            is_assignment=True

                    if verbose>2:
                        print "-----------------------------"
                        print line

                    ### flow control

                    cflag=False
                    if control_stacklen>0:

                        l=control_stack[-1]
                        if v["debug_flow"] > "":
                            print "control type:"+l["type"]+" block_do:"+str(l["block_do"])+" child_depth:"+str(l["child_depth"])

                        # nested condition tracking
                        if control_stack[-1]["block_do"]==False and (subj=='if' or subj=='while'):
                            control_stack[-1]["child_depth"]=control_stack[-1]["child_depth"]+1
                            if v["debug_flow"]>"":
                                print "Child depth: "+str(control_stack[-1]["child_depth"])

                        if control_stack[-1]["child_depth"]>0 and (subj=='endif' or subj=='endwhile'):
                            control_stack[-1]["child_depth"]=control_stack[-1]["child_depth"]-1
                            cflag=True
                            if v["debug_flow"]>"":
                                print "Child depth: "+str(control_stack[-1]["child_depth"])

                        if control_stack[-1]["child_depth"]>0 or cflag:
                            if v["debug_flow"]>"":
                                print "    ^^^ skipped: child"
                            continue

                        # current-level logic
                        if control_stack[-1]["type"]=='if' and subj!='elseif' and subj!='else' and subj!='endif' and control_stack[-1]["block_do"]==False:
                            if v["debug_flow"]>"":
                                print "    ^^^ skipped: if"
                            continue
                        elif control_stack[-1]["type"]=='while' and subj!='endwhile' and control_stack[-1]["block_do"]==False:
                            if v["debug_flow"]>"":
                                print "    ^^^ skipped: while"
                            continue


                    ### if / elseif / else / endif

                    if subj=='if':
                        boolObj=self.if_eval(arg, v)
                        if(boolObj["error"]==True):
                            return self.proc_error(boolObj["data"] + "\n" + line)

                        control_stack.append({
                        	"block_do": boolObj["data"],
                        	"if_satisfied": boolObj["data"],
                        	"type": "if",
                        	"child_depth": 0
                        })
                        control_stacklen=len(control_stack)

                    elif subj=='elseif':
                        if control_stacklen==0 or control_stack[-1]["type"]!='if':
                            return self.proc_error("elseif without if")
                        if control_stack[-1]["if_satisfied"]:
                            control_stack[-1]["block_do"]=False
                        else:
                            boolObj=self.if_eval(arg, v)
                            if(boolObj["error"]==True):
                                return self.proc_error(boolObj["data"] + "\n" + line)
                            control_stack[-1]["if_satisfied"]=boolObj["data"]
                            control_stack[-1]["block_do"]=boolObj["data"]

                    elif subj=='else':
                        if control_stacklen==0 or control_stack[-1]["type"]!='if':
                            return self.proc_error("else without if")
                        control_stack[-1]["block_do"]=not control_stack[-1]["if_satisfied"]

                    elif subj=='endif':
                        if control_stacklen==0 or control_stack[-1]["type"]!='if':
                            return self.proc_error("endif without if")
                        control_stack.pop()
                        control_stacklen=len(control_stack)

                    ### while / endwhile

                    elif subj=='while':
                        control_stack.append({
                        	"type": "while",
                        	"block_do": True,
                        	"loopstart": linenum,
                        	"execcount": 0,
                        	"child_depth": 0
                        })
                        control_stacklen=len(control_stack)

                        # determine loop type
                        wmatch=lparse.search(arg)
                        if wmatch is None:
                            return self.proc_error("syntax error: "+line)
                        wsubj=wmatch.group(1)
                        warg=wmatch.group(3)
                        if wsubj=='match':
                            control_stack[-1]["subtype"]='re'
                            control_stack[-1]["regex"]=re.compile(v['regex'])
                            control_stack[-1]["haystack"]=v[warg]
                            control_stack[-1]["searchstart"]=0
                        else:
                            return self.proc_error("unrecognized while condition '"+wsubj+"'")

                        wresult=self.while_eval(control_stack[-1],v)
                        if wresult["error"]:
                            return self.proc_error(wresult["message"])
                        if verbose>1:
                            print wresult["message"]

                    elif subj=='endwhile':

                        if control_stacklen==0 or control_stack[-1]["type"]!='while':
                            return self.proc_error("endwhile without while")
                        wresult=self.while_eval(control_stack[-1],v)
                        if wresult["error"]:
                            return self.proc_error(wresult["message"])
                        if verbose>1:
                            print wresult["message"]
                        if wresult["match"]:
                            linenum=control_stack[-1]["loopstart"]
                        else:
                            control_stack.pop()
                            control_stacklen=len(control_stack)
                            continue

                    ### standard methods / commands

                    elif subj=='scrape':
                        str_info="Processor:"
                        if phase>1:
                            str_info=str_info+" phase "+str(phase)
                        str_info=str_info+" scrape"
                        if scrape>1:
                            str_info=str_info+" "+str(scrape)
                        SetInfoText(str_info)
                        if v['s_url']=='':
                            return self.proc_error("no scrape URL defined")
                        scrape=scrape+1
                        scrape_args={
                          'referer': v['s_referer'],
                          'cookie': v['s_cookie'],
                          'method': v['s_method'],
                          'agent': v['s_agent'],
                          'action': v['s_action'],
                          'postdata': v['s_postdata'],
                          'headers': headers
                        }
                        print "Processor "+v['s_method'].upper()+"."+v['s_action']+": "+v['s_url']
                        if verbose>0:
                            print "Proc debug remote args:"
                            print scrape_args
                        remoteObj=getRemote(v['s_url'], scrape_args)
                        #print remoteObj


                        v['htmRaw']=remoteObj['content']
                        v['geturl']=remoteObj['geturl']
                        # backwards-compatibility for pre 3.5.4
                        if v['s_action']=='geturl':
                            v['v1']=v['geturl']
                        str_out="Proc debug headers:"
                        for ke in remoteObj['headers']:
                            hkey='headers.'+ke
                            str_out=str_out+"\n "+ke+": "+str(remoteObj['headers'][ke])
                            v[hkey]=str(remoteObj['headers'][ke])
                        if verbose>0:
                            print str_out

                        str_out="Proc debug cookies:"
                        for ke in remoteObj['cookies']:
                            hkey='cookies.'+ke
                            str_out=str_out+"\n "+ke+": "+str(remoteObj['cookies'][ke])
                            v[hkey]=str(remoteObj['cookies'][ke])
                        if verbose>0:
                            print str_out

                        if v['s_action']=='read' and v['regex']>'' and v['htmRaw']>'':
                            # get finished - run regex, populate v(alues) and rep(ort) if regex is defined
                            v['nomatch']=''
                            rep['nomatch']=''
                            for i in range(1,11):
                                ke='v'+str(i)
                                v[ke]=''
                                rep[ke]=''
                            p=re.compile(v['regex'])
                            match=p.search(v['htmRaw'])
                            if match:
                                rerep='Processor scrape:'
                                for i in range(1,len(match.groups())+1):
                                    val=match.group(i)
                                    if val is None:
                                        val=''
                                    key='v'+str(i)
                                    rerep=rerep+"\n "+key+'='+val
                                    rep[key]=val
                                    v[key]=val
                                if verbose>0:
                                    print rerep

                            else:
                                if verbose>0:
                                    print 'Processor scrape: no match'
                                rep['nomatch']=1
                                v['nomatch']=1

                        # reset scrape params to defaults
                        v.reset('scrape')

                    elif subj=='play':
                        if verbose==1:
                            print "Proc debug: play"
                        exflag=True
                        break

                    elif subj=='report':
                        rep['phase']=str(phase)
                        proc_args=urllib.urlencode(rep)
                        proc_args=re.sub('v\d+=&','&',proc_args)
                        proc_args=proc_args.replace('nomatch=&','&')
                        proc_args=re.sub('&+','&',proc_args)
                        proc_args=re.sub('^&','',proc_args)
                        str_report="Processor report:"
                        for ke in rep:
                            if rep[ke]>'':
                                str_report=str_report+"\n "+ke+": "+rep[ke]
                        print str_report
                        break

                    elif subj=='verbose':
                        verbose=int(arg)

                    elif subj=='error':
                        if arg[0:1]=="'":
                            errmsg=arg[1:]
                        else:
                            errmsg=v[arg]
                        return self.proc_error(errmsg)

                    elif subj=='report_val':
                        match=lparse.search(arg)
                        if match is None:
                            return self.proc_error("syntax error: "+line)
                        ke=match.group(1)
                        va=match.group(3)
                        if va[0:1]=="'":
                            rep[ke]=va[1:]
                            if verbose>0:
                                print "Proc debug report value: "+ke+" set to string literal\n "+va[1:]
                        else:
                            rep[ke]=v[va]
                            if verbose>0:
                                print "Proc debug report value: "+ke+" set to "+va+"\n "+v[va]

                    elif subj=='concat':
                        match=lparse.search(arg)
                        if match is None:
                            return self.proc_error("syntax error: "+line)
                        ke=match.group(1)
                        va=match.group(3)
                        oldtmp=v[ke]
                        if va[0:1]=="'":
                            v[ke]=v[ke]+va[1:]
                        else:
                            v[ke]=v[ke]+v[va]
                        if verbose>0:
                            print "Proc debug concat:\n old="+oldtmp+"\n new="+v[ke]

                    elif subj=='match':
                        v['nomatch']=''
                        rep['nomatch']=''
                        for i in range(1,11):
                            ke='v'+str(i)
                            v[ke]=''
                            rep[ke]=''
                        p=re.compile(v['regex'])
                        try:
                            match=p.search(v[arg])
                        except TypeError:
                            v['nomatch']=1

                        if match:
                            rerep='Processor match '+arg+':';
                            for i in range(1,len(match.groups())+1):
                                val=match.group(i)
                                if val is None:
                                    val=''
                                key='v'+str(i)
                                rerep=rerep+"\n "+key+'='+val
                                v[key]=val
                            if verbose>0:
                                print rerep

                        else:
                            if verbose>0:
                                print "Processor match: no match\n regex: "+v['regex']+"\n search: "+v[arg]
                            v['nomatch']=1

                    elif subj=='replace':
                       # pre-set regex, replace var [']val
                        match=lparse.search(arg)
                        if match is None:
                            return self.proc_error("syntax error: "+line)
                        ke=match.group(1)
                        va=match.group(3)
                        if va[0:1]=="'":
                            va=va[1:]
                        else:
                            va=v[va]
                        oldtmp=v[ke]
                        v[ke]=re.sub(v['regex'], va, v[ke])
                        if verbose>0:
                            print "Proc debug replace "+ke+":\n old="+oldtmp+"\n new="+v[ke]

                    elif subj=='unescape':
                        oldtmp=v[arg]
                        v[arg]=urllib.unquote(v[arg])
                        if verbose>0:
                            print "Proc debug unescape:\n old="+oldtmp+"\n new="+v[arg]

                    elif subj=='escape':
                        oldtmp=v[arg]
                        v[arg]=urllib.quote_plus(v[arg])
                        if verbose>0:
                            print "Proc debug escape:\n old="+oldtmp+"\n new="+v[arg]

                    elif subj=='debug':
                        if verbose>0:
                            try:
                                print "Processor debug "+arg+":\n "+v[arg]
                            except KeyError:
                                print "Processor debug "+arg+" - does not exist\n"

                    elif subj=='print':
                        if arg[0:1]=="'":
                            print "Processor print: "+arg[1:]
                        else:
                            print "Processor print "+arg+":\n "+v[arg]

                    elif subj=='countdown':
                        if arg[0:1]=="'":
                            secs=arg[1:]
                        else:
                            secs=v[arg]
                        cd_flag=countdown_timer(int(secs), v['countdown_title'], v['countdown_caption'])
                        if cd_flag==False:
                            SetInfoText("")
                            return {"code":0}

                    elif subj=='show_playlist':
                        if arg[0:1]=="'":
                            purl=arg[1:]
                        else:
                            purl=v[arg]
                        print "Processor: redirecting to playlist " + purl
                        return { "code":2, "data":purl }

                    elif is_assignment:
                        # assignment operator
                        if arg[0:1]=="'":
                            val=arg[1:]
                            areport="string literal"
                        else:
                            val=v[arg]
                            areport=arg

                        match=dotvarparse.search(subj);
                        if match:
                            dp_type=match.group(1)
                            dp_key=match.group(2)
                            tsubj=dp_key
                            if dp_type=='nookies':
                                # set nookie
                                treport="nookie"
                                NookieSet(mediaitem.processor, dp_key, val, v['nookie_expires'])
                                v[subj]=val

                            elif dp_type=='s_headers':
                                # set scrape header
                                treport="scrape header"
                                headers[dp_key]=val

                        else:
                            # set variable
                            treport="variable"
                            tsubj=subj
                            v[subj]=val

                        if verbose>0:
                            print "Proc debug "+treport+": "+tsubj+" set to "+areport+"\n "+val

                    else:
                        return self.proc_error("unrecognized method '"+subj+"'")

            if v['referer']>'':
                mediaitem.referer=v['referer']
            if v['agent']>'':
                v['url']=v['url']+'?|User-Agent='+v['agent']
                mediaitem.agent=v['agent']
            mediaitem.URL=v['url']
            if useLibrtmp and (v['playpath']>'' or v['swfplayer']>''):
                mediaitem.URL=mediaitem.URL+' tcUrl='+v['url']
                if v['app']>'':
                    mediaitem.URL=mediaitem.URL+' app='+v['app']
                if v['playpath']>'':
                    mediaitem.URL=mediaitem.URL+' playpath='+v['playpath']
                if v['swfplayer']>'':
                    mediaitem.URL=mediaitem.URL+' swfUrl='+v['swfplayer']
                if v['pageurl']>'':
                    mediaitem.URL=mediaitem.URL+' pageUrl='+v['pageurl']
                if v['swfVfy']>'':
                    mediaitem.URL=mediaitem.URL+' swfVfy='+v['swfVfy']

            else:
                mediaitem.swfplayer=v['swfplayer']
                mediaitem.playpath=v['playpath']
                mediaitem.pageurl=v['pageurl']

            mediaitem.processor=''

            ## cache
            if v['cacheable']>'' and not is_cached:
                f=open(cache_filename, 'w')
                f.write(proc_ori)    
                f.close()
                print "Processor cached as " + cache_filename


        else:
            ## proc v1
            arr=htmRaw.splitlines()
            if len(arr) < 1:
                return self.proc_error("nothing returned from learning phase")
            URL=arr[0]
            if URL.find('error')==0:
                return self.proc_error(URL)
            report="Processor: phase 2 - instruct\n URL: "+URL
            if len(arr) < 2:
                self.loc_url = URL
                SetInfoText("")
                print "Processor: single-line processor stage 1 result\n playing "+URL
                return {"code":0}
            filt=arr[1]
            report=report+"\n filter: "+filt
            if len(arr) > 2:
                ref=arr[2]
                report=report+"\n referer: "+ref
            else:
                ref=''
            if len(arr) > 3:
                cookie=arr[3]
                report=report+"\n cookie: "+cookie
            else:
                cookie=''

            print report
            SetInfoText("Processor: scraping...")
            htm=getRemote(URL,{'referer':ref,'cookie':cookie})['content']
            if htm == '':
                return self.proc_error("nothing returned from scrape")

            p=re.compile(filt)
            match=p.search(htm)
            if match:
                tgt=mediaitem.processor
                sep='?'
                report='Processor: phase 3 - scrape and report'
                for i in range(1,len(match.groups())+1):
                    valtmp=match.group(i)
                    if valtmp is None:
                        valtmp=''
                    val=urllib.quote_plus(valtmp)
                    tgt=tgt+sep+'v'+str(i)+'='+val
                    sep='&'
                    report=report+"\n v"+str(i)+": "+val
                print report
                SetInfoText("Processor: processing...")
                htmRaw2=getRemote(tgt)['content']
                if htmRaw2<='':
                    return self.proc_error("could not retrieve data from process phase")
                arr=htmRaw2.splitlines()
                mediaitem.URL=arr[0]

                if arr[0].find('error')==0:
                    return self.proc_error(arr[0])
                if len(arr) > 1:
                    if useLibrtmp:
                        mediaitem.URL=mediaitem.URL+' tcUrl='+arr[0]+' swfUrl='+arr[1]
                        if len(arr) > 2:
                            mediaitem.URL=mediaitem.URL+' playpath='+arr[2]
                        if len(arr) > 3:
                            mediaitem.URL=mediaitem.URL+' pageUrl='+arr[3]
                    else:
                        mediaitem.swfplayer=arr[1]
                        if len(arr) > 2:
                            mediaitem.playpath=arr[2]
                        if len(arr) > 3:
                            mediaitem.pageurl=arr[3]
                mediaitem.processor=''
            else:
                return self.proc_error("pattern not found in scraped data")

        self.loc_url = mediaitem.URL
        mediaitem.processed=True
        self.processed=True

        SetInfoText("Processor complete - playing...")
        time.sleep(.1)
        SetInfoText("")
        report="Processor final result:\n URL: "+self.loc_url
        if mediaitem.playpath>'':
            report=report+"\n PlayPath: "+mediaitem.playpath
        if mediaitem.swfplayer>'':
            report=report+"\n SWFPlayer: "+mediaitem.swfplayer
        if mediaitem.pageurl>'':
            report=report+"\n PageUrl: "+mediaitem.pageurl
        print report

        return {"code":0}

######################################################################
# Description: evaluate if / elseif line
#
# Parameters : str_in = condition(s) to test
#            : v = NIPLVars
# Return     : object: value=boolean, err=""
######################################################################
    def if_eval(self, str_in, v):
        match=self.multiIfTest.search(str_in)
        if match is None:
            # single condition request
            return self.condition_eval(str_in, v)
        else:
            # multiple condition request
            mflag=True
            while mflag==True:
                match=self.conditionExtract.search(str_in)
                if match:
                    cond=match.group(1)
                    #bool=self.condition_eval(cond, v)
                    boolObj=self.condition_eval(cond, v)
                    if(boolObj["error"]==True):
                        return self.proc_error(boolObj["data"])

                    if boolObj["data"]==True:
                        rep=''
                    else:
                        rep=''
                    str_in=str_in.replace(cond,rep)
                else:
                    mflag=False
            str_in=str_in.replace('','True')
            str_in=str_in.replace('','False')
            try:
                bool=eval(str_in)
            except Exception, ex:
                return {
                    "error": True,
                    "data": exception_parse(ex)
                }
            return {
                "error": False,
                "data": bool
            }


######################################################################
# Description: evaluate while loop iteration; modifies control_stack and v
#              by reference
#
# Parameters : if_obj = active entry of control_stack
#            : v = NIPLVars
# Return     : object: error=boolean, match=boolean, message=""
# To do      : implement other types of conditions - pass in flag
#              through v object
######################################################################
    def while_eval(self, control_obj, v):
        control_obj["execcount"]=control_obj["execcount"]+1
        if control_obj["execcount"]>500:
            return {
            	"error": True,
            	"match": False,
              "message": "While loop exceeded maximum iteration count"
             }
        for i in range(1,11):
            ke='v'+str(i)
            v[ke]=''

        # Hard-coded to "re" type for now
        match=control_obj['regex'].search(control_obj['haystack'][control_obj['searchstart']:])
        rerep='Processor while iteration:'
        if match is None:
            rerep=rerep+' no match'
            control_obj["block_do"]=False
            return {
            	"error": False,
            	"match": False,
            	"message": rerep
            }

        control_obj["searchstart"]=control_obj["searchstart"]+match.end()
        for i in range(1,len(match.groups())+1):
            val=match.group(i)
            if val is None:
                val=''
            key='v'+str(i)
            rerep=rerep+"\n "+key+'='+val
            v[key]=val

        return {
        	"error": False,
        	"match": True,
        	"message": rerep
        }

######################################################################
# Description: evaluate single condition
#
# Parameters : str_in = condition to test
#            : v = NIPLVars
# Return     : Boolean
######################################################################
    def condition_eval(self, cond, v):
        match=self.ifparse.search(cond)
        if match:
            ### process with operators
            lkey=match.group(1)
            oper=match.group(2)
            rraw=match.group(3)
            if oper=='=':
                oper='=='
            if rraw[0:1]=="'":
                rside=rraw[1:]
            else:
                rside=v[rraw]
            try:
                bool=eval("v[lkey]"+oper+"rside")
            except Exception, ex:
                return {
                    "error": True,
                    "data": exception_parse(ex)
                }

        else:
            ### process single if argument for >''
            bool=v[cond]>''

        return {
            "error": False,
            "data": bool
        }

    
######################################################################
# Description: handle processor error
#
# Parameters : msg = error message
# Return     : urlopen return object
######################################################################
    def proc_error(self, msg):
        SetInfoText("")
        print "Processor error in line "+str(self.linenum_display)+"\nline: " + self.line_display+"\nerror: "+str(msg)
        return {"code":1, "data":"p:" + str(msg)}


######################################################################
# Description: This class is used to create the variable dictionary
#              object used by NIPL. Its primary purpose is to allow
#              querying dictionary elements which don't exist without
#              crashing Python, although a couple of methods have been
#              added for initializing and resetting the object.
#
# Parameters : URL=source URL
# Return     : 0=successful, -1=fail
######################################################################
class NIPLVars:

    def __init__(self):
        self.data=self.defaults()

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return ''

    def __setitem__(self,key,value):
        if value is None:
            value=''
        self.data[key]=value

    def defaults(self):
        return {
            'htmRaw':'',
            's_url':'',
            'regex':'',
            's_method':'get',
            's_action':'read',
            's_agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
            's_referer':'',
            's_cookie':'',
            's_postdata':'',
            'url':'',
            'swfplayer':'',
            'playpath':'',
            'agent':'',
            'pageurl':'',
            'app':'',
            'swfVfy':'',
            'nookie_expires':'0'
        }

    def reset(self,rtype=""):
        v_defaults=self.defaults()
        if rtype=="scrape":
            for ke in ('s_method','s_action','s_agent','s_referer','s_cookie','s_postdata'):
                self.data[ke]=v_defaults[ke]
        elif rtype=="hard":
            self.data=self.defaults()
        else:
            for ke in v_defaults:
                self.data[ke]=v_defaults[ke]
