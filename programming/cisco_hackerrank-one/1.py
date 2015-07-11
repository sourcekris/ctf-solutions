import sys

key = sys.stdin.readline().strip()
input = sys.stdin.readline().strip().decode('hex')

output = ""

for i in range(len(input)):
    output += chr(ord(input[i]) ^ ord(key[i%len(key)]))
    
sys.stdout.write(output)
