import control
import os
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

db_path = os.path.join(control.dataPath, 'favourites.db')
if not os.path.exists(control.dataPath):
    os.makedirs(control.dataPath)

db=database.connect(db_path)

base = 'http://opentuner.is'

def add_favourite_show(name, link, thumb):
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Favourite_shows (Link TEXT,Title TEXT, Thumb TEXT )")    
        db.commit()
        cur.execute("SELECT Title,Link,Thumb from Favourite_shows WHERE Title = ? AND Link=? and Thumb=?", (name,link,thumb))
        data=cur.fetchall()
        if len(data)!=0:
            control.infoDialog(name + ' already exists in your TeeVee favourites',heading='Favourite Already Exists')
            return
        
        cur.execute("INSERT INTO Favourite_shows(Link,Title, Thumb) VALUES (?,?, ?);",(link,name,thumb))
        db.commit()
        cur.close()
    control.infoDialog('Added to TeeVee favourites!',heading=name)
    return

def get_favourites():
    with db:
        cur = db.cursor()
        cur.execute("begin")   
        cur.execute("create table if not exists Favourite_shows (Title TEXT, Link TEXT, Thumb TEXT)")    
        db.commit()  
        cur.execute("SELECT Title,Link,Thumb FROM Favourite_shows")
        rows = cur.fetchall()
        cur.close()
        favs=[]
        for i in range (len(rows)):
            folder=rows[i]
            url = folder[1].replace('http://opentuner.is','').lstrip('/')
            folder = (folder[0],url,folder[2])
            favs+=[folder]
    return favs


def delete_all_tv_favs():
    with db:
        cur = db.cursor()
        cur.execute("drop table if exists Favourite_shows")
        cur.close()
    return


def remove_tv_fav(title,link):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Favourite_shows WHERE Title = ? AND Link = ?",(title,link))
    db.commit()
    cur.close()

def add_search_query(query,type):
    his = get_search_history('tv')
    if query in his:
        return
    with db:
        cur = db.cursor()    
        cur.execute("begin") 
        cur.execute("create table if not exists Search_history (type TEXT, query TEXT)")    
        db.commit()
        cur.execute("INSERT INTO Search_history(type,query) VALUES (?,?);",(type,query))
        db.commit()
        cur.close()
    return
def get_search_history(type):
    with db:
        cur = db.cursor()
        cur.execute("begin")    
        cur.execute("create table if not exists Search_history (type TEXT, query TEXT)")    
        db.commit() 
        cur.execute("SELECT query FROM Search_history WHERE type = ?",(type,))
        rows = cur.fetchall()
        cur.close()
        his=[]
        for i in range (len(rows)):
            folder=rows[i][0]
            his+=[folder]
    return his
def delete_history(type):
    cur = db.cursor()  
    cur.execute("begin")  
    cur.execute("DELETE FROM Search_history WHERE type = ?",(type,))
    db.commit()
    cur.close()