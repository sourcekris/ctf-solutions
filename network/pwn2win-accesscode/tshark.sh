#!/bin/bash
tshark -i eth0 -Tfields -e tcp.dstport src host 104.236.81.9 and portrange 99-800 2> /dev/null > ports.txt

