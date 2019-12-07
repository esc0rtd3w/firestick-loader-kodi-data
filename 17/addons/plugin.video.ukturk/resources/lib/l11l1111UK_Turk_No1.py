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
def l1ll11lUK_Turk_No1(url):
    l11lll1lllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡸࡹࡺ࠲ࡩࡪࡩࡻ࡫࠴࠲ࡨࡵ࡭ࠨ಩")
    if url == l11l1lUK_Turk_No1 (u"ࠨ࠲ࠪಪ"):
        l11llll111UK_Turk_No1 = 1
    else:
        l11llll111UK_Turk_No1 = int(url) + 1
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪಫ")
    page = l11lll1lllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠪ࠳ࡱ࠴ࡰࡩࡲࡂࡷࡦࡿࡦࡢ࠿ࠪಬ") + str(l11llll111UK_Turk_No1)
    link=l1llll111UK_Turk_No1(page)
    try:
        l11llll11lUK_Turk_No1 = int(l11llll111UK_Turk_No1)+1
        l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠩಭ")+str(l11llll11lUK_Turk_No1)+l11l1lUK_Turk_No1 (u"ࠬࡂ࡮ࡱࡀࠪಮ")
    except: pass
    l11llll1l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡥ࡫ࡹࠤࡨࡲࡡࡴࡵࡀࠦࡩ࡯ࡺࡪ࠯ࡥࡳࡽࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠢࡷ࡭ࡹࡲࡥ࠾ࠤ࠱࠯ࡄࠨ࠾࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡻ࡮ࡪࡴࡩ࠿ࠥ࠲࠰ࡅࠢࠡࡪࡨ࡭࡬࡮ࡴ࠾ࠤ࠱࠯ࡄࠨࠠࡢ࡮ࡷࡁࠧ࠴ࠫࡀࠤࠣ࠳ࡃࡂࡳࡱࡣࡱࠤࡨࡲࡡࡴࡵࡀࠦ࠳࠱࠿ࠣࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡶࡴࡦࡴ࠾࠽࠱ࡤࡂࡁ࠵ࡤࡪࡸࡁࠫಯ"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in l11llll1l1UK_Turk_No1:
        name=name.split(l11l1lUK_Turk_No1 (u"ࠧ࠯ࠩರ"))[0]
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡱࠬಱ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡲ࠵࠰ࠨಲ"))
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡥࡦ࡬ࡾ࡮࠷࠮ࡤࡱࡰ࠳ࠬಳ")+l1l11l11UK_Turk_No1
        string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬ಴")+name+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫವ")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬಶ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡧࡱࡨࡃ࠭ಷ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll1l11UK_Turk_No1(url):
    parts=[]
    link=l1llll111UK_Turk_No1(url)
    parts.append(url)
    l1lll11l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡤࡪࡼ࡬࠱ࡵࡧࡲࡵࡵࠥࡂ࠭࠴ࠫࡀࠫ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡥ࡫ࡽ࡭࠲ࡼࡩࡥࡧࡲࠦࡃ࠭ಸ"),re.DOTALL).findall(link)[0]
    l1l11l1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࡂ࠳࠱࠿࠽࠱ࡤࡂࡁ࠵࡬ࡪࡀࠪಹ")).findall(l1lll11l1UK_Turk_No1)
    for page in l1l11l1llUK_Turk_No1:
        page=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡥࡦ࡬ࡾ࡮࠷࠮ࡤࡱࡰࠫ಺")+page
        parts.append(page)
    return parts
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11llll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡸࡸࡣ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠩ಻")).findall(link)
    print l11llll1llUK_Turk_No1
    for host in l11llll1llUK_Turk_No1:
        if l11l1lUK_Turk_No1 (u"ࠬࡪࡡࡪ࡮ࡼࡱࡴࡺࡩࡰࡰ಼ࠪ") in host or l11l1lUK_Turk_No1 (u"࠭ࡹࡰࡷࡷࡹࡧ࡫ࠧಽ") in host:
            return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫಾ"), l11l1lUK_Turk_No1 (u"ࠨࡏࡲࡾ࡮ࡲ࡬ࡢ࠱࠸࠲࠵ࠦࠨࡘ࡫ࡱࡨࡴࡽࡳࠡࡐࡗࠤ࠶࠶࠮࠱ࠫࠣࡅࡵࡶ࡬ࡦ࡙ࡨࡦࡐ࡯ࡴ࠰࠷࠶࠻࠳࠹࠶ࠡࠪࡎࡌ࡙ࡓࡌ࠭ࠢ࡯࡭ࡰ࡫ࠠࡈࡧࡦ࡯ࡴ࠯ࠠࡄࡪࡵࡳࡲ࡫࠯࠶࠶࠱࠴࠳࠸࠸࠵࠲࠱࠻࠶ࠦࡓࡢࡨࡤࡶ࡮࠵࠵࠴࠹࠱࠷࠻࠭ಿ"))
    response = urllib2.urlopen(req, timeout=30)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠤࠩࠧࡽࠨೀ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩು"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪೂ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠧ࠮࠿ࡪࠫࠩࠧࡡࡽࠫ࠼ࠤೃ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"࠭ࡉࡔࡑ࠰࠼࠽࠻࠹࠮࠳ࠪೄ")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭೅")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧೆ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠤࡤࡷࡨ࡯ࡩࠣೇ"), l11l1lUK_Turk_No1 (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࠥೈ")).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪ೉")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭ೊ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠨ࠿ࡶࡴ࡯ࡁࠧೋ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢೌ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠣࠨࡱࡥࡲ࡫࠽್ࠣ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠤࠩࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮࠾ࠤ೎")+str(description)+l11l1lUK_Turk_No1 (u"ࠥࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠣ೏")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠦࡉ࡫ࡦࡢࡷ࡯ࡸࡋࡵ࡬ࡥࡧࡵ࠲ࡵࡴࡧࠣ೐"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫ೑"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡉࡴࡒ࡯ࡥࡾࡧࡢ࡭ࡧࠥ೒"),l11l1lUK_Turk_No1 (u"ࠢࡵࡴࡸࡩࠧ೓"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok