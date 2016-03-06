#!/usr/bin/python

import libnum
import subprocess

################### LAYER 1 ######################
print "[*] Solving layer 1: Weak key factored with ECM method"
# layer 1 public key
n = 94738740796943840961823530695778701408987757287583492665919730017973847138345511139064596113422435977583856843887008168202003855906708039013487349390571801141407245039011598810542232029634564848797998534872251549660454277336502838185642937637576121533945369150901808833844341421315429263207612372324026271327
e = 65537

# layer 1 factored with ECC method
p = 9733382803370256893136109840971590971460094779242334919432347801491641617443615856221168611138933576118196795282443503609663168324106758595642231987245583
q = 9733382803370256893136109840971590971460094779242334919432347801491641617443615856221168611138933576118196795282443503609663168324106758595642231987246769 

# valid p and q right!?
assert(n % p == 0)
assert(n % q == 0)

c = libnum.s2n(open('almost_almost_almost_almost_there.encrypted','rb').read())
phi = (p - 1) * (q - 1)
d = libnum.invmod(e, phi)
m = pow(c,d,n)
zippassword = libnum.n2s(m)

################### LAYER 2 ######################
print "[*] Solving layer 2: Common factors!"
# unzip layer2
unzip = subprocess.check_output(['unzip','-o','-P',zippassword,'almost_almost_almost_almost_there.zip'])

# get next modulus
l2n = int(subprocess.check_output(['openssl', 'rsa', '-noout', '-modulus', '-pubin', '-in', 'almost_almost_almost_there.pub']).split('=')[1],16)

# load ciphertext
l2c = libnum.s2n(open('almost_almost_almost_there.encrypted','rb').read())

# layer 2 modulus has common factor with layer 1
l2q = libnum.gcd(l2n, n)
l2p = l2n / l2q
l2phi = (l2p - 1 ) * (l2q - 1)
l2d = libnum.invmod(e, l2phi)
l2m = pow(l2c, l2d, l2n)
l2zippass = libnum.n2s(l2m)

################### LAYER 3 ######################
print "[*] Solving layer 3: Small q "
unzip = subprocess.check_output(['unzip','-o','-P',l2zippass,'almost_almost_almost_there.zip'])
l3n = int(subprocess.check_output(['openssl', 'rsa', '-noout', '-modulus', '-pubin', '-in', 'almost_almost_there.pub']).split('=')[1],16)
l3c = libnum.s2n(open('almost_almost_there.encrypted','rb').read())


# small q, factored using ECM method or any simple method
l3q = 54311
l3p = l3n / l3q
l3phi = (l3p - 1) * (l3q - 1)
l3d = libnum.invmod(e, l3phi)
l3m = pow(l3c,l3d,l3n)
l3zippass = libnum.n2s(l3m)

################### LAYER 4 ######################
print "[*] Solving layer 4: Wieners attack!"
unzip = subprocess.check_output(['unzip','-o','-P',l3zippass,'almost_almost_there.zip'])
l4key = [(int(x.split(':')[3],16)) for x in subprocess.check_output(['openssl', 'asn1parse', '-in', 'almost_there.pub','-strparse','19']).splitlines() if 'INTEGER' in x]
l4c = libnum.s2n(open('almost_there.encrypted','rb').read())

# use Wiener attack to find d from n and e
from wiener import wiener
l4d = wiener(l4key[1],l4key[0])
l4m = pow(l4c, l4d, l4key[0])
l4zippass = libnum.n2s(l4m)

############## GET FLAG ###############
unzip = subprocess.check_output(['unzip','-o','-P',l4zippass,'almost_there.zip'])
print "[+] Flag: " + open('FLAG','r').read()

