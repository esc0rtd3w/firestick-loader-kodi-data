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
def l1ll11lUK_Turk_No1(url):
    print url
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬ൜")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡱࡣࡱࠤࡨࡲࡡࡴࡵࡀࡧࡺࡸࡲࡦࡰࡷࡂ࠳࠱࠿࠽࠱ࡶࡴࡦࡴ࠾ࠡ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁ࠲࠰ࡅ࠼࠰ࡣࡁࠫ൝")).findall(link)
        for l111lll11UK_Turk_No1 in l11l1111lUK_Turk_No1:
            l111lll11UK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱࠪ൞")+l111lll11UK_Turk_No1
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂࠬൟ")+l111lll11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡱࡴࡃ࠭ൠ")
    except: pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡪࡶࡨࡱࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡶ࡬ࡸࡱ࡫࠽ࠣ࠰࠮ࡃࠧࡄ࠮ࠬࡁ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠥࡨ࡯ࡳࡦࡨࡶࡂࠨ࠮ࠬࡁࠥࠤࡼ࡯ࡤࡵࡪࡀࠦ࠳࠱࠿ࠣࠢ࡫ࡩ࡮࡭ࡨࡵ࠿ࠥ࠲࠰ࡅࠢࠡࡣ࡯ࡸࡂࠨࡗࡢࡶࡦ࡬ࠥ࠮࠮ࠬࡁࠬࠦࡃࡂ࠯ࡢࡀ࠿࠳ࡩ࡯ࡶ࠿ࠩൡ"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡨࡱࡺࡥࡹࡩࡨࡧࡴࡨࡩࡲࡵࡶࡪࡧࡶ࠲ࡹࡵࠧൢ")+url
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼ࠪൣ")+l1l11l11UK_Turk_No1
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠴࠻࠾ࠦ൤"),l11l1lUK_Turk_No1 (u"ࠨࠧࠣ൥")).replace(l11l1lUK_Turk_No1 (u"ࠧࠧࡣࡰࡴࡀ࠭൦"),l11l1lUK_Turk_No1 (u"ࠨࠢࠩࠤࠬ൧"))
        string=l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠪ൨")+name+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩ൩")+url+l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡥࡱࡀࠪ൪")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂࡥ࡯ࡦࡁࠫ൫")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࠧ൬")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡣࠣࡨࡦࡺࡡ࠮࡫ࡧࡁࠧ࠴ࠫࡀࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡷࡪࡧࡳࡰࡰ࠰ࡸࡴ࡭ࡧ࡭ࡧࠥࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁࠬ࠳࠱࠿ࠪ࠾ࡶࡴࡦࡴࠠࡴࡶࡼࡰࡪࡃࠢ࠯࠭ࡂࠦࡃ࠭൭"),re.DOTALL).findall(link)
        for url,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡭࡯ࡸࡣࡷࡧ࡭࡬ࡲࡦࡧࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳࠬ൮")+url
            string=l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠪ൯")+name+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩ൰")+url+l11l1lUK_Turk_No1 (u"ࠫࡁ࡫࡮ࡥࡀࠪ൱")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l11lll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬ࠭൲")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡥ࡫ࡹࠤࡨࡲࡡࡴࡵࡀࠦࡹࡼ࡟ࡦࡲ࡬ࡷࡴࡪࡥࡠ࡫ࡷࡩࡲࠨ࠾ࠡ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁࡉ࠭࠴ࠫࡀࠫ࠿ࡷࡵࡧ࡮ࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡶࡹࡣࡪࡶࡩࡴࡱࡧࡩࡤࡴࡡ࡮ࡧࠥࡂࠥ࠮࠮ࠬࡁࠬࡀ࠴ࡹࡰࡢࡰࡁ࠲࠰ࡅ࠼ࡴࡲࡤࡲࠥࡩ࡬ࡢࡵࡶࡁࠧࡺࡶࡠࡧࡳ࡭ࡸࡵࡤࡦࡡࡤ࡭ࡷࡪࡡࡵࡧࠥࡂ࠳࠱࠿࠽࠱ࡶࡴࡦࡴ࠾ࠨ൳"),re.DOTALL).findall(link)
        for url,l1l1llllUK_Turk_No1,l1l111llUK_Turk_No1 in match:
            url=l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡸࡹࡺ࠲࡬ࡵࡷࡢࡶࡦ࡬࡫ࡸࡥࡦ࡯ࡲࡺ࡮࡫ࡳ࠯ࡶࡲࠫ൴")+url
            string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ࠩ൵")+l1l1llllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨ൶")+l1l111llUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩ൷")+url+l11l1lUK_Turk_No1 (u"ࠫࡁ࡫࡮ࡥࡀࠪ൸")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩ൹"), l11l1lUK_Turk_No1 (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠤ࠭࡝ࡩ࡯ࡦࡲࡻࡸࠦࡎࡕࠢ࠴࠴࠳࠶ࠩࠡࡃࡳࡴࡱ࡫ࡗࡦࡤࡎ࡭ࡹ࠵࠵࠴࠹࠱࠷࠻ࠦࠨࡌࡊࡗࡑࡑ࠲ࠠ࡭࡫࡮ࡩࠥࡍࡥࡤ࡭ࡲ࠭ࠥࡉࡨࡳࡱࡰࡩ࠴࠻࠴࠯࠲࠱࠶࠽࠺࠰࠯࠹࠴ࠤࡘࡧࡦࡢࡴ࡬࠳࠺࠹࠷࠯࠵࠹ࠫൺ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠢࠧࠥࡻࠦൻ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧർ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨൽ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠥࠬࡄ࡯ࠩࠧࠥ࡟ࡻ࠰ࡁࠢൾ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠫࡎ࡙ࡏ࠮࠺࠻࠹࠾࠳࠱ࠨൿ")).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫ඀")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠨࠨࡀ࡫ࠬࠪࠨࡢࡷࠬ࠽ࠥඁ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠢࡢࡵࡦ࡭࡮ࠨං"), l11l1lUK_Turk_No1 (u"ࠣ࡫ࡪࡲࡴࡸࡥࠣඃ")).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨ඄")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫඅ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠦࡄࡻࡲ࡭࠿ࠥආ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠧࠬ࡭ࡰࡦࡨࡁࠧඇ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡯ࡣࡰࡩࡂࠨඈ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠢࠧࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࡃࠢඉ")+str(description)+l11l1lUK_Turk_No1 (u"ࠣࠨ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࡂࠨඊ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠤࡇࡩ࡫ࡧࡵ࡭ࡶࡉࡳࡱࡪࡥࡳ࠰ࡳࡲ࡬ࠨඋ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡴࡡࡳࡶࡢ࡭ࡲࡧࡧࡦࠩඌ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠦࡎࡹࡐ࡭ࡣࡼࡥࡧࡲࡥࠣඍ"),l11l1lUK_Turk_No1 (u"ࠧࡺࡲࡶࡧࠥඎ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok