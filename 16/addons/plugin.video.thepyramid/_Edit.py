import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cDovL3B5cmFtaWQuemVyb3RvbGVyYW5jZS5ncS9weXJhbWlkL2hvbWUudHh0'))
addon = xbmcaddon.Addon('plugin.video.thepyramid')