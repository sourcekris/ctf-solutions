#!/usr/bin/python

from pwn import *

host = 'legit_00003_25e9ac445b159a3d5cf1d52aea007100.quals.shallweplayaga.me'
port = 32648

pov = 'mypov'
povbin = open(pov,'rb').read()
povlen = str(len(povbin))

conn = remote(host,port)

povlenq = conn.recvline()
print "[*] Sending length:",povlen
conn.sendline(povlen)
sendreq = conn.recvline()
print "[*] Sending pov:"
conn.sendline(povbin)
conn.interactive()
