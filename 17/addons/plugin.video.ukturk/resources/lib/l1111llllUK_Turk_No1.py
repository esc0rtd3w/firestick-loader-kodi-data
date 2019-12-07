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
#import xbmc,xbmcaddon,xbmcgui,xbmcplugin
def l1ll11lUK_Turk_No1(url):
    print url
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪࠫറ")
    l11lll1l1lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬല")
    link=l1llll111UK_Turk_No1(url)
    l11llll1l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧࡂ࡬ࡪࠢࡦࡰࡦࡹࡳ࠾ࠩ࡯࡭ࡸࡺࡅࡱ࡫ࡶࡳࡩ࡫ࠧࠩ࠰࠮ࡃ࠮ࡂ࠯࡭࡫ࡁࠦള"),re.DOTALL).findall(link)
    for show in l11llll1l1UK_Turk_No1:
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠼࠰ࡵࡳࡥࡳࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡡ࠿ࠤഴ")).findall(show)[0]
        date=re.compile(l11l1lUK_Turk_No1 (u"ࠢ࡝ࡀࠫ࠲࠰ࡅࠩࠡ࡞࠽ࠤࡁࡧࠠࡵࡣࡵ࡫ࡪࡺࠢവ")).findall(show)[0].replace(l11l1lUK_Turk_No1 (u"ࠨࠢࠪശ"),l11l1lUK_Turk_No1 (u"ࠩ࠲ࠫഷ"))
        day=date.split(l11l1lUK_Turk_No1 (u"ࠪ࠳ࠬസ"))[0]
        month=date.split(l11l1lUK_Turk_No1 (u"ࠫ࠴࠭ഹ"))[1]
        year=date.split(l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧഺ"))[2]
        if len(day)==1:
            day=l11l1lUK_Turk_No1 (u"࠭࠰ࠨ഻")+day
        date=l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢ഼࠭")+day+l11l1lUK_Turk_No1 (u"ࠨ࠱ࠪഽ")+month+l11l1lUK_Turk_No1 (u"ࠩ࠲ࠫാ")+year+l11l1lUK_Turk_No1 (u"ࠪ࡟࠴ࡉࡏࡍࡑࡕࡡࠬി")
        name=date+l11l1lUK_Turk_No1 (u"ࠫࠥ࠳ࠠࠨീ")+name
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠬ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࡂࠬു")).findall(show)[0]
        string=l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠧൂ")+name+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭ൃ")+url+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡨࡲࡩࡄࠧൄ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡥࠥࡺࡡࡳࡩࡨࡸࡂࠨ࡟ࡣ࡮ࡤࡲࡰࠨࠠࡳࡧ࡯ࡁࠧࡴ࡯ࡧࡱ࡯ࡰࡴࡽࠢࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠾ࡑ࡮ࡤࡽࡁ࠵ࡡ࠿ࠩ൅")).findall(link)
    return l11lllll11UK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧെ"), l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩേ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠧࠬࠣࡹࠤൈ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ൉"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ൊ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧോ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠩࡌࡗࡔ࠳࠸࠹࠷࠼࠱࠶࠭ൌ")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹്ࠩ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣൎ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠧࡧࡳࡤ࡫࡬ࠦ൏"), l11l1lUK_Turk_No1 (u"ࠨࡩࡨࡰࡲࡶࡪࠨ൐")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭൑")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩ൒")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠤࡂࡹࡷࡲ࠽ࠣ൓")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥൔ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠦࠫࡴࡡ࡮ࡧࡀࠦൕ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠧࠬࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࡁࠧൖ")+str(description)+l11l1lUK_Turk_No1 (u"ࠨࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠦൗ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦ൘"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧ൙"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠤࡌࡷࡕࡲࡡࡺࡣࡥࡰࡪࠨ൚"),l11l1lUK_Turk_No1 (u"ࠥࡸࡷࡻࡥࠣ൛"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok