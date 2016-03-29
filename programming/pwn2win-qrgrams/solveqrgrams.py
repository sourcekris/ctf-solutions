#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pwn import *
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from qrtools import QR
import sys
import re

host = 'pool.pwn2win.party'
port = 31337

font = ImageFont.truetype('clacon.ttf',16)

dictionary = open("/usr/share/wordlists/english.txt","r").readlines()
dictionary = [x.strip() for x in dictionary]

tmpfile = "qrimg-"

def qrimg(lines,filename):
    lines = unicode(lines, "utf-8")
    img=Image.new("RGBA", (380,380),(255,255,255))
    draw = ImageDraw.Draw(img)
    y_text =8 
    for line in lines.splitlines():
        width, height = font.getsize(line)
        draw.text((10,y_text),line,(0,0,0), font=font)
        y_text +=height
        draw = ImageDraw.Draw(img)
    #img = img.resize((380,420))
    img.save(filename)
    thedata = QR(filename=filename)
    if thedata.decode():
        return thedata.data
    else:
        return "Error: " + filename + " "

def get_words(text):
    return text.split()

def get_possible_words(words,jword):
    possible_words = []
    jword_length = len(jword)
    for word in words:
        jumbled_word = jword
        if len(word) == jword_length:
            letters = list(word)
            for letter in letters:
                if jumbled_word.find(letter) != -1:
                    jumbled_word = jumbled_word.replace(letter,'',1)
            if not jumbled_word:
                possible_words.append(word)
    return possible_words 

while True:
    conn = remote(host,port)
    print "[*] Downloading QR codes..."
    inputqrs = conn.recvuntil('Phrase?').split("\n\n")
    inputqrs.pop(-1) # pop "Phrase?" off the end

    counter   = 0 
    phrase    = ""

    # convert binary qrs to blocks
    for qr in inputqrs:
        if '100' in qr:
            qr = qr.replace('1','██').replace('0','  ')
        else:
            outbuf = ""
            last = 0
            for line in qr.splitlines():
                ansis = line.split("  ")
                for a in ansis:
                    if '7m' in a:
                        outbuf += '  '   
                        last = 7
                    elif '49m' in a:
                        outbuf += '██'
                        last = 49
                        
                    elif '0m' in a:
                        if last == 49:
                            outbuf += '██'
                        else:
                            outbuf += ' '
                outbuf += '\n'
            qr = outbuf

        phrase += qrimg(qr, tmpfile + str(counter).zfill(2) + ".png") + " "
        counter += 1

    print "[?] Decipher: " + phrase
    print "[*] Searcing for possible words..."
    newphrase = ""
    had_cap = False

    for word in get_words(phrase):

        had_cap   = False
        had_comma = False
        had_point = False
        had_exla  = False

        if re.search('[A-Z]',word):
            had_cap = True

        if re.search(',',word):
            had_comma = True

        if re.search('\.',word):
            had_point = True

        if re.search('!',word):
            had_exla = True

        word = word.lower()
        word = re.sub('[^A-Za-z\']','',word)
        possible = get_possible_words(dictionary, word) 
        try:
            newword = possible[0]
            if had_cap:
                newword = newword.capitalize()

            newphrase += newword
            
            if had_comma:        
                newphrase += ","
            if had_point:
                newphrase += "."
            if had_exla:
                newphrase += "!"

            newphrase += " "
        except IndexError:
            pass
        
    newphrase += get_words(phrase)[-2] + " "
    newphrase += get_words(phrase)[-1]
    newphrase = newphrase.strip()

    print "[?] Deciphered: " + newphrase
            
    conn.sendline(newphrase)
    result = conn.recvline()
    if 'Wrong Phrase' not in result:
        print "[+] Flag: " + result
        conn.close()
        quit()
    else:
        print "[-] Phrase not right, let's try again !"
