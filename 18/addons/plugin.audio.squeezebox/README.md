# plugin.audio.squeezebox
Squeezelite player for Kodi

________________________________________________________________________________________________________


Transform Kodi in a Squeezebox player with this addon.
It started as something for my own personal use but I figured with a few additional touches it can be usefull to others too.

Altough Logitech stopped producing the Squeezeboxes several years ago, the platform is still very popular and in active development by the opensource community.

Sure, systems like Sonos and Heos might be superior in ease of use but they're also (in my opinion) very expensive.
I wanted to have a way to have multi-room music with an ocassional need of syncing audio between players using my existing components such as Kodi Intel NUC's and raspberry pi's, including support of my Hi-Def audio tracks on disk and my Spotify playlists.

The Squeezebox setup with the Logitech Media Server is perfectly capable of doing all that, including support for a wide range of other devices in the mix such as Airplay devices. You can have a combination of original squeezeboxes, pc's with Squeezelite (software player for Squeezebox), Airplay devices and even Chromecast devices and let them all play your favorite tunes. There are even some nice projects available to turn a Raspberry Pi into a squeezebox like PiCoreAudio and Max2Play.

For all additional rooms such as kitchen, outside and my office, I use headless Pi's with PiCoreAudio connected to some actve speakers.

Offcourse in the living room and bedroom I have Kodi running as my all-in-one media solution and I didn't want to add another box in there just to play audio.

That's where Squeezelite comes in play, a nice piece of software that you can install on about any platform to make it play the sounds from the Squeezebox server (Logitech Media Server).

Squeezelite on it's own does it's job very great and you can install it side to side with Kodi on your setup but I was missing the interaction with kodi. Especially the "Now Playing" screen so I can watch some artwork and artist info while track are playing. That's when I decided to create something to fill that gap so I could have the benefits of the centralized audio control of LMS combined with the great Kodi software.

I realize there's already an addon for Kodi, named Xsqueeze but it's rather outdated and it's based on custom dialogs which is something I didn't want (personal taste, the Xsqueeze addon is other than that great software offcourse).

**So, how does this work ?**
At first I tried to feed Kodi with the audiostream directly from the Squeezeserver by using the Squeezelite source but I finally gave up on that as I couldn't get it stable enough, especially when sync comes in play. Offcourse doable maybe somewhere in the future but it will require a fair amount of work and tight integration into the Kodi source code.

To have something ready sooner I had the idea to just "trick" Kodi that it's playing something and instead use the default, well known and well working Squeezelite software to handle the playback directly to the sound device. 

And that is exactly what this add-on does, it feeds Kodi with a 100% silent PCM audio stream so that the "Now Playing" screen will show up whenever Squeezelite is pumping audio to the speakers. It's basically just one big workaround but it works pretty great. As soon as you start Kodi, this addon will auto start Squeezelite in the background and it will poll the server for changes every second. Everything is supported like playlist handling, skipping tracks, pause, stop, syncing etc.

**Features**
- Auto start Squeezelite in the background (can be disabled in the addon settings if you start squeezelite yourself, for example on Max2Play devices).
- Registers as a sqeezeplayer in the LMS server with the MAC address that is reported by Kodi.
- Auto detects the LMS server in the network and connects to the first instance it finds.
- Auto detects the default (ALSA) sound device and use that for audio playback.
- Plugin entry (audio addon) to browse your media on the LMS server, including apps like Spotify etc.
- Because the plugin entry you can use native Kodi library windows to navigate your media, including creation of widgets etc.
- Supports Windows, MacOS, Linux x86/x64, Libreelec (possibly also Raspbmc but I didn't test it)
- Supports Android if you install a Squeezebox player app (like SB Player)
- Supports iOS if you install a Squeezebox player app (like iPeng)
- Primary acts as both a player and a controller but can also be set to acts as controlled for another player. In that case set the addon settings to not start squeezelite and configure the Mac address manually. This is also used on Android where SB Player (or other) is actually playing the audio.

**Instructions / Notes**
- Install this add-on from my Kodi addon repository, that way all dependencies will be installed and you will get updates instantly. Please do not install directly from Github if you want to ask support on the forums.
- Libreelec users: Make sure you have the mediatools addon installed as that includes Squeezelite !
- You need to have a LMS Server on your network, for example installed on your NAS.
- This addon only utilizes the more recent Json API of LMS-Server, the older telnet API is not used, so you need a recent version of the LMS server. I've tested it with LMS server version 7.9 myself.
- Make sure the LMS server doesn't require authentication for internal connections. I did not yet implement support for authentication.

I have tested the addon on Windows, MacOS and libreelec running on a Pi.
Remember, this considered beta software. Altough I spent a fair amount of optimizing it and it works in my scenario, bugs can happen. In that case, or if you have a request to improve it, feel free to let me know on the forums. In case of asking for support when an issue arrises, please include as much info as possible about your setup including the error message in the Kodi log or the entire Kodi logfile itself. Also, Pull requests on Github to optimize the addon are always welcome, feel free to contribute!


I hope this addon brings some joy to others too, have fun!


Was my spare time usefull to you and you can spare a few bucks, consider buying me a beer with a small donation:
http://goo.gl/Zsniiz
Thanks!

**To install, grab the addon from my Kodi repository:**
https://github.com/marcelveldt/repository.marcelveldt/raw/master/repository.marcelveldt/repository.marcelveldt-1.0.1.zip


**Supportthread on kodi forums:**
http://forum.kodi.tv/showthread.php?tid=313912

