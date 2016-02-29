Kill the Devil
==============

Many of the Pragyan crypto challenges could be summed up as find a ciphertext, then find a relevant cipher and solve it. I’ve got one of those solutions and one other solution for this writeup.

In the former category we have Kill the devil. A 60 point challenge featuring a downloadable file “Problem.txt“. We grab the file and check it out:

    root@kali:~/pragyan/crypto/kill-the-devil# file Problem.txt 
    Problem.txt: ASCII text
    root@kali:~/pragyan/crypto/kill-the-devil# cat Problem.txt 
    4c6544144496414154444f434550474e5464857595241
  
Prior to the hint (shown above) being posted we tried a few methods to decode this, suspecting it to be a hex encoded ASCII string but the string contains an odd number of characters and if we zero pad it it does not decode to printable characters.

We found that “Kill the Devil” referred to killing or deleting the numbers 666. There are 3 “6” characters exactly in the Problem.txt. We remove and now can decode successfully!

    root@kali:~/pragyan/crypto/kill-the-devil# python -c 'print open("Problem.txt","r").read().strip().replace("6","").decode("hex")'
    LTADIAATDOCEPGNTHWYRA
    
Great ! But a ciphertext it seems. We analyse it with Crypto Crack and find the top 5 probable ciphers as follows:

    IC: 48,  Max IC: 142,  Max Kappa: 333
    Digraphic IC: 0,  Even Digraphic IC: 0
    3-char repeats: 0,  Odd spaced repeats: 50
    Avg digraph: 610,  Avg digraph discrep.: 129
    Most likely cipher type has the lowest score.
    
    Running Key............24
    Double CheckerBoard....27
    Route Transp...........31
    Seriated Playfair......32
    Nihilist Transp........32
  
We rule out CheckerBoard ciphers since it needs an even number of ciphertext characters. We try many variations of Running Key attacks, brute force and dictionary attacks with no luck. Finally we try Route Transposition and get lucky and spot the flag:

![The Flag](https://ctf.rip/wp-content/uploads/2016/02/route.png)
