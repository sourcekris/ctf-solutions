#!/usr/bin/python

import subprocess
import shutil

filename = "secret"

while True:
	format = subprocess.check_output(["file", filename])
	
	if '7-zip archive' in format:
		print "[+] Extracting 7-zip..."
		shutil.move(filename, filename + ".7z")
		subprocess.call(["7z","e",filename + ".7z"])	
	elif 'Microsoft Cabinet archive' in format:
		print "[+] Extracting Cab..."
		shutil.move(filename, filename + ".cab")
		subprocess.call(["cabextract",filename + ".cab"])	
	elif 'bzip2 compressed data' in format:
		print "[+] Extracting bz2..."
		shutil.move(filename, filename + ".bz2")
		subprocess.call(["bunzip2",filename + ".bz2"])	
	elif 'PPMD archive' in format:
		print "[+] Extracting ppmd..."
		shutil.move(filename, filename + ".ppmd")
		subprocess.call(["ppmd","d",filename + ".ppmd"])	
	elif 'POSIX tar archive' in format:
		print "[+] Extracting tar..."
		shutil.move(filename, filename + ".tar")
		subprocess.call(["tar","xvf",filename + ".tar"])	
	elif 'XZ compressed' in format:
		print "[+] Extracting xz..."
		shutil.move(filename, filename + ".xz")
		subprocess.call(["unxz",filename + ".xz"])	
	elif 'ARC archive data' in format:
		print "[+] Extracting ARC..."
		shutil.move(filename, filename + ".arc")
		subprocess.call(["arc","x",filename + ".arc"])	
	elif 'KGB Archiver file' in format:
		print "[+] Extracting KGB..."
		shutil.move(filename, filename + ".kgb")
		subprocess.call(["kgb",filename + ".kgb"])	
	elif 'ARJ archive' in format:
		print "[+] Extracting ARJ..."
		shutil.move(filename, filename + ".arj")
		subprocess.call(["arj","e", filename + ".arj"])	
	elif 'rzip compressed' in format:
		print "[+] Extracting rzip..."
		shutil.move(filename, filename + ".rz")
		subprocess.call(["rzip","-d", filename + ".rz"])	
	elif 'gzip compressed' in format:
		print "[+] Extracting gzip..."
		shutil.move(filename, filename + ".gz")
		subprocess.call(["gunzip",filename + ".gz"])	
	elif 'Zip archive data' in format:
		print "[+] Extracting Zip..."
		shutil.move(filename, filename + ".zip")
		subprocess.call(["unzip",filename + ".zip"])	
	elif 'Zoo archive' in format:
		print "[+] Extracting Zoo..."
		shutil.move(filename, filename + ".zoo")
		subprocess.call(["zoo","-extract",filename + ".zoo"])	
	elif 'RAR archive' in format:
		print "[+] Extracting Rar..."
		shutil.move(filename, filename + ".rar")
		subprocess.call(["unrar","e",filename + ".rar"])	
	else:
		print "[+] Unknown format: " + format
		quit()
