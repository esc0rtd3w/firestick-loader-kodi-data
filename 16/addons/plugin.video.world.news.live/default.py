import os, sys
import cgi
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import logging
logging.basicConfig(level=logging.DEBUG)
import urllib
from utils import urldecode
from channels import *
try:
    from sqlite3 import dbapi2 as sqlite
    
except:
    from pysqlite2 import dbapi2 as sqlite
    
__plugin__ = "World News Live"
__author__ = 'Florian Neagu <michaelneagu@gmail.com>'
__url__ = 'http://world-news-live.googlecode.com/svn/trunk'
__date__ = '1-10-2013'
__version__ = '1.2.7'
__settings__ = xbmcaddon.Addon(id='plugin.video.world.news.live')



class WorldNewsLivePlugin(object):
        
    
    def connect_to_db(self):
        path = xbmc.translatePath('special://profile/addon_data/plugin.video.world.news.live/')
        if not os.path.exists(path):
            os.makedirs(path)
        self.db_conn = sqlite.connect(os.path.join(path, 'custom_streams.db'))
        curs = self.db_conn.cursor()
        curs.execute("""create table if not exists custom_streams (
            id integer primary key,
            name text,
            url text,
            icon text
        )""")
        
        self.db_conn.commit()
        
        
    def get_url(self,urldata):
        """
        Constructs a URL back into the plugin with the specified arguments.
        
        """
        return "%s?%s" % (self.script_url, urllib.urlencode(urldata,1))

    
    def action_add_custom_stream(self):
        
        name = self.get_modal_keyboard_input("Untitled Stream", "Enter a name for the new Stream")
        if name:
            url = self.get_modal_keyboard_input("rtmp://", "Enter the full Stream URL")
            if url:
                icon = self.get_modal_keyboard_input("", "(Optional) Icon Path/URL")
                curs = self.db_conn.cursor()
                curs.execute("insert into custom_streams (name, url, icon) VALUES (?, ?, ?);", (name, url, icon))
                self.db_conn.commit()
        return xbmc.executebuiltin("Container.Refresh")
            
    def action_import_custom_streams(self):
        xmlfile = self.get_dialog().browse(1, "XML File Containing Stream Definitions", 'files')
        soup = BeautifulStoneSoup(open(xmlfile))
        curs = self.db_conn.cursor()
        
        for item in soup.findAll('item'):
            print item
            url = item.link.contents[0].strip()
            name = item.title.contents[0].strip()
            icon = item.thumbnail.contents[0].strip()
            curs.execute("select * from custom_streams where name = ?", (name,))
            if curs.fetchall():
                self.get_dialog().ok('Skipping "%s"', "'%s' already exists in the database")
            else:
                curs.execute("insert into custom_streams (name, url, icon) VALUES (?, ?, ?);", (name,url, icon))
                self.db_conn.commit()
        return xbmc.executebuiltin("Container.Refresh")
            
        
    def action_play_custom_stream(self):
        self.set_stream_url(self.args['stream_url'])
        
    def action_browse_custom_streams(self):
        self.add_list_item({'Title': '[Add New Stream]', 'action': 'add_custom_stream'})
        self.add_list_item({'Title': '[Import Streams from XML]', 'action': 'import_custom_streams'})
        curs = self.db_conn.cursor()
        curs.execute("select id, name, url, icon from custom_streams")
        for row in curs.fetchall():
            data = {}
            data.update(self.args)
            data['action'] = 'play_custom_stream'
            data['stream_url'] = row[2]
            data['Title'] = row[1]
            data['Thumb'] = row[3]
            
            edit_url_url = self.get_url({'action': 'edit_stream_url','id': row[0]})
            edit_name_url = self.get_url({'action': 'edit_stream_name','id': row[0]})
            edit_icon_url = self.get_url({'action': 'edit_stream_icon','id': row[0]})
            delete_stream_url = self.get_url({'action': 'delete_stream','id': row[0]})
            
            cmi = [
                ("Edit Stream URL", "XBMC.RunPlugin(%s)" % (edit_url_url,)),
                ("Edit Stream Name", "XBMC.RunPlugin(%s)" % (edit_name_url,)),
                ("Edit Stream Icon", "XBMC.RunPlugin(%s)" % (edit_icon_url,)),
                ("Delete Stream", "XBMC.RunPlugin(%s)" % (delete_stream_url,))
            ]
            
            self.add_list_item(data, context_menu_items=cmi, clear_context_menu=True, is_folder=False)
        self.end_list()

    def get_custom_stream(self, id):
        curs = self.db_conn.cursor()
        curs.execute("select id, name, url, icon from custom_streams where id = ?", (int(id),))
        row = curs.fetchall()[0]
        return {'id': row[0], 'name': row[1], 'url': row[2], 'icon': row[3]}

    def save_custom_stream(self, stream):
        curs = self.db_conn.cursor()
        curs.execute("update custom_streams set name=?, url=?, icon=? where id=?", (stream['name'], stream['url'], stream['icon'], stream['id']))
        self.db_conn.commit()
        
    def action_edit_stream_url(self):
        stream = self.get_custom_stream(self.args['id'])
        new = self.get_modal_keyboard_input(stream['url'], "Stream URL")
        if new is not None:
            stream['url'] = new
            self.save_custom_stream(stream)
        return xbmc.executebuiltin("Container.Refresh")
        

    def action_edit_stream_name(self):
        stream = self.get_custom_stream(self.args['id'])
        new = self.get_modal_keyboard_input(stream['name'], "Stream Name")
        if new is not None:
            stream['name'] = new
            self.save_custom_stream(stream)
        return xbmc.executebuiltin("Container.Refresh")
        
                        
    def action_edit_stream_icon(self):
        stream = self.get_custom_stream(self.args['id'])
        new = self.get_modal_keyboard_input(stream['icon'], "Icon Path/URL")
        if new is not None:
            stream['icon'] = new
            self.save_custom_stream(stream)
        return xbmc.executebuiltin("Container.Refresh")
        
    def action_delete_stream(self):
        ok = self.get_dialog().yesno("Are you Sure?", "Are you sure you want to delete this custom stream?")
        if ok:
            curs = self.db_conn.cursor()
            curs.execute("delete from custom_streams where id = ?", (int(self.args['id']),))
            self.db_conn.commit()
        return xbmc.executebuiltin("Container.Refresh")

        
    def action_channel_list(self):
        """
        List all registered Channels

        Channels are automatically registered simply by being imported 
        and being subclasses of BaseChannel.
        
        """
        self.add_list_item({'Title': '[My Custom Streams]', 'action':'browse_custom_streams'})
        minimum = int(self.get_setting("worst_channel_support"))
        for channel_code, channel_class in sorted(ChannelMetaClass.registry.channels.iteritems()):
            info = channel_class.get_channel_entry_info()

            # Default to <short_name>.png if no icon is set.
            if info['Thumb'] is None:
                info['Thumb'] = info['channel'] + ".png"

            try:
                info['Thumb'] = self.get_resource_path('images','channels', info['Thumb'])
            except ChannelException:
                logging.warn("Couldn't Find Channel Icon for %s" % (channel_code,))
            
            if channel_class.status >= minimum:
                self.add_list_item(info, is_folder=not channel_class.playable)
        self.end_list()
        
    def get_dialog(self):
        return xbmcgui.Dialog()
    
    def set_stream_url(self, url, info=None):
        """
        Resolve a Stream URL and return it to XBMC. 
        
        'info' is used to construct the 'now playing' information
        via add_list_item.
        
        """
        listitem = xbmcgui.ListItem(label='clip', path=url)
        xbmcplugin.setResolvedUrl(self.handle, True, listitem)
        
        
    
    def end_list(self): 
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle, succeeded=True)


    
    def get_cache_dir(self):
        """
        return an acceptable cache directory.
        
        """
        # I have no idea if this is right.
        path = xbmc.translatePath('special://profile/addon_data/plugin.video.world.news.live/cache/')
        if not os.path.exists(path):
            os.makedirs(path)
        return path


    def get_setting(self, id):
        """
        return a user-modifiable plugin setting.
        
        """
        return __settings__.getSetting(id)


    def add_list_item(self, info, is_folder=True, return_only=False, 
                      context_menu_items=None, clear_context_menu=False, bookmark_parent=None, bookmark_id=None, bookmark_folder_id=None):
        """
        Creates an XBMC ListItem from the data contained in the info dict.
        
        if is_folder is True (The default) the item is a regular folder item
        
        if is_folder is False, the item will be considered playable by xbmc
        and is expected to return a call to set_stream_url to begin playback.

        if return_only is True, the item item isn't added to the xbmc screen but 
        is returned instead.
        
        
        Note: This function does some renaming of specific keys in the info dict.
        you'll have to read the source to see what is expected of a listitem, but in 
        general you want to pass in self.args + a new 'action' and a new 'remote_url'
        'Title' is also required, anything *should* be optional
        
        """
        if context_menu_items is None:
            context_menu_items = []
        
        if bookmark_parent is None:
            bookmark_url = self.get_url({'action': 'add_to_bookmarks', 'url': self.get_url(info)})
#            context_menu_items.append(("Bookmark", "XBMC.RunPlugin(%s)" % (bookmark_url,)))
        else:
            bminfo = {'action': 'remove_from_bookmarks', 'url': self.get_url(info), 'folder_id': bookmark_parent}
            if bookmark_id is not None:
                bminfo['bookmark_id'] = bookmark_id
            elif bookmark_folder_id is not None:
                bminfo['bookmark_folder_id'] = bookmark_folder_id
                
            bookmark_url = self.get_url(bminfo)
#            context_menu_items.append(("Remove From Bookmarks", "XBMC.RunPlugin(%s)" % (bookmark_url,)))
            
        info.setdefault('Thumb', 'None')
        info.setdefault('Icon', info['Thumb'])
        if 'Rating' in info:
            del info['Rating']
        
        li=xbmcgui.ListItem(
            label=info['Title'], 
            iconImage=unicode(info['Icon']), 
            thumbnailImage=info['Thumb']
        )
        
        
        if not is_folder:
            li.setProperty("IsPlayable", "true") 
            context_menu_items.append(("Queue Item", "Action(Queue)"))
        li.setInfo(type='Video', infoLabels=dict((k, unicode(v)) for k, v in info.iteritems()))
        
        # Add Context Menu Items
        if context_menu_items:
            li.addContextMenuItems(context_menu_items, 
                                   replaceItems=clear_context_menu)
            
            
        # Handle the return-early case
        if not return_only:
            kwargs = dict(
                handle=self.handle, 
                url=self.get_url(info),
                listitem=li,
                isFolder=is_folder
            )            
            return xbmcplugin.addDirectoryItem(**kwargs)
        
        return li
        
    def get_resource_path(self, *path):
        """
        Returns a full path to a plugin resource.
        
        eg. self.get_resource_path("images", "some_image.png")
        
        """
        p = os.path.join(__settings__.getAddonInfo('path'), 'resources', *path)
        if os.path.exists(p):
            return p
        raise ChannelException("Couldn't Find Resource: %s" % (p, ))

    def get_modal_keyboard_input(self, default=None, heading=None, hidden=False):
        keyb = xbmc.Keyboard(default, heading, hidden)
        keyb.doModal()
        val = keyb.getText()
        if keyb.isConfirmed():
            return val
        return None
    
        
    def __call__(self):
        """
        This is the main entry point of the plugin.
        the querystring has already been parsed into self.args
        
        """
        
        action = self.args.get('action', None)
        
        if not action:
            action = 'channel_list'
        
        
        if hasattr(self, 'action_%s' % (action,)):
            func = getattr(self, 'action_%s' % (action,))
            return func()
        
        # If there is an action, then there should also be a channel
        channel_code = self.args.get('channel', None)

        # The meta class has a registry of all concrete Channel subclasses
        # so we look up the appropriate one here.
        
        channel_class = ChannelMetaClass.registry.channels[channel_code]
        chan = channel_class(self, **self.args)
        
        return chan()
    
        
    def __init__(self, script_url, handle, querystring):
        proxy = self.get_setting("http_proxy")
        port = self.get_setting("http_proxy_port")
        if proxy and port:
            proxy_handler = urllib2.ProxyHandler({'http':'%s:%s'%(proxy,port)})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)

        self.script_url = script_url
        self.handle = int(handle)
        if len(querystring) > 2:
            self.querystring = querystring[1:]
            items = urldecode(self.querystring)
            self.args = dict(items)
        else:
            self.querystring = querystring
            self.args = {}
        self.connect_to_db()
        logging.debug("Constructed Plugin %s" % (self.__dict__,))
        
if __name__ == '__main__':
    plugin = WorldNewsLivePlugin(*sys.argv)
    plugin()
