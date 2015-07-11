#!/usr/bin/python
#
# Captcha solver for VolgaCTF 2015.
# CaptureTheSwag - capturetheswag.blogspot.com
# by dacat

from pytesser import *
import os
import Image
import subprocess
import base64
import itertools

PNG_PATH='output/png/'
ATTEMPT_PATH='attempts/'
BEST_WIDTH=38
BEST_HEIGHT=50

# use factors of the total number of files or this will error
CHARS_WIDE=43

alphabet = ('I','l')
MAXLEN=11

print "[+] Foremosting input..."
subprocess.call(['foremost','-Q','capthca.png'])

pngfiles = [ f for f in os.listdir(PNG_PATH) if os.path.isfile(os.path.join(PNG_PATH, f)) ]
pngfiles.sort()
flag64 = ""
print "[+] Processing " + str(len(pngfiles)) + " image files " + str(CHARS_WIDE) + " characters at a time."
im = Image.new("RGB", (BEST_WIDTH * CHARS_WIDE,50), "white")
idx = 0
for f in pngfiles:
	letter = Image.open(PNG_PATH + f)
	width, height = letter.size
	left = (width - BEST_WIDTH)/2
	top = (height - BEST_HEIGHT)/2
	right = (width + BEST_WIDTH)/2
	bottom = (height + BEST_HEIGHT)/2
	letter = letter.crop((left,top,right,bottom))
	im.paste(letter,(idx*BEST_WIDTH,0))
	idx+=1
	if idx == CHARS_WIDE:
		im.show()
		thislot = image_to_string(im)	
		thislot = "".join(thislot.split())
		print "[+] OCRd: " + thislot
		check = raw_input("These ok? >> " )
		if 'n' in check:
			redo = list(thislot)
			chk = 0
			for r in redo:
				ok = raw_input("Correct this " + r + "["+r+"] >> ")
				if ok <> '':
					redo[chk] = ok
				chk += 1
			thislot = "".join(redo)
			flag64 += thislot		
			print "[+] Corrected: " + thislot
			subprocess.call(['killall','-9','display'])
		else:
			flag64 += thislot
			subprocess.call(['killall','-9','display'])
			
		flag64 = "".join(flag64.split())
		idx = 0
		im = Image.new("RGB", (BEST_WIDTH * CHARS_WIDE,50), "white")

subprocess.call(['rm','-fr','./output/'])
print "[+] OCR Completed. Creating permutations"
header=flag64[:361]
body=flag64[361:]

try:
	os.makedirs(ATTEMPT_PATH)
except OSError as exc:
	pass

# fiddle with all the l/I combinations and create a lot of PNGs
for i in itertools.product(alphabet, repeat=MAXLEN):
        idx = 0
        bodylist = list(body)
        for char in range(len(bodylist)):
                if 'I' in bodylist[char]:
                        bodylist[char] = i[idx]
                        idx += 1
                if idx >= MAXLEN:
                        flag = header + "".join(bodylist) 
                        flagbin = base64.b64decode(flag)
                        f=open(ATTEMPT_PATH+'attempt'+"".join(i)+".png", 'wb')
                        f.write(flagbin)
                        f.close()
                        break

print "[+] Completed, copy the png files from the " + ATTEMPT_PATH + " folder to a Windows system and find the flag!" 
