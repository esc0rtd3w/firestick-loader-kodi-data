import process
import re
import requests
import xbmcgui
from datetime import datetime
import xbmcaddon
import xbmc

Year = datetime.now().strftime('%Y')
Month = datetime.now().strftime('%m')
Day = datetime.now().strftime('%d')
Hour = datetime.now().strftime('%H')
Minute = datetime.now().strftime('%M')
time_now_number = str((int(Hour) * 60) + int(Minute))
addon_id = 'plugin.video.quantum'
ADDON = xbmcaddon.Addon(id=addon_id)



def TV_GUIDE_MENU():
    TV_GUIDE_CO_UK_CATS()



def TV_GUIDE_CO_UK_CATS():
	if ADDON.getSetting('type_select')=='Select':
		process.Menu('Search by channel number', '', 2207, '', '', '', '')
		process.Menu('Popular', '7', 2205, '', '', '', '')
		process.Menu('Freeview', '3', 2205, '', '', '', '')
		process.Menu('Sky', '5', 2205, '', '', '', '')
		process.Menu('Virgin XL', '25', 2205, '', '', '', '')
		process.Menu('Freesat', '19', 2205, '', '', '', '')
		process.Menu('BT', '22', 2205, '', '', '', '')
	elif ADDON.getSetting('type_select')=='Popular':
		tvguide_co_uk('7')
	elif ADDON.getSetting('type_select')=='Freeview':
		tvguide_co_uk('3')
	elif ADDON.getSetting('type_select')=='Sky':
		tvguide_co_uk('5')
	elif ADDON.getSetting('type_select')=='Virgin XL':
		tvguide_co_uk('25')
	elif ADDON.getSetting('type_select')=='Freesat':
		tvguide_co_uk('19')
	elif ADDON.getSetting('type_select')=='BT':
		tvguide_co_uk('22')

def Select_Type():
    choices = ['Select by Virgin No.', 'Select by Sky No.', 'Select by Freeview No.']
    choice = xbmcgui.Dialog().select('Search by channel number', choices)
    if choice == 0:
        find_channel(
            'http://www.tvguide.co.uk/?catcolor=&systemid=25&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323',
            'Virgin')
    if choice == 1:
        find_channel(
            'http://www.tvguide.co.uk/?catcolor=&systemid=5&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323',
            'Sky')
    if choice == 2:
        find_channel(
            'http://www.tvguide.co.uk/?catcolor=&systemid=3&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323',
            'Freeview')


def find_channel(url, name):
    channel_no = xbmcgui.Dialog().input("Channel No", type=xbmcgui.INPUT_NUMERIC)
    html = requests.get(url).text
    match = re.compile('qt-text="(.+?)" title="(.+?)"').findall(html)
    for number, channel_name in match:
        channel_name = channel_name.replace(' TV listings', '')
        number = number.replace('Channel Numbers<br> ', '')
        if ':' in number:
            if name == 'Sky':
                sky_no = re.compile('Sky:(.+?) ').findall(str(number))
                for item in sky_no:
                    if channel_no in sky_no:
                        WhatsOnCOUK(url, str(channel_name))
            elif name == 'Virgin':
                virgin_no = re.compile('Virgin:(.+?) ').findall(str(number))
                for item in virgin_no:
                    if channel_no in virgin_no:
                        WhatsOnCOUK(url, str(channel_name))
            elif name == 'Freeview':
                freeview_no = re.compile('Freeview:(.+?) ').findall(str(number))
                for item in freeview_no:
                    if channel_no in freeview_no:
                        WhatsOnCOUK(url, str(channel_name))



def tvguide_co_uk(url):
    List = [['All','http://www.tvguide.co.uk/?catcolor=&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Comedy','http://www.tvguide.co.uk/?catcolor=3253CF&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Sports','http://www.tvguide.co.uk/?catcolor=53CE32&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Music','http://www.tvguide.co.uk/?catcolor=FF9933&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Film','http://www.tvguide.co.uk/?catcolor=000000&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Soap','http://www.tvguide.co.uk/?catcolor=AB337D&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Kids','http://www.tvguide.co.uk/?catcolor=E3BB00&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Drama','http://www.tvguide.co.uk/?catcolor=CE3D32&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Talk show','http://www.tvguide.co.uk/?catcolor=800000&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Game show','http://www.tvguide.co.uk/?catcolor=669999&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Sci-fi','http://www.tvguide.co.uk/?catcolor=666699&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Documentary','http://www.tvguide.co.uk/?catcolor=CCCCCC&systemid=' + url + '&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Motor','http://www.tvguide.co.uk/?catcolor=996633&systemid=7&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323'],
            ['Horror','http://www.tvguide.co.uk/?catcolor=666633&systemid=7&thistime=' + Hour + '&thisDay=' + Month + '/' + Day + '/' + Year + '&gridspan=03:00&view=0&gw=1323']]
    for item in List:
        name = item[0]
        list_url = item[1]
        if ADDON.getSetting('cat_select')=='Show Menu':
            process.Menu(name, list_url, 2206, '', '', '', '')
        else:
            check_name = ADDON.getSetting('cat_select')
            if check_name == name:
                WhatsOnCOUK(list_url,'')
			
def WhatsOnCOUK(url,extra):
    try:
        html = requests.get(url).text
        channel_block = re.compile('<div class="div-epg-channel-progs">.+?<div class="div-epg-channel-name">(.+?)</div>(.+?)</div></div></div>',re.DOTALL).findall(html)
        for channel, block in channel_block:
            prog = re.compile('<a qt-title="(.+?)".+?<br>(.+?)<br>.+?</div>(.+?)<br>', re.DOTALL).findall(str(block.encode('utf-8')))
            for show_info, show_no, info in prog:
                show_no = show_no.replace('</div>','')
                info = info.replace('</div>','').replace('</a>','')
                if 'href' in info:
                    change = re.compile('(.+?)href').findall(str(info))
                    for thing in change:
                        info = thing					
                time_finder = re.compile('(.+?)-(.+?) ').findall(str(show_info))
                for start, finish in time_finder:
                    if 'am' in start:
                        time_split = re.compile('(.+?):(.+?)am').findall(str(start))
                        for hour, minute in time_split:
                            start_number = (int(hour) * 60) + int(minute)
                    elif 'pm' in start:
                        time_split = re.compile('(.+?):(.+?)pm').findall(str(start))
                        for hour, minute in time_split:
                            if hour == '12':
                                start_number = (int(hour) * 60) + int(minute)
                            else:
                                start_number = (int(hour) + 12) * 60 + int(minute)
                    if 'am' in finish:
                        time_split = re.compile('(.+?):(.+?)am').findall(str(finish))
                        for hour, minute in time_split:
                            finish_number = (int(hour) * 60) + int(minute)
                    elif 'pm' in finish:
                        time_split = re.compile('(.+?):(.+?)pm').findall(str(finish))
                        for hour, minute in time_split:
                            if hour == '12':
                                finish_number = (int(hour) * 60) + int(minute)
                            else:
                                finish_number = (int(hour) + 12) * 60 + int(minute)
                    if int(start_number) < int(time_now_number) < int(finish_number):
                        if not extra or extra == '':
                            clean_channel = channel.replace('BBC1 London', 'BBC1').replace('BBC2 London','BBC2').replace('ITV London', 'ITV1')
                            process.Menu(clean_channel.encode('utf-8') + ': ' + show_info.encode('utf-8'), '', 2203,'', '',show_no+'\n'+info, clean_channel.replace('HD',''))
                            process.setView('movies', 'INFO2')
                        else:
                            clean_channel = channel.replace('BBC1 London', 'BBC1').replace('BBC2 London','BBC2').replace('ITV London', 'ITV1')
                            clean_extra = extra.replace('BBC1 London', 'BBC1').replace('BBC2 London','BBC2').replace('ITV London','ITV1')
                            if clean_extra == clean_channel:
                                process.Menu(clean_channel.encode('utf-8') + ': ' + show_info.encode('utf-8'), '', 2203,'', '',show_no+'\n'+info, clean_channel.replace('HD',''))
                                process.setView('movies', 'INFO2')
                            else:
                                pass
    except:
        pass


def whatsoncat():
    html = process.OPEN_URL('http://tvguideuk.telegraph.co.uk/')
    match = re.compile('<li class="tabs"><span><a href="(.+?)">(.+?)</a></span></li>').findall(html)
    for url, name in match:
        if 'amp;' in url:
            if int(Hour) < 12:
                time = str(Hour) + '.' + Minute + 'am'
            else:
                pm = int(Hour) - 12
                time = str(pm) + '.' + Minute + 'pm'
            url = url.replace('amp;', '').replace('oclock=', 'oclock=' + time)
            process.Menu(name, 'http://tvguideuk.telegraph.co.uk/' + url, 2202, '', '', '', '')


def whatson(url):
    html = process.OPEN_URL(url)
    match = re.compile(
        '<div class="channel_name">(.+?)<.+?<div class="programme  showing".+?channel_id=(.+?).+?>(.+?)</a>',
        re.DOTALL).findall(html)
    for name, id, whatson in match:
        name = name.replace('(', '').replace(')', '').replace('Plus 1', '+1').replace('London', '').replace('Five', '5')
        process.Menu(name + ' - ' + whatson, '', 2203, '', '', '', name)


def search_split(extra):
    import search
    import Live
    search.Live_TV(extra.lower().replace('hd', '').replace(' ', '').replace('christmasgold','gold'))
    Live.search_next(extra.lower().replace('hd', '').replace(' ', '').replace('christmasgold','gold'))
