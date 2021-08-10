#### sRSA - Crypto - 100 Points

This challenge, again in the Crypto category reads:

```
we have created the securest possible rsa algorithm!
(209 solves)
```

With the challenge we get these files:

* `script.py`
* `output.txt`

The output.txt contains the typical components of an RSA public key (`n`, `e`) and a ciphertext (`ct`).

```
n = 5496273377454199065242669248583423666922734652724977923256519661692097814683426757178129328854814879115976202924927868808744465886633837487140240744798219
e = 431136
ct = 3258949841055516264978851602001574678758659990591377418619956168981354029697501692633419406607677808798749678532871833190946495336912907920485168329153735
```

The python script is the crypto algorithm used to get us the `ct` ciphertext and looks like this:

```python
from Crypto.Util.number import *

p = getPrime(256)
q = getPrime(256)
n = p * q
e = 0x69420

flag = bytes_to_long(open("flag.txt", "rb").read())
print("n =",n)
print("e =", e)
print("ct =",(flag * e) % n)
```

Initially I went down weak PRNG or small prime avenue but neither of these worked out. 256 bits is small for an RSA prime but not small enough to factor for a CTF challenge usually. The `Crypto.Util.number.getPrime()`method uses `Random.new().read()`as a RNG and so isn't considered weak like the `random` standard library is as far as I could see.

Careful reading of the clue after some time and the solution stuck out at me. The encryption is performed incorrectly. In the script we have: `c = me mod n` whereas RSA is supposed to be `c = m^e mod n`. The result is a much weaker ciphertext as `m * e` is a much smaller number than `m ^ e` and so we can simply brute force the solution. 

I wrote the following code to get it done:

```python
from libnum import *

n = 5496273377454199065242669248583423666922734652724977923256519661692097814683426757178129328854814879115976202924927868808744465886633837487140240744798219
e = 431136
ct = 3258949841055516264978851602001574678758659990591377418619956168981354029697501692633419406607677808798749678532871833190946495336912907920485168329153735

for i in range(e):
    pt = ct // e
    pts = n2s(pt)
    if pts.startswith(b'rar'):
        print(pts)
        break
    ct += n
```

On the 1185th iteration we got the solution:

```shell
$ python3 solve.py 
b'rarctf{ST3GL0LS_ju5t_k1dd1ng_th1s_w4s_n0t_st3g_L0L!_83b7e829d9}'
```
