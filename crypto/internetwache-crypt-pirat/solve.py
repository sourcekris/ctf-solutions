#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import codecs
import morse

ciphertext = codecs.open('README.txt','rb','utf-8').read()

# planets symbols from https://en.wikipedia.org/wiki/Planet#20th_century
# only 4 types are seen in the file
planets = { u'♀' : 2, u'⊕' : 3, u'♆' : 8, u'♇' : 9, ' ' : '' }

nextcipher = "".join([str(planets.get(c)) for c in ciphertext])

# split into integer pairs
nextcipher =  [nextcipher[i:i+2] for i in range(0, len(nextcipher),2)]

# tapir cipher decoder
tapir = {89:'.', 92:'-', 83:' ', 82:' '}

print "[+] Tapir code: " + repr(nextcipher)

# convert to morse code
themorse = "".join([tapir.get(int(c)) for c in nextcipher]).lstrip()

print "[+] Morse code: "  + themorse

# decode the morse code
data32 = morse.decodeMorse(themorse + " " )
print "[+] Base32: " + data32

#decode the b32
rot13 = base64.b32decode(data32)
print "[+] Rot13: " + rot13
print "[+] Flag: " + codecs.encode(rot13,'rot_13')
