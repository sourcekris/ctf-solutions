#!/usr/bin/python

from pwn import *
import itertools
import os

BINARY="./r200"		# name of the original binary file
PATCHLOC=0x400880	# location to patch
PATCHVAL='\xeb'		# what to patch with, 0xeb = jmp

CMPLOC="0x40082e"

alphabet = list("_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUFWXYZ1234567890!@#$%^&*()-=+:<>")

passsofar = ""

gdbscripttop =  "set width 0\n"
gdbscripttop += "set height 0\n"
gdbscripttop += "set verbose off\n"
gdbscripttop += "pset option ansicolor off\n"
gdbscripttop += "br *"+CMPLOC+"\n"
gdbscripttop += "r\n"

gdbscriptend = "quit\n"

# patch out the anti-debug
print "[+] Patching binary..."
e = ELF(BINARY)
e.write(PATCHLOC, PATCHVAL)
e.save(BINARY + ".patched")
os.chmod(BINARY + ".patched",755)

print "[+] Brute Forcing password..."
while len(passsofar) <= 21:
	for j in itertools.product(alphabet, repeat=1):
		found = 0
		linenum = 0 

		f=open(BINARY+".gdb","w")
		f.write(gdbscripttop)
		for x in range(len(passsofar)):
			f.write("c\n")
		f.write(gdbscriptend)
		f.close()

		with open(os.devnull, 'w') as devnull:
			p = subprocess.check_output("echo "+passsofar+"".join(j)+" | gdb --command="+BINARY+".gdb ./"+BINARY+".patched",shell=True,stderr=devnull)
		for line in p.splitlines():
			if "RAX" in line:
				rax = line.split()
				linenum+=1
			if "RDX" in line:
				rdx = line.split()
				linenum+=1

		if rax[1] == rdx[1]:
			print "[+] Password so far: " + passsofar + "".join(j)	
			passsofar += "".join(j)
			found = 1

		if found > 0:
			break
