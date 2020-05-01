#    Ice Channel

import os
import common
from plugnplay.interfaces import Indexer
from plugnplay.interfaces import Source
from plugnplay.interfaces import CustomSettings
from plugnplay.interfaces import iStreamSettings

srcr_count = 0
srcr_loop = 0
srcr_url_to_name_map = {}

iStream_settings = {}
def loadiStreamSettings():
    for cs in iStreamSettings.implementors(): 
        cs.Initialize()
        iStream_settings[cs.type] = cs
    import xbmc
    xbmc.executebuiltin('UpdateLocalAddons ')
'''
def AddIndexerToPluginLoad(type, types=[])    
    for indxr in Indexer.implementors():
        if indxr.indexer_type == type:
            types.append(indxr)
            break
            
def AddSourceToPluginLoad(type, types=[])    
    for src in Source.implementors():
        if src.source_type == type:
            types.append(src)
            break            
            
def AddiStreamSettingsToPluginLoad(types=[])
    from plugnplay.interfaces import iStreamSettings
    types.append(iStreamSettings)
    
def AddProxyToPluginLoad(types=[], load_webproxyproviders=True, load_proxysupportedplugins=True):
    if load_webproxyproviders == True:
        from entertainment.plugnplay.interfaces import WebProxy
        types.append(WebProxy)        
    if load_proxysupportedplugins == True:
        from entertainment.plugnplay.interfaces import ProxySupport        
        types.append(ProxySupport)

def loadiStreamSettingsSection(type, load_indexer=True, load_source=True):
    
    types=[]
    
    if type in ( common.settings_Movies, common.settings_TV_Shows, common.settings_Sports, common.settings_Lists, common.settings_Live_TV):
        if load_indexer==True: AddIndexerToPluginLoad(type, types)
        if load_source==True: AddSourceToPluginLoad(type, types)
        AddProxyToPluginLoad(types, True, False)
        
    elif type in ( common.settings_Internet_Connection ):
        AddProxyToPluginLoad(types, True, True)
    
    AddiStreamSettingsToPluginLoad(types)
    
    common.loadplugins(types)
    
    loadiStreamSettings()
    
def loadResolvers(type):
    from entertainment.plugnplay.interfaces import ProxySupport        
    from entertainment.plugnplay.interfaces import WebProxy
    types=[WebProxy]
    if type in ( common.settings_Movies, common.settings_TV_Shows, common.settings_Sports, common.settings_Lists, common.settings_Live_TV):
        for indxr in Indexer.implementors():
            if indxr.indexer_type == type:
                types.append(indxr)
                break
        for src in Source.implementors():
            if src.source_type == type:
                types.append(src)
                break        
    elif type in ( common.settings_Internet_Connection ):
        from entertainment.plugnplay.interfaces import ProxySupport        
        types.append(ProxySupport)
    if type in ( common.src_Movies, common.src_TV_Shows, 'file_stores'):
        from entertainment.plugnplay.interfaces import HostResolver
        from entertainment.plugnplay.interfaces import PremiumHostResolver
        from entertainment.plugnplay.interfaces import CaptchaHandler
        types.extend([HostResolver,PremiumHostResolver,CaptchaHandler])
    elif type in ( common.src_Sports, common.src_Live_TV):
        from entertainment.plugnplay.interfaces import LiveResolver
        types.append(LiveResolver)
    common.loadplugins(types)
    loadiStreamSettings()
    
def loadFileFormats():
    from entertainment.plugnplay.interfaces import ProxySupport        
    from entertainment.plugnplay.interfaces import WebProxy
    from entertainment.plugnplay.interfaces import FileFormat
    common.loadplugins([ProxySupport, WebProxy, FileFormat])
    loadiStreamSettings()
'''

def PreLoadiStreamPluginsThreaded():    
    try:
        import Queue as queue
    except:
        import queue
    message_queue = queue.Queue()
    
    import threading
    threading.Thread(target=PreLoadiStreamPlugins, args=(message_queue,)).start()
    
    return message_queue

def PreLoadiStreamPlugins(message_queue=None):
    loadiStreamPlugins()
    common.PreLoadiStreamPlugins(message_queue)

def loadiStreamPlugins(load_settingsxml=True, type=None, load_indexer=False, load_source=False, load_settings=False, load_resolvers=False, 
        load_proxysupportedplugins=False, load_webproxyproviders=False, load_fileformats=False, load_extnstoreconcrete=False, load_extnstoresearch=False):
    
    if load_settingsxml==True:
        common._update_settings_xml()
    
    types=[]
    
    if type:
        if type in ( common.settings_Movies, common.settings_TV_Shows, common.settings_Sports, common.settings_Lists, common.settings_Live_TV, 'file_stores'):
            if load_indexer==True: 
                for indxr in Indexer.implementors():
                    if indxr.indexer_type == type:
                        types.append(indxr)
                        break
            if load_source==True: 
                for src in Source.implementors():
                    if src.source_type == type:
                        types.append(src)
                        break 

            if load_resolvers==True:
                if type in ( common.src_Movies, common.src_TV_Shows, 'file_stores'):
                    from entertainment.plugnplay.interfaces import HostResolver, PremiumHostResolver, CaptchaHandler
                    types.extend([HostResolver,PremiumHostResolver,CaptchaHandler])
                elif type in ( common.src_Sports, common.src_Live_TV):
                    from entertainment.plugnplay.interfaces import LiveResolver
                    types.append(LiveResolver)
        elif type in ( common.settings_Internet_Connection, ):
            load_proxysupportedplugins=True
            load_webproxyproviders=True
            
    if load_settings==True:
        from plugnplay.interfaces import iStreamSettings
        types.append(iStreamSettings)
        
    if load_proxysupportedplugins==True:
        from entertainment.plugnplay.interfaces import ProxySupport        
        types.append(ProxySupport)
        
    if  load_webproxyproviders==True:
        from entertainment.plugnplay.interfaces import WebProxy        
        types.append(WebProxy)
        
    if load_fileformats==True:
        from entertainment.plugnplay.interfaces import FileFormat        
        types.append(FileFormat)
        
    if load_extnstoreconcrete==True:
        from entertainment.plugnplay.interfaces import ExtensionStoreConcrete
        types.append(ExtensionStoreConcrete)
        
    if load_extnstoresearch==True:
        from entertainment.plugnplay.interfaces import ExtensionStoreSearch
        types.append(ExtensionStoreSearch)
        
    common.loadpluginsNew(types)
    
    if load_settings==True:
        loadiStreamSettings()
        
def Initialize():  

    #from multiprocessing.pool import ThreadPool as Pool    
    from threadpool import ThreadPool as Pool
    pool = Pool(2)
    
    import threading
    lock = threading.RLock()    
    
    try:
        import Queue as queue
    except:
        import queue
    message_queue = queue.Queue()
    
    list=[]
    
    unique_list=[]
    
    return (pool, list, unique_list, lock, message_queue)

def Destroy(pool):
    pool.dismissWorkers(4, True)
    
def FinalizeSearch(pool, item_list, unique_list, message_queue):

    pool.wait()
    
    import threading
    threading.Thread(target=Destroy, args=(pool, )).start()
        
    import odict
    temp_dict = odict.odict()

    for item in item_list:        

        if item['id'].endswith('_info'):
        
            info_temp_dict_item = temp_dict.get('info', '')
            if info_temp_dict_item == '':
                item.update( { 'individual_total_pages': {} } )
                #item.update( { 'urls': {} } )
                temp_dict[ 'info' ] = item
                info_temp_dict_item = temp_dict[ 'info' ]
                            
            info_temp_dict_item['individual_total_pages'].update( {item['website']:item['total_pages']} )
                        
            #info_temp_dict_item['urls'].update( {item['website']:item['url']} )
            
            if int(item['total_pages']) > int(info_temp_dict_item['total_pages']):
                info_temp_dict_item['total_pages'] = item['total_pages']
        
        else:
            temp_dict_item = temp_dict.get(item['id'], '')
            if temp_dict_item == '':
                item.update( { 'urls': {} } )                
                temp_dict[ item['id'] ] = item
                temp_dict_item = temp_dict[ item['id'] ]
                
            temp_dict_item['urls'].update({item['website']:item['url']})
    
    for value in temp_dict.values():
        urls = value.get('urls', '')
        if urls != '':
            value['urls'] = common.ConvertDictToString(urls)
            
        individual_total_pages = value.get('individual_total_pages', '')
        if individual_total_pages != '':
            value['individual_total_pages'] = common.ConvertDictToString(individual_total_pages)

        unique_list.append( value )
        
    message_queue.put('done')
    
def FinalizeBasic(pool, item_list, unique_list, lock, message_queue):
    pool.wait()
    
    import threading
    threading.Thread(target=Destroy, args=(pool, )).start()
    
    message_queue.put('done')
    
def FinalizeExtnList(pool, item_list, unique_list, lock, message_queue):
    pool.wait()
    
    import threading
    threading.Thread(target=Destroy, args=(pool, )).start()
    
    if 'FEATURE_NOT_SUPPORTED' in str(item_list) or len(item_list) <= 0:
        unique_list.insert(0, {'mode': 'FEATURE_NOT_SUPPORTED'} )
    else:
        extns_processed = {}
        
        for extn in item_list:
            if extn.get('extn_id', None) == None: continue
            if extns_processed.get(extn['extn_id'], None) == None:
                extns_processed.update({extn['extn_id'] : extn})
            elif extns_processed[ extn['extn_id'] ]['extn_version'] < extn['extn_version']:
                extns_processed.update({extn['extn_id'] : extn})

        unique_list.extend( extns_processed.values() )
        
        unique_list.sort(key=lambda k: common.custom_item_sort(k['extn_name']))
        
        if item_list[0].get('extn_id', None) == None:
            unique_list.insert( 0, item_list[0] )
    
    message_queue.put('done')    

    
def FinalizeGetAddonsXMLAndMD5(pool, item_list, unique_list, lock, message_queue):
    pool.wait()
    
    extns_list=[]
    extns_list.append(item_list[0])
    
    from threadpool import WorkRequest
    from entertainment.plugnplay.interfaces import ExtensionStoreSearch
    
    for item in item_list:
        if item.get('addons_xml', None) == None: continue
        for store in ExtensionStoreSearch.implementors(): 
            if store.name == item['website']:
                pool.putRequest( WorkRequest( store.LoadiStreamStoreAndExtensions, args=(item['addons_xml'], item['addons_xml_md5'], extns_list, lock, message_queue) ) )
        
    import threading
    threading.Thread(target=FinalizeExtnList, args=(pool, extns_list, unique_list, lock, message_queue)).start()
    
def FinalizeSearchForExtensions(pool, item_list, unique_list, lock, message_queue):
    pool.wait()
    
    addons_xml_list = []
    
    from threadpool import WorkRequest
    from entertainment.plugnplay.interfaces import ExtensionStoreSearch
    
    for item in item_list:
        if item.get('id', '').endswith('_info'):
            if len(addons_xml_list) <= 0:
                addons_xml_list.append( {'page':item['page'], 'total_pages':item['total_pages'], 'individual_total_pages' : {} } )
            addons_xml_list[0]['individual_total_pages'].update( {item['website']:item['total_pages']} )
            if int(item['total_pages']) > int(addons_xml_list[0]['total_pages']):
                addons_xml_list[0].update( { 'total_pages' : item['total_pages'] } )
                
    for item in item_list:
        if item.get('id', '').endswith('_info'): continue
        for store in ExtensionStoreSearch.implementors(): 
            if store.name == item['website']:
                pool.putRequest( WorkRequest( store.GetAddonsXMLAndMD5, args=(item['url'], addons_xml_list, lock, message_queue) ) )
        
    import threading
    threading.Thread(target=FinalizeGetAddonsXMLAndMD5, args=(pool, addons_xml_list, unique_list, lock, message_queue)).start()
        
def Finalize(pool, src_type, item_list, unique_list, message_queue):

    try:
        pool.wait()
    except:
        pass
    
    import xbmc
    xbmc.sleep(1000)
    
    import threading
    threading.Thread(target=Destroy, args=(pool, )).start()
    sort = GetiStreamSettings(src_type, 'sort')
    if sort == "true":
    
        sort_quality_ranking = {}
        sort_qualities = GetiStreamSettings(src_type, 'sort_quality')        
        sort_qualities_list = sort_qualities.split(',')
        sort_quality_index = 1
        for sort_quality in sort_qualities_list:
            if sort_quality:
                sort_quality_ranking.update({sort_quality.upper() : sort_quality_index * 10000})
                sort_quality_index += 1
        na_sort_quality_ranking = sort_quality_index * 10000
        
        import re
        
        sort_hosts = ''
        sort_host_ranking = {}
        hosts_input_fields = 5
        for x in range(0,5):
            hosts_at_x = GetiStreamSettings(src_type, 'sort_hosts_' + str(x+1))
            if hosts_at_x:
                if sort_hosts:
                    sort_hosts += ','
                sort_hosts += hosts_at_x        
        sort_hosts_list = sort_hosts.split(',')
        sort_host_index = 1
        for sort_host in sort_hosts_list:
            if sort_host:
                sort_host_ranking.update({sort_host.upper() : sort_host_index * 100})
                sort_host_ranking.update({re.sub('\..*', '', sort_host.upper()) : sort_host_index})
                sort_host_index += 1
        na_sort_host_ranking = sort_host_index * 100
    
    import odict
    
    message_queue.put({'message':'Removing duplicate links...'})
    xbmc.sleep(1000)
    for unique_item in odict.odict((item['id'],item) for item in item_list).values():
        if sort == "true":
            item_quality_ranking = sort_quality_ranking.get( unique_item.get('quality', 'NA'),  na_sort_quality_ranking )
            item_host_ranking = sort_host_ranking.get( unique_item.get('host', 'NA'),  na_sort_host_ranking )
            if item_host_ranking == na_sort_host_ranking:
                item_host_ranking = sort_host_ranking.get( unique_item.get('website', 'NA').upper(),  na_sort_host_ranking )
            item_ranking = item_quality_ranking + item_host_ranking
            unique_item.update( { 'ranking' : item_ranking } )
        unique_list.append( unique_item )
    message_queue.put({'message':'Unique links retrieved: ' + str(len(unique_list))})
    xbmc.sleep(1000)
    if sort == "true":
        message_queue.put({'message':'Sorting links...'})        
        unique_list.sort(key=lambda k: k['ranking'])
        xbmc.sleep(1000)
    
    message_queue.put('done')
    
def LoadExtensionStore():
    
    loadiStreamPlugins(load_settingsxml=True, load_settings=True, load_proxysupportedplugins=True, load_webproxyproviders=True, 
        load_extnstoreconcrete=True)
    
    (pool, list, unique_list, lock, message_queue) = Initialize()
    
    from threadpool import WorkRequest
    from entertainment.plugnplay.interfaces import ExtensionStoreConcrete
    
    for store in ExtensionStoreConcrete.implementors(): 
        pool.putRequest( WorkRequest(store.LoadStoreAndExtensions, args=(list, lock, message_queue)))
        
    import threading
    threading.Thread(target=FinalizeExtnList, args=(pool, list, unique_list, lock, message_queue)).start()
    
    return (unique_list, message_queue)
    
def SearchForExtensions(page='', total_pages='', individual_total_pages=''):
    
    loadiStreamPlugins(load_settingsxml=True, load_settings=True, load_proxysupportedplugins=True, load_webproxyproviders=True, 
        load_extnstoresearch=True)
    
    (pool, list, unique_list, lock, message_queue) = Initialize()
    
    import odict
    
    from threadpool import WorkRequest
    from entertainment.plugnplay.interfaces import ExtensionStoreSearch
    
    ssi_count =  len( ExtensionStoreSearch.implementors() )
    if ssi_count <= 0: return None
    ssi_count = ssi_count * 4
    ssi_step = 50 / ssi_count
    
    list_item_count = 0
    
    import xbmc
    
    for store in ExtensionStoreSearch.implementors(): 
    
        message_queue.put( {'percent_step':ssi_step, 
            'line1':'Searching for third party extensions... ', 
            'line2':'[B]Searching: [COLOR gold]%s (%s)[/COLOR][/B]' % (store.display_name, store.name), 
            'line3':' ',
            'wait_time':1000
            } )
            
        store_total_pages=''
        if isinstance(individual_total_pages, odict.odict) or isinstance(individual_total_pages, dict):
            store_total_pages = individual_total_pages.get(store.name, '')
        #pool.putRequest( WorkRequest( store.Search, args=(list, lock, message_queue, page, store_total_pages) ) )
        store.Search(list, lock, message_queue, page, store_total_pages)
        
        message_queue.put( {'line1':'Searching for third party extensions... ', 
            'line2':'[B]Searching: [COLOR gold]%s (%s)[/COLOR][/B]' % (store.display_name, store.name), 
            'line3':'[I][COLOR gray]Found: %s source(s)[/COLOR][/I]' % str( len(list) - list_item_count - 1 ),
            'wait_time':1000
            } )
        
        list_item_count = len(list)
        
    message_queue.put( {'line1':'Searching for third party extensions... ', 
        'line2':'[B][COLOR gold]Retrieving Extensions from source(s)[/COLOR][/B]', 
        'line3':' ',
        'wait_time':1000
        } )
        
    import threading
    threading.Thread(target=FinalizeSearchForExtensions, args=(pool, list, unique_list, lock, message_queue)).start()
    
    return (unique_list, message_queue)

    
def GetMainSection():
    unique_list = []      
    
    unique_list.append( {'title':'myStream', 'mode':common.mode_MyStream, 'indexer':'mystream', 'section':'mystream',
                                            'img':common.get_themed_icon('mystream.png'),
                                            'fanart':common.get_themed_fanart('mystream.jpg')
                                            } )    
    
    for indxr in Indexer.implementors(): 
        #stg = iStream_settings.get(indxr.indexer_type, None)

        #if stg is not None:
        #    for indxrtyp in indxr.implementors():
        #        if stg.Settings().get_setting(indxr.indexer_type + '_' + indxrtyp.name + '_indexer_enabled') == 'true':
        unique_list.append( {   'indexer':indxr.indexer_type, 
                                'section':'main', 
                                'title':indxr.indexer_section_name, 
                                'mode':common.mode_Indexer,
                                'img':common.get_themed_icon(indxr.indexer_type+'.png'),
                                'fanart':common.get_themed_fanart(indxr.indexer_type+'.jpg')
                                } )    
        #            break
    
    unique_list.append( {'title':'Playlists', 'mode':common.mode_File_Stores, 'indexer':'file_stores', 'section':'file_stores',
                                            'img':common.get_themed_icon('playlists.png'),
                                            'fanart':common.get_themed_fanart('playlists.jpg')
                                            } )    
    unique_list.append( {'title':'Search', 'mode':common.mode_Search, 'indexer':'search', 'section':'search', 
                                            'img':common.get_themed_icon('search.png'),
                                            'fanart':common.get_themed_fanart('search.jpg')
                                            } )    
    unique_list.append( {'title':'Settings', 'mode':common.mode_Settings, 'indexer':'settings', 'section':'settings',
                                            'img':common.get_themed_icon('settings.png'),
                                            'fanart':common.get_themed_fanart('settings.jpg')
                                            } )        
    unique_list.append( {'title':'Tools', 'mode':common.mode_Tools, 'indexer':'tools', 'section':'tools',
                                            'img':common.get_themed_icon('tools.png'),
                                            'fanart':common.get_themed_fanart('tools.jpg')  
                                            } )        
                                            
    '''unique_list.append( {'title':'Extensions Installer', 'mode':common.mode_Installer, 'indexer':'installer', 'section':'installer',
                                            'img':common.get_themed_icon('installer.png'),
                                            'fanart':common.get_themed_fanart('installer.jpg')  
                                            } ) '''       
                                            
    unique_list.append( {'title':'View End User Agreement', 'mode':common.mode_EULA, 'indexer':'eula', 'section':'eula',
                                            'img':common.get_themed_icon('eula.png'),
                                            'fanart':common.get_themed_fanart('eula.jpg')  
                                            } )        
    return unique_list
    
def GetSearchItem(indexer):    

    unique_list = []
    
    for indxr in Indexer.implementors(): 
        if indxr.indexer_type == indexer:
            if indxr.search_supported:
                unique_list.append( {'indexer':indxr.indexer_type, 'indexer_id':'search', 'section':'search', 'title':'Search', 'mode':common.mode_Search,
                                            'img':common.get_themed_icon('search_'+indxr.indexer_type+'.png'),
                                            'fanart':common.get_themed_fanart('search_'+indxr.indexer_type+'.jpg')  
                                            } )    
            break
            
    return unique_list
    
def GetAllSearchItems():    
    unique_list = []
    
    for indxr in Indexer.implementors(): 
        if indxr.search_supported:
            unique_list.append( {'indexer':indxr.indexer_type, 'indexer_id':'search', 'section':'search', 'title':'Search ' + indxr.indexer_section_name, 
                                            'mode':common.mode_Search,
                                            'img':common.get_themed_icon('search_'+indxr.indexer_type+'.png'),
                                            'fanart':common.get_themed_fanart('search_'+indxr.indexer_type+'.jpg')
                                            } )    
            
    return unique_list
    
def GetIndexers(indexer):
    unique_list = []      
    
    stg = iStream_settings.get(indexer, None)
    if not stg:
        return unique_list
    
    for indxr in Indexer.implementors():
        if indxr.indexer_type == indexer:
            for indxrtyp in indxr.implementors():
                if stg.Settings().get_setting(indxr.indexer_type + '_' + indxrtyp.name + '_indexer_enabled') == 'true':
                    unique_list.append( 
                        {
                            'indexer':indxr.indexer_type, 
                            'indexer_id':indxrtyp.name, 
                            'section':'main', 
                            'title':indxrtyp.display_name, 
                            'mode':common.mode_Sports if indexer == common.indxr_Sports else ( common.mode_Live_TV if indexer == common.indxr_Live_TV else common.mode_Section ),
                            'img':common.get_themed_icon(indxrtyp.name + '.png') if common.get_themed_icon(indxrtyp.name + '.png') else indxrtyp.img,
                            'fanart':common.get_themed_fanart(indxrtyp.name + '.jpg') if common.get_themed_fanart(indxrtyp.name + '.jpg') else indxrtyp.fanart,
                            'other_names':indxrtyp.other_names if indexer == common.indxr_Live_TV else '',
                            'region':indxrtyp.get_regions_csv() if indexer == common.indxr_Live_TV else '',
                            'language':indxrtyp.get_languages_csv() if indexer == common.indxr_Live_TV else '',
                            'genre':indxrtyp.get_genres_csv() if indexer == common.indxr_Live_TV else '',
                        } )
                        
            break
                    
    return unique_list

def GetSettings():
    unique_list = []      

    for cs in CustomSettings.implementors(): 
        unique_list.append( {'settings_name':cs.settings_name, 'settings_id':cs.settings_id} )
        
    return unique_list
    
def GetExternalSettings():
    unique_list = []      
    
    unique_list.append( {'settings_name':'Metahandler', 'settings_id':'script.module.metahandler'} )
    unique_list.append( {'settings_name':'Universal Toolkit', 'settings_id':'script.module.universal'} )
    unique_list.append( {'settings_name':'URL Resolver', 'settings_id':'script.module.urlresolver'} )
        
    return unique_list

def GetSettingsSections(section = 'main'):
    
    unique_list = []      
    
    if not section: section = 'main'
    
    if section == 'main':
        unique_list.append( { 'id' : 'istream',         'name' : 'iStream', 'img':common.get_themed_icon('settings_istream.png'), 'fanart':common.get_themed_fanart('settings_istream.jpg') } )
        unique_list.append( { 'id' : 'movies',          'name' : 'Movies', 'img':common.get_themed_icon('settings_movies.png'), 'fanart':common.get_themed_fanart('settings_movies.jpg') } )
        unique_list.append( { 'id' : 'tvshows',         'name' : 'TV Shows', 'img':common.get_themed_icon('settings_tv_shows.png'), 'fanart':common.get_themed_fanart('settings_tv_shows.jpg') } )
        #unique_list.append( { 'id' : 'livetv',          'name' : 'Live TV', 'img':common.get_themed_icon('live_tv_settings.png'), 'fanart':common.get_themed_fanart('live_tv_settings.jpg') } )
        #unique_list.append( { 'id' : 'livesports',      'name' : 'Sports (Live)', 'img':common.get_themed_icon('live_sports_settings.png'), 'fanart':common.get_themed_fanart('live_sports_settings.jpg') } )
        unique_list.append( { 'id' : 'resolvers',       'name' : 'Resolvers', 'img':common.get_themed_icon('settings_resolvers.png'), 'fanart':common.get_themed_fanart('settings_resolvers.jpg') } )
        unique_list.append( { 'id' : 'prm_resolvers',   'name' : 'Premium Resolvers', 'img':common.get_themed_icon('resolvers_settings_prm.png'), 'fanart':common.get_themed_fanart('resolvers_settings_prm.jpg') } )
        unique_list.append( { 'id' : 'external',        'name' : 'External', 'img':common.get_themed_icon('settings_external.png'), 'fanart':common.get_themed_fanart('settings_external.jpg') } )
    
    elif section == 'istream':
        loadiStreamPlugins(load_settingsxml=False, load_settings=True)
        unique_list.append( {'name':'General', 'id':'script.icechannel', 'img':common.get_themed_icon('settings_istream.png'), 'fanart':common.get_themed_fanart('settings_istream.jpg') } )
        for cs in iStreamSettings.implementors(): 
            unique_list.append( {'name':cs.name, 'type':cs.type, 'id':cs.settings_id, 'img':common.get_themed_icon('settings_istream.png'), 'fanart':common.get_themed_fanart('settings_istream.jpg') } )
            
    elif section == 'movies':
        unique_list.append( {'name':'General', 'type':common.settings_Movies, 'id':'script.icechannel.iStream.movies.settings', 'img':common.get_themed_icon('settings_movies.png'), 'fanart':common.get_themed_fanart('settings_movies.jpg') } )
        from plugnplay.interfaces import MovieIndexer, MovieSource
        common.loadplugins([MovieIndexer,MovieSource])
        csi = CustomSettings.implementors()
        csi.sort(key=lambda k: common.custom_item_sort(k.name))
        for cs in csi:
            if isinstance(cs, MovieIndexer) or isinstance(cs, MovieSource):
                unique_list.append( {'name':cs.settings_name, 'id':cs.settings_id, 'img':common.get_themed_icon('settings_movies.png'), 'fanart':common.get_themed_fanart('settings_movies.jpg')} )
        
    elif section == 'tvshows':
        unique_list.append( {'name':'General', 'type':common.settings_TV_Shows, 'id':'script.icechannel.iStream.tv_shows.settings', 'img':common.get_themed_icon('settings_tv_shows.png'), 'fanart':common.get_themed_fanart('settings_tv_shows.jpg') } )
        from plugnplay.interfaces import TVShowIndexer, TVShowSource
        common.loadplugins([TVShowIndexer,TVShowSource])
        csi = CustomSettings.implementors()
        csi.sort(key=lambda k: common.custom_item_sort(k.name))
        for cs in csi:
            if isinstance(cs, TVShowIndexer) or isinstance(cs, TVShowSource):
                unique_list.append( {'name':cs.settings_name, 'id':cs.settings_id, 'img':common.get_themed_icon('settings_tv_shows.png'), 'fanart':common.get_themed_fanart('settings_tv_shows.jpg')} )
        
    elif section == 'livetv':
        unique_list.append( {'name':'General', 'type':common.settings_Live_TV, 'id':'script.icechannel.iStream.live_tv.settings', 'img':common.get_themed_icon('live_tv_general_settings.png'), 'fanart':common.get_themed_icon('live_tv_general_settings.jpg') } )
        from plugnplay.interfaces import LiveTVIndexer, LiveTVSource
        common.loadplugins([LiveTVIndexer,LiveTVSource])
        csi = CustomSettings.implementors()
        csi.sort(key=lambda k: common.custom_item_sort(k.name))
        for cs in csi:
            if isinstance(cs, LiveTVIndexer) or isinstance(cs, LiveTVSource):
                unique_list.append( {'name':cs.settings_name, 'id':cs.settings_id, 'img':cs.settings_img, 'fanart':cs.settings_fanart} )
                
    elif section == 'livesports':
        unique_list.append( {'name':'General', 'type':common.settings_Sports, 'id':'script.icechannel.iStream.sports.settings', 'img':common.get_themed_icon('live_tv_general_settings.png'), 'fanart':common.get_themed_icon('live_sports_general_settings.jpg') } )
        from plugnplay.interfaces import SportsIndexer, SportsSource
        common.loadplugins([SportsIndexer,SportsSource])
        csi = CustomSettings.implementors()
        csi.sort(key=lambda k: common.custom_item_sort(k.name))
        for cs in csi:
            if isinstance(cs, SportsIndexer) or isinstance(cs, SportsSource):
                unique_list.append( {'name':cs.settings_name, 'id':cs.settings_id, 'img':cs.settings_img, 'fanart':cs.settings_fanart} )
                
    elif section == 'resolvers':
        unique_list.append( {'name':'URL Resolver', 'id':'script.module.urlresolver', 'img':common.get_themed_icon('settings_resolvers.png'), 'fanart':common.get_themed_fanart('settings_resolvers.jpg')} )
        from plugnplay.interfaces import HostResolver, LiveResolver
        common.loadplugins([HostResolver,LiveResolver])
        csi = CustomSettings.implementors()
        csi.sort(key=lambda k: common.custom_item_sort(k.name))
        for cs in csi:
            if isinstance(cs, HostResolver) or isinstance(cs, LiveResolver):
                unique_list.append( {'name':cs.settings_name, 'id':cs.settings_id, 'img':common.get_themed_icon('settings_resolvers.png'), 'fanart':common.get_themed_fanart('settings_resolvers.jpg')} )
                
    elif section == 'prm_resolvers':
        from plugnplay.interfaces import PremiumHostResolver
        common.loadplugins([PremiumHostResolver])
        csi = CustomSettings.implementors()
        csi.sort(key=lambda k: common.custom_item_sort(k.name))
        for cs in csi:
            if isinstance(cs, PremiumHostResolver):
                unique_list.append( {'name':cs.settings_name, 'id':cs.settings_id, 'img':common.get_themed_icon('resolvers_settings_prm.png'), 'fanart':common.get_themed_fanart('resolvers_settings_prm.jpg')} )
        
                
    elif section == 'external':
        unique_list.append( {'name':'Metahandler', 'id':'script.module.metahandler', 'img':common.get_themed_icon('settings_external.png'), 'fanart':common.get_themed_fanart('settings_external.jpg')} )
        unique_list.append( {'name':'Universal Toolkit', 'id':'script.module.universal', 'img':common.get_themed_icon('settings_external.png'), 'fanart':common.get_themed_fanart('settings_external.jpg')} )
        unique_list.append( {'name':'URL Resolver', 'id':'script.module.urlresolver', 'img':common.get_themed_icon('settings_external.png'), 'fanart':common.get_themed_fanart('settings_external.jpg')} )
        
    if section not in ('main', 'istream', 'external',):
        import xbmc
        xbmc.executebuiltin('UpdateLocalAddons ')
            
    return unique_list
    
def GetiStreamSettings(type=None, id=None):
    if type and id:
        xs = iStream_settings.get(type, None)
        if xs:
            return xs.Settings().get_setting(id)
            
        else:
            return ''
    else:
        unique_list = []  

        unique_list.append( {'settings_name':'General', 'settings_id':'script.icechannel', 'img':common.get_themed_icon('istream_settings.png'), 'fanart':common.get_themed_fanart('istream_settings.jpg') } )
        
        for cs in iStreamSettings.implementors(): 
            unique_list.append( {'settings_name':cs.name, 'settings_id':cs.settings_id, 'img':common.get_themed_icon('istream_settings.png'), 'fanart':common.get_themed_fanart('istream_settings.jpg') } )
            
        return unique_list
        
def SetiStreamSettings(type, id, value):
    xs = iStream_settings.get(type, None)
    if xs:
        xs.Settings().set_setting(id, value)
    
def Search(indexer, keywords, type, page='', total_pages='', individual_total_pages=''):
    
    if individual_total_pages != '':
        individual_total_pages = common.ConvertStringToDict(individual_total_pages)    
    
    (pool, list, unique_list, lock, message_queue) = Initialize()
    
    from threadpool import WorkRequest
    
    processed_items =[]

    loadiStreamPlugins(type=indexer, load_indexer=True, load_source=True, load_settings=True, load_webproxyproviders=True, load_fileformats=True)
    
    stg = iStream_settings.get(indexer, None)
    if stg:
        for indx in Indexer.implementors(): 
            if indx.indexer_type == indexer: 
                if indx.indexer_type in (common.indxr_Live_TV):
                    indx.Search(indexer, keywords, type, list, lock, message_queue, page, total_pages)
                else:
                    for indxr in indx.implementors():
                        if indxr.name not in processed_items:                        
                            indxr_enabled = stg.Settings().get_setting(indx.indexer_type + '_' + indxr.name + '_indexer_enabled')
                            if indxr_enabled == 'true':
                                processed_items.append(indxr.name)
                                if individual_total_pages != '':
                                    indxr_individual_total_pages = individual_total_pages.get(indxr.name, '')
                                    if indxr_individual_total_pages:                            
                                        pool.putRequest( WorkRequest(indxr.Search, args=(indexer, keywords, type, list, lock, message_queue, page, indxr_individual_total_pages)))
                                elif total_pages == '':                    
                                    pool.putRequest( WorkRequest(indxr.Search, args=(indexer, keywords, type, list, lock, message_queue, page, total_pages)) )
                break
        
        if indexer not in (common.indxr_Live_TV) or (indexer in (common.indxr_Live_TV) and len(list) <= 0):

            for src in Source.implementors(): 
                if src.source_type == indexer:
                    for srcr in src.implementors():
                        if srcr.name not in processed_items:                        
                            srcr_enabled = stg.Settings().get_setting(src.source_type + '_' + srcr.name + '_source_enabled')
                            if srcr_enabled == 'true':
                                processed_items.append(srcr.name)
                                if individual_total_pages != '':
                                    srcr_individual_total_pages = individual_total_pages.get(srcr.name, '')
                                    if srcr_individual_total_pages:                            
                                        pool.putRequest( WorkRequest(srcr.Search, args=(indexer, keywords, type, list, lock, message_queue, page, srcr_individual_total_pages)))
                                elif total_pages == '':    
                                    pool.putRequest( WorkRequest(srcr.Search, args=(indexer, keywords, type, list, lock, message_queue, page, total_pages)) )
                    break
    
    import threading
    threading.Thread(target=FinalizeSearch, args=(pool, list, unique_list, message_queue)).start()
    
    return (unique_list, message_queue)


def GetSection(indexer, indexer_to_use, section, url, type, page='', total_pages='', sort_by='', sort_order=''): 

    unique_list = []
    meta = []
    
    the_indexer = None
    
    for indxr in Indexer.implementors(): 
        if indxr.indexer_type == indexer: 
            for indxrtyp in indxr.implementors():
                if indxrtyp.name == indexer_to_use:
                    the_indexer = indxrtyp
                    break
            break
            
    if the_indexer:
        the_indexer.GetSection(indexer, section, url, type, unique_list, page=page, total_pages=total_pages, sort_by=sort_by, sort_order=sort_order)
    
    return (unique_list, meta)
    
def GetContent(indexer, indexer_to_use, url, title, name, year, season, episode, type, urls=None):
    
    if urls:
        urls = common.ConvertStringToDict(urls)
        
        if len(urls) > 1:
        
            processed_items =[]
            
            loadiStreamSettings()
            stg = iStream_settings.get(indexer, None)
        
            (pool, list, unique_list, lock, message_queue) = Initialize()
            from threadpool import WorkRequest
            
            for indxr in Indexer.implementors(): 
                if indxr.indexer_type == indexer: 
                    for url_key, url_value in urls.items():
                        for indxrtyp in indxr.implementors():
                            prcsd = '%s_%s' % (url_key, indxrtyp.name)
                            if prcsd not in processed_items:                        
                                indxr_enabled = stg.Settings().get_setting(indxr.indexer_type + '_' + indxrtyp.name + '_indexer_enabled')
                                if indxr_enabled == 'true':
                                    processed_items.append(prcsd)
                                    if indxrtyp.name == url_key:
                                        pool.putRequest( WorkRequest(indxrtyp.GetContent, args=(indexer, url_value, title, name, year, season, episode, type, list)) )
                                        break
                    break
                    
            for srcr in Source.implementors(): 
                if srcr.source_type == indexer:
                    for url_key, url_value in urls.items():
                        for srcrtyp in srcr.implementors():
                            prcsd = '%s_%s' % (url_key, srcrtyp.name)
                            if prcsd not in processed_items:                        
                                srcr_enabled = stg.Settings().get_setting(srcr.source_type + '_' + srcrtyp.name + '_source_enabled')
                                if srcr_enabled == 'true':
                                    processed_items.append(prcsd)
                                    if srcrtyp.name == url_key:
                                        pool.putRequest( WorkRequest(srcrtyp.GetContent, args=(indexer, url_value, title, name, year, season, episode, type, list)) )
                                        break
                    break
            
            import threading
            threading.Thread(target=FinalizeSearch, args=(pool, list, unique_list, message_queue)).start()
        
            return (unique_list, message_queue)

    unique_list = []
    meta = []
    
    the_indexer = None
    
    for indxr in Indexer.implementors(): 
        if indxr.indexer_type == indexer: 
            for indxrtyp in indxr.implementors():
                if indxrtyp.name == indexer_to_use:
                    the_indexer = indxrtyp
                    break
            break
            
    if the_indexer:
        the_indexer.GetContent(indexer, url, title, name, year, season, episode, type, unique_list)
    
    return (unique_list, meta)    
    
def GetSportsContent(indexer, indexer_id ):

    (pool, list, unique_list, lock, message_queue) = Initialize()
    
    from threadpool import WorkRequest
        
    from plugnplay.interfaces import SportsSource
    for sprtsrcs in SportsSource.implementors():
        if indexer_id in sprtsrcs.source_sports_list:
            pool.putRequest( WorkRequest(sprtsrcs.GetSportsContent, args=(indexer, indexer_id, list, lock, message_queue)))
            
    import threading
    threading.Thread(target=FinalizeSearch, args=(pool, list, unique_list, message_queue)).start()
            
    return (unique_list, message_queue)

def GetLiveTVRegions( ):
    
    loadiStreamPlugins( type=common.settings_Live_TV, load_indexer=True, load_settings=True )

    unique_list = []
    
    stg = iStream_settings.get(common.indxr_Live_TV, None)
    if not stg:
        return unique_list
    
    regions_list = ''
    
    from plugnplay.interfaces import LiveTVIndexer
    for livetvindxr in LiveTVIndexer.implementors():
        regions = livetvindxr.regions
        for region in regions:
            region_name = region['name']
            region_id = common.CreateIdFromString(region_name)
            enabled = True if stg.Settings().get_setting( 'live_tv_' + region_id + '_indexer_enabled') == 'true' else False
            if not enabled: continue            
            if region_id not in regions_list:
                regions_list += region_id + '|'
                region.update({'indexer_id':region_id})
                region.update({'title':region_name})
                if not region.get('img', None):
                    region.update({'img':common.get_themed_icon(region_id + '.png')})
                if not region.get('fanart', None):
                    region.update({'fanart':common.get_themed_icon(region_id + '.jpg')})
                unique_list.append(region)
    
    return unique_list
    
def GetLiveTVForRegion( rgn_id ): 

    loadiStreamPlugins( type=common.settings_Live_TV, load_indexer=True, load_settings=True )
    
    unique_list = []
    
    channels_list = ''
    
    stg = iStream_settings.get(common.indxr_Live_TV, None)
    if not stg:
        return unique_list
    
    regions_list = ''
    
    from plugnplay.interfaces import LiveTVIndexer
    for livetvindxr in LiveTVIndexer.implementors():
        if livetvindxr.name not in channels_list: channels_list += livetvindxr.name + '|'
        regions = livetvindxr.regions
        for region in regions:
            region_name = region['name']
            region_id = common.CreateIdFromString(region_name)
            if region_id == rgn_id:
                enabled = True if stg.Settings().get_setting( 'live_tv_' + livetvindxr.name + '_indexer_enabled') == 'true' else False
                if not enabled: continue
                unique_list.append( 
                    {
                        'indexer':common.indxr_Live_TV, 
                        'indexer_id':livetvindxr.name, 
                        'section':'main2', 
                        'title':livetvindxr.display_name, 
                        'mode':common.mode_Live_TV,
                        'region':rgn_id,
                        'img':livetvindxr.img,
                        'fanart':livetvindxr.fanart,
                        'other_names':livetvindxr.other_names
                    } )
                
    
    return unique_list
    
def GetLiveTVLanguages( ):

    loadiStreamPlugins( type=common.settings_Live_TV, load_indexer=True, load_settings=True )

    unique_list = []
    
    stg = iStream_settings.get(common.indxr_Live_TV, None)
    if not stg:
        return unique_list
    
    languages_list = ''
    
    from plugnplay.interfaces import LiveTVIndexer
    for livetvindxr in LiveTVIndexer.implementors():
        languages = livetvindxr.languages
        for language in languages:
            language_name = language['name']
            language_id = common.CreateIdFromString(language_name)
            enabled = True if stg.Settings().get_setting( 'live_tv_' + language_id + '_indexer_enabled') == 'true' else False
            if not enabled: continue            
            if language_id not in languages_list:
                languages_list += language_id + '|'
                language.update({'indexer_id':language_id})
                language.update({'title':language_name})
                if not language.get('img', None):
                    language.update({'img':common.get_themed_icon(language_id + '.png')})
                if not language.get('fanart', None):
                    language.update({'fanart':common.get_themed_icon(language_id + '.jpg')})
                unique_list.append(language)
    
    return unique_list    
    
def GetLiveTVForLanguage( lang_id ):   

    loadiStreamPlugins( type=common.settings_Live_TV, load_indexer=True, load_settings=True )
    
    unique_list = []
    
    channels_list = ''
    
    stg = iStream_settings.get(common.indxr_Live_TV, None)
    if not stg:
        return unique_list
        
    from plugnplay.interfaces import LiveTVIndexer
    for livetvindxr in LiveTVIndexer.implementors():
        if livetvindxr.name not in channels_list: channels_list += livetvindxr.name + '|'
        languages = livetvindxr.languages
        for language in languages:
            language_name = language['name']
            language_id = common.CreateIdFromString(language_name)
            if language_id == lang_id:
                enabled = True if stg.Settings().get_setting( 'live_tv_' + livetvindxr.name + '_indexer_enabled') == 'true' else False
                if not enabled: continue
                unique_list.append( 
                    {
                        'indexer':common.indxr_Live_TV, 
                        'indexer_id':livetvindxr.name, 
                        'section':'main2', 
                        'title':livetvindxr.display_name, 
                        'mode':common.mode_Live_TV,
                        'language':lang_id,
                        'img':livetvindxr.img,
                        'fanart':livetvindxr.fanart,
                        'other_names':livetvindxr.other_names
                    } )
                
    
    return unique_list
    
def GetLiveTVGenres( ):
    
    loadiStreamPlugins( type=common.settings_Live_TV, load_indexer=True, load_settings=True )
    
    unique_list = []
    
    stg = iStream_settings.get(common.indxr_Live_TV, None)
    if not stg:
        return unique_list
    
    genres_list = ''
    
    from plugnplay.interfaces import LiveTVIndexer
    for livetvindxr in LiveTVIndexer.implementors():
        genres = livetvindxr.genres
        for genre in genres:
            genre_name = genre['name']
            genre_id = common.CreateIdFromString(genre_name)
            enabled = True if stg.Settings().get_setting( 'live_tv_' + genre_id + '_indexer_enabled') == 'true' else False
            if not enabled: continue            
            if genre_id not in genres_list:
                genres_list += genre_id + '|'
                genre.update({'indexer_id':genre_id})
                genre.update({'title':genre_name})
                if not genre.get('img', None):
                    genre.update({'img':common.get_themed_icon(genre_id + '.png')})
                if not genre.get('fanart', None):
                    genre.update({'fanart':common.get_themed_icon(genre_id + '.jpg')})
                unique_list.append(genre)
    
    return unique_list
    
def GetLiveTVForGenre( gnr_id ):   
    
    loadiStreamPlugins( type=common.settings_Live_TV, load_indexer=True, load_settings=True )
 
    unique_list = []
    
    channels_list = ''
    
    stg = iStream_settings.get(common.indxr_Live_TV, None)
    if not stg:
        return unique_list
    
    genres_list = ''
        
    from plugnplay.interfaces import LiveTVIndexer
    for livetvindxr in LiveTVIndexer.implementors():
        if livetvindxr.name not in channels_list: channels_list += livetvindxr.name + '|'
        genres = livetvindxr.genres
        for genre in genres:
            genre_name = genre['name']
            genre_id = common.CreateIdFromString(genre_name)
            if genre_id == gnr_id:
                enabled = True if stg.Settings().get_setting( 'live_tv_' + livetvindxr.name + '_indexer_enabled') == 'true' else False
                if not enabled: continue
                unique_list.append( 
                    {
                        'indexer':common.indxr_Live_TV, 
                        'indexer_id':livetvindxr.name, 
                        'section':'main2', 
                        'title':livetvindxr.display_name, 
                        'mode':common.mode_Live_TV,
                        'img':livetvindxr.img,
                        'fanart':livetvindxr.fanart,
                        'other_names':livetvindxr.other_names
                    } )
                
    
    return unique_list    
    
def GetLiveTVLinks(indexer, indexer_id, other_names, region, language ):
    
    loadiStreamPlugins(type=common.settings_Live_TV, load_indexer=True, load_source=True, load_settings=True, load_webproxyproviders=True, load_fileformats=True)
    
    stg = iStream_settings.get(indexer, None)

    (pool, list, unique_list, lock, message_queue) = Initialize()
    
    from threadpool import WorkRequest
    
    from plugnplay.interfaces import LiveTVIndexer
    from plugnplay.interfaces import LiveTVSource
    
    import re
    indexer_id = re.sub('\_\_.*', '', indexer_id)
    
    
    for livetvsrcs in LiveTVSource.implementors():
        srcr_enabled = True
        if not isinstance(livetvsrcs, LiveTVIndexer):
            srcr_enabled = stg.Settings().get_setting(livetvsrcs.source_type + '_' + livetvsrcs.name + '_source_enabled') == "true"
        if srcr_enabled:
            pool.putRequest( WorkRequest(livetvsrcs.GetFileHosts, args=(indexer_id, other_names, region, language, list, lock, message_queue)))
            
    import threading
    threading.Thread(target=FinalizeSearch, args=(pool, list, unique_list, message_queue)).start()
            
    return (unique_list, message_queue)   

def GetTools():    
    from plugnplay.interfaces import Tools
    common.loadplugins([Tools])
    
    unique_list = []
    
    for tool in Tools.implementors(): 
        tool_img = common.get_themed_icon('tools.png') if common.get_themed_icon('tools.png') else tool.img
        tool_fanart = common.get_themed_fanart('tools.jpg') if common.get_themed_fanart('tools.jpg') else tool.fanart 
        unique_list.append({'title':tool.display_name, 'mode':common.mode_Tools, 'indexer':'tools', 'section':'tools', 'name':tool.name,
            'img':tool_img, 'fanart':tool_fanart, 'notify_msg_header':tool.notify_msg_header, 'notify_msg_success':tool.notify_msg_success,
            'notify_msg_failure':tool.notify_msg_failure } )
    
    return unique_list
    
def GetContextMenuTools():    
    from plugnplay.interfaces import Tools
    common.loadplugins([Tools])
    
    unique_list = []
    
    from plugnplay.interfaces import Tools
    
    for tool in Tools.implementors(): 
        if tool.show_in_context_menu == True:
            unique_list.append({'title':tool.display_name, 'mode':common.mode_Tools, 'indexer':'tools', 'section':'tools', 'name':tool.name,
                'img':tool.img, 'fanart':tool.fanart, 'notify_msg_header':tool.notify_msg_header, 'notify_msg_success':tool.notify_msg_success,
                'notify_msg_failure':tool.notify_msg_failure})
    
    return unique_list
    
def ExecuteTool(name):    
    loadiStreamPlugins()
    
    from plugnplay.interfaces import Tools
    common.loadplugins([Tools])
    
    tool_to_execute = None
    
    for tool in Tools.implementors(): 
        if name == tool.name:
            tool_to_execute = tool
            break
        
    if tool_to_execute:
        return tool_to_execute.Execute()
        
    return False


def GetSportsLinks(indexer, indexer_id ):
    urls = common.ConvertStringToDict(urls)    

def _handle_thread_exception(request, exc_info):
    import traceback
    traceback.print_exception(*exc_info)
def callbackExceptionGetFileHosts(request, result):
    _handle_thread_exception(request, result)
    callbackGetFileHosts(request, result)
def callbackExceptionGetFileHostsForContent(request, result):
    _handle_thread_exception(request, result)
    callbackGetFileHostsForContent(request, result)    
def callbackGetFileHosts(request, result):
    request.args[2].acquire()
    print request.kwds
    global srcr_loop
    global srcr_count
    global srcr_url_to_name_map
    srcr_loop = srcr_loop + 1
    request.args[3].put({'index':1, 'message': str(srcr_loop) + ' of ' + str(srcr_count) + ' source(s) searched '})
    request.args[3].put({'index':2, 'message':'[COLOR yellow]Source: [/COLOR][B][COLOR ff00b7ff]' + srcr_url_to_name_map[request.requestID].upper() + '[/COLOR][/B]'})
    request.args[3].put({'index':3, 'message':'Number of links retreived: ' + str(len(request.args[1]))})
    request.args[2].release()        
def callbackGetFileHostsForContent(request, result):
    request.args[7].acquire()
    global srcr_loop
    global srcr_count
    srcr_loop = srcr_loop + 1
    request.args[8].put({'index':1, 'message': str(srcr_loop) + ' of ' + str(srcr_count) + ' source(s) searched' })
    request.args[8].put({'index':2, 'message':'[COLOR yellow]Source: [/COLOR][B][COLOR ff00b7ff]' + srcr_url_to_name_map[request.requestID].upper() + '[/COLOR][/B]'})
    request.args[8].put({'index':3, 'message':'Number of links retreived: ' + str(len(request.args[6]))})
    request.args[7].release()
def dismissThreadPool(pool, thread_count):
    import xbmcgui
    mainWindow = xbmcgui.Window(10000)
    
    import time
    
    while True:
        time.sleep(0.5)
        if mainWindow.getProperty('ISTREAM-PROGRES-DIALOG-CANCELLED') == 'TRUE':
            pool.dismissWorkers(thread_count, True)
            break
        elif not pool.workRequests or not pool.workers:
            break
    
def GetFileHosts(indexer, indexer_to_use, url, title, name, year, season, episode, type, urls='', autoplay=False ):    
    
    global srcr_count
    global srcr_loop
    global srcr_url_to_name_map
    
    if urls != '':
        urls = common.ConvertStringToDict(urls)    
    
    (pool, list, unique_list, lock, message_queue) = Initialize()
    
    import threading
    threading.Thread(target=dismissThreadPool, args=(pool, 2)).start()
    
    from threadpool import WorkRequest
    
    stg = iStream_settings.get(indexer, None)
    if stg:
        for src in Source.implementors(): 
            if src.source_type == indexer: 
                srcr_count = len([s for s in src.implementors() if ( (autoplay == False) or (autoplay == True and s.auto_play_supported == True) ) and ( (urls!='' and urls.get(s.name, '')!='') or stg.Settings().get_setting(src.source_type + '_' + s.name + '_source_enabled') == 'true' )] )
                srcr_loop = 0
                message_queue.put({'message': str(srcr_loop) + ' of ' + str(srcr_count) + ' source(s) searched' })
                message_queue.put({'message':'[COLOR yellow]Source: [/COLOR][B]-[/B]'})
                message_queue.put({'message': 'Number of links retrieved: 0' })
                for srcr in src.implementors():
                    fetch = True
                    if autoplay == True:
                        fetch = srcr.auto_play_supported
                        
                    if urls != '':
                        url = urls.get(srcr.name, '')
                        if url != '' and fetch == True:
                            srcr_url_to_name_map.update({hash(srcr.name):srcr.name})
                            pool.putRequest( WorkRequest(srcr.GetFileHosts, args=(url, list, lock, message_queue), requestID=srcr.name, callback=callbackGetFileHosts, exc_callback=callbackExceptionGetFileHosts))
                            continue
                    srcr_enabled = stg.Settings().get_setting(src.source_type + '_' + srcr.name + '_source_enabled')
                    if srcr_enabled == 'true' and fetch == True:
                        srcr_url_to_name_map.update({hash(srcr.name):srcr.name})
                        if srcr.name == indexer_to_use:
                            pool.putRequest( WorkRequest(srcr.GetFileHosts, args=(url, list, lock, message_queue), requestID=srcr.name, callback=callbackGetFileHosts, exc_callback=callbackExceptionGetFileHosts))
                        else:
                            pool.putRequest( WorkRequest(srcr.GetFileHostsForContent, args=(title, name, year, season, episode, type, list, lock, message_queue), requestID=srcr.name, callback=callbackGetFileHostsForContent, exc_callback=callbackExceptionGetFileHostsForContent))
                break
    
    threading.Thread(target=Finalize, args=(pool, indexer, list, unique_list, message_queue)).start()
    
    return (unique_list, message_queue)
    
def GetSortByOptions(indexer, indexer_to_use):
    
    the_indexer = None
    
    sort_by_options = None
    
    for indxr in Indexer.implementors(): 
        if indxr.indexer_type == indexer: 
            for indxrtyp in indxr.implementors():
                if indxrtyp.name == indexer_to_use:
                    the_indexer = indxrtyp
                    break
            break
            
    if the_indexer:
        sort_by_options = the_indexer.GetSortByOptions()
        
    return sort_by_options
        
def GetSortOrderOptions(indexer, indexer_to_use):
    
    the_indexer = None
    
    sort_order_options = None
    
    for indxr in Indexer.implementors(): 
        if indxr.indexer_type == indexer: 
            for indxrtyp in indxr.implementors():
                if indxrtyp.name == indexer_to_use:
                    the_indexer = indxrtyp
                    break
            break
            
    if the_indexer:
        sort_order_options = the_indexer.GetSortOrderOptions()       

    return sort_order_options
    
def ResolveUrl(url):
    src = Source()
    return src.Resolve(url)
    
def ResolveFileHostUrl(source, source_to_use, url):
    
    resolved_url = ''
    for src in Source.implementors():
        if src.source_type == source:
            for srcr in src.implementors():
                if srcr.name == source_to_use:
                    resolved_url = srcr.Resolve(url)
                    break
            break
    
    return resolved_url

'''
def GetFileStores():
    unique_list = []
    
    from entertainment.plugnplay.interfaces import FileStore
    common.loadplugins([FileStore])
    for fs in FileStore.implementors():
        unique_list.append( {'title':fs.display_name, 'mode':common.mode_File_Stores, 'indexer':'file_stores', 'section':'file_stores', 'indexer_id':fs.name} )
    
    return unique_list

def GetFileFormats():
    unique_list = []
    
    from entertainment.plugnplay.interfaces import FileStore
    common.loadplugins([FileStore])
    for fs in FileStore.implementors():
        unique_list.append( {'title':fs.display_name, 'mode':common.mode_File_Stores, 'indexer':'file_stores', 'section':'file_stores', 'indexer_id':fs.name} )
    
    return unique_list
'''
    
def GetFileFormatExtensionsMask():
    
    extensions_mask = ''
    
    from plugnplay.interfaces import FileFormat
    for fs in FileFormat.implementors():
        extensions_mask += '|' + fs.extensions
        
    extensions_mask = extensions_mask[1:]
    
    return extensions_mask

def GetFileFormats():
    
    unique_list = []
    
    from plugnplay.interfaces import FileFormat
    for fs in FileFormat.implementors():
        unique_list.append( { 'name' : fs.name, 'display_name' : fs.display_name })
    
    return unique_list
    
def GetFileFormatObj(format):
    
    ff = None
    
    from entertainment.plugnplay.interfaces import FileFormat
    for fs in FileFormat.implementors():
        if fs.name == format:
            ff = fs
            break

    return ff
    
def ReadFile(format, path):
    
    title = ''
    unique_list = []
    
    from plugnplay.interfaces import FileFormat
    for fs in FileFormat.implementors():
        if fs.name == format:
            (title, unique_list) = fs.ReadFile(path)
            break
    
    return (title, unique_list)  

def GetFileTitle(format, path):    
    title = 'NA'
    
    from plugnplay.interfaces import FileFormat
    for fs in FileFormat.implementors():
        if fs.name == format:
            title = fs.ReadFile(path, True)
            break
            
    return title

def ReadItem(format, item):
    title = ''
    unique_list = []
    
    from plugnplay.interfaces import FileFormat
    for fs in FileFormat.implementors():
        if fs.name == format:
            (title, unique_list) = fs.ReadItem(item)
            break
    return (title, unique_list)  
    
def DetectFileFormat(path):
    from plugnplay.interfaces import FileFormat
    ff = FileFormat()
    
    raw_data = ff.ReadFile(path, send_raw_data=True)

    if not raw_data:
        return (None, 'ISTREAM_MSG_NOT_AVAILABLE')
        
    
    detected_ff = None
    
    for fs in FileFormat.implementors():
        can_parse_response = fs.CanParse(raw_data)
        if can_parse_response in ( ff.ff_can_parse_yes, ff.ff_can_parse_maybe):
            detected_ff = fs
            if can_parse_response == ff.ff_can_parse_yes: break

    return (detected_ff, raw_data)

    
#make sure settings.xml is up to date
#common._update_settings_xml()

#make sure settings for other items are up to date
#GetSettings()
