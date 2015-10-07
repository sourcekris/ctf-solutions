#!/usr/bin/python

from pwn import *
import os
binary = ELF('/tmp/...,,,...,,')
binary.write(0x400a33, '\xeb')
binary.save('/tmp/...,,,...,,.patched')
os.chmod('/tmp/...,,,...,,.patched',755)
p = process('/tmp/...,,,...,,.patched')
flag = p.recvuntil('}')
print "[+] Flag: " + flag
