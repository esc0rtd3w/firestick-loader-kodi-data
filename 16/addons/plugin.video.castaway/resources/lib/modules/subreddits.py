import control
import os
from log_utils import log
import re
import urlparse

saveFile = os.path.join(control.dataPath,'subreddits.txt')

def get_subreddits():
    if not os.path.exists(saveFile):
        return []
    with open(saveFile,'r') as f:
        content = f.read()
        items = content.split('\n')
    items = filter(None,items)
    items = sorted(items)
    return items

def add_subreddit():
    reddit = control.get_keyboard('Enter subreddit')
    if not reddit:
        control.infoDialog('A problem occured. Try again!',heading='Castaway Lists')
        return
    reddit = reddit.replace('https://','').replace('http://','').replace('www.','').replace('reddit.com','').replace('r/','').replace('/','')
    items = get_subreddits()
    items.append(reddit)
    write_subreddits(items)

def write_subreddits(items):
    items = filter(None,items)
    f = open(saveFile,'w')
    for item in items:
        f.write("%s\n" % item)
    f.close()

def remove_subreddit(reddit):
    items = get_subreddits()
    items = filter(None,items)
    items.remove(reddit)
    write_subreddits(items)

def login(r):
    user = control.setting('reddit_user')
    passw = control.setting('reddit_pass')
    login = user!='' and passw!=''
    if login:
        try:
            r.login(user, passw)
        except:
            control.infoDialog('Please check your Reddit username and password.')
    return r

def events(subreddit):
    import praw
    new = []
    r = praw.Reddit(user_agent='Kodi Castaway')
    r = login(r)
    r.config.api_request_delay = 0
    
    filtering = control.setting('enable_subreddit_filters') == 'true'
    okay = True
    
    try:
        for submission in r.get_subreddit(subreddit).get_hot(limit=30):
            if filtering:
                words = control.setting('subreddit_filters').split(',')
                if any(word in submission.title.lower() for word in words):
                    okay = True
                else:
                    okay = False
            if okay:
                url = submission.id
                title = submission.title
                title = title.encode('utf-8')
                new.append((url,title))
        return new
    except:
        return []


def event_links(url):
    import praw
    r = praw.Reddit(user_agent='Kodi Castaway')
    r = login(r)
    r.config.api_request_delay = 0
    submission = r.get_submission(submission_id=url)
    links=[]
    regex = re.compile(r'([-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)',re.IGNORECASE)
    link = re.findall(regex, submission.selftext.encode('utf-8'))
    links = links + link
    links+=re.findall('((acestream://[^$\s]+))',submission.selftext.encode('utf-8'))
    links+=re.findall('((sop://[^$\s]+))',submission.selftext.encode('utf-8'))
    links += re.findall('To use kodi, make your .strm file with this:\s*((http://[^\s]+))',submission.selftext.encode('utf-8'))
            
    flat_comments = praw.helpers.flatten_tree(submission.comments)
    for comment in flat_comments:
        if not isinstance(comment,praw.objects.Comment):
            flat_comments.remove(comment)
    try:
        flat_comments.sort(key=lambda comment: comment.score , reverse=True)
    except:
        pass
    for comment in flat_comments:
        try:
            link = re.findall(regex, comment.body.encode('utf-8'))
            aces = re.findall('([a-z0-9]{40})', comment.body.encode('utf-8'))
            for ace in aces:
                links.append(('acestream://'+ace,'acestream://'+ace))
           
            links += re.findall('To use kodi, make your .strm file with this:\s*((http://[^\s]+))',comment.body.encode('utf-8'))
            links += link
            links+=re.findall('((acestream://[^$\s]+))',comment.body.encode('utf-8'))
            links+=re.findall('((sop://[^$\s]+))',comment.body.encode('utf-8'))
            if i>3:
                continue

        except:
            pass
    return __prepare_links(links)  

def __prepare_links(links):
    new = []
    urls = []
    unwanted = ['koora','reddit','imraising','navix','imgur','changetip','blogspot','imgflip','coinbase','acestreamguide','vipleague','vipbox','hlsvariant','blackout.jsp','domain=mlb.com','streamwoop','strikeout']
    for l in links:
        
        url = l[0]
        url = url.replace('https://','http://')
        url = url.replace('101livesportsvideos','www.101livesportsvideos')
        if not (url.startswith('http://') or url.startswith('sop://') or url.startswith('acestream://') or url.startswith('https://')):
            url = 'http://' + url

        dms = ['nba.com','mlb.com','nhl.com']
        if any(w in url for w in dms):
            if 'Cookie=' not in url:
                continue
        title = url.replace('http://','').replace('https://','').replace('www.','')

        if 'm3u8' in url:
            title = 'M3U8 ' + urlparse.urlparse(url).netloc
        elif 'acestream' in url:
            title = l[1]
        elif 'sop://' in url:
            title = 'Sopcast ' + urlparse.urlparse(url).netloc
        elif title =='':
            title = url
        a = False
        

        for u in unwanted:
            if u in title:
                a = True
                break
        if not a:
            if url not in urls:
                if not (url.startswith('http://') or url.startswith('sop://') or url.startswith('acestream://')):
                    url = 'http://' + url
                new.append((url,title))
                urls.append(url)
    return new