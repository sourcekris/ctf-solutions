#!/usr/bin/python

nifs = [x.strip() for x in open('ifs.txt','r').readlines()]

print "from z3 import *"

# build a set of variable names for the pointer+offset syntax search and replace
repl = [ "var_0 *a1" ]
offset = 4
for i in range(1,14):
    repl.append("var_"+str(i)+" *(a1 + "+str(offset)+")")
    offset += 4
    # while were hear print variable declarations for the z3
    print "var_"+str(i-1)+" = Int('var_"+str(i-1)+"')"

ifblocks = []
subblock = []
for n in nifs:
    if 'if (' in n: 
        if len(subblock) > 0:
            ifblocks.append(subblock)
        subblock = []
        subblock.append(n)
    else:
        if '{' not in n:
            subblock.append(n)

# do the find and replace 
for n in range(len(ifblocks)):
    for m in range(len(ifblocks[n])):
        for o in repl:
            data, pointer = o.split(' ',1)
            if pointer in ifblocks[n][m]:
                ifblocks[n][m] = ifblocks[n][m].replace(pointer,data).replace('if','').replace('(','').replace(')',',')

# output the 
solution = 'solve('
for i in ifblocks:
    solution += ' '.join(i).lstrip()
solution = solution.rstrip(', ') + ')'
print solution
