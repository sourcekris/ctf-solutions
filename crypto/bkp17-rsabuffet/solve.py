#!/usr/bin/python

from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.PublicKey import RSA
from secretsharing import PlaintextToHexSecretSharer as rs
import glob

def decrypt(private_key, ciphertext):
  if len(ciphertext) < 512 + 16:
    return None
  msg_header = ciphertext[:512]
  msg_iv = ciphertext[512:512+16]
  msg_body = ciphertext[512+16:]
  try:
    symmetric_key = PKCS1_OAEP.new(private_key).decrypt(msg_header)
  except ValueError:
    return None
  if len(symmetric_key) != 32:
    return None
  return AES.new(symmetric_key,
      mode=AES.MODE_CFB,
      IV=msg_iv).decrypt(msg_body)


if __name__=="__main__":
  cts = glob.glob('ciphertext-?.bin')
  keys = glob.glob('key-?.priv')

  secrets = []
  for k in keys:
     for c in cts:
        private_key = RSA.importKey(open(k).read())
        ciphertext = open(c,'rb').read()
        plaintext  = decrypt(private_key,ciphertext)
        
        if plaintext is not None:
           if 'Congrat' in plaintext:
              secrets = secrets + plaintext.splitlines()[1:]

  for sec1 in [x for x in secrets if '1-' in x]:
     for sec2 in [x for x in secrets if '4-' in x]:
        for sec3 in [x for x in secrets if '5-' in x]:
           rec = rs.recover_secret([sec1,sec2,sec3])
           if 'FLAG' in rec:
              print rec
