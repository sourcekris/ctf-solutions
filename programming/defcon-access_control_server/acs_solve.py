#!/usr/bin/python

from pwn import *

HOST='access_control_server_f380fcad6e9b2cdb3c73c651824222dc.quals.shallweplayaga.me'
PORT=17069

username = 'duchess'
password = username[:5]
version = 'version 3.11.54'

def cipherpw(connectionid, password, offset):
	connectionid = connectionid[offset:]
	pl = list(password)
	cl = list(connectionid)
	result = ""
	for p in range(len(pl)):
		result += chr(ord(pl[p]) ^ ord(cl[p]))

	a1 = list(result)
	r2 = ""
	for i in range(5):
		if ord(a1[i]) <= 31:
			a1[i] = chr(ord(a1[i]) + 32)
		r2 += a1[i]
	return r2

conn = remote(HOST,PORT)

connectionid = conn.recvline().split(" ")[2]
print "[+] Connection ID: " + connectionid,
conn.recvlines(4)	# banner
conn.sendline(version)

o = 0
while True:
	conn.recvline()		# login prompt
	print "[+] Sending username: " + username
	conn.sendline(username)
	conn.recvline()		# password prompt
	print "[+] Sending password attempt " + str(o) + "..."
	conn.sendline(cipherpw(connectionid,password,o))
	result = conn.recvline()
	if 'what would you like to do' in result:
		print "[+] Login success with offset " + str(o)
		break
	else:
		print "[+] Retrying..."
	o += 1

conn.sendline('print key')
challenge = conn.recvline().split(" ")[1]
print "[+] Challenge received: " + challenge
conn.recvline() # answer prompt
for i in range(8):
	answer = cipherpw(connectionid, challenge, i)
	print "[+] Possible answer: " + answer

print "[+] Challenge response: " + answer
conn.sendline(answer)
print "[+] Result: " + conn.recvline()
conn.close()
