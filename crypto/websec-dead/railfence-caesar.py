#!/usr/bin/python

import base64

ct = "2v2w3z2yJsJwajTiaqIpILErELEM5pyqyo0"

# Test cases
testct = "t hhoeelrle"
testpt = "hello there"
testshift = "UAPV{ada_yjxajh_xh_vds}"
testplain = "FLAG{lol_juilus_is_god}"


def caesar(plainText, shift): 
  cipherText = ""
  for ch in plainText:
    if ch.isalpha() and ch.islower():
      stayInAlphabet = ord(ch) + shift 
      if stayInAlphabet > ord('z'):
        stayInAlphabet -= 26
      finalLetter = chr(stayInAlphabet)
      cipherText += finalLetter
    elif ch.isalpha() and ch.isupper():
      stayInAlphabet = ord(ch) + shift 
      if stayInAlphabet > ord('Z'):
        stayInAlphabet -= 26
      finalLetter = chr(stayInAlphabet)
      cipherText += finalLetter
    else:
      cipherText += ch
  return cipherText

def Railfence(text, rails, offset):
   while offset < 0:
      offset += rails * 2 - 2

   offset = offset % (rails * 2 - 2)
   return rail_decode(text, rails, offset )


def rail_decode(t,r,o):
   o_idx = [None] * ((r - 1) *2)
   out_a = [0] * r

   for i in range(len(o_idx)):
      j = (o + i) % len(o_idx)
      if j < r:
         o_idx[i] = j
      else:
         o_idx[i] = (2 * (r - 1)) - j
   
   for i in range(len(t)):
      out_a[o_idx[i % len(o_idx)]] += 1

   j = 0;
   for i in range(len(out_a)):
      out_a[i] = t[j:j + out_a[i]]
      j += len(out_a[i])
 
   j = "";
   for i in range(len(t)):
      k = o_idx[i % len(o_idx)]
      j += out_a[k][0]
      out_a[k] = out_a[k][1:len(out_a[k])]
   
   return j

assert(Railfence(testct, 5, 2) == testpt)
assert(caesar(testshift,11) == testplain)

for i in range(2,len(ct)):
    for j in range(len(ct)):
        for k in range(26):
            print base64.b64decode(caesar(Railfence(ct,i,j),k)+"=")
