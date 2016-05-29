# AusCERT 2016 CTF - Unbreakable 2.0 - Crypto Challenge

According to the challenge text this was a re-implemented challenge first seen at the AISA 2015 CTF. Since that was an onsite event I had not seen or heard of it before. So I approached it as a new challenge.

The challenge consists of a file called unbreakable-2.0.tar.gz which when we download, unpacks to three files:

```
root@kali:~/auscert/unbreakable# tar xvf unbreakable-2.0.tar.gz 
unbreakable-2.0
key
encrypted_flag
root@kali:~/auscert/unbreakable# ls -la
total 28
drwxr-xr-x 2 root root    4096 May 29 19:12 .
drwxr-xr-x 3 root root    4096 May 29 19:12 ..
-rw-rw-r-- 1 1000 inetsim   29 May 19 13:56 encrypted_flag
-rwxrwxr-x 1 1000 inetsim  552 Apr 10 00:38 key
-rwxrwxr-x 1 1000 inetsim 6320 May 19 14:19 unbreakable-2.0
-rwxrw-rw- 1 root root    2833 May 25 14:23 unbreakable-2.0.tar.gz
root@kali:~/auscert/unbreakable# file unbreakable-2.0
unbreakable-2.0: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=773418f1f6e1f04c9b791cf99ca7f22f76aaf976, stripped
root@kali:~/auscert/unbreakable# cat encrypted_flag 
}umk|TTr3am_c2��S�w_u�grSet�
root@kali:~/auscert/unbreakable# cat key
William Shakespeare was an English poet, playwright, and actor, widely regarded as the greatest writer in the English language and the world's pre-eminent dramatist.[2] He is often called England's national poet, and the "Bard of Avon".[3][nb 2] His extant works, including collaborations, consist of approximately 38 plays,[nb 3] 154 sonnets, two long narrative poems, and a few other verses, some of uncertain authorship. His plays have been translated into every major living language and are performed more often than those of any other playwright.
```

When we check with strace, it's clear that the unbreakable-2.0 file is the program responsible for encrypting some original file called "flag" with the key stored in "key". The output is then sent to stdout and that is what the "encrypted_flag" file we have now contains.

So it's our task to use the key plus the binary to reverse the encryption process to recover the plaintext from the ciphertext.

We examine the binary in IDA Pro and quickly reverse the main function. The important parts are shown below:

```
    flag_fd = fopen("flag", "r");
    fgets(flag_input_buf, 29, flag_fd);
    if ( access("key", 0) == -1 )
    {
      result = 1LL;
    }
    else
    {
      key_fd = fopen("key", "r");
      fgets(key_input_buf, 29, key_fd);
      seed = 127;
      for ( i = 0; i <= 28; ++i )
      {
        key_byte = key_input_buf[i];
        flag_byte = flag_input_buf[i];
        seed = generate_next_seed(&seed);
        and_result = and_seed_with_key(&seed, &key_byte);
        ciphertext_byte = add_and_result_and_flag_byte(&and_result, &flag_byte);
        putchar(ciphertext_byte);
      }
```

The generate_next_seed() function looks like this:

```
__int64 __fastcall sub_4006BD(_DWORD *a1)
{
  unsigned __int8 input_seed; // [sp+Fh] [bp-9h]@1
  int i; // [sp+10h] [bp-8h]@1

  input_seed = *a1;
  for ( i = 0; i <= 0; ++i )
    input_seed = (input_seed >> 1) | ((input_seed ^ (input_seed >> 1)) << 7);
  return input_seed;
}
```

So the binary is taking a static seed value of 127, performing an operation on the value and returning the value which is then stored in the same memory address. This ensures that each iteration of the main loop uses a unique seed value. However since the original seed is static (always 127) then this function produces the same result for all inputs and we can therefore run it once to see all of it's possible values.

The fastest way to do this is with GDB so we set a breakpoint at the call to the generate_next_seed() function and examine the arguments:

```
root@kali:~/auscert/unbreakable# gdb -q ./unbreakable-2.0
Reading symbols from ./unbreakable-2.0...(no debugging symbols found)...done.
gdb-peda$ br *0x40086c
Breakpoint 1 at 0x40086c
gdb-peda$ display/1bx $rax
1: x/xb $rax  <error: No registers.>
gdb-peda$ c
The program is not being run.
gdb-peda$ r
Starting program: /root/auscert/unbreakable/unbreakable-2.0 
Breakpoint 1, 0x000000000040086c in ?? ()
1: x/xb $rax  0x7fffffffe2a8:   0x7f
gdb-peda$ c
Breakpoint 1, 0x000000000040086c in ?? ()
1: x/xb $rax  0x7fffffffe2a8:   0x3f
gdb-peda$ 
Breakpoint 1, 0x000000000040086c in ?? ()
1: x/xb $rax  0x7fffffffe2a8:   0x1f
gdb-peda$ c
...
```

We find that the following static seeds are generated: 

<ul>
    <li>0x3f,0x1f,0x0f,0x07,0x03,0x01,0x80,0x40,0x20,0x10,0x8,0x4,0x2,0x81,0xc0,0x60,0x30,0x18,0xc,0x6,0x83,0x41,0xa0,0x50,0x28,0x14,0xa,0x85</li>
</ul>

The next step in the unbreakable binary is that it performs a bitwise AND operation on the keystream and the generated seed. Finally it adds the value of the (keystream & seed) to the plaintext to arrive at the ciphertext.

This is all rather trivial, since we have the key, the seeds and the ciphertext, we can reverse the operations to decrypt the flag. The following python code takes care of the matter:

```
#!/usr/bin/python

ands = [ 0x3f,0x1f,0x0f,0x07,0x03,0x01,0x80,
         0x40,0x20,0x10,0x8,0x4,0x2,0x81,0xc0,
         0x60,0x30,0x18,0xc,0x6,0x83,0x41,0xa0,
         0x50,0x28,0x14,0xa,0x85]

ciphertext = open('encrypted_flag','rb').read()
key = open('key','r').read()

v7 = ""
for a in range(len(ands)):
    v7 += chr(ands[a] & ord(key[a]))

plaintext = ""
for a in range(len(v7)):
    plaintext += chr(ord(ciphertext[a]) - ord(v7[a]))   

print plaintext
```

When we run the code we get the flag:

```
root@kali:~/auscert/unbreakable# ./decrypt.py 
flag{STr3am_c1ph3rs_r_Gr3at}
```
