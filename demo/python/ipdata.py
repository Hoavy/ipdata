#!/usr/bin/env python
# coding: utf-8
#from __future__ import with_statement
import re, socket, sys
from struct import pack,unpack

class ipdata():
    def __init__(self):
        self.ipdatafile = './tinyipdata.dat'
        self.re = '';
        
    def setipdatafile(self,file):
        self.ipdatafile = file
        
    def ip2long(self,ip):
        return unpack("!I", socket.inet_aton(ip))[0]
        
    def convertip(self,ip):
        pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
        if pat.match(ip):
            ipdot = ip.split('.')
            #
            if int(ipdot[0]) == 10 or int(ipdot[0]) == 127 or (int(ipdot[0]) == 192 and int(ipdot[1]) == 168) or (int(ipdot[0]) == 172 and (int(ipdot[1]) >= 16 and int(ipdot[1]) <= 31)):
                self.re = '- LAN'
            elif int(ipdot[0]) > 255 or int(ipdot[1]) > 255 or int(ipdot[2]) > 255 or int(ipdot[3]) > 255 :
                self.re = '- Invalid IP Address'
            else :
                fp = None ; offset = 0 ;index = None ; index_length = index_offset = 0
                ip = pack('>i',self.ip2long(ip))
                ipdot[0] = int(ipdot[0])
                ipdot[1] = int(ipdot[1])
                if fp == None :
                    try:
                        fp = open(self.ipdatafile, 'rb')
                    except Exception, e:
                        return  '- Invalid IP data file'
                    
                    offset = unpack('>i', fp.read(4))[0]
                    index  = fp.read(offset - 4)
                    length = offset - 1028;
                    
                    start  = unpack('<i', index[ipdot[0] * 4] + index[ipdot[0] * 4 + 1] + index[ipdot[0] * 4 + 2] + index[ipdot[0] * 4 + 3])[0]
                    start = start * 8 + 1024

                    while start < length :
                        if index[start] + index[start + 1] + index[start + 2] + index[start + 3] >= ip :
                            index_offset = unpack('<i', index[start + 4] + index[start + 5] + index[start + 6] + '\x00')[0]
                            index_length = unpack('B', index[start + 7])[0]
                            break
                        else :
                            start = start+ 8
                            continue

                    fp.seek(offset + index_offset - 1024)
                    if index_length > 0 :
                        return '- ' + fp.read(index_length)
                    else :
                        return '- UnKnown'
        return self.re
    
if __name__ == '__main__':
    path = sys.path[0]
    file =  path[:-11]+'tinyipdata.dat'
    ip = '42.242.160.0'
    ipdata = ipdata()
    ipdata.setipdatafile(file)
    print 'ip %s => %s' %(ip,ipdata.convertip(ip))