domain="https://forums.tvaddons.ag/"
encoding="utf-8"
import re
def strip(text):
    text=re.sub(unichr(9),"",text)
    text=re.sub("\\\\r\\\\n","[CR]",text)
    text=re.sub("\\\\n","[CR]",text)
    text=re.sub("<br.?/>","",text)
    text=re.sub("&amp;","&",text)
    text=re.sub("&amp;","&",text)
    text=re.sub("&gt;",">",text)
    text=re.sub("\\\\'","'",text)
    text=re.sub("<b>","[B]",text)
    text=re.sub("</b>","[/B]",text)
    text=re.sub("<i>","[I]",text)
    text=re.sub("</i>","[/I]",text)
    text=re.sub("<font.*?>","[COLOR blue]",text)
    text=re.sub("</font>","[/COLOR]",text)
    text=re.sub("\[/SIZE\]","",text)
    text=re.sub("\' \+ \'","",text)
    text=re.sub("\[CR\]                              ","",text)
    text=re.sub('<div class="bbcode.*?>(.*?)</div>',r"[I][COLOR gray]\1[/I][/COLOR]",text)
    text=re.sub('\<div class\="message"\>(.*?)</div>',r"[I][COLOR gray]\1[/I][/COLOR]",text)
    msg=re.findall('<blockquote class="postcontent.*?>(.*?)</blockquote>',text,re.DOTALL)[0]
    poster=re.findall('<li class="optionlabel">(.*?)</li>',text)[0]
    msg=re.sub("<[^>]+>","",msg)
    postdate=re.findall('<span class="date">(.*?)</span>',text)[0]
    postdate=re.sub("<[^>]+>","",postdate)
    return "[CR][COLOR red] >> %s posted at %s [/COLOR]: %s"%(poster,postdate,msg)

def run(ump):
    if ump.page=="root":
        page=ump.get_page(domain+"boogie-s-kodi-repo",encoding)
        threads=re.findall('<a class="title.*?href="(.*?)" id="(.*?)">(.*?)</a>.*?</span>\s*?<a href="(.*?)" class="lastpostdate',page,re.DOTALL)
        for link,id,title,lastlink in threads:
            ump.index_item(title,"showthread",args={"link":ump.absuri(domain,lastlink),"label":title},isFolder=False)
        ump.set_content(ump.defs.CC_FILES)
    elif ump.page=="showthread":
        page=ump.get_page(ump.args["link"].split("#")[0]+"?mode=threaded",encoding)
        text=""
        for post in sorted(re.findall("pd\[.*?\] = \'(.*?)\'\;",page),reverse=True):
            text+=strip(post)
        ump.view_text(ump.args["label"],text)