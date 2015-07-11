#!/usr/bin/python

import ContinuedFractions, Arithmetic
import sys
import base64
import gmpy
import sympy
import math
import fractions
import struct

sys.setrecursionlimit(100000)

f = open('cap','rb')
rsastuff = f.read()
f.close()

rsatrunk = rsastuff.splitlines()

modulii = []
exponents = []
ciphers = []
for junk in rsatrunk:
	gear = junk.split(":")
	gear[0] = gear[0].replace("{","")
	gear[2] = gear[2].lstrip()
	gear[2] = gear[2].replace("}","")
	if "N" in gear[0]:	# handle the header
		continue
	modint = long(gear[0],16)
	expint = long(gear[1],16)
	ciphint = long(gear[2],16)
        modulii.append(modint)
	exponents.append(expint)
	ciphers.append(ciphint)

print "[+] Loaded " + str(len(ciphers)) + " ciphertexts and public keys."

def hack_RSA(e,n):
    print "[+] Wiener attack in progress..."
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)
    for (k,d) in convergents:
        #check if d is actually the key
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    return d

for a in range(len(modulii)):
	print "[+] Attacking n["+str(a)+"] and e["+str(a)+"]"
	hacked_d = hack_RSA(exponents[a], modulii[a])
	testd = str(hacked_d)
	if "None" in testd:
		continue
	else:
		print "[+] Found d = " + str(hacked_d)
		m = pow(ciphers[a], hacked_d, modulii[a])
		print "[+] Flag:"
		print("%0512x" %m).decode("hex")
		quit()
	
