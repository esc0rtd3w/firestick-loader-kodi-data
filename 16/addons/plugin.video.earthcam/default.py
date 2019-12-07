# -*- coding: utf-8 -*-
#------------------------------------------------------------
# RadioReference.com
#------------------------------------------------------------
# Based on code from pelisalacarta
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import urllib, urllib2
import os,sys

from core import logger
from core import config

PLUGIN_NAME = "earthcam"

def run():
    logger.info("[launcher.py] run")
    
    # Extract parameters from sys.argv
    params, channel_name, title, fulltitle, url, thumbnail, plot, action, server, extra, subtitle, category, show, password = extract_parameters()
    logger.info("[launcher.py] channel_name=%s, title=%s, fulltitle=%s, url=%s, thumbnail=%s, plot=%s, action=%s, server=%s, extra=%s, subtitle=%s, category=%s, show=%s, password=%s" % (channel_name, title, fulltitle, url, thumbnail, plot, action, server, extra, subtitle, category, show, password))

    from core.item import Item
    item = Item(channel=channel_name, title=title , fulltitle=fulltitle, url=url, thumbnail=thumbnail , plot=plot , server=server, category=category, extra=extra, subtitle=subtitle, show=show, password=password)

    try:
        # Actualizar version
        if ( action=="configuracion" ):
            logger.info("[launcher.py] configuracion")
            config.open_settings( )

        elif ( action=="vacio" ):
            logger.info("[launcher.py] vacio")

        elif action=="play":
            import channel
            generico = True
            itemlist = channel.play(item)
            if len(itemlist)==0:
                return
            elif len(itemlist)==1:

                item = itemlist[0]

                if item.url.lower().endswith(".jpg") or item.url.lower().endswith(".png"):
                    import os
                    slideshowpath = os.path.join(config.get_data_path(),"slideshow")
                    if not os.path.exists(slideshowpath):
                        try:
                            os.mkdir(slideshowpath)
                        except:
                            pass

                    urllib.urlretrieve(item.url, os.path.join(slideshowpath,"temp.jpg"))
                    import xbmc
                    xbmc.executebuiltin( "SlideShow("+slideshowpath+")" )
                else:
                    import xbmcplugin,xbmcgui,xbmc,xbmcaddon,sys
                    xlistitem = xbmcgui.ListItem( item.title, iconImage="DefaultVideo.png", thumbnailImage=item.thumbnail, path=item.url)
                    xlistitem.setInfo( "video", { "Title": item.title, "Plot" : item.plot , "Genre" : item.category } )

                    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=item.url))

                    # Añadimos el listitem a una lista de reproducción (playlist)
                    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
                    playlist.clear()
                    playlist.add( item.url, xlistitem )

                    # Reproduce
                    xbmcPlayer = xbmc.Player()
                    xbmcPlayer.play(playlist)

                return

        # if other action
        # OR
        # len(itemlist)>1 for action=="play":

        import channel
        generico = True

        if action=="search":
            logger.info("[launcher.py] search")
            import xbmc
            keyboard = xbmc.Keyboard("")
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                tecleado = keyboard.getText()
                tecleado = tecleado.replace(" ", "+")
                itemlist = channel.search(item,tecleado)
            else:
                itemlist = []

        else:
            exec "itemlist = channel."+action+"(item)"

        # Activa el modo biblioteca
        #import xbmcplugin
        #import sys
        #handle = sys.argv[1]
        #xbmcplugin.setContent(int( handle ),"movies")

        # AÃ±ade los items a la lista de XBMC

        import xbmctools
        xbmctools.renderItems(itemlist, params, url, category)

    except urllib2.URLError,e:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        import xbmcgui
        ventana_error = xbmcgui.Dialog()
        # Agarra los errores surgidos localmente enviados por las librerias internas
        if hasattr(e, 'reason'):
            logger.info("Razon del error, codigo: %d , Razon: %s" %(e.code,e.reason))
            texto = "No se puede conectar con el sitio web"
            ok = ventana_error.ok ("plugin", texto)
        # Agarra los errores con codigo de respuesta del servidor externo solicitado     
        elif hasattr(e,'code'):
            logger.info("codigo de error HTTP : %d" %e.code)
            texto = ("El sitio web no funciona correctamente (error http %d)" % e.code)
            ok = ventana_error.ok ("plugin", texto)    

# Parse XBMC params - based on script.module.parsedom addon    
def get_params():
    logger.info("get_params")
    
    param_string = sys.argv[2]
    
    logger.info("get_params "+str(param_string))
    
    commands = {}

    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
    
        for command in split_commands:
            logger.info("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = urllib.unquote_plus(split_command[1])
                    commands[key] = value
                else:
                    commands[command] = ""
    
    logger.info("get_params "+repr(commands))
    return commands

# Extract parameters from sys.argv
def extract_parameters():
    logger.info("[launcher.py] extract_parameters")
    #Imprime en el log los parametros de entrada
    logger.info("[launcher.py] sys.argv=%s" % str(sys.argv))
    
    # Crea el diccionario de parametros
    params = get_params()
    logger.info("[launcher.py] params=%s" % str(params))

    if (params.has_key("channel")):
        channel = urllib.unquote_plus( params.get("channel") )
    else:
        channel=''
    
    # Extrae la url de la pana
    if (params.has_key("url")):
        url = urllib.unquote_plus( params.get("url") )
    else:
        url=''

    # Extrae la accion
    if (params.has_key("action")):
        action = params.get("action")
    else:
        action = "mainlist"

    # Extrae el server
    if (params.has_key("server")):
        server = params.get("server")
    else:
        server = ""

    # Extrae la categoria
    if (params.has_key("category")):
        category = urllib.unquote_plus( params.get("category") )
    else:
        if params.has_key("channel"):
            category = params.get("channel")
        else:
            category = ""
            
    # Extrae el título de la serie
    if (params.has_key("show")):
        show = params.get("show")
    else:
        show = ""

    # Extrae el título del video
    if params.has_key("title"):
        title = urllib.unquote_plus( params.get("title") )
    else:
        title = ""

    # Extrae el título del video
    if params.has_key("fulltitle"):
        fulltitle = urllib.unquote_plus( params.get("fulltitle") )
    else:
        fulltitle = ""

    if params.has_key("thumbnail"):
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    else:
        thumbnail = ""

    if params.has_key("plot"):
        plot = urllib.unquote_plus( params.get("plot") )
    else:
        plot = ""

    if params.has_key("extradata"):
        extra = urllib.unquote_plus( params.get("extradata") )
    else:
        extra = ""

    if params.has_key("subtitle"):
        subtitle = urllib.unquote_plus( params.get("subtitle") )
    else:
        subtitle = ""

    if params.has_key("password"):
        password = urllib.unquote_plus( params.get("password") )
    else:
        password = ""

    if params.has_key("show"):
        show = urllib.unquote_plus( params.get("show") )
    else:
        if params.has_key("Serie"):
            show = urllib.unquote_plus( params.get("Serie") )
        else:
            show = ""

    return params, channel, title, fulltitle, url, thumbnail, plot, action, server, extra, subtitle, category, show, password

run()
