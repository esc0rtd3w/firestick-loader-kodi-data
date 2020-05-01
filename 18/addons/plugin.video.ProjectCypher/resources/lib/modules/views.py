# -*- coding: utf-8 -*-




import re,os

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

from resources.lib.modules import control


def addView(content):
    try:
        skin = control.skin
        skinPath = control.skinPath
        xml = os.path.join(skinPath,'addon.xml')
        file = control.openFile(xml)
        read = file.read().replace('\n','')
        file.close()
        try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
        except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
        src = os.path.join(skinPath, src)
        src = os.path.join(src, 'MyVideoNav.xml')
        file = control.openFile(src)
        read = file.read().replace('\n','')
        file.close()
        views = re.compile('<views>(.+?)</views>').findall(read)[0]
        views = [int(x) for x in views.split(',')]
        for view in views:
            label = control.infoLabel('Control.GetLabel(%s)' % (view))
            if not (label == '' or label == None): break
        record = (skin, content, str(view))
        control.makeFile(control.dataPath)
        dbcon = database.connect(control.viewsFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS views (""skin TEXT, ""view_type TEXT, ""view_id TEXT, ""UNIQUE(skin, view_type)"");")
        dbcur.execute("DELETE FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
        dbcur.execute("INSERT INTO views Values (?, ?, ?)", record)
        dbcon.commit()

        viewName = control.infoLabel('Container.Viewmode')
        skinName = control.addon(skin).getAddonInfo('name')
        skinIcon = control.addon(skin).getAddonInfo('icon')

        control.infoDialog(viewName, heading=skinName, sound=True, icon=skinIcon)
    except:
        return


def setView(content, viewDict=None):
    for i in range(0, 200):
        if control.condVisibility('Container.Content(%s)' % content):
            try:
                skin = control.skin
                record = (skin, content)
                dbcon = database.connect(control.viewsFile)
                dbcur = dbcon.cursor()
                dbcur.execute("SELECT * FROM views WHERE skin = '%s' AND view_type = '%s'" % (record[0], record[1]))
                view = dbcur.fetchone()
                view = view[2]
                if view == None: raise Exception()
                return control.execute('Container.SetViewMode(%s)' % str(view))
            except:
                try: return control.execute('Container.SetViewMode(%s)' % str(viewDict[skin]))
                except: return

        control.sleep(100)


