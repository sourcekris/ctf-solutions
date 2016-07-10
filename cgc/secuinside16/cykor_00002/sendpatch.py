#!/usr/bin/python

from pwn import *

powfile = "cykor_00002.patched"
host, port = "cgc.cykor.kr", 34632
conn = remote(host,port)
print conn.recvline()
powdata = open(powfile,'rb').read()
conn.sendline(str(len(powdata)))
print conn.recvline()
conn.sendline(powdata)
conn.interactive()

