#!/usr/bin/python
#
# Extract the VNC keystrokes from a PCAP using tshark
#
# kris, Capture The Swag
#
# http://github.com/sourcekris/
#

import subprocess
import sys
import os
import re

if len(sys.argv) < 2:
	print "Usage: " + sys.argv[0] + " <pcap or pcapng>"
	sys.exit(-1)

# read the tshark data in PDML format - hope its not huge
DEVNULL = open(os.devnull,'w')
print "[+] Reading pcap file: " + sys.argv[1]
pdmllines = subprocess.check_output(['tshark','-r',sys.argv[1],'-Tpdml'],stderr=DEVNULL).splitlines()

message = []
keydown = False
for line in pdmllines:
	if 'name="vnc.key_down"' in line and 'showname="Key down: Yes"' in line:
		keydown = True
	elif 'name="vnc.key_down"' in line and 'showname="Key down: No"' in line:
		keydown = False
	elif keydown and 'name="vnc.key"' in line and 'showname="Key: ' in line:
		keyval = re.sub(r'[^a-f0-9]','',line.split('value=')[1])[-2:]
		try:
			chr(int(keyval,16)).decode('ascii')
		except:
			pass
		else:
			message.append(chr(int(keyval,16)))

		
print "[+] Message: " + "".join(message)
	
