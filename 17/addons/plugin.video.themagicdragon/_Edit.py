import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RvbWJlYmJzMS9tYWdpY2RyYWdvbi9tYXN0ZXIvaG9tZS50eHQ='))
addon = xbmcaddon.Addon('plugin.video.themagicdragon')