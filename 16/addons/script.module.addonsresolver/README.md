Instructions how to interact this addon with others.<p>

To import the addon:<br>
import addonsresolver
<p>
Add a entry to setup the addon in your own:<br>
import xbmc<br>
xbmc.executebuiltin('Addon.OpenSettings('script.module.addonsresolver')<br>
<p>
Function to call:<br>
addonsresolver.custom_choice(originalname,url,imdb_id,year)<br>
<p>
Parameters:<br>
originalname -> Original Name of movie<br>
imdb_id -> imdb ID<br>
year -> Release Year of movie<br>
url -> still optional, should be sent as '' if not used.<br>
<p>
Working with:<br>
Portuguese addons:<br>
- Wareztuga;<br>
- RatoTV;<br>
- Sites_dos_Portugas.<br>
International addons:<br>
- Genesis;<br>
- KmediaTorrent;<br>
- Stream.<br>
