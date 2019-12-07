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
    string=l11l1lUK_Turk_No1 (u"ࠨࠩැ")
    link=l1llll111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡦࡶ࡮ࡩࡦࡳࡧࡨ࠲ࡸࡩ࠯ࡧࡱࡲࡸࡧࡧ࡬࡭࠯࡯࡭ࡻ࡫࠭ࡴࡶࡵࡩࡦࡳࠢෑ"))
    events=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡹࡪ࠾࠽ࡵࡳࡥࡳࠦࡣ࡭ࡣࡶࡷࡂࠨࡳࡱࡱࡵࡸ࠲࡯ࡣࡰࡰࠫ࠲࠰ࡅࠩ࠽࠱ࡷࡶࡃ࠭ි"),re.DOTALL).findall(link)
    for event in events:
        l11lll111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡤ࠿ࠪ࠱࠯ࡄ࠯࠼ࡣࡴࠫ࠲࠰ࡅࠩ࠽࠱ࡷࡨࡃ࠭ී")).findall(event)
        for day,date in l11lll111lUK_Turk_No1:
            day=l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠࠫු")+day+l11l1lUK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨ෕")
            date=date.replace(l11l1lUK_Turk_No1 (u"ࠧ࠿ࠩූ"),l11l1lUK_Turk_No1 (u"ࠨࠩ෗"))
        time=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨ࡭ࡢࡶࡦ࡬ࡹ࡯࡭ࡦࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦ࠹࠹࠻࠴࠶࠶࠾ࡪࡴࡴࡴ࠮ࡹࡨ࡭࡬࡮ࡴ࠻ࡤࡲࡰࡩࡁࡦࡰࡰࡷ࠱ࡸ࡯ࡺࡦ࠼ࠣ࠽ࡵࡾࠢ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶࡧࡂࠬෘ")).findall(event)[0]
        time=l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡦࡱࡻࡥ࡞ࠪࠪෙ")+time+l11l1lUK_Turk_No1 (u"ࠫ࠮ࡡ࠯ࡄࡑࡏࡓࡗࡣࠧේ")
        l11lll1l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࠡࡵࡷࡽࡱ࡫࠽ࠣࡶࡨࡼࡹ࠳ࡤࡦࡥࡲࡶࡦࡺࡩࡰࡰ࠽ࡲࡴࡴࡥࠡࠣ࡬ࡱࡵࡵࡲࡵࡣࡱࡸࡀࡩ࡯࡭ࡱࡵ࠾ࠨ࠻࠴࠶࠶࠸࠸ࡀࠨࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࠩෛ")).findall(event)
        for url,l11lll11llUK_Turk_No1 in l11lll1l11UK_Turk_No1:
            url=url
            l11lll11llUK_Turk_No1=l11lll11llUK_Turk_No1
        string=string+l11l1lUK_Turk_No1 (u"࠭࡜࡯࠾࡬ࡸࡪࡳ࠾࡝ࡰ࠿ࡸ࡮ࡺ࡬ࡦࡀࠨࡷࡁ࠵ࡴࡪࡶ࡯ࡩࡃࡢ࡮࠽ࡵࡳࡳࡷࡺࡳࡥࡧࡹ࡭ࡱࡄࠥࡴ࠾࠲ࡷࡵࡵࡲࡵࡵࡧࡩࡻ࡯࡬࠿࡞ࡱࠫො")%(day+l11l1lUK_Turk_No1 (u"ࠧࠡࠩෝ")+time+l11l1lUK_Turk_No1 (u"ࠨࠢ࠰ࠤࠬෞ")+l11lll11llUK_Turk_No1,url)
        string=string+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࡉ࡮ࡣࡪࡩࡍ࡫ࡲࡦ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄ࡜࡯࠾ࡩࡥࡳࡧࡲࡵࡀࡩࡥࡳࡧࡲࡵ࠾࠲ࡪࡦࡴࡡࡳࡶࡁࡠࡳࡂ࠯ࡪࡶࡨࡱࡃࡢ࡮ࠨෟ")
    return string
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧ෠"), l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩ෡"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link