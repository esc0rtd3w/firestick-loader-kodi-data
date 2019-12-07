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
import urllib,urllib2,re,os
def l11lll11l1UK_Turk_No1():
    string=l11l1lUK_Turk_No1 (u"ࠨࠩෂ")
    link=l1llll111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡳࡱࡱࡵࡸࡸ࠳ࡳࡵࡴࡨࡥࡲ࠴࡮ࡦࡶ࠲ࡷࡨ࡮ࡥࡥࡷ࡯ࡩ࠳࡮ࡴ࡮࡮ࠥස"))
    events=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡵࡄ࠼ࡴࡲࡤࡲࠥࡹࡴࡺ࡮ࡨࡁ࠭࠴ࠫࡀࠫ࠿࠳ࡵࡄࠧහ"),re.DOTALL).findall(link)
    for event in events:
        time=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡰࡢࡰࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡊࡋ࠶࠰࠱࠲࠾ࠦࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡹࡰࡢࡰࡁࠫළ")).findall(event)[0]
        time=l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡨ࡬ࡶࡧࡠࠫෆ")+time+l11l1lUK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨ෇")
        l11lll1l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽࠱ࡶࡴࡦࡴ࠾ࠡࠪ࠱࠯ࡄ࠯ࠠ࠮ࠢ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄ࠮ࠬࡁ࠿࠳ࡦࡄࠧ෈")).findall(event)
        for l11lll11llUK_Turk_No1,url in l11lll1l11UK_Turk_No1:
            url=url
            l11lll11llUK_Turk_No1=l11lll11llUK_Turk_No1
            l11lll11llUK_Turk_No1=l11lll11llUK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠨ࠯ࠪ෉"),l11l1lUK_Turk_No1 (u"ࠩࡹࡷ්ࠬ"))
        string=string+l11l1lUK_Turk_No1 (u"ࠪࡠࡳࡂࡩࡵࡧࡰࡂࡡࡴ࠼ࡵ࡫ࡷࡰࡪࡄࠥࡴ࠾࠲ࡸ࡮ࡺ࡬ࡦࡀ࡟ࡲࡁࡹࡰࡰࡴࡷࡷࡩ࡫ࡶࡪ࡮ࡁࠩࡸࡂ࠯ࡴࡲࡲࡶࡹࡹࡤࡦࡸ࡬ࡰࡃࡢ࡮ࠨ෋")%(time+l11l1lUK_Turk_No1 (u"ࠫࠥ࠳ࠠࠨ෌")+l11lll11llUK_Turk_No1,url)
        string=string+l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࡌࡱࡦ࡭ࡥࡉࡧࡵࡩࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀ࡟ࡲࡁ࡬ࡡ࡯ࡣࡵࡸࡃ࡬ࡡ࡯ࡣࡵࡸࡁ࠵ࡦࡢࡰࡤࡶࡹࡄ࡜࡯࠾࠲࡭ࡹ࡫࡭࠿࡞ࡱࠫ෍")
    return string
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪ෎"), l11l1lUK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠵࠵࠴࠰ࠪࠢࡄࡴࡵࡲࡥࡘࡧࡥࡏ࡮ࡺ࠯࠶࠵࠺࠲࠸࠼ࠠࠩࡍࡋࡘࡒࡒࠬࠡ࡮࡬࡯ࡪࠦࡇࡦࡥ࡮ࡳ࠮ࠦࡃࡩࡴࡲࡱࡪ࠵࠵࠵࠰࠳࠲࠷࠾࠴࠱࠰࠺࠵࡙ࠥࡡࡧࡣࡵ࡭࠴࠻࠳࠸࠰࠶࠺ࠬා"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link