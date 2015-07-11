#!/usr/bin/python

from pwn import *
import hashlib, itertools

# list of combinations of plaintext possibly
pool = ('ikon', 'ionk', 'inok','onik','oink','nino','nini', 'niko', 'koni', 'koin', 'kino', 'niok', 'noik','noki','niko',);

# iterate through the combinations
for findsalt in itertools.product(pool, repeat = 3):
	plaintext = '{}{}{}'.format(*findsalt)
	conn = remote('localhost',8888)
	#conn = remote('146.148.79.13',8888)
	task = conn.recvline()
	line = task.split()
	proof = line[25]
	print "Got challenge ("+proof+"). Brute forcing a response..."
	charset = ''.join( [ chr( x ) for x in xrange( 0, 128 ) ] )
	found = False
	for comb in itertools.combinations( charset, 5 ):
	    test = proof + ''.join( comb )
	    ha=hashlib.sha1()
	    ha.update( test )
	    if ( ord( ha.digest()[ -1 ] ) == 0x00 and
		    ord( ha.digest()[ -2 ] ) == 0x00):
		found = True
		break

	if not found:
	    print 'Could not find string =('
	    quit()

	print "Responding to challenge..."
	conn.send(test)
	conn.sendafter(':', plaintext + "\n")
	encrypted = conn.recvline()
	line = encrypted.split()
	print "Plaintext "+plaintext+" encrypted is "+line[3]
	conn.close()
