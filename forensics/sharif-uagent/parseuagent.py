#!/usr/bin/python

import subprocess
import os
import base64
import binascii
import re

print "[*] Extracting useragent strings from pcap..."
with open(os.devnull) as DEVNULL:
	uagents = subprocess.check_output(["tshark","-r","ragent.pcap","-T","fields","-e","http.user_agent"],stderr=DEVNULL).splitlines()
uagents = filter(None, uagents)

out = ""
for a in uagents:
	data64 = a.replace("sctf-app/","")[:-1]
	out += base64.b64decode(data64)

print "[+] Output into out.png..."
open('out.png','wb').write(out)

print "[*] Extracting files from pcap..."
with open(os.devnull) as DEVNULL:
	filedata = subprocess.check_output(["tshark","-r","ragent.pcap","-T","fields","-e","media.type", "-e", "http.request.line"],stderr=DEVNULL).splitlines()
filedata = filter(None, filedata)

outfiledata = []
for f in filedata:
	if "Range: bytes=" in f:
		bytefrom = int(f.split("=")[1].split("-")[0])
		byteto   = int(f.split("=")[1].split("-")[1])
	if re.match("[0-9a-f][0-9a-f]:",f):
		out = binascii.unhexlify(f.replace(":","").strip())
		outfiledata.append([bytefrom,byteto,out])

print "[*] Finding file size."
filesize = 0
for s in outfiledata:
	if s[1] > filesize:
		filesize = s[1]
print "[*] Found file size is: " + str(filesize)

print "[+] Output into out.zip..."
outf = open('out.zip','wb')
outf.write("\x00" * filesize)

for s in outfiledata:
	outf.seek(s[0],0)
	outf.write(s[2])

outf.close()

