#!/usr/bin/python3

import string

flag = [281,547,54,380,392,98,158,440,724,218,406,672,193,457,694,208,455,745,196,450,724]

def enc(plaintext, key):
    def f(x):
        yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727

    # g is a generator with the key == id(f), f will yield one integer per next call to xor the bytes of the plaintext with.
    # to leak the original key we can xor the known PT with the bytes of the output.txt    
    g=f(key)
    return map(lambda c:ord(c)^next(g),list(plaintext))

known_pt_start = "rarctf{"
print("Known Plaintext: %s" % known_pt_start)
known_flag_bytes = []
for i in range(len(known_pt_start)):
    known_flag_bytes.append(ord(known_pt_start[i])^flag[i])

print("Known flag bytes: %s" % known_flag_bytes)

def check(key):
    def f(x):
        yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727
    g=f(key)
    return map(lambda c:next(g), known_flag_bytes)

# Since we can guess what the generator will return based on the known plaintext we can find a
# number < 727 that will yield the same series. We dont need to search past 727 since all 
# generator results are modulo 727
enckey = 0
for t in range(0,727):
    res = list(check(t))
    if res == known_flag_bytes:
        enckey = t
        print("Suitable key found: %d" % enckey)
        continue

# brute force encrypt byte by byte with the key we just found comparing the encrypted byte
# with the known output.txt. If its the same then we know the flag byte in the position.
def inner(ptflag):
    for char in string.printable:
            test = ptflag + char
            ct = list(enc(test, 470))
            if ct[i] == flag[i]:
                ptflag = ptflag + char
                return ptflag

ptflag = ''
for i in range(len(flag)):
    ptflag = inner(ptflag)

print("%s" % ptflag)
