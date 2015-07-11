#!/usr/bin/python

import ContinuedFractions, Arithmetic
import time
import sys
import base64
import binascii
import gmpy
import sympy
import math
import fractions
import struct
import subprocess

sys.setrecursionlimit(100000)

# modulus from the RSA public key
n=0x323FADA9CFA3C3037E0B907D2CEA83B9AD3655092CB04AEED95500BCA4E366A06CB4D215C65BB3D630B779D27BDC8DCD907D655ACBDCEF465E411BEB1BE3DDDAABA20FB058E7850AA355EC1B89358602FDE7F8BE59D4150770CACC1B77B775F7CAA358167B3226515F15FCA8A4659FEA2C4EFB0360E31993DDE4D1C199832B89

# exponent from the RSA public key
e=0x1E4805A218009C7F779033E3378B07693F56B266786A295B32D7275AE2E2CD3449DAC7468CDAE9BB04F547EC759E560739E0D448EBBA0DED244095FE1D9B900A885AE931EC760715DBDEE4ACDDB6170B036753C8B572C8AF9A02EF370D41A0F2009388BFA042B9F1D0D0847E2FD6FD7AC9E231B17CC95D1DEC4540681262C919

def hack_RSA(e,n):
    time.sleep(1)
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
                    return d,phi

print "[+] Performing wiener attack..."
hacked_d,phi = hack_RSA(e, n)
print "[+] Found private exponent d = " + str(hacked_d)
print "[+] Found value for phi = " + str(phi)

p_val = sympy.Symbol('p_val')
eq = sympy.Eq(p_val*p_val + (n+1-phi)*p_val + n)
solved = sympy.solve(eq,p_val)

p_val = int(-1*(solved[0]))
q_val = int(-1*(solved[1]))

print "[+] Found the value of prime 1, p = " + str(p_val)
print "[+] Found the value of prime 2, q = " + str(q_val)
print "[+] Running rsatool.py to create a private key..."
rsatool = subprocess.check_output(['python', 'rsatool.py', '-o', 'key.private', '-p', str(p_val), '-q',str(q_val),'-e',str(long(e))])
print "[+] Running decryptor.py to decrypt the ciphertext.bin..."
flag = subprocess.check_output(['python', 'decryptor.py'])
print "[+] Flag: " + flag


