#!/usr/bin/python

import numpy
import re

clue = "0000000000,0000000000,0001111100,0000000100,0000001000,0000010000,0000100000,0001000000,0000000000,0000000000".split(",")

# this function does all the work
def play_life(a):
    xmax, ymax = a.shape
    b = a.copy() # copy grid & Rule 2
    for x in range(xmax):
        for y in range(ymax):
            n = numpy.sum(a[max(x - 1, 0):min(x + 2, xmax), max(y - 1, 0):min(y + 2, ymax)]) - a[x, y]
            if a[x, y]:
                if n < 2 or n > 3:
                    b[x, y] = 0 # Rule 1 and 3
            elif n == 3:
                b[x, y] = 1 # Rule 4
    return(b)

# replace (5, 5) with the desired dimensions
life = numpy.zeros((10, 10), dtype=numpy.byte)

for i in range(len(clue)):
	for j in range(len(clue[i])):
		if clue[i][j] == "1":
			life[i][j] = 1

for i in range(7):
    life = play_life(life)

strlife = repr(life).splitlines()

flag = ""

for line in strlife:
	flag += re.sub('[^0-1]','',line)
	flag += ","	

print "[+] Flag: " + flag[:-1]
