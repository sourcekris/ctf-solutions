#!/usr/bin/python

import subprocess
import string

allkeys = open('all_keys.txt','r').readlines()

print "[*] Extracting all modulii from all_keys.txt ..."

modulii = []

print "[*] Decrypting warrior.txt with all keys..."
for i in range(0,len(allkeys),9):
	buf = "".join(allkeys[i:i+9])
	open('tmpkey','w').write(buf)
	decrypted = subprocess.check_output(['openssl','rsautl','-pubin','-in','warrior.txt','-inkey','tmpkey','-verify','-raw'],stderr=subprocess.STDOUT)

	if 'fighter' in decrypted:
		print "[+] Flag: " + decrypted
		break

