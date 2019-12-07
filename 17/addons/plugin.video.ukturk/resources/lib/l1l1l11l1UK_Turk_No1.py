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
def l1ll11l11UK_Turk_No1(name,url,l11lll1ll1UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬ೺")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡪࡱࡧࡧࡴࠤࡁࠬ࠳࠱࠿ࠪ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡡࡥࡡࡷࡳࡵࠨ࠾ࠨ೻"),re.DOTALL).findall(link)[0]
    cat=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠾࡯࡭ࡃࡂࡩࠡࡶ࡬ࡸࡱ࡫࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣ࠰࠮ࡃࠧࡄ࠼࠰࡫ࡁࠫ೼")).findall(match)
    for url,name in cat:
        url=l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠭೽")+url
        string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ࠩ೾")+name+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨ೿")+url+l11l1lUK_Turk_No1 (u"ࠪࡀࡪࡴࡤ࠿ࠩഀ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨഁ"), l11l1lUK_Turk_No1 (u"ࠬࡓ࡯ࡻ࡫࡯ࡰࡦ࠵࠵࠯࠲ࠣࠬ࡜࡯࡮ࡥࡱࡺࡷࠥࡔࡔࠡ࠳࠳࠲࠵࠯ࠠࡂࡲࡳࡰࡪ࡝ࡥࡣࡍ࡬ࡸ࠴࠻࠳࠸࠰࠶࠺ࠥ࠮ࡋࡉࡖࡐࡐ࠱ࠦ࡬ࡪ࡭ࡨࠤࡌ࡫ࡣ࡬ࡱࠬࠤࡈ࡮ࡲࡰ࡯ࡨ࠳࠺࠺࠮࠱࠰࠵࠼࠹࠶࠮࠸࠳ࠣࡗࡦ࡬ࡡࡳ࡫࠲࠹࠸࠽࠮࠴࠸ࠪം"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link