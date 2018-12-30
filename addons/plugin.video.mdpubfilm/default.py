# -*- coding: utf-8 -*-
import sys
l1lll11Created_By_Mucky_Duck = sys.version_info [0] == 2
l111ll1Created_By_Mucky_Duck = 2048
l1llllCreated_By_Mucky_Duck = 7
def l111l1Created_By_Mucky_Duck (llCreated_By_Mucky_Duck):
    global l111lCreated_By_Mucky_Duck
    l11l111Created_By_Mucky_Duck = ord (llCreated_By_Mucky_Duck [-1])
    l1lll1lCreated_By_Mucky_Duck = llCreated_By_Mucky_Duck [:-1]
    l111Created_By_Mucky_Duck = l11l111Created_By_Mucky_Duck % len (l1lll1lCreated_By_Mucky_Duck)
    l1lllCreated_By_Mucky_Duck = l1lll1lCreated_By_Mucky_Duck [:l111Created_By_Mucky_Duck] + l1lll1lCreated_By_Mucky_Duck [l111Created_By_Mucky_Duck:]
    if l1lll11Created_By_Mucky_Duck:
        l1l1l11Created_By_Mucky_Duck = unicode () .join ([unichr (ord (char) - l111ll1Created_By_Mucky_Duck - (l11l11Created_By_Mucky_Duck + l11l111Created_By_Mucky_Duck) % l1llllCreated_By_Mucky_Duck) for l11l11Created_By_Mucky_Duck, char in enumerate (l1lllCreated_By_Mucky_Duck)])
    else:
        l1l1l11Created_By_Mucky_Duck = str () .join ([chr (ord (char) - l111ll1Created_By_Mucky_Duck - (l11l11Created_By_Mucky_Duck + l11l111Created_By_Mucky_Duck) % l1llllCreated_By_Mucky_Duck) for l11l11Created_By_Mucky_Duck, char in enumerate (l1lllCreated_By_Mucky_Duck)])
    return eval (l1l1l11Created_By_Mucky_Duck)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import os,re,sys,shutil
# PubFilm Add-on Created By Mucky Duck (1/2016)
l11ll1lCreated_By_Mucky_Duck = xbmcaddon.Addon().getAddonInfo(l111l1Created_By_Mucky_Duck (u"ࠫ࡮ࡪࠧࠀ"))
l11lll1Created_By_Mucky_Duck = Addon(l11ll1lCreated_By_Mucky_Duck, sys.argv)
l1ll1llCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_name()
l11llllCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_path()
md = md(l11ll1lCreated_By_Mucky_Duck, sys.argv)
l1ll11Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠁ"))
l1l111lCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥࡳࡩࡱࡺࡷࠬࠂ"))
l1l1lCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠧࡦࡰࡤࡦࡱ࡫࡟࡮ࡱࡹ࡭ࡪࡹࠧࠃ"))
l1ll1Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠨࡧࡱࡥࡧࡲࡥࡠࡨࡤࡺࡸ࠭ࠄ"))
l11llCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠩࡤࡨࡩࡥࡳࡦࡶࠪࠅ"))
l1111l1Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠪࡩࡳࡧࡢ࡭ࡧࡢࡱࡪࡺࡡࡠࡵࡨࡸࠬࠆ"))
l11Created_By_Mucky_Duck = md.get_art()
l1lllllCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_icon()
l1l1llCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_fanart()
if l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠫࡧࡧࡳࡦࡡࡸࡶࡱ࠭ࠇ")):
	l1llCreated_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_setting(l111l1Created_By_Mucky_Duck (u"ࠬࡨࡡࡴࡧࡢࡹࡷࡲࠧࠈ"))
else:
	l1llCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡰࡶࡤࡩ࡭ࡱࡳ࠮ࡪࡵࠪࠉ")
reload(sys)
sys.setdefaultencoding(l111l1Created_By_Mucky_Duck (u"ࠢࡶࡶࡩ࠱࠽ࠨࠊ"))
def l1111llCreated_By_Mucky_Duck():
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠋ"):l111l1Created_By_Mucky_Duck (u"ࠩࡶࡩࡦࡸࡣࡩࠩࠌ"),l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠍ"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡓࡆࡃࡕࡇࡍࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࠎ"), l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠏ"):l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠐ")})
	if l1l1lCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠧࡵࡴࡸࡩࠬࠑ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠒ"):l111l1Created_By_Mucky_Duck (u"ࠩ࠴ࠫࠓ"),l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠔ"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣࡍࡐࡘࡌࡉࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࠕ"), l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠖ"):l111l1Created_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡷࡥ࡬࠵࡭ࡰࡸ࡬ࡩࡸ࠭ࠗ") %l1llCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࠘"):content})
	if l1l111lCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭࠙"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࠚ"):l111l1Created_By_Mucky_Duck (u"ࠪ࠵ࠬࠛ"),l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࠜ"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡔࡇࡕࡍࡊ࡙࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࠝ"), l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠞ"):l111l1Created_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡸࡦ࡭࠯ࡴࡧࡵ࡭ࡪࡹࠧࠟ") %l1llCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࠠ"):content})
        l111lllCreated_By_Mucky_Duck()
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࠡ"):l111l1Created_By_Mucky_Duck (u"ࠪ࠷ࠬࠢ"),l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࠣ"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡈࡇࡑࡖࡊࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࠤ"), l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠥ"):l111l1Created_By_Mucky_Duck (u"ࠧࡈࡇࡑࡖࡊ࠭ࠦ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࠧ"):l111l1Created_By_Mucky_Duck (u"ࠩ࠶ࠫࠨ"),l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࠩ"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠ࡟ࡇࡣ࡙ࡆࡃࡕࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࠪ"), l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠫ"):l111l1Created_By_Mucky_Duck (u"࡙࠭ࡆࡃࡕࡗࠬࠬ")})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬ࠭"):l111l1Created_By_Mucky_Duck (u"ࠨ࠳ࠪ࠮"),l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧ࠯"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡏࡎࠡࡖࡋࡉࡆ࡚ࡅࡓࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࠰"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨ࠱"):l111l1Created_By_Mucky_Duck (u"ࠬࠫࡳ࠰ࡥࡤࡸࡪ࡭࡯ࡳࡻ࠲ࡱࡴࡹࡴ࠮ࡹࡤࡸࡨ࡮ࡥࡥࠩ࠲") %l1llCreated_By_Mucky_Duck})
	md.addDir({l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫ࠳"):l111l1Created_By_Mucky_Duck (u"ࠧ࠲ࠩ࠴"),l111l1Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭࠵"):l111l1Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞࡝ࡅࡡࡓࡋࡗࡍ࡛ࠣࡅࡉࡊࡅࡅ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧ࠶"), l111l1Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ࠷"):l111l1Created_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡵࡣࡪ࠳ࡳ࡫ࡷ࠮ࡣࡧࡨࡪࡪࠧ࠸") %l1llCreated_By_Mucky_Duck})
	md.addDir({l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ࠹"):l111l1Created_By_Mucky_Duck (u"࠭࠱ࠨ࠺"),l111l1Created_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ࠻"):l111l1Created_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝࡜ࡄࡠࡖࡊࡉࡏࡎࡏࡈࡒࡉࡋࡄ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭࠼"), l111l1Created_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭࠽"):l111l1Created_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡣࡢࡶࡨ࡫ࡴࡸࡹ࠰ࡴࡨࡧࡴࡳ࡭ࡦࡰࡧࡩࡩ࠭࠾") %l1llCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬ࠿"):content})
	if l1ll1Created_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠬࡺࡲࡶࡧࠪࡀ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡦࡨࠫࡁ"): l111l1Created_By_Mucky_Duck (u"ࠧࡧࡧࡷࡧ࡭ࡥࡦࡢࡸࡶࠫࡂ"), l111l1Created_By_Mucky_Duck (u"ࠨࡰࡤࡱࡪ࠭ࡃ"):l111l1Created_By_Mucky_Duck (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞࡝ࡅࡡࡒ࡟ࠠࡇࡃ࡙ࡓ࡚ࡘࡉࡕࡇࡖ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࡄ"), l111l1Created_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧࡅ"):l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࡆ")})
	if l1ll11Created_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"ࠬࡺࡲࡶࡧࠪࡇ"):
		if l1111l1Created_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࡈ"):
			md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࡉ"):l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡨࡸࡦࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨࡊ"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࡋ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓࡅࡕࡃࠣࡗࡊ࡚ࡔࡊࡐࡊࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡌ"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࡍ"):l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡎ")}, is_folder=False)
	if l11llCreated_By_Mucky_Duck == l111l1Created_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࡏ"):
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࡐ"):l111l1Created_By_Mucky_Duck (u"ࠨࡣࡧࡨࡴࡴ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠩࡑ"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࡒ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡇࡄࡅࡑࡑࠤࡘࡋࡔࡕࡋࡑࡋࡘࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡓ"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࡔ"):l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡕ")}, is_folder=False)
        l1111Created_By_Mucky_Duck()
	setView(l11ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬࡖ"), l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪࡗ"))
	l11lll1Created_By_Mucky_Duck.end_of_directory()
def l1Created_By_Mucky_Duck(url,content):
	link = open_url(url).content
	l1ll111Created_By_Mucky_Duck = md.regex_get_all(link, l111l1Created_By_Mucky_Duck (u"ࠨࠤࡵࡩࡨ࡫࡮ࡵ࠯࡬ࡸࡪࡳࠢ࠿ࠩࡘ"), l111l1Created_By_Mucky_Duck (u"ࠩࠥࡴࡴࡹࡴ࠮࡯ࡨࡸࡦࠨ࠾ࠨ࡙"))
	items = len(l1ll111Created_By_Mucky_Duck)
	for a in l1ll111Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠪࡀ࡭࠹ࠠࡤ࡮ࡤࡷࡸࡃࠢࡱࡱࡶࡸ࠲ࡨ࡯ࡹ࠯ࡷ࡭ࡹࡲࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠳࠱࠿ࠣࠢࡵࡩࡱࡃࠢࡣࡱࡲ࡯ࡲࡧࡲ࡬ࠤࡁ࡚ࠫ"), l111l1Created_By_Mucky_Duck (u"ࠫࡁ࠵ࡡ࠿࡛ࠩ"))
		name = name.replace(l111l1Created_By_Mucky_Duck (u"࡙ࠬࡥࡢࡱࡶࡲࠬ࡜"),l111l1Created_By_Mucky_Duck (u"࠭ࡓࡦࡣࡶࡳࡳ࠭࡝")).replace(l111l1Created_By_Mucky_Duck (u"ࠧࡇࡷ࡯ࡰࠥ࠮ࡈࡅࠫࠪ࡞"),l111l1Created_By_Mucky_Duck (u"ࠨࠩ࡟"))
		name = l11lll1Created_By_Mucky_Duck.unescape(name).strip()
		l111l11Created_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠩࠥࡪࡤࡺࡡࡨࠤࡁࠫࡠ"), l111l1Created_By_Mucky_Duck (u"ࠪࡀࠬࡡ")).strip()
		url = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠫ࡭ࡸࡥࡧ࠿ࠥࠫࡢ"), l111l1Created_By_Mucky_Duck (u"ࠬࠨࠧࡣ"))
		l1ll1lCreated_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"࠭ࡳࡳࡥࡀࠦࠬࡤ"), l111l1Created_By_Mucky_Duck (u"ࠧࠣࠩࡥ"))
		fan_art = {l111l1Created_By_Mucky_Duck (u"ࠨ࡫ࡦࡳࡳ࠭ࡦ"):l1ll1lCreated_By_Mucky_Duck}
		if l111l1Created_By_Mucky_Duck (u"ࠩ࠲ࠫࡧ") in l111l11Created_By_Mucky_Duck or l111l1Created_By_Mucky_Duck (u"ࠪࡗࡪࡧࡳࡰࡰࠣࠫࡨ") in name:
			content = l111l1Created_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬࡩ")
			l111l11Created_By_Mucky_Duck = l111l11Created_By_Mucky_Duck.replace(l111l1Created_By_Mucky_Duck (u"ࠬ࠵ࠧࡪ"),l111l1Created_By_Mucky_Duck (u"࠭ࠠࡰࡨࠣࠫ࡫"))
			l1111lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠧࠨ࡬")
			try:
				l1l11l1Created_By_Mucky_Duck = name.partition(l111l1Created_By_Mucky_Duck (u"ࠨ࠼ࠪ࡭"))
				if len(l1l11l1Created_By_Mucky_Duck) > 0:
					name = l1l11l1Created_By_Mucky_Duck[0].strip()
					name = name[:-5].strip()
					l1111lCreated_By_Mucky_Duck = l1l11l1Created_By_Mucky_Duck[2]
			except:
				pass
			md.addDir({l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧ࡮"):l111l1Created_By_Mucky_Duck (u"ࠪ࠶ࠬ࡯"), l111l1Created_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࡰ"):l111l1Created_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠࠤࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡌࡡ࠭ࠫࡳࠡࡇࡳ࡭ࡸࡵࡤࡦࡵࠣࠩࡸ࠯࡛࠰ࡋࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࡱ") %(name,l1111lCreated_By_Mucky_Duck,l111l11Created_By_Mucky_Duck), l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࡲ"):url,
				   l111l1Created_By_Mucky_Duck (u"ࠧࡵ࡫ࡷࡰࡪ࠭ࡳ"):name, l111l1Created_By_Mucky_Duck (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࡴ"):l1ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࡵ"):l111l1Created_By_Mucky_Duck (u"ࠪࡸࡻࡹࡨࡰࡹࡶࠫࡶ"), l111l1Created_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡴࡱࡱࠫࡷ"):l1111lCreated_By_Mucky_Duck},
				  {l111l1Created_By_Mucky_Duck (u"ࠬࡹ࡯ࡳࡶࡷ࡭ࡹࡲࡥࠨࡸ"):name, l111l1Created_By_Mucky_Duck (u"࠭ࡳࡦࡣࡶࡳࡳ࠭ࡹ"):l1111lCreated_By_Mucky_Duck}, fan_art, item_count=items)
		else:
			content = l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧࡺ")
			year = name[-4:]
			year = year.replace(l111l1Created_By_Mucky_Duck (u"ࠨࠢࠪࡻ"),l111l1Created_By_Mucky_Duck (u"ࠩࠪࡼ"))
			name = name[:-4].strip()
			md.addDir({l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࡽ"):l111l1Created_By_Mucky_Duck (u"ࠫ࠹࠭ࡾ"), l111l1Created_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࡿ"):l111l1Created_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࠥࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟࡞ࡍࡢ࠮ࠥࡴ࠯ࠨࡷ࠮ࡡ࠯ࡊ࡟࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨࢀ") %(name,year,l111l11Created_By_Mucky_Duck), l111l1Created_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࢁ"):url, l111l1Created_By_Mucky_Duck (u"ࠨ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࠫࢂ"):l1ll1lCreated_By_Mucky_Duck,
				   l111l1Created_By_Mucky_Duck (u"ࠩࡦࡳࡳࡺࡥ࡯ࡶࠪࢃ"):l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪࢄ")}, {l111l1Created_By_Mucky_Duck (u"ࠫࡸࡵࡲࡵࡶ࡬ࡸࡱ࡫ࠧࢅ"):name, l111l1Created_By_Mucky_Duck (u"ࠬࡿࡥࡢࡴࠪࢆ"):year}, fan_art, is_folder=False, item_count=items)
	try:
		l111llCreated_By_Mucky_Duck = re.compile(l111l1Created_By_Mucky_Duck (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠮ࡄ࠯ࠢࠡࡀ࡟ࠪࡷࡧࡱࡶࡱ࠾ࡀ࠴ࡧ࠾ࠨࢇ")).findall(link)[0]
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬ࢈"):l111l1Created_By_Mucky_Duck (u"ࠨ࠳ࠪࢉ"), l111l1Created_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࢊ"):l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝࡜ࡄࡠ࡟ࡎࡣ࠾࠿ࡐࡨࡼࡹࠦࡐࡢࡩࡨࡂࡃࡄ࡛࠰ࡋࡠ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࢋ"), l111l1Created_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࢌ"):l111llCreated_By_Mucky_Duck})
	except: pass
	if content == l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࢍ"):
		setView(l11ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࢎ"), l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪ࠳ࡶࡪࡧࡺࠫ࢏"))
	elif content == l111l1Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩ࢐"):
		setView(l11ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪ࢑"), l111l1Created_By_Mucky_Duck (u"ࠪࡷ࡭ࡵࡷ࠮ࡸ࡬ࡩࡼ࠭࢒"))
	l11lll1Created_By_Mucky_Duck.end_of_directory()
def l11lCreated_By_Mucky_Duck(title, url, l1l11lCreated_By_Mucky_Duck, content, l1111lCreated_By_Mucky_Duck):
	link = open_url(url).content
	match = re.compile(l111l1Created_By_Mucky_Duck (u"ࠫࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࡜ࡠࠥࡡ࠰࠯ࠢࡵࡣࡵ࡫ࡪࡺ࠽ࠣࡇ࡝࡛ࡪࡨࡐ࡭ࡣࡼࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡢࡤࡸࡸࡹࡵ࡮ࠡࡱࡵࡥࡳ࡭ࡥࠡ࡯ࡨࡨ࡮ࡻ࡭ࠣࡀࠫ࠲࠯ࡅࠩ࠽࠱ࡤࡂࠬ࢓")).findall(link)
	items = len(match)
	fan_art = {l111l1Created_By_Mucky_Duck (u"ࠬ࡯ࡣࡰࡰࠪ࢔"):l1l11lCreated_By_Mucky_Duck}
	for url,name in match:
		name = re.sub(l111l1Created_By_Mucky_Duck (u"࠭࡜ࡅࠩ࢕"), l111l1Created_By_Mucky_Duck (u"ࠧࠨ࢖"), name)
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࢗ"):l111l1Created_By_Mucky_Duck (u"ࠩ࠷ࠫ࢘"), l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨ࢙"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡅࡱ࡫ࡶࡳࡩ࡫ࠠ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࢚࠭") %name,
			   l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭࢛ࠩ"):url, l111l1Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦࠩ࢜"):l1l11lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨ࢝"):l111l1Created_By_Mucky_Duck (u"ࠨࡧࡳ࡭ࡸࡵࡤࡦࡵࠪ࢞")},
			  {l111l1Created_By_Mucky_Duck (u"ࠩࡶࡳࡷࡺࡴࡪࡶ࡯ࡩࠬ࢟"):title, l111l1Created_By_Mucky_Duck (u"ࠪࡷࡪࡧࡳࡰࡰࠪࢠ"):l1111lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫࡪࡶࡩࡴࡱࡧࡩࠬࢡ"):name},
			  fan_art, is_folder=False, item_count=items)
	setView(l11ll1lCreated_By_Mucky_Duck,l111l1Created_By_Mucky_Duck (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪࡹࠧࢢ"), l111l1Created_By_Mucky_Duck (u"࠭ࡥࡱ࡫࠰ࡺ࡮࡫ࡷࠨࢣ"))
	l11lll1Created_By_Mucky_Duck.end_of_directory()
def l1l1111Created_By_Mucky_Duck(url):
	link = open_url(l1llCreated_By_Mucky_Duck).content
	l1llll1Created_By_Mucky_Duck = md.regex_get_all(link, l111l1Created_By_Mucky_Duck (u"ࠧ࠿ࠧࡶࡀࠬࢤ") %url, l111l1Created_By_Mucky_Duck (u"ࠨ࠾࠲ࡹࡱࡄࠧࢥ"))
	l1ll111Created_By_Mucky_Duck = md.regex_get_all(str(l1llll1Created_By_Mucky_Duck), l111l1Created_By_Mucky_Duck (u"ࠩ࠿ࡰ࡮࠭ࢦ"), l111l1Created_By_Mucky_Duck (u"ࠪࡀ࠴ࡲࡩࠨࢧ"))
	items = len(l1ll111Created_By_Mucky_Duck)
	for a in l1ll111Created_By_Mucky_Duck:
		name = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠫ࡭ࡸࡥࡧ࠿࠱࠮ࡄࡄࠧࢨ"), l111l1Created_By_Mucky_Duck (u"ࠬࡂࠧࢩ"))
		url = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"࠭ࡨࡳࡧࡩࡁࠧ࠭ࢪ"), l111l1Created_By_Mucky_Duck (u"ࠧࠣࠩࢫ"))
		if l1llCreated_By_Mucky_Duck not in url:
			url = l1llCreated_By_Mucky_Duck + url
		md.addDir({l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࢬ"):l111l1Created_By_Mucky_Duck (u"ࠩ࠴ࠫࢭ"),l111l1Created_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࢮ"):l111l1Created_By_Mucky_Duck (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡅࡡࡠࡏ࡝ࠦࡵ࡞࠳ࡎࡣ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࢯ") %name, l111l1Created_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࢰ"):url})
	setView(l11ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࡷࠬࢱ"), l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡧࡱࡹ࠲ࡼࡩࡦࡹࠪࢲ"))
	l11lll1Created_By_Mucky_Duck.end_of_directory()
def l1lll1Created_By_Mucky_Duck(content, query):
	try:
                if query:
                        search = query
                else:
                        search = md.search(l111l1Created_By_Mucky_Duck (u"ࠨࠢࠪࢳ"))
                        if search == l111l1Created_By_Mucky_Duck (u"ࠩࠪࢴ"):
                                md.notification(l111l1Created_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞࡝ࡅࡡࡊࡓࡐࡕ࡛ࠣࡕ࡚ࡋࡒ࡚࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠬࡂࡤࡲࡶࡹ࡯࡮ࡨࠢࡶࡩࡦࡸࡣࡩࠩࢵ"),l1lllllCreated_By_Mucky_Duck)
                                return
                        else:
                                pass
                url = l111l1Created_By_Mucky_Duck (u"ࠫࠪࡹ࠯ࡸࡲ࠰ࡧࡴࡴࡴࡦࡰࡷ࠳ࡵࡲࡵࡨ࡫ࡱࡷ࠴ࡧࡪࡢࡺ࠰ࡷࡪࡧࡲࡤࡪ࠰ࡴࡷࡵ࠯ࡢ࡬ࡤࡼࡤࡹࡥࡢࡴࡦ࡬࠳ࡶࡨࡱࠩࢶ") %l1llCreated_By_Mucky_Duck
                params = {l111l1Created_By_Mucky_Duck (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬࢷ"):l111l1Created_By_Mucky_Duck (u"࠭ࡡ࡫ࡣࡻࡷࡪࡧࡲࡤࡪࡳࡶࡴࡥࡳࡦࡣࡵࡧ࡭࠭ࢸ"), l111l1Created_By_Mucky_Duck (u"ࠧࡢࡵࡳࡴࠬࢹ"):search, l111l1Created_By_Mucky_Duck (u"ࠨࡣࡶ࡭ࡩ࠭ࢺ"):l111l1Created_By_Mucky_Duck (u"ࠩ࠴ࠫࢻ"),
                          l111l1Created_By_Mucky_Duck (u"ࠪࡥࡸࡶ࡟ࡪࡰࡶࡸࡤ࡯ࡤࠨࢼ"):l111l1Created_By_Mucky_Duck (u"ࠫ࠶ࡥ࠱ࠨࢽ"), l111l1Created_By_Mucky_Duck (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ࢾ"):l111l1Created_By_Mucky_Duck (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡱࡣࡪࡩࡤ࡯ࡤ࠾࠹ࠩࡵࡹࡸࡡ࡯ࡵ࡯ࡥࡹ࡫࡟࡭ࡣࡱ࡫ࡂ࠶ࠦࡴࡧࡷࡣ࡮ࡴࡴࡪࡶ࡯ࡩࡂࡔ࡯࡯ࡧࠩࡧࡺࡹࡴࡰ࡯ࡶࡩࡹࠫ࠵ࡃࠧ࠸ࡈࡂࡶ࡯ࡴࡶࠪࢿ")}
                link = open_url(url, method=l111l1Created_By_Mucky_Duck (u"ࠧࡱࡱࡶࡸࠬࣀ"), data=params).content
                l1ll111Created_By_Mucky_Duck = md.regex_get_all(link, l111l1Created_By_Mucky_Duck (u"ࠨࡣࡶࡴࡤࡩ࡯࡯ࡶࡨࡲࡹ࠭ࣁ"), l111l1Created_By_Mucky_Duck (u"ࠩ࠿࠳࡭࠹࠾ࠨࣂ"))
                items = len(l1ll111Created_By_Mucky_Duck)
                for a in l1ll111Created_By_Mucky_Duck:
                        name = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠪࡀ࡭࠹࠾࠽࠰࠭ࡃࡃ࠭ࣃ"), l111l1Created_By_Mucky_Duck (u"ࠫࡁ࠭ࣄ"))
                        name = name.replace(l111l1Created_By_Mucky_Duck (u"࡙ࠬࡥࡢࡱࡶࡲࠬࣅ"),l111l1Created_By_Mucky_Duck (u"࠭ࡓࡦࡣࡶࡳࡳ࠭ࣆ")).replace(l111l1Created_By_Mucky_Duck (u"ࠧࡇࡷ࡯ࡰࠥ࠮ࡈࡅࠫࠪࣇ"),l111l1Created_By_Mucky_Duck (u"ࠨࠩࣈ"))
                        name = l11lll1Created_By_Mucky_Duck.unescape(name).strip()
                        url = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠤ࠿࡬࠸ࡄ࠼ࡢࠢࡦࡰࡦࡹࡳ࠾࡞ࠥࡥࡸࡶ࡟ࡳࡧࡶࡣࡺࡸ࡬࡝ࠤࠣ࡬ࡷ࡫ࡦ࠾ࠩࠥࣉ"), l111l1Created_By_Mucky_Duck (u"ࠥࠫࠧ࣊"))
                        l1ll1lCreated_By_Mucky_Duck = md.regex_from_to(a, l111l1Created_By_Mucky_Duck (u"ࠦࡦࡹࡰࡠࡴࡨࡷࡤ࡯࡭ࡢࡩࡨࡣࡺࡸ࡬ࠨࠢ࡫ࡶࡪ࡬࠽ࠨࠤ࣋"), l111l1Created_By_Mucky_Duck (u"ࠧ࠭ࠢ࣌"))
                        fan_art = {l111l1Created_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫ࣍"):l1ll1lCreated_By_Mucky_Duck}
                        if l111l1Created_By_Mucky_Duck (u"ࠧࡔࡧࡤࡷࡴࡴࠠࠨ࣎") in name:
                                content = l111l1Created_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴ࣏ࠩ")
                                l1111lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"࣐ࠩࠪ")
                                try:
                                        l1l11l1Created_By_Mucky_Duck = name.partition(l111l1Created_By_Mucky_Duck (u"ࠪ࠾࣑ࠬ"))
                                        if len(l1l11l1Created_By_Mucky_Duck) > 0:
                                                name = l1l11l1Created_By_Mucky_Duck[0].strip()
                                                name = name[:-5].strip()
                                                l1111lCreated_By_Mucky_Duck = l1l11l1Created_By_Mucky_Duck[2]
                                except:
                                        pass
                                md.addDir({l111l1Created_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦ࣒ࠩ"):l111l1Created_By_Mucky_Duck (u"ࠬ࠸࣓ࠧ"), l111l1Created_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࣔ"):l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢ࡛ࠦࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠ࡟ࡎࡣࠨࠦࡵࠬ࡟࠴ࡏ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࣕ") %(name,l1111lCreated_By_Mucky_Duck), l111l1Created_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࣖ"):url,
                                           l111l1Created_By_Mucky_Duck (u"ࠩࡷ࡭ࡹࡲࡥࠨࣗ"):name, l111l1Created_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭ࣘ"):l1ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࣙ"):l111l1Created_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࣚ"), l111l1Created_By_Mucky_Duck (u"࠭ࡳࡦࡣࡶࡳࡳ࠭ࣛ"):l1111lCreated_By_Mucky_Duck},
                                          {l111l1Created_By_Mucky_Duck (u"ࠧࡴࡱࡵࡸࡹ࡯ࡴ࡭ࡧࠪࣜ"):name, l111l1Created_By_Mucky_Duck (u"ࠨࡵࡨࡥࡸࡵ࡮ࠨࣝ"):l1111lCreated_By_Mucky_Duck}, fan_art, item_count=items)
                        else:
                                content = l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩࣞ")
                                year = name[-4:]
                                year = year.replace(l111l1Created_By_Mucky_Duck (u"ࠪࠤࠬࣟ"),l111l1Created_By_Mucky_Duck (u"ࠫࠬ࣠"))
                                name = name[:-4].strip()
                                md.addDir({l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ࣡"):l111l1Created_By_Mucky_Duck (u"࠭࠴ࠨ࣢"), l111l1Created_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࣣࠬ"):l111l1Created_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣࠠ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡠࡏ࡝ࠩࠧࡶ࠭ࡠ࠵ࡉ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࣤ") %(name,year), l111l1Created_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࣥ"):url, l111l1Created_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࣦ࠭"):l1ll1lCreated_By_Mucky_Duck,
                                           l111l1Created_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࣧ"):l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡷ࡫ࡨࡷࠬࣨ")}, {l111l1Created_By_Mucky_Duck (u"࠭ࡳࡰࡴࡷࡸ࡮ࡺ࡬ࡦࣩࠩ"):name, l111l1Created_By_Mucky_Duck (u"ࠧࡺࡧࡤࡶࠬ࣪"):year}, fan_art, is_folder=False, item_count=items)
                if content == l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨ࣫"):
                        setView(l11ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩ࣬"), l111l1Created_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦ࠯ࡹ࡭ࡪࡽ࣭ࠧ"))
                elif content == l111l1Created_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷ࣮ࠬ"):
                        setView(l11ll1lCreated_By_Mucky_Duck, l111l1Created_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࣯࠭"), l111l1Created_By_Mucky_Duck (u"࠭ࡳࡩࡱࡺ࠱ࡻ࡯ࡥࡸࣰࠩ"))
                l11lll1Created_By_Mucky_Duck.end_of_directory()
        except:
		md.notification(l111l1Created_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡡࡂ࡞ࡕࡲࡶࡷࡿࠠࡏࡱࠣࡖࡪࡹࡵ࡭ࡶࡶ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࣱࠩ"),l1lllllCreated_By_Mucky_Duck)
l111l1lCreated_By_Mucky_Duck = xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯࡯ࡧࡴࡺࡨࡦࡪ࡮ࡰࡣࡴࡶࡹࠨࣲ"))
if os.path.exists(l111l1lCreated_By_Mucky_Duck):
        shutil.rmtree(l111l1lCreated_By_Mucky_Duck, ignore_errors=True)
def l111lllCreated_By_Mucky_Duck():
	link = open_url(l111l1Created_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡴࡦࡹࡴࡦࡤ࡬ࡲ࠳ࡩ࡯࡮࠱ࡵࡥࡼ࠵ࡃࡧ࠶ࡆ࠷ࡺࡎ࠱ࠨࣳ")).content
	version = re.findall(l111l1Created_By_Mucky_Duck (u"ࡵࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠠࠣࠪ࡞ࡢࠧࡣࠫࠪࠤࠪࣴ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴ࡹࡣࡳ࡫ࡳࡸ࠳ࡳ࡯ࡥࡷ࡯ࡩ࠳ࡳࡵࡤ࡭ࡼࡷ࠳ࡩ࡯࡮࡯ࡲࡲ࠴ࡧࡤࡥࡱࡱ࠲ࡽࡳ࡬ࠨࣵ")), l111l1Created_By_Mucky_Duck (u"ࠬࡸࠫࠨࣶ")) as f:
		l1l1ll1Created_By_Mucky_Duck = f.read()
		if re.search(l111l1Created_By_Mucky_Duck (u"ࡸࠧࡷࡧࡵࡷ࡮ࡵ࡮࠾ࠤࠨࡷࠧ࠭ࣷ") %version, l1l1ll1Created_By_Mucky_Duck):
			l11lll1Created_By_Mucky_Duck.log(l111l1Created_By_Mucky_Duck (u"ࠧࡗࡧࡵࡷ࡮ࡵ࡮ࠡࡅ࡫ࡩࡨࡱࠠࡐࡍࠪࣸ"))
		else:
			l11ll1Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"࡙ࠣࡵࡳࡳ࡭ࠠࡗࡧࡵࡷ࡮ࡵ࡮ࠡࡑࡩࠤࡒࡻࡣ࡬ࡻࡶࠤࡈࡵ࡭࡮ࡱࡱࠤࡒࡵࡤࡶ࡮ࡨࣹࠦ")
			l11lllCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠤࡓࡰࡪࡧࡳࡦࠢࡌࡲࡸࡺࡡ࡭࡮ࠣࡇࡴࡸࡲࡦࡥࡷࠤ࡛࡫ࡲࡴ࡫ࡲࡲࠥࡌࡲࡰ࡯ࠣࡘ࡭࡫ࠠࡓࡧࡳࡳࣺࠧ")
			l1l111Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠥࡄࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡪࡷࡸࡵࡀ࠯࠰࡯ࡸࡧࡰࡿࡳ࠯࡯ࡨࡨ࡮ࡧࡰࡰࡴࡷࡥࡱ࠺࡫ࡰࡦ࡬࠲ࡲࡲ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣࣻ")
			l11lll1Created_By_Mucky_Duck.show_ok_dialog([l11ll1Created_By_Mucky_Duck, l11lllCreated_By_Mucky_Duck, l1l111Created_By_Mucky_Duck], l1ll1llCreated_By_Mucky_Duck)
			xbmc.executebuiltin(l111l1Created_By_Mucky_Duck (u"ࠦ࡝ࡈࡍࡄ࠰ࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡛ࡰࡥࡣࡷࡩ࠭ࡶࡡࡵࡪ࠯ࡶࡪࡶ࡬ࡢࡥࡨ࠭ࠧࣼ"))
			xbmc.executebuiltin(l111l1Created_By_Mucky_Duck (u"ࠧ࡞ࡂࡎࡅ࠱ࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡍࡵ࡭ࡦࠫࠥࣽ"))
def l1ll1l1Created_By_Mucky_Duck(url,name,content,fan_art,l11ll11Created_By_Mucky_Duck):
	if content == l111l1Created_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࣾ"):
		link = open_url(url).content
		l11111Created_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡲࠨ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࡹࡧࡲࡨࡧࡷࡁࠧࡋ࡚ࡘࡧࡥࡔࡱࡧࡹࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡦࡨࡵࡵࡶࡲࡲࠥࡵࡲࡢࡰࡪࡩࠥࡳࡥࡥ࡫ࡸࡱࠧࡄࡓࡆࡔ࡙ࡉࡗࠦ࠱࠽࠱ࡤࡂࠬࣿ"), str(link), re.I|re.DOTALL)[0]
	else:
		l11111Created_By_Mucky_Duck = url
	if l111l1Created_By_Mucky_Duck (u"ࠨࡪࡷࡸࡵ࠭ऀ") not in l11111Created_By_Mucky_Duck:
		l11111Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠩ࡫ࡸࡹࡶ࠺ࠨँ") + l11111Created_By_Mucky_Duck
	host = l1llCreated_By_Mucky_Duck.split(l111l1Created_By_Mucky_Duck (u"ࠪ࠳࠴࠭ं"))[1].split(l111l1Created_By_Mucky_Duck (u"ࠫ࠴࠭ः"))[0]
	headers = {l111l1Created_By_Mucky_Duck (u"ࠬࡎ࡯ࡴࡶࠪऄ"): l111l1Created_By_Mucky_Duck (u"࠭ࡰ࡭ࡣࡼࡩࡷ࠴ࠥࡴࠩअ") %host, l111l1Created_By_Mucky_Duck (u"ࠧࡓࡧࡩࡩࡷ࡫ࡲࠨआ"): url, l111l1Created_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬइ"): md.User_Agent()}
	l1l1lllCreated_By_Mucky_Duck = open_url(l11111Created_By_Mucky_Duck, headers=headers).content
	data = re.findall(l111l1Created_By_Mucky_Duck (u"ࡴࠪࡷࡴࡻࡲࡤࡧࡶ࠾ࡡࡡࠨ࠯ࠬࡂ࠭ࡡࡣࠧई"), str(l1l1lllCreated_By_Mucky_Duck), re.I|re.DOTALL)[0].replace(l111l1Created_By_Mucky_Duck (u"ࠪࠤࠬउ"),l111l1Created_By_Mucky_Duck (u"ࠫࠬऊ"))
	value = []
	l11l1Created_By_Mucky_Duck = []
	l11l1l1Created_By_Mucky_Duck= l111l1Created_By_Mucky_Duck (u"ࠬ࠭ऋ")
	match = re.findall(l111l1Created_By_Mucky_Duck (u"ࡸࠧࡧ࡫࡯ࡩࠧࡀࠢࠩ࠰࠭ࡃ࠮ࠨࠧऌ"), str(data), re.I|re.DOTALL)
	l1ll11lCreated_By_Mucky_Duck = re.findall(l111l1Created_By_Mucky_Duck (u"ࡲࠨ࡮ࡤࡦࡪࡲࠢ࠻ࠤࠫ࠲࠯ࡅࠩࠣࠩऍ"), str(data), re.I|re.DOTALL)
	for url in match:
		l11l1Created_By_Mucky_Duck.append(url)
	for l11l1lCreated_By_Mucky_Duck in l1ll11lCreated_By_Mucky_Duck:
		value.append(int(re.sub(l111l1Created_By_Mucky_Duck (u"ࠨ࡞ࡇࠫऎ"), l111l1Created_By_Mucky_Duck (u"ࠩࠪए"), l11l1lCreated_By_Mucky_Duck)))
	try:
		l11l1l1Created_By_Mucky_Duck =  l11l1Created_By_Mucky_Duck[md.get_max_value_index(value)[0]]
	except:
		l11l1l1Created_By_Mucky_Duck = match[0]
	md.resolved(l11l1l1Created_By_Mucky_Duck, name, fan_art, l11ll11Created_By_Mucky_Duck)
	l11lll1Created_By_Mucky_Duck.end_of_directory()
def l1111Created_By_Mucky_Duck():
        l1l11llCreated_By_Mucky_Duck = xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠪࡷࡵ࡫ࡣࡪࡣ࡯࠾࠴࠵ࡨࡰ࡯ࡨ࠳ࡦࡪࡤࡰࡰࡶ࠳ࡷ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹ࠯࡯ࡤࡪࠬऐ"))
        l1l1l1lCreated_By_Mucky_Duck = xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡶࡲࡰࡩࡵࡥࡲ࠴ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡰࡳࡱࡪࡶࡦࡳ࠮࡮ࡣࡩࡻ࡮ࢀࡡࡳࡦࠪऑ"))
        l11l11lCreated_By_Mucky_Duck = xbmc.translatePath(l111l1Created_By_Mucky_Duck (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳ࡱࡲࡢࡶࡲࡷࠬऒ"))
        if os.path.exists(l1l11llCreated_By_Mucky_Duck):
                l11ll1Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"࡙࠭ࡰࡷࠣࡌࡦࡼࡥࠡࡋࡱࡷࡹࡧ࡬࡭ࡧࡧࠤࡋࡸ࡯࡮ࠢࡄࡲࠬओ")
                l11lllCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠧࡖࡰࡲࡪ࡫࡯ࡣࡪࡣ࡯ࠤࡘࡵࡵࡳࡥࡨࠤࠫࠦࡗࡪ࡮࡯ࠤࡓࡵࡷࠡࡆࡨࡰࡪࡺࡥࠡࡒ࡯ࡩࡦࡹࡥࠨऔ")
                l1l111Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠨࡋࡱࡷࡹࡧ࡬࡭ࠢࡃ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝ࡩࡶࡷࡴ࠿࠵࠯࡮ࡷࡦ࡯ࡾࡹ࠮࡮ࡧࡧ࡭ࡦࡶ࡯ࡳࡶࡤࡰ࠹ࡱ࡯ࡥ࡫࠱ࡱࡱࡡ࠯ࡄࡑࡏࡓࡗࡣࠧक")
                l1lCreated_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠩࡕࡩࡲࡵࡶࡦࡦࠣࡅࡳࡵ࡮ࡺ࡯ࡲࡹࡸࠦࡒࡦࡲࡲࠤࡆࡴࡤࠡࡃࡧࡨࡴࡴࡳࠨख")
                l1l1l1Created_By_Mucky_Duck = l111l1Created_By_Mucky_Duck (u"ࠪࡗࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡓࡰࡪࡧࡳࡦࠢࡇࡳࡳࡺࠠࡔࡷࡳࡴࡴࡸࡴࠡࡋࡧ࡭ࡴࡺࡳࠨग")
                l11lll1Created_By_Mucky_Duck.show_ok_dialog([l11ll1Created_By_Mucky_Duck, l11lllCreated_By_Mucky_Duck, l1l111Created_By_Mucky_Duck], l1ll1llCreated_By_Mucky_Duck)
                l1l1Created_By_Mucky_Duck = l11lll1Created_By_Mucky_Duck.get_path()
                shutil.rmtree(l1l1Created_By_Mucky_Duck, ignore_errors=True)
                shutil.rmtree(l1l11llCreated_By_Mucky_Duck, ignore_errors=True)
                shutil.rmtree(l1l1l1lCreated_By_Mucky_Duck, ignore_errors=True)
                shutil.rmtree(l11l11lCreated_By_Mucky_Duck, ignore_errors=True)
                l11lll1Created_By_Mucky_Duck.log(l111l1Created_By_Mucky_Duck (u"ࠫࡂࡃ࠽ࡅࡇࡏࡉ࡙ࡏࡎࡈ࠿ࡀࡁࡆࡔࡏࡏ࡛ࡐࡓ࡚࡙࠽࠾࠿ࡄࡈࡉࡕࡎࡔ࠿ࡀࡁ࠰ࡃ࠽࠾ࡔࡈࡔࡔࡃ࠽࠾ࠩघ"))
                l11lll1Created_By_Mucky_Duck.show_ok_dialog([l1lCreated_By_Mucky_Duck, l1l1l1Created_By_Mucky_Duck], l1ll1llCreated_By_Mucky_Duck)
                time.sleep(2)
                os._exit(0)
md.check_source()
mode = md.args[l111l1Created_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪङ")]
url = md.args.get(l111l1Created_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪच"), None)
name = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬछ"), None)
query = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠨࡳࡸࡩࡷࡿࠧज"), None)
title = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠩࡷ࡭ࡹࡲࡥࠨझ"), None)
year = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠪࡽࡪࡧࡲࠨञ"), None)
l1111lCreated_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡴࡱࡱࠫट"), None)
l11l1llCreated_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪ࠭ठ") ,None)
l11ll11Created_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"࠭ࡩ࡯ࡨࡲࡰࡦࡨࡥ࡭ࠩड"), None)
content = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨढ"), None)
l1l11Created_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪࡥࡩࡥࠩण"), None)
l1l11lCreated_By_Mucky_Duck = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠩ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠬत"), None)
fan_art = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠪࡪࡦࡴ࡟ࡢࡴࡷࠫथ"), None)
is_folder = md.args.get(l111l1Created_By_Mucky_Duck (u"ࠫ࡮ࡹ࡟ࡧࡱ࡯ࡨࡪࡸࠧद"), True)
if mode is None or url is None or len(url)<1:
	l1111llCreated_By_Mucky_Duck()
elif mode == l111l1Created_By_Mucky_Duck (u"ࠬ࠷ࠧध"):
	l1Created_By_Mucky_Duck(url,content)
elif mode == l111l1Created_By_Mucky_Duck (u"࠭࠲ࠨन"):
	l11lCreated_By_Mucky_Duck(title, url,l1l11lCreated_By_Mucky_Duck,content,l1111lCreated_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠧ࠴ࠩऩ"):
	l1l1111Created_By_Mucky_Duck(url)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠨ࠶ࠪप"):
	l1ll1l1Created_By_Mucky_Duck(url,name,content,fan_art,l11ll11Created_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠩࡶࡩࡦࡸࡣࡩࠩफ"):
	l1lll1Created_By_Mucky_Duck(content, query)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠪࡥࡩࡪ࡯࡯ࡡࡶࡩࡦࡸࡣࡩࠩब"):
	md.addon_search(content,query,fan_art,l11ll11Created_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠫࡦࡪࡤࡠࡴࡨࡱࡴࡼࡥࡠࡨࡤࡺࠬभ"):
	md.add_remove_fav(name,url,l11ll11Created_By_Mucky_Duck,fan_art,
			  content,l1l11Created_By_Mucky_Duck,is_folder)
elif mode == l111l1Created_By_Mucky_Duck (u"ࠬ࡬ࡥࡵࡥ࡫ࡣ࡫ࡧࡶࡴࠩम"):
	md.fetch_favs(l1llCreated_By_Mucky_Duck)
elif mode == l111l1Created_By_Mucky_Duck (u"࠭ࡡࡥࡦࡲࡲࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧय"):
	l11lll1Created_By_Mucky_Duck.show_settings()
elif mode == l111l1Created_By_Mucky_Duck (u"ࠧ࡮ࡧࡷࡥࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧर"):
	import metahandler
	metahandler.display_settings()
l11lll1Created_By_Mucky_Duck.end_of_directory()