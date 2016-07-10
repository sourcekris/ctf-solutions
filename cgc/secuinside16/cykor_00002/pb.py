#!/usr/bin/python

bytelist = [x.strip() for x in open('bytes.txt','r').readlines()]

lin = open('linear_eqs.py','w')
lin.write("#!/usr/bin/python\nfrom z3 import *\n")

for i in range(26):
    lin.write("var_"+str(i)+" = Int('var_"+str(i)+"')\n")

lin.write("solve(")

def replacelabel(bytenum):
    firstbyte = 0x805F454
    thisbyte = int(bytenum.split("_")[1],16)
    intnum = thisbyte - firstbyte
    return("var_" + str(intnum))

block = []
for line in bytelist:
    if "=" in line:
        block.append(replacelabel(line.split()[0]))
        lin.write(' + '.join(block)+" == "+line.split()[2]+",")
        block = []
    elif "byte_" in line:
        block.append(replacelabel(line))
     
lin.write(")")
lin.close()

