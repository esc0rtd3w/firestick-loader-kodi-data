#
#  Simple meta data provider
#  All information is extracted from the name string using regular expressions
#  Only the watched status is written to CSV files (one per series) that reside in the cache folder
#
#  Copyright (C) 2015 Sean Poyser / QnD (camael@gmx.net)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import os 
import re


import wco_utils as utils
import sfile

DELIMETER = ';'

class metadata:
    def __init__(self):
        self.cache_dir      = ''
        self.titleMatch     = re.compile("^(.+?)(?:Season\s(\d+))?\s*(?:Episode\s*(\d+\s*(?:-\s*\d+)?)\s*[:-]?(.*))?$")
        self.lastContent = []
        self.lastName    = ''

    # Set the directory to store the watched files
    def SetDir(self, cache_dir):        
        self.cache_dir = cache_dir
        if not sfile.exists(self.cache_dir):
            sfile.makedirs(self.cache_dir)

        
    def SetImageDir(self, image_dir):
        self.image_dir = image_dir
        if not sfile.exists(self.image_dir):
            sfile.makedirs(self.image_dir)


    def SetSeriesImage(self, name, image):
        targetFile = self.GetSeriesImage(name)
        if not sfile.exists(targetFile):
	    import urllib2
            req = urllib2.Request(image)
            req.add_header('User-Agent', utils.getUserAgent())
            response = urllib2.urlopen(req)
            sfile.write(targetFile, response.read())
            response.close()
        return targetFile
    
    
    def GetSeriesImage(self, name):
        return os.path.join(self.image_dir, self.format_filename(name)+'.jpg')

        
    # Retrieve meta data from "name" and add it to the dict metaInfo
    # Names will be compatible to XBMC infoLabels
    def GetMetaData(self, name, metaInfo):
        # Extract data from name string
        titleInfo = self.titleMatch.match(name)
        
        # This is what we can find
        seriesName  = titleInfo.group(1)
        seasonNum   = titleInfo.group(2)
        episodeNum  = titleInfo.group(3)
        episodeName = titleInfo.group(4)
        
        # Season info is optional
        if not seasonNum:
            seasonNum = '1'
        
        # Set meta data
        try:    metaInfo['episode']     = episodeNum.strip()
        except: metaInfo['episode']     = ''

        try:    metaInfo['season']      = seasonNum.strip()
        except: metaInfo['season']      = ''

        try:    metaInfo['episodeSeriesName']  = seriesName.strip()
        except: metaInfo['episodeSeriesName']  = ''

        try:    metaInfo['episodeName'] = episodeName.strip()
        except: metaInfo['episodeName'] = ''

        
    # Set watched status for meta info dict
    # At least the meta info dict must define the field "seriesName"
    def SetWatchedStatus(self, metaInfo, status):
        # If the seriesName is not known then we do not know where to put the information
        if not metaInfo['episodeSeriesName']:
            return

        try:
            # Generate the file system friendly name
            fileName = os.path.join(self.cache_dir, 'watched_' + self.format_filename(metaInfo['episodeSeriesName']) + '.txt')
            fileName = fileName.strip()

            # Generate the field name from the meta info
            epName   = self._GenerateEPName(metaInfo)
            stateStr = '1' if status == True else '0'
            
            valueFound = False
            lines = []
            
            # If the file exists then read the content and try to find the content
            if sfile.isfile(fileName):
                lines = sfile.readlines(fileName)
                for idx, line in enumerate(lines):
                    if line.split(DELIMETER)[0] == epName:
                        lines[idx] = '%s%s%s' % (epName, DELIMETER, stateStr)
                        valueFound = True
                        break
                        
            # ... otherwise append the content
            if not valueFound:
                lines.append('%s%s%s' % (epName, DELIMETER, stateStr))
            
            # Write the file back
            sfile.writelines(fileName, lines)
        except Exception, e:
            print 'WCO EXCEPTION: WRITING METADATA: ' + str(e)
    
    

    # Get watched status for information stored in metaInfo. Must be
    # equal to the meta info that was used for storing the info. At least
    # the field "seriesName" must be defined
    def GetWatchedStatus(self, metaInfo):
        # Do nothing if we do not know where to look
        if not metaInfo['seriesName']:
            return False
            
        # Generate the file system friendly name
        fileName = os.path.join(self.cache_dir, 'watched_' + self.format_filename(metaInfo['episodeSeriesName']) + '.txt')
        fileName = fileName.strip()

        # If the file does not exist then we have not watched this entry yet
        if not sfile.isfile(fileName):
            return False
        
        try:
            # Check if we still know this file, otherwise try to open it
            # This way, the content will be read only once for consecutive requests on the same series
            if not metaInfo['episodeSeriesName'] == self.lastName:
                self.lastName    = metaInfo['episodeSeriesName']
                self.lastContent = sfile.readlines(fileName)
                
            # Generate a string for the episode
            epName = self._GenerateEPName(metaInfo)
            
            # Look this episode name up in the table
            for line in self.lastContent:
                line = line.split(DELIMETER)
                if line[0] == epName:
                    return line[1] == '1'

        except Exception,e:
            # Reset everything
            self.lastContent = []
            self.lastName    = ''
            print 'WCO EXCEPTION: READING META ' + str(e)
            raise

        return False

        
    # Generate the field from the meta info
    def _GenerateEPName(self, metaInfo):
        season = metaInfo['season']
        if not season:
            season = '0'

        episode = metaInfo['episode']
        if not episode:
            episode = '0'

        epTitle = metaInfo['episodeName']
        if not epTitle:
            epTitle = 'title'

        return season + 'x' + episode + epTitle.replace(DELIMETER,'')


    def format_filename(self, s):
        filename = utils.fileSystemSafe(s)
        filename = filename.replace(' ','_') # I don't like spaces in filenames.
        return filename