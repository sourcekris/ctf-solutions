#!/usr/bin/python

from pwn import *

powfile = "pov.xml"
host, port = "cgc.cykor.kr", 34523
conn = remote(host,port)
print conn.recvline()
conn.sendline("XML")
powdata = open(powfile,'rb').read()
print "[*] POW:",powfile
print "[*] POW len:",len(powdata)
print conn.recvline()
conn.sendline(str(len(powdata)))
print conn.recvline()
conn.sendline(powdata)
conn.interactive()

