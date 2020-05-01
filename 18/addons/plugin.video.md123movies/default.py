# -*- coding: utf-8 -*-
import sys
l1ll111lCreated_By_Mucky_Duck = sys.version_info [0] == 2
l11l1l1Created_By_Mucky_Duck = 2048
l1lll1llCreated_By_Mucky_Duck = 7
def l11lCreated_By_Mucky_Duck (l1l1llCreated_By_Mucky_Duck):
    global l11ll11Created_By_Mucky_Duck
    l11111lCreated_By_Mucky_Duck = ord (l1l1llCreated_By_Mucky_Duck [-1])
    l1ll11l1Created_By_Mucky_Duck = l1l1llCreated_By_Mucky_Duck [:-1]
    l1l1lllCreated_By_Mucky_Duck = l11111lCreated_By_Mucky_Duck % len (l1ll11l1Created_By_Mucky_Duck)
    l11lllCreated_By_Mucky_Duck = l1ll11l1Created_By_Mucky_Duck [:l1l1lllCreated_By_Mucky_Duck] + l1ll11l1Created_By_Mucky_Duck [l1l1lllCreated_By_Mucky_Duck:]
    if l1ll111lCreated_By_Mucky_Duck:
        l1l11Created_By_Mucky_Duck = unicode () .join ([unichr (ord (char) - l11l1l1Created_By_Mucky_Duck - (l1llCreated_By_Mucky_Duck + l11111lCreated_By_Mucky_Duck) % l1lll1llCreated_By_Mucky_Duck) for l1llCreated_By_Mucky_Duck, char in enumerate (l11lllCreated_By_Mucky_Duck)])
    else:
        l1l11Created_By_Mucky_Duck = str () .join ([chr (ord (char) - l11l1l1Created_By_Mucky_Duck - (l1llCreated_By_Mucky_Duck + l11111lCreated_By_Mucky_Duck) % l1lll1llCreated_By_Mucky_Duck) for l1llCreated_By_Mucky_Duck, char in enumerate (l11lllCreated_By_Mucky_Duck)])
    return eval (l1l11Created_By_Mucky_Duck)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from md_request import open_url
from md_view import setView
from common import Addon
from md_tools import md
import jsunfuck,os,re,sys,shutil,time
# 123Movies By Mucky Duck (12/2015)
l1111llCreated_By_Mucky_Duck = xbmcaddon.Addon().getAddonInfo(l11lCreated_By_Mucky_Duck (u"ࠫ࡮ࡪࠧࠀ"))
l111Created_By_Mucky_Duck = Addon(l1111llCreated_By_Mucky_Duck, sys.argv)
l1ll1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_name()
l1llllllCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_path()
md = md(l1111llCreated_By_Mucky_Duck, sys.argv)
l1l1l11Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠬࡧࡵࡵࡱࡳࡰࡦࡿࠧࠁ"))
l11l11Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"࠭ࡥ࡯ࡣࡥࡰࡪࡥ࡭ࡦࡶࡤࠫࠂ"))
l111ll1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠧࡦࡰࡤࡦࡱ࡫࡟ࡴࡪࡲࡻࡸ࠭ࠃ"))
l1llll1lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠨࡧࡱࡥࡧࡲࡥࡠ࡯ࡲࡺ࡮࡫ࡳࠨࠄ"))
l1l11llCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠩࡨࡲࡦࡨ࡬ࡦࡡࡩࡥࡻࡹࠧࠅ"))
l1111Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠪࡩࡳࡧࡢ࡭ࡧࡢࡴࡷࡵࡸࡺࠩࠆ"))
l1lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠫࡦࡪࡤࡠࡵࡨࡸࠬࠇ"))
l1l111l1Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࡢࡷࡪࡺࠧࠈ"))
l1l11lCreated_By_Mucky_Duck = md.get_art()
l1l1l11lCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_icon()
l1l1111Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_fanart()
if l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"࠭ࡢࡢࡵࡨࡣࡺࡸ࡬ࠨࠉ")):
	l11l111Created_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_setting(l11lCreated_By_Mucky_Duck (u"ࠧࡣࡣࡶࡩࡤࡻࡲ࡭ࠩࠊ"))
else:
	l11l111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡩࡲࡱࡴࡼࡩࡦࡵ࠱ࡸࡪࡩࡨࠨࠋ")
reload(sys)
sys.setdefaultencoding(l11lCreated_By_Mucky_Duck (u"ࠤࡸࡸ࡫࠳࠸ࠣࠌ"))
l11llCreated_By_Mucky_Duck = [l11lCreated_By_Mucky_Duck (u"ࠪࡶࡦࡺࡩ࡯ࡩࠪࠍ"),l11lCreated_By_Mucky_Duck (u"ࠫࡱࡧࡴࡦࡵࡷࠫࠎ"),l11lCreated_By_Mucky_Duck (u"ࠬࡼࡩࡦࡹࠪࠏ"),l11lCreated_By_Mucky_Duck (u"࠭ࡦࡢࡸࡲࡶ࡮ࡺࡥࠨࠐ"),l11lCreated_By_Mucky_Duck (u"ࠧࡪ࡯ࡧࡦࡤࡳࡡࡳ࡭ࠪࠑ")]
sort = [l11lCreated_By_Mucky_Duck (u"ࠨ࡝ࡅࡡࡠࡏ࡝࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡒࡵࡳࡵࠢࡕࡥࡹ࡫ࡤ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࠒ"), l11lCreated_By_Mucky_Duck (u"ࠩ࡞ࡆࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡘࡥࡤࡧࡱࡸࡱࡿࠠࡂࡦࡧࡩࡩࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨࠓ"),
	l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡊ࡟࡞ࡇࡔࡒࡏࡓࠢࡵࡩࡩࡣࡍࡰࡵࡷࠤ࡛࡯ࡥࡸࡧࡧ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡉ࡞࡝࠲ࡆࡢ࠭ࠔ"), l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡋࡠ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝ࡎࡱࡶࡸࠥࡌࡡࡷࡱࡸࡶ࡮ࡺࡥࡥ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡎࡣ࡛࠰ࡄࡠࠫࠕ"),
	l11lCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡌࡡࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡋࡐࡈࡇࠦࡒࡢࡶ࡬ࡲ࡬ࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨࠖ")]
def l1ll11Created_By_Mucky_Duck():
	if l1llll1lCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࠗ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬ࠘"): l11lCreated_By_Mucky_Duck (u"ࠨ࠳ࠪ࠙"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࠚ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓࡏࡗࡋࡈࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࠛ"), l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࠜ"):l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࠝ"), l11lCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࠞ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧࠟ")})
	if l111ll1Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠨࡶࡵࡹࡪ࠭ࠠ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࠡ"): l11lCreated_By_Mucky_Duck (u"ࠪ࠵ࠬࠢ"), l11lCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࠣ"):l11lCreated_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡠࡈ࡝ࡕࡘࠣࡗࡍࡕࡗࡔ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧࠤ"), l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࠥ"):l11lCreated_By_Mucky_Duck (u"ࠧࡶࡴ࡯ࠫࠦ"), l11lCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩࠧ"):l11lCreated_By_Mucky_Duck (u"ࠩࡷࡺࡸ࡮࡯ࡸࡵࠪࠨ")})
	if l1l11llCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨࠩ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࠪ"): l11lCreated_By_Mucky_Duck (u"ࠬ࡬ࡥࡵࡥ࡫ࡣ࡫ࡧࡶࡴࠩࠫ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࠬ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࡐ࡝ࠥࡌࡁࡗࡑࡘࡖࡎ࡚ࡅࡔ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧ࠭"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࠮"):l11lCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭࠯")})
	if l11l11Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠪࡸࡷࡻࡥࠨ࠰"):
		if l1l111l1Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠫࡹࡸࡵࡦࠩ࠱"):
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ࠲"):l11lCreated_By_Mucky_Duck (u"࠭࡭ࡦࡶࡤࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭࠳"), l11lCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ࠴"):l11lCreated_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝࡜ࡄࡠࡑࡊ࡚ࡁࠡࡕࡈࡘ࡙ࡏࡎࡈࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࠵"), l11lCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭࠶"):l11lCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ࠷")}, is_folder=False, is_playable=False)
	if l1lCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠫࡹࡸࡵࡦࠩ࠸"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠬࡳ࡯ࡥࡧࠪ࠹"):l11lCreated_By_Mucky_Duck (u"࠭ࡡࡥࡦࡲࡲࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ࠺"), l11lCreated_By_Mucky_Duck (u"ࠧ࡯ࡣࡰࡩࠬ࠻"):l11lCreated_By_Mucky_Duck (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝࡜ࡄࡠࡅࡉࡊࡏࡏࠢࡖࡉ࡙࡚ࡉࡏࡉࡖ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ࠼"), l11lCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭࠽"):l11lCreated_By_Mucky_Duck (u"ࠪࡹࡷࡲࠧ࠾")}, is_folder=False, is_playable=False)
	l1llll11Created_By_Mucky_Duck()
        l1ll1lCreated_By_Mucky_Duck()
	setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪ࠿"), l11lCreated_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨࡀ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1l11l11Created_By_Mucky_Duck(content):
	if l1l11llCreated_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"࠭ࡴࡳࡷࡨࠫࡁ"):
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬࡂ"): l11lCreated_By_Mucky_Duck (u"ࠨࡨࡨࡸࡨ࡮࡟ࡧࡣࡹࡷࠬࡃ"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࡄ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡞ࡆࡢࡓ࡙ࠡࡃࡇࡈ࠲ࡕࡎࠡࡈࡄ࡚ࡔ࡛ࡒࡊࡖࡈࡗࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡅ"), l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࡆ"):l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࡇ")})
	if content == l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࡈ"):
		l1lllll1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪ࠭ࡉ")
	elif content == l11lCreated_By_Mucky_Duck (u"ࠨࡶࡹࡷ࡭ࡵࡷࡴࠩࡊ"):
		l1lllll1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠩࡶࡩࡷ࡯ࡥࡴࠩࡋ")
	l11lll1Created_By_Mucky_Duck = l11l111Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"ࠪ࠳ࡲࡵࡶࡪࡧ࠲ࡪ࡮ࡲࡴࡦࡴ࠲ࠩࡸ࠵ࠥࡴ࠱ࡤࡰࡱ࠵ࡡ࡭࡮࠲ࡥࡱࡲ࠯ࡢ࡮࡯࠳ࡦࡲ࡬ࠨࡌ")
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡍ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠸ࠧࡎ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡏ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓࡘ࡚ࠠࡓࡇࡆࡉࡓ࡚ࡌ࡚ࠢࡄࡈࡉࡋࡄ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࡐ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡑ"):l11lll1Created_By_Mucky_Duck %(l1lllll1Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩࡒ")), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡓ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡔ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠸ࠧࡕ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡖ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓࡘ࡚ࠠࡇࡃ࡙ࡓ࡚ࡘࡉࡕࡇࡇ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩࡗ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡘ"):l11lll1Created_By_Mucky_Duck %(l1lllll1Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠩࡩࡥࡻࡵࡲࡪࡶࡨ࡙ࠫ")), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷ࡚ࠫ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦ࡛ࠩ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠸ࠧ࡜"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࡝"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓࡘ࡚ࠠࡓࡃࡗࡍࡓࡍࡓ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭࡞"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࡟"):l11lll1Created_By_Mucky_Duck %(l1lllll1Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠩࡵࡥࡹ࡯࡮ࡨࠩࡠ")), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡡ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡢ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠸ࠧࡣ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡤ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡐࡓࡘ࡚ࠠࡗࡋࡈ࡛ࡊࡊ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬࡥ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡦ"):l11lll1Created_By_Mucky_Duck %(l1lllll1Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠩࡹ࡭ࡪࡽࠧࡧ")), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡨ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡩ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠸ࠧࡪ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫ࡫"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡗࡓࡕࠦࡉࡎࡆࡅ࡟࠴ࡉࡏࡍࡑࡕࡡࡠ࠵ࡂ࡞ࠩ࡬"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬ࡭"):l11lll1Created_By_Mucky_Duck %(l1lllll1Created_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠩ࡬ࡱࡩࡨ࡟࡮ࡣࡵ࡯ࠬ࡮")), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫ࡯"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡰ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠼ࠧࡱ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡲ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡆࡓ࡚ࡔࡔࡓ࡛࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨࡳ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡴ"):l11l111Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"ࠩ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳࠩࡵ"), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡶ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡷ"): l11lCreated_By_Mucky_Duck (u"ࠬࡹࡥࡢࡴࡦ࡬ࠬࡸ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࡹ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡖࡉࡆࡘࡃࡉ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࡺ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࡻ"):l11lCreated_By_Mucky_Duck (u"ࠩࡸࡶࡱ࠭ࡼ"), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࡽ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࡾ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠺ࠧࡿ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࢀ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡊࡉࡓࡘࡅ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࢁ"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢂ"):l11l111Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"ࠩ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳࠩࢃ"), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࢄ"):content})
	md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࢅ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠻ࠧࢆ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࢇ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟࡜ࡉࡆࡘ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ࢈"), l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢉ"):l11l111Created_By_Mucky_Duck+l11lCreated_By_Mucky_Duck (u"ࠩ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳࠩࢊ"), l11lCreated_By_Mucky_Duck (u"ࠪࡧࡴࡴࡴࡦࡰࡷࠫࢋ"):content})
	setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࡵࠪࢌ"), l11lCreated_By_Mucky_Duck (u"ࠬࡳࡥ࡯ࡷ࠰ࡺ࡮࡫ࡷࠨࢍ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1l1l1Created_By_Mucky_Duck(url,content):
	link = open_url(url,verify=False).content
	l1l1lCreated_By_Mucky_Duck = md.regex_get_all(link, l11lCreated_By_Mucky_Duck (u"࠭ࡣ࡭ࡣࡶࡷࡂࠨ࡭࡭࠯࡬ࡸࡪࡳࠢ࠿ࠩࢎ"), l11lCreated_By_Mucky_Duck (u"ࠧ࠽࠱࡫࠶ࡃࡂ࠯ࡴࡲࡤࡲࡃ࠭࢏"))
	items = len(l1l1lCreated_By_Mucky_Duck)
	for a in l1l1lCreated_By_Mucky_Duck:
		name = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠨࡶ࡬ࡸࡱ࡫࠽ࠣࠩ࢐"), l11lCreated_By_Mucky_Duck (u"ࠩࠥࠫ࢑"))
		name = l111Created_By_Mucky_Duck.unescape(name).replace(l11lCreated_By_Mucky_Duck (u"ࠥࡠࡡ࠭ࠢ࢒"),l11lCreated_By_Mucky_Duck (u"ࠦࠬࠨ࢓"))
		url = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠬ࡮ࡲࡦࡨࡀࠦࠬ࢔"), l11lCreated_By_Mucky_Duck (u"࠭ࠢࠨ࢕"))
		l11Created_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠧࡰࡴ࡬࡫࡮ࡴࡡ࡭࠿ࠥࠫ࢖"), l11lCreated_By_Mucky_Duck (u"ࠨࠤࠪࢗ"))
		l111lllCreated_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠩࡰࡰ࡮࠳ࡱࡶࡣ࡯࡭ࡹࡿࠢ࠿ࠩ࢘"), l11lCreated_By_Mucky_Duck (u"ࠪࡀ࢙ࠬ"))
		l1l11l1lCreated_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠫࠧࡳ࡬ࡪ࠯ࡨࡴࡸࠨ࠾ࠨ࢚"), l11lCreated_By_Mucky_Duck (u"ࠬࡂ࠯ࠨ࢛"))
		l1l11l1lCreated_By_Mucky_Duck = l1l11l1lCreated_By_Mucky_Duck.replace(l11lCreated_By_Mucky_Duck (u"࠭࠼ࡴࡲࡤࡲࡃ࠭࢜"),l11lCreated_By_Mucky_Duck (u"ࠧࠡࠩ࢝")).replace(l11lCreated_By_Mucky_Duck (u"ࠨ࠾࡬ࡂࠬ࢞"),l11lCreated_By_Mucky_Duck (u"ࠩࠣࠫ࢟"))
		if content == l11lCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦࡵࠪࢠ"):
			if l111lllCreated_By_Mucky_Duck:
                                title = name
                                md.remove_punctuation(title)
				md.addDir({l11lCreated_By_Mucky_Duck (u"ࠫࡲࡵࡤࡦࠩࢡ"): l11lCreated_By_Mucky_Duck (u"ࠬ࠽ࠧࢢ"), l11lCreated_By_Mucky_Duck (u"࠭࡮ࡢ࡯ࡨࠫࢣ"):l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢ࠮ࠥࡴࠫ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡏ࡝࡜࠱ࡅࡡࠬࢤ") %(name,l111lllCreated_By_Mucky_Duck),
					   l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢥ"):url+l11lCreated_By_Mucky_Duck (u"ࠩࡺࡥࡹࡩࡨࡪࡰࡪ࠲࡭ࡺ࡭࡭ࠩࢦ"), l11lCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭ࢧ"):l11Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࢨ"):content}, {l11lCreated_By_Mucky_Duck (u"ࠬࡹ࡯ࡳࡶࡷ࡭ࡹࡲࡥࠨࢩ"):title},
					  fan_art={l11lCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱࠫࢪ"):l11Created_By_Mucky_Duck}, is_folder=False, item_count=items)
		elif content == l11lCreated_By_Mucky_Duck (u"ࠧࡵࡸࡶ࡬ࡴࡽࡳࠨࢫ"):
			if l1l11l1lCreated_By_Mucky_Duck:
				data = name.split(l11lCreated_By_Mucky_Duck (u"ࠨ࠯ࠣࡗࡪࡧࡳࡰࡰࠪࢬ"))
				l111111Created_By_Mucky_Duck = data[0].strip()
				md.remove_punctuation(l111111Created_By_Mucky_Duck)
				try:
					l11l11lCreated_By_Mucky_Duck = data[1].strip()
				except:
					l11l11lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠩࠪࢭ")
				md.addDir({l11lCreated_By_Mucky_Duck (u"ࠪࡱࡴࡪࡥࠨࢮ"): l11lCreated_By_Mucky_Duck (u"ࠫ࠸࠭ࢯ"), l11lCreated_By_Mucky_Duck (u"ࠬࡴࡡ࡮ࡧࠪࢰ"):l11lCreated_By_Mucky_Duck (u"࡛࠭ࡃ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࠥࡡࡉ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡍࡢࡡ࠯ࡃ࡟ࠪࢱ") %(name,l1l11l1lCreated_By_Mucky_Duck),
					   l11lCreated_By_Mucky_Duck (u"ࠧࡵ࡫ࡷࡰࡪ࠭ࢲ"):l111111Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬࢳ"):url+l11lCreated_By_Mucky_Duck (u"ࠩࡺࡥࡹࡩࡨࡪࡰࡪ࠲࡭ࡺ࡭࡭ࠩࢴ"), l11lCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭ࢵ"):l11Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠫࡨࡵ࡮ࡵࡧࡱࡸࠬࢶ"):content, l11lCreated_By_Mucky_Duck (u"ࠬࡹࡥࡢࡵࡲࡲࠬࢷ"):l11l11lCreated_By_Mucky_Duck},
					  {l11lCreated_By_Mucky_Duck (u"࠭ࡳࡰࡴࡷࡸ࡮ࡺ࡬ࡦࠩࢸ"):l111111Created_By_Mucky_Duck}, fan_art={l11lCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲࠬࢹ"):l11Created_By_Mucky_Duck}, item_count=items)
	try:
		l1l1Created_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠨ࠾࡯࡭ࠥࡩ࡬ࡢࡵࡶࡁࠧࡴࡥࡹࡶࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯ࠬࡂ࠭ࠧࠦࡤࡢࡶࡤ࠱ࡨ࡯࠭ࡱࡣࡪ࡭ࡳࡧࡴࡪࡱࡱ࠱ࡵࡧࡧࡦ࠿ࠥ࠲࠯ࡅࠢࠡࡴࡨࡰࡂࠨ࡮ࡦࡺࡷࠦࡃ࠭ࢺ")).findall(link)[0]
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫ࠧࢻ"): l11lCreated_By_Mucky_Duck (u"ࠪ࠶ࠬࢼ"), l11lCreated_By_Mucky_Duck (u"ࠫࡳࡧ࡭ࡦࠩࢽ"):l11lCreated_By_Mucky_Duck (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡄ࠾ࡏࡧࡻࡸࠥࡖࡡࡨࡧࡁࡂࡃࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠫࢾ"), l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠪࢿ"):l1l1Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࣀ"):content})
	except: pass
	if content == l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡺ࡮࡫ࡳࠨࣁ"):
		setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩࣂ"), l11lCreated_By_Mucky_Duck (u"ࠪࡱࡴࡼࡩࡦ࠯ࡹ࡭ࡪࡽࠧࣃ"))
	elif content == l11lCreated_By_Mucky_Duck (u"ࠫࡹࡼࡳࡩࡱࡺࡷࠬࣄ"):
		setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ࣅ"), l11lCreated_By_Mucky_Duck (u"࠭ࡳࡩࡱࡺ࠱ࡻ࡯ࡥࡸࠩࣆ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1111l1Created_By_Mucky_Duck(title, url, l111llCreated_By_Mucky_Duck, content, l11l11lCreated_By_Mucky_Duck):
	link = open_url(url,verify=False).content
	l111l1lCreated_By_Mucky_Duck = url
	l11l1llCreated_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠧࡪࡦ࠽ࠤࠧ࠮࡛࡟ࠤࡠ࠯࠮ࠨࠧࣇ")).findall(link)[0]
	request_url = l11lCreated_By_Mucky_Duck (u"ࠨࠧࡶ࠳ࡦࡰࡡࡹ࠱ࡰࡳࡻ࡯ࡥࡠࡧࡳ࡭ࡸࡵࡤࡦࡵ࠲ࠩࡸ࠭ࣈ") %(l11l111Created_By_Mucky_Duck,l11l1llCreated_By_Mucky_Duck)
	headers = {l11lCreated_By_Mucky_Duck (u"ࠩࡄࡧࡨ࡫ࡰࡵ࠯ࡈࡲࡨࡵࡤࡪࡰࡪࠫࣉ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡫ࡿ࡯ࡰ࠭ࠢࡧࡩ࡫ࡲࡡࡵࡧ࠯ࠤࡸࡪࡣࡩ࠮ࠣࡦࡷ࠭࣊"), l11lCreated_By_Mucky_Duck (u"ࠫࡗ࡫ࡦࡦࡴࡨࡶࠬ࣋"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩ࣌"):md.User_Agent()}
	l1ll1111Created_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
	l11ll1lCreated_By_Mucky_Duck = md.regex_get_all(l1ll1111Created_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"࠭ࡨࡵ࡯࡯ࠫ࣍")], l11lCreated_By_Mucky_Duck (u"ࠧ࠿ࡕࡨࡶࡻ࡫ࡲࠡ࠳࠳ࡀࠬ࣎"), l11lCreated_By_Mucky_Duck (u"ࠨࠤࡦࡰࡪࡧࡲࡧ࡫ࡻ࣏ࠦࠬ"))
	l1l1lCreated_By_Mucky_Duck = md.regex_get_all(str(l11ll1lCreated_By_Mucky_Duck), l11lCreated_By_Mucky_Duck (u"ࠩ࠿ࡥ࣐ࠬ"), l11lCreated_By_Mucky_Duck (u"ࠪࡀ࠴ࡧ࠾ࠨ࣑"))
	items = len(l1l1lCreated_By_Mucky_Duck)
	for a in l1l1lCreated_By_Mucky_Duck:
		name = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠫࡹ࡯ࡴ࡭ࡧࡀ࣒ࠦࠬ"), l11lCreated_By_Mucky_Duck (u"ࠬࠨ࣓ࠧ"))
		name = l111Created_By_Mucky_Duck.unescape(name).replace(l11lCreated_By_Mucky_Duck (u"ࠨ࡜࡝ࠩࠥࣔ"),l11lCreated_By_Mucky_Duck (u"ࠢࠨࠤࣕ"))
		l1l1lll1Created_By_Mucky_Duck = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠨࡦࡤࡸࡦ࠳ࡩࡥ࠿ࠥࠫࣖ"), l11lCreated_By_Mucky_Duck (u"ࠩࠥࠫࣗ"))
		headers = l111l1lCreated_By_Mucky_Duck + l11lCreated_By_Mucky_Duck (u"ࠪࡠࢁ࠭ࣘ") + l1l1lll1Created_By_Mucky_Duck + l11lCreated_By_Mucky_Duck (u"ࠫࡡࢂࠧࣙ") + l11l1llCreated_By_Mucky_Duck
		url =  l11lCreated_By_Mucky_Duck (u"ࠬࠫࡳ࠰ࡣ࡭ࡥࡽ࠵࡭ࡰࡸ࡬ࡩࡤࡹ࡯ࡶࡴࡦࡩࡸ࠵ࠥࡴࠩࣚ") %(l11l111Created_By_Mucky_Duck,l1l1lll1Created_By_Mucky_Duck)
		try:
			l1l1l111Created_By_Mucky_Duck = name.split(l11lCreated_By_Mucky_Duck (u"࠭ࡅࡱ࡫ࡶࡳࡩ࡫ࠧࣛ"))[1].strip()[:2]
		except:pass
		fan_art = {l11lCreated_By_Mucky_Duck (u"ࠧࡪࡥࡲࡲࠬࣜ"):l111llCreated_By_Mucky_Duck}
		md.remove_punctuation(title)
		md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ࣝ"): l11lCreated_By_Mucky_Duck (u"ࠩ࠺ࠫࣞ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࣟ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧ࣠") %name,
			   l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩ࣡"):url, l11lCreated_By_Mucky_Duck (u"࠭ࡩࡤࡱࡱ࡭ࡲࡧࡧࡦࠩ࣢"):l111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡤࡱࡱࡸࡪࡴࡴࠨࣣ"):l11lCreated_By_Mucky_Duck (u"ࠨࡧࡳ࡭ࡸࡵࡤࡦࡵࠪࣤ"), l11lCreated_By_Mucky_Duck (u"ࠩࡴࡹࡪࡸࡹࠨࣥ"):headers},
			  {l11lCreated_By_Mucky_Duck (u"ࠪࡷࡴࡸࡴࡵ࡫ࡷࡰࡪࣦ࠭"):title, l11lCreated_By_Mucky_Duck (u"ࠫࡸ࡫ࡡࡴࡱࡱࠫࣧ"):l11l11lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠬ࡫ࡰࡪࡵࡲࡨࡪ࠭ࣨ"):l1l1l111Created_By_Mucky_Duck},
			  fan_art, is_folder=False, item_count=items)
	setView(l1111llCreated_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࡳࠨࣩ"), l11lCreated_By_Mucky_Duck (u"ࠧࡦࡲ࡬࠱ࡻ࡯ࡥࡸࠩ࣪"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1l111llCreated_By_Mucky_Duck(url, content):
	l111l1Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡕࡲࡶࡹࠦࡍࡦࡶ࡫ࡳࡩ࠭࣫"),sort)
	l111l11Created_By_Mucky_Duck = l11llCreated_By_Mucky_Duck[l111l1Created_By_Mucky_Duck]
	link = open_url(url,verify=False).content
	match = re.compile(l11lCreated_By_Mucky_Duck (u"ࠩ࠿࡭ࡳࡶࡵࡵࠢࡦࡰࡦࡹࡳ࠾ࠤࡪࡩࡳࡸࡥ࠮࡫ࡧࡷࠧࠦࡶࡢ࡮ࡸࡩࡂࠨࠨ࠯ࠬࡂ࠭ࠧࠦ࡮ࡢ࡯ࡨࡁࠧ࠴ࠪࡀࠤ࡟ࡲ࠳࠰࠿ࡵࡻࡳࡩࡂࠨࡣࡩࡧࡦ࡯ࡧࡵࡸࠣࠢࡁࠬ࠳࠰࠿ࠪ࠾࠲ࡰࡦࡨࡥ࡭ࡀࠪ࣬")).findall(link)
	for l1llll1Created_By_Mucky_Duck,name in match:
		name = name.replace(l11lCreated_By_Mucky_Duck (u"ࠪࠤ࣭ࠬ"),l11lCreated_By_Mucky_Duck (u"࣮ࠫࠬ"))
		if content == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࣯࠭"):
			url = l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰ࡵࡨࡶ࡮࡫ࡳ࠰ࠧࡶ࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࣰࠩ") %(l11l111Created_By_Mucky_Duck,l111l11Created_By_Mucky_Duck,l1llll1Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࣱࠬ"): l11lCreated_By_Mucky_Duck (u"ࠨ࠴ࣲࠪ"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧࣳ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ࣴ") %name, l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨࣵ"):url, l11lCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹࣶ࠭"):content})
		elif content == l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ࣷ"):
			url = l11lCreated_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡰࡳࡻ࡯ࡥ࠰ࠧࡶ࠳ࠪࡹ࠯ࡢ࡮࡯࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩࣸ") %(l11l111Created_By_Mucky_Duck,l111l11Created_By_Mucky_Duck,l1llll1Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪࣹ࠭"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵ࣺࠫ"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨࣻ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧࣼ") %name, l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩࣽ"):url, l11lCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧࣾ"):content})
	setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭ࣿ"), l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫऀ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l11l1Created_By_Mucky_Duck(url, content):
	l111l1Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠩࡖࡩࡱ࡫ࡣࡵࠢࡖࡳࡷࡺࠠࡎࡧࡷ࡬ࡴࡪࠧँ"),sort)
	l111l11Created_By_Mucky_Duck = l11llCreated_By_Mucky_Duck[l111l1Created_By_Mucky_Duck]
	l11ll1Created_By_Mucky_Duck = md.numeric_select(l11lCreated_By_Mucky_Duck (u"ࠪࡉࡳࡺࡥࡳࠢ࡜ࡩࡦࡸࠧं"), l11lCreated_By_Mucky_Duck (u"ࠫ࠷࠶࠱࠸ࠩः"))
	if content == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ऄ"):
		l1l1l1Created_By_Mucky_Duck(l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰ࡵࡨࡶ࡮࡫ࡳ࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࠫࡳ࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩअ") %(l11l111Created_By_Mucky_Duck,l111l11Created_By_Mucky_Duck,l11ll1Created_By_Mucky_Duck), content)
	elif content == l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧआ"):
		l1l1l1Created_By_Mucky_Duck(l11lCreated_By_Mucky_Duck (u"ࠨࠧࡶ࠳ࡲࡵࡶࡪࡧ࠲ࡪ࡮ࡲࡴࡦࡴ࠲ࡱࡴࡼࡩࡦ࠱ࠨࡷ࠴ࡧ࡬࡭࠱ࡤࡰࡱ࠵ࠥࡴ࠱ࡤࡰࡱ࠵ࡡ࡭࡮ࠪइ") %(l11l111Created_By_Mucky_Duck,l111l11Created_By_Mucky_Duck,l11ll1Created_By_Mucky_Duck), content)
	setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠩࡩ࡭ࡱ࡫ࡳࠨई"), l11lCreated_By_Mucky_Duck (u"ࠪࡱࡪࡴࡵ࠮ࡸ࡬ࡩࡼ࠭उ"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l1ll1lCreated_By_Mucky_Duck():
	link = open_url(l11lCreated_By_Mucky_Duck (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡶࡡࡴࡶࡨࡦ࡮ࡴ࠮ࡤࡱࡰ࠳ࡷࡧࡷ࠰ࡅࡩ࠸ࡈ࠹ࡵࡉ࠳ࠪऊ")).content
	version = re.findall(l11lCreated_By_Mucky_Duck (u"ࡷ࠭ࡶࡦࡴࡶ࡭ࡴࡴࠠ࠾ࠢࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࠬऋ"), str(link), re.I|re.DOTALL)[0]
	with open(xbmc.translatePath(l11lCreated_By_Mucky_Duck (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࡴࡥࡵ࡭ࡵࡺ࠮࡮ࡱࡧࡹࡱ࡫࠮࡮ࡷࡦ࡯ࡾࡹ࠮ࡤࡱࡰࡱࡴࡴ࠯ࡢࡦࡧࡳࡳ࠴ࡸ࡮࡮ࠪऌ")), l11lCreated_By_Mucky_Duck (u"ࠧࡳ࠭ࠪऍ")) as f:
		l1111lCreated_By_Mucky_Duck = f.read()
		if re.search(l11lCreated_By_Mucky_Duck (u"ࡳࠩࡹࡩࡷࡹࡩࡰࡰࡀࠦࠪࡹࠢࠨऎ") %version, l1111lCreated_By_Mucky_Duck):
			l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"࡙ࠩࡩࡷࡹࡩࡰࡰࠣࡇ࡭࡫ࡣ࡬ࠢࡒࡏࠬए"))
		else:
			l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࡛ࠥࡷࡵ࡮ࡨ࡙ࠢࡩࡷࡹࡩࡰࡰࠣࡓ࡫ࠦࡍࡶࡥ࡮ࡽࡸࠦࡃࡰ࡯ࡰࡳࡳࠦࡍࡰࡦࡸࡰࡪࠨऐ")
			l1ll1l1lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠦࡕࡲࡥࡢࡵࡨࠤࡎࡴࡳࡵࡣ࡯ࡰࠥࡉ࡯ࡳࡴࡨࡧࡹࠦࡖࡦࡴࡶ࡭ࡴࡴࠠࡇࡴࡲࡱ࡚ࠥࡨࡦࠢࡕࡩࡵࡵࠢऑ")
			l1ll1ll1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࡆ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠ࡬ࡹࡺࡰ࠻࠱࠲ࡱࡺࡩ࡫ࡺࡵ࠱ࡱࡪࡪࡩࡢࡲࡲࡶࡹࡧ࡬࠵࡭ࡲࡨ࡮࠴࡭࡭࡝࠲ࡇࡔࡒࡏࡓ࡟ࠥऒ")
			l111Created_By_Mucky_Duck.show_ok_dialog([l1Created_By_Mucky_Duck, l1ll1l1lCreated_By_Mucky_Duck, l1ll1ll1Created_By_Mucky_Duck], l1ll1Created_By_Mucky_Duck)
			xbmc.executebuiltin(l11lCreated_By_Mucky_Duck (u"ࠨࡘࡃࡏࡆ࠲ࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡖࡲࡧࡥࡹ࡫ࠨࡱࡣࡷ࡬࠱ࡸࡥࡱ࡮ࡤࡧࡪ࠯ࠢओ"))
			xbmc.executebuiltin(l11lCreated_By_Mucky_Duck (u"࡙ࠢࡄࡐࡇ࠳ࡇࡣࡵ࡫ࡹࡥࡹ࡫ࡗࡪࡰࡧࡳࡼ࠮ࡈࡰ࡯ࡨ࠭ࠧऔ"))
def l1l111Created_By_Mucky_Duck(url, content):
	l111l1Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡕࡲࡶࡹࠦࡍࡦࡶ࡫ࡳࡩ࠭क"),sort)
	l111l11Created_By_Mucky_Duck = l11llCreated_By_Mucky_Duck[l111l1Created_By_Mucky_Duck]
	link = open_url(url,verify=False).content
	match=re.compile(l11lCreated_By_Mucky_Duck (u"ࠩ࠿࡭ࡳࡶࡵࡵࠢࡦࡰࡦࡹࡳ࠾ࠤࡦࡳࡺࡴࡴࡳࡻ࠰࡭ࡩࡹࠢࠡࡸࡤࡰࡺ࡫࠽ࠣࠪ࠱࠮ࡄ࠯ࠢࠡࡰࡤࡱࡪࡃࠢ࠯ࠬࡂࠦࡡࡴ࠮ࠫࡁࡷࡽࡵ࡫࠽ࠣࡥ࡫ࡩࡨࡱࡢࡰࡺࠥࠤࡃ࠮࠮ࠫࡁࠬࡀ࠴ࡲࡡࡣࡧ࡯ࡂࠬख")).findall(link)
	for l1lll11Created_By_Mucky_Duck,name in match:
		name = name.replace(l11lCreated_By_Mucky_Duck (u"ࠪࠤࠬग"),l11lCreated_By_Mucky_Duck (u"ࠫࠬघ"))
		if content == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡶࡴࡪࡲࡻࡸ࠭ङ"):
			url = l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡨ࡬ࡰࡹ࡫ࡲ࠰ࡵࡨࡶ࡮࡫ࡳ࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩच") %(l11l111Created_By_Mucky_Duck,l111l11Created_By_Mucky_Duck,l1lll11Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬछ"): l11lCreated_By_Mucky_Duck (u"ࠨ࠴ࠪज"), l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧझ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭ञ") %name, l11lCreated_By_Mucky_Duck (u"ࠫࡺࡸ࡬ࠨट"):url, l11lCreated_By_Mucky_Duck (u"ࠬࡩ࡯࡯ࡶࡨࡲࡹ࠭ठ"):content})
		elif content == l11lCreated_By_Mucky_Duck (u"࠭࡭ࡰࡸ࡬ࡩࡸ࠭ड"):
			url = l11lCreated_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡱࡴࡼࡩࡦ࠱ࡩ࡭ࡱࡺࡥࡳ࠱ࡰࡳࡻ࡯ࡥ࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࠧࡶ࠳ࡦࡲ࡬࠰ࡣ࡯ࡰ࠴ࡧ࡬࡭ࠩढ") %(l11l111Created_By_Mucky_Duck,l111l11Created_By_Mucky_Duck,l1lll11Created_By_Mucky_Duck)
			md.addDir({l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡲࡨࡪ࠭ण"): l11lCreated_By_Mucky_Duck (u"ࠩ࠵ࠫत"), l11lCreated_By_Mucky_Duck (u"ࠪࡲࡦࡳࡥࠨथ"):l11lCreated_By_Mucky_Duck (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞࠳ࡇࡣࠧद") %name, l11lCreated_By_Mucky_Duck (u"ࠬࡻࡲ࡭ࠩध"):url, l11lCreated_By_Mucky_Duck (u"࠭ࡣࡰࡰࡷࡩࡳࡺࠧन"):content})
	setView(l1111llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡧ࡫࡯ࡩࡸ࠭ऩ"), l11lCreated_By_Mucky_Duck (u"ࠨ࡯ࡨࡲࡺ࠳ࡶࡪࡧࡺࠫप"))
	l111Created_By_Mucky_Duck.end_of_directory()
def l11l1lCreated_By_Mucky_Duck(content, query):
	try:
		if query:
			search = query.replace(l11lCreated_By_Mucky_Duck (u"ࠩࠣࠫफ"),l11lCreated_By_Mucky_Duck (u"ࠪ࠯ࠬब"))
		else:
			search = md.search()
			if search == l11lCreated_By_Mucky_Duck (u"ࠫࠬभ"):
				md.notification(l11lCreated_By_Mucky_Duck (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠ࡟ࡇࡣࡅࡎࡒࡗ࡝ࠥࡗࡕࡆࡔ࡜࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞࠮ࡄࡦࡴࡸࡴࡪࡰࡪࠤࡸ࡫ࡡࡳࡥ࡫ࠫम"),l1l1l11lCreated_By_Mucky_Duck)
				return
			else:
				pass
		url = l11lCreated_By_Mucky_Duck (u"࠭ࠥࡴ࠱ࡰࡳࡻ࡯ࡥ࠰ࡵࡨࡥࡷࡩࡨ࠰ࠧࡶࠫय") %(l11l111Created_By_Mucky_Duck,search)
		l1l1l1Created_By_Mucky_Duck(url,content)
	except:
		md.notification(l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡡࡂ࡞ࡕࡲࡶࡷࡿࠠࡏࡱࠣࡖࡪࡹࡵ࡭ࡶࡶ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩर"),l1l1l11lCreated_By_Mucky_Duck)
def __1l1l1llCreated_By_Mucky_Duck(data):
        l1l1ll1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠨࠩऱ")
        l1l1l1lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠩࠪल")
        try:
            data = l11lCreated_By_Mucky_Duck (u"ࠪࠬࠬळ") + data.split(l11lCreated_By_Mucky_Duck (u"ࠦ࠭ࡥࠤࠥࠫࠬࠤ࠭࠭࡟ࠨࠫ࠾ࠦऴ"))[0].split(l11lCreated_By_Mucky_Duck (u"ࠧ࠵ࠪࠡࡢࠧࠨࡥࠦࠪ࠰ࠤव"))[-1].strip()
            data = data.replace(l11lCreated_By_Mucky_Duck (u"࠭ࠨࡠࡡࠧ࠭ࡠࠪࠤࠥ࡟ࠪश"), l11lCreated_By_Mucky_Duck (u"ࠧ࡝ࠩࠥࡠࠬ࠭ष"))
            data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠨࠪࡢࡣࠩ࠯࡛ࡠࠦࡠࠫस"), l11lCreated_By_Mucky_Duck (u"ࠩࠥࡠࡡࡢ࡜ࠣࠩह"))
            data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠪࠬࡴࡤ࡟࡟ࡱࠬࠫऺ"), l11lCreated_By_Mucky_Duck (u"ࠫ࠸࠭ऻ"))
            data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠬ࠮ࡣ࡟ࡡࡡࡳ࠮़࠭"), l11lCreated_By_Mucky_Duck (u"࠭࠰ࠨऽ"))
            data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠧࠩࡡࠧࠨ࠮࠭ा"), l11lCreated_By_Mucky_Duck (u"ࠨ࠳ࠪि"))
            data = data.replace(l11lCreated_By_Mucky_Duck (u"ࠩࠫࠨࠩࡥࠩࠨी"), l11lCreated_By_Mucky_Duck (u"ࠪ࠸ࠬु"))
            code = l11lCreated_By_Mucky_Duck (u"ࠫࠬ࠭ࡤࡦࡨࠣࡶࡪࡺࡁࠩࠫ࠽ࠎࠥࠦࠠࠡࡥ࡯ࡥࡸࡹࠠࡊࡰࡩ࡭ࡽࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡥ࡟ࡪࡰ࡬ࡸࡤࡥࠨࡴࡧ࡯ࡪ࠱ࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡨࡰ࡫࠴ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡ࠿ࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡦࡨࠣࡣࡤࡸ࡯ࡳࡡࡢࠬࡸ࡫࡬ࡧ࠮ࠣࡳࡹ࡮ࡥࡳࠫ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡌࡲ࡫࡯ࡸࠩ࡮ࡤࡱࡧࡪࡡࠡࡺ࠯ࠤࡸ࡫࡬ࡧ࠿ࡶࡩࡱ࡬ࠬࠡࡱࡷ࡬ࡪࡸ࠽ࡰࡶ࡫ࡩࡷࡀࠠࡴࡧ࡯ࡪ࠳࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠨࡰࡶ࡫ࡩࡷ࠲ࠠࡹࠫࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡥࡧࠢࡢࡣࡴࡸ࡟ࡠࠪࡶࡩࡱ࡬ࠬࠡࡱࡷ࡬ࡪࡸࠩ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠࡴࡧ࡯ࡪ࠳࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠨࡰࡶ࡫ࡩࡷ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡥ࡟ࡳ࡮ࡶ࡬࡮࡬ࡴࡠࡡࠫࡷࡪࡲࡦ࠭ࠢࡲࡸ࡭࡫ࡲࠪ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡋࡱࡪ࡮ࡾࠨ࡭ࡣࡰࡦࡩࡧࠠࡹ࠮ࠣࡷࡪࡲࡦ࠾ࡵࡨࡰ࡫࠲ࠠࡰࡶ࡫ࡩࡷࡃ࡯ࡵࡪࡨࡶ࠿ࠦࡳࡦ࡮ࡩ࠲࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠮࡯ࡵࡪࡨࡶ࠱ࠦࡸࠪࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡࡡࡢࡶࡸ࡮ࡩࡧࡶࡢࡣ࠭ࡹࡥ࡭ࡨ࠯ࠤࡴࡺࡨࡦࡴࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡷࡪࡲࡦ࠯ࡨࡸࡲࡨࡺࡩࡰࡰࠫࡳࡹ࡮ࡥࡳࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡫ࡦࠡࡡࡢࡧࡦࡲ࡬ࡠࡡࠫࡷࡪࡲࡦ࠭ࠢࡹࡥࡱࡻࡥ࠲࠮ࠣࡺࡦࡲࡵࡦ࠴ࠬ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡷࡪࡲࡦ࠯ࡨࡸࡲࡨࡺࡩࡰࡰࠫࡺࡦࡲࡵࡦ࠳࠯ࠤࡻࡧ࡬ࡶࡧ࠵࠭ࠏࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡺࡡࡤࡨࡩ࠮ࡸ࠭ࠢࡼ࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡵࡴࡼ࠾ࠥࡸࡥࡵࡷࡵࡲࠥࡾࠠࠬࠢࡼࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡫ࡸࡤࡧࡳࡸࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡵࡩࡹࡻࡲ࡯ࠢࡶࡸࡷ࠮ࡸࠪࠢ࠮ࠤࡸࡺࡲࠩࡻࠬࠎࠥࠦࠠࠡࡺࠣࡁࠥࡏ࡮ࡧ࡫ࡻࠬࡲࡿ࡟ࡢࡦࡧ࠭ࠏࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࠨࡷࠏࡶࡡࡳࡣࡰࠤࡂࠦࡲࡦࡶࡄࠬ࠮࠭ࠧࠨू")
            l1l11lllCreated_By_Mucky_Duck = {l11lCreated_By_Mucky_Duck (u"ࠧࡥ࡟ࡣࡷ࡬ࡰࡹ࡯࡮ࡴࡡࡢࠦृ"): None, l11lCreated_By_Mucky_Duck (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨॄ"):__name__, l11lCreated_By_Mucky_Duck (u"ࠧࡴࡶࡵࠫॅ"):str, l11lCreated_By_Mucky_Duck (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫॆ"):Exception}
            l1l111lCreated_By_Mucky_Duck = { l11lCreated_By_Mucky_Duck (u"ࠩࡳࡥࡷࡧ࡭ࠨे"): None }
            exec( code % data.replace(l11lCreated_By_Mucky_Duck (u"ࠪ࠯ࠬै"),l11lCreated_By_Mucky_Duck (u"ࠫࢁࡾࡼࠨॉ")), l1l11lllCreated_By_Mucky_Duck, l1l111lCreated_By_Mucky_Duck)
            data = l1l111lCreated_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠬࡶࡡࡳࡣࡰࠫॊ")].decode(l11lCreated_By_Mucky_Duck (u"࠭ࡳࡵࡴ࡬ࡲ࡬ࡥࡥࡴࡥࡤࡴࡪ࠭ो"))
            data = re.compile(l11lCreated_By_Mucky_Duck (u"ࠧࠨࠩࡀ࡟ࠬࠨ࡝ࠩ࡝ࡡࠦࡣ࠭࡝ࠬࡁࠬ࡟ࠬࠨ࡝ࠨࠩࠪौ")).findall(data)
            x = data[0]
            y = data[1]
        except Exception as e:
            l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡹ࠱ࡼࠤࡩ࡫ࡣࡰࡦࡨࠤ࠭࠷ࠩࠨ्"))
        return {l11lCreated_By_Mucky_Duck (u"ࠩࡻࠫॎ"): x, l11lCreated_By_Mucky_Duck (u"ࠪࡽࠬॏ"): y}
def __1l1ll11Created_By_Mucky_Duck(script):
        try:
            l11111Created_By_Mucky_Duck = jsunfuck.l111lCreated_By_Mucky_Duck(script).decode()
            x = re.search(l11lCreated_By_Mucky_Duck (u"ࠫࠬ࠭࡟ࡹ࠿࡞ࠫࠧࡣࠨ࡜ࡠࠥࠫࡢ࠱ࠩࠨࠩࠪॐ"), l11111Created_By_Mucky_Duck).group(1)
            y = re.search(l11lCreated_By_Mucky_Duck (u"ࠬ࠭ࠧࡠࡻࡀ࡟ࠬࠨ࡝ࠩ࡝ࡡࠦࠬࡣࠫࠪࠩࠪࠫ॑"), l11111Created_By_Mucky_Duck).group(1)
            return {l11lCreated_By_Mucky_Duck (u"࠭ࡸࠨ॒"): x, l11lCreated_By_Mucky_Duck (u"ࠧࡺࠩ॓"): y}
        except Exception as e:
            l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡹ࠱ࡼࠤࡩ࡫ࡣࡰࡦࡨࠤ࠭࠸ࠩࠨ॔"))
def __1l1ll1lCreated_By_Mucky_Duck(script):
        try:
            x = re.search(l11lCreated_By_Mucky_Duck (u"ࠩࠪࠫࡤࡾ࠽࡜ࠩࠥࡡ࠭ࡡ࡞ࠣࠩࡠ࠯࠮࠭ࠧࠨॕ"), script).group(1)
            y = re.search(l11lCreated_By_Mucky_Duck (u"ࠪࠫࠬࡥࡹ࠾࡝ࠪࠦࡢ࠮࡛࡟ࠤࠪࡡ࠰࠯ࠧࠨࠩॖ"), script).group(1)
            return {l11lCreated_By_Mucky_Duck (u"ࠫࡽ࠭ॗ"): x, l11lCreated_By_Mucky_Duck (u"ࠬࡿࠧक़"): y}
        except Exception as e:
            l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡾ࠯ࡺࠢࡧࡩࡨࡵࡤࡦࠢࠫ࠷࠮࠭ख़"))
def l1lll1Created_By_Mucky_Duck(url,name,l111llCreated_By_Mucky_Duck,content,l1llllCreated_By_Mucky_Duck,query):
        try:
                if content == l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧग़"):
                        link = open_url(url,verify=False).content
                        l111l1lCreated_By_Mucky_Duck = url
                        headers = {l11lCreated_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬज़"):md.User_Agent()}
                        link = open_url(url, headers=headers).content
                        l11l1llCreated_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠩ࡬ࡨ࠿ࠦࠢࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩड़")).findall(link)[0]
                        request_url = l11lCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡲࡵࡶࡪࡧࡢࡩࡵ࡯ࡳࡰࡦࡨࡷ࠴ࠫࡳࠨढ़") %(l11l111Created_By_Mucky_Duck,l11l1llCreated_By_Mucky_Duck)
                        headers = {l11lCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡊࡴࡣࡰࡦ࡬ࡲ࡬࠭फ़"):l11lCreated_By_Mucky_Duck (u"ࠬ࡭ࡺࡪࡲ࠯ࠤࡩ࡫ࡦ࡭ࡣࡷࡩ࠱ࠦࡳࡥࡥ࡫࠰ࠥࡨࡲࠨय़"), l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦࡨࡨࡶࡪࡸࠧॠ"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫॡ"):md.User_Agent()}
                        l1ll1111Created_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
                        l1l1lll1Created_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠨࡦࡤࡸࡦ࠳ࡩࡥ࠿ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࠬॢ")).findall(l1ll1111Created_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡲࡲࠧॣ")])[1]
                else:
                        l1ll11llCreated_By_Mucky_Duck = re.split(l11lCreated_By_Mucky_Duck (u"ࡵࠫࡡࢂࠧ।"), str(query), re.I)
                        l111l1lCreated_By_Mucky_Duck = l1ll11llCreated_By_Mucky_Duck[0].replace(l11lCreated_By_Mucky_Duck (u"ࠫࡡࡢࠧ॥"),l11lCreated_By_Mucky_Duck (u"ࠬ࠭०"))
                        l1l1lll1Created_By_Mucky_Duck = l1ll11llCreated_By_Mucky_Duck[1].replace(l11lCreated_By_Mucky_Duck (u"࠭࡜࡝ࠩ१"),l11lCreated_By_Mucky_Duck (u"ࠧࠨ२"))
                        l11l1llCreated_By_Mucky_Duck = l1ll11llCreated_By_Mucky_Duck[2].replace(l11lCreated_By_Mucky_Duck (u"ࠨ࡞࡟ࠫ३"),l11lCreated_By_Mucky_Duck (u"ࠩࠪ४"))
                l1ll1l11Created_By_Mucky_Duck = int(time.time() * 10000)
                l1lll1lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡲࡵࡶࡪࡧࡢࡸࡴࡱࡥ࡯ࠩ५") %l11l111Created_By_Mucky_Duck
                params = {l11lCreated_By_Mucky_Duck (u"ࠫࡪ࡯ࡤࠨ६"):l1l1lll1Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠬࡳࡩࡥࠩ७"):l11l1llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭࡟ࠨ८"):l1ll1l11Created_By_Mucky_Duck}
                headers = {l11lCreated_By_Mucky_Duck (u"ࠧࡂࡥࡦࡩࡵࡺࠧ९"):l11lCreated_By_Mucky_Duck (u"ࠨࡶࡨࡼࡹ࠵ࡪࡢࡸࡤࡷࡨࡸࡩࡱࡶ࠯ࠤࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡥࡻࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴࡫ࡣ࡮ࡣࡶࡧࡷ࡯ࡰࡵ࠮ࠣࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰ࡩࡨࡳࡡࡴࡥࡵ࡭ࡵࡺࠬࠡࠬ࠲࠮ࡀࠦࡱ࠾࠲࠱࠴࠶࠭॰"),
                           l11lCreated_By_Mucky_Duck (u"ࠩࡄࡧࡨ࡫ࡰࡵ࠯ࡈࡲࡨࡵࡤࡪࡰࡪࠫॱ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡫ࡿ࡯ࡰ࠭ࠢࡧࡩ࡫ࡲࡡࡵࡧ࠯ࠤࡸࡪࡣࡩ࠮ࠣࡦࡷ࠭ॲ"), l11lCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡑࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ॳ"):l11lCreated_By_Mucky_Duck (u"ࠬ࡫࡮࠮ࡗࡖ࠰ࡪࡴ࠻ࡲ࠿࠳࠲࠽࠭ॴ"),
                           l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦࡨࡨࡶࡪࡸࠧॵ"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫॶ"):md.User_Agent(), l11lCreated_By_Mucky_Duck (u"ࠨ࡚࠰ࡖࡪࡷࡵࡦࡵࡷࡩࡩ࠳ࡗࡪࡶ࡫ࠫॷ"):l11lCreated_By_Mucky_Duck (u"࡛ࠩࡑࡑࡎࡴࡵࡲࡕࡩࡶࡻࡥࡴࡶࠪॸ")}
                data = open_url(l1lll1lCreated_By_Mucky_Duck, params=params, headers=headers, verify=False).content
                if l11lCreated_By_Mucky_Duck (u"ࠪࠨࡤࠪࠧॹ") in data:
                    params = __1l1l1llCreated_By_Mucky_Duck(data)
                elif data.startswith(l11lCreated_By_Mucky_Duck (u"ࠫࡠࡣࠧॺ")) and data.endswith(l11lCreated_By_Mucky_Duck (u"ࠬ࠮ࠩࠨॻ")):
                    params = __1l1ll11Created_By_Mucky_Duck(data)
                else:
                    params = __1l1ll1lCreated_By_Mucky_Duck(data)
                if params is None:
                    l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"࠭ࡕ࡯ࡴࡨࡧࡴ࡭࡮ࡪࡼࡨࡨࠥࡰࡳࠡ࡫ࡱࠤࠪࡹࠧॼ") % (l1lll1lCreated_By_Mucky_Duck))
                l1ll111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡥ࡯ࡧࡸ࠰࡯ࡲࡺ࡮࡫࡟ࡴࡱࡸࡶࡨ࡫ࡳ࠰ࠧࡶࠫॽ") %(l11l111Created_By_Mucky_Duck,l1l1lll1Created_By_Mucky_Duck)
                headers = {l11lCreated_By_Mucky_Duck (u"ࠨࡃࡦࡧࡪࡶࡴࠨॾ"):l11lCreated_By_Mucky_Duck (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲ࠱ࠦࡴࡦࡺࡷ࠳࡯ࡧࡶࡢࡵࡦࡶ࡮ࡶࡴ࠭ࠢ࠭࠳࠯ࡁࠠࡲ࠿࠳࠲࠵࠷ࠧॿ"),
                           l11lCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡉࡳࡩ࡯ࡥ࡫ࡱ࡫ࠬঀ"):l11lCreated_By_Mucky_Duck (u"ࠫ࡬ࢀࡩࡱ࠮ࠣࡨࡪ࡬࡬ࡢࡶࡨ࠰ࠥࡹࡤࡤࡪ࠯ࠤࡧࡸࠧঁ"), l11lCreated_By_Mucky_Duck (u"ࠬࡇࡣࡤࡧࡳࡸ࠲ࡒࡡ࡯ࡩࡸࡥ࡬࡫ࠧং"):l11lCreated_By_Mucky_Duck (u"࠭ࡥ࡯࠯ࡘࡗ࠱࡫࡮࠼ࡳࡀ࠴࠳࠾ࠧঃ"),
                           l11lCreated_By_Mucky_Duck (u"ࠧࡓࡧࡩࡩࡷ࡫ࡲࠨ঄"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬঅ"):md.User_Agent(), l11lCreated_By_Mucky_Duck (u"࡛ࠩ࠱ࡗ࡫ࡱࡶࡧࡶࡸࡪࡪ࠭ࡘ࡫ࡷ࡬ࠬআ"):l11lCreated_By_Mucky_Duck (u"ࠪ࡜ࡒࡒࡈࡵࡶࡳࡖࡪࡷࡵࡦࡵࡷࠫই")}
                final = open_url(l1ll111Created_By_Mucky_Duck, params=params, headers=headers, verify=False).json()
                l1lllllCreated_By_Mucky_Duck = []
                l1ll1l1Created_By_Mucky_Duck = []
                l1l11l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠫࠬঈ")
                if l1l1l11Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡲࡶࡧࠪউ"):
                        url = max(final[l11lCreated_By_Mucky_Duck (u"࠭ࡰ࡭ࡣࡼࡰ࡮ࡹࡴࠨঊ")][0][l11lCreated_By_Mucky_Duck (u"ࠧࡴࡱࡸࡶࡨ࡫ࡳࠨঋ")], key=lambda l1l1llllCreated_By_Mucky_Duck: int(re.sub(l11lCreated_By_Mucky_Duck (u"ࠨ࡞ࡇࠫঌ"), l11lCreated_By_Mucky_Duck (u"ࠩࠪ঍"), l1l1llllCreated_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠪࡰࡦࡨࡥ࡭ࠩ঎")])))
                        url = url[l11lCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࠩএ")]
                else:
                        match = final[l11lCreated_By_Mucky_Duck (u"ࠬࡶ࡬ࡢࡻ࡯࡭ࡸࡺࠧঐ")][0][l11lCreated_By_Mucky_Duck (u"࠭ࡳࡰࡷࡵࡧࡪࡹࠧ঑")]
                        for a in match:
                                l1l11l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨ঒") %a[l11lCreated_By_Mucky_Duck (u"ࠨ࡮ࡤࡦࡪࡲࠧও")]
                                l1lllllCreated_By_Mucky_Duck.append(l1l11l1Created_By_Mucky_Duck)
                                l1ll1l1Created_By_Mucky_Duck.append(a[l11lCreated_By_Mucky_Duck (u"ࠩࡩ࡭ࡱ࡫ࠧঔ")])
                        if len(match) >1:
                                l111l1Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠪࡗࡪࡲࡥࡤࡶࠣࡗࡹࡸࡥࡢ࡯ࠣࡕࡺࡧ࡬ࡪࡶࡼࠫক"),l1lllllCreated_By_Mucky_Duck)
                                if l111l1Created_By_Mucky_Duck == -1:
                                        return
                                elif l111l1Created_By_Mucky_Duck > -1:
                                        url = l1ll1l1Created_By_Mucky_Duck[l111l1Created_By_Mucky_Duck]
                        else:
                                url = final[l11lCreated_By_Mucky_Duck (u"ࠫࡵࡲࡡࡺ࡮࡬ࡷࡹ࠭খ")][0][l11lCreated_By_Mucky_Duck (u"ࠬࡹ࡯ࡶࡴࡦࡩࡸ࠭গ")][0][l11lCreated_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࠫঘ")]
        except:
                if content == l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡹ࡭ࡪࡹࠧঙ"):
                        link = open_url(url,verify=False).content
                        l111l1lCreated_By_Mucky_Duck = url
                        headers = {l11lCreated_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬচ"):md.User_Agent()}
                        link = open_url(url, headers=headers).content
                        l11l1llCreated_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠩ࡬ࡨ࠿ࠦࠢࠩ࡝ࡡࠦࡢ࠱ࠩࠣࠩছ")).findall(link)[0]
                        request_url = l11lCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡲࡵࡶࡪࡧࡢࡩࡵ࡯ࡳࡰࡦࡨࡷ࠴ࠫࡳࠨজ") %(l11l111Created_By_Mucky_Duck,l11l1llCreated_By_Mucky_Duck)
                        headers = {l11lCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡊࡴࡣࡰࡦ࡬ࡲ࡬࠭ঝ"):l11lCreated_By_Mucky_Duck (u"ࠬ࡭ࡺࡪࡲ࠯ࠤࡩ࡫ࡦ࡭ࡣࡷࡩ࠱ࠦࡳࡥࡥ࡫࠰ࠥࡨࡲࠨঞ"), l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦࡨࡨࡶࡪࡸࠧট"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫঠ"):md.User_Agent()}
                        l1ll1111Created_By_Mucky_Duck = open_url(request_url, headers=headers, verify=False).json()
                        l1l1lll1Created_By_Mucky_Duck = re.compile(l11lCreated_By_Mucky_Duck (u"ࠨࡦࡤࡸࡦ࠳ࡩࡥ࠿ࠥࠬࡠࡤࠢ࡞࠭ࠬࠦࠬড")).findall(l1ll1111Created_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠩ࡫ࡸࡲࡲࠧঢ")])[3]
                else:
                        l1ll11llCreated_By_Mucky_Duck = re.split(l11lCreated_By_Mucky_Duck (u"ࡵࠫࡡࢂࠧণ"), str(query), re.I)
                        l111l1lCreated_By_Mucky_Duck = l1ll11llCreated_By_Mucky_Duck[0].replace(l11lCreated_By_Mucky_Duck (u"ࠫࡡࡢࠧত"),l11lCreated_By_Mucky_Duck (u"ࠬ࠭থ"))
                        l1l1lll1Created_By_Mucky_Duck = l1ll11llCreated_By_Mucky_Duck[1].replace(l11lCreated_By_Mucky_Duck (u"࠭࡜࡝ࠩদ"),l11lCreated_By_Mucky_Duck (u"ࠧࠨধ"))
                        l11l1llCreated_By_Mucky_Duck = l1ll11llCreated_By_Mucky_Duck[2].replace(l11lCreated_By_Mucky_Duck (u"ࠨ࡞࡟ࠫন"),l11lCreated_By_Mucky_Duck (u"ࠩࠪ঩"))
                l1ll1l11Created_By_Mucky_Duck = int(time.time() * 10000)
                l1lll1lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪࠩࡸ࠵ࡡ࡫ࡣࡻ࠳ࡲࡵࡶࡪࡧࡢࡸࡴࡱࡥ࡯ࠩপ") %l11l111Created_By_Mucky_Duck
                params = {l11lCreated_By_Mucky_Duck (u"ࠫࡪ࡯ࡤࠨফ"):l1l1lll1Created_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠬࡳࡩࡥࠩব"):l11l1llCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"࠭࡟ࠨভ"):l1ll1l11Created_By_Mucky_Duck}
                headers = {l11lCreated_By_Mucky_Duck (u"ࠧࡂࡥࡦࡩࡵࡺࠧম"):l11lCreated_By_Mucky_Duck (u"ࠨࡶࡨࡼࡹ࠵ࡪࡢࡸࡤࡷࡨࡸࡩࡱࡶ࠯ࠤࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡥࡻࡧࡳࡤࡴ࡬ࡴࡹ࠲ࠠࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴࡫ࡣ࡮ࡣࡶࡧࡷ࡯ࡰࡵ࠮ࠣࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰ࡩࡨࡳࡡࡴࡥࡵ࡭ࡵࡺࠬࠡࠬ࠲࠮ࡀࠦࡱ࠾࠲࠱࠴࠶࠭য"),
                           l11lCreated_By_Mucky_Duck (u"ࠩࡄࡧࡨ࡫ࡰࡵ࠯ࡈࡲࡨࡵࡤࡪࡰࡪࠫর"):l11lCreated_By_Mucky_Duck (u"ࠪ࡫ࡿ࡯ࡰ࠭ࠢࡧࡩ࡫ࡲࡡࡵࡧ࠯ࠤࡸࡪࡣࡩ࠮ࠣࡦࡷ࠭঱"), l11lCreated_By_Mucky_Duck (u"ࠫࡆࡩࡣࡦࡲࡷ࠱ࡑࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ল"):l11lCreated_By_Mucky_Duck (u"ࠬ࡫࡮࠮ࡗࡖ࠰ࡪࡴ࠻ࡲ࠿࠳࠲࠽࠭঳"),
                           l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦࡨࡨࡶࡪࡸࠧ঴"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫ঵"):md.User_Agent(), l11lCreated_By_Mucky_Duck (u"ࠨ࡚࠰ࡖࡪࡷࡵࡦࡵࡷࡩࡩ࠳ࡗࡪࡶ࡫ࠫশ"):l11lCreated_By_Mucky_Duck (u"࡛ࠩࡑࡑࡎࡴࡵࡲࡕࡩࡶࡻࡥࡴࡶࠪষ")}
                data = open_url(l1lll1lCreated_By_Mucky_Duck, params=params, headers=headers, verify=False).content
                if l11lCreated_By_Mucky_Duck (u"ࠪࠨࡤࠪࠧস") in data:
                    params = __1l1l1llCreated_By_Mucky_Duck(data)
                elif data.startswith(l11lCreated_By_Mucky_Duck (u"ࠫࡠࡣࠧহ")) and data.endswith(l11lCreated_By_Mucky_Duck (u"ࠬ࠮ࠩࠨ঺")):
                    params = __1l1ll11Created_By_Mucky_Duck(data)
                else:
                    params = __1l1ll1lCreated_By_Mucky_Duck(data)
                if params is None:
                    l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"࠭ࡕ࡯ࡴࡨࡧࡴ࡭࡮ࡪࡼࡨࡨࠥࡰࡳࠡ࡫ࡱࠤࠪࡹࠧ঻") % (l1lll1lCreated_By_Mucky_Duck))
                l1ll111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࠦࡵ࠲ࡥ࡯ࡧࡸ࠰࡯ࡲࡺ࡮࡫࡟ࡴࡱࡸࡶࡨ࡫ࡳ࠰ࠧࡶ়ࠫ") %(l11l111Created_By_Mucky_Duck,l1l1lll1Created_By_Mucky_Duck)
                headers = {l11lCreated_By_Mucky_Duck (u"ࠨࡃࡦࡧࡪࡶࡴࠨঽ"):l11lCreated_By_Mucky_Duck (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲ࠱ࠦࡴࡦࡺࡷ࠳࡯ࡧࡶࡢࡵࡦࡶ࡮ࡶࡴ࠭ࠢ࠭࠳࠯ࡁࠠࡲ࠿࠳࠲࠵࠷ࠧা"),
                           l11lCreated_By_Mucky_Duck (u"ࠪࡅࡨࡩࡥࡱࡶ࠰ࡉࡳࡩ࡯ࡥ࡫ࡱ࡫ࠬি"):l11lCreated_By_Mucky_Duck (u"ࠫ࡬ࢀࡩࡱ࠮ࠣࡨࡪ࡬࡬ࡢࡶࡨ࠰ࠥࡹࡤࡤࡪ࠯ࠤࡧࡸࠧী"), l11lCreated_By_Mucky_Duck (u"ࠬࡇࡣࡤࡧࡳࡸ࠲ࡒࡡ࡯ࡩࡸࡥ࡬࡫ࠧু"):l11lCreated_By_Mucky_Duck (u"࠭ࡥ࡯࠯ࡘࡗ࠱࡫࡮࠼ࡳࡀ࠴࠳࠾ࠧূ"),
                           l11lCreated_By_Mucky_Duck (u"ࠧࡓࡧࡩࡩࡷ࡫ࡲࠨৃ"):l111l1lCreated_By_Mucky_Duck, l11lCreated_By_Mucky_Duck (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬৄ"):md.User_Agent(), l11lCreated_By_Mucky_Duck (u"࡛ࠩ࠱ࡗ࡫ࡱࡶࡧࡶࡸࡪࡪ࠭ࡘ࡫ࡷ࡬ࠬ৅"):l11lCreated_By_Mucky_Duck (u"ࠪ࡜ࡒࡒࡈࡵࡶࡳࡖࡪࡷࡵࡦࡵࡷࠫ৆")}
                final = open_url(l1ll111Created_By_Mucky_Duck, params=params, headers=headers, verify=False).json()
                l1lllllCreated_By_Mucky_Duck = []
                l1ll1l1Created_By_Mucky_Duck = []
                l1l11l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠫࠬে")
                if l1l1l11Created_By_Mucky_Duck == l11lCreated_By_Mucky_Duck (u"ࠬࡺࡲࡶࡧࠪৈ"):
                        url = max(final[l11lCreated_By_Mucky_Duck (u"࠭ࡰ࡭ࡣࡼࡰ࡮ࡹࡴࠨ৉")][0][l11lCreated_By_Mucky_Duck (u"ࠧࡴࡱࡸࡶࡨ࡫ࡳࠨ৊")], key=lambda l1l1llllCreated_By_Mucky_Duck: int(re.sub(l11lCreated_By_Mucky_Duck (u"ࠨ࡞ࡇࠫো"), l11lCreated_By_Mucky_Duck (u"ࠩࠪৌ"), l1l1llllCreated_By_Mucky_Duck[l11lCreated_By_Mucky_Duck (u"ࠪࡰࡦࡨࡥ࡭্ࠩ")])))
                        url = url[l11lCreated_By_Mucky_Duck (u"ࠫ࡫࡯࡬ࡦࠩৎ")]
                else:
                        match = final[l11lCreated_By_Mucky_Duck (u"ࠬࡶ࡬ࡢࡻ࡯࡭ࡸࡺࠧ৏")][0][l11lCreated_By_Mucky_Duck (u"࠭ࡳࡰࡷࡵࡧࡪࡹࠧ৐")]
                        for a in match:
                                l1l11l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡄࡠ࡟ࡎࡣ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࠩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡋࡠ࡟࠴ࡈ࡝ࠨ৑") %a[l11lCreated_By_Mucky_Duck (u"ࠨ࡮ࡤࡦࡪࡲࠧ৒")]
                                l1lllllCreated_By_Mucky_Duck.append(l1l11l1Created_By_Mucky_Duck)
                                l1ll1l1Created_By_Mucky_Duck.append(a[l11lCreated_By_Mucky_Duck (u"ࠩࡩ࡭ࡱ࡫ࠧ৓")])
                        if len(match) >1:
                                l111l1Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠪࡗࡪࡲࡥࡤࡶࠣࡗࡹࡸࡥࡢ࡯ࠣࡕࡺࡧ࡬ࡪࡶࡼࠫ৔"),l1lllllCreated_By_Mucky_Duck)
                                if l111l1Created_By_Mucky_Duck == -1:
                                        return
                                elif l111l1Created_By_Mucky_Duck > -1:
                                        url = l1ll1l1Created_By_Mucky_Duck[l111l1Created_By_Mucky_Duck]
                        else:
                                url = final[l11lCreated_By_Mucky_Duck (u"ࠫࡵࡲࡡࡺ࡮࡬ࡷࡹ࠭৕")][0][l11lCreated_By_Mucky_Duck (u"ࠬࡹ࡯ࡶࡴࡦࡩࡸ࠭৖")][0][l11lCreated_By_Mucky_Duck (u"࠭ࡦࡪ࡮ࡨࠫৗ")]
	md.resolved(url, name, fan_art, l1llllCreated_By_Mucky_Duck)
	l111Created_By_Mucky_Duck.end_of_directory()
def l1llll11Created_By_Mucky_Duck():
        l11llllCreated_By_Mucky_Duck = [l11lCreated_By_Mucky_Duck (u"ࠧࡳࡧࡳࡳࡸ࡯ࡴࡰࡴࡼ࠲ࡲࡧࡦࠨ৘"), l11lCreated_By_Mucky_Duck (u"ࠨࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡰࡥ࡫ࡽࡩࡻࡣࡵࡨࠬ৙"), l11lCreated_By_Mucky_Duck (u"ࠩࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯࡭ࡵࡥࡹࡵࡳࠨ৚"),
                    l11lCreated_By_Mucky_Duck (u"ࠪࡶࡪࡶ࡯ࡴ࡫ࡷࡳࡷࡿ࠮ࡢࡰࡲࡲࡾࡳ࡯ࡶࡵࡷࡶࡺࡺࡨࠨ৛"), l11lCreated_By_Mucky_Duck (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡵࡸ࡯ࡨࡴࡤࡱ࠳ࡧ࡮ࡰࡰࡼࡱࡴࡻࡳࡵࡴࡸࡸ࡭࠭ড়"),
                    l11lCreated_By_Mucky_Duck (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡰࡸࡡࡵࡱࡶࡪࡺࡩ࡫ࡴࡦࡸࡧࡰࡿࠧঢ়"), l11lCreated_By_Mucky_Duck (u"࠭ࡳࡤࡴ࡬ࡴࡹ࠴࡫ࡳࡣࡷࡳࡸ࡬ࡵࡤ࡭ࡶࡨࡺࡩ࡫ࡺ࠰ࡤࡶࡹࡽ࡯ࡳ࡭ࠪ৞"),
                    l11lCreated_By_Mucky_Duck (u"ࠧࡴࡥࡵ࡭ࡵࡺ࠮࡬ࡴࡤࡸࡴࡹࡦࡶࡥ࡮ࡷࡩࡻࡣ࡬ࡻ࠱ࡱࡪࡺࡡࡥࡣࡷࡥࠬয়"), l11lCreated_By_Mucky_Duck (u"ࠨࡵࡦࡶ࡮ࡶࡴ࠯࡯ࡲࡨࡺࡲࡥ࠯ࡩ࡬࡫࡬࡯ࡴࡺࠩৠ")]
        l1llll11Created_By_Mucky_Duck = any(xbmc.getCondVisibility(l11lCreated_By_Mucky_Duck (u"ࠩࡖࡽࡸࡺࡥ࡮࠰ࡋࡥࡸࡇࡤࡥࡱࡱࠬࠪࡹࠩࠨৡ") % (l111Created_By_Mucky_Duck)) for l111Created_By_Mucky_Duck in l11llllCreated_By_Mucky_Duck)
        if l1llll11Created_By_Mucky_Duck:
                l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪ࡝ࡴࡻࠠࡉࡣࡹࡩࠥࡏ࡮ࡴࡶࡤࡰࡱ࡫ࡤࠡࡃࡧࡨࡴࡴࡳࠨৢ")
                l1ll1l1lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࡙ࠫ࡮ࡡࡵࠢࡐࡹࡨࡱࡹࠡࡆࡸࡧࡰࠦࡄࡰࡧࡶࠤࡓࡵࡴࠨৣ")
                l1ll1ll1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࡙ࠬࡵࡱࡲࡲࡶࡹࠦࡁ࡯ࡦ࡛ࠣ࡮ࡲ࡬ࠡࡐࡲࡻࠥࡘࡥ࡮ࡱࡹࡩࠬ৤")
                l1ll1lllCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"࠭ࡒࡦ࡯ࡲࡺࡪࡪࠠࡂࡰࡲࡲࡾࡳ࡯ࡶࡵࠣࡖࡪࡶ࡯ࠡࡃࡱࡨࠥࡇࡤࡥࡱࡱࡷࠬ৥")
                l1lll111Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠧࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡐ࡭ࡧࡤࡷࡪࠦࡄࡰࡰࡷࠤࡘࡻࡰࡱࡱࡵࡸࠥࡏࡤࡪࡱࡷࡷࠬ০")
                l1lll11lCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠨࡔࡨࡱࡴࡼࡥࡥࠢࠨࡷࠬ১") %l1ll1Created_By_Mucky_Duck
                l1lll1l1Created_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠩࡘࡲ࡫ࡵࡲࡵࡷࡱࡥࡹ࡫࡬ࡺࠢ࡜ࡳࡺࠦࡓࡶࡲࡳࡳࡷࡺࠠࡊࡦ࡬ࡳࡹࡹࠧ২")
                l111Created_By_Mucky_Duck.show_ok_dialog([l1Created_By_Mucky_Duck, l1ll1l1lCreated_By_Mucky_Duck, l1ll1ll1Created_By_Mucky_Duck], l1ll1Created_By_Mucky_Duck)
                l1ll1llCreated_By_Mucky_Duck = l11lCreated_By_Mucky_Duck (u"ࠪ࡝ࡴࡻࡲࠡࡅ࡫ࡳ࡮ࡩࡥࠡࡇ࡬ࡸ࡭࡫ࡲࠡࡗࡱ࡭ࡳࡹࡴࡢ࡮࡯ࠤࠪࡹࠠࡐࡴ࡙ࠣࡳ࡯࡮ࡴࡶࡤࡰࡱࠦࡔࡩࡧࠣࡅࡳࡵ࡮ࡺ࡯ࡲࡹࡸࠦࡒࡦࡲࡲࠤ࠰ࠦࡁࡥࡦࡲࡲࡸ࠭৩") %l1ll1Created_By_Mucky_Duck
                if md.dialog_yesno(l1ll1llCreated_By_Mucky_Duck,l11lCreated_By_Mucky_Duck (u"ࠫࡆࡴ࡯࡯ࡻࡰࡳࡺࡹࠧ৪"),l1ll1Created_By_Mucky_Duck):
                        l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠬࡃ࠽࠾ࡆࡈࡐࡊ࡚ࡉࡏࡉࡀࡁࡂࡇࡎࡐࡐ࡜ࡑࡔ࡛ࡓ࠾࠿ࡀࡅࡉࡊࡏࡏࡕࡀࡁࡂ࠱࠽࠾࠿ࡕࡉࡕࡕ࠽࠾࠿ࠪ৫"))
                        for root, dirs, files in os.walk(xbmc.translatePath(l11lCreated_By_Mucky_Duck (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹࠧ৬"))):
                                dirs[:] = [d for d in dirs if d in l11llllCreated_By_Mucky_Duck]
                                for d in dirs:
                                        try:
                                                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
                                        except OSError:
                                                pass
                        l111Created_By_Mucky_Duck.show_ok_dialog([l1ll1lllCreated_By_Mucky_Duck, l1lll111Created_By_Mucky_Duck], l1ll1Created_By_Mucky_Duck)
                else:
                        l111Created_By_Mucky_Duck.log(l11lCreated_By_Mucky_Duck (u"ࠧ࠾࠿ࡀࡈࡊࡒࡅࡕࡋࡑࡋࡂࡃ࠽ࠦࡵࡀࡁࡂ࠭৭") %l1ll1Created_By_Mucky_Duck)
                        llCreated_By_Mucky_Duck = l111Created_By_Mucky_Duck.get_path()
			shutil.rmtree(llCreated_By_Mucky_Duck, ignore_errors=True)
			l111Created_By_Mucky_Duck.show_ok_dialog([l1lll11lCreated_By_Mucky_Duck, l1lll1l1Created_By_Mucky_Duck], l1ll1Created_By_Mucky_Duck)
                time.sleep(2)
                os._exit(0)
def l1l11ll1Created_By_Mucky_Duck(url):
	l1l1l1l1Created_By_Mucky_Duck = []
	l1lllCreated_By_Mucky_Duck = []
	link = open_url(url).content
	l1l1lCreated_By_Mucky_Duck = md.regex_get_all(link, l11lCreated_By_Mucky_Duck (u"ࠨࡲ࡯࠱࡮ࡺࡥ࡮ࠩ৮"), l11lCreated_By_Mucky_Duck (u"ࠩ࠿࠳ࡹࡸ࠾ࠨ৯"))
	for a in l1l1lCreated_By_Mucky_Duck:
		name = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠪࡸ࡮ࡺ࡬ࡦ࠿ࠥࠫৰ"), l11lCreated_By_Mucky_Duck (u"ࠫࠧ࠭ৱ"))
		url = md.regex_from_to(a, l11lCreated_By_Mucky_Duck (u"ࠬ࡮ࡲࡦࡨࡀࠦࠬ৲"), l11lCreated_By_Mucky_Duck (u"࠭ࠢࠨ৳"))
		l1l1l1l1Created_By_Mucky_Duck.append(l11lCreated_By_Mucky_Duck (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࠨࡷࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ৴") %name)
		l1lllCreated_By_Mucky_Duck.append(url)
	if len(l1l1lCreated_By_Mucky_Duck) >1:
		l111l1Created_By_Mucky_Duck = md.dialog_select(l11lCreated_By_Mucky_Duck (u"ࠨࡕࡨࡰࡪࡩࡴࠡࡒࡵࡳࡽࡿࠠࡂࡦࡧࡶࡪࡹࡳࠨ৵"), l1l1l1l1Created_By_Mucky_Duck)
		if l111l1Created_By_Mucky_Duck == -1:
			return
		elif l111l1Created_By_Mucky_Duck > -1:
			url = l1lllCreated_By_Mucky_Duck[l111l1Created_By_Mucky_Duck]
		else:
			url = l1lllCreated_By_Mucky_Duck[0]
	headers = open_url(url, redirects=False).headers
	if l11lCreated_By_Mucky_Duck (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫ৶") in headers:
		url = headers[l11lCreated_By_Mucky_Duck (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ৷")]
	if url[-1] == l11lCreated_By_Mucky_Duck (u"ࠫ࠴࠭৸"):
		url = url[:-1]
	l111Created_By_Mucky_Duck.set_setting(l11lCreated_By_Mucky_Duck (u"ࠬࡨࡡࡴࡧࡢࡹࡷࡲࠧ৹"), url)
	md.notification(l11lCreated_By_Mucky_Duck (u"࠭ࡵࡳ࡮ࠣࡥࡩࡪࡥࡥࠢࡷࡳࠥࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠭৺"),l1l1l11lCreated_By_Mucky_Duck)
	return
md.check_source()
mode = md.args[l11lCreated_By_Mucky_Duck (u"ࠧ࡮ࡱࡧࡩࠬ৻")]
url = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠨࡷࡵࡰࠬৼ"), None)
name = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠩࡱࡥࡲ࡫ࠧ৽"), None)
query = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠪࡵࡺ࡫ࡲࡺࠩ৾"), None)
title = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠫࡹ࡯ࡴ࡭ࡧࠪ৿"), None)
l11l11lCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠬࡹࡥࡢࡵࡲࡲࠬ਀"), None)
l1l1l111Created_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"࠭ࡥࡱ࡫ࡶࡳࡩ࡫ࠧਁ") ,None)
l1llllCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠧࡪࡰࡩࡳࡱࡧࡢࡦ࡮ࡶࠫਂ"), None)
content = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠨࡥࡲࡲࡹ࡫࡮ࡵࠩਃ"), None)
l1ll11lCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠩࡰࡳࡩ࡫࡟ࡪࡦࠪ਄"), None)
l111llCreated_By_Mucky_Duck = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠪ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪ࠭ਅ"), None)
fan_art = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠫ࡫ࡧ࡮ࡠࡣࡵࡸࠬਆ"), None)
is_folder = md.args.get(l11lCreated_By_Mucky_Duck (u"ࠬ࡯ࡳࡠࡨࡲࡰࡩ࡫ࡲࠨਇ"), True)
if mode is None or url is None or len(url)<1:
	l1ll11Created_By_Mucky_Duck()
elif mode == l11lCreated_By_Mucky_Duck (u"࠭࠱ࠨਈ"):
	l1l11l11Created_By_Mucky_Duck(content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠧ࠳ࠩਉ"):
	l1l1l1Created_By_Mucky_Duck(url,content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠨ࠵ࠪਊ"):
	l1111l1Created_By_Mucky_Duck(title, url, l111llCreated_By_Mucky_Duck, content, l11l11lCreated_By_Mucky_Duck)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠩ࠷ࠫ਋"):
	l1l111llCreated_By_Mucky_Duck(url, content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠪ࠹ࠬ਌"):
	l11l1Created_By_Mucky_Duck(url, content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠫ࠻࠭਍"):
	l1l111Created_By_Mucky_Duck(url, content)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠬ࠽ࠧ਎"):
	l1lll1Created_By_Mucky_Duck(url,name,l111llCreated_By_Mucky_Duck,content,l1llllCreated_By_Mucky_Duck,query)
elif mode == l11lCreated_By_Mucky_Duck (u"࠭ࡳࡦࡣࡵࡧ࡭࠭ਏ"):
	l11l1lCreated_By_Mucky_Duck(content,query)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠧࡢࡦࡧࡳࡳࡥࡳࡦࡣࡵࡧ࡭࠭ਐ"):
	md.addon_search(content,query,fan_art,l1llllCreated_By_Mucky_Duck)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠨࡩࡨࡸࡤࡶࡲࡰࡺࡼࠫ਑"):
	l1l11ll1Created_By_Mucky_Duck(url)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠩࡤࡨࡩࡥࡲࡦ࡯ࡲࡺࡪࡥࡦࡢࡸࠪ਒"):
	md.add_remove_fav(name, url, l1llllCreated_By_Mucky_Duck, fan_art,
			  content, l1ll11lCreated_By_Mucky_Duck, is_folder)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠪࡪࡪࡺࡣࡩࡡࡩࡥࡻࡹࠧਓ"):
	md.fetch_favs(l11l111Created_By_Mucky_Duck)
elif mode == l11lCreated_By_Mucky_Duck (u"ࠫࡦࡪࡤࡰࡰࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬਔ"):
	l111Created_By_Mucky_Duck.show_settings()
elif mode == l11lCreated_By_Mucky_Duck (u"ࠬࡳࡥࡵࡣࡢࡷࡪࡺࡴࡪࡰࡪࡷࠬਕ"):
	import metahandler
	metahandler.display_settings()
l111Created_By_Mucky_Duck.end_of_directory()