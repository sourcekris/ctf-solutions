#!/usr/bin/python

from pwn import *
import binascii
import sys

e = 0x10001

#alice - http://factordb.com/index.php?query=1696206139052948924304948333474767
a_n = 0x53a121a11e36d7a84dde3f5d73cf
a_p = 44106885765559411
a_q = 38456719616722997

#bob - http://factordb.com/index.php?query=3104649130901425335933838103517383
b_n = 0x99122e61dc7bede74711185598c7
b_p = 62515288803124247
b_q = 49662237675630289

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return x

codez = open('strings.64').read().splitlines()

messages = []
for code in codez:
	msg = b64d(code).split(';')[0:3]
	out = []
	for m in msg:
		out.append(m.split('=')[1].strip().replace('0x','').replace('L',''))
	
	messages.append(out)		

flag = []
for msg in messages:
	seq = int(msg[0],10)
	c   = int(msg[1],16)
	sig = int(msg[2],16)

	d = egcd(e, (b_p - 1) * (b_q - 1))
	m = pow(c, d, b_n)
	v = pow(sig,e,a_n)	# calculate the actual signature
	
	if m == v:
		flag.append([seq,chr(m)])

flag.sort(key=lambda y: int(y[0]))
print "[+] flag: ",
for c in flag:
	sys.stdout.write(c[1])

print
