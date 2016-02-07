#!/usr/bin/python

import subprocess
import zlib
import os

inputfile = "start.pdf"

counter = 0

print "[*] Extracting sub-pdfs..."

while True:
	tmp1 = 'outfile' + str(counter) + ".zlib"
	tmp2 = str(counter) + ".pdf"
	with open('/dev/null') as DEVNULL:
		subprocess.call(['python','pdf-parser.py','-d',tmp1,inputfile],stdout=DEVNULL,stderr=DEVNULL)

	zdata = open(tmp1, 'rb').read()
	try:
		unzdata = zlib.decompress(zdata)
	except:
		print "[+] Cant uncompress this: " + tmp1 + " so we're done. "
		print "[+] Check " + str(counter-1) + ".pdf for password protected PDF..."
		break

	open(tmp2, 'wb').write(unzdata)

	os.unlink(tmp1)
	inputfile = tmp2
	counter += 1
