#!/usr/bin/python

import subprocess
import sys
import json

if len(sys.argv) < 2:
	print "Usage: ./extract-firmware.py <firmwarefilename>"
	quit()

firmwarefile = sys.argv[1]

print "[*] Walking firmware binary " + firmwarefile

for line in subprocess.check_output(["binwalk",firmwarefile]).splitlines():
	if 'Squashfs' in line:
		sfsoffset = line.split()[0]
		sfssize   = line.split()[10]
		print "[+] Squashfs found at offset " + sfsoffset + " size " + sfssize + " bytes"


print "[*] Extracting Squashfs from " + firmwarefile
ddout = subprocess.check_output(["dd","if="+firmwarefile,"bs=1","skip="+sfsoffset,"count="+sfssize,"of="+firmwarefile+".squashfs"])

print "[*] Unsquashing Squashfs from " + firmwarefile + ".squashfs"
unsqout = subprocess.check_output(["unsquashfs",firmwarefile+".squashfs"])

print "[*] Parsing mongodb configuration..."
dbcfg = open('squashfs-root/etc/mongod.conf','r').read().splitlines()

for line in dbcfg:
	if 'dbPath:' in line:
		dbpath = "squashfs-root" + line.split()[1]
		print "[+] MongoDB found in " + dbpath


print "[*] Dumping mongodb..."
dbdump = subprocess.check_output(['mongodump','--dbpath',dbpath])
print "[*] Dumping users.bson..."
bsondump = subprocess.check_output(['bsondump','dump/gnome/users.bson'])

print bsondump
