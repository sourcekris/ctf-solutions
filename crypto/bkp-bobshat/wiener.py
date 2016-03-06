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

sys.setrecursionlimit(100000)

def wiener(e,n):
    time.sleep(1)
    frac = ContinuedFractions.rational_to_contfrac(e, n)
    convergents = ContinuedFractions.convergents_from_contfrac(frac)
    
    for (k,d) in convergents:
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    return d
