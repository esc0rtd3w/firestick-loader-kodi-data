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
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩฤ")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡱࡴࡲ࡫ࡷࡧ࡭ࡴࡡ࡬ࡸࡪࡳࠠࡤࡱ࡯࠱ࡱ࡭࠭࠴ࠢࡦࡳࡱ࠳࡭ࡥ࠯࠶ࠤࡨࡵ࡬࠮ࡵࡰ࠱࠹ࠦࡣࡰ࡮࠰ࡼࡸ࠳࠴ࠡࡥࡲࡰ࠲ࡾࡸࡴ࠯࠹ࠦࡃ࠴ࠫࡀ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁ࠲࠰ࡅ࠼ࡪ࡯ࡪࠤࡨࡲࡡࡴࡵࡀࠦ࡮ࡳࡧ࠮ࡴࡨࡷࡵࡵ࡮ࡴ࡫ࡹࡩࠧࠦࡳࡳࡥࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡦࡲࡴ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠢ࠲ࡂࠬล"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡶࡵࡸ࠳ࡺࡶࠨฦ")+url
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠫࠫࡷࡵࡰࡶ࠾ࠫว"),l11l1lUK_Turk_No1 (u"ࠬࠨࠧศ")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠴࠶࠵ࡀࠨษ"),l11l1lUK_Turk_No1 (u"ࠢࡤࠤส")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠵࠾࠿࠻ࠣห"),l11l1lUK_Turk_No1 (u"ࠤࡆࠦฬ")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠵࠳࠽ࠥอ"),l11l1lUK_Turk_No1 (u"ࠦࡺࠨฮ")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠴࠳࠿ࠧฯ"),l11l1lUK_Turk_No1 (u"ࠨࡕࠣะ")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠵࠹ࡁࠢั"),l11l1lUK_Turk_No1 (u"ࠣࡑࠥา")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠷࠺࠶࠼ࠤำ"),l11l1lUK_Turk_No1 (u"ࠥࡳࠧิ")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠳࠺࠽ࠥี"),l11l1lUK_Turk_No1 (u"ࠧ࠭ࠢึ"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"࠭ࠠࠨื"),l11l1lUK_Turk_No1 (u"ࠧࠦ࠴࠳ุࠫ"))
        string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ูࠩ")+name+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨฺ")+url+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩ฻")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁ࡫࡮ࡥࡀࠪ฼")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11llll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡻࡲ࡭࠼ࠣࠦ࠭࠴ࠫࡀࠫࡂࡁ࠳࠱࠿ࠣࠩ฽")).findall(link)
    print l11llll1llUK_Turk_No1
    for host in l11llll1llUK_Turk_No1:
        return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪ฾"), l11l1lUK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠵࠵࠴࠰ࠪࠢࡄࡴࡵࡲࡥࡘࡧࡥࡏ࡮ࡺ࠯࠶࠵࠺࠲࠸࠼ࠠࠩࡍࡋࡘࡒࡒࠬࠡ࡮࡬࡯ࡪࠦࡇࡦࡥ࡮ࡳ࠮ࠦࡃࡩࡴࡲࡱࡪ࠵࠵࠵࠰࠳࠲࠷࠾࠴࠱࠰࠺࠵࡙ࠥࡡࡧࡣࡵ࡭࠴࠻࠳࠸࠰࠶࠺ࠬ฿"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠣࠨࠦࡼࠧเ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨแ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩโ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣใ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠬࡏࡓࡐ࠯࠻࠼࠺࠿࠭࠲ࠩไ")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬๅ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦๆ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠣࡣࡶࡧ࡮࡯ࠢ็"), l11l1lUK_Turk_No1 (u"ࠤ࡬࡫ࡳࡵࡲࡦࠤ่")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹้ࠩ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"๊ࠫࠬ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠧࡅࡵࡳ࡮ࡀ๋ࠦ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨ์")+str(mode)+l11l1lUK_Turk_No1 (u"ࠢࠧࡰࡤࡱࡪࡃࠢํ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠣࠨࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴ࠽ࠣ๎")+str(description)+l11l1lUK_Turk_No1 (u"ࠤࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠢ๏")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠥࡈࡪ࡬ࡡࡶ࡮ࡷࡊࡴࡲࡤࡦࡴ࠱ࡴࡳ࡭ࠢ๐"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪ๑"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡏࡳࡑ࡮ࡤࡽࡦࡨ࡬ࡦࠤ๒"),l11l1lUK_Turk_No1 (u"ࠨࡴࡳࡷࡨࠦ๓"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok