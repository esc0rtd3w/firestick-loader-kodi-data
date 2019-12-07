"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


    Overview:

        Drop this PY in the plugins folder, and set up the colors below.
        Default colors for each selection is the first in the list, so this means they all are the same.

    Version:
        2018.5.2
            - Updated color chart.

        2018.5.1
            - Updated xml processing so can both colorize and process color selection on same item
            - Added force container refresh after color selection

    XML Explanations:
        Tags: 
            <colorselect></colorselect> - Use this tag to select the color for specific types.
            <colorit></colorit> - Use this tag to colorize the Title using the given color variable.
            <colorize></colorize> - This is not used in XML files, but set by the plugin to mark an item as "Colorized".

        Color Variables: These are used to store the chosen colors, and can be recalled in the XML tags as described above.
            In the usage examples, we give examples for the color variables listed below. These are NOT hardcoded, and you
            can have as many custom color variables as you want. By adding a new variable via the colorselect tag, it saves
            it to the Settings for your plugin and can then be accessed by the colorit tag to specify the colors.

            If the a colorit tag tries to use a color variable that has not been set, it will default to the first color in
            the COLOR_CHART. 

            You can call the Select Dialog for multiple colors with a single colorselect entry by separating each with a /.

            Example variables listed in the Usage Examples below:
                title_color_1
                title_color_2
                header_color_1
                header_color_2

    Usage Examples:

        <item>
            <title>Select Title Color 1</title>
            <colorselect>title_color_1</colorselect>
        </item>

        <item>
            <title>Select Title Color 2</title>
            <colorselect>title_color_2</colorselect>
        </item>

        <item>
            <title>Select Title Colors</title>
            <colorselect>title_color_1/title_color_2</colorselect>
        </item>

        <item>
            <title>Select Header Color 1</title>
            <colorselect>header_color_1</colorselect>
        </item>

        <item>
            <title>Select Header Color 2</title>
            <colorselect>header_color_2</colorselect>
        </item>

        <item>
            <title>Select Header Colors</title>
            <colorselect>header_color_1/header_color_2</colorselect>
        </item>

        <item>
            <title>Regular Item</title>
            <colorit>title_color_1</colorit>
        </item>



"""

import collections,requests,re,os,traceback
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

COLOR_CHART = [ ("antiquewhite", "faebd7"),
        ("aqua", "00ffff"),
        ("aquamarine", "7fffd4"),
        ("azure", "f0ffff"),
        ("beige", "f5f5dc"),
        ("bisque", "ffe4c4"),
        ("black", "000000"),
        ("blanchedalmond", "ffebcd"),
        ("blue", "0000ff"),
        ("blueviolet", "8a2be2"),
        ("brown", "a52a2a"),
        ("burlywood", "deb887"),
        ("cadetblue", "5f9ea0"),
        ("chartreuse", "7fff00"),
        ("chocolate", "d2691e"),
        ("coral", "ff7f50"),
        ("cornflowerblue", "6495ed"),
        ("cornsilk", "fff8dc"),
        ("crimson", "dc143c"),
        ("cyan", "00ffff"),
        ("darkblue", "00008b"),
        ("darkcyan", "008b8b"),
        ("darkgoldenrod", "b8860b"),
        ("darkgreen", "006400"),
        ("darkgrey", "434343"),
        ("darkkhaki", "bdb76b"),
        ("darkmagenta", "8b008b"),
        ("darkolivegreen", "556b2f"),
        ("darkorange", "ff8c00"),
        ("darkorchid", "9932cc"),
        ("darkred", "8b0000"),
        ("darksalmon", "e9967a"),
        ("darkseagreen", "8fbc8f"),
        ("darkslateblue", "483d8b"),
        ("darkslategray", "2f4f4f"),
        ("darkslategrey", "2f4f4f"),
        ("darkturquoise", "00ced1"),
        ("darkviolet", "9400d3"),
        ("deeppink", "ff1493"),
        ("deepskyblue", "00bfff"),
        ("dimgray", "696969"),
        ("dimgrey", "696969"),
        ("dodgerblue", "1e90ff"),
        ("firebrick", "b22222"),
        ("floralwhite", "fffaf0"),
        ("forestgreen", "228b22"),
        ("fuchsia", "ff00ff"),
        ("ghostwhite", "f8f8ff"),
        ("gold", "ffd700"),
        ("goldenrod", "daa520"),
        ("gray", "808080"),
        ("green", "008000"),
        ("greenyellow", "adff2f"),
        ("grey", "808080"),
        ("honeydew", "f0fff0"),
        ("hotpink", "ff69b4"),
        ("indianred", "cd5c5c"),
        ("indigo", "4b0082"),
        ("ivory", "fffff0"),
        ("khaki", "f0e68c"),
        ("lawngreen", "7cfc00"),
        ("lemonchiffon", "fffacd"),
        ("lightblue", "add8e6"),
        ("lightcoral", "f08080"),
        ("lightcyan", "e0ffff"),
        ("lightgoldenrodyellow", "fafad2"),
        ("lightgray", "d3d3d3"),
        ("lightgreen", "90ee90"),
        ("lightgrey", "d3d3d3"),
        ("lightpink", "ffb6c1"),
        ("lightsalmon", "ffa07a"),
        ("lightseagreen", "20b2aa"),
        ("lightskyblue", "87cefa"),
        ("lightslategray", "778899"),
        ("lightslategrey", "778899"),
        ("lightsteelblue", "b0c4de"),
        ("lightyellow", "ffffe0"),
        ("lime", "00ff00"),
        ("limegreen", "32cd32"),
        ("magenta", "ff00ff"),
        ("maroon", "800000"),
        ("mediumaquamarine", "66cdaa"),
        ("mediumblue", "0000cd"),
        ("mediumorchid", "ba55d3"),
        ("mediumpurple", "9370db"),
        ("mediumseagreen", "3cb371"),
        ("mediumslateblue", "7b68ee"),
        ("mediumspringgreen", "00fa9a"),
        ("mediumturquoise", "48d1cc"),
        ("mediumvioletred", "c71585"),
        ("midnightblue", "191970"),
        ("mistyrose", "ffe4e1"),
        ("moccasin", "ffe4b5"),
        ("navajowhite", "ffdead"),
        ("navy", "000080"),
        ("olive", "808000"),
        ("olivedrab", "6b8e23"),
        ("orange", "ffa500"),
        ("orangered", "ff4500"),
        ("orchid", "da70d6"),
        ("palegoldenrod", "eee8aa"),
        ("palegreen", "98fb98"),
        ("paleturquoise", "afeeee"),
        ("palevioletred", "db7093"),
        ("papayawhip", "ffefd5"),
        ("peachpuff", "ffdab9"),
        ("peru", "cd853f"),
        ("pink", "ffc0cb"),
        ("plum", "dda0dd"),
        ("powderblue", "b0e0e6"),
        ("purple", "800080"),
        ("red", "ff0000"),
        ("rosybrown", "bc8f8f"),
        ("royalblue", "4169e1"),
        ("saddlebrown", "8b4513"),
        ("salmon", "fa8072"),
        ("sandybrown", "f4a460"),
        ("seagreen", "2e8b57"),
        ("seashell", "fff5ee"),
        ("sienna", "a0522d"),
        ("silver", "c0c0c0"),
        ("skyblue", "87ceeb"),
        ("slateblue", "6a5acd"),
        ("slategray", "708090"),
        ("slategrey", "708090"),
        ("snow", "fffafa"),
        ("springgreen", "00ff7f"),
        ("steelblue", "4682b4"),
        ("tan", "d2b48c"),
        ("teal", "008080"),
        ("thistle", "d8bfd8"),
        ("tomato", "ff6347"),
        ("turquoise", "40e0d0"),
        ("violet", "ee82ee"),
        ("wheat", "f5deb3"),
        ("white", "ffffff"),
        ("yellow", "ffff00"),
        ("yellowgreen", "9acd32") ]
COLOR_CHART = collections.OrderedDict(COLOR_CHART)

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')

class JenColorize(Plugin):
    name = "colorize"
    priority = 200

    def process_item(self, item_xml):
        if "<colorize>" not in item_xml:
            item = JenItem(item_xml)
            colorit = item.get("colorit", "")
            the_setting = xbmcaddon.Addon().getSetting('%s' % (colorit))
            if the_setting == None or the_setting == '':
                the_setting = 'white'
                xbmcaddon.Addon().setSetting('%s' % (colorit), str(the_setting))
            color = COLOR_CHART[the_setting]
            if "<name>" in item_xml:
                item_xml = item_xml.replace("<name>", "<name>[COLOR FFff%s]" % color, 1)
                item_xml = item_xml.replace("</name>", "[/COLOR]</name>", 1)
            else:
                item_xml = item_xml.replace("<title>", "<title>[COLOR FFff%s]" % color, 1)
                item_xml = item_xml.replace("</title>", "[/COLOR]</title>", 1)
            item_xml += "<colorize></colorize>"
            return JenList(item_xml).process_item(item_xml)
        if "<colorselect>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "COLORSELECT",
                'url': item.get("colorselect", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item


@route(mode='COLORSELECT', args=["url"])
def selectmy_color(url):
    try:
        vars = url.split('/')
        names = []
        for item in COLOR_CHART:
            names.append('[COLOR FFff%s]%s[/COLOR]'%(COLOR_CHART[item],item))

        count = 0
        for entry in vars:
            count += 1
            the_setting = xbmcaddon.Addon().getSetting('%s' % (entry))
            if the_setting == None or the_setting == '':
                the_setting = 'white'
                xbmcaddon.Addon().setSetting('%s' % (entry), str(the_setting))

            selected = xbmcgui.Dialog().select('Select Color %s of %s' % (str(count),str(len(vars))), names)
            chart_item = re.sub('\[.*?]','',names[selected])
            xbmcaddon.Addon().setSetting('%s' % (entry), chart_item)
        xbmc.executebuiltin('Container.Refresh')
    except:
        pass