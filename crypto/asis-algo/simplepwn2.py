#!/usr/bin/python

import string
import itertools

# try n-grams of how many characters at a time?
atatime=4

# Example:  ASIS{b026324c6904b2a9cb4b88d6d61c81d1}
initflag = 'ASIS{00000000000000000000000000000000}'

encint = "2712733801194381163880124319146586498182192151917719248224681364019142438188097307292437016388011943193619457377217328473027324319178428"

def FAN(n, m):
    i = 0
    z = []
    s = 0
    while n > 0:
    	if n % 2 != 0:
    		z.append(2 - (n % 4))
    	else:
    		z.append(0)
    	n = (n - z[i])/2
    	i = i + 1
    z = z[::-1]
    l = len(z)
    for i in range(0, l):
        s += z[i] * m ** (l - 1 - i)
    return s

def enc(plaintext):
	hflag = plaintext.encode('hex')
	iflag = int(hflag[2:], 16)
	i = 0
	r = ''
	while i < len(str(iflag)):
	    d = str(iflag)[i:i+2]
	    nf = FAN(int(d), 3)
	    r += str(nf)
	    i += 2

	return r 

def compareit(attemptstr):
       enclist = list(encint)
       attempt = list(attemptstr)
       correct = 0
       for c in range(len(enclist)):
       	   if attempt[c] == enclist[c]:
       		correct += 1 
           else:
                break

       return correct


# start exchanging pairs at the n'th column
startchar = 5
# baseline from that column of correct integers in output
baseline  = 14
alphabet = '0123456789abcdef'
pair = startchar
currentflag = initflag

print "[+] Cracking ciphertext..."

while pair < len(initflag)-1:

	# special case for the final two characters
	flaglist = list(currentflag)
	goodresults = []
	# for every pair of hexdigits
	for maybe in itertools.product(alphabet, repeat=atatime):	
		flaglist[pair] = maybe[0]
		flaglist[pair+1] = maybe[1]
		flaglist[pair+2] = maybe[2]
		flaglist[pair+3] = maybe[3]

		tryflag = "".join(flaglist)
		attempt = enc(tryflag)
		result = compareit(attempt)
		if result > baseline+2:
			#print "[+] " + repr(maybe) + "baseline: " + str(baseline) + " result: " + str(result)
			maybelist = list(maybe)
			maybelist.append(result)
			goodresults.append(maybelist)
			
	bestresult = 0
	bestfit = ""

	# Parse the good results looking for the best result
	for r in goodresults:
		if r[atatime] > bestresult:
			bestresult 	= r[atatime]
			flaglist[pair] 	= r[0]
			flaglist[pair+1] = r[1]
			flaglist[pair+2] = r[2]
			flaglist[pair+3] = r[3]

	currentflag = "".join(flaglist)
	print "[+] Flag so far: " + currentflag
			
	pair += atatime

print "[+] Flag: " + currentflag
