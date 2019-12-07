#   Google Analytics Python Script, Raw Media's Google Analytics Python Script
#   Copyright (C) 2014  Adam Parker
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import httplib, urllib

class GAconnection:
        
    def buildHeaders(self):
        self.Headers = {"Host": "www.google-analytics.com"}
        
    def buildParams(self):
        self.Params = [("v" , self.v),("tid" , self.tid), ("cid"  , self.cid)]

    def __init__(self, ProjectID, UserID):
        self.google = httplib.HTTPConnection("www.google-analytics.com")
        self.v = '1'
        self.tid = ProjectID
        self.cid = UserID
        self.buildHeaders()
        self.buildParams()
        
    def GASend(self):
		try:
			self.google.request("POST", "/collect", urllib.urlencode(self.Params), self.Headers)
		except:
			return -1
			
		return 1
        
    def GAResponse(self):
        try:
            response = self.google.getresponse()
            if response.status != "200":
                return -2
        except:
            return -1
            
        return 1
                        
    def sendEvent(self, EventCatagory, EventAction):
        self.buildParams()
        self.Body = [("t" , "event"), ("ec" , EventCatagory), ("ea" , EventAction)]
        self.Params = self.Params + self.Body
            
        self.GASend()
        return self.GAResponse()
            
        
    def sendPageView(self, DocumentHost, DocumentPath, DocumentTitle):
        self.buildParams()
        self.Body = [("t" , "pageview"),("dh" , DocumentHost),( "dp" , DocumentPath),( "dt" , DocumentTitle)]
        self.Params = self.Params + self.Body
        print self.Params
            
        self.GASend()
        return self.GAResponse()
