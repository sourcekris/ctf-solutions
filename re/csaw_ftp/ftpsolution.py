#!/usr/bin/python

import itertools
from pwn import *

targethost = "54.175.183.202"

target = "d386d209"

alphabet = list("abcdefghijklmnopqrstuvwxyz")

def enc(a1):
  start = 0x1505;
  op = start << 5
  op = op + start
  for i in a1:
        op = op + ord(i)
        saveop = op
        op = op << 5
        op = op + saveop

  op = op + 10
  return str(hex(op))[-8:]

print "[+] Cracking password: 0x"+target

for i in itertools.product(alphabet, repeat=6):
        encrypted = enc(i)
        if(encrypted == target):
                print "[+] Found it: " + "".join(i)
                password = "".join(i)
                break


conn=remote(targethost, 12012)
print "[+] " + conn.recvline()
print "[+] Sending user: blankwall"
conn.sendline("USER blankwall")
print "[+] " + conn.recvline()
print "[+] Sending password: " + password
conn.sendline("PASS " + password)
print "[+] " + conn.recvline()
print "[+] Send RDF"
conn.sendline("RDF")
print "[+] Flag: " + conn.recvline()
conn.close()

