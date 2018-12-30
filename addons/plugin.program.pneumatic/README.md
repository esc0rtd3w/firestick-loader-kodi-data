Pneumatic
=========
Pneumatic is a NZB engine add-on for [XBMC](http://www.xbmc.org) Eden.
It uses [SABnzbd](http://www.sabnzbd.org) as backbone.

API
===

Pneumatic has a set of API's for other add-on's to use.

BASE
----
plugin://plugin.program.pneumatic/

PLAY
----
?mode=play&nzb=[url.encoded.nzb.http.path]&nzbname=[url.encoded.output.name]

DOWNLOAD
--------
?mode=download&nzb=[url.encoded.nzb.http.path]&nzbname=[url.encoded.output.name]

INCOMPLETE
----------
?mode=incomplete

SAVE .STRM
----------
?mode=save_strm&nzb=[url.encoded.nzb.http.path]&nzbname=[url.encoded.output.name]

STRM
----
?mode=strm&nzb=[url.encoded.nzb.http.path]&nzbname=[url.encoded.output.name]