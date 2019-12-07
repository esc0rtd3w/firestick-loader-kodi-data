import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os
import re

ADDON = xbmcaddon.Addon(id='plugin.video.EasyNews')


def addon():
    return ADDON
    
def mlang_ex():
    return ADDON.getSetting('mlangex').replace(' ','+')
      
    
def m_filesize():
    quality = ADDON.getSetting('mfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '8'
    elif quality == '2':
        return '9'
    elif quality == '3':
        return '10'
    elif quality == '4':
        return '11'
    elif quality == '5':
        return '12'
    elif quality == '6':
        return '13'
    elif quality == '7':
        return '14'
    elif quality == '8':
        return '15'
    elif quality == '9':
        return '16'
    elif quality == '10':
        return '17'
    elif quality == '11':
        return '18'
    elif quality == '12':
        return '19'
    elif quality == '13':
        return '20'
    elif quality == '14':
        return '21'
    elif quality == '15':
        return '22'
    elif quality == '16':
        return '23'
    elif quality == '17':
        return '24'
    elif quality == '18':
        return '25'
    elif quality == '19':
        return '26'
    elif quality == '20':
        return '27'
    elif quality == '21':
        return '28'
    elif quality == '22':
        return '29'
    elif quality == '23':
        return '30'
    elif quality == '24':
        return '31'
    elif quality == '25':
        return '32'
        
        
def m_maxfilesize():
    quality = ADDON.getSetting('mmaxfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '8'
    elif quality == '2':
        return '9'
    elif quality == '3':
        return '10'
    elif quality == '4':
        return '11'
    elif quality == '5':
        return '12'
    elif quality == '6':
        return '13'
    elif quality == '7':
        return '14'
    elif quality == '8':
        return '15'
    elif quality == '9':
        return '16'
    elif quality == '10':
        return '17'
    elif quality == '11':
        return '18'
    elif quality == '12':
        return '19'
    elif quality == '13':
        return '20'
    elif quality == '14':
        return '21'
    elif quality == '15':
        return '22'
    elif quality == '16':
        return '23'
    elif quality == '17':
        return '24'
    elif quality == '18':
        return '25'
    elif quality == '19':
        return '26'
    elif quality == '20':
        return '27'
    elif quality == '21':
        return '28'
    elif quality == '22':
        return '29'
    elif quality == '23':
        return '30'
    elif quality == '24':
        return '31'
    elif quality == '25':
        return '32'
        
def tv_filesize():
    quality = ADDON.getSetting('tvfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '8'
    elif quality == '2':
        return '9'
    elif quality == '3':
        return '10'
    elif quality == '4':
        return '11'
    elif quality == '5':
        return '12'
    elif quality == '6':
        return '13'
    elif quality == '7':
        return '14'
    elif quality == '8':
        return '15'
    elif quality == '9':
        return '16'
    elif quality == '10':
        return '17'
    elif quality == '11':
        return '18'
    elif quality == '12':
        return '19'
    elif quality == '13':
        return '20'
    elif quality == '14':
        return '21'
    elif quality == '15':
        return '22'
    elif quality == '16':
        return '23'
    elif quality == '17':
        return '24'
    elif quality == '18':
        return '25'
    elif quality == '19':
        return '26'
    elif quality == '20':
        return '27'
    elif quality == '21':
        return '28'
    elif quality == '22':
        return '29'
    elif quality == '23':
        return '30'
    elif quality == '24':
        return '31'
    elif quality == '25':
        return '32'
        
        
def tv_maxfilesize():
    quality = ADDON.getSetting('tvmaxfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '8'
    elif quality == '2':
        return '9'
    elif quality == '3':
        return '10'
    elif quality == '4':
        return '11'
    elif quality == '5':
        return '12'
    elif quality == '6':
        return '13'
    elif quality == '7':
        return '14'
    elif quality == '8':
        return '15'
    elif quality == '9':
        return '16'
    elif quality == '10':
        return '17'
    elif quality == '11':
        return '18'
    elif quality == '12':
        return '19'
    elif quality == '13':
        return '20'
    elif quality == '14':
        return '21'
    elif quality == '15':
        return '22'
    elif quality == '16':
        return '23'
    elif quality == '17':
        return '24'
    elif quality == '18':
        return '25'
    elif quality == '19':
        return '26'
    elif quality == '20':
        return '27'
    elif quality == '21':
        return '28'
    elif quality == '22':
        return '29'
    elif quality == '23':
        return '30'
    elif quality == '24':
        return '31'
    elif quality == '25':
        return '32'
        

def m_fileext():
    quality = ADDON.getSetting('mfileext')
    if quality == '0':
        return ''
    elif quality == '1':   
        return 'AVI'
    elif quality == '2':
        return 'MKV'
    elif quality == '3':
        return 'MP4'
    elif quality == '4':
        return 'ISO'
    elif quality == '5':
        return 'DIVX'
    elif quality == '6':
        return 'MPG'
    elif quality == '7':
        return 'FLV'
    elif quality == '8':
        return 'WMV'
    elif quality == '9':
        return 'MOV'
    elif quality == '10':
        return 'ASF'
    elif quality == '11':
        return 'RM'
        
def tv_fileext():
    quality = ADDON.getSetting('tvfileext')
    if quality == '0':
        return ''
    elif quality == '1':   
        return 'AVI'
    elif quality == '2':
        return 'MKV'
    elif quality == '3':
        return 'MP4'
    elif quality == '4':
        return 'ISO'
    elif quality == '5':
        return 'DIVX'
    elif quality == '6':
        return 'MPG'
    elif quality == '7':
        return 'FLV'
    elif quality == '8':
        return 'WMV'
    elif quality == '9':
        return 'MOV'
    elif quality == '10':
        return 'ASF'
    elif quality == '11':
        return 'RM'


def easy_url():
    return 'http://members-beta.easynews.com/global5/search.html?&gps='
    
def end_url():
    return '&st=adv&safe=1&boost=1&sb=1'
    
def m_subject():
    return  ADDON.getSetting('msubject')
    
    
def m_poster():
    return ADDON.getSetting('mposter')
    
def m_newsgroup():
    return ADDON.getSetting('mnewsgroup').replace(',','%2c')
    
def m_filename():
    return ADDON.getSetting('mfilename')
    
def m_vcodec():
    return ADDON.getSetting('mvcodec')
    
def m_acodec():
    return ADDON.getSetting('macodec')
    
def m_filename():
    return ADDON.getSetting('mfilename')
    
def m_results():
    return ADDON.getSetting('mresults')
    
   
    
def tv_subject():
    return ADDON.getSetting('tvsubject')
    
def tv_poster():
    return ADDON.getSetting('tvposter')
    
def tv_newsgroup():
    return ADDON.getSetting('tvnewsgroup')
    
def tv_vcodec():
    return ADDON.getSetting('tvvcodec')
    
def tv_acodec():
    return ADDON.getSetting('tvacodec')
    
def tv_filename():
    return ADDON.getSetting('tvfilename')
    
def tv_results():
    return ADDON.getSetting('tvresults')
    
def m_spam():
    if ADDON.getSetting('mspam') == "true":
        return '&spamf=1'
    if ADDON.getSetting('mspam') == "false":
        return ''
        
def tv_spam():
    if ADDON.getSetting('tvspam') == "true":
        return '&spamf=1'
    if ADDON.getSetting('tvspam') == "false":
        return ''
             
def m_rem():
    if ADDON.getSetting('mrem') == "true":
        return '&u=1'
    if ADDON.getSetting('mrem') == "false":
        return ''
        
def tv_rem():
    if ADDON.getSetting('tvrem') == "true":
        return '&u=1'
    if ADDON.getSetting('tvrem') == "false":
        return ''
                
def m_grex():
    if ADDON.getSetting('mgrex') == "true":
        return '&gx=1'
    if ADDON.getSetting('mgrex') == "false":
        return ''
        
def tv_grex():
    if ADDON.getSetting('tvgrex') == "true":
        return '&gx=1'
    if ADDON.getSetting('tvgrex') == "false":
        return ''
        
def tvlang_ex():
    return ADDON.getSetting('tvlangex').replace(' ','+')
    
def tv_reso():
    quality = ADDON.getSetting('tvreso')
    if quality == '0':
        return '&px1=&px1t=&px=&px2t='
    if quality == '1':
        return '&px1=&px1t=&px2=&px2t=9'
    elif quality == '2':
        return '&px1=&px1t=5&px2=&px2t=9'
    elif quality == '3':
        return '&px1=&px1t=8&px2=&px2t=10'
        
def m_reso():
    quality = ADDON.getSetting('mreso')
    if quality == '0':
        return '&px1=&px1t=&px=&px2t='
    if quality == '1':
        return '&px1=&px1t=&px2=&px2t=9'
    elif quality == '2':
        return '&px1=&px1t=5&px2=&px2t=9'
    elif quality == '3':
        return '&px1=&px1t=8&px2=&px2t=10'
    
def gl_filesize():
    quality = ADDON.getSetting('glfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '8'
    elif quality == '2':
        return '9'
    elif quality == '3':
        return '10'
    elif quality == '4':
        return '11'
    elif quality == '5':
        return '12'
    elif quality == '6':
        return '13'
    elif quality == '7':
        return '14'
    elif quality == '8':
        return '15'
    elif quality == '9':
        return '16'
    elif quality == '10':
        return '17'
    elif quality == '11':
        return '18'
    elif quality == '12':
        return '19'
    elif quality == '13':
        return '20'
    elif quality == '14':
        return '21'
    elif quality == '15':
        return '22'
    elif quality == '16':
        return '23'
    elif quality == '17':
        return '24'
    elif quality == '18':
        return '25'
    elif quality == '19':
        return '26'
    elif quality == '20':
        return '27'
    elif quality == '21':
        return '28'
    elif quality == '22':
        return '29'
    elif quality == '23':
        return '30'
    elif quality == '24':
        return '31'
    elif quality == '25':
        return '32'
        
        
def gl_maxfilesize():
    quality = ADDON.getSetting('glmaxfilesize')
    if quality == '0':
        return ''
    elif quality == '1':
        return '8'
    elif quality == '2':
        return '9'
    elif quality == '3':
        return '10'
    elif quality == '4':
        return '11'
    elif quality == '5':
        return '12'
    elif quality == '6':
        return '13'
    elif quality == '7':
        return '14'
    elif quality == '8':
        return '15'
    elif quality == '9':
        return '16'
    elif quality == '10':
        return '17'
    elif quality == '11':
        return '18'
    elif quality == '12':
        return '19'
    elif quality == '13':
        return '20'
    elif quality == '14':
        return '21'
    elif quality == '15':
        return '22'
    elif quality == '16':
        return '23'
    elif quality == '17':
        return '24'
    elif quality == '18':
        return '25'
    elif quality == '19':
        return '26'
    elif quality == '20':
        return '27'
    elif quality == '21':
        return '28'
    elif quality == '22':
        return '29'
    elif quality == '23':
        return '30'
    elif quality == '24':
        return '31'
    elif quality == '25':
        return '32'

def gl_fileext():
    quality = ADDON.getSetting('glfileext')
    if quality == '0':
        return ''
    elif quality == '1':   
        return 'AVI'
    elif quality == '2':
        return 'MKV'
    elif quality == '3':
        return 'MP4'
    elif quality == '4':
        return 'ISO'
    elif quality == '5':
        return 'DIVX'
    elif quality == '6':
        return 'MPG'
    elif quality == '7':
        return 'FLV'
    elif quality == '8':
        return 'WMV'
    elif quality == '9':
        return 'MOV'
    elif quality == '10':
        return 'ASF'
    elif quality == '11':
        return 'RM'

def gl_subject():
    return ADDON.getSetting('glsubject')
    
def gl_poster():
    return ADDON.getSetting('glposter')
    
def gl_newsgroup():
    return ADDON.getSetting('glnewsgroup').replace(',','%2c')
    
def gl_vcodec():
    return ADDON.getSetting('glvcodec')
    
def gl_acodec():
    return ADDON.getSetting('glacodec')
    
def gl_filename():
    return ADDON.getSetting('glfilename')
    
def gl_results():
    return ADDON.getSetting('glresults')

def gl_spam():
    if ADDON.getSetting('glspam') == "true":
        return '&spamf=1'
    if ADDON.getSetting('glspam') == "false":
        return ''

def gl_rem():
    if ADDON.getSetting('glrem') == "true":
        return '&u=1'
    if ADDON.getSetting('glrem') == "false":
        return ''
        
def gl_grex():
    if ADDON.getSetting('glgrex') == "true":
        return '&gx=1'
    if ADDON.getSetting('glgrex') == "false":
        return ''
        
def gllang_ex():
    return ADDON.getSetting('gllangex').replace(' ','+')
    
def gl_reso():
    quality = ADDON.getSetting('glreso')
    if quality == '0':
        return '&px1=&px1t=&px=&px2t='
    if quality == '1':
        return '&px1=&px1t=&px2=&px2t=9'
    elif quality == '2':
        return '&px1=&px1t=5&px2=&px2t=9'
    elif quality == '3':
        return '&px1=&px1t=8&px2=&px2t=10'

  
def imdbtv_watchlist_url():
    return "http://akas.imdb.com/user/" + ADDON.getSetting('imdb_user') + "/watchlist?start=1&view=grid&sort=listorian:asc&defaults=1"
    
def imdb_list_url():
    return 'http://akas.imdb.com/user/' + ADDON.getSetting('imdb_user')
    
    

