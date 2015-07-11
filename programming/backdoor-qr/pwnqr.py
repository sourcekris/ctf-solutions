#!/usr/bin/python

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import qrcode
from pwn import *

def qrimg(lines,filename):
	font = ImageFont.truetype('clacon.ttf')
	img=Image.new("RGBA", (380,380),(255,255,255))
	draw = ImageDraw.Draw(img)
	y_text =8 
	for line in lines:
		line = unicode(line, "utf-8")
		width, height = font.getsize(line)
		draw.text((0,y_text),line,(0,0,0), font=font)
		y_text +=height
		draw = ImageDraw.Draw(img)
	img.save(filename)

conn = remote('hack.bckdr.in',8010)
for messagenum in range(1,100+1):
	input = conn.recvlines(47)
	print "[+] Got challenge number " + str(messagenum)
	qrimg(input, "qrtmp.png")
	thedata = qrcode.Decoder()
	if thedata.decode("qrtmp.png"):
		conn.send(thedata.result)

flag = conn.recvall()
print "Flag message: " + flag
conn.close()
