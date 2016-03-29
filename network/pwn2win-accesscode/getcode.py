#!/usr/bin/python

import time
import sys
from pwn import *

host = 'access.pwn2win.party'
port = 8111
control_port = 1110

response = ""
prefix = "Code"

# outbound channel
conn = remote(host,port)

# control channel
l = listen(port=control_port, bindaddr='0.0.0.0')
c = l.wait_for_connection()
control_packet = c.recvline()
c.close()

print "[+] Received control packet: " + control_packet.strip()
op = control_packet.split()[0].replace("xor", "^").replace("mod","%")
cv = int(control_packet.split()[1].strip())

banner = conn.recvuntil('Code?')
print "[*] Code should be ready, killing tshark."
subprocess.call(['killall','-TERM','tshark'])
time.sleep(1)
ports = open('ports.txt','r').readlines()
if len(ports) > 1:
    print "[*] Got ports", repr(ports)
    for p in ports:
        p = int(p.strip())
        r = eval(str(p)+op+str(cv))
        print "[.] ", p,op,cv,"=",r
        response += str(r) 
        
response = prefix + response
print "[>] Sending: " + str(response)
conn.sendline(response)
result = conn.recvline()

if 'Wrong Key' in result:
    print "[-] Failed: " + result
    conn.close()
    quit()

conn.interactive()

