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
import urllib,urllib2,re,os,sys
def l11ll1l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪࠫౘ")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡳࡥ࡬࡯࡮ࡢࡶ࡬ࡳࡳࠨ࠾ࠩ࠰࠮ࡃ࠮ࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡷ࡮ࡪࡥࡣࡣࡵࠤࡸࡩࡲࡰ࡮࡯࡭ࡳ࡭ࠢ࠿ࠩౙ"),re.DOTALL).findall(link)
        for items in l11l1111lUK_Turk_No1:
            url=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠ࠿ࠩౚ")).findall(items)[-1]
            l111l1lllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡲࡤࡲࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡹࡰࡢࡰࡁࠫ౛")).findall(items)[0]
            url=url.replace(l11l1lUK_Turk_No1 (u"ࠧࠧࠥ࠳࠷࠽ࡁࠧ౜"),l11l1lUK_Turk_No1 (u"ࠨࠨࠪౝ"))
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡲࡵࡄࠧ౞")+l111l1lllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡳࡶ࠾ࠨ౟")+url+l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠩౠ")
    except:pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࡳࡶ࡬ࡧࡱ࡫ࠠࡪࡦࡀࠦ࠳࠱࠿ࠣࠢࡦࡰࡦࡹࡳ࠾ࠤ࡬ࡸࡪࡳࠠ࡮ࡱࡹ࡭ࡪࡹࠢ࠿࠰࠮ࡃࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡳࡳࡸࡺࡥࡳࠤࡁ࠲࠰ࡅ࠼ࡪ࡯ࡪࠤࡸࡸࡣ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠢࡤࡰࡹࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠾࠯࠭ࡂࡀࡸࡶࡡ࡯ࠢࡦࡰࡦࡹࡳ࠾ࠤࡴࡹࡦࡲࡩࡵࡻࠥࡂ࠳࠱࠿࠽࠱ࡶࡴࡦࡴ࠾࠯࠭ࡂࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࡃࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡷࡪ࡫ࠢ࠿ࠩౡ"),re.DOTALL).findall(link)
    for l1l11l11UK_Turk_No1,name,url in match:
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠺࠵࠵࠼ࡁࠢౢ"),l11l1lUK_Turk_No1 (u"ࠢࠨࠤౣ")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠼࠷࠷࠱࠼ࠤ౤"),l11l1lUK_Turk_No1 (u"ࠤ࠰ࠦ౥"))
        string=l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠫ౦")+name+l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡥࡱࡀࠪ౧")+url+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫ౨")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"࠭࠼ࡦࡰࡧࡂࠬ౩")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽࡫ࡩࡶࡦࡳࡥࠡࡥ࡯ࡥࡸࡹ࠽ࠣ࡯ࡨࡸࡦ࡬ࡲࡢ࡯ࡨࠤࡷࡶࡴࡴࡵࠥࠤࡸࡸࡣ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠩ౪"),re.DOTALL).findall(link)
    return l11lllll11UK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬ౫"), l11l1lUK_Turk_No1 (u"ࠩࡐࡳࡿ࡯࡬࡭ࡣ࠲࠹࠳࠶࡙ࠠࠩ࡬ࡲࡩࡵࡷࡴࠢࡑࡘࠥ࠷࠰࠯࠲ࠬࠤࡆࡶࡰ࡭ࡧ࡚ࡩࡧࡑࡩࡵ࠱࠸࠷࠼࠴࠳࠷ࠢࠫࡏࡍ࡚ࡍࡍ࠮ࠣࡰ࡮ࡱࡥࠡࡉࡨࡧࡰࡵࠩࠡࡅ࡫ࡶࡴࡳࡥ࠰࠷࠷࠲࠵࠴࠲࠹࠶࠳࠲࠼࠷ࠠࡔࡣࡩࡥࡷ࡯࠯࠶࠵࠺࠲࠸࠼ࠧ౬"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠥࠪࠨࡾࠢ౭"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪ౮"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫ౯"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠨࠨࡀ࡫ࠬࠪࠨࡢࡷࠬ࠽ࠥ౰"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠧࡊࡕࡒ࠱࠽࠾࠵࠺࠯࠴ࠫ౱")).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧ౲")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠤࠫࡃ࡮࠯ࠦࠤ࡞ࡺ࠯ࡀࠨ౳"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠥࡥࡸࡩࡩࡪࠤ౴"), l11l1lUK_Turk_No1 (u"ࠦ࡮࡭࡮ࡰࡴࡨࠦ౵")).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫ౶")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ౷")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠢࡀࡷࡵࡰࡂࠨ౸")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠣࠨࡰࡳࡩ࡫࠽ࠣ౹")+str(mode)+l11l1lUK_Turk_No1 (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤ౺")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠥࠪࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯࠿ࠥ౻")+str(description)+l11l1lUK_Turk_No1 (u"ࠦࠫ࡯ࡣࡰࡰ࡬ࡱࡦ࡭ࡥ࠾ࠤ౼")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠧࡊࡥࡧࡣࡸࡰࡹࡌ࡯࡭ࡦࡨࡶ࠳ࡶ࡮ࡨࠤ౽"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬ౾"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠢࡊࡵࡓࡰࡦࡿࡡࡣ࡮ࡨࠦ౿"),l11l1lUK_Turk_No1 (u"ࠣࡶࡵࡹࡪࠨಀ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok