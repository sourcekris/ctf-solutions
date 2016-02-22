#!/usr/bin/python

clear = open('Heart_clear.txt', 'rb').read()
crypt = open('Heart_crypt.txt','rb').read()

key = []
for i in range(0,len(clear)):
	key.append(chr(ord(clear[i]) ^ ord(crypt[i])))

xorkey = "".join(key)

print "[+] XOR Key: " + repr(xorkey)

mind = open('Mind_crypt.txt','rb').read()

flag = []
for i in range(0,len(mind)):
	flag.append(chr(ord(mind[i]) ^ ord(xorkey[i])))

print "[+] Flag: " + "".join(flag)
