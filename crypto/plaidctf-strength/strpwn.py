#!/usr/bin/python

import sys

sys.setrecursionlimit(5000)  

# math code from http://h34dump.com/2013/05/volgactf-quals-2013-crypto-200/ 
def gcd(a, b):
  if a == 0:
    x, y = 0, 1;
    return (b, x, y);
  tup = gcd(b % a, a)
  d = tup[0]
  x1 = tup[1]
  y1 = tup[2]
  x = y1 - (b / a) * x1
  y = x1
  return (d, x, y)
 
#solve the Diophantine equation a*x0 + b*y0 = c
def find_any_solution(a, b, c):
  tup = gcd(abs(a), abs(b))
  g = tup[0]
  x0 = tup[1]
  y0 = tup[2]
  if c % g != 0:
    return (False, x0, y0)
  x0 *= c / g
  y0 *= c / g
  if a < 0:
    x0 *= -1
  if b < 0:
    y0 *= -1
  return (True, x0, y0)

# read all the rsa stuff into a buffer 
f = open('captured_827a1815859149337d928a8a2c88f89f','rb')
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
        if "N" in gear[0]:      # handle the header
                continue
        modulii.append(long(gear[0],16))
        exponents.append(long(gear[1],16))
        ciphers.append(long(gear[2],16))

print "[+] Performing common modulus attack..."

for a in exponents:
    for b in exponents:
        if a <> b:
		c1 = ciphers[exponents.index(a)]
		c2 = ciphers[exponents.index(b)]
		n = modulii[exponents.index(a)]
		(x, a1, a2) = find_any_solution(a, b, 1)
		if a1 < 0:
		    (x, c1, y) = find_any_solution(c1, n, 1)#get inverse element
		    a1 = -a1

		if a2 < 0:
		    (x, c2, y) = find_any_solution(c2, n, 1)
		    a2 = -a2

		m = (pow(c1, a1, n) * pow(c2, a2, n)) % n
		flag = ("%0512x" %m).decode("hex")

		if "flag" in flag: 
			print "[+] Flag: " + flag 
			quit()

		
 
		 
