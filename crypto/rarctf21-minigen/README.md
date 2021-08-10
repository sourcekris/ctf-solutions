#### <a name="minigen"></a>Minigen - Crypto - 100 Points

This challenge reads:

```
A stream cipher in only 122 bytes!

Note: This has been tested on python versions 3.8 and 3.9
(141 solves)
```

With the challenge we get these files:

* `minigen.py`
* `output.txt`

The output.txt contains a list of numbers, judging by the clue and filename I assumed these were the encrypted bytes that are the result of the given stream cipher:

```
281 547 54 380 392 98 158 440 724 218 406 672 193 457 694 208 455 745 196 450 724
```

The python script is the entire stream cipher algorithm:

```python
exec('def f(x):'+'yield((x:=-~x)*x+-~-x)%727;'*100)
g=f(id(f));print(*map(lambda c:ord(c)^next(g),list(open('f').read())))
```

The python is written in a mildly obtuse way but its fairly easy to reconcile into re-usable code which I did for purposes of understanding how it worked better. Re-written the code looks like this:

```python
flag = [281,547,54,380,392,98,158,440,724,218,406,672,193,457,694,208,455,745,196,450,724]

def enc(plaintext, key):
    def f(x):
        yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727

    # g is a generator with the key == id(f), f will yield one integer per next call.
    g=f(key)
    return map(lambda c:ord(c)^next(g),list(plaintext))

```

Useful to note here is the following observations:

1. `g` is a generator used with a seed that will return key bytes. In the default code the key generator is seeded with the key `id(f)`.
2. In python the  `id()` built-in is used to return the memory address of the object referenced. In our case in the code provided it will return the memory address of the function `f`.
3. This means the seed to the key generator is always random and there's too many possible memory addresses to brute-force.
4. The constraint that helps us though is that every call to the generator returns a number modulo 727. So there are really only 727 possible seed values reducing the keyspace a huge amount.
5. There were originally 100 x `yield` statements in the `enc` function but the flag is only 21 bytes long so we're only ever going to ask it for 21 key bytes so we just need 21 yields.

Now we know how the key is generated we need to know how the encryption happens. In our case it simply `XOR`s the bytes of the plaintext by the bytes of the key generator. In order to figure out what seed was used to generate the key in our `output.txt` we can conduct a known plaintext attack against it since we know the flag format is always `rarctf{...}`

```python
flag = [281,547,54,380,392,98,158,440,724,218,406,672,193,457,694,208,455,745,196,450,724]

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
```

This finds a suitable seed value of `470` which yields the flag bytes in the correct order so will likely be enough to illuminate the entire flag.

```
$ python3 getkey.py 
Known Plaintext: rarctf{
Known flag bytes: [363, 578, 68, 287, 508, 4, 229]
Suitable key found: 470
```

We know the cipher is a stream cipher and we know the seed used to generate the key, so we can now go ahead brute force the plaintext and compare against the known ciphertext (encrypted flag). Once the two are equal we have our plaintext flag. The following code gets the job done.

```python
import string

flag = [281,547,54,380,392,98,158,440,724,218,406,672,193,457,694,208,455,745,196,450,724]

def enc(plaintext, key):
    def f(x):
        yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727;yield((x:=-~x)*x+-~-x)%727   
    g=f(key)
    return map(lambda c:ord(c)^next(g),list(plaintext))

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
```

Which finds our flag very quickly:
```shell
$ python solve.py
rarctf{pyg01f_1s_fun}
```
