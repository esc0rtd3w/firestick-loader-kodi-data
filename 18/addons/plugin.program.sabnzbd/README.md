SABnzbd
=========
SABnzbd is an Open Source Binary Newsreader written in Python. This is the XBMC addon for managing SABnzbd.
This is a continuation of the first SABnzbd addon made by "Kricker" in the XBMC.org forum.
The code is re-written from scratch by  "Popeye".
It uses [SABnzbd](http://www.sabnzbd.org) as backbone.

API
===

SABnzbd has a set of API's for other add-on's to use. 

BASE
----
plugin://plugin.program.sabnzbd/

?mode=sab_action
--------
Any parameter prefixed by sab_ will be sent straight to sabnzbd using connection
settings by the addon.
Example using the sabnzbd api for adding a nzb url:
"api?mode=addurl&name=http://www.example.com/example.nzb&nzbname=NiceName"
can be called by 
?mode=sab_action&sab_mode=addurl&sab_name=http://www.example.com/example.nzb&sab_nzbname=NiceName
