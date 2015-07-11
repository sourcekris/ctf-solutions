#!/usr/bin/python

from pwn import *

HOST='52.5.150.223'

for port in [13102,18264,18282]:
	conn = remote(HOST,port,typ="udp")
	conn.sendline("hi")
	conn.close()


conn = remote(HOST,10785)
conn.interactive()
