import Logger
import VeetleData
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import base64,urllib2

__settings__ = xbmcaddon.Addon(id='plugin.video.veetle')
__language__ = __settings__.getLocalizedString

URL_VIEW_CHANNEL = '?channel='
URL_VIEW_CATEGORY = '?category='
URL_VIEW_CATEGORIES = '?categories'
URL_VIEW_SCHEDULE = '?schedule'
URL_VIEW_SEARCH = '?search'

URL_AKAMAI_PROXY = 'http://127.0.0.1:9000/veetle/%s'

dialog = xbmcgui.Dialog()

log = Logger.Logger("VeetleViews")

class VeetleViews:

    def __init__(self, pluginUrl, pluginHandle, dataSource):
        self.baseUrl = pluginUrl
        self.pluginHandle = pluginHandle
        self.dataSource = dataSource

    def buildChannelUrl(self, channelId):
        return self.baseUrl + URL_VIEW_CHANNEL + channelId

    def buildCategoryUrl(self, categoryId):
        return self.baseUrl + URL_VIEW_CATEGORY + str(categoryId)

    def createChannelListItem(self, channel, scheduleItems):

        if channel.viewers == None: extra=''
        else: extra=' / %s %s'  % (channel.viewers,str(__language__(40016)))
        channelDisplayTitle = '[B]%s[/B] (%s kbps%s)' % (channel.title,channel.bitRate/1000,extra)

        if channel.currentItem:
            channelDisplayTitle += ' ([COLOR=blue]%s[/COLOR])' %channel.currentItem.title

        listItem = xbmcgui.ListItem(
            channelDisplayTitle,
            iconImage=channel.logoUrl,
            thumbnailImage=channel.logoUrl)

        infoLabels = {
            'title': channel.title,
            'director': channel.userName,
            'genre': VeetleData.CategoryMap[channel.categoryId].title,
            'tagline': channel.description,
            'plot': channel.createScheduleSummary(scheduleItems),
        }

        listItem.setInfo('video', infoLabels)
        listItem.setProperty('IsPlayable', 'true')

        return listItem

    def createScheduleListItem(self, scheduleItem):

        displayTitle = scheduleItem.label()

        listItem = xbmcgui.ListItem(
            displayTitle)

        infoLabels = {'title': scheduleItem.title}
        listItem.setInfo('video', infoLabels)
        listItem.setProperty('IsPlayable', 'true')

        return listItem

    def renderHome(self, queryUrl):

        categoriesListItem = xbmcgui.ListItem(
            __language__(40001),
            iconImage='',
            thumbnailImage='')

        xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                self.baseUrl + URL_VIEW_CATEGORIES,
                categoriesListItem,
                isFolder=True)

        categoriesListItem = xbmcgui.ListItem(
            __language__(40002),
            iconImage='',
            thumbnailImage='')

        xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                self.baseUrl + URL_VIEW_SCHEDULE,
                categoriesListItem,
                isFolder=True)

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderCategories(self, queryUrl):

        # Load the channel list
        channels = self.dataSource.loadChannels()

        for category in VeetleData.Categories:

            # Get channel count for category
            channelCount = len(channels) if category.id == VeetleData.CategoryAll.id else len([channel for channel in channels if channel.categoryId == category.id])

            listItem = xbmcgui.ListItem(
                category.title + (' ([COLOR=blue]%s[/COLOR])' % str(channelCount)),
                iconImage='',
                thumbnailImage='')

            xbmcplugin.addDirectoryItem(
                    self.pluginHandle,
                    self.buildCategoryUrl(category.id),
                    listItem,
                    isFolder=True)

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderCategory(self, queryUrl):

        # Set content type for a category view to movies - this will enable more view types like media info
        xbmcplugin.setContent(self.pluginHandle, 'movies')

        categoryId = queryUrl[len(URL_VIEW_CATEGORY):].strip()

        # Load the channel list
        channels = self.dataSource.loadChannels()
        scheduleItems = self.dataSource.loadSchedule()

        # Filter channel for specified category
        channels = channels if categoryId == VeetleData.CategoryAll.id else [channel for channel in channels if channel.categoryId == categoryId]

        # Sort channels by popularity
        channels = sorted(channels, key=lambda channel: channel.popularityIndex, reverse=True)

        for channel in channels:

            url = self.buildChannelUrl(channel.channelId)
            listItem = self.createChannelListItem(channel, scheduleItems)

            xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                url,
                listItem,
                isFolder=False,
                totalItems=len(channels))

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderChannel(self, queryUrl):

        #Play a stream with the given channel id
        channelId = queryUrl[len(URL_VIEW_CHANNEL):].strip()
        if len(channelId)==32: #embed id
            try: channelId=self.abrir_url('http://fightnightaddons.esy.es/tools/veet.php?id=%s' % (channelId)).replace(' ','')
            except: pass
        
        channelStreamUrl = self.dataSource.loadChannelStreamUrl(channelId)
        try:
            VIDb64 = base64.encodestring(channelStreamUrl).replace('\n', '')
            fullUrl = URL_AKAMAI_PROXY % VIDb64
        except: pass

        if channelStreamUrl:
            xbmcplugin.setResolvedUrl(
                self.pluginHandle,
                True,
                xbmcgui.ListItem(path=fullUrl))
        else:
            xbmcplugin.setResolvedUrl(
                self.pluginHandle,
                False,
                xbmcgui.ListItem())

            
            ok = dialog.ok(__language__(30000), __language__(30001))

    def renderSchedule(self, queryUrl):

        # Load the schedule list
        schedule = self.dataSource.loadSchedule()

        for scheduleItem in schedule:

            url = self.buildChannelUrl(scheduleItem.channelId)
            listItem = self.createScheduleListItem(scheduleItem)

            xbmcplugin.addDirectoryItem(
                self.pluginHandle,
                url,
                listItem,
                isFolder=False)

        xbmcplugin.endOfDirectory(self.pluginHandle)

    def renderUrl(self, queryUrl):

        log.debug("Rendering URL: %s%s" % (self.baseUrl, queryUrl))

        if queryUrl.startswith(URL_VIEW_CHANNEL):
            self.renderChannel(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_CATEGORIES):
            self.renderCategories(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_CATEGORY):
            self.renderCategory(queryUrl)
            return

        if queryUrl.startswith(URL_VIEW_SCHEDULE):
            self.renderSchedule(queryUrl)
            return

        self.renderHome(queryUrl)

    def abrir_url(self,url,erro=True):
        print "A fazer request normal de: " + url
        try:
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            return link
        except urllib2.HTTPError, e:
            if erro==True:
                dialog.ok('Veetle',str(urllib2.HTTPError(e.url, e.code, __language__(30000), e.hdrs, e.fp)))
                sys.exit(0)
        except urllib2.URLError, e:
            if erro==True:
                dialog.ok('Veetle',__language__(30000))
                sys.exit(0)

