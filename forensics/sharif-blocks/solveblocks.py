#!/usr/bin/python

import sqlite3
import binascii
import struct
import itertools

# limit the number of candidate PNGs to this
LIMIT = 3100

print "[*] Fixing the SQLite file..."
orig = "SQLite format"
orig += open('data3','rb').read()
open('data3.sqlite','wb').write(orig)

print "[*] Extracting the PNG Data from SQLite DB..."
conn = sqlite3.connect('data3.sqlite')
cursor = conn.cursor()

# PNG Magic bytes
png = "\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0d"

# get IHDR first
ihdr = "IHDR" 
cursor.execute("SELECT Data FROM data WHERE Cat = 4")
ihdr += str(cursor.fetchone()[0])
ihdr += "\x89\xb8\x68\xee\x00\x00\x03\x00" # CRC32

# Next the PLTE
plte = "PLTE"
cursor.execute("SELECT Data FROM data WHERE Cat = 7")
plte += str(cursor.fetchone()[0])
plte += "\xe2\xb0\x5d\x7d\x00\x00\x00\x02"

# Next the tRNS
trns = "tRNS"
cursor.execute("SELECT Data FROM data WHERE Cat = 8")
trns += str(cursor.fetchone()[0])
trns += "\xe5\xb7\x30\x4a\x00\x00\x0b\xc3"

# finally the IDAT
idat = "IDAT"
cursor.execute("SELECT Data FROM data WHERE Cat = 2")

puzzle = []
known  = [None] * 11
for row in cursor.fetchall():
	if str(row[0])[0] == "\x78":		# known 1st block
		known[0] = str(row[0])		
	elif str(row[0])[0] == "\x5c":		# learned 2nd block
		known[1] = str(row[0])		
	elif str(row[0])[0] == "\x13":		# learned 3rd block
		known[2] = str(row[0])		
	elif len(str(row[0])) == 270:		# known final block
		known[10] = str(row[0])		
	else:
		puzzle.append(str(row[0]))

idat += "".join(known[0:3])

# define an IEND for later
iend = "IEND" + "\xae\x42\x60\x82"

print "[*] Building potential flag PNGs..."
 
counter = 0
for i in itertools.permutations(puzzle, 7):

	if counter > LIMIT:
		quit()

	image = idat + "".join(i)
	image += known[10]
	image += "\x08\x8d\x8d\xb6\x00\x00\x00\x00"
	open(str(counter).zfill(6) + '.png','wb').write(png + ihdr + plte + trns + image + iend)
	counter += 1
