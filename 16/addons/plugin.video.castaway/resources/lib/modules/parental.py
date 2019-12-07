# -*- coding: utf-8 -*-
import xbmc, sys
import sqlite3 as sql
import control

from resources.lib.modules.addon import Addon
addon = Addon('plugin.video.castaway', sys.argv)

db_path = control.databaseFile




class Parental():
    def __init__(self):
        self.db = sql.connect(db_path)
        self.cur = self.db.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Settings (Name TEXT PRIMARY KEY , Enabled INT DEFAULT 0, Value Text DEFAULT __not__set__, Modified INT DEFAULT 0)')
        self.db.commit()

    def isEnabled(self):
        item = self.cur.execute("SELECT * FROM Settings WHERE Name=?",('Parental',)).fetchall()
        if len(item)==0:
            self.cur.execute('INSERT INTO Settings Values(?,?,?,?)',('Parental',0,'__not__set__',0))
            self.db.commit()
            return False
        else:
            return item[0][1]==1

    def isVisible(self):
        item = self.cur.execute("SELECT * FROM Settings WHERE Name=?",('Adult visible',)).fetchall()
        if len(item)==0:
            self.cur.execute('INSERT INTO Settings Values(?,?,?,?)',('Adult visible',0,'__not__set__',0))
            self.db.commit()
            return False
        else:
            return item[0][1]==1

    def setVisible(self, value):
        correct = self.promptPassword()
        if correct:
            self.cur.execute('UPDATE Settings SET Enabled=? WHERE Name=?',(value, 'Adult visible',))
            self.db.commit()
        return
    

    def isPasswordSet(self):
        item = self.cur.execute("SELECT * FROM Settings WHERE Name=?",('Parental',)).fetchall()
        if len(item)==0:
            self.cur.execute('INSERT INTO Settings Values(?,?,?,?)',('Parental',0,'__not__set__',0))
            self.db.commit()
            return False
        else:
            return item[0][2]!='__not__set__'
        


    def enable(self):
        if self.isEnabled():
            return
        correct = self.promptPassword()
        if correct:
            self.cur.execute("UPDATE Settings SET Enabled=? WHERE Name=?",(1,'Parental',))
            self.db.commit()
        return

    def disable(self):
        if not self.isEnabled():
            return
        correct = self.promptPassword()
        if correct:
            self.cur.execute("UPDATE Settings SET Enabled=? WHERE Name=?",(0,'Parental',))
            self.db.commit()
        return

    def setPassword(self):
        keyboard = xbmc.Keyboard('', 'Enter new password:', True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            password = keyboard.getText()
            self.cur.execute("UPDATE Settings SET Value=? WHERE Name=?",(password,'Parental',))
            self.db.commit()
            addon.show_small_popup('Password set', 'Your new password was saved.')
        return password

    def changePassword(self):
        old_password = self.cur.execute("SELECT Value FROM Settings WHERE Name=?",('Parental',)).fetchall()[0][0]
        keyboard = xbmc.Keyboard('', 'Enter old password:', True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            passw = keyboard.getText()
            if passw==old_password:
                self.setPassword()
        return

    def promptPassword(self):
        if self.isPasswordSet():
            password = self.cur.execute("SELECT Value FROM Settings WHERE Name=?",('Parental',)).fetchall()[0][0]
        else:
            addon.show_small_popup('Password not set', 'Set your password first.')
            return False

        keyboard = xbmc.Keyboard('', 'Enter your password:', True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            passw = keyboard.getText()
            if passw==password:
                return True
            else:
                addon.show_small_popup('Incorrect password', 'You entered the wrong password.')
                return False
