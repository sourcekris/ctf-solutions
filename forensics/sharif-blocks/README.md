# SharifCTF 2016 - Blocks - Forensics 400 Point Challenge

![blocks](https://ctf.rip/wp-content/uploads/2016/02/blocks.png) 

Good fun this one, and worth a lot of points also as I solved it very early. It involves a small file of "unknown" data which we're told is probably not complete in the clue. First things first let's grab the file and check it out: 
    
    
    root@kali:~/sharif/blocks# file data3
    data3: data
    

Ok that's of no help, what about strings: 
    
    
    root@kali:~/sharif/blocks# strings data3 | head -7
    tabledatadata
    CREATE TABLE "data" (
    	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    	`Data`	BLOB NOT NULL,
    	`Cat`	INTEGER NOT NULL
    indexsqlite_autoindex_data_1data
    Ytablesqlite_sequencesqlite_sequence
    

Ok probably SQLite3 file then? Let's try! 
    
    
    root@kali:~/sharif/blocks# sqlite3 data3
    SQLite version 3.9.2 2015-11-02 18:31:45
    Enter ".help" for usage hints.
    sqlite> select table_name from information_schema.tables;
    Error: file is encrypted or is not a database
    

Nope. How about repairing it? 
    
    
    root@kali:~/sharif/blocks# sqlite3 data3 "PRAGMA integrity_check"
    Error: file is encrypted or is not a database
    

No, it's just too messed up? Let's look at the [SQLite file format](https://www.sqlite.org/fileformat2.html)... The file should have the magic bytes "SQLite format 3\x00". Our file has this: 
    
    
    oot@kali:~/sharif/blocks# xxd -l 16 data3
    00000000: 2033 0004 0001 0100 4020 2000 0000 0b00   3......@  .....
    

So we've got a 0x20 (Space), 3, Null. Looks a lot like the ending of the proper file header, let's stick some bytes on the front and see if we can load it... 
    
    
    root@kali:~/sharif/blocks# python
    Python 2.7.11 (default, Jan 11 2016, 21:04:40) 
    [GCC 5.3.1 20160101] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> open('fixed','wb').write("SQLite format" + open('data3','rb').read())
    >>> quit()
    root@kali:~/sharif/blocks# file fixed
    fixed: SQLite 3.x database
    root@kali:~/sharif/blocks# sqlite3 fixed "PRAGMA integrity_check"
    ok
    

Sweet. What lies within this then? I found a tool called sqlitebrowser installed. It's a bit cool. With it we can browse the structure of the SQLite db file graphically. That helped come up with a strategy for me: This is the main UI for the browser, you can see the file loaded pretty successfully. 

![sqlite1](https://ctf.rip/wp-content/uploads/2016/02/sqlite1.png) 

In the data browser we see what the deal is. One table has common PNG header values as category names... 

![sqlite2](https://ctf.rip/wp-content/uploads/2016/02/sqlite2.png) 

And in the Data table, we have binary blobs with category fields which relate them back to the Category table in accordance to what PNG chunk they belong to. 

![sqlite3](https://ctf.rip/wp-content/uploads/2016/02/sqlite3.png) 

So pretty much this looks straightforward for IHDR, PLTE, tRNS chunks. However the IDAT chunk (the actual image data) is split into multiple 270ish byte chunks and deposited into the database. And yes, before you ask, the blob's are in random order. So we have a total of 11 chunks of image data in a completely random order. Leaving us with a totally massive number of possible image data permutations. Let's see if there's any hints in the blob data to see if we can reduce the permutations. Firstly, below is the 5th row blob data. It begins with an "x" character which I often see as the first byte in IDAT chunks in PNG images. So let's try placing that first. 

![sqlite4](https://ctf.rip/wp-content/uploads/2016/02/sqlite4.png) 

Next I see the final row 14 blob data is 270 bytes while all other blobs are 274 bytes. This could mean it's the final block. Upon further inspection it contains a few null bytes towards the end, further cementing the idea this is the final blob in the IDAT chunk. 

![sqlite5](https://ctf.rip/wp-content/uploads/2016/02/sqlite5.png) 

This leaves us with 9 x 9 x 9 x 9 x 9 x 9 x 9 x 9 x 9 permutations of PNG file these could add up to. How else can we work on this problem? I figured that PNG data is compressed and so attempting to decompress a permutation of the data blobs should yield either an exception or a successful decompression. I implemented this theory in some Python code but found zero solutions resulted in successful decompression. So perhaps more work was needed on that theory. In order to just move forward with the challenge, I decided to write some Python code that will generate PNG image candidates which I can quickly review in Windows explorer thumbnail view for likely candidates. I've done a challenge like this before so I knew that it would "work". I used this code with a itertools.permutations() with the r value set to 9 for about 360,000 PNGs. With a very fast SSD this was actually no big deal to quickly scroll through for candidates. On the 327,600 image I found that blocks 2 & 3 were aligned and I saw a partial flag image (I could read** SharifCTF{6**). This reduced the permutations needed down to an "r" value of 7 so I added these block markers into the Python code. 
    
    
    #!/usr/bin/python
    
    import sqlite3
    import binascii
    import struct
    import itertools
    
    # limit the number of candidate PNGs to this
    LIMIT = 3100
    
    print "[*] Fixing the SQLite file..."
    orig = "SQLite format"
    orig += open('data3','rb').read()
    open('data3.sqlite','wb').write(orig)
    
    print "[*] Extracting the PNG Data from SQLite DB..."
    conn = sqlite3.connect('data3.sqlite')
    cursor = conn.cursor()
    
    # PNG Magic bytes
    png = "\x89PNG\x0d\x0a\x1a\x0a\x00\x00\x00\x0d"
    
    # get IHDR first
    ihdr = "IHDR" 
    cursor.execute("SELECT Data FROM data WHERE Cat = 4")
    ihdr += str(cursor.fetchone()[0])
    ihdr += "\x89\xb8\x68\xee\x00\x00\x03\x00" # CRC32
    
    # Next the PLTE
    plte = "PLTE"
    cursor.execute("SELECT Data FROM data WHERE Cat = 7")
    plte += str(cursor.fetchone()[0])
    plte += "\xe2\xb0\x5d\x7d\x00\x00\x00\x02"
    
    # Next the tRNS
    trns = "tRNS"
    cursor.execute("SELECT Data FROM data WHERE Cat = 8")
    trns += str(cursor.fetchone()[0])
    trns += "\xe5\xb7\x30\x4a\x00\x00\x0b\xc3"
    
    # finally the IDAT
    idat = "IDAT"
    cursor.execute("SELECT Data FROM data WHERE Cat = 2")
    
    puzzle = []
    known  = [None] * 11
    for row in cursor.fetchall():
    	if str(row[0])[0] == "\x78":		# known 1st block
    		known[0] = str(row[0])		
    	elif str(row[0])[0] == "\x5c":		# learned 2nd block
    		known[1] = str(row[0])		
    	elif str(row[0])[0] == "\x13":		# learned 3rd block
    		known[2] = str(row[0])		
    	elif len(str(row[0])) == 270:		# known final block
    		known[10] = str(row[0])		
    	else:
    		puzzle.append(str(row[0]))
    
    idat += "".join(known[0:3])
    
    # define an IEND for later
    iend = "IEND" + "\xae\x42\x60\x82"
    
    print "[*] Building potential flag PNGs..."
     
    counter = 0
    for i in itertools.permutations(puzzle, 7):
    
    	if counter > LIMIT:
    		quit()
    
    	image = idat + "".join(i)
    	image += known[10]
    	image += "\x08\x8d\x8d\xb6\x00\x00\x00\x00"
    	open(str(counter).zfill(6) + '.png','wb').write(png + ihdr + plte + trns + image + iend)
    	counter += 1
    	
After just 3046 more PNGs I had the flag so I stopped looking for other ways to solve this:

![3046](https://ctf.rip/wp-content/uploads/2016/02/003046.png) 
