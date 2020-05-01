import re
import json
from xbmcswift2 import xbmc, xbmcgui, xbmcvfs
from meta import plugin
from meta.gui import dialogs
from meta.utils.text import to_unicode
from settings import SETTING_AUTOPATCH, SETTING_AUTOPATCHES
from language import get_string as _

EXTENSION = ".metalliq.json"
HTML_TAGS_REGEX = re.compile(r'\[/?(?:color|b|i|u).*?\]', re.I|re.UNICODE)

class AddonPlayer(object):
    def __init__(self, filename, media, meta):
        self.media = media
        self.title = meta["name"]
        self.id = meta.get("id", filename.replace(".metalliq.json", ""))
        self.clean_title = HTML_TAGS_REGEX.sub('', self.title)
        self.repoid = meta.get("repository")
        self.pluginid = meta.get("plugin")
        self.order = meta.get("priority") or 1000
        self.filters = meta.get("filters", {})
        self.commands = meta.get(media, [])
        self._postprocess = meta.get("postprocess")

    def postprocess(self, link):
        code = self._postprocess
        if not code or not isinstance(code, basestring) or "__" in code:
            return link
        link = eval(code, {"__builtins__": {}, "link": link})        
        return link

    def is_empty(self):
        if self.pluginid and not xbmc.getCondVisibility('System.HasAddon(%s)' % self.pluginid):
            return True
        return not bool(self.commands)

def get_players(media, filters = {}):
    assert media in ("tvshows", "movies", "musicvideos", "music", "live")
    players = []
    players_path = "special://profile/addon_data/{0}/players/".format(plugin.id)
    files = [x for x in xbmcvfs.listdir(players_path)[1] if x.endswith(EXTENSION)]
    for file in files:
        path = players_path + file
        try:
            f = xbmcvfs.File(path)
            try:
                content = f.read()
                meta = json.loads(content)
            finally:
                f.close()
            player = AddonPlayer(file, media, meta)
            if not player.is_empty():
                players.append(player)
        except Exception, e:
            plugin.log.error(repr(e))
            msg = "player %s is invalid" % file
            xbmcgui.Dialog().ok('Invalid player', msg)
            raise
    return sort_players(players, filters)

def sort_players(players, filters = {}):
    result = []
    for player in players:
        filtered = False
        checked = False
        for filter_key, filter_value in filters.items():    
            value = player.filters.get(filter_key)
            if value:
                checked = True
                if to_unicode(value) != to_unicode(filter_value):
                    filtered = True
        if not filtered:
            needs_browsing = False
            for command_group in player.commands:
                for command in command_group:
                    if command.get('steps'):
                        needs_browsing = True
                        break
            result.append((not checked, needs_browsing, player.order, player.clean_title.lower(), player))
    result.sort()
    return [x[-1] for x in result]

def get_needed_langs(players):
    languages = set()
    for player in players:
        for command_group in player.commands:  
            for command in command_group:
                command_lang = command.get("language", "en")
                languages.add(command_lang)
    return languages

ADDON_SELECTOR = AddonPlayer("selector", "any", meta={"name": "Selector"})
ADDON_CONTEXT = AddonPlayer("context", "any", meta={"name": "Context"})
ADDON_DEFAULT = AddonPlayer("default", "any", meta={"name": "Default"})

@plugin.route('/patch/<mode>', options = {"mode": "all"})
def patch(mode):
    import xbmcaddon
    adir = "special://home/addons/"
    AUTOS = eval(plugin.get_setting(SETTING_AUTOPATCHES, unicode))
#    try: AUTOS = plugin.get_setting(SETTING_AUTOPATCHES, unicode)
#    except: AUTOS = [[], [], [], []]
#    return [p for p in get_players() if p.id in AUTOS]
#    xbmc.log("QQQQQ AUTOS = {0}".format(str(AUTOS)), xbmc.LOGNOTICE)
    INSTALLED = [i for i in xbmcvfs.listdir(adir)[0]]
    PATCHES = [[], ["resources/lib/modules/control.py", "pass", "sys.exit()"], ["default.py", "", "\n    cool_down_active = kodi.get_setting('cool_down') == 'true'\n    if not salts_utils.is_salts() or cool_down_active:\n        kodi.notify(msg=i18n('playback_limited'))\n        return False"], ["lib/dudehere/routines/scrapers/__init__.py", "", "\n\t\tif self._caller not in ALLOWED_CALLERS and self._caller: \n\t\t\tplugin.log('Caller not allowed')\n\t\t\tplugin.raise_error('Violation', 'This addon is not allowed.', 'Please do not use %s with %s' % (self._caller, ADDON_NAME))\n\t\t\tif return_sources:\n\t\t\t\treturn [], [], []\n\t\t\telse:\n\t\t\t\treturn []"]]
    if mode == "auto":
        if AUTOS != [[], [], [], []]:
            ADDONS = AUTOS
        else:
            if dialogs.yesno('{0}: Patch'.format(plugin.name), '{0}.[CR]{1} & {2}'.format(_("%s not found") % 'Auto-patches', _("Enable"), _("Continue?"))): return patch("all")
            else:
                plugin.set_setting(SETTING_AUTOPATCH, "false")
                return
    else:
        ADDONS = [[], [i for i in INSTALLED if i.startswith("plugin.video.") and xbmcvfs.exists("{0}{1}/{2}".format(adir, i, PATCHES[1][0]))], [i for i in INSTALLED if i.startswith("plugin.video.") and xbmcvfs.exists("{0}{1}/{2}".format(adir, i, PATCHES[2][0]))], [i for i in INSTALLED if i.startswith("script.module.") and xbmcvfs.exists("{0}{1}/{2}".format(adir, i, PATCHES[3][0]))]]
    count = 0
    for i in range(1, len(ADDONS)):
        for a in ADDONS[i]:
            count = count + 1
            b = "{0}{1}/{2}".format(adir, a, PATCHES[i][0])
            c = xbmcvfs.File(b)
            d = c.read()
            c.close()
            if PATCHES[i][2] in d:
                ADDON = xbmcaddon.Addon(a)
                if mode == "auto" or dialogs.yesno('{0}: Patch "{1}"?'.format(plugin.name, ADDON.getAddonInfo("name")), '"{0}" {1} block-code.[CR]{2}'.format(ADDON.getAddonInfo("name"), _("contains"), _("Would you like to remove it from the library?").replace(_("Library").lower(), _("Add-on").lower()))):
                    h = xbmcvfs.File(b, 'w')
                    d = d.replace(PATCHES[i][2], PATCHES[i][1])
                    result = h.write(d)
                    h.close()
                    if mode != "auto" and dialogs.yesno("{0}: {1} Patch?".format(plugin.name, _("Auto")), '"{0}"[CR]{1} {2} re-patching?'.format(ADDON.getAddonInfo("name"), _("Enable"), _("Auto").lower())):
                        if ADDON.getAddonInfo("id") not in AUTOS[i]: AUTOS[i].append(ADDON.getAddonInfo("id"))
    if AUTOS != [[], [], [], []] and AUTOS != ADDONS:
        plugin.set_setting(SETTING_AUTOPATCHES, AUTOS)