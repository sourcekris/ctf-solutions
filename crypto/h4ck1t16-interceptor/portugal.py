#!/usr/bin/python

# RSA broadcast attack for Interceptor challenge @ H4ckIT 2016
# @ctfkris - Capture the Swag

import libnum

rsashit = [int(x.strip().split('=')[1]) for x in open('EvelSniff_c637ac54760f179a5aa3e164847405fa.log').readlines() if '=' in x]

n_0 = rsashit[1]
n_1 = rsashit[4]
n_2 = rsashit[7]

ct_0 = rsashit[2]
ct_1 = rsashit[5]
ct_2 = rsashit[8]

# product of all moduli
N_012 = n_0 * n_1 * n_2

# n1 * n2
m_s_0 = n_1 * n_2
# n0 * n2
m_s_1 = n_0 * n_2
# n0 * n1
m_s_2 = n_0 * n_1

crt = libnum.solve_crt([ct_0,ct_1,ct_2], [n_0,n_1,n_2])

c_0 = crt % n_0
c_1 = crt % n_1
c_2 = crt % n_2

result = ((c_0 * m_s_0 * libnum.invmod(m_s_0, n_0)) + (c_1 * m_s_1 * libnum.invmod(m_s_1, n_1)) + (c_2 * m_s_2 * libnum.invmod(m_s_2, n_2))) % N_012 

pt = libnum.nroot(result, 3)
print libnum.n2s(pt)
