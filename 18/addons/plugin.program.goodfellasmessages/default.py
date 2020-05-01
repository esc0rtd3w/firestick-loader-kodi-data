import os,sys,xbmc,xbmcplugin,xbmcaddon,xbmcgui,urllib,urllib2,re,time,datetime,string,StringIO,logging,random,array,htmllib,xbmcvfs
import common as Common #from common import * #import common
## ################################################## ##
## ################################################## ##
## Start of program
TypeOfMessage="t"; (NewImage,NewMessage)=Common.FetchNews(); 
Common.CheckNews(TypeOfMessage,NewImage,NewMessage,False); 
## ################################################## ##
## ################################################## ##