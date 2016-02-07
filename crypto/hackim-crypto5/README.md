
# HackIM 2016 - Crypto 5 - 500 Point Challenge

![crypto500clue](https://ctf.rip/wp-content/uploads/2016/01/crypto500clue.png) 

I don't really want to get into all of the commentary surrounding HackIM as a CTF. I do recommend if you're interested to know whether HackIM should even be rated on CTFTime [you should read the comments there](https://ctftime.org/event/285). I agree with the comments there for the most part. This was a 500 point challenge in the cryptography category. This one was interesting to me as it involved RSA public key encryption but I felt pretty deflated after solving it. The other cryptography questions were as simple as this and involved at maximum, brute forcing XOR ciphers to recover plaintext. The trick is that we have all of the public keys we need to try and open the file, we just need to find the 1 in 50 that works. That is done programatically with this script: 
    
    
    #!/usr/bin/python
    import subprocess
    
    allkeys = open('all_keys.txt','r').readlines()
    
    print "[*] Decrypting warrior.txt with all keys..."
    for i in range(0,len(allkeys),9):
    	buf = "".join(allkeys[i:i+9])
    	open('tmpkey','w').write(buf)
    	decrypted = subprocess.check_output(['openssl','rsautl','-pubin','-in','warrior.txt','-inkey','tmpkey','-verify','-raw'],stderr=subprocess.STDOUT)
    
    	if 'fighter' in decrypted:
    		print "[+] Flag: " + decrypted
    		break
    

Which gives us the "flag" text: 
    
    
    root@kali:~/hackim/crypto/5# ./useopenssl.py 
    [*] Decrypting warrior.txt with all keys...
    [+] Flag: This fighter is a designation for two separate, heavily upgraded derivatives of the Su-35 'Flanker' jet plane. They are single-seaters designed by Sukhoi(KnAAPO).
    

Which when we google, gives us the flag of "Sutkhoi Su-35".

