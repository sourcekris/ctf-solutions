#!/usr/bin/python

import os
import itertools

from Crypto.Hash import MD5

from pwn import *

HOST = 'bringthenoise.insomnihack.ch'
PORT = 1111

POWLEN = 5

conn = remote(HOST, PORT)
challenge = conn.recvline().split()[2]
print "[*] Got challenge: " + challenge

responsehash = ""
charset = "abcdefghijklmnopqrstuvwxyz0123456789"

for i in itertools.product(charset, repeat=5):
	responsehash = MD5.new(''.join(i)).hexdigest() 
	
	if responsehash[:POWLEN] == challenge:
		response = ''.join(i)
		break

print "[*] Sending challenge response: " + response
conn.sendline(response)

puzzle = conn.recvlines(40)

print "[*] Received equation sets. Computing candidate solutions..."

def checkmath(attempt, equation, result):
	check = sum([attempt[i]*equation[i] for i in range(6)]) % 8
	
	if check == result or check == (result + 1) or check == (result - 1):
		return True
	else:
		return False

for k in itertools.product(range(8),repeat=6):
	truthlist = []
	for p in puzzle:
		coefs  = map(int, p.split(",")[:6])
		result = int(p.split(",")[6])

		if checkmath(k,coefs,result):
			truthlist.append(1)

	if len(truthlist) > 30:
		print "[+] " + repr(k) + " Satisfied " + str(len(truthlist)) + " equations"
		solution = map(str, k)
		conn.recvline()
		conn.sendline(", ".join(solution))
		flag = conn.recvline()
		print "[+] Got flag: " + flag

