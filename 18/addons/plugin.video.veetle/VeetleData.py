import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.veetle')
__language__ = __settings__.getLocalizedString

class VeetleCategory:

    def __init__(self, id, title):
        self.id = id
        self.title = title

class VeetleChannel:

    def __init__(self):

        self.channelId = 0
        self.title = ''
        self.description = ''
        self.categoryId = ''

        self.userName = ''

        self.popularityIndex = 0
        self.bitRate = 0

        self.logoUrl = ''

        self.currentItem = None

    def createScheduleSummary(self, scheduleItems):

        scheduleItems = [scheduleItem for scheduleItem in scheduleItems if scheduleItem.channelId == self.channelId]
        summary = ''

        for scheduleItem in scheduleItems:
            summary += scheduleItem.label()
            summary += '[CR]'

        return summary

class VeetleScheduleItem:

    def __init__(self):

        self.title = ''
        self.description = ''
        self.duration = None
        self.startTime = None

    def label(self):
        return '[B]%s[/B] - %s ([COLOR=blue]%s mins[/COLOR])' % (self.startTime.strftime('%H:%M'), self.title, self.duration.seconds / 60)

CategoryAll = VeetleCategory('0', __language__(40003))
CategoryEntertainment = VeetleCategory('10', __language__(40004))
CategoryShows = VeetleCategory('20', __language__(40005))
CategoryAnimation = VeetleCategory('60', __language__(40006))
CategorySports = VeetleCategory('80', __language__(40007))
CategoryComedy = VeetleCategory('50', __language__(40008))
CategoryMusic = VeetleCategory('70', __language__(40009))
CategoryEducation = VeetleCategory('90', __language__(40010))
CategoryGaming = VeetleCategory('40', __language__(40011))
CategoryNews = VeetleCategory('30', __language__(40012))
CategoryReligion = VeetleCategory('100', __language__(40013))
CategoryMobile = VeetleCategory('110', __language__(40014))

Categories = [
    CategoryAll,
    CategoryEntertainment,
    CategoryShows,
    CategoryAnimation,
    CategorySports,
    CategoryComedy,
    CategoryMusic,
    CategoryEducation,
    CategoryGaming,
    CategoryNews,
    CategoryReligion,
    CategoryMobile
    ]

CategoryMap = {
    CategoryAll.id: CategoryAll,
    CategoryAnimation.id: CategoryAnimation,
    CategoryComedy.id: CategoryComedy,
    CategoryEducation.id: CategoryEducation,
    CategoryGaming.id: CategoryGaming,
    CategoryMobile.id: CategoryMobile,
    CategoryEntertainment.id: CategoryEntertainment,
    CategoryShows.id: CategoryShows,
    CategorySports.id: CategorySports,
    CategoryMusic.id: CategoryMusic,
    CategoryNews.id: CategoryNews,
    CategoryReligion.id: CategoryReligion
}
