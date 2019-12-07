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
def l111lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩ೔")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡵࡧ࡮ࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡥࡸࡶࡷ࡫࡮ࡵࠤࡁ࠲࠰ࡅ࠼࠰ࡵࡳࡥࡳࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡲࡤ࡫ࡪࠨࠠࡵ࡫ࡷࡰࡪࡃࠢ࠯࠭ࡂࠦࡃ࠴ࠫࡀ࠾࠲ࡥࡃ࠭ೕ"),re.DOTALL).findall(link)
        for l111lll11UK_Turk_No1 in l11l1111lUK_Turk_No1:
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡳࡶ࠾ࠨೖ")+l111lll11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠩ೗")
    except: pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡸࡩࡥ࡭ࡰࡦࡸࡰࡪࡥ࠱ࠡࡶࡧࡣࡲࡵࡤࡶ࡮ࡨࡣࡼࡸࡡࡱࠢࡷࡨ࠲ࡧ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮࠮ࡵࡷࡥࡨࡱࠢ࠿࠰࠮ࡃࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡷࡨ࠲ࡳ࡯ࡥࡷ࡯ࡩ࠲ࡺࡨࡶ࡯ࡥࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠࡳࡧ࡯ࡁࠧࡨ࡯ࡰ࡭ࡰࡥࡷࡱࠢࠡࡶ࡬ࡸࡱ࡫࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠾࡬ࡱ࡬ࠦࡷࡪࡦࡷ࡬ࡂࠨ࠮ࠬࡁࠥࠤ࡭࡫ࡩࡨࡪࡷࡁࠧ࠴ࠫࡀࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡩࡳࡺࡲࡺ࠯ࡷ࡬ࡺࡳࡢࠣࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࡅࡲࡦࡵ࡬ࡾࡪࡃ࠮ࠬࡁࠥࠤࡦࡲࡴ࠾ࠤࠥࠤࡹ࡯ࡴ࡭ࡧࡀࠦ࠳࠱࠿ࠣࠢ࠲ࡂࡁ࠵ࡡ࠿࠾࠲ࡨ࡮ࡼ࠾ࠨ೘"),re.DOTALL).findall(link)
    for url,name,l1l11l11UK_Turk_No1 in match:
        name=name.replace(l11l1lUK_Turk_No1 (u"࠭ࠦࠤ࠺࠵࠵࠶ࡁࠧ೙"),l11l1lUK_Turk_No1 (u"ࠧࠡ࠯ࠣࠫ೚")).replace(l11l1lUK_Turk_No1 (u"ࠨࠨࠦ࠴࠸࠾࠻ࠨ೛"),l11l1lUK_Turk_No1 (u"ࠩࠪ೜")).replace(l11l1lUK_Turk_No1 (u"ࠪࠤࡋࡻ࡬࡭ࠢࡐࡥࡹࡩࡨࠨೝ"),l11l1lUK_Turk_No1 (u"ࠫࠬೞ"))
        string=l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠭೟")+name+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬೠ")+url+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭ೡ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡨࡲࡩࡄࠧೢ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1lll1l1lUK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭࡫ࡸࡡ࡮ࡧ࠱࠯ࡄࡹࡲࡤ࠿ࠥ࠲࠰ࡅࠢࠡࡦࡤࡸࡦ࠳࡬ࡢࡼࡼ࠱ࡸࡸࡣ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠢࡩࡶࡦࡳࡥࡣࡱࡵࡨࡪࡸ࠽ࠨೣ"),re.DOTALL).findall(link)
    return l11lllll11UK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧ೤"), l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩ೥"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠧࠬࠣࡹࠤ೦"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ೧"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭೨"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧ೩"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠩࡌࡗࡔ࠳࠸࠹࠷࠼࠱࠶࠭೪")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩ೫")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣ೬"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠧࡧࡳࡤ࡫࡬ࠦ೭"), l11l1lUK_Turk_No1 (u"ࠨࡩࡨࡰࡲࡶࡪࠨ೮")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭೯")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩ೰")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠤࡂࡹࡷࡲ࠽ࠣೱ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥೲ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠦࠫࡴࡡ࡮ࡧࡀࠦೳ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠧࠬࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࡁࠧ೴")+str(description)+l11l1lUK_Turk_No1 (u"ࠨࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠦ೵")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦ೶"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧ೷"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠤࡌࡷࡕࡲࡡࡺࡣࡥࡰࡪࠨ೸"),l11l1lUK_Turk_No1 (u"ࠥࡸࡷࡻࡥࠣ೹"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok