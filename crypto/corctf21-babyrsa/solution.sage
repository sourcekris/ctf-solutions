#!/usr/bin/env sage
# 
# Not my writeup, original URL: https://hackmd.io/@LHyyoaqQRTGd0Pw3CjNUhw/ByHiLa1-t#babyrsa
#
# I took that code and generalised and commented it so I could understand it. Their writeup below:
# 
#    # We get partial information on the decimal digits of the primes p and q which make up n. Doing a bit of testing by using the
#    # full value of n, along with the value in the image, we can deduce that there are 41 missing digits. Therefore, we can write 
#    # p as:
#    #   
#    #  108294440701045353595867242719660522374526250640690193563048263854806748525172379331?????????????????????????????????????????341078269246532299656864881223
#    #
#    # where ? are the unknown digits. We can then form the polynomial k1 ∗ 10^71 + x ∗ 10^30 + k2 , with k1 and k2 being our leaked decimal digits. 
#    # 
#    # Then, notice that this polynomial has a small root mod p and therefore will also have a small root mod n, as p is a factor of n . Therefore, using coppersmith to solve for 
#    # x should give us the value of p, and from there decrypting the flag is trivial.
#    #
#    # However, one thing we need to be aware of is that the polynomial is not monic, and coppersmith requires our polynomial to be monic (i.e. the term of highest degree,
#    # in this case x, has the coefficent 1). With one x term, this is quite simple; we can just multiply the entire polynomial by the inverse of 10^30 mod n or alternatively
#    # just use sage’s .monic() to do it for you.
#
# Implementation below.

from Crypto.Util.number import long_to_bytes

n = 73542616560647877565544036788738025202939381425158737721544398356851787401183516163221837013929559568993844046804187977705376289108065126883603562904941748653607836358267359664041064708762154474786168204628181667371305788303624396903323216279110685399145476916585122917284319282272004045859138239853037072761
e = 65537
ct = 2657054880167593054409755786316190176139048369036893368834913798649283717358246457720021168590230987384201961744917278479195838455294205306264398417522071058105245210332964380113841646083317786151272874874267948107036095666198197073147087762030842808562672646078089825632314457231611278451324232095496184838

# prime size (base 10 digits)
ps = 155

# p msb and lsb
pm = 108294440701045353595867242719660522374526250640690193563048263854806748525172379331
pl = 341078269246532299656864881223

# size in base 10 digits for each
pms = len(str(pm))
pls = len(str(pl))

# how many digits are we missing?
mb = ps - pms - pls

# digits we need (including lsb digits)
need = mb + pls

print('pm    = %d (%d digits)' % (pm, pms))
print('pl    = %d (%d digits)' % (pl, pls))
print('mb    = %d digits' % (mb))
print('need  = %d digits' % (need))
print()
print("polynomial: %d * 10^%d + x * 10^%d + %d" % (pm, need, pls, pl))

P.<x> = PolynomialRing(Zmod(n), implementation='NTL')
poly = pm * 10^need + x * 10^pls + pl
f = poly.monic()
d_p = f.small_roots(X=10^mb, beta=mb/ps)[0]
p = int(poly(d_p))
q = n // p
assert p * q == n
d = pow(e, -1, (p-1)*(q-1))

print()
print(long_to_bytes(pow(ct,d,n)))