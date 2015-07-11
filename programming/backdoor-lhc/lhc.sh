#!/bin/bash
 
rm data.txt
curl -s -r 1099999999978-1100000000042 -o data.txt http://lhc-cdn.herokuapp.com/data.txt
echo "Flag: "`cat data.txt`
rm data.txt
