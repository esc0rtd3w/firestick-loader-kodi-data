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
import urllib,urllib2,re,os,sys,base64
def l1ll11lUK_Turk_No1(url):
    print url
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࠧඏ")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡳࡥࡳࠦࡣ࡭ࡣࡶࡷࡂࡩࡵࡳࡴࡨࡲࡹࡄ࠮ࠬࡁ࠿࠳ࡸࡶࡡ࡯ࡀࠣࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࡃ࠴ࠫࡀ࠾࠲ࡥࡃ࠭ඐ")).findall(link)
        for l111lll11UK_Turk_No1 in l11l1111lUK_Turk_No1:
            l111lll11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡭࡯ࡸࡣࡷࡧ࡭࡬ࡲࡦࡧࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳࠬඑ")+l111lll11UK_Turk_No1
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡲࡵࡄࠧඒ")+l111lll11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡳࡶ࠾ࠨඓ")
    except: pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤ࡬ࡸࡪࡳࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡸ࡮ࡺ࡬ࡦ࠿ࠥ࠲࠰ࡅࠢ࠿࠰࠮ࡃࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠࡣࡱࡵࡨࡪࡸ࠽ࠣ࠰࠮ࡃࠧࠦࡷࡪࡦࡷ࡬ࡂࠨ࠮ࠬࡁࠥࠤ࡭࡫ࡩࡨࡪࡷࡁࠧ࠴ࠫࡀࠤࠣࡥࡱࡺ࠽࡙ࠣࡤࡸࡨ࡮ࠠࠩ࠰࠮ࡃ࠮ࠨ࠾࠽࠱ࡤࡂࡁ࠵ࡤࡪࡸࡁࠫඔ"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        url=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡪࡳࡼࡧࡴࡤࡪࡩࡶࡪ࡫࡭ࡰࡸ࡬ࡩࡸ࠴ࡴࡰࠩඕ")+url
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾ࠬඖ")+l1l11l11UK_Turk_No1
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠶࠽ࡀࠨ඗"),l11l1lUK_Turk_No1 (u"ࠣࠩࠥ඘")).replace(l11l1lUK_Turk_No1 (u"ࠩࠩࡥࡲࡶ࠻ࠨ඙"),l11l1lUK_Turk_No1 (u"ࠪࠤࠫࠦࠧක"))
        string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬඛ")+name+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫග")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬඝ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡧࡱࡨࡃ࠭ඞ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩඟ")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡥࠥࡪࡡࡵࡣ࠰࡭ࡩࡃࠢ࠯࠭ࡂࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡹࡥࡢࡵࡲࡲ࠲ࡺ࡯ࡨࡩ࡯ࡩࠧࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࡃ࠮࠮ࠬࡁࠬࡀࡸࡶࡡ࡯ࠢࡶࡸࡾࡲࡥ࠾ࠤ࠱࠯ࡄࠨ࠾ࠨච"),re.DOTALL).findall(link)
        for url,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡨࡱࡺࡥࡹࡩࡨࡧࡴࡨࡩࡲࡵࡶࡪࡧࡶ࠲ࡹࡵࠧඡ")+url
            string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬජ")+name+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫඣ")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡦࡰࡧࡂࠬඤ")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l11lll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࠨඥ")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡴࡷࡡࡨࡴ࡮ࡹ࡯ࡥࡧࡢ࡭ࡹ࡫࡭ࠣࡀࠣࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࡃࡋࠨ࠯࠭ࡂ࠭ࡁࡹࡰࡢࡰࠣࡧࡱࡧࡳࡴ࠿ࠥࡸࡻࡥࡥࡱ࡫ࡶࡳࡩ࡫࡟࡯ࡣࡰࡩࠧࡄࠠࠩ࠰࠮ࡃ࠮ࡂ࠯ࡴࡲࡤࡲࡃ࠴ࠫࡀ࠾ࡶࡴࡦࡴࠠࡤ࡮ࡤࡷࡸࡃࠢࡵࡸࡢࡩࡵ࡯ࡳࡰࡦࡨࡣࡦ࡯ࡲࡥࡣࡷࡩࠧࡄ࠮ࠬࡁ࠿࠳ࡸࡶࡡ࡯ࡀࠪඦ"),re.DOTALL).findall(link)
        for url,l1l1llllUK_Turk_No1,l1l111llUK_Turk_No1 in match:
            url=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡧࡰࡹࡤࡸࡨ࡮ࡦࡳࡧࡨࡱࡴࡼࡩࡦࡵ࠱ࡸࡴ࠭ට")+url
            string=l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠫඨ")+l1l1llllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡥࡱࡀࠪඩ")+l1l111llUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫඪ")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡦࡰࡧࡂࠬණ")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫඬ"), l11l1lUK_Turk_No1 (u"ࠨࡏࡲࡾ࡮ࡲ࡬ࡢ࠱࠸࠲࠵ࠦࠨࡘ࡫ࡱࡨࡴࡽࡳࠡࡐࡗࠤ࠶࠶࠮࠱ࠫࠣࡅࡵࡶ࡬ࡦ࡙ࡨࡦࡐ࡯ࡴ࠰࠷࠶࠻࠳࠹࠶ࠡࠪࡎࡌ࡙ࡓࡌ࠭ࠢ࡯࡭ࡰ࡫ࠠࡈࡧࡦ࡯ࡴ࠯ࠠࡄࡪࡵࡳࡲ࡫࠯࠶࠶࠱࠴࠳࠸࠸࠵࠲࠱࠻࠶ࠦࡓࡢࡨࡤࡶ࡮࠵࠵࠴࠹࠱࠷࠻࠭ත"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠤࠩࠧࡽࠨථ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩද"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪධ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠧ࠮࠿ࡪࠫࠩࠧࡡࡽࠫ࠼ࠤන"), fixup, text.decode(l11l1lUK_Turk_No1 (u"࠭ࡉࡔࡑ࠰࠼࠽࠻࠹࠮࠳ࠪ඲")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ඳ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧප"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠤࡤࡷࡨ࡯ࡩࠣඵ"), l11l1lUK_Turk_No1 (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࠥබ")).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪභ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭ම")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠨ࠿ࡶࡴ࡯ࡁࠧඹ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢය")+str(mode)+l11l1lUK_Turk_No1 (u"ࠣࠨࡱࡥࡲ࡫࠽ࠣර")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠤࠩࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮࠾ࠤ඼")+str(description)+l11l1lUK_Turk_No1 (u"ࠥࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠣල")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠦࡉ࡫ࡦࡢࡷ࡯ࡸࡋࡵ࡬ࡥࡧࡵ࠲ࡵࡴࡧࠣ඾"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫ඿"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡉࡴࡒ࡯ࡥࡾࡧࡢ࡭ࡧࠥව"),l11l1lUK_Turk_No1 (u"ࠢࡵࡴࡸࡩࠧශ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok