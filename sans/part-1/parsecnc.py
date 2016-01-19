#!/usr/bin/python
#
# sewid666@gmail.com - parse sans pcap
#
# 19dec15
#

import subprocess
import base64
import os

beginfile 	= False
bigdata 	= []

# use tshark to extract the DNS TXT response data as well as lengths
with open('/dev/null') as DEVNULL:
	proc = subprocess.Popen(['tshark','-T','fields','-e','dns.txt','-e','dns.txt.length','-e','frame.number','-r','giyh-capture.pcap'],stdout=subprocess.PIPE,stderr=DEVNULL)
	rawdata = proc.communicate()[0].splitlines()

for frame in rawdata:
	framedata = frame.split('	')
	if framedata[0]:
		cmd = base64.b64decode(framedata[0]).strip()

		if beginfile == True:
			bigdata.append(base64.b64decode(framedata[0]).replace('FILE:',''))
		else:
			print "Frame: " + framedata[2] + " " + cmd

		if "FILE:START_STATE" in cmd:
			fname = os.path.basename(cmd.split('NAME=')[1])
			beginfile = True

		if "FILE:STOP_STATE" in cmd:
			print cmd
			beginfile = False
			open(fname,'wb').write(''.join(bigdata))
			print "[*] Wrote " + fname + " to disk."
