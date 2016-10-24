#!/usr/bin/python

import requests
import string

url = "https://cthulhu.fluxfingers.net:1505/"

user = "flag:"
suffix1 = "BCDEFGHIJKL"

s = requests.Session()
baseline = []

while True:
    for i in range(50):
        print "[*] Char",i,", performing baseline:"
        # baseline test
        print "[*] Baseline test: user="+user+"#"+suffix1
        r = s.get(url, params={'user':user+"#"+suffix1})
        auth = r.cookies['auth']
        baseline.append(len(auth))
        print "[*] AuthLen:",baseline[i]

        before = len(user)

        for c in string.printable:
            userfield = user+c+suffix1
            r = s.get(url, params={'user':userfield})
            auth = r.cookies['auth']
            if len(auth) < baseline[i]:
                user += c
                print "[*] flag so far:",user
                break

        if len(user) == before:
            print "[*] Flag: flag{"+user.replace('flag:','')+"}"
            quit()
