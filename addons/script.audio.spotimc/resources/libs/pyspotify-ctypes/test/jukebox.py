#!/usr/bin/env python
'''
Created on 07/11/2010

@author: mikel
'''
import sys, os.path
os.chdir(os.path.abspath(os.path.dirname(__file__)))

#Search path for dlls/extensions
sys.path.append('../dlls')

#Search path for python libs/eggs
sys.path.append("../libs")

#Put the spotify bindings on the search path also
sys.path.append("../src")

#mandatory libspotify imports
from appkey import appkey
from spotify import session, MainLoop, playlistcontainer, playlist, handle_sp_error
from spotify import BulkConditionChecker, link, artistbrowse, albumbrowse, search, toplistbrowse, inbox, track, link

#Imports for jukebox
import cmd
import threading



class JukeboxCallbacks(session.SessionCallbacks):
    _mainloop = None
    __buf = None
    
    
    def __init__(self, mainloop):
        self._mainloop = mainloop
    
    
    def logged_in(self, session, error):
        handle_sp_error(error)
        print "login successful"  
    
    
    def logged_out(self, session):
        print "logout successful"
    
    
    def connection_error(self, session, error):
        print "conn error"
    
    
    def log_message(self, session, data):
        print "log: %s" % data
    
    
    def notify_main_thread(self, session):
        self._mainloop.notify()
    
    
    def metadata_updated(self, session):
        pass



def print_user(user):
    print "user loaded (cb): %d" % user.is_loaded()



def main():
    print "uses SPOTIFY(R) CORE"
    ml = MainLoop()
    cb = JukeboxCallbacks(ml)
    s = session.Session(
        cb,
        app_key=appkey,
        user_agent="python ctypes bindings",
        settings_location="../tmp/settings",
        cache_location="../tmp/cache",
    )
    
    c = JukeboxCmd(s, ml)
    c.start()
    ml.loop(s)



class JukeboxPlaylistContainerCallbacks(playlistcontainer.PlaylistContainerCallbacks):
    _checker = None
    
    
    def __init__(self, checker):
        self._checker = checker
    
    
    def container_loaded(self, container):
        self._checker.check_conditions()
        
        

#Callback classes for artist loading
class ArtistLoadCallbacks(session.SessionCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def metadata_updated(self, session):
        self.__checker.check_conditions()



class ArtistbrowseLoadCallbacks(artistbrowse.ArtistbrowseCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def artistbrowse_complete(self, artistbrowse):
        self.__checker.check_conditions()



class AlbumLoadCallbacks(session.SessionCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def metadata_updated(self, session):
        self.__checker.check_conditions()



class AlbumbrowseLoadCallbacks(albumbrowse.AlbumbrowseCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def albumbrowse_complete(self, albumbrowse):
        self.__checker.check_conditions()



class SearchLoadCallbacks(search.SearchCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
        
    def search_complete(self, search):
        self.__checker.check_conditions()



class ToplistbrowseLoadCallbacks(toplistbrowse.ToplistbrowseCallbacks):
    __checker = None
    
    
    def __init__(self, checker):
        self.__checker = checker
    
    
    def toplistbrowse_complete(self, toplistbrowse):
        self.__checker.check_conditions()



class InboxLoadCallbacks(inbox.InboxpostCallbacks):
    __event = None
    
    
    def __init__(self, event):
        self.__event = event


    def inboxpost_complete(self, inbox):
        self.__event.set()



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
    
    
    def _load_artist(self, id):
        full_id = "spotify:artist:%s" % id
        checker = BulkConditionChecker()
        
        #Get the artist object
        link_obj = link.create_from_string(full_id)
        artist_obj = link_obj.as_artist()
        
        #Now initialize the artistbrowse load stuff
        callbacks = ArtistbrowseLoadCallbacks(checker)
        artistbrowse_obj = artistbrowse.Artistbrowse(
            self._session, artist_obj, callbacks
        )
        checker.add_condition(artistbrowse_obj.is_loaded)
        checker.complete_wait(10)
        
        return artist_obj, artistbrowse_obj
    
    
    def _load_album(self, id):
        import time
        full_id = "spotify:album:%s" % id
        checker = BulkConditionChecker()
        
        #All the album loading stuff
        link_obj = link.create_from_string(full_id)
        album_obj = link_obj.as_album()
        
        #Now the albumbrowse object
        callbacks = AlbumbrowseLoadCallbacks(checker)
        albumbrowse_obj = albumbrowse.Albumbrowse(
            self._session, album_obj, callbacks
        )
        checker.add_condition(albumbrowse_obj.is_loaded)
        checker.complete_wait(10)
        
        return album_obj, albumbrowse_obj
    
    
    def _load_search(self, query):
        checker = BulkConditionChecker()
        callbacks = SearchLoadCallbacks(checker)
        search_obj = search.Search(
            self._session, query,
            track_count=100, album_count=100, artist_count=100,
            callbacks=callbacks
        )
        checker.add_condition(search_obj.is_loaded)
        checker.complete_wait(10)
        
        return search_obj
    
    
    def _load_toplist(self, type, region, user):
        checker = BulkConditionChecker()
        callbacks = ToplistbrowseLoadCallbacks(checker)
        toplistbrowse_obj = toplistbrowse.Toplistbrowse(
            self._session, type, region, user, callbacks
        )
        checker.add_condition(toplistbrowse_obj.is_loaded)
        checker.complete_wait(10)
        
        return toplistbrowse_obj
    
    
    def _do_inboxpost(self, to_user, track_list, message):
        ev = threading.Event()
        callbacks = InboxLoadCallbacks(ev)
        inbox_obj = inbox.Inbox(
            self._session, to_user, track_list, message, callbacks
        )
        ev.wait(10)
        
    
    def do_artist(self, line):
        args = line.split(' ', 2)
        if len(args) != 1:
            print "this command only takes one argument"
        
        else:
            artist_obj, artistbrowse_obj = self._load_artist(args[0])
            print "artist: %s" % artist_obj.name()
            print " - Albums: %d" % artistbrowse_obj.num_albums()
            print " - Tracks: %d" % artistbrowse_obj.num_tracks()
            print " - Portraits: %d" % artistbrowse_obj.num_portraits()
    
    
    def do_album(self, line):
        args = line.split(' ', 2)
        if len(args) != 1:
            print "this command takes one argument"
        
        else:
            album_obj, albumbrowse_obj = self._load_album(args[0])
            print "album: %s" % album_obj.name()
            print " - Tracks: %d" % albumbrowse_obj.num_tracks()
            print " - Copyrights: %d" % albumbrowse_obj.num_copyrights()
    
    
    def do_search(self, line):
        search_obj = self._load_search(line)
        print "total tracks: %d" % search_obj.total_tracks()
        print "total artists: %d" % search_obj.total_artists()
        print "total albums: %d" % search_obj.total_albums()
        
        if search_obj.did_you_mean() != "":
            print "did you mean: %s" % search_obj.did_you_mean()
    
    
    def do_link(self, line):
        lo = link.create_from_string(line)
        if lo is not None:
            print "link parsed OK"
        else:
            print "failed parsing link"
    
    
    def do_toplist(self, line):
        args = line.split(' ', 4)
        if len(args) != 3:
            print "error: this command takes exactly three arguments"
        else:
            #user arg first
            user_arg = None
        
            #type
            if args[0] == 'artists':
                type_arg = toplistbrowse.ToplistType.Artists
            elif args[0] == 'albums':
                type_arg = toplistbrowse.ToplistType.Albums
            elif args[0] == 'tracks':
                type_arg = toplistbrowse.ToplistType.Tracks
            else:
                print "error: unrecognized toplist type: %s" % args[0]
                return
            
            #region
            if args[1] == 'everywhere':
                region_arg = toplistbrowse.ToplistRegion.Everywhere
            elif args[1] == 'user':
                region_arg = toplistbrowse.ToplistRegion.User
                user_arg = args[2]
            else:
                region_arg = toplistbrowse.encode_region(args[1])
            
            toplistbrowse_obj = self._load_toplist(
                type_arg, region_arg, user_arg
            )
            
            
            if type_arg == toplistbrowse.ToplistType.Artists:
                print "artists: %d" % toplistbrowse_obj.num_artists()
                for idx, item in enumerate(toplistbrowse_obj.artists()):
                    print "#%d: %s" % (idx + 1, item.name())
            
            elif type_arg == toplistbrowse.ToplistType.Albums:
                print "albums: %d" % toplistbrowse_obj.num_albums()
                for idx, item in enumerate(toplistbrowse_obj.albums()):
                    print "#%d: %s by %s" % (idx + 1, item.name(), item.artist().name())
                
            elif type_arg == toplistbrowse.ToplistType.Tracks:
                print "tracks: %d" % toplistbrowse_obj.num_tracks()
                for idx, item in enumerate(toplistbrowse_obj.tracks()):
                    artists = ", ".join([artist.name() for artist in item.artists()])
                    print "#%d: %s by %s" % (idx + 1, item.name(), artists)
    
    
    def do_share(self, line):
        args = line.split(' ', 2)
        to_user = args[0]
        track_ids = args[1].split(',')
        message = args[2]
        track_list = []
        
        for item in track_ids:
            link_obj = link.create_from_string(item)
            track_list.append(link_obj.as_track())
        
        self._do_inboxpost(to_user, track_list, message)
        print "%d track(s) where sent successfully to '%s" % (len(track_list), to_user)
    
    
    def do_set_starred(self, line):
        track_ids = line.split(',')
        track_list = []
        
        for item in track_ids:
            link_obj = link.create_from_string(item)
            track_list.append(link_obj.as_track())
        
        track.set_starred(self._session, track_list, True)
    
    
    def do_list(self, line):
        container = self._session.playlistcontainer()
        
        if not container.is_loaded():
            checker = BulkConditionChecker()
            #Wait until the container is loaded
            checker.add_condition(container.is_loaded)
            callbacks = JukeboxPlaylistContainerCallbacks(checker)
            container.add_callbacks(callbacks)
            checker.complete_wait()
            
            for item in container.playlists():
                item.set_in_ram(self._session, True)
        
        if not line:
            #Print all playlists
            print "%d playlists:" % container.num_playlists()
            
            for k, item in enumerate(container.playlists()):
                if item.is_loaded():
                    print "playlist #%d: %s" % (k, item.name()) 
                else:
                    print "playlist #%d: loading..." % k
        else:
            pos = int(line)
            pl = container.playlist(pos)
            print "playlist #%d, %d tracks:" % (pos, pl.num_tracks())
            
            for index,item in enumerate(pl.tracks()):
                if item.is_loaded():
                    print "track #%d: %s" % (index, item.name())
                    #print item.album().cover()
                else:
                    print "track #%d: loading..." % index
    
    
    do_EOF = do_quit


if __name__ == '__main__':
    main()
