Insomnihack Teaser 2016 – Bring the noise – Crypto – 200 pts
------------------------------------------------------------
Great challenge! Connecting to the server seen we’re given a challenge. This is a standard challenge/response scenario designed just to prevent rapid brute force attacks against the server. We solve it quickly with itertools and move forward to the real problem.

Past the initial challenge response, we’re given set of 40 lists of seven integers per list. Upon inspection of the server source code which we’re also given, we see that what we have is a list of 40 coefficients and the result of a multiplication of those coefficients (mod 8) and a randomly chosen single solution. Additionally a “vibration” is factored in in such a way that it can vary the result +/- 1.

My solution was to simply split the coefficients in the input and iterate (again, thanks itertools!) through all possible solutions searching for a solution that best fits the value in the results field (give or take 1). The math we can re-use straight from the server code so very little hard stuff to do here.

A good fit is anything that met > 30 of the 40 equations given to us by the server. This seemed to be good enough because my solution worked each time I tried it.

See solve.py in this repo.

Which, when run, results in the flag below:

```
root@ubuntu:~/insomnihack/bringnoise# ./solve.py 
[+] Opening connection to bringthenoise.insomnihack.ch on port 1111: Done
[*] Got challenge: 2f58a
[*] Sending challenge response: a505f
[*] Received equation sets. Computing candidate solutions...
[+] (0, 2, 7, 2, 7, 3) Satisfied 33 equations
[+] Got flag: INS{ErrorsOccurMistakesAreMade}
```

