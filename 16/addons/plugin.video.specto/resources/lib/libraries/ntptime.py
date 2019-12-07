'''
    Copyright (C) 2013 Sean Poyser (seanpoyser@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time, datetime


def getNTPTime(host="pool.ntp.org"):
    port = 123
    buf = 1024
    address = (host, port)
    msg = '\x1b' + 47 * '\0'

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800L  # 1970-01-01 00:00:00

    # connect to server
    client = socket.socket(AF_INET, SOCK_DGRAM)
    client.sendto(msg, address)
    msg, address = client.recvfrom(buf)

    t = struct.unpack("!12I", msg)[10]
    t -= TIME1970
    return t

    return time.ctime(t).replace("  ", " ")

def checkDate():
    try:
        expirein = 1 * 60 * 60 * 24 * 5  # 5 days
        expirewhen = datetime.datetime.now() + datetime.timedelta(seconds=expirein)
        WhenExpire = int(time.mktime(expirewhen.timetuple()))
        NtpTime = getNTPTime()
        if WhenExpire < NtpTime:
            print "Datetime setup"
            return True
        else:
            return False
    except Exception as e:
        print "Error %s" % e
        return False


