

###########################################################
#                                                         #
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html) #
#                                                         #
# info: grab images from the internet ,  this creates a   #
# folder called backgrounds in home folder and downloads  #
# images to that folder for use as backgrounds            #
#                                                         #
##################Author:Les][smor#########################


import os           
import urlparse     
import xbmc         
import xbmcaddon   
import xbmcgui      
import xbmcplugin   
import koding
from koding import Download 
from koding import route, Run 

dialog = xbmcgui.Dialog()      



@route(mode="dialog_specific")
def  Dialog_specific():
    
    main_text = 'Click below to download an image to be used as a background.\n\nYou will first need to enter a name for your image,\nThen you must enter the Url to that image .\nPlease keep image names different else they will be overwritten!\nYou may need to add home folder as a source to file manager before u can use the images.'
    my_buttons = ['Grab it']
    my_choice = koding.Custom_Dialog(main_content=main_text,pos='center',size='650x400',buttons=my_buttons,transparency=95,highlight_color='white',header='INSTALLA')      
    my_path = xbmc.translatePath('special://home/backgrounds/')
    if not os.path.exists( my_path ):os.makedirs(my_path)
    if my_choice ==0:
                my_path = xbmc.translatePath('special://home/backgrounds/')
                image_name = koding.Keyboard(heading='Type in a name for your image',default='test text')
                src = koding.Keyboard(heading='Please enter the url of your image',default='http://')
                dst = xbmc.translatePath('special://home/backgrounds/'  + image_name + '.jpg')
                full_path_image = my_path + image_name + '.jpg'
                dp = xbmcgui.DialogProgress()
                dp.create('Downloading File','Please Wait')
                koding.Download(src,dst,dp)
                dialog.ok('[COLOR gold]DOWNLOAD COMPLETE[/COLOR]','Your download is complete, You can find images in home/backgrounds -')

    