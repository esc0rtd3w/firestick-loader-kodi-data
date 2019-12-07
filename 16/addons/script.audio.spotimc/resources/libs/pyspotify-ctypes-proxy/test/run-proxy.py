#!/usr/bin/env python
'''
Created on 07/11/2010

@author: mikel
'''
import sys, os, os.path
os.chdir(os.path.abspath(os.path.dirname(__file__)))

#Search path for dlls/extensions
sys.path.append('../dlls')

#Search paths for python libs/eggs
sys.path.append("../libs/PyspotifyCtypes.egg")
sys.path.append("../libs/CherryPy.egg")

#Put spotifyproxy source on path
sys.path.append('../src')

#mandatory libspotify imports
from appkey import appkey
from spotify import session, MainLoop, handle_sp_error

#Imports for jukebox
import cmd
import threading

#Import the proxy server
from spotifyproxy import audio, httpproxy



class JukeboxCallbacks(session.SessionCallbacks):
    _mainloop = None
    __buf = None
    
    def __init__(self, mainloop, buf):
        self._mainloop = mainloop
        self.__buf = buf
    
    
    def logged_in(self, session, error):
        handle_sp_error(error)
        print "login successful"  
    
    
    def logged_out(self, session):
        print "logout successful"
            
    
    def connection_error(self, session, error):
        print "conn error"
    
    
    def log_message(self, session, data):
        print "log: %s" % data
    
    
    def streaming_error(self, error):
        print "streaming error: %d" % error
    
    
    def end_of_track(self, session):
        self.__buf.set_track_ended()
    
    
    def notify_main_thread(self, session):
        self._mainloop.notify()
    
    
    def music_delivery(self, session, data, num_samples, sample_type, sample_rate, num_channels):
        return self.__buf.music_delivery(data, num_samples, sample_type, sample_rate, num_channels)
    
    
    def get_audio_buffer_stats(self, session):
        return self.__buf.get_stats()



def main():
    print "uses SPOTIFY(R) CORE"
    ml = MainLoop()
    buf = audio.BufferManager()
    cb = JukeboxCallbacks(ml, buf)
    s = session.Session(
        cb,
        app_key=appkey,
        user_agent="python ctypes bindings",
        settings_location="../tmp/settings",
        cache_location="../tmp/cache",
    )
    
    pr = httpproxy.ProxyRunner(s, buf)
    c = JukeboxCmd(s, ml)
    c.start()
    pr.start()
    ml.loop(s)
    pr.stop()



#The main jukebox command prompt
class JukeboxCmd(cmd.Cmd, threading.Thread):
    prompt = "jukebox>"
    
    _session = None
    _mainloop = None
    
    def __init__(self, session, mainloop):
        cmd.Cmd.__init__(self)
        threading.Thread.__init__(self)
        self._session = session
        self._mainloop = mainloop
    
    
    def run(self):
        self.cmdloop()
    
    
    def do_login(self, line):
        args = line.split(' ', 2)
        self._session.login(args[0], args[1])
    
    
    def do_logout(self, line):
        self._session.logout()
    
    
    def do_quit(self, line):
        self._mainloop.quit()
        return True
    
    
    do_EOF = do_quit


if __name__ == '__main__':
    main()
