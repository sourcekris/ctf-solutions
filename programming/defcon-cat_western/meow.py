#!/usr/bin/python

from pwn import *
import subprocess
import re
import os

HOST='catwestern_631d7907670909fc4df2defc13f2057c.quals.shallweplayaga.me'
PORT=9999

conn = remote(HOST,PORT)

print "[+] Getting register states."
regstates = conn.recvuntil("****Send")

# Store the states in a list
initials = []
for register in regstates.splitlines():
	if '****' in register:
		continue
	else:
		initials.append(register.split("=")[0])
		initials.append(register.split("=")[1])
			
conn.recvline()
size = int(conn.recvline().split(" ")[3],10)
data = conn.recvn(size)
print "[+] Received binary data of size " + str(size)
with open('data.bin','wb') as f:
	f.write(data) 

print "[+] Building GDB script ..."
with open('gdbscript.txt','wb') as f:
	f.write("pset option ansicolor off\nbr main\nr\n")
	a = 0
	while a < len(initials):
		f.write("set $" + initials[a] + "=" + initials[a+1]+"\n")
		a += 2
	
	f.write("info reg\nrestore data.bin binary $pc\nc\ninfo reg\nquit\n")

print "[+] Executing code..."
with open(os.devnull) as DEVNULL:
	gdbout = subprocess.check_output(['gdb','-x','gdbscript.txt','./hw'], stderr=DEVNULL)
print "[+] Parsing registers..."

foundsegv = 0
finals = []
for line in gdbout.splitlines():
	if 'Stopped reason: SIGSEGV' in line:	# the ret instruction causes segv
		foundsegv = 1
	
	i = 0
	while i < len(initials):
		if initials[i] in line and foundsegv > 0:
			finalval = re.split('\s+',line)[1]
			finals.append(initials[i])
			finals.append(finalval)
		i+=2

print "[+] Uploading final state registers..."
i = 0
while i < len(finals):
	payload = finals[i] + "=" + finals[i+1]
	print "[>>] " + payload
	conn.sendline(payload)
	i += 2
	
result = conn.recvall()
print "[+] Result: " + result
conn.close()
