# -*- coding: utf-8 -*-
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
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,urlresolver,random,liveresolver,base64,pyxbmct,glob,net,json
from resources.lib.common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources.lib import scraper1
from resources.lib import scraper2
from resources.lib import scraper3
from resources.lib import l111111UK_Turk_No1
from resources.lib import l1111UK_Turk_No1
from resources.lib import l11lll1lUK_Turk_No1
from resources.lib import l11l1111UK_Turk_No1
from resources.lib import l1l11l11lUK_Turk_No1
from resources.lib import l1111llllUK_Turk_No1
from resources.lib import l11ll1lUK_Turk_No1
from resources.lib import l1l1l11l1UK_Turk_No1
from resources.lib import l1l1111UK_Turk_No1
from resources.lib import l1l1111l1UK_Turk_No1
from resources.lib import l1l1lll11UK_Turk_No1
from resources.lib import wizard as l1l1l111UK_Turk_No1, downloader as l1l11lUK_Turk_No1, notify
import time;import ntpath;
import shutil;import zipfile;import hashlib;
import platform;
import subprocess
import xbmcvfs
import atexit
import cookielib
import uuid
import plugintools
import webbrowser as l1ll11l1UK_Turk_No1
from uuid import getnode as l11ll1UK_Turk_No1
mac = l11ll1UK_Turk_No1()
l11l1l1llUK_Turk_No1   = xbmcaddon.Addon(l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡻ࡯ࡤࡦࡱ࠱ࡹࡰࡺࡵࡳ࡭ࠪࠀ"))
addon_id        = l11l1lUK_Turk_No1 (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡺࡱࡴࡶࡴ࡮ࠫࠁ")
DP              = xbmcgui.DialogProgress()
addon           = Addon(addon_id, sys.argv)
l1l1111lUK_Turk_No1       = xbmcaddon.Addon(id=addon_id)
l11l11l1lUK_Turk_No1        = xbmc.translatePath(l1l1111lUK_Turk_No1.getAddonInfo(l11l1lUK_Turk_No1 (u"࠭ࡰࡳࡱࡩ࡭ࡱ࡫ࠧࠂ")))
DIALOG          = xbmcgui.Dialog()
l11l11111UK_Turk_No1      = xbmc.translatePath(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࠩࠃ"))+l11l1lUK_Turk_No1 (u"ࠨ࠱࠭࠲࠯࠭ࠄ")
l1l11l1UK_Turk_No1    = xbmc.translatePath(l11l1lUK_Turk_No1 (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࡥࡩࡪ࡯࡯ࡵ࠲ࠫࠅ"))
fanart          = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠪࡷࡵ࡫ࡣࡪࡣ࡯࠾࠴࠵ࡨࡰ࡯ࡨ࠳ࡦࡪࡤࡰࡰࡶ࠳ࠬࠆ") + addon_id, l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷ࠲࡯ࡶࡧࠨࠇ")))
l1l11111lUK_Turk_No1         = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࠧࠈ") + addon_id, l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡰࡤࡶࡹ࠴ࡪࡱࡩࠪࠉ")))
icon            = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࠩࠊ") + addon_id, l11l1lUK_Turk_No1 (u"ࠨ࡫ࡦࡳࡳ࠴ࡰ࡯ࡩࠪࠋ")))
HOME            = xbmc.translatePath(l11l1lUK_Turk_No1 (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࠫࠌ"))
ADDONS          = os.path.join(HOME,      l11l1lUK_Turk_No1 (u"ࠪࡥࡩࡪ࡯࡯ࡵࠪࠍ"))
PACKAGES        = os.path.join(ADDONS,    l11l1lUK_Turk_No1 (u"ࠫࡵࡧࡣ࡬ࡣࡪࡩࡸ࠭ࠎ"))
l11ll11llUK_Turk_No1        = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࠧࠏ") + addon_id, l11l1lUK_Turk_No1 (u"࠭࡮ࡦࡺࡷ࠲ࡵࡴࡧࠨࠐ")))
l11111lUK_Turk_No1        = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠧࡢࡦࡸࡰࡹ࠭ࠑ"))
l111l1l11UK_Turk_No1       = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪࠒ"))
l11111lUK_Turk_No1        = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡤࡨࡺࡲࡴࠨࠓ"))
l1ll1l1UK_Turk_No1         = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠪࡴ࡮ࡴࠧࠔ"))
count           = int(l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫࡨࡵࡵ࡯ࡶࠪࠕ")))
l1111l1l1UK_Turk_No1         = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠖ"))
l1lll1UK_Turk_No1        = xbmc.translatePath(l11l1lUK_Turk_No1 (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡶࡵࡨࡶࡩࡧࡴࡢ࠱ࡤࡨࡩࡵ࡮ࡠࡦࡤࡸࡦ࠵ࠧࠗ") + addon_id)
l1ll1ll11UK_Turk_No1         = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡷࡶࡩࡷࡪࡡࡵࡣ࠲ࡈࡦࡺࡡࡣࡣࡶࡩࠬ࠘"), l11l1lUK_Turk_No1 (u"ࠨࡗࡎࡘࡺࡸ࡫࠯ࡦࡥࠫ࠙")))
l1ll1l11lUK_Turk_No1      = l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡩࡪ࡯࡯ࡥ࡯ࡳࡺࡪ࠮ࡰࡴࡪ࠳ࡺࡱࡴࡶࡴ࡮࠳࡚ࡑࡔࡶࡴ࡮࠳ࡺࡱࡴࡶࡴ࡮࠽࠵࠸࠱࠱࠰࡭ࡴ࡬࠭ࠚ")
l1lll111UK_Turk_No1 =l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡩࡲࡳ࡬ࡲࡥࡢࡲ࡬ࡷ࠳ࡩ࡯࡮࠱ࡼࡳࡺࡺࡵࡣࡧ࠲ࡺ࠸࠵ࡳࡦࡣࡵࡧ࡭ࡅࡱ࠾ࠩࠛ")
l1111lll1UK_Turk_No1 =l11l1lUK_Turk_No1 (u"ࠫࠫࡸࡥࡨ࡫ࡲࡲࡈࡵࡤࡦ࠿ࡘࡗࠫࡶࡡࡳࡶࡀࡷࡳ࡯ࡰࡱࡧࡷࠪ࡭ࡲ࠽ࡦࡰࡢ࡙ࡘࠬ࡫ࡦࡻࡀࡅࡎࢀࡡࡔࡻࡅ࡫࡝࡬ࡄ࠱ࡉࡻ࡭ࡸࡰࡖࡩ࡯࡙࠶࡯࠶ࡪࡣࡆ࡚ࡍ࡝ࡑࡷࡰ࠶ࡄࡧ࠽ࡽࡷࠧࡶࡼࡴࡪࡃࡶࡪࡦࡨࡳࠫࡳࡡࡹࡔࡨࡷࡺࡲࡴࡴ࠿࠸࠴ࠬࠜ")
l1111l1llUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡵࡧ࡭ࡧࡤࡴ࡮ࡹ࠮ࡤࡱࡰ࠳ࡾࡵࡵࡵࡷࡥࡩ࠴ࡼ࠳࠰ࡲ࡯ࡥࡾࡲࡩࡴࡶࡌࡸࡪࡳࡳࡀࡲࡤࡶࡹࡃࡳ࡯࡫ࡳࡴࡪࡺࠦࡱ࡮ࡤࡽࡱ࡯ࡳࡵࡋࡧࡁࠬࠝ")
l111l11UK_Turk_No1 = l11l1lUK_Turk_No1 (u"࠭ࠦ࡮ࡣࡻࡖࡪࡹࡵ࡭ࡶࡶࡁ࠺࠶ࠦ࡬ࡧࡼࡁࡆࡏࡺࡢࡕࡼࡆ࡬࡞ࡦࡅ࠲ࡊࡼ࡮ࡹࡪࡗࡪࡰ࡚࠷ࡰ࠰࡫ࡤࡇ࡛ࡎ࡞ࡋࡸࡱ࠷ࡅࡨ࠾ࡷࡸࠩࠞ")
l1l1lll1UK_Turk_No1 = open(l1ll1ll11UK_Turk_No1,l11l1lUK_Turk_No1 (u"ࠧࡢࠩࠟ"))
l1l1lll1UK_Turk_No1.close()
net = net.Net()
l1111ll1lUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡨࡩࡵ࡮ࡤ࡮ࡲࡹࡩ࠴࡯ࡳࡩ࠲ࡻ࡮ࢀࡡࡳࡦ࠱ࡴ࡭ࡶࠧࠠ")
USER_AGENT   = l11l1lUK_Turk_No1 (u"ࠩࡐࡳࡿ࡯࡬࡭ࡣ࠲࠹࠳࠶࡙ࠠࠩ࡬ࡲࡩࡵࡷࡴࠢࡑࡘࠥ࠷࠰࠯࠲࠾ࠤ࡜ࡕࡗ࠷࠶ࠬࠤࡆࡶࡰ࡭ࡧ࡚ࡩࡧࡑࡩࡵ࠱࠸࠷࠼࠴࠳࠷ࠢࠫࡏࡍ࡚ࡍࡍ࠮ࠣࡰ࡮ࡱࡥࠡࡉࡨࡧࡰࡵࠩࠡࡅ࡫ࡶࡴࡳࡥ࠰࠶࠺࠲࠵࠴࠲࠶࠴࠹࠲࠼࠹ࠠࡔࡣࡩࡥࡷ࡯࠯࠶࠵࠺࠲࠸࠼ࠠࡓࡧࡳࡰ࡮ࡩࡡ࡯ࡶ࡚࡭ࡿࡧࡲࡥ࠱࠴࠲࠵࠴࠰ࠨࠡ")
l1lllllllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"࡙ࠥࡐ࡚ࡵࡳ࡭ࡶࠦࠢ")
P = plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠫࡵ࡯࡮ࠨࠣ"))
M = plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠬࡹࡵࡣ࡯ࡨࡷࡸࡧࡧࡦࠩࠤ"))
def l11ll1lllUK_Turk_No1():
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡸࠪࠥ"),l11l1lUK_Turk_No1 (u"ࠧ࡯ࡱࠪࠦ"))
        if not os.path.exists(l1lll1UK_Turk_No1):
                os.mkdir(l1lll1UK_Turk_No1)
        link=l1llll111UK_Turk_No1(l1ll1l11lUK_Turk_No1)
	l1l1l1l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾࡬ࡲࡩ࡫ࡸ࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡱࡨࡪࡾ࠾ࠨࠧ")).findall(link)[0]
	link=l1llll111UK_Turk_No1(l1l1l1l11UK_Turk_No1)
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠩࡱࡥࡲ࡫࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠯࠭ࡂࡶࡱࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠮ࠬࡁࡰ࡫ࡂࠨࠨ࠯࠭ࡂ࠭ࠧ࠭ࠨ"),re.DOTALL).findall(link)
	for name,url,l1l11l11UK_Turk_No1 in match:
		if not l11l1lUK_Turk_No1 (u"ࠪ࡜࡝࡞ࠧࠩ") in name:
			l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
		if l11l1lUK_Turk_No1 (u"ࠫ࡝࡞ࡘࠨࠪ") in name:
			if l11111lUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠬࡺࡲࡶࡧࠪࠫ"):
				if l111l1l11UK_Turk_No1 == l11l1lUK_Turk_No1 (u"࠭ࠧࠬ"):
				    dialog = xbmcgui.Dialog()
				    ret = dialog.yesno(l11l1lUK_Turk_No1 (u"ࠧࡂࡦࡸࡰࡹࠦࡃࡰࡰࡷࡩࡳࡺࠧ࠭"), l11l1lUK_Turk_No1 (u"ࠨ࡛ࡲࡹࠥ࡮ࡡࡷࡧࠣࡳࡵࡺࡥࡥࠢࡷࡳࠥࡹࡨࡰࡹࠣࡥࡩࡻ࡬ࡵࠢࡦࡳࡳࡺࡥ࡯ࡶࠪ࠮"),l11l1lUK_Turk_No1 (u"ࠩࠪ࠯"),l11l1lUK_Turk_No1 (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡷࡪࡺࠠࡢࠢࡳࡥࡸࡹࡷࡰࡴࡧࠤࡹࡵࠠࡱࡴࡨࡺࡪࡴࡴࠡࡣࡦࡧ࡮ࡪࡥ࡯ࡶࡤࡰࠥࡧࡣࡤࡧࡶࡷࠬ࠰"),l11l1lUK_Turk_No1 (u"ࠫࡈࡧ࡮ࡤࡧ࡯ࠫ࠱"),l11l1lUK_Turk_No1 (u"ࠬࡒࡥࡵࡵࠣࡋࡴ࠭࠲"))
				    if ret == 1:
					l1lll111lUK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"࠭ࠧ࠳"), l11l1lUK_Turk_No1 (u"ࠧࡔࡧࡷࠤࡕࡧࡳࡴࡹࡲࡶࡩ࠭࠴"))
					l1lll111lUK_Turk_No1.doModal()
					if (l1lll111lUK_Turk_No1.isConfirmed()):
					    l1l1UK_Turk_No1 = l1lll111lUK_Turk_No1.getText()
					    l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ࠵"),l1l1UK_Turk_No1)
					l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
			if l11111lUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠩࡷࡶࡺ࡫ࠧ࠶"):
				if l111l1l11UK_Turk_No1 <> l11l1lUK_Turk_No1 (u"ࠪࠫ࠷"):
					l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
	l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳࠨ࠸"),l1ll1ll11UK_Turk_No1,15,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡧࡤࡥࡱࡱࡧࡱࡵࡵࡥ࠰ࡲࡶ࡬࠵ࡵ࡬ࡶࡸࡶࡰ࠵ࡕࡌࡖࡸࡶࡰ࠵ࡴࡩࡷࡰࡦࡸ࠵࡮ࡦࡹ࠲࡙ࡰࠫ࠲࠱ࡶࡸࡶࡰࠫ࠲࠱ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡷࠪ࠸࠰ࡧࡣࡹࡳࡺࡸࡩࡵࡧࡶ࠲࡯ࡶࡧࠨ࠹"),fanart)
	l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࠭ࡓࡦࡣࡵࡧ࡭࠭࠺"),l11l1lUK_Turk_No1 (u"ࠧࡶࡴ࡯ࠫ࠻"),5,l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡣࡧࡨࡴࡴࡣ࡭ࡱࡸࡨ࠳ࡵࡲࡨ࠱ࡸ࡯ࡹࡻࡲ࡬࠱ࡘࡏ࡙ࡻࡲ࡬࠱ࡷ࡬ࡺࡳࡢࡴ࠱ࡱࡩࡼ࠵ࡕ࡬ࠧ࠵࠴ࡹࡻࡲ࡬ࠧ࠵࠴ࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲࡳࠦ࠴࠳ࡷࡪࡧࡲࡤࡪ࠱࡮ࡵ࡭ࠧ࠼"),fanart)
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨ࠽"))
	l1l1l111lUK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪࡱࡴࡼࡩࡦࡵࠪ࠾"), l11l1lUK_Turk_No1 (u"ࠫࡒࡇࡉࡏࠩ࠿"),link)
def l11l1l1l1UK_Turk_No1(url):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩࡀ"),l11l1lUK_Turk_No1 (u"࠭ࡹࡦࡵࠪࡁ"))
        l111111l1UK_Turk_No1 = None
	file = open(l1ll1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡳࠩࡂ"))
	l111111l1UK_Turk_No1 = file.read()
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠣ࠾࡬ࡸࡪࡳ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡪࡶࡨࡱࡃࠨࡃ"),re.DOTALL).findall(l111111l1UK_Turk_No1)
	for item in match:
                data=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡮ࡺ࡬ࡦࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡭ࡹࡲࡥ࠿࠰࠮ࡃࡱ࡯࡮࡬ࡀࠫ࠲࠰ࡅࠩ࠽࠱࡯࡭ࡳࡱ࠾࠯࠭ࡂࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪࡄ"),re.DOTALL).findall(item)
                for name,url,l1l11l11UK_Turk_No1 in data:
                        if l11l1lUK_Turk_No1 (u"ࠪ࠲ࡹࡾࡴࠨࡅ") in url:
                                l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
                        else:
                                l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
def l1111l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
	url=url.replace(l11l1lUK_Turk_No1 (u"ࠫࠥ࠭ࡆ"),l11l1lUK_Turk_No1 (u"ࠬࠫ࠲࠱ࠩࡇ"))
	l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"࠭ࠠࠨࡈ"),l11l1lUK_Turk_No1 (u"ࠧࠦ࠴࠳ࠫࡉ"))
	string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡉࡅ࡛ࡄ࠼ࡪࡶࡨࡱࡃࡢ࡮࠽ࡶ࡬ࡸࡱ࡫࠾ࠨࡊ")+name+l11l1lUK_Turk_No1 (u"ࠩ࠿࠳ࡹ࡯ࡴ࡭ࡧࡁࡠࡳࡂ࡬ࡪࡰ࡮ࡂࠬࡋ")+url+l11l1lUK_Turk_No1 (u"ࠪࡀ࠴ࡲࡩ࡯࡭ࡁࡠࡳ࠭ࡌ")+l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩࡍ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂ࠯ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࡠࡳࡂ࠯ࡪࡶࡨࡱࡃࡂ࠯ࡇࡃ࡙ࡂࡡࡴࠧࡎ")
	l1l1lll1UK_Turk_No1 = open(l1ll1ll11UK_Turk_No1,l11l1lUK_Turk_No1 (u"࠭ࡡࠨࡏ"))
	l1l1lll1UK_Turk_No1.write(string)
	l1l1lll1UK_Turk_No1.close()
def l11l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
	l111111l1UK_Turk_No1 = None
	file = open(l1ll1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡳࠩࡐ"))
	l111111l1UK_Turk_No1 = file.read()
	l11l1l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩࡑ")
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭ࡹ࡫࡭࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡷࡩࡲࡄࠧࡒ"),re.DOTALL).findall(l111111l1UK_Turk_No1)
	for data in match:
		string=l11l1lUK_Turk_No1 (u"ࠪࡠࡳࡂࡆࡂࡘࡁࡀ࡮ࡺࡥ࡮ࡀ࡟ࡲࠬࡓ")+data+l11l1lUK_Turk_No1 (u"ࠫࡁ࠵ࡩࡵࡧࡰࡂࡡࡴࠧࡔ")
		if name in data:
			string=string.replace(l11l1lUK_Turk_No1 (u"ࠬ࡯ࡴࡦ࡯ࠪࡕ"),l11l1lUK_Turk_No1 (u"࠭ࠠࠨࡖ"))
		l11l1l11UK_Turk_No1=l11l1l11UK_Turk_No1+string
	file = open(l1ll1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡸࠩࡗ"))
	file.truncate()
	file.write(l11l1l11UK_Turk_No1)
	file.close()
	xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡗ࡫ࡦࡳࡧࡶ࡬ࠬࡘ"))
def l1lll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1,fanart):
        l1l1l11lUK_Turk_No1=l1llllUK_Turk_No1(name)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠩࡷࡺ࡙ࠬ"),l1l1l11lUK_Turk_No1)
        link=l1llll111UK_Turk_No1(url)
        if l11l1lUK_Turk_No1 (u"ࠪ࠳࡚ࡑࡔࡶࡴ࡮࠳࡙ࡻࡲ࡬࡫ࡶ࡬࡙࡜࠮ࡵࡺࡷ࡚ࠫ") in url: l1l1ll111UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠫ࠴࡛ࡋࡕࡷࡵ࡯࠴࡚ࡵࡳ࡭࡬ࡷ࡭࡚ࡖ࠯ࡶࡻࡸ࡛ࠬ") in url: KD()
        if l11l1lUK_Turk_No1 (u"ࠬ࠵ࡕࡌࡖࡸࡶࡰ࠵ࡔࡶࡴ࡮࡭ࡸ࡮ࡔࡗ࠰ࡷࡼࡹ࠭࡜") in url: l1l11l1l1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"࠭࠯ࡖࡍࡗࡹࡷࡱ࠯ࡕࡷࡵ࡯࡮ࡹࡨࡕࡘ࠱ࡸࡽࡺࠧ࡝") in url: l11llll1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠧ࠰ࡗࡎࡘࡺࡸ࡫࠰ࡖࡸࡶࡰ࡯ࡳࡩࡖ࡙࠲ࡹࡾࡴࠨ࡞") in url: l1lll1ll1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠨ࠱ࡘࡏ࡙ࡻࡲ࡬࠱ࡷࡺࠪ࠸࠰ࡴࡪࡲࡻࡸ࠵ࡉ࡯ࡦࡨࡼ࠳ࡺࡸࡵࠩ࡟") in url: l1ll1l1llUK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠩ࠲࡙ࡐ࡚ࡵࡳ࡭࠲ࡸࡻࠫ࠲࠱ࡵ࡫ࡳࡼࡹ࠯ࡊࡰࡧࡩࡽ࠴ࡴࡹࡶࠪࡠ") in url: l11ll1111UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠪ࠳࡚ࡑࡔࡶࡴ࡮࠳ࡘࡶ࡯ࡳࡶࡶࡐ࡮ࡹࡴ࠯ࡶࡻࡸࠬࡡ") in url: l1lll1111UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠫ࠴࡛ࡋࡕࡷࡵ࡯࠴࡙ࡰࡰࡴࡷࡷࡑ࡯ࡳࡵ࠰ࡷࡼࡹ࠭ࡢ") in url: l1lllllll1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠬ࠵ࡕࡌࡖࡸࡶࡰ࠵࡭ࡰࡸ࡬ࡩࡸ࠵ࡉ࡯ࡦࡨࡼ࠳ࡺࡸࡵࠩࡣ") in url: l1l111111UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"࠭࠯ࡖࡍࡗࡹࡷࡱ࠯ࡤࡣࡵࡸࡴࡵ࡮ࡴ࠱ࡌࡲࡩ࡫ࡸ࠯ࡶࡻࡸࠬࡤ") in url: l1ll1111lUK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠧࡊࡰࡧࡩࡽ࠭ࡥ") in url:
                l1lllll1lUK_Turk_No1(url)
        if l11l1lUK_Turk_No1 (u"ࠨ࡚࡛࡜ࠬࡦ") in name: l1l1ll1UK_Turk_No1(link)
        match= re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭ࡹ࡫࡭࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡷࡩࡲࡄࠧࡧ"),re.DOTALL).findall(link)
        count=str(len(match))
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡧࡴࡻ࡮ࡵࠩࡨ"),count)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧࡶࠨࡩ"),l11l1lUK_Turk_No1 (u"ࠬࡴ࡯ࠨࡪ"))
        for item in match:
                try:
                        if l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡲࡲࡶࡹࡹࡤࡦࡸ࡬ࡰࡃ࠭࡫") in item: l11111llUK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽࡫ࡳࡸࡻࡄࠧ࡬")in item: l11l11llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠨ࠾ࡌࡱࡦ࡭ࡥ࠿ࠩ࡭")in item: l11l11ll1UK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸࡪࡾࡴ࠿ࠩ࡮")in item: l1llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡩࡲࡢࡲࡨࡶࡃ࠭࡯") in item: l11l11lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠫࡁࡸࡥࡥ࡫ࡵࡩࡨࡺ࠾ࠨࡰ") in item: l111l111lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠬࡂ࡯࡬ࡶ࡬ࡸࡱ࡫࠾ࠨࡱ") in item: OK(item)
                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡥ࡮ࡁࠫࡲ") in item: l111llllUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡦࡶࡦࡶࡥࡳࡀࠪࡳ") in item: l11l11lUK_Turk_No1(item)
                        else:l11l1UK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                except:pass
def apkInstaller(apk, url):
	ADDONTITLE=l11l1lUK_Turk_No1 (u"ࠨࡄࡵࡳࡼࡹࡥࡳࠢࡵࡩࡶࡻࡩࡳࡧࡧࠫࡴ")
	l1l1l111UK_Turk_No1.log(apk)
	l1l1l111UK_Turk_No1.log(url)
	if l1l1l111UK_Turk_No1.platform() == l11l1lUK_Turk_No1 (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪࡵ"):
		yes = DIALOG.yesno(ADDONTITLE, l11l1lUK_Turk_No1 (u"࡛ࠥࡴࡻ࡬ࡥࠢࡼࡳࡺࠦ࡬ࡪ࡭ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡲࡩࠦࡩ࡯ࡵࡷࡥࡱࡲ࠺ࠣࡶ"), apk, yeslabel=l11l1lUK_Turk_No1 (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩࠨࡷ"), nolabel=l11l1lUK_Turk_No1 (u"ࠧࡉࡡ࡯ࡥࡨࡰࠧࡸ"))
		if not yes: l1l1l111UK_Turk_No1.LogNotify(ADDONTITLE, l11l1lUK_Turk_No1 (u"࠭ࡅࡓࡔࡒࡖ࠿ࠦࡉ࡯ࡵࡷࡥࡱࡲࠠࡄࡣࡱࡧࡪࡲ࡬ࡦࡦࠪࡹ")); return
		display = apk
		if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
		if not l1l1l111UK_Turk_No1.workingURL(url) == True: l1l1l111UK_Turk_No1.LogNotify(ADDONTITLE, l11l1lUK_Turk_No1 (u"ࠧࡂࡒࡎࠤࡎࡴࡳࡵࡣ࡯ࡰࡪࡸ࠺ࠡࡋࡱࡺࡦࡲࡩࡥࠢࡄࡴࡰࠦࡕࡳ࡮ࠤࠫࡺ") % COLOR2); return
		DP.create(l11l1lUK_Turk_No1 (u"ࠨࡅ࡫ࡶࡴࡳࡥࠨࡻ"),l11l1lUK_Turk_No1 (u"ࠩ࡞ࡆࡢࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩ࠽࡟࠴ࡈ࡝ࠡࡅ࡫ࡶࡴࡳࡥࠨࡼ"),l11l1lUK_Turk_No1 (u"ࠪࠫࡽ"), l11l1lUK_Turk_No1 (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡜ࡧࡩࡵࠩࡾ"))
		lib=os.path.join(PACKAGES, l11l1lUK_Turk_No1 (u"ࠧࠫࡳ࠯ࡣࡳ࡯ࠧࡿ") % apk.replace(l11l1lUK_Turk_No1 (u"࠭࡜࡝ࠩࢀ"), l11l1lUK_Turk_No1 (u"ࠧࠨࢁ")).replace(l11l1lUK_Turk_No1 (u"ࠨ࠱ࠪࢂ"), l11l1lUK_Turk_No1 (u"ࠩࠪࢃ")).replace(l11l1lUK_Turk_No1 (u"ࠪ࠾ࠬࢄ"), l11l1lUK_Turk_No1 (u"ࠫࠬࢅ")).replace(l11l1lUK_Turk_No1 (u"ࠬ࠰ࠧࢆ"), l11l1lUK_Turk_No1 (u"࠭ࠧࢇ")).replace(l11l1lUK_Turk_No1 (u"ࠧࡀࠩ࢈"), l11l1lUK_Turk_No1 (u"ࠨࠩࢉ")).replace(l11l1lUK_Turk_No1 (u"ࠩࠥࠫࢊ"), l11l1lUK_Turk_No1 (u"ࠪࠫࢋ")).replace(l11l1lUK_Turk_No1 (u"ࠫࡁ࠭ࢌ"), l11l1lUK_Turk_No1 (u"ࠬ࠭ࢍ")).replace(l11l1lUK_Turk_No1 (u"࠭࠾ࠨࢎ"), l11l1lUK_Turk_No1 (u"ࠧࠨ࢏")).replace(l11l1lUK_Turk_No1 (u"ࠨࡾࠪ࢐"), l11l1lUK_Turk_No1 (u"ࠩࠪ࢑")))
		try: os.remove(lib)
		except: pass
		l1l11lUK_Turk_No1.download(url, lib, DP)
		xbmc.sleep(100)
		DP.close()
		notify.apkInstaller(apk)
		l1l1l111UK_Turk_No1.ebi(l11l1lUK_Turk_No1 (u"ࠪࡗࡹࡧࡲࡵࡃࡱࡨࡷࡵࡩࡥࡃࡦࡸ࡮ࡼࡩࡵࡻࠫࠦࠧ࠲ࠢࡢࡰࡧࡶࡴ࡯ࡤ࠯࡫ࡱࡸࡪࡴࡴ࠯ࡣࡦࡸ࡮ࡵ࡮࠯ࡘࡌࡉ࡜ࠨࠬࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡶ࡯ࡦ࠱ࡥࡳࡪࡲࡰ࡫ࡧ࠲ࡵࡧࡣ࡬ࡣࡪࡩ࠲ࡧࡲࡤࡪ࡬ࡺࡪࠨࠬࠣࡨ࡬ࡰࡪࡀࠧ࢒")+lib+l11l1lUK_Turk_No1 (u"ࠫࠧ࠯ࠧ࢓"))
	else: l1l1l111UK_Turk_No1.LogNotify(ADDONTITLE, l11l1lUK_Turk_No1 (u"ࠬࡋࡒࡓࡑࡕ࠾ࠥࡔ࡯࡯ࡧࠣࡅࡳࡪࡲࡰ࡫ࡧࠤࡉ࡫ࡶࡪࡥࡨࠫ࢔"))
def l1ll1l1llUK_Turk_No1():
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡸࠪ࢕"),l11l1lUK_Turk_No1 (u"ࠧ࡯ࡱࠪ࢖"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡐࡨࡻࠥࡋࡰࡪࡵࡲࡨࡪࡹࠠࡰࡨࠣࡘ࡛ࠦࡓࡩࡱࡺࡷࠬࢗ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡦࡺࡣࡩࡵࡨࡶ࡮࡫ࡳ࠮ࡱࡱࡰ࡮ࡴࡥ࠯ࡤࡨ࠳ࡱࡧࡳࡵ࠯࠶࠹࠵࠳ࡥࡱ࡫ࡶࡳࡩ࡫ࡳࠨ࢘"),23,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡥࡩࡪ࡯࡯ࡥ࡯ࡳࡺࡪ࠮ࡰࡴࡪ࠳ࡺࡱࡴࡶࡴ࡮࠳࡚ࡑࡔࡶࡴ࡮࠳ࡹࡼࠥ࠳࠲ࡶ࡬ࡴࡽࡳ࠰ࡗ࡮ࠤࡹࡻࡲ࡬ࠢࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡸࠦ࡮ࡦࡹࠣࡩࡵ࡯ࡳࡰࡦࡨࡷࠥࡺࡶࠡࡵ࡫ࡳࡼࡹ࠱࠯࡬ࡳ࡫࢙ࠬ"),fanart,description=l11l1lUK_Turk_No1 (u"࢚ࠫࠬ"))
def l1l1ll1l1UK_Turk_No1(url):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷ࢛ࠩ"),l11l1lUK_Turk_No1 (u"࠭࡮ࡰࠩ࢜"))
        l111lUK_Turk_No1=l1111llllUK_Turk_No1.l1ll11lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧ࢝")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
                l1111111UK_Turk_No1(name,url,24,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩ࢞"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠯ࠧ࢟"))
def l1l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡼࠧࢠ"),l11l1lUK_Turk_No1 (u"ࠫࡳࡵࠧࢡ"))
        l1l111UK_Turk_No1=[l11l1lUK_Turk_No1 (u"ࠬࡹࡴࡳࡧࡤࡱࡦࡴࡧࡰ࠰ࡦࡳࡲ࠭ࢢ"),l11l1lUK_Turk_No1 (u"࠭ࡶࡪࡦࡷࡳ࠳ࡳࡥࠨࢣ"),l11l1lUK_Turk_No1 (u"ࠧࡨࡱࡵ࡭ࡱࡲࡡࡷ࡫ࡧ࠲࡮ࡴࠧࢤ"),l11l1lUK_Turk_No1 (u"ࠨࡸ࡬ࡨࡿ࡯࠮ࡵࡸࠪࢥ"),l11l1lUK_Turk_No1 (u"ࠩࡵࡥࡵ࡯ࡤࡷ࡫ࡧࡩࡴ࠴ࡷࡴࠩࢦ")]
        count=[]
        l11lll1llUK_Turk_No1=[]
        l1l11ll11UK_Turk_No1=l1111llllUK_Turk_No1.l111l1l1UK_Turk_No1(url)
        i=1
        for link in l1l11ll11UK_Turk_No1:
                if urlresolver.HostedMediaFile(link).valid_url():
                        for l11ll1ll1UK_Turk_No1 in l1l111UK_Turk_No1:
                                if l11ll1ll1UK_Turk_No1 in link:
                                        count.append(l11l1lUK_Turk_No1 (u"ࠪࡐ࡮ࡴ࡫ࠡࠩࢧ")+str(i))
                                        l11lll1llUK_Turk_No1.append(link)
                                        i=i+1
        dialog = xbmcgui.Dialog()
        select = dialog.select(l11l1lUK_Turk_No1 (u"ࠫࡈ࡮࡯ࡰࡵࡨࠤࡦࠦ࡬ࡪࡰ࡮࠲࠳࠭ࢨ"),count)
        if select < 0:quit()
        url = l11lll1llUK_Turk_No1[select]
	l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1ll1111lUK_Turk_No1():
     l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡑࡱࡳࡹࡱࡧࡲࠡࡅࡤࡶࡹࡵ࡯࡯ࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨࢩ"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱ࠲࡫ࡪࡴࡲࡦ࠱ࡤࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡄࡹ࡯ࡳࡶࡀࡺ࡮࡫ࡷࡴࠨ࡮ࡩࡾࡽ࡯ࡳࡦࡀࠪࡹࡼ࠽ࠨࢪ"),27,l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫࠱࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡌࡆࡆࡰࡴ࠾ࡽ࠮࡫ࡲࡪࠫࢫ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩࢬ"))
def l11ll1111UK_Turk_No1():
    l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡻ࠭ࢭ"),l11l1lUK_Turk_No1 (u"ࠪࡲࡴ࠭ࢮ"))
    l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡕࡵࡰࡶ࡮ࡤࡶ࡚ࠥࡖࠡࡕ࡫ࡳࡼࡹࠧࢯ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡪࡳࡼࡧࡴࡤࡪࡩࡶࡪ࡫࡭ࡰࡸ࡬ࡩࡸ࠴ࡴࡰ࠱ࡂࡷࡴࡸࡴ࠾ࡸ࡬ࡩࡼࡹࠦ࡬ࡧࡼࡻࡴࡸࡤ࠾ࠨࡷࡺࡂ࠭ࢰ"),27,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࡍࡽ࡮ࡴࡵࡇ࡝࠲࡯ࡶࡧࠨࢱ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨࢲ"))
    l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡐࡨࡻ࡚ࠥࡖࠡࡕ࡫ࡳࡼࡹࠧࢳ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡧࡰࡹࡤࡸࡨ࡮ࡦࡳࡧࡨࡱࡴࡼࡩࡦࡵ࠱ࡸࡴ࠵࠿ࡴࡱࡵࡸࡂࡸࡥ࡭ࡧࡤࡷࡪࠬ࡫ࡦࡻࡺࡳࡷࡪ࠽ࠧࡶࡹࡁࠬࢴ"),27,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࡪࡓࡴࡕࡉ࠷ࡴ࠯࡬ࡳ࡫ࠬࢵ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬࢶ"))
def l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩࢷ"),l11l1lUK_Turk_No1 (u"࠭࡮ࡰࠩࢸ"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢ࡙ࡅࡂࡔࡆࡌࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࢹ"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡭࡯ࡸࡣࡷࡧ࡭࡬ࡲࡦࡧࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳ࠴ࡅ࡫ࡦࡻࡺࡳࡷࡪ࠽ࠨࢺ"),35,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࡥࡤ࠸ࡘࡾ࠸ࡱ࠰࡭ࡴ࡬࠭ࢻ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫࢼ"))
        l111lUK_Turk_No1=l1l1111UK_Turk_No1.l1ll11lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂ࠭࠴ࠫࡀࠫ࠿ࡷࡪࡶ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧࢽ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1l11111UK_Turk_No1(name,url,28,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭ࢾ"))
        try:
                l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡯ࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡱࡴࡃ࠭ࢿ")).findall(str(l111lUK_Turk_No1))[0]
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡓ࡫ࡸࡵࠢࡓࡥ࡬࡫ࠠ࠿ࡀࡁ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࣀ"),l11l1111lUK_Turk_No1,27,l11ll11llUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩࣁ"))
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨࣂ"))
def l11ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡼࠧࣃ"),l11l1lUK_Turk_No1 (u"ࠫࡳࡵࠧࣄ"))
        l111lUK_Turk_No1=l1l1111UK_Turk_No1.l1ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡦࡰࡧࡂࠬࣅ")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
                l1l11111UK_Turk_No1(name,url,29,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧࣆ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠭ࠬࣇ"))
def l1ll1lll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬࣈ"),l11l1lUK_Turk_No1 (u"ࠩࡱࡳࠬࣉ"))
        l111lUK_Turk_No1=l1l1111UK_Turk_No1.l11lll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠬ࠳࠱࠿ࠪ࠾ࡶࡩࡵࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡧࡱࡨࡃ࠭࣊")).findall(str(l111lUK_Turk_No1))
        for l1l1llllUK_Turk_No1,l1l111llUK_Turk_No1,url in match:
                l1111111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡊࡶࡩࡴࡱࡧࡩࠥࠫࡳࠨ࣋")%l1l1llllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠬ࠳ࠠࠦࡵࠪ࣌")%l1l111llUK_Turk_No1,url,30,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ࣍"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠭ࠬ࣎"))
def l1lll11llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺ࣏ࠬ"),l11l1lUK_Turk_No1 (u"ࠩࡱࡳ࣐ࠬ"))
        link=l1llll111UK_Turk_No1(url)
        l111l1llUK_Turk_No1=[]
        l1111lllUK_Turk_No1=[]
        l11l11l1UK_Turk_No1=[]
        l1l111UK_Turk_No1=[l11l1lUK_Turk_No1 (u"ࠪࡷࡹࡸࡥࡢ࡯ࡤࡲ࡬ࡵ࠮ࡤࡱࡰ࣑ࠫ"),l11l1lUK_Turk_No1 (u"ࠫࡻ࡯ࡤࡵࡱ࠱ࡱࡪ࣒࠭"),l11l1lUK_Turk_No1 (u"ࠬ࡭࡯ࡳ࡫࡯ࡰࡦࡼࡩࡥ࠰࡬ࡲ࣓ࠬ"),l11l1lUK_Turk_No1 (u"࠭ࡶࡪࡦࡽ࡭࠳ࡺࡶࠨࣔ"),l11l1lUK_Turk_No1 (u"ࠧࡳࡣࡳ࡭ࡩࡼࡩࡥࡧࡲ࠲ࡼࡹࠧࣕ")]
        l11lll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡶࡪࡲ࠽ࠣࡰࡲࡪࡴࡲ࡬ࡰࡹࠥࠤࡹ࡯ࡴ࡭ࡧࡀࠦ࠳࠱࠿ࠣࠢࡲࡲࡨࡲࡩࡤ࡭ࡀࠦ࠳࠱࠿ࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࡉ࡯ࡲࡦࡥࡷࠤࡑ࡯࡮࡬࠾࠲ࡥࡃ࠭ࣖ"),re.DOTALL).findall(link)
        i=1
        for l1lll1l1UK_Turk_No1 in l11lll1llUK_Turk_No1:
            l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠩ࠲࡫ࡴ࠴ࡰࡩࡲࡂ࡫ࡹ࡬࡯࠾ࠩࣗ"),l11l1lUK_Turk_No1 (u"ࠪࠫࣘ"))
            l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠫࠫࡺࡩࡵ࡮ࡨࡁࠬࣙ"))[0]
            if not l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧࣚ") in l1lll1l1UK_Turk_No1:
                l1lll1l1UK_Turk_No1=base64.b64decode(l1lll1l1UK_Turk_No1)
                l11l11l11UK_Turk_No1=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"࠭ࡳࡵࡴࡨࡥࡲࡧ࡮ࡨࡱࠪࣛ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠧࡷ࡫ࡧࡸࡴ࠭ࣜ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠨࡩࡲࡶ࡮ࡲ࡬ࡢࡸ࡬ࡨࠬࣝ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠩࡹ࡭ࡩࢀࡩࠨࣞ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠪࡳࡵ࡫࡮࡭ࡱࡤࡨࠬࣟ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠫࡪࡹࡴࡳࡧࡤࡱࠬ࣠") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠬࡴ࡯ࡸࡸ࡬ࡨࡪࡵࠧ࣡") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"࠭ࡲࡢࡲ࡬ࡨࡻ࡯ࡤࡦࡱࠪ࣢") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠧࡍ࡫ࡱ࡯ࣣࠥ࠭")+str(i))
                    i=i+1
        dialog = xbmcgui.Dialog()
        select = dialog.select(name,l1111lllUK_Turk_No1)
        if select < 0:quit()
        else:
            url=l111l1llUK_Turk_No1[select]
            l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1111l11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡩࡵࡧࡰࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠࡵ࡫ࡷࡰࡪࡃࠢ࠯࠭ࡂࠦࡃ࠴ࠫࡀ࠾࡬ࡱ࡬ࠦࡳࡳࡥࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡧࡵࡲࡥࡧࡵࡁࠧ࠴ࠫࡀࠤࠣࡻ࡮ࡪࡴࡩ࠿ࠥ࠲࠰ࡅࠢࠡࡪࡨ࡭࡬࡮ࡴ࠾ࠤ࠱࠯ࡄࠨࠠࡢ࡮ࡷࡁࠧ࡝ࡡࡵࡥ࡫ࠤ࠭࠴ࠫࡀࠫࠥࡂࡁ࠵ࡡ࠿࠾࠲ࡨ࡮ࡼ࠾ࠨࣤ"),re.DOTALL).findall(link)
        for url,l1l11l11UK_Turk_No1,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡧࡰࡹࡤࡸࡨ࡮ࡦࡳࡧࡨࡱࡴࡼࡩࡦࡵ࠱ࡸࡴ࠭ࣥ")+url
            l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻ࣦࠩ")+l1l11l11UK_Turk_No1
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠳࠺࠽ࠥࣧ"),l11l1lUK_Turk_No1 (u"ࠧ࠭ࠢࣨ")).replace(l11l1lUK_Turk_No1 (u"࠭ࠦࡢ࡯ࡳ࠿ࣩࠬ"),l11l1lUK_Turk_No1 (u"ࠧࠡࠨࠣࠫ࣪"))
            if l11l1lUK_Turk_No1 (u"ࠨࡶࡹ࠱ࡸ࡮࡯ࡸࠩ࣫") in url:
                l1l11111UK_Turk_No1(name,url,28,l1l11l11UK_Turk_No1,fanart)
def l11ll11lUK_Turk_No1(url):
    string =l11l1lUK_Turk_No1 (u"ࠩࠪ࣬")
    keyboard = xbmc.Keyboard(string, l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡈࡲࡹ࡫ࡲࠡࡕࡨࡥࡷࡩࡨࠡࡖࡨࡶࡲࡡ࠯ࡄࡑࡏࡓࡗࡣ࣭ࠧ"))
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(l11l1lUK_Turk_No1 (u"࣮ࠫࠥ࠭"),l11l1lUK_Turk_No1 (u"ࠬ࠱࣯ࠧ"))
        if len(string)>1:
            url = l11l1lUK_Turk_No1 (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱ࠲ࡃࡰ࡫ࡹࡸࡱࡵࡨࡂࠨࣰ") + string
            l1111l11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        else: quit()
def l11llll1UK_Turk_No1():
        url = l11l1lUK_Turk_No1 (u"ࠧ࠱ࣱࠩ")
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࠪࠫࠬ࠭ࠤ࡞࡫ࡲ࡭࡫ࠣ࡝ࡪࡴࡩࠡࡇ࡮ࡰࡪࡴࡥ࡯࡮ࡨࡶࠥࡊࡩࡻ࡫࡯ࡩࡷࠦ࠱ࠡࠬ࠭࠮࠯ࡡ࠯ࡄࡑࡏࡓࡗࡣࣲࠧ"),url,25,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡳࡔࡵࡲࡺ࡬ࡑ࠮࡫ࡲࡪࠫࣳ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫࣴ"))
def l1ll1l111UK_Turk_No1(url):
        l111lUK_Turk_No1=l11l1111UK_Turk_No1.l1ll11lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂ࠭࠴ࠫࡀࠫ࠿ࡷࡪࡶ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧࣵ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                if not l11l1lUK_Turk_No1 (u"ࠬࡪऱࡻ࡮ࡤࡶࣶࠬ") in name:
                        l1111111UK_Turk_No1(name,url,26,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧࣷ"))
        try:
                l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡲࡵࡄࠧࣸ")).findall(str(l111lUK_Turk_No1))[0]
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡔࡥࡹࡶࠣࡔࡦ࡭ࡥࠡࡀࡁࡂࡠ࠵ࡃࡐࡎࡒࡖࡢࣹ࠭"),l11l1111lUK_Turk_No1,25,l11ll11llUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࣺࠩࠪ"))
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠪࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶ࠩࠨࣻ"))
def l11llll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111ll11lUK_Turk_No1=l11l1111UK_Turk_No1.l11ll1l11UK_Turk_No1(url)
        l111ll11lUK_Turk_No1 = l111ll11lUK_Turk_No1[1:]
        l1l11lllUK_Turk_No1=len(l111ll11lUK_Turk_No1)
        if l1l11lllUK_Turk_No1 > 1:
                count=[]
                i=1
                for part in l111ll11lUK_Turk_No1:
                        count.append(l11l1lUK_Turk_No1 (u"ࠫࡕࡧࡲࡵࠢࠪࣼ")+str(i))
                        i=i+1
                        dialog = xbmcgui.Dialog()
                select = dialog.select(l11l1lUK_Turk_No1 (u"ࠬࡉࡨࡰࡱࡶࡩࠥࡧࠠࡑࡣࡵࡸ࠳࠴ࠧࣽ"),count)
                if select < 0:quit()
                url = l111ll11lUK_Turk_No1[select]
	l1llll1llUK_Turk_No1=l11l1111UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1l1UK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def l1lll1ll1UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡ࠯࠰ࠪࠫࠢ࡜ࡩࡷࡲࡩ࡛ࠡࡨࡲ࡮ࠦࡅ࡬࡮ࡨࡲࡪࡴ࡬ࡦࡴࠣࡈ࡮ࢀࡩ࡭ࡧࡵࠤ࠷ࠦࠪࠫࠬ࠭࡟࠴ࡉࡏࡍࡑࡕࡡࠬࣾ"),l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡸࡹࡺ࠲ࡨࡧ࡮࡭࡫ࡧ࡭ࡿ࡯ࡨࡥ࠸࠱ࡧࡴࡳ࠯ࠨࣿ"),36,l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴ࡹࡓࡴࡱࡹ࡫ࡐ࠴ࡪࡱࡩࠪऀ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪँ"))
def l11ll111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l1l11l11lUK_Turk_No1.l1ll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠬ࠳࠱࠿ࠪ࠾ࡶࡩࡵࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡧࡱࡨࡃ࠭ं")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,37,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬः"))
        try:
                l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂ࡮ࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡰࡳࡂࠬऄ")).findall(str(l111lUK_Turk_No1))[0]
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡒࡪࡾࡴࠡࡒࡤ࡫ࡪࠦ࠾࠿ࡀ࡞࠳ࡈࡕࡌࡐࡔࡠࠫअ"),l11l1111lUK_Turk_No1,36,l11ll11llUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨआ"))
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠴࠮࠭इ"))
def l1ll111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111ll11lUK_Turk_No1=l1l11l11lUK_Turk_No1.l11ll1l11UK_Turk_No1(url)
        l1l11lllUK_Turk_No1=len(l111ll11lUK_Turk_No1)
        if l1l11lllUK_Turk_No1 > 1:
                count=[]
                i=1
                for part in l111ll11lUK_Turk_No1:
                        count.append(l11l1lUK_Turk_No1 (u"ࠩࡓࡥࡷࡺࠠࠨई")+str(i))
                        i=i+1
                        dialog = xbmcgui.Dialog()
                select = dialog.select(l11l1lUK_Turk_No1 (u"ࠪࡇ࡭ࡵ࡯ࡴࡧࠣࡥࠥࡖࡡࡳࡶ࠱࠲ࠬउ"),count)
                if select < 0:quit()
                url = l111ll11lUK_Turk_No1[select]
	l1llll1llUK_Turk_No1=l1l11l11lUK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1l1UK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def l1l1ll111UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟࠭࠮࠯࠰ࠠࡕࡔࡗࠤ࡞࡫ࡲ࡭࡫ࠣ࡝ࡪࡴࡩࠡࡇ࡮ࡰࡪࡴࡥ࡯࡮ࡨࡶࠥࡊࡩࡻ࡫࡯ࡩࡷࠦࠪࠫࠬ࠭࡟࠴ࡉࡏࡍࡑࡕࡡࠬऊ"),url,45,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࠯࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࡦࡰ࠲ࡲ࡙࡬ࡱ࠳ࡰࡰࡨࠩऋ"),fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧऌ"))
def l1ll1lUK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡊࡉ࡛ࡋ࡞࠳ࡈࡕࡌࡐࡔࡠࠫऍ"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡴࡳࡶ࠱ࡸࡻ࠵࠲࠰ࡦ࡬ࡾ࡮ࡲࡥࡳࠩऎ"),21,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰࡫ࡓ࡝ࡹࡋࡷ࠴࠰࡭ࡴ࡬࠭ए"),fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫऐ"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟ࡓࡖࡔࡍࡒࡂࡏ࡞࠳ࡈࡕࡌࡐࡔࡠࠫऑ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡸࡷࡺ࠮ࡵࡸ࠲࠶࠵࠷࠴࠺࠱ࡳࡶࡴ࡭ࡲࡢ࡯࡯ࡥࡷ࠭ऒ"),21,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࠰࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴࠺ࡕࡲࡗࡘࡍ࡬࠴ࡪࡱࡩࠪओ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨऔ"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࡂࡆࡎࡊࡉࡘࡋࡌ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩक"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡼࡽ࠮ࡵࡴࡷ࠲ࡹࡼ࠯࠳࠲࠴࠹࠸࠵ࡢࡦ࡮ࡪࡩࡸ࡫࡬ࠨख"),21,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮࠴ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱ࡋࡉࡎ࠾ࡃࡵࡶ࠱࡮ࡵ࡭ࠧग"),fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬघ"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠࡇࡔࡉࡕࡌ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪङ"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡹࡸࡴ࠯ࡶࡹ࠳࠷࠶࠱࠶࠹࠲ࡧࡴࡩࡵ࡬ࠩच"),21,l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫࠱࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵࡚ࡘ࠷ࡨࡓ࡬ࡲ࠮࡫ࡲࡪࠫछ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩज"))
def l1ll1111UK_Turk_No1(url):
        l111lUK_Turk_No1=l111111UK_Turk_No1.l11l1ll11UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠫ࠲࠰ࡅࠩ࠽ࡵࡨࡴࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡦࡰࡧࡂࠬझ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
            l1111111UK_Turk_No1(name,url,22,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫञ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠫࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠰࠱ࠫࠪट"))
def l11111lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l11l111l1UK_Turk_No1=[]
        l1l111llUK_Turk_No1=[]
        l1l1l1111UK_Turk_No1=[]
        link=l1llll111UK_Turk_No1(url)
        l1l11l1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥ࡭ࡹ࡫࡭ࡠࡪࡨ࡭࡬࡮ࡴࠡࡥࡲࡰ࠲ࡲࡧ࠮࠴ࠣࡧࡴࡲ࠭࡮ࡦ࠰࠶ࠥࡩ࡯࡭࠯ࡶࡱ࠲࠹ࠠࡤࡱ࡯࠱ࡽࡹ࠭࠵ࠢࡦࡳࡱ࠳ࡸࡹࡵ࠰࠺ࠧࠦࡴࡪࡶ࡯ࡩࡂࠨࠢ࠿࠰࠮ࡃࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠮ࠬࡁ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧ࠴ࠫࡀࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡴࡱࡧࡹࠣࠢࡤࡰࡹࡃࠢࡪࡼ࡯ࡩࠧࠦ࠯࠿࠰࠮ࡃࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࡅࡶ࠾࠰࠮ࡃࠧࠦࡡ࡭ࡶࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡨࡲࡡࡴࡵࡀࠦ࡮ࡳࡧ࠮ࡴࡨࡷࡵࡵ࡮ࡴ࡫ࡹࡩࠥ࡮ࡡࡴࡡࡷࡳࡴࡲࡴࡪࡲࠥࠤ࠴ࡄࠧठ"),re.DOTALL).findall(link)
        for url,l1l11l11UK_Turk_No1,name in l1l11l1llUK_Turk_No1:
            url=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡹࡸࡴ࠯ࡶࡹࠫड")+url
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠧࡳࡸࡳࡹࡁࠧढ"),l11l1lUK_Turk_No1 (u"ࠨࠤࠪण")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠷࠹࠱࠼ࠤत"),l11l1lUK_Turk_No1 (u"ࠥࡧࠧथ")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠱࠺࠻࠾ࠦद"),l11l1lUK_Turk_No1 (u"ࠧࡉࠢध")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠴࠸࠶ࡀࠨन"),l11l1lUK_Turk_No1 (u"ࠢࡶࠤऩ")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠷࠶࠻ࠣप"),l11l1lUK_Turk_No1 (u"ࠤࡘࠦफ")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠱࠵࠽ࠥब"),l11l1lUK_Turk_No1 (u"ࠦࡔࠨभ")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠶࠹࠿ࠧम"),l11l1lUK_Turk_No1 (u"ࠨ࡯ࠣय")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠶࠽ࡀࠨर"),l11l1lUK_Turk_No1 (u"ࠣࠩࠥऱ"))
            l1l111llUK_Turk_No1.append(name)
            l11l111l1UK_Turk_No1.append(url)
        dialog = xbmcgui.Dialog()
        select = dialog.select(l11l1lUK_Turk_No1 (u"ࠩࡅࡳࡱࡻ࡭࡭ࡧࡵࠫल"),l1l111llUK_Turk_No1)
        if select < 0:quit()
	l1llll1llUK_Turk_No1=l111111UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1l1UK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def KD():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࠬ࠭࠮࠯ࠦࡋࡂࡐࡄࡐࠥࡊ࡚ࠠࡧࡵࡰ࡮࡙ࠦࡦࡰ࡬ࠤࡊࡱ࡬ࡦࡰࡨࡲࡱ࡫ࡲࠡࡆ࡬ࡾ࡮ࡲࡥࡳࠢ࠭࠮࠯࠰࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨळ"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡪࡴࡧࡦ࡮ࡶ࡭ࡿ࠴࡫ࡢࡰࡤࡰࡩ࠴ࡣࡰ࡯࠱ࡸࡷ࠵ࠧऴ"),46,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࠯࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࡩࡿࡘࡵ࡫ࡖࡳ࠳ࡰࡰࡨࠩव"),fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧश"))
def l11llllUK_Turk_No1(url):
        l111lUK_Turk_No1=l1111UK_Turk_No1.l11l1ll11UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡶࡩࡵࡄࠨ࠯࠭ࡂ࠭ࡁ࡫࡮ࡥࡀࠪष")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
            l1111111UK_Turk_No1(name,url,47,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩस"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨह"))
def l11lll1l1UK_Turk_No1(name,url):
        l11l111l1UK_Turk_No1=[]
        l1l111llUK_Turk_No1=[]
        link=l1llll111UK_Turk_No1(url)
        l1lll11l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡩ࡯ࡶࠡࡥ࡯ࡥࡸࡹ࠽ࠣ࡮࡬ࡷࡹࠨ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡴࡧ࡯ࡩࡨࡺ࠾ࠨऺ"),re.DOTALL).findall(link)[0]
        l1l11l1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡵࡰࡵ࡫ࡲࡲࠥࡼࡡ࡭ࡷࡨࡁࠧ࠮࠮ࠬࡁࠬࠦࠥࡄࠨ࠯࠭ࡂ࠭ࡁ࠵࡯ࡱࡶ࡬ࡳࡳࡄࠧऻ")).findall(l1lll11l1UK_Turk_No1)
        for url,name in l1l11l1llUK_Turk_No1:
            url=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡫࡮ࡨࡧ࡯ࡷ࡮ࢀ࠮࡬ࡣࡱࡥࡱࡪ࠮ࡤࡱࡰ࠲ࡹࡸ࠯ࡗ࡫ࡧࡩࡴ࠵ࡄࡦࡶࡤ࡭ࡱ࠵़ࠧ")+url
            name=name.replace(l11l1lUK_Turk_No1 (u"࠭ࠦࡲࡷࡲࡸࡀ࠭ऽ"),l11l1lUK_Turk_No1 (u"ࠧࠣࠩा")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠸࠷࠻ࠣि"),l11l1lUK_Turk_No1 (u"ࠤࡦࠦी")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠷࠹࠺࠽ࠥु"),l11l1lUK_Turk_No1 (u"ࠦࡈࠨू")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠷࠵࠿ࠧृ"),l11l1lUK_Turk_No1 (u"ࠨࡵࠣॄ")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠶࠵ࡁࠢॅ"),l11l1lUK_Turk_No1 (u"ࠣࡗࠥॆ")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠷࠷࠴࠼ࠤे"),l11l1lUK_Turk_No1 (u"ࠥࡓࠧै")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠵࠸࠾ࠦॉ"),l11l1lUK_Turk_No1 (u"ࠧࡵࠢॊ")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠵࠼࠿ࠧो"),l11l1lUK_Turk_No1 (u"ࠢࠨࠤौ"))
            l1l111llUK_Turk_No1.append(name)
            l11l111l1UK_Turk_No1.append(url)
        dialog = xbmcgui.Dialog()
        select = dialog.select(l11l1lUK_Turk_No1 (u"ࠨࡄࡲࡰࡺࡳ࡬ࡦࡴ्ࠪ"),l1l111llUK_Turk_No1)
        if select < 0:quit()
	l1llll1llUK_Turk_No1=l1111UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1l1UK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def l1l11l1l1UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝ࠫࠬ࠭࠮࡙ࠥࡈࡐ࡙ࡗ࡚ࠥ࡟ࡥࡳ࡮࡬ࠤ࡞࡫࡮ࡪࠢࡈ࡯ࡱ࡫࡮ࡦࡰ࡯ࡩࡷࠦࡄࡪࡼ࡬ࡰࡪࡸࠠࠫࠬ࠭࠮ࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ॎ"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡴࡪࡲࡻࡹࡻࡲ࡬࠰ࡦࡳࡲ࠴ࡴࡳ࠱ࡧ࡭ࡿ࡯࡬ࡦࡴ࠲ࡥࡷࡹࡩࡷࡦࡨ࡯࡮࠳ࡤࡪࡼ࡬ࡰࡪࡸࠧॏ"),48,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࠮ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲࡭ࡳ࠾࡮ࡄࡄ࠼࠲࡯ࡶࡧࠨॐ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭॑"))
def l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11lll1lUK_Turk_No1.l11l1ll1lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡵࡨࡴࡃ࠮࠮ࠬࡁࠬࡀࡪࡴࡤ࠿॒ࠩ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
            l1l11111UK_Turk_No1(name,url,49,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨ॓"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠴࠵࠯ࠧ॔"))
def l111lllllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11lll1lUK_Turk_No1.l11ll1l1UK_Turk_No1(name,url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠫ࠲࠰ࡅࠩ࠽ࡵࡨࡴࡃ࠮࠮ࠬࡁࠬࡀࡪࡴࡤ࠿ࠩॕ")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
            l1l11111UK_Turk_No1(name,url,50,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫॖ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠫࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡔࡧࡷ࡚࡮࡫ࡷࡎࡱࡧࡩ࠭࠻࠰ࠪࠩॗ"))
def l1llllll1UK_Turk_No1(url):
    parts=[]
    link=l1llll111UK_Turk_No1(url)
    parts.append(url)
    l1lll11l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡵ࡭ࠢࡦࡰࡦࡹࡳ࠾ࠤࡹ࡭ࡩ࡫࡯࠮ࡲࡤࡶࡹ࠳࡮ࡶ࡯ࡥࡩࡷࠨ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡶ࡮ࡁࠫक़"),re.DOTALL).findall(link)[0]
    l1l11l1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡣࡁࡀ࠴ࡲࡩ࠿ࠩख़")).findall(l1lll11l1UK_Turk_No1)
    for page,name in l1l11l1llUK_Turk_No1:
        page=l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡸࡹࡺ࠲ࡸ࡮࡯ࡸࡶࡹ࠲ࡨࡵ࡭࠯ࡶࡵࠫग़")+page
        parts.append(page)
        l1111111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡒࡤࡶࡨࡧࠠࠦࡵࠪज़")%name,page,51,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪड़"))
def l11ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡲ࡫ࡴࡢࠢࡱࡥࡲ࡫࠽ࠣࡲࡲࡴࡨࡵࡲ࡯࠼ࡶࡸࡷ࡫ࡡ࡮ࠤࠣࡧࡴࡴࡴࡦࡰࡷࡁࠧ࠮࠮ࠬࡁࠬࠦࠥ࠵࠾ࠨढ़"),re.DOTALL).findall(link)
        for url in match:
            l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1lll1111UK_Turk_No1():
    l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡬ࡸࡥࡦࡰࡠ࠱࠲࠳࠭࠮ࠢࡖࡴࡴࡸࡴࡴࠢࡋ࡭࡬࡮࡬ࡪࡩ࡫ࡸࡸࠦ࠭࠮࠯࠰࠱ࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭फ़"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡱ࡫ࡴࡲ࡯ࡴ࠰ࡦࡳࡲ࠵ࠧय़"),52,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࠰࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴ࡴࡧࡆࡨࡋ࡜࠸࠴ࡪࡱࡩࠪॠ"),fanart)
def l1ll11lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l1l1l11l1UK_Turk_No1.l1ll11l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧॡ")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
            l1l11111UK_Turk_No1(name,url,53,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩॢ"))
def l1l1ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢ࡮ࡣࡷࡧ࡭ࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠰ࡅࠩࠣࡀ࠿࡭ࡲ࡭ࠠࡴࡴࡦࡁࠧ࠴ࠫࡀࠤࠣ࠳ࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡧ࠾࠽࠱ࡧ࡭ࡻࡄࠧॣ"),re.DOTALL).findall(link)
        for url,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮࡯ࡩࡲࡰࡴࡹ࠮ࡤࡱࡰࠫ।")+url
            l1111111UK_Turk_No1(name,url,54,l1l11l11UK_Turk_No1,fanart)
        try:
            l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁ࠵ࡳࡱࡣࡱࡂࠥࡂࡡࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡥࡱ࠱ࡵࡧࡧࡦ࠯ࡱࡩࡼࡹࠢࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠾࠯࠭ࡂࡀ࠴ࡧ࠾ࠨ॥"),re.DOTALL).findall(link)
            for l111lll11UK_Turk_No1 in l11l1111lUK_Turk_No1:
                url=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡱ࡫ࡴࡲ࡯ࡴ࠰ࡦࡳࡲ࠭०")+l111lll11UK_Turk_No1
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡒࡊ࡞ࡔࠡࡒࡄࡋࡊࠦ࠾࠿ࡀ࡞࠳ࡈࡕࡌࡐࡔࡠࠫ१"),url,53,l11ll11llUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨ२"))
        except:pass
def llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
            link=l1llll111UK_Turk_No1(url)
            l111l1llUK_Turk_No1=[]
            l1111lllUK_Turk_No1=[]
            l11l11l1UK_Turk_No1=[]
            match=re.compile(l11l1lUK_Turk_No1 (u"ࠨࡣࡧࡨࡹ࡮ࡩࡴࡡ࡬ࡲࡱ࡯࡮ࡦࡡࡶ࡬ࡦࡸࡥࡠࡶࡲࡳࡱࡨ࡯ࡹࠪ࠱࠯ࡄ࠯ࠥ࠳ࡈࡶࡸࡷࡵ࡮ࡨࠧ࠶ࡉࠪ࠸࠰ࠨ३"),re.DOTALL).findall(link)[0]
            l11lll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩࡶࡶࡨࠫ࠳ࡅࠧ࠵࠶࠭࠴ࠫࡀࠫࠨ࠶࠷࠭४"),re.DOTALL).findall(match)
            i=1
            for l1lll1l1UK_Turk_No1 in l11lll1llUK_Turk_No1:
                l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠪࠩ࠸ࡇࠧ५"),l11l1lUK_Turk_No1 (u"ࠫ࠿࠭६")).replace(l11l1lUK_Turk_No1 (u"ࠬࠫ࠲ࡇࠩ७"),l11l1lUK_Turk_No1 (u"࠭࠯ࠨ८"))
                l11l11l11UK_Turk_No1=l1lll1l1UK_Turk_No1
                domain=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠧࡰ࡭࠱ࡶࡺ࠭९") in l1lll1l1UK_Turk_No1:
                    l1lll1l1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀࠧ॰")+l1lll1l1UK_Turk_No1
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠩࡋ࡭࡬࡮࡬ࡪࡩ࡫ࡸࡸ࠭ॱ"))
                elif l11l1lUK_Turk_No1 (u"ࠪࡷࡹࡸࡥࡢ࡯ࡤࡦࡱ࡫ࠧॲ") in l1lll1l1UK_Turk_No1:
                    l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠫ࠴࡫࠯ࠨॳ"),l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧॴ"))
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"࠭ࡈࡪࡩ࡫ࡰ࡮࡭ࡨࡵࡵࠪॵ"))
                elif l11l1lUK_Turk_No1 (u"ࠧࡪ࡯ࡪࡸࡨ࠭ॶ") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠨࡉࡲࡥࡱࡹࠧॷ"))
                elif l11l1lUK_Turk_No1 (u"ࠩࡰ࡭ࡽࡺࡡࡱࡧࠪॸ") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠪࡌ࡮࡭ࡨ࡭࡫ࡪ࡬ࡹࡹࠧॹ"))
                elif l11l1lUK_Turk_No1 (u"ࠫࡾࡵࡵࡵࡷࡥࡩࠬॺ") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠬࡎࡩࡨࡪ࡯࡭࡬࡮ࡴࡴࠩॻ"))
                else:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(domain)
                i=i+1
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,l1111lllUK_Turk_No1)
            if select < 0:quit()
            else:
                url=l111l1llUK_Turk_No1[select]
                l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1lllllll1UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡳࡧࡨࡲࡢ࠳࠭࠮࠯࠰ࠤࡋࡵ࡯ࡵࡤࡤࡰࡱࠦࡈࡪࡩ࡫ࡰ࡮࡭ࡨࡵࡵࠣ࠱࠲࠳࠭࠮࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪॼ"),url,32,l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳࠵ࡻࡨࡣ࠹ࡈࡆ࠳ࡰࡰࡨࠩॽ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩॾ"))
def l111l1l1lUK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩࡋ࡭࡬࡮࡬ࡪࡩ࡫ࡸࡸ࠭ॿ"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡧࡷ࡯ࡰࡲࡧࡴࡤࡪࡨࡷࡦࡴࡤࡴࡪࡲࡻࡸ࠴ࡣࡰ࡯࠲ࡧࡦࡺࡥࡨࡱࡵࡽ࠴࡮ࡩࡨࡪ࡯࡭࡬࡮ࡴࡴ࠱ࠪঀ"),33,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࡄࡳࡗ࡙࡭࠲ࡖ࠰࡭ࡴ࡬࠭ঁ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡓ࡯ࡳࡧࠣࡌ࡮࡭ࡨ࡭࡫ࡪ࡬ࡹࡹࠧং"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱ࡪࡺࡲ࡬࡮ࡣࡷࡧ࡭࡫ࡳࡢࡰࡧࡷ࡭ࡵࡷࡴ࠰ࡦࡳࡲ࠵ࡣࡢࡶࡨ࡫ࡴࡸࡹ࠰ࡨࡸࡰࡱ࠳࡭ࡢࡶࡦ࡬࠴࠭ঃ"),33,l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫࠱࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡃ࠺ࡼ࡜࠺ࡼࡺ࠮࡫ࡲࡪࠫ঄"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡒࡵࡩࡲ࡯ࡥࡳࠢࡏࡩࡦ࡭ࡵࡦࠩঅ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡦࡶ࡮࡯ࡱࡦࡺࡣࡩࡧࡶࡥࡳࡪࡳࡩࡱࡺࡷ࠳ࡩ࡯࡮࠱ࡦࡥࡹ࡫ࡧࡰࡴࡼ࠳ࡵࡸࡥ࡮࡫ࡨࡶ࠲ࡲࡥࡢࡩࡸࡩ࠴࠭আ"),33,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࡈࡆࡰࡪࡖ࡞ࡄ࠯࡬ࡳ࡫ࠬই"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡊࡴࡧ࡭ࡣࡱࡨࠬঈ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡩࡹࡱࡲ࡭ࡢࡶࡦ࡬ࡪࡹࡡ࡯ࡦࡶ࡬ࡴࡽࡳ࠯ࡥࡲࡱ࠴ࡩࡡࡵࡧࡪࡳࡷࡿ࠯ࡦࡰࡪࡰࡦࡴࡤ࠰ࠩউ"),33,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࡆࡷࡏࡨ࠸ࡄࡎ࠲࡯ࡶࡧࠨঊ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧࡔࡲࡤ࡭ࡳ࠭ঋ"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡬ࡵ࡭࡮ࡰࡥࡹࡩࡨࡦࡵࡤࡲࡩࡹࡨࡰࡹࡶ࠲ࡨࡵ࡭࠰ࡥࡤࡸࡪ࡭࡯ࡳࡻ࠲ࡷࡵࡧࡩ࡯࠱ࠪঌ"),33,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡃ࡫ࡩ࡝࡞࡮࠿࠮࡫ࡲࡪࠫ঍"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪࡍࡹࡧ࡬ࡺࠩ঎"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡨࡸࡰࡱࡳࡡࡵࡥ࡫ࡩࡸࡧ࡮ࡥࡵ࡫ࡳࡼࡹ࠮ࡤࡱࡰ࠳ࡨࡧࡴࡦࡩࡲࡶࡾ࠵ࡩࡵࡣ࡯ࡽࠬএ"),33,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱ࡋ࡮࠽ࡗࡦࡷ࡛࠱࡮ࡵ࡭ࠧঐ"),fanart)
def l1l1l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11ll1lUK_Turk_No1.l111lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡵࡨࡴࡃ࠮࠮ࠬࡁࠬࡀࡪࡴࡤ࠿ࠩ঑")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,34,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨ঒"))
        try:
            l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡱࡴࡃ࠮࠮ࠬࡁࠬࡀࡳࡶ࠾ࠨও")).findall(str(l111lUK_Turk_No1))
            for url in l11l1111lUK_Turk_No1:
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡵࡩࡩࡣࡎࡦࡺࡷࠤࡕࡧࡧࡦࠢࡁࡂࡃࡡ࠯ࡄࡑࡏࡓࡗࡣࠧঔ"),url,mode,l11ll11llUK_Turk_No1,fanart)
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠪࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶࠰ࠪࠩক"))
def l1ll11111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
            link=l1llll111UK_Turk_No1(url)
            l111l1llUK_Turk_No1=[]
            l1111lllUK_Turk_No1=[]
            l11l11l1UK_Turk_No1=[]
            l11lll1llUK_Turk_No1=l11ll1lUK_Turk_No1.l1lll1l1lUK_Turk_No1(url)
            i=1
            for l1lll1l1UK_Turk_No1 in l11lll1llUK_Turk_No1:
                l11l11l11UK_Turk_No1=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠫࡴࡱ࠮ࡳࡷࠪখ") in l1lll1l1UK_Turk_No1:
                    l1lll1l1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽ࠫগ")+l1lll1l1UK_Turk_No1
                    domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"࠭࠯ࠨঘ"))[2].replace(l11l1lUK_Turk_No1 (u"ࠧࡸࡹࡺ࠲ࠬঙ"),l11l1lUK_Turk_No1 (u"ࠨࠩচ"))
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠩࡏ࡭ࡳࡱࠠࠨছ")+str(i))
                else:
                    domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠪ࠳ࠬজ"))[2].replace(l11l1lUK_Turk_No1 (u"ࠫࡼࡽࡷ࠯ࠩঝ"),l11l1lUK_Turk_No1 (u"ࠬ࠭ঞ"))
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"࠭ࡌࡪࡰ࡮ࠤࠬট")+str(i))
                i=i+1
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,l1111lllUK_Turk_No1)
            if select < 0:quit()
            else:
                url=l111l1llUK_Turk_No1[select]
                l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1l111111UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧࡂ࠯࡝ࠤࡒࡵࡶࡪࡧࡶࠫঠ"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡰࡳࡻ࡯ࡥ࠵ࡷ࠱ࡧ࡭࠭ড"),39,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࡖ࠺ࡾ࡙࠹ࡰࡊ࠰࡭ࡴ࡬࠭ঢ"),fanart)
def l1l1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡦࡱࡻࡥ࡞ࡕࡈࡅࡗࡉࡈࠡࡃ࠰࡞ࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ণ"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡳ࡯ࡷ࡫ࡨ࠸ࡺ࠴ࡣࡩࠩত"),42,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࠯࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࡨࡧ࠴ࡔࡺ࠻ࡴ࠳ࡰࡰࡨࠩথ"),fanart)
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡭࡫ࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࠥࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡡ࠿࠾࠲ࡰ࡮ࡄࠧদ")).findall(link)
        for url,name in match:
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠤࠩধ"),l11l1lUK_Turk_No1 (u"ࠨ࠲࠰࠽ࠬন"))
            if l11l1lUK_Turk_No1 (u"ࠩ࠲ࡃࡱ࡫ࡴࡵࡧࡵࡁࠬ঩") in url:
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢ࠭প") %name,url,40,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࠮ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲࠹࡫࡛࡚ࡶ࡭ࡩ࠲࡯ࡶࡧࠨফ"),fanart)
def l111llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l1l1lll11UK_Turk_No1.l11ll1l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡴࡧࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡩࡳࡪ࠾ࠨব")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,41,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧভ"))
        try:
            l11l1111lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡲࡵࡄࠨ࠯࠭ࡂ࠭ࡁࡴࡰ࠿ࠩম")).findall(str(l111lUK_Turk_No1))
            for l111l1lllUK_Turk_No1,url in l11l1111lUK_Turk_No1:
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࠫࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩয")%l111l1lllUK_Turk_No1,url,40,l11ll11llUK_Turk_No1,fanart)
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨর"))
def l111l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
            link=l1llll111UK_Turk_No1(url)
            l111l1llUK_Turk_No1=[]
            l1111lllUK_Turk_No1=[]
            l11l11l1UK_Turk_No1=[]
            l11lll1llUK_Turk_No1=l1l1lll11UK_Turk_No1.l111l1l1UK_Turk_No1(url)
            i=1
            for l1lll1l1UK_Turk_No1 in l11lll1llUK_Turk_No1:
                l11l11l11UK_Turk_No1=l1lll1l1UK_Turk_No1
                domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠪ࠳ࠬ঱"))[2].replace(l11l1lUK_Turk_No1 (u"ࠫࡼࡽࡷ࠯ࠩল"),l11l1lUK_Turk_No1 (u"ࠬ࠭঳"))
                l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"࠭ࡌࡪࡰ࡮ࠤࠬ঴")+str(i))
                i=i+1
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,l1111lllUK_Turk_No1)
            if select < 0:quit()
            else:
                url=l111l1llUK_Turk_No1[select]
                l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    string =l11l1lUK_Turk_No1 (u"ࠧࠨ঵")
    keyboard = xbmc.Keyboard(string, l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡆࡰࡷࡩࡷࠦࡓࡦࡣࡵࡧ࡭ࠦࡔࡦࡴࡰ࡟࠴ࡉࡏࡍࡑࡕࡡࠬশ"))
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(l11l1lUK_Turk_No1 (u"ࠩࠣࠫষ"),l11l1lUK_Turk_No1 (u"ࠪ࠯ࠬস"))
        if len(string)>1:
            url = l11l1lUK_Turk_No1 (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡳ࡯ࡷ࡫ࡨ࠸ࡺ࠴ࡣࡩ࠱ࡂࡷࡂࠨহ") + string
            l1111l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        else: quit()
def l1111l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        l11lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࠦࡡ࡯࡫ࡰࡥࡹ࡯࡯࡯࠯࠵ࠦࡃ࠴ࠫࡀ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁ࠲࠰ࡅ࠼ࡪ࡯ࡪࠤࡸࡸࡣ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠢࡤࡰࡹࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠ࠰ࡀࠪ঺"),re.DOTALL).findall(link)
        for url,l1l11l11UK_Turk_No1,name in l11lUK_Turk_No1:
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠺࠵࠵࠼ࡁࠢ঻"),l11l1lUK_Turk_No1 (u"ࠢࠨࠤ়")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠼࠷࠷࠱࠼ࠤঽ"),l11l1lUK_Turk_No1 (u"ࠤ࠰ࠦা"))
            l1111111UK_Turk_No1(name,url,43,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫি"))
def l11l11lUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡩࡵ࡮ࡨࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡯ࡴ࡭ࡧࡁࠫী")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠭ু")).findall(item)[0]
        url=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡥࡵࡥࡵ࡫ࡲ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡵࡦࡶࡦࡶࡥࡳࡀࠪূ")).findall(item)[0]
        l1l11111UK_Turk_No1(name,url,20,l1l11l11UK_Turk_No1,fanart)
def l1lllll11UK_Turk_No1(url,l1l11l11UK_Turk_No1):
        string=url+l11l1lUK_Turk_No1 (u"ࠧ࠯ࡵࡦࡶࡦࡶࡥࠩࠫࠪৃ")
        link=eval(string)
        match= re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾࡬ࡸࡪࡳ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡪࡶࡨࡱࡃ࠭ৄ"),re.DOTALL).findall(link)
        count=str(len(match))
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠩࡦࡳࡺࡴࡴࠨ৅"),count)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡼࠧ৆"),l11l1lUK_Turk_No1 (u"ࠫࡳࡵࠧে"))
        for item in match:
                try:
                        if l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡱࡱࡵࡸࡸࡪࡥࡷ࡫࡯ࡂࠬৈ") in item: l11111llUK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡪࡲࡷࡺࡃ࠭৉")in item: l11l11llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽ࡋࡰࡥ࡬࡫࠾ࠨ৊")in item: l11l11ll1UK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷࡩࡽࡺ࠾ࠨো")in item: l1llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡨࡸࡡࡱࡧࡵࡂࠬৌ") in item: l11l11lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠪࡀࡷ࡫ࡤࡪࡴࡨࡧࡹࡄ্ࠧ") in item: l111l111lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠫࡁࡵ࡫ࡵ࡫ࡷࡰࡪࡄࠧৎ") in item: OK(item)
                        elif l11l1lUK_Turk_No1 (u"ࠬࡂࡤ࡭ࡀࠪ৏") in item: l111llllUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡥࡵࡥࡵ࡫ࡲ࠿ࠩ৐") in item: l11l11lUK_Turk_No1(item,l1l11l11UK_Turk_No1)
                        else:l11l1UK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                except:pass
def l111llllUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵ࡫ࡷࡰࡪࡄࠧ৑")).findall(item)[0]
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧࡰࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡪ࡬࠿ࠩ৒")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪ৓")).findall(item)[0]
        l11l1llUK_Turk_No1(name,url,19,l1l11l11UK_Turk_No1,fanart)
def l111l11l1UK_Turk_No1(name,url):
        filename=url.split(l11l1lUK_Turk_No1 (u"ࠪ࠳ࠬ৔"))[-1]
        if filename==l11l1lUK_Turk_No1 (u"ࠫࡱࡧࡴࡦࡵࡷࠫ৕"):filename=l11l1lUK_Turk_No1 (u"ࠬࡇࡣࡦࡕࡷࡶࡪࡧ࡭ࡆࡰࡪ࡭ࡳ࡫࠮ࡢࡲ࡮ࠫ৖")
        import downloader
        dialog = xbmcgui.Dialog()
        dp = xbmcgui.DialogProgress()
        l11lll1UK_Turk_No1 = dialog.browse(0, l11l1lUK_Turk_No1 (u"࠭ࡓࡦ࡮ࡨࡧࡹࠦࡦࡰ࡮ࡧࡩࡷࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹࡵࠧৗ"), l11l1lUK_Turk_No1 (u"ࠧ࡮ࡻࡳࡶࡴ࡭ࡲࡢ࡯ࡶࠫ৘"))
        lib=os.path.join(l11lll1UK_Turk_No1, filename)
        dp.create(l11l1lUK_Turk_No1 (u"ࠨࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬࠭৙"),l11l1lUK_Turk_No1 (u"ࠩࠪ৚"),l11l1lUK_Turk_No1 (u"ࠪࠫ৛"), l11l1lUK_Turk_No1 (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡜ࡧࡩࡵࠩড়"))
        downloader.download(url, lib, dp)
        dp.close()
        dialog = xbmcgui.Dialog()
        dialog.ok(l11l1lUK_Turk_No1 (u"ࠬࡊ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࠩঢ়"),l11l1lUK_Turk_No1 (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡧࡴࡲࡱ࠳࠴ࠧ৞"),l11lll1UK_Turk_No1)
def OK(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵ࡫ࡷࡰࡪࡄࠧয়")).findall(item)[0]
        l1l1l1l1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡲ࡯ࡹ࡯ࡴ࡭ࡧࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡳࡰࡺࡩࡵ࡮ࡨࡂࠬৠ")).findall(item)[0]
        line1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡰ࡮ࡴࡥ࠲ࡀࠫ࠲࠰ࡅࠩ࠽࠱࡯࡭ࡳ࡫࠱࠿ࠩৡ")).findall(item)[0]
        line2=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡱ࡯࡮ࡦ࠴ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡰ࡮ࡴࡥ࠳ࡀࠪৢ")).findall(item)[0]
        line3=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡲࡩ࡯ࡧ࠶ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡱ࡯࡮ࡦ࠵ࡁࠫৣ")).findall(item)[0]
        text=l11l1lUK_Turk_No1 (u"ࠬࠩࠣࠨ৤")+l1l1l1l1lUK_Turk_No1+l11l1lUK_Turk_No1 (u"࠭ࠣࠨ৥")+line1+l11l1lUK_Turk_No1 (u"ࠧࠤࠩ০")+line2+l11l1lUK_Turk_No1 (u"ࠨࠥࠪ১")+line3+l11l1lUK_Turk_No1 (u"ࠩࠦࠧࠬ২")
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠫ৩")).findall(item)[0]
        l11l1llUK_Turk_No1(name,text,17,l1l11l11UK_Turk_No1,fanart)
def l111lll1UK_Turk_No1(name,url):
        lines=re.compile(l11l1lUK_Turk_No1 (u"ࠫࠨࠩࠨ࠯࠭ࡂ࠭ࠨࠩࠧ৪")).findall(url)[0].split(l11l1lUK_Turk_No1 (u"ࠬࠩࠧ৫"))
        dialog = xbmcgui.Dialog()
        dialog.ok(lines[0],lines[1],lines[2],lines[3])
def l1llUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵ࡫ࡷࡰࡪࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡪࡶ࡯ࡩࡃ࠭৬")).findall(item)[0]
        text=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶࡨࡼࡹࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡦࡺࡷࡂࠬ৭")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩ৮")).findall(item)[0]
        l11l1llUK_Turk_No1(name,text,9,l1l11l11UK_Turk_No1,fanart)
def l11l1lllUK_Turk_No1(name,url):
        textfile=l1llll111UK_Turk_No1(url)
        l11111l1lUK_Turk_No1(name, textfile)
def l11l11ll1UK_Turk_No1(item):
        images=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡍࡲࡧࡧࡦࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡌࡱࡦ࡭ࡥ࠿ࠩ৯")).findall(item)
        if len(images)==1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡹ࡯ࡴ࡭ࡧࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡮ࡺ࡬ࡦࡀࠪৰ")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡂࠬৱ")).findall(item)[0]
                image=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡉ࡮ࡣࡪࡩࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡏ࡭ࡢࡩࡨࡂࠬ৲")).findall(item)[0]
                l1l11l11UK_Turk_No1 = image.replace(l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱ࠪ৳"),l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡪ࠰࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴࠭৴"))+l11l1lUK_Turk_No1 (u"ࠨ࠰࡭ࡴ࡬࠭৵")
                image = image.replace(l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴࠭৶"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࠩ৷"))+l11l1lUK_Turk_No1 (u"ࠫ࠳ࡰࡰࡨࠩ৸")
                l11l1llUK_Turk_No1(name,image,7,l1l11l11UK_Turk_No1,fanart)
        elif len(images)>1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡪࡶ࡯ࡩࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡩࡵ࡮ࡨࡂࠬ৹")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠧ৺")).findall(item)[0]
                l1l1llll1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࠨ৻")
                for image in images:
                        l1l11l11UK_Turk_No1 = image.replace(l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࠬৼ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡬࠲࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࠨ৽"))+l11l1lUK_Turk_No1 (u"ࠪ࠲࡯ࡶࡧࠨ৾")
                        image = image.replace(l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࠨ৿"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡯࠮ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࠫ਀"))+l11l1lUK_Turk_No1 (u"࠭࠮࡫ࡲࡪࠫਁ")
                        l1l1llll1UK_Turk_No1=l1l1llll1UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡋࡰࡥ࡬࡫࠾ࠨਂ")+image+l11l1lUK_Turk_No1 (u"ࠨ࠾࠲ࡍࡲࡧࡧࡦࡀࠪਃ")
                path = l1lll1UK_Turk_No1
                name=l1llllUK_Turk_No1(name)
                l1l1ll11UK_Turk_No1 = os.path.join(os.path.join(path,l11l1lUK_Turk_No1 (u"ࠩࠪ਄")), name+l11l1lUK_Turk_No1 (u"ࠪ࠲ࡹࡾࡴࠨਅ"))
                if not os.path.exists(l1l1ll11UK_Turk_No1):file(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠫࡼ࠭ਆ")).close()
                l111ll111UK_Turk_No1 = open(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡽࠢਇ"))
                l111ll111UK_Turk_No1.write(l1l1llll1UK_Turk_No1)
                l111ll111UK_Turk_No1.close()
                l11l1llUK_Turk_No1(name,l11l1lUK_Turk_No1 (u"࠭ࡩ࡮ࡣࡪࡩࠬਈ"),8,l1l11l11UK_Turk_No1,fanart)
def l11l11llUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵ࡫ࡷࡰࡪࡄࠧਉ")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩਊ")).findall(item)[0]
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭ࡵࡺࡶ࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡳࡸࡻࡄࠧ਋")).findall(item)[0]
        l1l11111UK_Turk_No1(name,url,6,l1l11l11UK_Turk_No1,fanart)
def l1ll11ll1UK_Turk_No1(url,l1l11l11UK_Turk_No1):
	link=l1llll111UK_Turk_No1(url)
	matches=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡢࠨ࠴ࠫࡀ࠼࠰ࡃࡠ࠶࠭࠺࡟࠭ࠬ࠳࠰࠿ࠪ࠮ࠫ࠲࠯ࡅࠩ࡝ࡰࠫ࠲࠯ࡅࠩࠥࠩ਌"),re.I+re.M+re.U+re.S).findall(link)
	l1l1l11UK_Turk_No1 = []
	for params, name, url in matches:
		l1ll1l11UK_Turk_No1 = {l11l1lUK_Turk_No1 (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦ਍"): params, l11l1lUK_Turk_No1 (u"ࠧࡴࡡ࡮ࡧࠥ਎"): name, l11l1lUK_Turk_No1 (u"ࠨࡵࡳ࡮ࠥਏ"): url}
		l1l1l11UK_Turk_No1.append(l1ll1l11UK_Turk_No1)
	list = []
	for l111lll1lUK_Turk_No1 in l1l1l11UK_Turk_No1:
		l1ll1l11UK_Turk_No1 = {l11l1lUK_Turk_No1 (u"ࠢ࡯ࡣࡰࡩࠧਐ"): l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠣࡰࡤࡱࡪࠨ਑")], l11l1lUK_Turk_No1 (u"ࠤࡸࡶࡱࠨ਒"): l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠥࡹࡷࡲࠢਓ")]}
		matches=re.compile(l11l1lUK_Turk_No1 (u"ࠫࠥ࠮࠮ࠬࡁࠬࡁࠧ࠮࠮ࠬࡁࠬࠦࠬਔ"),re.I+re.M+re.U+re.S).findall(l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠧࡶࡡࡳࡣࡰࡷࠧਕ")])
		for field, value in matches:
			l1ll1l11UK_Turk_No1[field.strip().lower().replace(l11l1lUK_Turk_No1 (u"࠭࠭ࠨਖ"), l11l1lUK_Turk_No1 (u"ࠧࡠࠩਗ"))] = value.strip()
		list.append(l1ll1l11UK_Turk_No1)
        for l111lll1lUK_Turk_No1 in list:
                if l11l1lUK_Turk_No1 (u"ࠨ࠰ࡷࡷࠬਘ") in l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠤࡸࡶࡱࠨਙ")]:l11l1llUK_Turk_No1(l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠥࡲࡦࡳࡥࠣਚ")],l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠦࡺࡸ࡬ࠣਛ")],2,l1l11l11UK_Turk_No1,fanart)
                else:l1111111UK_Turk_No1(l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠧࡴࡡ࡮ࡧࠥਜ")],l111lll1lUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠨࡵࡳ࡮ࠥਝ")],2,l1l11l11UK_Turk_No1,fanart)
def l11l1UK_Turk_No1(item,url,l1l11l11UK_Turk_No1):
        l11l1l111UK_Turk_No1=l1l11l11UK_Turk_No1
        base=url
        l11lll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽࡮࡬ࡲࡰࡄࠨ࠯࠭ࡂ࠭ࡁ࠵࡬ࡪࡰ࡮ࡂࠬਞ")).findall(item)
        data=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡭ࡹࡲࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡬ࡸࡱ࡫࠾࠯࠭ࡂࡰ࡮ࡴ࡫࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡮࡬ࡲࡰࡄ࠮ࠬࡁࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩਟ"),re.DOTALL).findall(item)
        for name,l11l1lll1UK_Turk_No1,l1l11l11UK_Turk_No1 in data:
                if l11l1lUK_Turk_No1 (u"ࠩࡼࡳࡺࡺࡵࡣࡧ࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡱ࡯ࡳࡵࡁࠪਠ") in l11l1lll1UK_Turk_No1:
                        l11111l11UK_Turk_No1 = l11l1lll1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠪࡰ࡮ࡹࡴ࠾ࠩਡ"))[1]
                        l1l11111UK_Turk_No1(name,l11l1lll1UK_Turk_No1,mode,l1l11l11UK_Turk_No1,fanart,description=l11111l11UK_Turk_No1)
        if len(l11lll1llUK_Turk_No1)==1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡩࡵ࡮ࡨࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡯ࡴ࡭ࡧࡁࠫਢ")).findall(item)[0]
                url=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂ࡬ࡪࡰ࡮ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡱ࡯࡮࡬ࡀࠪਣ")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠧਤ")).findall(item)[0]
                print l1l11l11UK_Turk_No1
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠧࡊ࡯ࡤ࡫ࡪࡎࡥࡳࡧࠪਥ"):l1l11l11UK_Turk_No1=l11l1l111UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠨ࠰ࡷࡷࠬਦ") in url:l11l1llUK_Turk_No1(name,url,16,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪਧ"))
                elif l11l1lUK_Turk_No1 (u"ࠪࡱࡴࡼࡩࡦࡵࠪਨ") in base:
                        l1l11UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,int(count),isFolder=False)
                else:l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
        elif len(l11lll1llUK_Turk_No1)>1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡩࡵ࡮ࡨࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡯ࡴ࡭ࡧࡁࠫ਩")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠭ਪ")).findall(item)[0]
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"࠭ࡉ࡮ࡣࡪࡩࡍ࡫ࡲࡦࠩਫ"):l1l11l11UK_Turk_No1=l11l1l111UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠧ࠯ࡶࡶࠫਬ") in url:l11l1llUK_Turk_No1(name,url,16,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩਭ"))
                elif l11l1lUK_Turk_No1 (u"ࠩࡰࡳࡻ࡯ࡥࡴࠩਮ") in base:
                        l1l11UK_Turk_No1(name,url,3,l1l11l11UK_Turk_No1,int(count),isFolder=False)
                else:l1111111UK_Turk_No1(name,url,3,l1l11l11UK_Turk_No1,fanart)
def l1lllll1lUK_Turk_No1(url):
	link=l1llll111UK_Turk_No1(url)
	sort=False
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡲࡦࡳࡥ࠾ࠤࠫ࠲࠰ࡅࠩࠣ࠰࠮ࡃࡷࡲ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠯࠭ࡂࡱ࡬ࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠧਯ"),re.DOTALL).findall(link)
	if l11l1lUK_Turk_No1 (u"ࠫࡹࡼࠥ࠳࠲ࡶ࡬ࡴࡽࡳࠨਰ") in url or l11l1lUK_Turk_No1 (u"ࠬࡩࡡࡳࡶࡲࡳࡳࡹࠧ਱") in url:
                match=sorted(match)
                sort=True
	for name,url,icon in match:
                        if name[0]==l11l1lUK_Turk_No1 (u"࠭࠰ࠨਲ"):
                                if sort==True:
                                        name=name[1:] + l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࠦࠠࠡࠪࡑࡩࡼ࠯࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨਲ਼")
                        if l11l1lUK_Turk_No1 (u"ࠨࡻࡲࡹࡹࡻࡢࡦ࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡰ࡮ࡹࡴࡀ࡮࡬ࡷࡹࡃࠧ਴") in url:
                                l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                        elif l11l1lUK_Turk_No1 (u"ࠩࡼࡳࡺࡺࡵࡣࡧ࠱ࡧࡴࡳ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡵࡨࡥࡷࡩࡨࡠࡳࡸࡩࡷࡿ࠽ࠨਵ") in url:
                                l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                        else:
                                l1l11111UK_Turk_No1(name,url,1,icon,fanart)
def l11111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        if l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨ࠲ࡨࡵ࡭࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡶࡩࡦࡸࡣࡩࡡࡴࡹࡪࡸࡹ࠾ࠩਸ਼") in url:
		l11111l11UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠫࡸ࡫ࡡࡳࡥ࡫ࡣࡶࡻࡥࡳࡻࡀࠫ਷"))[1]
		l111l11llUK_Turk_No1 = l1lll111UK_Turk_No1 + l11111l11UK_Turk_No1 + l1111lll1UK_Turk_No1
		req = urllib2.Request(l111l11llUK_Turk_No1)
		req.add_header(l11l1lUK_Turk_No1 (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩਸ"), l11l1lUK_Turk_No1 (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠤ࠭࡝ࡩ࡯ࡦࡲࡻࡸࡁࠠࡖ࠽࡛ࠣ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠶࠰࠴࠿ࠥ࡫࡮࠮ࡉࡅ࠿ࠥࡸࡶ࠻࠳࠱࠽࠳࠶࠮࠴ࠫࠣࡋࡪࡩ࡫ࡰ࠱࠵࠴࠵࠾࠰࠺࠴࠷࠵࠼ࠦࡆࡪࡴࡨࡪࡴࡾ࠯࠴࠰࠳࠲࠸࠭ਹ"))
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		link = link.replace(l11l1lUK_Turk_No1 (u"ࠧ࡝ࡴࠪ਺"),l11l1lUK_Turk_No1 (u"ࠨࠩ਻")).replace(l11l1lUK_Turk_No1 (u"ࠩ࡟ࡲ਼ࠬ"),l11l1lUK_Turk_No1 (u"ࠪࠫ਽")).replace(l11l1lUK_Turk_No1 (u"ࠫࠥࠦࠧਾ"),l11l1lUK_Turk_No1 (u"ࠬ࠭ਿ"))
		match=re.compile(l11l1lUK_Turk_No1 (u"࠭ࠢࡷ࡫ࡧࡩࡴࡏࡤࠣ࠼ࠣࠦ࠭࠴ࠫࡀࠫࠥ࠲࠰ࡅࠢࡵ࡫ࡷࡰࡪࠨ࠺ࠡࠤࠫ࠲࠰ࡅࠩࠣࠩੀ"),re.DOTALL).findall(link)
		for l1l1111llUK_Turk_No1,name in match:
			url = l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡿ࡯ࡶࡶࡸࡦࡪ࠴ࡣࡰ࡯࠲ࡻࡦࡺࡣࡩࡁࡹࡁࠬੁ")+l1l1111llUK_Turk_No1
			l1l11l11UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡬࠲ࡾࡺࡩ࡮ࡩ࠱ࡧࡴࡳ࠯ࡷ࡫࠲ࠩࡸ࠵ࡨࡲࡦࡨࡪࡦࡻ࡬ࡵ࠰࡭ࡴ࡬࠭ੂ")%l1l1111llUK_Turk_No1
			l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
	elif l11l1lUK_Turk_No1 (u"ࠩࡼࡳࡺࡺࡵࡣࡧ࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡱ࡯ࡳࡵࡁ࡯࡭ࡸࡺ࠽ࠨ੃") in url:
		l11111l11UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠪࡴࡱࡧࡹ࡭࡫ࡶࡸࡄࡲࡩࡴࡶࡀࠫ੄"))[1]
		l111l11llUK_Turk_No1 = l1111l1llUK_Turk_No1 + l11111l11UK_Turk_No1 + l111l11UK_Turk_No1
		req = urllib2.Request(l111l11llUK_Turk_No1)
		req.add_header(l11l1lUK_Turk_No1 (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨ੅"), l11l1lUK_Turk_No1 (u"ࠬࡓ࡯ࡻ࡫࡯ࡰࡦ࠵࠵࠯࠲ࠣࠬ࡜࡯࡮ࡥࡱࡺࡷࡀࠦࡕ࠼࡚ࠢ࡭ࡳࡪ࡯ࡸࡵࠣࡒ࡙ࠦ࠵࠯࠳࠾ࠤࡪࡴ࠭ࡈࡄ࠾ࠤࡷࡼ࠺࠲࠰࠼࠲࠵࠴࠳ࠪࠢࡊࡩࡨࡱ࡯࠰࠴࠳࠴࠽࠶࠹࠳࠶࠴࠻ࠥࡌࡩࡳࡧࡩࡳࡽ࠵࠳࠯࠲࠱࠷ࠬ੆"))
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		link = link.replace(l11l1lUK_Turk_No1 (u"࠭࡜ࡳࠩੇ"),l11l1lUK_Turk_No1 (u"ࠧࠨੈ")).replace(l11l1lUK_Turk_No1 (u"ࠨ࡞ࡱࠫ੉"),l11l1lUK_Turk_No1 (u"ࠩࠪ੊")).replace(l11l1lUK_Turk_No1 (u"ࠪࠤࠥ࠭ੋ"),l11l1lUK_Turk_No1 (u"ࠫࠬੌ"))
		match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࠨࡴࡪࡶ࡯ࡩࠧࡀࠠࠣࠪ࠱࠯ࡄ࠯ࠢ࠯࠭ࡂࠦࡻ࡯ࡤࡦࡱࡌࡨࠧࡀࠠࠣࠪ࠱࠯ࡄ࠯ࠢࠨ੍"),re.DOTALL).findall(link)
		for name,l1l1111llUK_Turk_No1 in match:
			url = l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡾࡵࡵࡵࡷࡥࡩ࠳ࡩ࡯࡮࠱ࡺࡥࡹࡩࡨࡀࡸࡀࠫ੎")+l1l1111llUK_Turk_No1
			l1l11l11UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫࠱ࡽࡹ࡯࡭ࡨ࠰ࡦࡳࡲ࠵ࡶࡪ࠱ࠨࡷ࠴࡮ࡱࡥࡧࡩࡥࡺࡲࡴ࠯࡬ࡳ࡫ࠬ੏")%l1l1111llUK_Turk_No1
			l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
def l1l111l1lUK_Turk_No1(item):
        item=item.replace(l11l1lUK_Turk_No1 (u"ࠨ࡞ࡵࠫ੐"),l11l1lUK_Turk_No1 (u"ࠩࠪੑ")).replace(l11l1lUK_Turk_No1 (u"ࠪࡠࡹ࠭੒"),l11l1lUK_Turk_No1 (u"ࠫࠬ੓")).replace(l11l1lUK_Turk_No1 (u"ࠬࠬ࡮ࡣࡵࡳ࠿ࠬ੔"),l11l1lUK_Turk_No1 (u"࠭ࠧ੕")).replace(l11l1lUK_Turk_No1 (u"ࠧ࡝ࠩࠪ੖"),l11l1lUK_Turk_No1 (u"ࠨࠩ੗")).replace(l11l1lUK_Turk_No1 (u"ࠩ࡟ࡲࠬ੘"),l11l1lUK_Turk_No1 (u"ࠪࠫਖ਼"))
        data=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡳࡧ࡭ࡦ࠿ࠥࠬ࠳࠱࠿ࠪࠤ࠱࠯ࡄࡸ࡬࠾ࠤࠫ࠲࠰ࡅࠩࠣ࠰࠮ࡃࡲ࡭࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠨਗ਼"),re.DOTALL).findall(item)
        for name,url,l1l11l11UK_Turk_No1 in data:
                if l11l1lUK_Turk_No1 (u"ࠬࡿ࡯ࡶࡶࡸࡦࡪ࠴ࡣࡰ࡯࠲ࡧ࡭ࡧ࡮࡯ࡧ࡯࠳ࠬਜ਼") in url:
                        l11111l11UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"࠭ࡣࡩࡣࡱࡲࡪࡲ࠯ࠨੜ"))[1]
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11111l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠧࡺࡱࡸࡸࡺࡨࡥ࠯ࡥࡲࡱ࠴ࡻࡳࡦࡴ࠲ࠫ੝") in url:
                        l11111l11UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠨࡷࡶࡩࡷ࠵ࠧਫ਼"))[1]
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11111l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠩࡼࡳࡺࡺࡵࡣࡧ࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡱ࡯ࡳࡵࡁࠪ੟") in url:
                        l11111l11UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠪࡰ࡮ࡹࡴ࠾ࠩ੠"))[1]
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11111l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠾࠴࠵ࠧ੡") in url:
                        l1ll1l1lUK_Turk_No1 = HTMLParser()
                        url=l1ll1l1lUK_Turk_No1.unescape(url)
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart)
                else:
                        l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
def l11111llUK_Turk_No1(item,url,l1l11l11UK_Turk_No1):
        l11l1l111UK_Turk_No1=l1l11l11UK_Turk_No1
        l11lll1llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡱࡱࡵࡸࡸࡪࡥࡷ࡫࡯ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡸࡶ࡯ࡳࡶࡶࡨࡪࡼࡩ࡭ࡀࠪ੢")).findall(item)
        l1l1l1lllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡭࡫ࡱ࡯ࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡲࡩ࡯࡭ࡁࠫ੣")).findall(item)
        if len(l11lll1llUK_Turk_No1)+len(l1l1l1lllUK_Turk_No1)==1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵ࡫ࡷࡰࡪࡄࠧ੤")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩ੥")).findall(item)[0]
                url=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡵࡵࡲࡵࡵࡧࡩࡻ࡯࡬࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡵࡳࡳࡷࡺࡳࡥࡧࡹ࡭ࡱࡄࠧ੦")).findall(item)[0]
                url = l11l1lUK_Turk_No1 (u"ࠪࡴࡱࡻࡧࡪࡰ࠽࠳࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡘࡶ࡯ࡳࡶࡶࡈࡪࡼࡩ࡭࠱ࡂࡱࡴࡪࡥ࠾࠳ࠩࡥࡲࡶ࠻ࡪࡶࡨࡱࡂࡩࡡࡵࡥ࡫ࡩࡷࠫ࠳ࡥࡵࡷࡶࡪࡧ࡭ࡴࠧ࠵࠺ࡺࡸ࡬࠾ࠩ੧") +url
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠫࡎࡳࡡࡨࡧࡋࡩࡷ࡫ࠧ੨"):l1l11l11UK_Turk_No1=l11l1l111UK_Turk_No1
                l11l1llUK_Turk_No1(name,url,16,l1l11l11UK_Turk_No1,fanart)
        elif len(l11lll1llUK_Turk_No1)+len(l1l1l1lllUK_Turk_No1)>1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡪࡶ࡯ࡩࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡩࡵ࡮ࡨࡂࠬ੩")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠧ੪")).findall(item)[0]
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠧࡊ࡯ࡤ࡫ࡪࡎࡥࡳࡧࠪ੫"):l1l11l11UK_Turk_No1=l11l1l111UK_Turk_No1
                l11l1llUK_Turk_No1(name,url,3,l1l11l11UK_Turk_No1,fanart)
def l1l1ll1UK_Turk_No1(link):
	if l111l1l11UK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠨࠩ੬"):
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(l11l1lUK_Turk_No1 (u"ࠩࡄࡨࡺࡲࡴࠡࡅࡲࡲࡹ࡫࡮ࡵࠩ੭"), l11l1lUK_Turk_No1 (u"ࠪ࡝ࡴࡻࠠࡩࡣࡹࡩࠥࡵࡰࡵࡧࡧࠤࡹࡵࠠࡴࡪࡲࡻࠥࡧࡤࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡱࡸࠬ੮"),l11l1lUK_Turk_No1 (u"ࠫࠬ੯"),l11l1lUK_Turk_No1 (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡤࠤࡵࡧࡳࡴࡹࡲࡶࡩࠦࡴࡰࠢࡳࡶࡪࡼࡥ࡯ࡶࠣࡥࡨࡩࡩࡥࡧࡱࡸࡦࡲࠠࡢࡥࡦࡩࡸࡹࠧੰ"),l11l1lUK_Turk_No1 (u"࠭ࡃࡢࡰࡦࡩࡱ࠭ੱ"),l11l1lUK_Turk_No1 (u"ࠧࡐࡍࠪੲ"))
		if ret == 1:
                        l1lll111lUK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠨࠩੳ"), l11l1lUK_Turk_No1 (u"ࠩࡖࡩࡹࠦࡐࡢࡵࡶࡻࡴࡸࡤࠨੴ"))
			l1lll111lUK_Turk_No1.doModal()
			if (l1lll111lUK_Turk_No1.isConfirmed()):
			    l1l1UK_Turk_No1 = l1lll111lUK_Turk_No1.getText()
			    l11l1l1llUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬੵ"),l1l1UK_Turk_No1)
                else:quit()
	elif l111l1l11UK_Turk_No1 <> l11l1lUK_Turk_No1 (u"ࠫࠬ੶"):
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(l11l1lUK_Turk_No1 (u"ࠬࡇࡤࡶ࡮ࡷࠤࡈࡵ࡮ࡵࡧࡱࡸࠬ੷"), l11l1lUK_Turk_No1 (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡶࡨࡶࠥࡺࡨࡦࠢࡳࡥࡸࡹࡷࡰࡴࡧࠤࡾࡵࡵࠡࡵࡨࡸࠬ੸"),l11l1lUK_Turk_No1 (u"ࠧࡵࡱࠣࡧࡴࡴࡴࡪࡰࡸࡩࠬ੹"),l11l1lUK_Turk_No1 (u"ࠨࠩ੺"),l11l1lUK_Turk_No1 (u"ࠩࡆࡥࡳࡩࡥ࡭ࠩ੻"),l11l1lUK_Turk_No1 (u"ࠪࡓࡐ࠭੼"))
		if ret == 1:
			l1lll111lUK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠫࠬ੽"), l11l1lUK_Turk_No1 (u"ࠬࡋ࡮ࡵࡧࡵࠤࡕࡧࡳࡴࡹࡲࡶࡩ࠭੾"))
			l1lll111lUK_Turk_No1.doModal()
			if (l1lll111lUK_Turk_No1.isConfirmed()):
				l1l1UK_Turk_No1 = l1lll111lUK_Turk_No1.getText()
			if l1l1UK_Turk_No1 <> l111l1l11UK_Turk_No1:
				quit()
		else:quit()
def l1l1l1l1UK_Turk_No1():
        link=l1llll111UK_Turk_No1(l1ll1l11lUK_Turk_No1)
        l1l1lllllUK_Turk_No1=[l11l1lUK_Turk_No1 (u"࠭ࡌࡪࡸࡨࠤ࡙࡜ࠧ੿"),l11l1lUK_Turk_No1 (u"ࠧࡔࡲࡲࡶࡹࡹࠧ઀"),l11l1lUK_Turk_No1 (u"ࠨࡏࡲࡺ࡮࡫ࡳࠨઁ"),l11l1lUK_Turk_No1 (u"ࠩࡗ࡚࡙ࠥࡨࡰࡹࡶࠫં"),l11l1lUK_Turk_No1 (u"ࠪࡇࡦࡸࡴࡰࡱࡱࡷࠬઃ"),l11l1lUK_Turk_No1 (u"ࠫࡉࡵࡣࡶ࡯ࡨࡲࡹࡧࡲࡪࡧࡶࠫ઄"),l11l1lUK_Turk_No1 (u"࡙ࠬࡴࡢࡰࡧࡹࡵ࠭અ"),l11l1lUK_Turk_No1 (u"࠭ࡃࡰࡰࡦࡩࡷࡺࡳࠨઆ"),l11l1lUK_Turk_No1 (u"ࠧࡓࡣࡧ࡭ࡴ࠭ઇ"),l11l1lUK_Turk_No1 (u"ࠨࡅࡆࡘ࡛࠭ઈ"),l11l1lUK_Turk_No1 (u"ࠩࡗࡹࡷࡱࡩࡴࡪࠣࡘ࡛࠭ઉ"),l11l1lUK_Turk_No1 (u"ࠪࡘࡺࡸ࡫ࡪࡵ࡫ࠤࡒࡵࡶࡪࡧࡶࠫઊ"),l11l1lUK_Turk_No1 (u"ࠫࡋ࡯ࡴ࡯ࡧࡶࡷࠬઋ"),l11l1lUK_Turk_No1 (u"ࠬࡌ࡯ࡰࡦࠣࡔࡴࡸ࡮ࠨઌ")]
        l1lll111lUK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"࠭ࠧઍ"), l11l1lUK_Turk_No1 (u"ࠧࡔࡧࡤࡶࡨ࡮ࠧ઎"))
	l1lll111lUK_Turk_No1.doModal()
	if (l1lll111lUK_Turk_No1.isConfirmed()):
		l11111l11UK_Turk_No1=l1lll111lUK_Turk_No1.getText()
		l11111l11UK_Turk_No1=l11111l11UK_Turk_No1.upper()
	else:quit()
        l1llll1l1UK_Turk_No1=[]
        l11llUK_Turk_No1=[]
        link=l1llll111UK_Turk_No1(l1ll1l11lUK_Turk_No1)
        dialog = xbmcgui.Dialog()
	ret = dialog.multiselect(l11l1lUK_Turk_No1 (u"ࠣࡕࡨࡰࡪࡩࡴࠡࡹ࡫࡭ࡨ࡮ࠠࡤࡣࡷࡩ࡬ࡵࡲࡪࡧࡶࠤࡹࡵࠠࡴࡧࡤࡶࡨ࡮ࠢએ"), l1l1lllllUK_Turk_No1)
	for num in ret:
                l1llll1l1UK_Turk_No1.append(l1l1lllllUK_Turk_No1[num])
        for l1ll11l1lUK_Turk_No1 in l1llll1l1UK_Turk_No1:
                string=l11l1lUK_Turk_No1 (u"ࠩ࠿ࠫઐ")+l1ll11l1lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡂ࠭࠴ࠫࡀࠫ࠿࠳ࠬઑ")+l1ll11l1lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡃ࠭઒")
                match=re.compile(string,re.DOTALL).findall(link)
                for data in match:
                        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡣࡢࡶࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡧࡦࡺ࠾ࠨઓ")).findall(data)
                        print match
                        for data in match:
                                l11llUK_Turk_No1.append(data)
        for l11lllllUK_Turk_No1 in l11llUK_Turk_No1:
                try:
                        link=l1llll111UK_Turk_No1(l11lllllUK_Turk_No1)
                        l1l1l111lUK_Turk_No1(content, l1111111lUK_Turk_No1,link)
                        if l11l1lUK_Turk_No1 (u"࠭ࡉ࡯ࡦࡨࡼࠬઔ") in l11lllllUK_Turk_No1:
                                sort=False
                                match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࡯ࡣࡰࡩࡂࠨࠨ࠯࠭ࡂ࠭ࠧ࠴ࠫࡀࡴ࡯ࡁࠧ࠮࠮ࠬࡁࠬࠦ࠳࠱࠿࡮ࡩࡀࠦ࠭࠴ࠫࡀࠫࠥࠫક"),re.DOTALL).findall(link)
                                for name,url,icon in match:
                                        if l11111l11UK_Turk_No1 in name.upper():
                                                if name[0]==l11l1lUK_Turk_No1 (u"ࠨ࠲ࠪખ"):
                                                        name=name[1:] + l11l1lUK_Turk_No1 (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝ࠡࠢࠣࠬࡓ࡫ࡷࠪ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪગ")
                                                if l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨ࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡲࡩࡴࡶࡂࡰ࡮ࡹࡴ࠾ࠩઘ") in url:
                                                        l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                                                elif l11l1lUK_Turk_No1 (u"ࠫࡾࡵࡵࡵࡷࡥࡩ࠳ࡩ࡯࡮࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡷࡪࡧࡲࡤࡪࡢࡵࡺ࡫ࡲࡺ࠿ࠪઙ") in url:
                                                        l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                                                else:
                                                        l1l11111UK_Turk_No1(name,url,1,icon,fanart)
                        else:
                                match= re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡩࡵࡧࡰࡂ࠭࠴ࠫࡀࠫ࠿࠳࡮ࡺࡥ࡮ࡀࠪચ"),re.DOTALL).findall(link)
                                count=str(len(match))
                                l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭ࡣࡰࡷࡱࡸࠬછ"),count)
                                l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠧࡧࡣࡹࠫજ"),l11l1lUK_Turk_No1 (u"ࠨࡰࡲࠫઝ"))
                                for item in match:
                                        title= re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡮ࡺ࡬ࡦࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡭ࡹࡲࡥ࠿ࠩઞ")).findall(item)[0]
                                        if l11111l11UK_Turk_No1 in title.upper():
                                                try:
                                                        if l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡶ࡯ࡳࡶࡶࡨࡪࡼࡩ࡭ࡀࠪટ") in item: l11111llUK_Turk_No1(item,l11lllllUK_Turk_No1,l1l11l11UK_Turk_No1)
                                                        elif l11l1lUK_Turk_No1 (u"ࠫࡁ࡯ࡰࡵࡸࡁࠫઠ")in item: l11l11llUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠬࡂࡉ࡮ࡣࡪࡩࡃ࠭ડ")in item: l11l11ll1UK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡧࡻࡸࡃ࠭ઢ")in item: l1llUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡦࡶࡦࡶࡥࡳࡀࠪણ") in item: l11l11lUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠨ࠾ࡵࡩࡩ࡯ࡲࡦࡥࡷࡂࠬત") in item: l111l111lUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠩ࠿ࡳࡰࡺࡩࡵ࡮ࡨࡂࠬથ") in item: OK(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠪࡀࡩࡲ࠾ࠨદ") in item: l111llllUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡣࡳࡣࡳࡩࡷࡄࠧધ") in item: l11l11lUK_Turk_No1(item)
                                                        else:l11l1UK_Turk_No1(item,l11lllllUK_Turk_No1,l1l11l11UK_Turk_No1)
                                                except:pass
                except:pass
def l1ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l11l1l111UK_Turk_No1=l1l11l11UK_Turk_No1
	l111l1llUK_Turk_No1=[]
	l1111lllUK_Turk_No1=[]
	l11l11l1UK_Turk_No1=[]
	link=l1llll111UK_Turk_No1(url)
	urls=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡪࡶ࡯ࡩࡃ࠭ન")+re.escape(name)+l11l1lUK_Turk_No1 (u"࠭࠼࠰ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡪࡶࡨࡱࡃ࠭઩"),re.DOTALL).findall(link)[0]
        l11lll1llUK_Turk_No1=[]
	if l11l1lUK_Turk_No1 (u"ࠧ࠽࡮࡬ࡲࡰࡄࠧપ") in urls:
                l11111l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾࡯࡭ࡳࡱ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯࡭࡫ࡱ࡯ࡃ࠭ફ")).findall(urls)
                for l1l1lllUK_Turk_No1 in l11111l1UK_Turk_No1:
                        l11lll1llUK_Turk_No1.append(l1l1lllUK_Turk_No1)
        if l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡵࡵࡲࡵࡵࡧࡩࡻ࡯࡬࠿ࠩબ") in urls:
                l1l1l11llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡶ࡯ࡳࡶࡶࡨࡪࡼࡩ࡭ࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡶࡴࡴࡸࡴࡴࡦࡨࡺ࡮ࡲ࠾ࠨભ")).findall(urls)
                for l11ll1llUK_Turk_No1 in l1l1l11llUK_Turk_No1:
                        l11ll1llUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠾࠴࠵ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳࡙ࡰࡰࡴࡷࡷࡉ࡫ࡶࡪ࡮࠲ࡃࡲࡵࡤࡦ࠿࠴ࠪࡦࡳࡰ࠼࡫ࡷࡩࡲࡃࡣࡢࡶࡦ࡬ࡪࡸࠥ࠴ࡦࡶࡸࡷ࡫ࡡ࡮ࡵࠨ࠶࠻ࡻࡲ࡭࠿ࠪમ") +l11ll1llUK_Turk_No1
                        l11lll1llUK_Turk_No1.append(l11ll1llUK_Turk_No1)
	i=1
	for l1lll1l1UK_Turk_No1 in l11lll1llUK_Turk_No1:
                l11l11l11UK_Turk_No1=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠬࡧࡣࡦࡵࡷࡶࡪࡧ࡭࠻࠱࠲ࠫય") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"࠭࠮ࡢࡥࡨࡰ࡮ࡼࡥࠨર") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠧࡴࡱࡳ࠾࠴࠵ࠧ઱")in l1lll1l1UK_Turk_No1:l1l11l111UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠢࠫࡅࡨ࡫ࡳࡵࡴࡨࡥࡲࡹࠩࠨલ")
                else:l1l11l111UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪળ")
                if l11l1lUK_Turk_No1 (u"ࠪࠬࠬ઴") in l1lll1l1UK_Turk_No1:
                        l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠫ࠭࠭વ"))[0]
                        l1111l1lUK_Turk_No1=str(l11l11l11UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠬ࠮ࠧશ"))[1].replace(l11l1lUK_Turk_No1 (u"࠭ࠩࠨષ"),l11l1lUK_Turk_No1 (u"ࠧࠨસ"))+l1l11l111UK_Turk_No1)
                        l111l1llUK_Turk_No1.append(l1lll1l1UK_Turk_No1)
                        l1111lllUK_Turk_No1.append(l1111l1lUK_Turk_No1)
                else:
                        domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠨ࠱ࠪહ"))[2].replace(l11l1lUK_Turk_No1 (u"ࠩࡺࡻࡼ࠴ࠧ઺"),l11l1lUK_Turk_No1 (u"ࠪࠫ઻"))
                        l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                        l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠫࡑ࡯࡮࡬઼ࠢࠪ")+str(i)+l1l11l111UK_Turk_No1)#+ l11l1lUK_Turk_No1 (u"ࠬࠦࡼࠡࠩઽ") +domain)
                i=i+1
	dialog = xbmcgui.Dialog()
	select = dialog.select(l11l1lUK_Turk_No1 (u"࠭ࡃࡩࡱࡲࡷࡪࠦࡡࠡ࡮࡬ࡲࡰ࠴࠮ࠨા"),l1111lllUK_Turk_No1)
	if select < 0:quit()
	else:
		url = l111l1llUK_Turk_No1[select]
		l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1ll11llUK_Turk_No1(url):
    string = l11l1lUK_Turk_No1 (u"ࠢࡔࡪࡲࡻࡕ࡯ࡣࡵࡷࡵࡩ࠭ࠫࡳࠪࠤિ") %url
    xbmc.executebuiltin(string)
def l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        try:
                if l11l1lUK_Turk_No1 (u"ࠨࡵࡲࡴ࠿࠵࠯ࠨી")in url:
                        url = urllib.quote(url)
                        url=l11l1lUK_Turk_No1 (u"ࠩࡳࡰࡺ࡭ࡩ࡯࠼࠲࠳ࡵࡸ࡯ࡨࡴࡤࡱ࠳ࡶ࡬ࡦࡺࡸࡷ࠴ࡅ࡭ࡰࡦࡨࡁ࠷ࠬࡵࡳ࡮ࡀࠩࡸࠬ࡮ࡢ࡯ࡨࡁࠪࡹࠧુ")%(url,name.replace(l11l1lUK_Turk_No1 (u"ࠪࠤࠬૂ"),l11l1lUK_Turk_No1 (u"ࠫ࠰࠭ૃ")))
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠬࡧࡣࡦࡵࡷࡶࡪࡧ࡭࠻࠱࠲ࠫૄ") in url or l11l1lUK_Turk_No1 (u"࠭࠮ࡢࡥࡨࡰ࡮ࡼࡥࠨૅ") in url:
                        url = urllib.quote(url)
                        url=l11l1lUK_Turk_No1 (u"ࠧࡱ࡮ࡸ࡫࡮ࡴ࠺࠰࠱ࡳࡶࡴ࡭ࡲࡢ࡯࠱ࡴࡱ࡫ࡸࡶࡵ࠲ࡃࡲࡵࡤࡦ࠿࠴ࠪࡺࡸ࡬࠾ࠧࡶࠪࡳࡧ࡭ࡦ࠿ࠨࡷࠬ૆")%(url,name.replace(l11l1lUK_Turk_No1 (u"ࠨࠢࠪે"),l11l1lUK_Turk_No1 (u"ࠩ࠮ࠫૈ")))
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠪࡴࡱࡻࡧࡪࡰ࠽࠳࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡘࡶ࡯ࡳࡶࡶࡈࡪࡼࡩ࡭࠱ࠪૉ") in url:
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠫ࠳ࡺࡳࠨ૊")in url:
                        url = l11l1lUK_Turk_No1 (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠿࠵࠯ࡱ࡮ࡸ࡫࡮ࡴ࠮ࡷ࡫ࡧࡩࡴ࠴ࡦ࠵࡯ࡗࡩࡸࡺࡥࡳ࠱ࡂࡷࡹࡸࡥࡢ࡯ࡷࡽࡵ࡫࠽ࡕࡕࡇࡓ࡜ࡔࡌࡐࡃࡇࡉࡗࠬࡡ࡮ࡲ࠾ࡲࡦࡳࡥ࠾ࠩો")+name+l11l1lUK_Turk_No1 (u"࠭ࠦࡢ࡯ࡳ࠿ࡺࡸ࡬࠾ࠩૌ")+url
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif urlresolver.HostedMediaFile(url).valid_url():
                        url = urlresolver.HostedMediaFile(url).resolve()
                        l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif liveresolver.isValid(url)==True:
                        url=liveresolver.resolve(url)
                        l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                else:l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        except:
                notification(l11l1lUK_Turk_No1 (u"ࠧࡖࡍࡗࡹࡷࡱ્ࠧ"),l11l1lUK_Turk_No1 (u"ࠨࡕࡷࡶࡪࡧ࡭ࠡࡗࡱࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠭૎"), l11l1lUK_Turk_No1 (u"ࠩ࠶࠴࠵࠶ࠧ૏"), icon)
def l11111111UK_Turk_No1(url):
        if urlresolver.HostedMediaFile(url).valid_url():
                url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player ().play(url)
def l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l1l11l11UK_Turk_No1,thumbnailImage=l1l11l11UK_Turk_No1); l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"࡚ࠥ࡮ࡪࡥࡰࠤૐ"), infoLabels={ l11l1lUK_Turk_No1 (u"࡙ࠦ࡯ࡴ࡭ࡧࠥ૑"): name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l111l1lUK_Turk_No1)
        l111l1lUK_Turk_No1.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, l111l1lUK_Turk_No1)
def l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠬࡊࡩࡢ࡮ࡲ࡫࠳ࡉ࡬ࡰࡵࡨࠬࡦࡲ࡬࠭ࡖࡵࡹࡪ࠯ࠧ૒"))
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠨࡄࡦࡨࡤࡹࡱࡺࡆࡰ࡮ࡧࡩࡷ࠴ࡰ࡯ࡩࠥ૓"), thumbnailImage=l1l11l11UK_Turk_No1); l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"ࠢࡗ࡫ࡧࡩࡴࠨ૔"), infoLabels={ l11l1lUK_Turk_No1 (u"ࠣࡖ࡬ࡸࡱ࡫ࠢ૕"): name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l111l1lUK_Turk_No1)
        xbmc.Player ().play(url, l111l1lUK_Turk_No1, False)
def l111ll1lUK_Turk_No1(url):
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠤࡓࡰࡦࡿࡍࡦࡦ࡬ࡥ࠭ࠫࡳࠪࠤ૖")%url)
def l1llll1UK_Turk_No1(url):
        display=l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠪࡰࡦࡿ࡯ࡶࡶࠪ૗"))
        if display==l11l1lUK_Turk_No1 (u"ࠫࡑ࡯ࡳࡵࡧࡵࡷࠬ૘"):l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬࡲࡡࡺࡱࡸࡸࠬ૙"),l11l1lUK_Turk_No1 (u"࠭ࡃࡢࡶࡨ࡫ࡴࡸࡹࠨ૚"))
        else:l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠧ࡭ࡣࡼࡳࡺࡺࠧ૛"),l11l1lUK_Turk_No1 (u"ࠨࡎ࡬ࡷࡹ࡫ࡲࡴࠩ૜"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳ࡘࡥࡧࡴࡨࡷ࡭࠭૝"))
def l1llll111UK_Turk_No1(url):
        link = net.http_GET(url).content
        link=link.replace(l11l1lUK_Turk_No1 (u"ࠪࡀ࠴࡬ࡡ࡯ࡣࡵࡸࡃ࠭૞"),l11l1lUK_Turk_No1 (u"ࠫࡁ࡬ࡡ࡯ࡣࡵࡸࡃࡾ࠼࠰ࡨࡤࡲࡦࡸࡴ࠿ࠩ૟")).replace(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀ࠿࠳ࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲ࠾ࠨૠ"),l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࡼࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪૡ")).replace(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡷࡷࡹࡧ࡫࠾ࠨૢ"),l11l1lUK_Turk_No1 (u"ࠨ࠾࡯࡭ࡳࡱ࠾ࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡿ࡯ࡶࡶࡸࡦࡪ࠴ࡣࡰ࡯࠲ࡻࡦࡺࡣࡩࡁࡹࡁࠬૣ")).replace(l11l1lUK_Turk_No1 (u"ࠩ࠿࠳ࡺࡺࡵࡣࡧࡁࠫ૤"),l11l1lUK_Turk_No1 (u"ࠪࡀ࠴ࡲࡩ࡯࡭ࡁࠫ૥"))#.replace(l11l1lUK_Turk_No1 (u"ࠫࡃࡂ࠯ࠨ૦"),l11l1lUK_Turk_No1 (u"ࠬࡄࡸ࠽࠱ࠪ૧"))
        if l11l1lUK_Turk_No1 (u"࠭࠰࠷࠲࠴࠴࠺࠭૨") in link:link=decode(link)
        return link
def l1ll111l1UK_Turk_No1():
        param=[]
        l1ll1ll1lUK_Turk_No1=sys.argv[2]
        if len(l1ll1ll1lUK_Turk_No1)>=2:
                params=sys.argv[2]
                l1111ll1UK_Turk_No1=params.replace(l11l1lUK_Turk_No1 (u"ࠧࡀࠩ૩"),l11l1lUK_Turk_No1 (u"ࠨࠩ૪"))
                if (params[len(params)-1]==l11l1lUK_Turk_No1 (u"ࠩ࠲ࠫ૫")):
                        params=params[0:len(params)-2]
                l11UK_Turk_No1=l1111ll1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠪࠪࠬ૬"))
                param={}
                for i in range(len(l11UK_Turk_No1)):
                        l11l11UK_Turk_No1={}
                        l11l11UK_Turk_No1=l11UK_Turk_No1[i].split(l11l1lUK_Turk_No1 (u"ࠫࡂ࠭૭"))
                        if (len(l11l11UK_Turk_No1))==2:
                                param[l11l11UK_Turk_No1[0]]=l11l11UK_Turk_No1[1]
        return param
params=l1ll111l1UK_Turk_No1(); url=None; name=None; mode=None; l11lll111UK_Turk_No1=None; l1l11l11UK_Turk_No1=None
try: l11lll111UK_Turk_No1=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠧࡹࡩࡵࡧࠥ૮")])
except: pass
try: url=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠨࡵࡳ࡮ࠥ૯")])
except: pass
try: name=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠢ࡯ࡣࡰࡩࠧ૰")])
except: pass
try: mode=int(params[l11l1lUK_Turk_No1 (u"ࠣ࡯ࡲࡨࡪࠨ૱")])
except: pass
try: l1l11l11UK_Turk_No1=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠤ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠧ૲")])
except: pass
try: fanart=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠥࡪࡦࡴࡡࡳࡶࠥ૳")])
except: pass
try: description=urllib.unquote_plus([l11l1lUK_Turk_No1 (u"ࠦࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤ૴")])
except: pass
def notification(title, message, l1l111ll1UK_Turk_No1, l11l11lllUK_Turk_No1):
    xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧ࡞ࡂࡎࡅ࠱ࡲࡴࡺࡩࡧ࡫ࡦࡥࡹ࡯࡯࡯ࠪࠥ૵") + title + l11l1lUK_Turk_No1 (u"ࠨࠬࠣ૶") + message + l11l1lUK_Turk_No1 (u"ࠢ࠭ࠤ૷") + l1l111ll1UK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠣ࠮ࠥ૸") + l11l11lllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠤࠬࠦૹ"))
def l1llllUK_Turk_No1(string):
        l11l1l1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡠࡠ࠮࠮ࠬࡁࠬࡠࡢ࠭ૺ")).findall(string)
        for tag in l11l1l1lUK_Turk_No1:string=string.replace(tag,l11l1lUK_Turk_No1 (u"ࠫࠬૻ")).replace(l11l1lUK_Turk_No1 (u"ࠬࡡ࠯࡞ࠩૼ"),l11l1lUK_Turk_No1 (u"࠭ࠧ૽")).replace(l11l1lUK_Turk_No1 (u"ࠧ࡜࡟ࠪ૾"),l11l1lUK_Turk_No1 (u"ࠨࠩ૿"))
        return string
def l1l11ll1lUK_Turk_No1(string):
        string=string.split(l11l1lUK_Turk_No1 (u"ࠩࠣࠫ଀"))
        final=l11l1lUK_Turk_No1 (u"ࠪࠫଁ")
        for l1111ll11UK_Turk_No1 in string:
            l11111ll1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࠬଂ")+l1111ll11UK_Turk_No1[0].upper()+l11l1lUK_Turk_No1 (u"ࠬࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢ࠭ଃ")+l1111ll11UK_Turk_No1[1:]+l11l1lUK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠥ࠭଄")
            final=final+l11111ll1UK_Turk_No1
        return final
def l1l11UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,l11lll11UK_Turk_No1,isFolder=False):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠧࠡࠩଅ"),l11l1lUK_Turk_No1 (u"ࠨࠧ࠵࠴ࠬଆ"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠩࠣࠫଇ"),l11l1lUK_Turk_No1 (u"ࠪࠩ࠷࠶ࠧଈ"))
	if l1111l1l1UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠫࡹࡸࡵࡦࠩଉ"):
	  if not l11l1lUK_Turk_No1 (u"ࠬࡉࡏࡍࡑࡕࠫଊ") in name:
	    l111l1111UK_Turk_No1=name.partition(l11l1lUK_Turk_No1 (u"࠭ࠨࠨଋ"))
	    l1ll1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠢࠣଌ")
	    l1l1l1lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠣࠤ଍")
	    if len(l111l1111UK_Turk_No1)>0:
		l1ll1UK_Turk_No1=l111l1111UK_Turk_No1[0]
		l1l1l1lUK_Turk_No1=l111l1111UK_Turk_No1[2].partition(l11l1lUK_Turk_No1 (u"ࠩࠬࠫ଎"))
	    if len(l1l1l1lUK_Turk_No1)>0:
		l1l1l1lUK_Turk_No1=l1l1l1lUK_Turk_No1[0]
            l1l11lll1UK_Turk_No1 = eval(base64.b64decode(l11l1lUK_Turk_No1 (u"ࠪࡦ࡜࡜࠰࡚࡙࡫࡬ࡧࡳࡒࡴ࡜࡛ࡎࡿࡒ࡫࠲࡮ࡧࡋࡋࡋ࡙࡙ࡔ࡫ࡏࡍࡘࡴ࡛ࡉࡍࡪ࡞࡞ࡂࡱ࡚࠵ࡸࡱ࡫ࡔ࠱࡫࡝ࡈࡰ࠷ࡎࡘࡓ࠷࡞࡯ࡇࡹ࡚ࡖࡑࡱࡒࡰࡑ࠵ࡏࡊࡉ࠶ࡓࡔࡨ࠶ࡐ࡛࡟ࡲࡎࡈࡏ࠸ࡒࡲ࡟ࡸࡎࡉࡘ࡭ࡐࡗ࠽࠾ࠩଏ")))
	    l1l111lllUK_Turk_No1 = l1l11lll1UK_Turk_No1.l1lll1l11UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡲࡵࡶࡪࡧࠪଐ"), name=l1ll1UK_Turk_No1 ,year=l1l1l1lUK_Turk_No1)
	    u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠧࡅࡵࡳ࡮ࡀࠦ଑")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠨࠦࡴ࡫ࡷࡩࡂࠨ଒")+str(l11lll111UK_Turk_No1)+l11l1lUK_Turk_No1 (u"ࠢࠧ࡯ࡲࡨࡪࡃࠢଓ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠣࠨࡱࡥࡲ࡫࠽ࠣଔ")+urllib.quote_plus(name)
	    ok=True
	    l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l1l111lllUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠩࡦࡳࡻ࡫ࡲࡠࡷࡵࡰࠬକ")], thumbnailImage=l1l111lllUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠪࡧࡴࡼࡥࡳࡡࡸࡶࡱ࠭ଖ")])
	    l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"࡛ࠦ࡯ࡤࡦࡱࠥଗ"), infoLabels= l1l111lllUK_Turk_No1 )
	    l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡏࡳࡑ࡮ࡤࡽࡦࡨ࡬ࡦࠤଘ"),l11l1lUK_Turk_No1 (u"ࠨࡴࡳࡷࡨࠦଙ"))
	    l1l11llUK_Turk_No1=[]
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠧࡧࡣࡹࠫଚ"))==l11l1lUK_Turk_No1 (u"ࠨࡻࡨࡷࠬଛ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡵࡩࡩࡣࡒࡦ࡯ࡲࡺࡪࠦࡦࡳࡱࡰࠤ࡚ࡑࠠࡕࡷࡵ࡯ࠥࡌࡡࡷࡱࡸࡶ࡮ࡺࡥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪଜ"),l11l1lUK_Turk_No1 (u"ࠪ࡜ࡇࡓࡃ࠯ࡔࡸࡲࡕࡲࡵࡨ࡫ࡱࠬࠪࡹ࠿࡮ࡱࡧࡩࡂ࠷࠴ࠧࡰࡤࡱࡪࡃࠥࡴࠨࡸࡶࡱࡃࠥࡴࠨ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࡂࠫࡳࠪࠩଝ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧࡶࠨଞ"))==l11l1lUK_Turk_No1 (u"ࠬࡴ࡯ࠨଟ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࡇࡤࡥࠢࡷࡳ࡛ࠥࡋࠡࡖࡸࡶࡰࠦࡆࡢࡸࡲࡹࡷ࡯ࡴࡦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠࠫଠ"),l11l1lUK_Turk_No1 (u"࡙ࠧࡄࡐࡇ࠳ࡘࡵ࡯ࡒ࡯ࡹ࡬࡯࡮ࠩࠧࡶࡃࡲࡵࡤࡦ࠿࠴࠶ࠫࡴࡡ࡮ࡧࡀࠩࡸࠬࡵࡳ࡮ࡀࠩࡸࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠨࡷ࠮࠭ଡ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
	    if not l1l111lllUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠨࡤࡤࡧࡰࡪࡲࡰࡲࡢࡹࡷࡲࠧଢ")] == l11l1lUK_Turk_No1 (u"ࠩࠪଣ"): l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡴࡡࡳࡶࡢ࡭ࡲࡧࡧࡦࠩତ"), l1l111lllUK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠫࡧࡧࡣ࡬ࡦࡵࡳࡵࡥࡵࡳ࡮ࠪଥ")])
	    else: l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫଦ"), fanart)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=isFolder,totalItems=l11lll11UK_Turk_No1)
	    return ok
	else:
	    u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠨ࠿ࡶࡴ࡯ࡁࠧଧ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠢࠧࡵ࡬ࡸࡪࡃࠢନ")+str(l11lll111UK_Turk_No1)+l11l1lUK_Turk_No1 (u"ࠣࠨࡰࡳࡩ࡫࠽ࠣ଩")+str(mode)+l11l1lUK_Turk_No1 (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤପ")+urllib.quote_plus(name)
	    ok=True
	    l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l1l11l11UK_Turk_No1, thumbnailImage=l1l11l11UK_Turk_No1)
	    l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"࡚ࠥ࡮ࡪࡥࡰࠤଫ"), infoLabels={ l11l1lUK_Turk_No1 (u"࡙ࠦ࡯ࡴ࡭ࡧࠥବ"): name } )
	    l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡ࡯ࡣࡵࡸࡤ࡯࡭ࡢࡩࡨࠫଭ"), fanart)
	    l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡉࡴࡒ࡯ࡥࡾࡧࡢ࡭ࡧࠥମ"),l11l1lUK_Turk_No1 (u"ࠢࡵࡴࡸࡩࠧଯ"))
	    l1l11llUK_Turk_No1=[]
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬର"))==l11l1lUK_Turk_No1 (u"ࠩࡼࡩࡸ࠭଱"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝ࡓࡧࡰࡳࡻ࡫ࠠࡧࡴࡲࡱ࡛ࠥࡋࠡࡖࡸࡶࡰࠦࡆࡢࡸࡲࡹࡷ࡯ࡴࡦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠࠫଲ"),l11l1lUK_Turk_No1 (u"ࠫ࡝ࡈࡍࡄ࠰ࡕࡹࡳࡖ࡬ࡶࡩ࡬ࡲ࠭ࠫࡳࡀ࡯ࡲࡨࡪࡃ࠱࠵ࠨࡱࡥࡲ࡫࠽ࠦࡵࠩࡹࡷࡲ࠽ࠦࡵࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠥࡴࠫࠪଳ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩ଴"))==l11l1lUK_Turk_No1 (u"࠭࡮ࡰࠩଵ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡁࡥࡦࠣࡸࡴࠦࡕࡌࠢࡗࡹࡷࡱࠠࡇࡣࡹࡳࡺࡸࡩࡵࡧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࠬଶ"),l11l1lUK_Turk_No1 (u"ࠨ࡚ࡅࡑࡈ࠴ࡒࡶࡰࡓࡰࡺ࡭ࡩ࡯ࠪࠨࡷࡄࡳ࡯ࡥࡧࡀ࠵࠷ࠬ࡮ࡢ࡯ࡨࡁࠪࡹࠦࡶࡴ࡯ࡁࠪࡹࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠩࡸ࠯ࠧଷ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=isFolder)
	    return ok
def l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪସ")):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠪࠤࠬହ"),l11l1lUK_Turk_No1 (u"ࠫࠪ࠸࠰ࠨ଺"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠬࠦࠧ଻"),l11l1lUK_Turk_No1 (u"࠭ࠥ࠳࠲଼ࠪ"))
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠢࡀࡷࡵࡰࡂࠨଽ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠣࠨࡰࡳࡩ࡫࠽ࠣା")+str(mode)+l11l1lUK_Turk_No1 (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤି")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠥࠪࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯࠿ࠥୀ")+str(description)+l11l1lUK_Turk_No1 (u"ࠦࠫ࡬ࡡ࡯ࡣࡵࡸࡂࠨୁ")+urllib.quote_plus(fanart)+l11l1lUK_Turk_No1 (u"ࠧࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠥୂ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠨࡄࡦࡨࡤࡹࡱࡺࡆࡰ࡮ࡧࡩࡷ࠴ࡰ࡯ࡩࠥୃ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"ࠢࡗ࡫ࡧࡩࡴࠨୄ"), infoLabels={ l11l1lUK_Turk_No1 (u"ࠣࡖ࡬ࡸࡱ࡫ࠢ୅"): name, l11l1lUK_Turk_No1 (u"ࠩࡳࡰࡴࡺࠧ୆"): description } )
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡴࡡࡳࡶࡢ࡭ࡲࡧࡧࡦࠩେ"), fanart)
        l1l11llUK_Turk_No1=[]
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧࡶࠨୈ"))==l11l1lUK_Turk_No1 (u"ࠬࡿࡥࡴࠩ୉"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡖࡪࡳ࡯ࡷࡧࠣࡪࡷࡵ࡭ࠡࡗࡎࠤ࡙ࡻࡲ࡬ࠢࡉࡥࡻࡵࡵࡳ࡫ࡷࡩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣࠧ୊"),l11l1lUK_Turk_No1 (u"࡙ࠧࡄࡐࡇ࠳ࡘࡵ࡯ࡒ࡯ࡹ࡬࡯࡮ࠩࠧࡶࡃࡲࡵࡤࡦ࠿࠴࠸ࠫࡴࡡ࡮ࡧࡀࠩࡸࠬࡵࡳ࡮ࡀࠩࡸࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠨࡷ࠮࠭ୋ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬୌ"))==l11l1lUK_Turk_No1 (u"ࠩࡱࡳ୍ࠬ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡄࡨࡩࠦࡴࡰࠢࡘࡏ࡚ࠥࡵࡳ࡭ࠣࡊࡦࡼ࡯ࡶࡴ࡬ࡸࡪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ୎"),l11l1lUK_Turk_No1 (u"ࠫ࡝ࡈࡍࡄ࠰ࡕࡹࡳࡖ࡬ࡶࡩ࡬ࡲ࠭ࠫࡳࡀ࡯ࡲࡨࡪࡃ࠱࠳ࠨࡱࡥࡲ࡫࠽ࠦࡵࠩࡹࡷࡲ࠽ࠦࡵࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠥࡴࠫࠪ୏")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
        if l11l1lUK_Turk_No1 (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠿࠵࠯ࠨ୐") in url:
                u=url
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=True)
        return ok
def l11l1llUK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ୑")):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠧࠡࠩ୒"),l11l1lUK_Turk_No1 (u"ࠨࠧ࠵࠴ࠬ୓"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠩࠣࠫ୔"),l11l1lUK_Turk_No1 (u"ࠪࠩ࠷࠶ࠧ୕"))
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠦࡄࡻࡲ࡭࠿ࠥୖ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠧࠬ࡭ࡰࡦࡨࡁࠧୗ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡯ࡣࡰࡩࡂࠨ୘")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠢࠧࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࡃࠢ୙")+str(description)+l11l1lUK_Turk_No1 (u"ࠣࠨ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࡂࠨ୚")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠤࡇࡩ࡫ࡧࡵ࡭ࡶࡉࡳࡱࡪࡥࡳ࠰ࡳࡲ࡬ࠨ୛"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡴࡡࡳࡶࡢ࡭ࡲࡧࡧࡦࠩଡ଼"), fanart)
        l1l11llUK_Turk_No1=[]
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧࡶࠨଢ଼"))==l11l1lUK_Turk_No1 (u"ࠬࡿࡥࡴࠩ୞"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡖࡪࡳ࡯ࡷࡧࠣࡪࡷࡵ࡭ࠡࡗࡎࠤ࡙ࡻࡲ࡬ࠢࡉࡥࡻࡵࡵࡳ࡫ࡷࡩࡸࡡ࠯ࡄࡑࡏࡓࡗࡣࠧୟ"),l11l1lUK_Turk_No1 (u"࡙ࠧࡄࡐࡇ࠳ࡘࡵ࡯ࡒ࡯ࡹ࡬࡯࡮ࠩࠧࡶࡃࡲࡵࡤࡦ࠿࠴࠸ࠫࡴࡡ࡮ࡧࡀࠩࡸࠬࡵࡳ࡮ࡀࠩࡸࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠨࡷ࠮࠭ୠ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬୡ"))==l11l1lUK_Turk_No1 (u"ࠩࡱࡳࠬୢ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡄࡨࡩࠦࡴࡰࠢࡘࡏ࡚ࠥࡵࡳ࡭ࠣࡊࡦࡼ࡯ࡶࡴ࡬ࡸࡪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨୣ"),l11l1lUK_Turk_No1 (u"ࠫ࡝ࡈࡍࡄ࠰ࡕࡹࡳࡖ࡬ࡶࡩ࡬ࡲ࠭ࠫࡳࡀ࡯ࡲࡨࡪࡃ࠱࠳ࠨࡱࡥࡲ࡫࠽ࠦࡵࠩࡹࡷࡲ࠽ࠦࡵࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠥࡴࠫࠪ୤")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭୥")):
        url=url.replace(l11l1lUK_Turk_No1 (u"࠭ࠠࠨ୦"),l11l1lUK_Turk_No1 (u"ࠧࠦ࠴࠳ࠫ୧"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠨࠢࠪ୨"),l11l1lUK_Turk_No1 (u"ࠩࠨ࠶࠵࠭୩"))
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠥࡃࡺࡸ࡬࠾ࠤ୪")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠦࠫࡳ࡯ࡥࡧࡀࠦ୫")+str(mode)+l11l1lUK_Turk_No1 (u"ࠧࠬ࡮ࡢ࡯ࡨࡁࠧ୬")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠨࠦࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࡂࠨ୭")+str(description)+l11l1lUK_Turk_No1 (u"ࠢࠧ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࡁࠧ୮")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠣࡆࡨࡪࡦࡻ࡬ࡵࡈࡲࡰࡩ࡫ࡲ࠯ࡲࡱ࡫ࠧ୯"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡳࡧࡲࡵࡡ࡬ࡱࡦ࡭ࡥࠨ୰"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠥࡍࡸࡖ࡬ࡢࡻࡤࡦࡱ࡫ࠢୱ"),l11l1lUK_Turk_No1 (u"ࠦࡹࡸࡵࡦࠤ୲"))
        l1l11llUK_Turk_No1=[]
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩ୳"))==l11l1lUK_Turk_No1 (u"࠭ࡹࡦࡵࠪ୴"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡗ࡫࡭ࡰࡸࡨࠤ࡫ࡸ࡯࡮ࠢࡘࡏ࡚ࠥࡵࡳ࡭ࠣࡊࡦࡼ࡯ࡶࡴ࡬ࡸࡪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ୵"),l11l1lUK_Turk_No1 (u"ࠨ࡚ࡅࡑࡈ࠴ࡒࡶࡰࡓࡰࡺ࡭ࡩ࡯ࠪࠨࡷࡄࡳ࡯ࡥࡧࡀ࠵࠹ࠬ࡮ࡢ࡯ࡨࡁࠪࡹࠦࡶࡴ࡯ࡁࠪࡹࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠩࡸ࠯ࠧ୶")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡻ࠭୷"))==l11l1lUK_Turk_No1 (u"ࠪࡲࡴ࠭୸"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡅࡩࡪࠠࡵࡱ࡙ࠣࡐࠦࡔࡶࡴ࡮ࠤࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ୹"),l11l1lUK_Turk_No1 (u"ࠬ࡞ࡂࡎࡅ࠱ࡖࡺࡴࡐ࡭ࡷࡪ࡭ࡳ࠮ࠥࡴࡁࡰࡳࡩ࡫࠽࠲࠴ࠩࡲࡦࡳࡥ࠾ࠧࡶࠪࡺࡸ࡬࠾ࠧࡶࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠦࡵࠬࠫ୺")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok
def popup(url,name):
        message=l1llll111UK_Turk_No1(url)
        if len(message)>1:
                path = l1lll1UK_Turk_No1
                l1l1ll11UK_Turk_No1 = os.path.join(os.path.join(path,l11l1lUK_Turk_No1 (u"࠭ࠧ୻")), name+l11l1lUK_Turk_No1 (u"ࠧ࠯ࡶࡻࡸࠬ୼"))
                if not os.path.exists(l1l1ll11UK_Turk_No1):
                    file(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠨࡹࠪ୽")).close()
                r = open(l1l1ll11UK_Turk_No1)
                l1ll1llllUK_Turk_No1 = r.read()
                if l1ll1llllUK_Turk_No1 == message:pass
                else:
                        l11111l1lUK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩࡘࡏ࡙ࡻࡲ࡬ࠩ୾"), message)
                        l111ll111UK_Turk_No1 = open(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠥࡻࠧ୿"))
                        l111ll111UK_Turk_No1.write(message)
                        l111ll111UK_Turk_No1.close()
def l11111l1lUK_Turk_No1(heading, text):
    id = 10147
    xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠫࡆࡩࡴࡪࡸࡤࡸࡪ࡝ࡩ࡯ࡦࡲࡻ࠭ࠫࡤࠪࠩ஀") % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass
def l11l1llllUK_Turk_No1(name):
        global l1111lUK_Turk_No1
        global l1ll1ll1UK_Turk_No1
        global l1lllll1UK_Turk_No1
        global window
        global l1llll11UK_Turk_No1
        global images
        l1l1ll11UK_Turk_No1 = os.path.join(os.path.join(l1lll1UK_Turk_No1,l11l1lUK_Turk_No1 (u"ࠬ࠭஁")), name+l11l1lUK_Turk_No1 (u"࠭࠮ࡵࡺࡷࠫஂ"))
        r = open(l1l1ll11UK_Turk_No1)
        l1ll1llllUK_Turk_No1 = r.read()
        images=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽࡫ࡰࡥ࡬࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡪ࡯ࡤ࡫ࡪࡄࠧஃ")).findall(l1ll1llllUK_Turk_No1)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡲࡲࡷࠬ஄"),l11l1lUK_Turk_No1 (u"ࠩ࠳ࠫஅ"))
	window= pyxbmct.AddonDialogWindow(l11l1lUK_Turk_No1 (u"ࠪࠫஆ"))
        l1l1lll1lUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠫ࠴ࡸࡥࡴࡱࡸࡶࡨ࡫ࡳ࠰ࡣࡵࡸࠬஇ")
        l1lllUK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࠧஈ") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"࠭࡮ࡦࡺࡷࡣ࡫ࡵࡣࡶࡵ࠱ࡴࡳ࡭ࠧஉ")))
        l11l111UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࠩஊ") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠨࡰࡨࡼࡹ࠷࠮ࡱࡰࡪࠫ஋")))
        l1UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࡥࡩࡪ࡯࡯ࡵ࠲ࠫ஌") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠪࡴࡷ࡫ࡶࡪࡱࡸࡷࡤ࡬࡯ࡤࡷࡶ࠲ࡵࡴࡧࠨ஍")))
        l1lll11UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴࠭எ") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠬࡶࡲࡦࡸ࡬ࡳࡺࡹ࠮ࡱࡰࡪࠫஏ")))
        l1ll1lllUK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࠨஐ") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡤ࡮ࡲࡷࡪࡥࡦࡰࡥࡸࡷ࠳ࡶ࡮ࡨࠩ஑")))
        l111l11lUK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࠪஒ") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠩࡦࡰࡴࡹࡥ࠯ࡲࡱ࡫ࠬஓ")))
        l11ll11l1UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠪࡷࡵ࡫ࡣࡪࡣ࡯࠾࠴࠵ࡨࡰ࡯ࡨ࠳ࡦࡪࡤࡰࡰࡶ࠳ࠬஔ") + addon_id + l1l1lll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠫࡲࡧࡩ࡯࠯ࡥ࡫࠶࠴ࡰ࡯ࡩࠪக")))
        window.setGeometry(1300, 720, 100, 50)
        background=pyxbmct.Image(l11ll11l1UK_Turk_No1)
        window.placeControl(background, -10, -10, 130, 70)
        text = l11l1lUK_Turk_No1 (u"ࠬ࠶ࡸࡇࡈ࠳࠴࠵࠶࠰࠱ࠩ஖")
	l1lllll1UK_Turk_No1 = pyxbmct.Button(l11l1lUK_Turk_No1 (u"࠭ࠧ஗"),focusTexture=l1UK_Turk_No1,noFocusTexture=l1lll11UK_Turk_No1,textColor=text,focusedColor=text)
	l1ll1ll1UK_Turk_No1 = pyxbmct.Button(l11l1lUK_Turk_No1 (u"ࠧࠨ஘"),focusTexture=l1lllUK_Turk_No1,noFocusTexture=l11l111UK_Turk_No1,textColor=text,focusedColor=text)
	l1llll11UK_Turk_No1 = pyxbmct.Button(l11l1lUK_Turk_No1 (u"ࠨࠩங"),focusTexture=l1ll1lllUK_Turk_No1,noFocusTexture=l111l11lUK_Turk_No1,textColor=text,focusedColor=text)
	l1111lUK_Turk_No1=pyxbmct.Image(images[0], aspectRatio=1)
	window.placeControl(l1lllll1UK_Turk_No1 ,102, 1,  10, 10)
	window.placeControl(l1ll1ll1UK_Turk_No1 ,102, 40, 10, 10)
	window.placeControl(l1llll11UK_Turk_No1 ,102, 21, 10, 10)
	window.placeControl(l1111lUK_Turk_No1, 0, 0, 100, 50)
	l1lllll1UK_Turk_No1.controlRight(l1ll1ll1UK_Turk_No1)
	l1lllll1UK_Turk_No1.controlUp(l1llll11UK_Turk_No1)
	window.connect(l1lllll1UK_Turk_No1,l1llllllUK_Turk_No1)
	window.connect(l1ll1ll1UK_Turk_No1,l1l1ll11lUK_Turk_No1)
	l1lllll1UK_Turk_No1.l111l111UK_Turk_No1(False)
        window.setFocus(l1llll11UK_Turk_No1)
        l1lllll1UK_Turk_No1.controlRight(l1llll11UK_Turk_No1)
        l1llll11UK_Turk_No1.controlLeft(l1lllll1UK_Turk_No1)
        l1llll11UK_Turk_No1.controlRight(l1ll1ll1UK_Turk_No1)
        l1ll1ll1UK_Turk_No1.controlLeft(l1llll11UK_Turk_No1)
	window.connect(l1llll11UK_Turk_No1, window.close)
	window.doModal()
	del window
def l1l1ll11lUK_Turk_No1():
        l1l1l1UK_Turk_No1=int(l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡳࡳࡸ࠭ச")))
        l11llllllUK_Turk_No1=int(l1l1l1UK_Turk_No1)+1
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡴࡴࡹࠧ஛"),str(l11llllllUK_Turk_No1))
        l1llllllllUK_Turk_No1=len(images)
        l1111lUK_Turk_No1.setImage(images[int(l11llllllUK_Turk_No1)])
        l1lllll1UK_Turk_No1.l111l111UK_Turk_No1(True)
        if int(l11llllllUK_Turk_No1) ==int(l1llllllllUK_Turk_No1)-1:
                l1ll1ll1UK_Turk_No1.l111l111UK_Turk_No1(False)
def l1llllllUK_Turk_No1():
        l1l1l1UK_Turk_No1=int(l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫࡵࡵࡳࠨஜ")))
        l11l1l1UK_Turk_No1=int(l1l1l1UK_Turk_No1)-1
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬࡶ࡯ࡴࠩ஝"),str(l11l1l1UK_Turk_No1))
        l1111lUK_Turk_No1.setImage(images[int(l11l1l1UK_Turk_No1)])
        l1ll1ll1UK_Turk_No1.l111l111UK_Turk_No1(True)
        if int(l11l1l1UK_Turk_No1) ==0:
                l1lllll1UK_Turk_No1.l111l111UK_Turk_No1(False)
def decode(s):
    l1llll11lUK_Turk_No1 = [ s[ i : i + 3] for i in range(0, len(s), 3) ]
    return l11l1lUK_Turk_No1 (u"࠭ࠧஞ").join( chr(int(val)) for val in l1llll11lUK_Turk_No1 )
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠢࠧࠥࡻࠦட"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧ஠"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨ஡"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠥࠬࡄ࡯ࠩࠧࠥ࡟ࡻ࠰ࡁࠢ஢"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠫࡎ࡙ࡏ࠮࠺࠻࠹࠾࠳࠱ࠨண")).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫத")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠨࠨࡀ࡫ࠬࠪࠨࡢࡷࠬ࠽ࠥ஥"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠢࡢࡵࡦ࡭࡮ࠨ஦"), l11l1lUK_Turk_No1 (u"ࠣ࡫ࡪࡲࡴࡸࡥࠣ஧")).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨந")))
def l111ll1l1UK_Turk_No1():
	if xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠪࡷࡾࡹࡴࡦ࡯࠱ࡴࡱࡧࡴࡧࡱࡵࡱ࠳ࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ன")):
		return l11l1lUK_Turk_No1 (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬப")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠬࡹࡹࡴࡶࡨࡱ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠮࡭࡫ࡱࡹࡽ࠭஫")):
		return l11l1lUK_Turk_No1 (u"࠭࡬ࡪࡰࡸࡼࠬ஬")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠧࡴࡻࡶࡸࡪࡳ࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠰ࡺ࡭ࡳࡪ࡯ࡸࡵࠪ஭")):
		return l11l1lUK_Turk_No1 (u"ࠨࡹ࡬ࡲࡩࡵࡷࡴࠩம")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠩࡶࡽࡸࡺࡥ࡮࠰ࡳࡰࡦࡺࡦࡰࡴࡰ࠲ࡴࡹࡸࠨய")):
		return l11l1lUK_Turk_No1 (u"ࠪࡳࡸࡾࠧர")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠫࡸࡿࡳࡵࡧࡰ࠲ࡵࡲࡡࡵࡨࡲࡶࡲ࠴ࡡࡵࡸ࠵ࠫற")):
		return l11l1lUK_Turk_No1 (u"ࠬࡧࡴࡷ࠴ࠪல")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"࠭ࡳࡺࡵࡷࡩࡲ࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠯࡫ࡲࡷࠬள")):
		return l11l1lUK_Turk_No1 (u"ࠧࡪࡱࡶࠫழ")
	else:
		return l11l1lUK_Turk_No1 (u"ࠨࡑࡷ࡬ࡪࡸࠧவ")
def l11llll1lUK_Turk_No1(url):
	request  = urllib2.Request(url)
	request.add_header(l11l1lUK_Turk_No1 (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ஶ"), USER_AGENT)
	response = urllib2.urlopen(request)
	link = response.read()
	response.close()
	return link
def l1ll1l1UK_Turk_No1():
	url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡪࡤࡰࡰࡦࡰࡴࡻࡤ࠯ࡱࡵ࡫࠴ࡶࡩ࡯࠰ࡳ࡬ࡵ࠭ஷ")
	l111ll11UK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠫࡸࡿࡳࡵࡧࡰ࠲ࡵࡲࡡࡵࡨࡲࡶࡲ࠴ࡷࡪࡰࡧࡳࡼࡹࠧஸ"))
	l1111l1UK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠬࡹࡹࡴࡶࡨࡱ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠮ࡰࡵࡻࠫஹ"))
	l1111llUK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"࠭ࡳࡺࡵࡷࡩࡲ࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠯࡮࡬ࡲࡺࡾࠧ஺"))
	l1l11l1lUK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠧࡔࡻࡶࡸࡪࡳ࠮ࡑ࡮ࡤࡸ࡫ࡵࡲ࡮࠰ࡄࡲࡩࡸ࡯ࡪࡦࠪ஻"))
	if l1111l1UK_Turk_No1:
		# _ l111111llUK_Turk_No1 the url with the default l11l111lUK_Turk_No1 browser
		xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠣࡕࡼࡷࡹ࡫࡭࠯ࡇࡻࡩࡨ࠮࡯ࡱࡧࡱࠤࠧ஼")+url+l11l1lUK_Turk_No1 (u"ࠤࠬࠦ஽"))
	elif l111ll11UK_Turk_No1:
		# _ l111111llUK_Turk_No1 the url with the default l11l111lUK_Turk_No1 browser
		xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠥࡗࡾࡹࡴࡦ࡯࠱ࡉࡽ࡫ࡣࠩࡥࡰࡨ࠳࡫ࡸࡦࠢ࠲ࡧࠥࡹࡴࡢࡴࡷࠤࠧா")+url+l11l1lUK_Turk_No1 (u"ࠦ࠮ࠨி"))
	elif l1l11l1lUK_Turk_No1:
		try:
			xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"࡙ࠧࡴࡢࡴࡷࡅࡳࡪࡲࡰ࡫ࡧࡅࡨࡺࡩࡷ࡫ࡷࡽ࠭ࡩ࡯࡮࠰ࡤࡲࡩࡸ࡯ࡪࡦ࠱ࡧ࡭ࡸ࡯࡮ࡧ࠯ࡥࡳࡪࡲࡰ࡫ࡧ࠲࡮ࡴࡴࡦࡰࡷ࠲ࡦࡩࡴࡪࡱࡱ࠲࡛ࡏࡅࡘ࠮࠯ࠦீ")+url+l11l1lUK_Turk_No1 (u"ࠨࠩࠣு"))
		except:
			xbmcgui.Dialog().ok( l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࠦࠧࠡࠢࠢࡄࡐࡊࡘࡔࠡࠣࠤࠥࠦࡡ࠯ࡄࡑࡏࡓࡗࡣࠧூ"),l11l1lUK_Turk_No1 (u"࡛ࠣࡲࡹࡷࠦࡤࡦࡸ࡬ࡧࡪࠦࡤࡰࡧࡶࡲࠬࡺࠠࡩࡣࡹࡩࠥࡧࠠࡣࡴࡲࡻࡸ࡫ࡲ࠯ࠢࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡥࠥࡨࡲࡰࡹࡶࡩࡷࠦࡴࡩࡧࡱࠤࡺࡹࡥࠡࡶ࡫࡭ࡸࠦࡡࡥࡦࡲࡲࠧ௃"))
def l111111lUK_Turk_No1(P):
	global l1l1llUK_Turk_No1
	global l1l111lUK_Turk_No1
	if P == l11l1lUK_Turk_No1 (u"ࠤࠥ௄") :
		l1lllllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠥ࡝ࡴࡻࠠࡏࡧࡨࡨࠥࡧࠠ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࡓࡍࡓࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠤࡹࡵࠠࡂࡥࡦࡩࡸࡹࠠࡖࡍࠣࡘࡺࡸ࡫ࡴࠣࠥ௅")
		msg2 = l11l1lUK_Turk_No1 (u"ࠦࡌࡵࠠࡵࡱࠣ࡟ࡈࡕࡌࡐࡔࠣࡦࡱࡻࡥ࡞࡝ࡅࡡ࡚࡚ࡐࡊࡐ࠱ࡇࡔࡓ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠥࡵ࡮ࠡࡻࡲࡹࡷࠦࡍࡰࡤ࡬ࡰࡪ࠵ࡐࡄࠢࡷࡳࠥ࡭ࡥࡵࠢࡼࡳࡺࡸࠠࡑࡋࡑࠤࡳࡻ࡭ࡣࡧࡵࠤࡹ࡮ࡥ࡯ࠢࡦࡰ࡮ࡩ࡫ࠡࡱࡱࠤࡾ࡫ࡳࠡࡶࡲࠤ࡮ࡴࡰࡶࡶࠣࡽࡴࡻࡲࠡࡲ࡬ࡲࠥࡵࡲࠡࡥ࡯࡭ࡨࡱࠠࡰࡰࠣࡒࡴࠦࡴࡰࠢࡨࡼ࡮ࡺࠢெ")
		if l1l1l111UK_Turk_No1.platform() == l11l1lUK_Turk_No1 (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ே"):
			yes = DIALOG.yesno(l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࠥࠦࡉࡨࡳࡱࡰࡩࠥࡈࡲࡰࡹࡶࡩࡷࠦࡒࡦࡳࡸ࡭ࡷ࡫ࡤࠢࠣ࡞࠳ࡈࡕࡌࡐࡔࡠࠫை"), l11l1lUK_Turk_No1 (u"ࠢࡊࡨࠣࡽࡴࡻࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡪࡤࡺࡪࠦࡃࡩࡴࡲࡱࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠢࡷ࡬ࡪࡴࠠࡤ࡮࡬ࡧࡰ࡛ࠦࡄࡑࡏࡓࡗࠦࡧࡳࡧࡨࡲࡢࡉ࡯࡯ࡶ࡬ࡲࡺ࡫࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣ௉"), l11l1lUK_Turk_No1 (u"ࠣࡆࡲࡲࠬࡺࠠࡩࡣࡹࡩࠥࡉࡨࡳࡱࡰࡩࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࡀࠢࡦࡰ࡮ࡩ࡫ࠡ࡝ࡆࡓࡑࡕࡒࠡࡥࡼࡥࡳࡣࡄࡰࡹࡱࡰࡴࡧࡤ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤொ"), yeslabel=l11l1lUK_Turk_No1 (u"ࠤ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡩࡹࡢࡰࡠࡈࡴࡽ࡮࡭ࡱࡤࡨࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠥோ"), nolabel=l11l1lUK_Turk_No1 (u"ࠥ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡧࡳࡧࡨࡲࡢࡉ࡯࡯ࡶ࡬ࡲࡺ࡫࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠧௌ"))
			if yes:
				apkInstaller(l11l1lUK_Turk_No1 (u"ࠫࡨ࡮ࡲࡰ࡯ࡨ்ࠫ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡥࡦࡲࡲࡨࡲ࡯ࡶࡦ࠱ࡳࡷ࡭࠯ࡶ࡭ࡷࡹࡷࡱ࠯ࡧ࡫࡯ࡩࡸ࠵ࡣࡩࡴࡲࡱࡪࡥࡶ࠷࠳࠱࠴࠳࠹࠱࠷࠵࠱࠽࠽࠴ࡡࡱ࡭ࠪ௎"))
			else:
				pass
		yes_pressed = plugintools.message_yes_no(l1lllllllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠨࠠࠡࡒ࡬ࡲࠥࡇࡣࡤࡧࡶࡷ࡙ࠥࡹࡴࡶࡨࡱࠧ௏"), l1lllllUK_Turk_No1, msg2)
		if yes_pressed:
			l1ll1l1UK_Turk_No1()
			l1ll111llUK_Turk_No1()
		else:
			sys.exit()
	else:
		link  = l11llll1lUK_Turk_No1(l1111ll1lUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠧࡀࡲ࡬ࡲࡂ࠭ௐ") + plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠨࡲ࡬ࡲࠬ௑")) ).replace(l11l1lUK_Turk_No1 (u"ࠩ࡟ࡲࠬ௒"), l11l1lUK_Turk_No1 (u"ࠪࠫ௓")).replace(l11l1lUK_Turk_No1 (u"ࠫࡡࡸࠧ௔"), l11l1lUK_Turk_No1 (u"ࠬ࠭௕"))
		total = re.compile(l11l1lUK_Turk_No1 (u"࠭ࡩ࡯ࡵࡷࡥࡱࡲ࠽ࠣࠪ࡟ࡨ࠮ࠨࠧ௖")).findall(link)
		try:
			if (str(total[0]) == l11l1lUK_Turk_No1 (u"ࠧ࠲ࠩௗ")):
				pass
		except:
			l1lllllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡓࡍࡓ࠲ࠢ௘")
			msg2 = l11l1lUK_Turk_No1 (u"ࠤࡓࡶࡪࡹࡳࠡࡻࡨࡷࠥࡺ࡯ࠡࡧࡱࡸࡪࡸࠠࡑࡋࡑࠤࡦ࡭ࡡࡪࡰࠣࡳࡷࠦࡎࡰࠢࡷࡳࠥ࡫ࡸࡪࡶ࠱ࠦ௙")
			yes_pressed = plugintools.message_yes_no(l1lllllllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠥࠤࠥࡖࡩ࡯ࠢࡄࡧࡨ࡫ࡳࡴࠢࡖࡽࡸࡺࡥ࡮ࠤ௚"), l1lllllUK_Turk_No1, msg2)
			if yes_pressed:
				l1ll1l1UK_Turk_No1()
				l1ll111llUK_Turk_No1()
			else:
				sys.exit()
def l1ll111llUK_Turk_No1():
	l1l111l11UK_Turk_No1()
	global P
	P = plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠫࡵ࡯࡮ࠨ௛"))
	l111111lUK_Turk_No1(P)
def l1l111l11UK_Turk_No1():
	try:
		l1l1llUK_Turk_No1 = l1lll1llUK_Turk_No1()
		if l1l1llUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠧࠨ௜"):
			plugintools.message(l1lllllllUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠨ࡙ࡰࡷࡵࠤࡵ࡯࡮ࠡࡥࡤࡲࡳࡵࡴࠡࡤࡨࠤࡪࡳࡰࡵࡻࠥ௝"))
			l1l111l11UK_Turk_No1()
		else:
			plugintools.set_setting(l11l1lUK_Turk_No1 (u"ࠢࡱ࡫ࡱࠦ௞"), l1l1llUK_Turk_No1)
			return
	except:
		l1l111l11UK_Turk_No1()
def l1lll1llUK_Turk_No1():
        l1lll111lUK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠨࠩ௟"), l11l1lUK_Turk_No1 (u"ࠩࡓࡰࡪࡧࡳࡦࠢࡨࡲࡹ࡫ࡲࠡࡻࡲࡹࡷࠦࡰࡪࡰࠣ࡬ࡪࡸࡥࠨ௠"))
        l1lll111lUK_Turk_No1.doModal()
        if (l1lll111lUK_Turk_No1.isConfirmed()):
            l1l1UK_Turk_No1 = l1lll111lUK_Turk_No1.getText()
            l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡴ࡮ࡴࠧ௡"),l1l1UK_Turk_No1)
        return l1l1UK_Turk_No1
def l1l1l111lUK_Turk_No1(content, l1111111lUK_Turk_No1,link):
	try:
		if (content):
			xbmcplugin.setContent(int(sys.argv[1]), content)
		if (l11l1l1llUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫࡦࡻࡴࡰ࠯ࡹ࡭ࡪࡽࠧ௢")) == l11l1lUK_Turk_No1 (u"ࠬࡺࡲࡶࡧࠪ௣")):
			xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"࠭ࡃࡰࡰࡷࡥ࡮ࡴࡥࡳ࠰ࡖࡩࡹ࡜ࡩࡦࡹࡐࡳࡩ࡫ࠨࠦࡵࠬࠫ௤") % l11l1l1llUK_Turk_No1.getSetting(l1111111lUK_Turk_No1))
	except:pass
if ((mode == None) or (url == None) or len(url) < 1):
	l111111lUK_Turk_No1(P)
	l11ll1lllUK_Turk_No1()
elif mode==1:l1lll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1,fanart)
elif mode==2:l1ll1l1l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==3:l1ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==4:l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==5:l1l1l1l1UK_Turk_No1()
elif mode==6:l1ll11ll1UK_Turk_No1(url,l1l11l11UK_Turk_No1)
elif mode==7:l1ll11llUK_Turk_No1(url)
elif mode==8:l11l1llllUK_Turk_No1(name)
elif mode==9:l11l1lllUK_Turk_No1(name,url)
elif mode==10:l1lll11lUK_Turk_No1(name,url)
elif mode==11:l111ll1lUK_Turk_No1(url)
elif mode==12:l1111l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==13:l1llll1UK_Turk_No1(url)
elif mode==14:l11l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==15:l11l1l1l1UK_Turk_No1(url)
elif mode==16:l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==17:l111lll1UK_Turk_No1(name,url)
elif mode==18:l11111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==19:l111l11l1UK_Turk_No1(name,url)
elif mode==20:l1lllll11UK_Turk_No1(url,l1l11l11UK_Turk_No1)
elif mode==21:l1ll1111UK_Turk_No1(url)
elif mode==22:l11111lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==23:l1l1ll1l1UK_Turk_No1(url)
elif mode==24:l1l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==25:l1ll1l111UK_Turk_No1(url)
elif mode==26:l11llll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==27:l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==28:l11ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==29:l1ll1lll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==30:l1lll11llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==31:l1lllllll1UK_Turk_No1()
elif mode==32:l111l1l1lUK_Turk_No1()
elif mode==33:l1l1l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==34:l1ll11111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==35:l11ll11lUK_Turk_No1(url)
elif mode==36:l11ll111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==37:l1ll111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==38:l1l111111UK_Turk_No1()
elif mode==39:l1l1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==40:l111llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==41:l111l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==42:l1l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==43:l1111l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==44:l1111l11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==45:l1ll1lUK_Turk_No1()
elif mode==46:l11llllUK_Turk_No1(url)
elif mode==47:l11lll1l1UK_Turk_No1(name,url)
elif mode==48:l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==49:l111lllllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==50:l1llllll1UK_Turk_No1(url)
elif mode==51:l11ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==52:l1ll11lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==53:l1l1ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==54:llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
xbmcplugin.endOfDirectory(int(sys.argv[1]))