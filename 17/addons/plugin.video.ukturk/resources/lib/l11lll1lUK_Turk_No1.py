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
def l11l1ll1lUK_Turk_No1(url):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࠨෲ")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡤࡪࡼ࡬ࠦࠥ࡯ࡤ࠾ࠤ࠱࠯ࡄࠨ࠾࠯࠭ࡂࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࡃࡂࡩ࡮ࡩࠣࡧࡱࡧࡳࡴ࠿ࠥࡨ࡮ࢀࡩࡊ࡯ࡤ࡫ࡪࠨࠠࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࡃࡻࡃ࠮ࠬࡁࠥࠤࡼ࡯ࡤࡵࡪࡀࠦ࠳࠱࠿ࠣࠢ࡫ࡩ࡮࡭ࡨࡵ࠿ࠥ࠲࠰ࡅࠢ࠿࠰࠮ࡃࡁࡻ࡬ࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡦ࡬ࡾ࡮ࡈࡩ࡭ࡩ࡬ࠦࡃ࠴ࠫࡀ࠾࡯࡭ࠥࡩ࡬ࡢࡵࡶࡁࠧࡪࡩࡻ࡫ࡢࡥࡩ࡯ࠢ࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡮࡬ࡂࠬෳ"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠸࠿࠻ࠣ෴"),l11l1lUK_Turk_No1 (u"ࠥࠫࠧ෵")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠴࠳࠾ࠦ෶"),l11l1lUK_Turk_No1 (u"ࠧࡩࠢ෷")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠳࠼࠽ࡀࠨ෸"),l11l1lUK_Turk_No1 (u"ࠢࡄࠤ෹")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠺࠸࠻ࠣ෺"),l11l1lUK_Turk_No1 (u"ࠤࡸࠦ෻")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠲࠱࠽ࠥ෼"),l11l1lUK_Turk_No1 (u"࡚ࠦࠨ෽")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠳࠷࠿ࠧ෾"),l11l1lUK_Turk_No1 (u"ࠨࡏࠣ෿")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠸࠻ࡁࠢ฀"),l11l1lUK_Turk_No1 (u"ࠣࡱࠥก"))
        string=l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠪข")+name+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩฃ")+url+l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡥࡱࡀࠪค")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂࡥ࡯ࡦࡁࠫฅ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll1l1UK_Turk_No1(name,url):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࠧฆ")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡦ࡬ࡺࠥࡩ࡬ࡢࡵࡶࡁࠧࡪࡲࡰࡲࡧࡳࡼࡴ࠭ࡤࡱࡱࡸࡪࡴࡴࠡࡦࡵࡳࡵࡪ࡯ࡸࡰ࠰ࡷࡨࡸ࡯࡭࡮ࠥࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡩ࡯ࡶ࠿ࠩง"),re.DOTALL).findall(link)[0]
    l11ll111llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥ࡮ࡦࡼࡡࡴࡥࡵ࡭ࡵࡺ࠺࠼ࠤࠣ࡭ࡩࡃࠢࠣࠢࡧࡥࡹࡧ࠭ࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡡ࠿ࠩจ")).findall(match)
    for url,name in l11ll111llUK_Turk_No1:
        url=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡳࡩࡱࡺࡸࡻ࠴ࡣࡰ࡯࠱ࡸࡷ࠭ฉ")+url
        string=l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠫช")+name+l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡥࡱࡀࠪซ")+url+l11l1lUK_Turk_No1 (u"ࠬࡂࡥ࡯ࡦࡁࠫฌ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll111l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11llll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡮ࡧࡷࡥࠥࡴࡡ࡮ࡧࡀࠦࡵࡵࡰࡤࡱࡵࡲ࠿ࡹࡴࡳࡧࡤࡱࠧࠦࡣࡰࡰࡷࡩࡳࡺ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡ࠱ࡁࠫญ"),re.DOTALL).findall(link)
    print l11llll1llUK_Turk_No1
    for host in l11llll1llUK_Turk_No1:
        return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫฎ"), l11l1lUK_Turk_No1 (u"ࠨࡏࡲࡾ࡮ࡲ࡬ࡢ࠱࠸࠲࠵ࠦࠨࡘ࡫ࡱࡨࡴࡽࡳࠡࡐࡗࠤ࠶࠶࠮࠱ࠫࠣࡅࡵࡶ࡬ࡦ࡙ࡨࡦࡐ࡯ࡴ࠰࠷࠶࠻࠳࠹࠶ࠡࠪࡎࡌ࡙ࡓࡌ࠭ࠢ࡯࡭ࡰ࡫ࠠࡈࡧࡦ࡯ࡴ࠯ࠠࡄࡪࡵࡳࡲ࡫࠯࠶࠶࠱࠴࠳࠸࠸࠵࠲࠱࠻࠶ࠦࡓࡢࡨࡤࡶ࡮࠵࠵࠴࠹࠱࠷࠻࠭ฏ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠤࠩࠧࡽࠨฐ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩฑ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪฒ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠧ࠮࠿ࡪࠫࠩࠧࡡࡽࠫ࠼ࠤณ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"࠭ࡉࡔࡑ࠰࠼࠽࠻࠹࠮࠳ࠪด")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ต")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧถ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠤࡤࡷࡨ࡯ࡩࠣท"), l11l1lUK_Turk_No1 (u"ࠥ࡭࡬ࡴ࡯ࡳࡧࠥธ")).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪน")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭บ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠨ࠿ࡶࡴ࡯ࡁࠧป")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢผ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠣࠨࡱࡥࡲ࡫࠽ࠣฝ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠤࠩࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮࠾ࠤพ")+str(description)+l11l1lUK_Turk_No1 (u"ࠥࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠣฟ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠦࡉ࡫ࡦࡢࡷ࡯ࡸࡋࡵ࡬ࡥࡧࡵ࠲ࡵࡴࡧࠣภ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫม"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡉࡴࡒ࡯ࡥࡾࡧࡢ࡭ࡧࠥย"),l11l1lUK_Turk_No1 (u"ࠢࡵࡴࡸࡩࠧร"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok