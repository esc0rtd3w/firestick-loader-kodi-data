# -*- coding: utf-8 -*-
import control,client,webutils,os,re,cache
from log_utils import log
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database


if not os.path.exists(control.dataPath):
    os.mkdir(control.dataPath)
    
dbFile_old  = os.path.join(control.dataPath, 'lists.db')
dbFile  = os.path.join(control.dataPath, 'listsNew.db')
db = database.connect(dbFile)

def initDB():
    dbcur = db.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS Lists (Name TEXT, Path TEXT)")
    db.commit()
    migrate()

def migrate():
    dbcur = db.cursor()
    try:
        dby = database.connect(dbFile_old)
        dbcury = dby.cursor()
        dbcury.execute("SELECT * FROM Lists")
        items = dbcury.fetchall()
        if len(items)==0:
            return
        for item in items:
            name = item[0].rstrip("'").lstrip("'")
            path = item[1].rstrip("'").lstrip("'")
            dbcur.execute("INSERT INTO Lists Values (?, ?)", (name,path))
            db.commit()
        dby.close()
        os.remove(dbFile_old)

    except:
        pass
    

def addList(name,path):
    if 'raw' not in path:
        path = path.replace('pastebin.com/','pastebin.com/raw/')
    initDB()
    dbcur = db.cursor()
    dbcur.execute("INSERT INTO Lists Values (?, ?)", (name,path))
    db.commit()

def removeList(name):
    initDB()
    dbcur = db.cursor()
    dbcur.execute("DELETE FROM Lists WHERE Name='%s'"%name)
    db.commit()

def getLists():
    initDB()
    out = []
    dbcur = db.cursor()
    dbcur.execute("SELECT * FROM Lists")
    items = dbcur.fetchall()
    for item in items:
        i = (item[0],item[1].replace('raw/raw','raw'))
        out.append(i)
    return out

def getItems(path):
    out = []
    if 'http' in path:
        content = client.request(path)
    else:
        f = open(path,'r')
        content = f.read()
        
        if path.endswith('.cl'):
            results = []
            paths = content.splitlines()
            for p in paths:
                results += cache.get(getItems,1000,p)
            return results
        f.close()



        

    if '#ext' in content.lower():
        return getItemsM3U(content)

    items = content.split('<item>')
    items = filter(None,items)
    for item in items:
        title = re.findall('<title>(.+?)</title>',item,flags = re.DOTALL)[0]
        url = re.findall('<url>(.+?)</url>',item,flags = re.DOTALL)[0]
        try:
            thumb = re.findall('<thumbnail>(.+?)</thumbnail>',item,flags = re.DOTALL)[0]
        except:
            thumb = 'x'

        out.append((url,title,thumb))

    out.sort(key=lambda x: x[1])
    return out


def getItemsM3U(content):
    out = []
    urls = []
    import m3u_parser
    playlist = m3u_parser.parseM3U(content)
    thumb = 'x'
    for item in playlist:
        url = item.path
        title = item.title
        if url not in urls:
            out.append((url,title,thumb))
            urls.append(url)

    return out



def getItems_extended(path):
    out = []
    if 'http' in path:
        content = client.request(path)
    else:
        f = open(path,'r')
        content = f.read()
        f.close()
    items = content.split('<item>')
    items = filter(None,items)
    for item in items:

        title = re.findall('<title>(.+?)</title>',item,flags = re.DOTALL)[0]
        url = re.findall('<url>(.+?)</url>',item,flags = re.DOTALL)[0]
        try:
            thumb = re.findall('<thumbnail>(.+?)</thumbnail>',item,flags = re.DOTALL)[0]
        except:
            thumb = 'x'

        out.append((url,title,thumb, item))
    return out

def removeItem(item, path):
    if 'http' in path:
        control.infoDIalog('Cannot modify remote list.',heading='Castaway Lists')
        return

    items = getItems_extended(path)
    toReplace = False
    for it in items:
        i2 = (it[0],it[1],it[2])
        if i2 == item:
            toReplace = it[3]
            break

    if toReplace:
        f = open(path,'r')
        content = f.read()
        f.close()
        content = content.replace(toReplace,'')
        f = open(path,'w')
        f.write(content)
        f.close()

def addItem(item,path):
    if 'http' in path:
        control.infoDIalog('Cannot modify remote list.',heading='Castaway Lists')
        return

    
    f = open(path,'r')
    content = f.read()
    f.close()
    itemx = '''
    <item>
        <title>%s</title>
        <thumbnail>%s</thumbnail>
        <url>%s</url>
    </item>'''%(item[1],item[2],item[0])
    content += '%s'%itemx
    f = open(path,'w')
    f.write(content)
    f.close()
