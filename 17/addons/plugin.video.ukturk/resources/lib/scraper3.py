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
    string=l11l1lUK_Turk_No1 (u"ࠬ࠭෢")
    print l11l1lUK_Turk_No1 (u"࠭ࡸࡹࡺࡻࡼࡽࡾࡸࡹࡺࡻࡼࡽࡾࡸࡹࡺࡻࡼࠬ෣")
    link=l1llll111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰࡯ࡤࡱࡦ࡮ࡤ࠯ࡶࡹ࠳ࠧ෤")).replace(l11l1lUK_Turk_No1 (u"ࠨ࡞ࡱࠫ෥"),l11l1lUK_Turk_No1 (u"ࠩࠪ෦")).replace(l11l1lUK_Turk_No1 (u"ࠪࡠࡹ࠭෧"),l11l1lUK_Turk_No1 (u"ࠫࠬ෨"))
    l11ll1ll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡩࠢࡦࡰࡦࡹࡳ࠾ࠤ࡫ࡳࡲ࡫࠭ࡴࡶࡵࡩࡦࡳࡳࠣࡀࠫ࠲࠰ࡅࠩࡸ࡫ࡧ࡫ࡪࡺ࠭ࡤࡱࡱࡸࡪࡴࡴࠡࡵࡷࡽࡱ࡫࠱ࠣࡀࠪ෩")).findall(link)[0]
    #l11ll11lllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠰࠮ࡃࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠮ࠬࡁ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡩࡱࡰࡩࠥࡩࡥ࡭࡮ࠥࡂ࠳࠱࠿࠽ࡵࡳࡥࡳࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂ࠳࠱࠿࠽ࡵࡳࡥࡳࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂ࠳࠱࠿࠽࠱ࡤࡂࠬ෪")).findall(l11ll1ll11UK_Turk_No1)
    l11ll1lll1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦ࡭ࡵ࡭ࡦ࠯ࡷ࡭ࡲ࡫ࠢ࠿ࠪ࠱࠯ࡄ࠯࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥ࡬ࡴࡳࡥ࠮ࡵࡷࡥࡹࡻࡳࠣࡀࠪ෫"),re.DOTALL).findall(l11ll1ll11UK_Turk_No1)
    print l11ll1lll1UK_Turk_No1[0]
    for l11ll1l1llUK_Turk_No1 in l11ll1lll1UK_Turk_No1:
            date=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡴࡦࡴࠠࡤ࡮ࡤࡷࡸࡃࠢࡥࡣࡷࡩࠧࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂࠬ෬"),re.DOTALL).findall(l11ll1l1llUK_Turk_No1)[0]
            print date
            url=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࡂࠬ෭")).findall(l11ll1l1llUK_Turk_No1)[0]
            print url
            l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀ࡮ࡳࡧࠡࡵࡵࡧࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄࠧ෮")).findall(l11ll1l1llUK_Turk_No1)[0]
            print l1l11l11UK_Turk_No1
            home=url.split(l11l1lUK_Turk_No1 (u"ࠫ࠲࠭෯"))[0]
            print home
    #https://l11ll1l111UK_Turk_No1.tv/4657-l11ll1l11lUK_Turk_No1-l11ll11l11UK_Turk_No1-l11ll1l1l1UK_Turk_No1-l11ll11l1lUK_Turk_No1-l11lll1111UK_Turk_No1-l11ll1llllUK_Turk_No1-l11ll1ll1lUK_Turk_No1-stream.html
    #for url,l1l11l11UK_Turk_No1,home,l11ll11ll1UK_Turk_No1 in l11ll11lllUK_Turk_No1:
    #return string
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩ෰"), l11l1lUK_Turk_No1 (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠤ࠭࡝ࡩ࡯ࡦࡲࡻࡸࠦࡎࡕࠢ࠴࠴࠳࠶ࠩࠡࡃࡳࡴࡱ࡫ࡗࡦࡤࡎ࡭ࡹ࠵࠵࠴࠹࠱࠷࠻ࠦࠨࡌࡊࡗࡑࡑ࠲ࠠ࡭࡫࡮ࡩࠥࡍࡥࡤ࡭ࡲ࠭ࠥࡉࡨࡳࡱࡰࡩ࠴࠻࠴࠯࠲࠱࠶࠽࠺࠰࠯࠹࠴ࠤࡘࡧࡦࡢࡴ࡬࠳࠺࠹࠷࠯࠵࠹ࠫ෱"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link