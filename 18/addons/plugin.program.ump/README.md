UMP: UNIVERSAL MEDIA PROVIDER
=============================

WHAT IS UMP:
------------



**UMP** is a KODI/XBMC plugin provides latest **movies,series,animes,mangas** and **music** in specific. It actually is a generic framework that can provide internet media in all kodi forms with a scalable methodology.

Once it is installed you can acces the plugin either from movies, music or images. The basic principle of it is to index your media through a globally accepted website (ie: imdb for movies) and then search your media in a link provider (ie: primewire for movies), and the then decompile this link and make a kodi playable media (ie:flv,mp4 for movies).

HOW TO INSTALL:
---------------

Dowload Boogie's repo below
[Boogie's Kodi Repo](https://raw.githubusercontent.com/huseyinbiyik/repository.boogie.dist/master/repository.boogie/repository.boogie-0.0.2.zip) 

and navigate to:
System > Settings > Add-ons > Install from Zip File on kodi and select the zip file you downloaded. When the menu pops up select install from the options.

Once the Boogie's repo is installed navigate to:

System > Settings > Add-ons > Get Add-ons > Boogie's Kodi Repo > Videos/Music/Picture (Any of them is ok) > **Universal Media Provider**. When the menu pops up select install from the options.

That's all!, whenever there is a new version your Kodi will update the add-on automatically.

**Manual install:**

This is not very much advised but if you want to install specific version of UMP navigate to TAGS section on github and download the zipball. From kodi select install from zip file:

Caution, when you apply manual install from zipfile, after uninstall you may need to remove kodi/userdata/addon*.db, otherwise it may cause auto update issues for UMP.


HOW IS UMP DIFFERENT?
---------------------

**SCALABLE:** Eeach provider is independently maintained and developed with only UMP API dependancy. Since API has the very most necessary tools to scrape and provide the media, each provider is easy to develop, fast to run, reliable to watch.

**MEDIA VALIDATION:** The other cool stuff in UMP is the media validation. The link providers are generally crap what UMP does is to first download the header of the media, and check if the media is really alive, whats the quality of it (ie:720p,480p) and provide a selection UI to the user. So user will never face a dead link or a link that claims it is hd but it is crappy 144p in reality.

**GREEDY&FAST:** UMP is CPU greedy and multithreaded, so it is fast. I mean really fast. No bs4 is used for scraping all done by regex and it is all pure pythonic so it can work in any device without binary manipulation and etc. (not tested in early versions of XBMC)

**YOU FAVORITE SWISS KNIFE:** It has it is own image player rewritten with kodi controls since image player in kodi is quite limited for manga viewing. It has a built in browser that can handle cookies, save sessions between your scraper and video player and can make yourself pretty stealth and bug-free also it has gzip compression already implemented.

LIST OF CURRENT PORVIDERS:
--------------------------

||  Index Provider |   Link Provider | URL Provider  |
|----|----|----|----|
|VIDEO|IMDB, AnimeNews Network, The TVDB|primewire, kissanime, turkanimetv, 720pizle, dizipub|vodlocker, vk, google, videoweed, sharesix, sharerepo, ok.ru, nowvideo, novamov, myvi, movshare, mail.ru, kiwi, divxstage, cloudy|
|AUDIO|LastFM|redmp3|redmp3|
|IMAGE|MangaUpdates(BakaUpdates)|mangafox|mangafox|

SOME SCREENSHOTS:
-----------------

![](http://i58.tinypic.com/2rzt2f9.png)
![](http://i58.tinypic.com/4zx1jq.png)
![](http://i57.tinypic.com/30u8mle.png)
![](http://i61.tinypic.com/2rvykpf.png)
![](http://i61.tinypic.com/28rihqf.png)
![](http://i59.tinypic.com/25ph9q1.png)
![](http://i60.tinypic.com/2mdnymq.png)
![](http://i60.tinypic.com/2uy3hiu.png)
![](http://i62.tinypic.com/97pefo.png)
![](http://i59.tinypic.com/34ycoi1.png)
