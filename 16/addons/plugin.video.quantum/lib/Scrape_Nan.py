import xbmc,xbmcgui

'''
def scrape_episode(title,show_year,year,season,episode,imdb):
    xbmc.log('title:'+title+'# season:'+season+'# episode:'+episode+'# year:'+year,xbmc.LOGNOTICE)
    from nanscrapers import scrape_episode_with_dialog
    progress = []
    item = []
    dp =  xbmcgui.DialogProgress()
    dp.create('Initiating Scrapers')
    links_scraper = scrape_episode_with_dialog(title, show_year, year, season, episode,imdb,None)
    if links_scraper is False:
        xbmcgui.Dialog().ok("Movie not found", "No Links Found for " + name + " (" + year + ")")
    else:
        if links_scraper:
            url = links_scraper['url']
            xbmc.Player().play(url, xbmcgui.ListItem(title))
'''
def scrape_episode(title,show_year,year,season,episode,imdb):
    if season[0]=='0':
        season = season[1:]
    if episode[0]=='0':
        episode = episode[1:]
    from nanscrapers import scrape_episode_with_dialog
    progress = []
    item = []
    dp =  xbmcgui.DialogProgress()
    dp.create('Initiating Scrapers')
    links_scraper = scrape_episode_with_dialog(title, show_year, year, season, episode, imdb, None)
    if links_scraper is False:
        xbmcgui.Dialog().ok("Movie not found", "No Links Found for " + name + " (" + year + ")")
    else:
        if links_scraper:
            url = links_scraper['url']
            xbmc.Player().play(url, xbmcgui.ListItem(title))
'''	if links_scraper is False:
		xbmc.log('passed',xbmc.LOGNOTICE)
		pass
	else:
		scraped_links = []
		if len(scraped_links)!=0:
			for scraper_links in links_scraper():
				item.append(scraper_links)
			items = len(item)
			for scraper_links in links_scraper():
				if scraper_links is not None:
					progress.append(scraper_links)
					dp_add = len(progress) / float(items) * 100
					dp.update(int(dp_add),'Checking sources',"Checking Nan Scrapers",'Please Wait')				
					scraped_links.extend(scraper_links)
			xbmc.log('links:'+str(scraper_links),xbmc.LOGNOTICE)
			for link in scraped_links:
				if link["quality"]=='SD': name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='CAM': name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='360': name = ' '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='480': name = ' '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='560': name = '  '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='720': name = '  '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='1080': name = '  '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='HD': name = '  '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif 'vidzi' in link["source"]: name = '  '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				else: name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				url = link['url']
				url = url
				process.Big_Resolve(name,url)
				xbmc.Player().play(url, xbmcgui.ListItem(name))'''

#		process.PLAY('test',link["url"],906,'','','','')
#		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE);

def scrape_movie(name,year,imdb):
	import xbmc
	from nanscrapers import scrape_movie_with_dialog
	link = scrape_movie_with_dialog(name, year, imdb, timeout=600)
	if link is False:
		xbmcgui.Dialog().ok("Movie not found", "No Links Found for " + name + " (" + year + ")")
	else:
		if link:
			url = link['url']
			xbmc.Player().play(url, xbmcgui.ListItem(name))


'''	progress = []
		item = []
		dp =  xbmcgui.DialogProgress()
		dp.create('Initiating Scrapers')
		links_scraper = scrape_movie(name, year, '', timeout=60)
		if links_scraper is False:
			pass
		else:
			scraped_links = []
			for scraper_links in links_scraper():
				item.append(scraper_links)
			items = len(item)
			for scraper_links in links_scraper():
				if scraper_links is not None:
					progress.append(scraper_links)
					dp_add = len(progress) / float(items) * 100
					dp.create('Checking for stream')
					dp.update(int(dp_add),'Checking sources',"Checking Nan Scrapers",'Please Wait')				
					scraped_links.extend(scraper_links)
			for link in scraped_links:
				if link["quality"]=='SD': name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='CAM': name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='360': name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='480': name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='560': name = ' '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='720': name = ' '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='1080': name = ' '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif link["quality"]=='HD': name = ' '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				elif 'vidzi' in link["source"]: name = '  '+link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				else: name = link["source"] + " - " + link["scraper"] + " (" + link["quality"] + ")"
				process.Play(name,link["url"],906,'','','','')
				xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE);'''