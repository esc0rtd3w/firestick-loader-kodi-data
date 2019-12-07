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
def l11l1ll11UK_Turk_No1(url):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࠧഃ")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽࡮࡬ࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࠦࡴࡪࡶ࡯ࡩࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠮ࠬࡁ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠥࡽࡩࡥࡶ࡫ࡁࠧ࠴ࠫࡀࠤࠣ࡬ࡪ࡯ࡧࡩࡶࡀࠦ࠳࠱࠿ࠣࠢࡤࡰࡹࡃࠢ࠯࠭ࡂࠦࠥ࠵࠾࠽࠱ࡤࡂࡁ࠵࡬ࡪࡀࠪഄ"),re.DOTALL).findall(link)
    for url,name,l1l11l11UK_Turk_No1 in match:
        url=l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡧࡱ࡫ࡪࡲࡳࡪࡼ࠱࡯ࡦࡴࡡ࡭ࡦ࠱ࡧࡴࡳ࠮ࡵࡴ࠲ࠫഅ")+url
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠸࠿࠻ࠣആ"),l11l1lUK_Turk_No1 (u"ࠥࠫࠧഇ")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠴࠳࠾ࠦഈ"),l11l1lUK_Turk_No1 (u"ࠧࡩࠢഉ")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠳࠼࠽ࡀࠨഊ"),l11l1lUK_Turk_No1 (u"ࠢࡄࠤഋ")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠺࠸࠻ࠣഌ"),l11l1lUK_Turk_No1 (u"ࠤࡸࠦ഍")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠲࠱࠽ࠥഎ"),l11l1lUK_Turk_No1 (u"࡚ࠦࠨഏ")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠳࠷࠿ࠧഐ"),l11l1lUK_Turk_No1 (u"ࠨࡏࠣ഑")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠸࠻ࡁࠢഒ"),l11l1lUK_Turk_No1 (u"ࠣࡱࠥഓ"))
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡨࡲ࡬࡫࡬ࡴ࡫ࡽ࠲ࡰࡧ࡮ࡢ࡮ࡧ࠲ࡨࡵ࡭࠯ࡶࡵ࠳ࠬഔ")+l1l11l11UK_Turk_No1
        string=l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠫക")+name+l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡥࡱࡀࠪഖ")+url+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫഗ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"࠭࠼ࡦࡰࡧࡂࠬഘ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11llll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠢࡶࡴ࡯࠾ࠥ࠭࡭ࡱ࠶࠽ࡩࡳ࡭ࡥ࡭ࡵ࡬ࡾ࠴࠮࠮ࠬࡁࠬࠫࠧങ")).findall(link)
    print l11llll1llUK_Turk_No1
    for host in l11llll1llUK_Turk_No1:
        host=l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡥࡧࡲ࠻࠴࡫ࡢࡰࡤࡰࡩ࠴ࡣࡰ࡯࠱ࡸࡷ࠵ࠧച")+host
        return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ഛ"), l11l1lUK_Turk_No1 (u"ࠪࡑࡴࢀࡩ࡭࡮ࡤ࠳࠺࠴࠰࡚ࠡࠪ࡭ࡳࡪ࡯ࡸࡵࠣࡒ࡙ࠦ࠱࠱࠰࠳࠭ࠥࡇࡰࡱ࡮ࡨ࡛ࡪࡨࡋࡪࡶ࠲࠹࠸࠽࠮࠴࠸ࠣࠬࡐࡎࡔࡎࡎ࠯ࠤࡱ࡯࡫ࡦࠢࡊࡩࡨࡱ࡯ࠪࠢࡆ࡬ࡷࡵ࡭ࡦ࠱࠸࠸࠳࠶࠮࠳࠺࠷࠴࠳࠽࠱ࠡࡕࡤࡪࡦࡸࡩ࠰࠷࠶࠻࠳࠹࠶ࠨജ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠦࠫࠩࡸࠣഝ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫഞ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬട"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦഠ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠨࡋࡖࡓ࠲࠾࠸࠶࠻࠰࠵ࠬഡ")).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨഢ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠥࠬࡄ࡯ࠩࠧࠥ࡟ࡻ࠰ࡁࠢണ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠦࡦࡹࡣࡪ࡫ࠥത"), l11l1lUK_Turk_No1 (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࠧഥ")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬദ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨധ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠣࡁࡸࡶࡱࡃࠢന")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤഩ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥപ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠦࠫࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࡀࠦഫ")+str(description)+l11l1lUK_Turk_No1 (u"ࠧࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠥബ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠨࡄࡦࡨࡤࡹࡱࡺࡆࡰ࡮ࡧࡩࡷ࠴ࡰ࡯ࡩࠥഭ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡧࡣࡱࡥࡷࡺ࡟ࡪ࡯ࡤ࡫ࡪ࠭മ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠣࡋࡶࡔࡱࡧࡹࡢࡤ࡯ࡩࠧയ"),l11l1lUK_Turk_No1 (u"ࠤࡷࡶࡺ࡫ࠢര"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok