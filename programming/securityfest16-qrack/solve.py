#!/usr/bin/python

import glob
import sys

files = glob.glob("*")
files.remove('solve.py')
files.remove('all')

alldata = [x.strip() for x in open('all').readlines()]

b64chunks = []
l = 0
while l < len(alldata):
    fourblock = []
    fourblock.extend(alldata[l:l+4])
    try:
        if alldata[l+3].endswith('=') or alldata[l+3].endswith('AAA'):
            b64chunks.append(fourblock)
            l += 4
        else:
            fourblock.append(alldata[l+4])
            b64chunks.append(fourblock)
            l += 5
    except IndexError:
        break

filechunks = {}
for f in files:
    filechunks[f] = [x.strip() for x in open(f).readlines()]

for subchunk in b64chunks:
    gotit = False
    for piece in subchunk:  # the base64 chunk is piece
        if len(piece) > 10:
            for f in filechunks: # f is the filename
                for fsub in filechunks[f]:
                    if fsub == piece:
                        sys.stdout.write(f)
                        gotit = True
                        break
                if gotit:
                    break
print 
            

    


    
