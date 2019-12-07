# coding: UTF-8
import sys
l111ll1llUK_Turk_No1 = sys.version_info [0] == 2
l11l1l11lUK_Turk_No1 = 2048
l111llll1UK_Turk_No1 = 7
def l11l1lUK_Turk_No1 (l1llll1lUK_Turk_No1):
    global l1l1ll1llUK_Turk_No1
    l11lllll1UK_Turk_No1 = ord (l1llll1lUK_Turk_No1 [-1])
    l11l111llUK_Turk_No1 = l1llll1lUK_Turk_No1 [:-1]
    l1lll1lllUK_Turk_No1 = l11lllll1UK_Turk_No1 % len (l11l111llUK_Turk_No1)
    l1l11llllUK_Turk_No1 = l11l111llUK_Turk_No1 [:l1lll1lllUK_Turk_No1] + l11l111llUK_Turk_No1 [l1lll1lllUK_Turk_No1:]
    if l111ll1llUK_Turk_No1:
        l1ll1llUK_Turk_No1 = unicode () .join ([unichr (ord (char) - l11l1l11lUK_Turk_No1 - (l11lllUK_Turk_No1 + l11lllll1UK_Turk_No1) % l111llll1UK_Turk_No1) for l11lllUK_Turk_No1, char in enumerate (l1l11llllUK_Turk_No1)])
    else:
        l1ll1llUK_Turk_No1 = str () .join ([chr (ord (char) - l11l1l11lUK_Turk_No1 - (l11lllUK_Turk_No1 + l11lllll1UK_Turk_No1) % l111llll1UK_Turk_No1) for l11lllUK_Turk_No1, char in enumerate (l1l11llllUK_Turk_No1)])
    return eval (l1ll1llUK_Turk_No1)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,re,os,sys
def l1ll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪಁ")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡦࠦࡣ࡭ࡣࡶࡷࡂࠨ࡮ࡦࡺࡷࡴࡴࡹࡴࡴ࡮࡬ࡲࡰࠨࠠࡳࡧ࡯ࡁࠧࡴࡥࡹࡶࠥࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁ࠲࠰ࡅ࠼࠰ࡣࡁࠫಂ")).findall(link)[0]
        l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠩಃ")+l11l1111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂ࡮ࡱࡀࠪ಄")
    except: pass
    l11llll1l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡥ࡫ࡹࠤࡨࡲࡡࡴࡵࡀࠦࡰࡻࡴࡶ࠯ࡵࡩࡸ࡯࡭ࠣࡀࠣࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࠥࡺࡩࡵ࡮ࡨࡁࠧ࠮࠮ࠬࡁࠬࠦࡃࡂࡩ࡮ࡩࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡦࡴࡸࡤࡦࡴ࠰ࡻ࡮ࡪࡴࡩ࠼ࠣ࠴ࡵࡾ࠻ࠡࡪࡨ࡭࡬࡮ࡴ࠻ࠢ࠱࠯ࡄࡁࠠࡸ࡫ࡧࡸ࡭ࡀࠠ࠯࠭ࡂ࠿ࠧࠦࡳࡳࡥࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡦࡲࡴ࠾ࠤ࠱࠯ࡄࠨࠠࡸ࡫ࡧࡸ࡭ࡃࠢ࠯࠭ࡂࠦࠥ࡮ࡥࡪࡩ࡫ࡸࡂࠨ࠮ࠬࡁࠥ࠳ࡃ࠭ಅ"),re.DOTALL).findall(link)
    for url,name,l1l11l11UK_Turk_No1 in l11llll1l1UK_Turk_No1:
        name=name.split(l11l1lUK_Turk_No1 (u"ࠧ࠯ࠩಆ"))[0]
        string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ࠩಇ")+name+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨಈ")+url+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩಉ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁ࡫࡮ࡥࡀࠪಊ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll1l11UK_Turk_No1(url):
    parts=[]
    link=l1llll111UK_Turk_No1(url)
    parts.append(url)
    print parts
    l1lll11l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣ࡭ࡩࡃࠢࡱࡣࡵࡸࠧࡄࠨ࠯࠭ࡂ࠭ࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡹ࡭ࡩ࡫࡯ࠣࡀࠪಋ"),re.DOTALL).findall(link)[0]
    l1l11l1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠾ࡶࡴࡦࡴ࠾ࠨಌ")).findall(l1lll11l1UK_Turk_No1)
    for page in l1l11l1llUK_Turk_No1:
        parts.append(page)
    return parts
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    link=l1llll111UK_Turk_No1(url)
    l11llll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠬ಍")).findall(link)
    print l11llll1llUK_Turk_No1
    for host in l11llll1llUK_Turk_No1:
        if l11l1lUK_Turk_No1 (u"ࠨࡦࡤ࡭ࡱࡿ࡭ࡰࡶ࡬ࡳࡳ࠭ಎ") in host or l11l1lUK_Turk_No1 (u"ࠩ࡫ࡵࡶ࠭ಏ") in host:
            return host
        elif l11l1lUK_Turk_No1 (u"ࠪࡧࡦࡴ࡬ࡪࡦ࡬ࡾ࡮࡮ࡤ࠷ࠩಐ") in host:
            link=l1llll111UK_Turk_No1(host)
            l11llll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡸࡸࡣ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠩ಑")).findall(link)
            for host in l11llll1llUK_Turk_No1:
                if l11l1lUK_Turk_No1 (u"ࠬࡪࡡࡪ࡮ࡼࡱࡴࡺࡩࡰࡰࠪಒ") in host:
                    return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪಓ"), l11l1lUK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠵࠵࠴࠰ࠪࠢࡄࡴࡵࡲࡥࡘࡧࡥࡏ࡮ࡺ࠯࠶࠵࠺࠲࠸࠼ࠠࠩࡍࡋࡘࡒࡒࠬࠡ࡮࡬࡯ࡪࠦࡇࡦࡥ࡮ࡳ࠮ࠦࡃࡩࡴࡲࡱࡪ࠵࠵࠵࠰࠳࠲࠷࠾࠴࠱࠰࠺࠵࡙ࠥࡡࡧࡣࡵ࡭࠴࠻࠳࠸࠰࠶࠺ࠬಔ"))
    response = urllib2.urlopen(req, timeout=30)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠣࠨࠦࡼࠧಕ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨಖ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩಗ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣಘ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠬࡏࡓࡐ࠯࠻࠼࠺࠿࠭࠲ࠩಙ")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬಚ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦಛ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠣࡣࡶࡧ࡮࡯ࠢಜ"), l11l1lUK_Turk_No1 (u"ࠤ࡬࡫ࡳࡵࡲࡦࠤಝ")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩಞ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬಟ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠧࡅࡵࡳ࡮ࡀࠦಠ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨಡ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠢࠧࡰࡤࡱࡪࡃࠢಢ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠣࠨࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴ࠽ࠣಣ")+str(description)+l11l1lUK_Turk_No1 (u"ࠤࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠢತ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠥࡈࡪ࡬ࡡࡶ࡮ࡷࡊࡴࡲࡤࡦࡴ࠱ࡴࡳ࡭ࠢಥ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪದ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡏࡳࡑ࡮ࡤࡽࡦࡨ࡬ࡦࠤಧ"),l11l1lUK_Turk_No1 (u"ࠨࡴࡳࡷࡨࠦನ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok