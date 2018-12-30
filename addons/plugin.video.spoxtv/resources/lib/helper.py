# -*- coding: utf-8 -*-

def get_category_items(data):
    items = []
    live_item = {'type':'dir', 'mode':'live_videos', 'name':'Live', 'id':''}
    items.append(live_item)
    sport = data[0]
    category = sport['category']
    id = 0
    for i in category:
        name = i['name'].encode('utf-8')
        items.append({'type':'dir', 'mode':'channels', 'name':name, 'id':id})
        id += 1
    return items

def get_channel_items(data,id):
    items = []
    channels = []
    sport = data[0]
    category = sport['category'][int(id)]
    channel = category['channel']
    if 'name' in channel:
        channels.append(channel)
    else:
        channels = channel
    for i in channels:
        name = i['name'].encode('utf-8')
        id = i['id']
        image = i.get('thumbnail', '')
        items.append({'type':'dir', 'mode':'videos', 'name':name, 'id':id, 'image':image})
    return items
    
def get_video_items(data,get_total=False):
    items = []
    channel = data['channel']
    total = channel['page']['total']
    if get_total:
        return total
    item = channel['item']
    for i in item:
        group = i['group']
        content = group['content']
        title = i['title']
        image = group['thumbnail']['url']
        duration = int(content[0]['duration'])
        date = i['pubDate']
        name = '%s (%s)' % (title,get_datetime(date))
        name = name.encode('utf-8')
        if 'hls' in group:
            url = group['hls']['url']
        else:
            url = content
        items.append({'type':'video', 'mode':'play_video', 'name':name, 'id':url, 'image':image, 'duration':duration})
    return items

def get_next_item(items,id,offset,total):
    offset = str(int(offset)+6)
    if int(total) - int(offset) > 0:
        items.append({'type':'dir', 'mode':'videos', 'name':'Weiter..', 'id':id, 'image':None, 'offset':offset, 'total':total})
    return items

def get_live_items(data):
    from datetime import datetime
    items = []
    streams = data['streams']
    for s in streams:
        if s['geoblocked'] == False:
            description = s['description'].encode('utf-8')
            starttime = str(s.get('streamStartTime', '0'))[:10]
            endtime = str(s.get('streamEndTime', '0'))[:10]
            live = is_live(int(starttime),int(endtime))
            duration = int(endtime) - int(starttime)
            dt = datetime.fromtimestamp(int(starttime))
            dt = str(dt)[:16]
            if live:
                name = '[COLOR red]LIVE[/COLOR] - %s' % (description)
            else:
                name = '%s %s' % (dt,description)
            id = s['streamId']
            image = s['playerConfig']['slates']['low']
            items.append({'type':'video', 'mode':'play_live_video', 'name':name, 'id':id, 'image':image, 'duration':duration})
    return items

def get_live_url(data,quality):
    url = None
    launcher = data['launchInfo']['streamLauncher']
    for i in launcher:
        url = i['launcherURL']
        if i['playerAlias'] == 'iPhone' and quality == 'Niedrig':
            break
        if i['playerAlias'] == 'hlshd' and quality == 'Hoch':
            break
    return url

def get_datetime(date):
    import re
    result = '?-?-?'
    try:
        pattern = '\w+, (\d{2}) (\w+) (\d{4})'
        r = re.search(pattern, date)
        day = r.group(1)
        month = r.group(2)
        year = r.group(3)
        datetime = '%s-%s-%s' % (day, month, year)
        return datetime
    except:
        pass
    return result

def is_live(starttime,endtime):
    import time
    now = int(str(time.time())[:10])
    live = False
    if starttime <= now <= endtime:
        live = True
    return live